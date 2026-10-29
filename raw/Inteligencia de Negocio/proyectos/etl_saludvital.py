"""
ETL SaludVital: Excel (7 hojas) -> Staging -> Data Mart (DIM_* / FACT_*) en CSV para Power BI.
Sigue la documentación del proyecto (secciones 3, 5, 6 y 7).

Uso:  python etl_saludvital.py
Requiere: pandas, openpyxl
"""
import re
import sys
import unicodedata
from datetime import datetime, date, time
from pathlib import Path

import pandas as pd

# ------------------------------------------------------------------ CONFIG
ARCHIVO = Path("SaludVital_BaseDatos.xlsx")
SALIDA = Path("datamart")           # CSV finales (se cargan en Power BI)
SALIDA_STG = Path("staging")        # copia fiel del origen + auditoría
SALIDA_CTRL = Path("control")       # logs y cuarentena
GUARDAR_STAGING = True

# Seed RN01/RN02: nombre maestro por EspecialidadID (deducido de 04_PRESTACIONES)
MAP_ESPECIALIDAD = {
    "E01": "Medicina General", "E02": "Pediatría", "E03": "Traumatología",
    "E04": "Ginecología", "E05": "Cardiología", "E06": "Dermatología",
    "E07": "Neurología", "E08": "Oftalmología", "E09": "Endocrinología",
    "E10": "Kinesiología",
}
# Alias -> nombre maestro (claves ya normalizadas)
MAP_ALIAS_ESPECIALIDAD = {
    "trauma": "Traumatología", "traumatologia": "Traumatología",
    "medicina general": "Medicina General", "pediatria": "Pediatría",
}
ESTADOS = {1: "Atendida", 2: "Cancelada", 3: "No asistió", 4: "Pendiente"}

# ------------------------------------------------------------------ UTILIDADES
FECHA_EJEC = datetime.now()
ERROR_LOG = []          # ETL_ERROR_LOG
QUARANTINE = {}         # nombre -> lista de DataFrames


def normalizar(s):
    """minúsculas, sin tildes, sin puntuación, espacios colapsados (RN02/RN03)."""
    if pd.isna(s):
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def clave_paciente(nombre):
    """Nombre normalizado sin iniciales sueltas: 'juan a perez' -> 'juan perez'."""
    return " ".join(t for t in normalizar(nombre).split() if len(t) > 1)


def log(tabla, campo, valor, codigo, severidad, accion):
    ERROR_LOG.append({
        "Tabla": tabla, "Campo": campo, "ValorOriginal": valor, "CodigoDQ": codigo,
        "Severidad": severidad, "Accion": accion, "Fecha": FECHA_EJEC.isoformat(timespec="seconds"),
    })


def cuarentena(nombre, df, codigo):
    if df is not None and len(df):
        d = df.copy()
        d["CodigoDQ"] = codigo
        QUARANTINE.setdefault(nombre, []).append(d)


def critico(msg):
    log("-", "-", msg, "CRITICA", "Crítica", "Ejecución detenida")
    volcar_control("Con errores", 0, 0, 0)
    sys.exit(f"[CRÍTICO] {msg}")


def a_fecha(serie):
    return pd.to_datetime(serie, errors="coerce")


def a_hhmm(v):
    if pd.isna(v):
        return None
    if isinstance(v, (time, datetime, pd.Timestamp)):
        return v.strftime("%H:%M")
    if isinstance(v, (int, float)):          # fracción de día de Excel
        m = round(float(v) * 24 * 60)
        return f"{m // 60 % 24:02d}:{m % 60:02d}"
    t = pd.to_datetime(str(v), errors="coerce")
    return None if pd.isna(t) else t.strftime("%H:%M")


def guardar(df, carpeta, nombre):
    carpeta.mkdir(exist_ok=True)
    df.to_csv(carpeta / f"{nombre}.csv", index=False, encoding="utf-8-sig")


# ------------------------------------------------------------------ 1-2. ORIGEN Y EXTRACCIÓN
def extraer():
    if not ARCHIVO.exists():
        critico(f"No se encontró el archivo origen: {ARCHIVO}")
    hojas = ["01_PACIENTES", "02_MEDICOS", "03_ESPECIALIDADES", "04_PRESTACIONES",
             "05_RESERVAS", "06_ATENCIONES", "07_DETALLE_ATENCION"]
    xl = pd.ExcelFile(ARCHIVO)
    faltan = [h for h in hojas if h not in xl.sheet_names]
    if faltan:
        critico(f"Hojas faltantes: {faltan}")

    stg = {}
    for h in hojas:
        df = xl.parse(h)
        df.columns = [str(c).strip() for c in df.columns]
        # DQ02: columnas 100% nulas / 'Unnamed'
        for c in [c for c in df.columns if c.startswith("Unnamed") and df[c].isna().all()]:
            log(h, c, "100% nula", "DQ02", "Informativa", "Excluida en la extracción")
            df = df.drop(columns=c)
        # Normalizar IDs (mayúsculas, sin espacios)
        for c in [c for c in df.columns if c.endswith("ID")]:
            df[c] = df[c].astype("string").str.strip().str.upper()
        df.insert(0, "NroFila", range(2, len(df) + 2))
        df["FechaCarga"] = FECHA_EJEC.isoformat(timespec="seconds")
        df["ArchivoOrigen"] = ARCHIVO.name
        stg[h] = df
        if GUARDAR_STAGING:
            guardar(df, SALIDA_STG, "STG_" + h[3:])
    # DQ01: 03_ESPECIALIDADES es copia de 02_MEDICOS -> se lee pero no se usa
    cols = ["MedicoID", "Medico", "EspecialidadID"]
    if all(c in stg["03_ESPECIALIDADES"].columns for c in cols) and \
            stg["03_ESPECIALIDADES"][cols].reset_index(drop=True).equals(
                stg["02_MEDICOS"][cols].reset_index(drop=True)):
        log("03_ESPECIALIDADES", "*", "Copia exacta de 02_MEDICOS", "DQ01", "Informativa",
            "Descartada; DIM_ESPECIALIDAD se construye desde 04_PRESTACIONES")
    return stg


# ------------------------------------------------------------------ 3. LIMPIEZA + DIMENSIONES
def pk_duplicada(df, col, tabla):
    d = df[df.duplicated(col, keep=False)]
    if len(d):
        critico(f"PK duplicada en {tabla}.{col}: {d[col].tolist()}")


def dim_especialidad(prest):
    ids = sorted(prest["EspecialidadID"].dropna().unique())
    filas = []
    for i, eid in enumerate(ids, start=1):
        nombre = MAP_ESPECIALIDAD.get(eid)
        if nombre is None:
            critico(f"EspecialidadID '{eid}' sin nombre en MAP_ESPECIALIDAD")
        # RN02: si el nombre maestro coincide con un alias, se resuelve al maestro
        nombre = MAP_ALIAS_ESPECIALIDAD.get(normalizar(nombre), nombre)
        filas.append({"EspecialidadKey": i, "EspecialidadID": eid, "NombreEspecialidad": nombre})
    d = pd.DataFrame(filas)
    if len(d) != 10:
        log("DIM_ESPECIALIDAD", "-", f"{len(d)} especialidades (esperadas 10)", "RN01", "Advertencia", "Revisar")
    return d


def dim_medico(med, d_esp):
    d = med.copy()
    d["Nombre"] = d["Medico"].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
    d = d.merge(d_esp[["EspecialidadID", "EspecialidadKey"]], on="EspecialidadID", how="left")
    d.insert(0, "MedicoKey", range(1, len(d) + 1))
    d = d[["MedicoKey", "MedicoID", "Nombre", "EspecialidadID", "EspecialidadKey"]]
    desc = pd.DataFrame([{"MedicoKey": -1, "MedicoID": "N/A", "Nombre": "Médico desconocido",
                          "EspecialidadID": "N/A", "EspecialidadKey": -1}])
    return pd.concat([desc, d], ignore_index=True)


def dim_prestacion(prest, d_esp):
    d = prest.copy()
    d["ValorListado"] = pd.to_numeric(d["Valor"], errors="coerce")
    malos = d[d["ValorListado"].isna() | (d["ValorListado"] < 0)]
    for _, r in malos.iterrows():
        log("04_PRESTACIONES", "Valor", r["Valor"], "DQ11", "Error", "Cuarentena")
    cuarentena("QUARANTINE_PRESTACIONES", malos, "DQ11")
    d = d.drop(malos.index)
    d = d.merge(d_esp[["EspecialidadID", "EspecialidadKey"]], on="EspecialidadID", how="left")
    d = d.rename(columns={"Prestacion": "NombrePrestacion"})
    d.insert(0, "PrestacionKey", range(1, len(d) + 1))
    return d[["PrestacionKey", "PrestacionID", "NombrePrestacion", "EspecialidadID",
              "EspecialidadKey", "ValorListado"]]


def dim_estado():
    return pd.DataFrame({"EstadoKey": list(ESTADOS), "EstadoReserva": list(ESTADOS.values())})


def dim_tiempo(reservas):
    f = a_fecha(reservas["FechaReserva"]).dropna()
    ini, fin = date(f.min().year, 1, 1), date(f.max().year, 12, 31)
    dias = pd.date_range(ini, fin, freq="D")
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
             "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    sem = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return pd.DataFrame({
        "FechaKey": dias.strftime("%Y%m%d").astype(int),
        "Fecha": dias.date,
        "Día": dias.day, "Mes": dias.month,
        "NombreMes": [meses[m - 1] for m in dias.month],
        "Trimestre": dias.quarter, "Año": dias.year,
        "DiaSemana": [sem[d] for d in dias.dayofweek],
        "EsFinDeSemana": (dias.dayofweek >= 5).astype(int),
    })


def dim_paciente(pac):
    """Cuarentena de vacíos (DQ03) + deduplicación (RN03/DQ06). Devuelve (dim, MAP_PACIENTE)."""
    campos = [c for c in pac.columns if c not in ("PacienteID", "NroFila", "FechaCarga", "ArchivoOrigen")]
    vacios = pac[pac[campos].isna().all(axis=1)]
    for _, r in vacios.iterrows():
        log("01_PACIENTES", "PacienteID", r["PacienteID"], "DQ03", "Error", "Cuarentena; no se carga en DIM_PACIENTE")
    cuarentena("QUARANTINE_PACIENTES", vacios, "DQ03")
    p = pac.drop(vacios.index).copy()

    p["Nombre"] = p["Nombre"].astype("string").str.strip().str.replace(r"\s+", " ", regex=True).str.title()
    p["Comuna"] = p["Comuna"].astype("string").str.strip().str.title().fillna("Sin informar")
    p["FechaNacimiento"] = a_fecha(p["FechaNacimiento"])
    prev = p["Prevision"].astype("string").str.strip().str.upper()
    p["Previsión"] = prev.map({"FONASA": "Fonasa", "ISAPRE": "Isapre"}).fillna(prev.str.title())
    p["Sexo"] = p["Sexo"].astype("string").str.strip().str.upper().map(
        {"F": "Femenino", "M": "Masculino"})
    p["Edad"] = p["FechaNacimiento"].apply(
        lambda f: None if pd.isna(f) else
        FECHA_EJEC.year - f.year - ((FECHA_EJEC.month, FECHA_EJEC.day) < (f.month, f.day)))
    p["_clave"] = p["Nombre"].apply(clave_paciente)
    p["_completo"] = p[["Nombre", "Comuna", "FechaNacimiento", "Previsión", "Sexo"]].notna().sum(axis=1)

    # Agrupar por nombre completo normalizado; no fusionar si sexo o fecha de nacimiento contradicen
    sobrevivientes, equivalencia = [], {}
    for _, g in p.groupby("_clave"):
        g = g.sort_values(["_completo", "PacienteID"], ascending=[False, True])
        if len(g) == 1:
            sobrevivientes.append(g.iloc[0]); equivalencia[g.iloc[0]["PacienteID"]] = g.iloc[0]["PacienteID"]
            continue
        sexos = g["Sexo"].dropna().unique()
        fechas = g["FechaNacimiento"].dropna().unique()
        if len(sexos) > 1 or len(fechas) > 1:      # posibles homónimos -> revisión manual
            for _, r in g.iterrows():
                sobrevivientes.append(r); equivalencia[r["PacienteID"]] = r["PacienteID"]
            log("01_PACIENTES", "Nombre", g["PacienteID"].tolist(), "DQ06", "Advertencia",
                "Coincidencia parcial; revisión manual, no se fusiona")
        else:
            sob = g.iloc[0]
            sobrevivientes.append(sob)
            for _, r in g.iterrows():
                equivalencia[r["PacienteID"]] = sob["PacienteID"]
                if r["PacienteID"] != sob["PacienteID"]:
                    log("01_PACIENTES", "PacienteID", r["PacienteID"], "DQ06", "Corrección",
                        f"Consolidado en {sob['PacienteID']}")
    d = pd.DataFrame(sobrevivientes).sort_values("PacienteID").reset_index(drop=True)
    d.insert(0, "PacienteKey", range(1, len(d) + 1))
    d = d[["PacienteKey", "PacienteID", "Nombre", "Comuna", "FechaNacimiento", "Edad", "Previsión", "Sexo"]]
    key_por_id = dict(zip(d["PacienteID"], d["PacienteKey"]))
    mapa = {orig: key_por_id[sob] for orig, sob in equivalencia.items()}
    desc = pd.DataFrame([{"PacienteKey": -1, "PacienteID": "N/A", "Nombre": "Paciente desconocido",
                          "Comuna": "Sin informar", "FechaNacimiento": pd.NaT, "Edad": None,
                          "Previsión": "Sin informar", "Sexo": "Sin informar"}])
    return pd.concat([desc, d], ignore_index=True), mapa


# ------------------------------------------------------------------ 4-5. HECHOS
def fact_reservas(res, mapa_pac, d_med):
    r = res.copy()
    pk_duplicada(r, "ReservaID", "05_RESERVAS")
    r["_est"] = r["EstadoReserva"].apply(normalizar)
    cat = {normalizar(v): k for k, v in ESTADOS.items()}
    r["EstadoKey"] = r["_est"].map(cat)
    r["Fecha"] = a_fecha(r["FechaReserva"])
    r["Hora"] = r["HoraReserva"].apply(a_hhmm)

    # DQ04 estado fuera de catálogo / DQ12 fecha-hora inválida
    mal_estado = r[r["EstadoKey"].isna()]
    mal_fecha = r[r["Fecha"].isna() | r["Hora"].isna()]
    for _, x in mal_estado.iterrows():
        log("05_RESERVAS", "EstadoReserva", x["EstadoReserva"], "DQ04", "Error", "Cuarentena")
    for _, x in mal_fecha.iterrows():
        log("05_RESERVAS", "FechaReserva/HoraReserva", f"{x['FechaReserva']} {x['HoraReserva']}",
            "DQ12", "Error", "Cuarentena")
    cuarentena("QUARANTINE_RESERVAS", mal_estado, "DQ04")
    cuarentena("QUARANTINE_RESERVAS", mal_fecha, "DQ12")
    r = r.drop(mal_estado.index.union(mal_fecha.index))

    r["PacienteKey"] = r["PacienteID"].map(mapa_pac)
    r["MedicoKey"] = r["MedicoID"].map(dict(zip(d_med["MedicoID"], d_med["MedicoKey"])))
    for col, k in (("PacienteID", "PacienteKey"), ("MedicoID", "MedicoKey")):
        for _, x in r[r[k].isna()].iterrows():
            log("05_RESERVAS", col, x[col], "DQ08", "Error", "Clave -1 asignada")
        r[k] = r[k].fillna(-1).astype(int)
    r["EstadoKey"] = r["EstadoKey"].astype(int)
    r["FechaKey"] = r["Fecha"].dt.strftime("%Y%m%d").astype(int)
    r["EsAtendida"] = (r["EstadoKey"] == 1).astype(int)
    r["EsInasistencia"] = (r["EstadoKey"] == 3).astype(int)
    r = r.rename(columns={"Hora": "HoraReservaHHMM"})
    return r[["ReservaID", "PacienteKey", "MedicoKey", "EstadoKey", "FechaKey",
              "HoraReservaHHMM", "EsAtendida", "EsInasistencia"]]


def fact_prestaciones(stg, f_res, mapa_pac, d_med, d_prest, d_esp):
    det, aten, res = stg["07_DETALLE_ATENCION"].copy(), stg["06_ATENCIONES"].copy(), stg["05_RESERVAS"].copy()
    prest = stg["04_PRESTACIONES"]
    pk_duplicada(det, "DetalleID", "07_DETALLE_ATENCION")
    pk_duplicada(aten, "AtencionID", "06_ATENCIONES")

    # DQ09: reserva Atendida <-> existe atención
    atendidas = set(f_res.loc[f_res["EsAtendida"] == 1, "ReservaID"])
    for rid in sorted(atendidas - set(aten["ReservaID"])):
        log("05_RESERVAS", "ReservaID", rid, "DQ09", "Error", "Reserva Atendida sin atención")
    aten["FechaAten"] = a_fecha(aten["FechaAtencion"])
    mal = aten[aten["FechaAten"].isna()]
    for _, x in mal.iterrows():
        log("06_ATENCIONES", "FechaAtencion", x["FechaAtencion"], "DQ12", "Error", "Cuarentena")
    cuarentena("QUARANTINE_ATENCIONES", mal, "DQ12")
    aten = aten.drop(mal.index)
    fuera = aten[~aten["ReservaID"].isin(atendidas)]
    for _, x in fuera.iterrows():
        log("06_ATENCIONES", "ReservaID", x["ReservaID"], "DQ09", "Error",
            "Atención cuya reserva no está Atendida; excluida")
    aten = aten[aten["ReservaID"].isin(atendidas)]

    df = det.merge(aten[["AtencionID", "ReservaID", "FechaAten"]], on="AtencionID", how="left")
    sin_aten = df[df["ReservaID"].isna()]
    for _, x in sin_aten.iterrows():
        log("07_DETALLE_ATENCION", "AtencionID", x["AtencionID"], "DQ08", "Error", "Detalle excluido (sin atención válida)")
    cuarentena("QUARANTINE_DETALLE", sin_aten, "DQ08")
    df = df.dropna(subset=["ReservaID"])

    df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce")
    df["ValorUnitario"] = pd.to_numeric(df["ValorUnitario"], errors="coerce")
    mal = df[(df["Cantidad"].isna()) | (df["Cantidad"] <= 0) | (df["ValorUnitario"].isna()) | (df["ValorUnitario"] < 0)]
    for _, x in mal.iterrows():
        log("07_DETALLE_ATENCION", "Cantidad/ValorUnitario", f"{x['Cantidad']}/{x['ValorUnitario']}", "DQ11", "Error", "Cuarentena")
    cuarentena("QUARANTINE_DETALLE", mal, "DQ11")
    df = df.drop(mal.index)

    df = df.merge(res[["ReservaID", "PacienteID", "MedicoID"]], on="ReservaID", how="left")
    df = df.merge(prest[["PrestacionID", "EspecialidadID", "Valor"]], on="PrestacionID", how="left")
    df = df.merge(d_med[["MedicoID", "EspecialidadID"]].rename(columns={"EspecialidadID": "EspMedico"}),
                  on="MedicoID", how="left")

    # DQ10 precio distinto del maestro; DQ13 especialidad prestación != médico
    for _, x in df[df["ValorUnitario"] != pd.to_numeric(df["Valor"], errors="coerce")].iterrows():
        log("07_DETALLE_ATENCION", "ValorUnitario", f"{x['DetalleID']}: {x['ValorUnitario']} vs {x['Valor']}",
            "DQ10", "Advertencia", "Cargado con ValorUnitario")
    for _, x in df[df["EspecialidadID"] != df["EspMedico"]].iterrows():
        log("07_DETALLE_ATENCION", "EspecialidadID", f"{x['DetalleID']}: prestación {x['EspecialidadID']} vs médico {x['EspMedico']}",
            "DQ13", "Advertencia", "Cargado con la especialidad de la prestación")

    df["PacienteKey"] = df["PacienteID"].map(mapa_pac)
    df["MedicoKey"] = df["MedicoID"].map(dict(zip(d_med["MedicoID"], d_med["MedicoKey"])))
    df["EspecialidadKey"] = df["EspecialidadID"].map(dict(zip(d_esp["EspecialidadID"], d_esp["EspecialidadKey"])))
    df["PrestacionKey"] = df["PrestacionID"].map(dict(zip(d_prest["PrestacionID"], d_prest["PrestacionKey"])))
    for k in ("PacienteKey", "MedicoKey", "EspecialidadKey", "PrestacionKey"):
        for _, x in df[df[k].isna()].iterrows():
            log("FACT_PRESTACIONES", k, x["DetalleID"], "DQ08", "Error", "Clave -1 asignada")
        df[k] = df[k].fillna(-1).astype(int)
    df["FechaKey"] = df["FechaAten"].dt.strftime("%Y%m%d").astype(int)
    df["Cantidad"] = df["Cantidad"].astype(int)
    df["IngresoLinea"] = df["Cantidad"] * df["ValorUnitario"]
    return df[["DetalleID", "AtencionID", "ReservaID", "PacienteKey", "MedicoKey", "EspecialidadKey",
               "PrestacionKey", "FechaKey", "Cantidad", "ValorUnitario", "IngresoLinea"]]


# ------------------------------------------------------------------ 6. CARGA Y CONTROL
def volcar_control(estado, leidas, cargadas, rechazadas):
    SALIDA_CTRL.mkdir(exist_ok=True)
    guardar(pd.DataFrame(ERROR_LOG, columns=["Tabla", "Campo", "ValorOriginal", "CodigoDQ",
                                             "Severidad", "Accion", "Fecha"]), SALIDA_CTRL, "ETL_ERROR_LOG")
    guardar(pd.DataFrame([{"FechaInicio": FECHA_EJEC.isoformat(timespec="seconds"),
                           "FechaFin": datetime.now().isoformat(timespec="seconds"),
                           "Estado": estado, "FilasLeidas": leidas,
                           "FilasCargadas": cargadas, "FilasRechazadas": rechazadas}]),
            SALIDA_CTRL, "ETL_LOG_EJECUCION")
    for nombre, dfs in QUARANTINE.items():
        guardar(pd.concat(dfs, ignore_index=True), SALIDA_CTRL, nombre)


def main():
    stg = extraer()
    for h, col in (("01_PACIENTES", "PacienteID"), ("02_MEDICOS", "MedicoID"),
                   ("04_PRESTACIONES", "PrestacionID"), ("05_RESERVAS", "ReservaID")):
        pk_duplicada(stg[h], col, h)

    # Dimensiones (orden de 7.2)
    d_tiempo = dim_tiempo(stg["05_RESERVAS"])
    d_estado = dim_estado()
    d_esp = dim_especialidad(stg["04_PRESTACIONES"])
    d_pac, mapa_pac = dim_paciente(stg["01_PACIENTES"])
    d_med = dim_medico(stg["02_MEDICOS"], d_esp)
    d_prest = dim_prestacion(stg["04_PRESTACIONES"], d_esp)

    # Hechos
    f_res = fact_reservas(stg["05_RESERVAS"], mapa_pac, d_med)
    f_pre = fact_prestaciones(stg, f_res, mapa_pac, d_med, d_prest, d_esp)

    # Carga
    tablas = {"DIM_TIEMPO": d_tiempo, "DIM_ESTADO_RESERVA": d_estado, "DIM_ESPECIALIDAD": d_esp,
              "DIM_PACIENTE": d_pac, "DIM_MEDICO": d_med, "DIM_PRESTACION": d_prest,
              "FACT_RESERVAS": f_res, "FACT_PRESTACIONES": f_pre}
    for n, t in tablas.items():
        guardar(t, SALIDA, n)

    # Conciliación (7.4.4)
    n_res_origen = len(stg["05_RESERVAS"])
    ing_origen = (pd.to_numeric(stg["07_DETALLE_ATENCION"]["Cantidad"]) *
                  pd.to_numeric(stg["07_DETALLE_ATENCION"]["ValorUnitario"])).sum()
    checks = [
        ("FACT_RESERVAS = filas de 05_RESERVAS", len(f_res), n_res_origen),
        ("FACT_PRESTACIONES = filas de 07_DETALLE_ATENCION", len(f_pre), len(stg["07_DETALLE_ATENCION"])),
        ("Suma IngresoLinea = suma origen", f_pre["IngresoLinea"].sum(), ing_origen),
        ("Hechos con clave -1", int((f_res[["PacienteKey", "MedicoKey"]] == -1).sum().sum()
                                    + (f_pre[["PacienteKey", "MedicoKey", "EspecialidadKey", "PrestacionKey"]] == -1).sum().sum()), 0),
    ]
    ok = True
    print("\n=== CONCILIACIÓN ===")
    for desc, obtenido, esperado in checks:
        bien = obtenido == esperado
        ok &= bien
        print(f"[{'OK' if bien else 'FALLA'}] {desc}: obtenido={obtenido} esperado={esperado}")
    print("\n=== FILAS POR TABLA ===")
    for n, t in tablas.items():
        print(f"{n:22s}{len(t):>6}")
    resumen = pd.DataFrame(ERROR_LOG).groupby(["CodigoDQ", "Severidad"]).size() if ERROR_LOG else "sin incidencias"
    print("\n=== INCIDENCIAS (ETL_ERROR_LOG) ===\n", resumen, sep="")

    rechazadas = sum(len(pd.concat(v)) for v in QUARANTINE.values())
    volcar_control("Exitoso" if ok else "Con errores", sum(len(v) for v in stg.values()),
                   len(f_res) + len(f_pre), rechazadas)
    print(f"\nListo. Data Mart en ./{SALIDA}/  |  Logs y cuarentena en ./{SALIDA_CTRL}/")
    if not ok:
        print("ATENCIÓN: hay validaciones que fallaron; no cargues el Data Mart en Power BI hasta revisar.")


if __name__ == "__main__":
    main()
