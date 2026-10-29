# ETL visual para RetailMax

**GUÍA PRÁCTICA · SSIS / SSDT**

Cómo construir un flujo repetible desde Excel hasta un Data Warehouse en SQL Server.

`RAW` (trazabilidad) → `STG` (calidad) → `DW` (consumo)

Paso a paso · Flujo de datos · Cuarentena · Carga dimensional · Idempotencia

*Basado en Proyecto 1 · RetailMax y documentación oficial de Microsoft SSIS*

---

## 02 · Arquitectura: la arquitectura separa trazabilidad, calidad y consumo

| # | Capa | Descripción |
| --- | --- | --- |
| 1 | **ORÍGENES** | Excel base + complemento |
| 2 | **RAW** | Copia fiel + metadatos |
| 3 | **STG** | Tipos + reglas + homologación |
| 4 | **DW** | Dimensiones + hechos |
| 5 | **BI** | Medidas + visualización |

**CUARENTENA:** archivo · hoja · fila · clave · regla · motivo

> **Principio:** el flujo aceptado y el rechazado se contabilizan siempre.

*Fuente: Proyecto 1 · RetailMax; Microsoft Learn · Flujo de datos SSIS*

---

## 03 · Paso 1: empieza por el proyecto, no por el primer componente

1. **Crear proyecto:** Integration Services Project en Visual Studio + SSDT.
2. **Definir parámetros:** `RutaArchivo`, `LoteID`, `FechaCarga`, `ConnectionStringDW`.
3. **Crear conexiones:** Excel para los libros; OLE DB para SQL Server.
4. **Preparar paquetes:** `00_Control`, `01_RAW`, `02_STG`, `03_Dimensiones`, `04_Hechos`.

**Solución RETAILMAX_ETL**

```text
RetailMax_ETL
├─ Connection Managers
│   ├─ Excel_Base
│   ├─ Excel_Complemento
│   └─ DW_RetailMax
└─ SSIS Packages
    ├─ 00_Control.dtsx
    ├─ 01_Cargar_RAW.dtsx
    └─ 02_Transformar_STG.dtsx …
```

Configura `TargetServerVersion` y prueba cada conexión antes de diseñar el flujo.

*Fuente técnica: Microsoft Learn · Integration Services Projects y Data Flow Task*

---

## 04 · Paso 2: el contrato de datos se diseña antes del flujo

### Capas SQL

| Capa | Contenido |
| --- | --- |
| **RAW** | Entrada fiel; todo texto cuando el origen es incierto |
| **STG** | Tipos, reglas, códigos canónicos y banderas de calidad |
| **DW** | Dimensiones, `HechoVentas` y `HechoMetas` |
| **AUDIT** | Conteos por lote y tabla de rechazos |

### Metadatos obligatorios

| Campo | Propósito |
| --- | --- |
| `LoteID` | Identificar una ejecución |
| `ArchivoOrigen` | Trazar el archivo |
| `HojaOrigen` | Trazar la hoja |
| `FilaOrigen` | Volver al registro exacto |
| `FechaCarga` | Auditar cuándo ingresó |
| `MotivoRechazo` | Explicar la regla fallida |

> **Regla de oro:** no reemplaces el origen; conserva evidencia para volver a ejecutar.

*Fuente: Proyecto 1 · RetailMax · RAW, auditoría y cuarentena*

---

## 05 · Paso 3 · Paquete 01: cada archivo entra a RAW sin perder contexto

### Data Flow · `01_CARGAR_RAW`

```text
Excel Source → Derived Column (+ metadatos) → Conditional Split
                                                ├─ válidas → OLE DB Destination → raw.*
                                                └─ vacías · cabecera repetida · auxiliar
                                                     → OLE DB Destination → audit.Rechazos
```

### Configuración

- **Origen:** tabla o rango único; no hoja + tabla.
- **Tipos:** desactiva inferencias peligrosas.
- **Destino:** OLE DB con Fast Load.

Repite el patrón para `CLIENTES_ALTAS`, `PRODUCTOS_ALTAS`, `VENTAS_NUEVAS`, `DETALLE_NUEVO`, `EQUIVALENCIAS` y `METAS`.

**Control inmediato:** filas leídas = filas RAW + filas descartadas por estructura.

*Fuente: Proyecto 1 · RetailMax; Microsoft Learn · OLE DB Destination*

---

## 06 · Paso 4 · Paquete 02: tipar y normalizar sin ocultar errores

| Campo | Antes · RAW | Transformación | Después · STG |
| --- | --- | --- | --- |
| ClienteID | `' c-001 '` | Derived Column | `C-001` |
| Fecha | `'31/02/2026'` | Data Conversion | **RECHAZO:** fecha inválida |
| Cantidad | `'3'` | Data Conversion | `3` · entero |
| Precio | `'$ 12.990'` | Derived Column | `12990` · decimal |
| Descuento | `'10 %'` | Derived Column | `0,10` · decimal |
| Estado | `'completada '` | Lookup equivalencias | `COMPLETADA` |

Las filas con error se separan mediante **Conditional Split**.

> No uses "Quitar errores" sin redirigir la fila y registrar la regla fallida.

*Fuente: Proyecto 1 · RetailMax · tipos, fechas, claves y normalización*

---

## 07 · Paso 5 · Paquete 03: homologar maestros requiere prioridad explícita

### Flujo

```text
CLIENTES base ──┐
                ├→ Union All → Sort / Aggregate (prioridad canónica) → Lookup EQUIVALENCIAS → DimCliente
CLIENTES_ALTAS ─┘
                                      └→ Conflicto / alta incompleta
```

### Criterio de consolidación

1. Resolver primero códigos locales a códigos canónicos.
2. Eliminar duplicado exacto por clave.
3. Si difiere, priorizar ficha canónica y documentar conflicto.

Aplica el mismo patrón a Productos. Un nombre parecido no autoriza inferir una identidad.

*Fuente: Proyecto 1 · RetailMax · EQUIVALENCIAS, clientes y productos*

---

## 08 · Paso 6 · Paquete 04: valida ventas antes de calcular

### Flujo principal

`STG Detalle` → `Lookup VentaID` → `Lookup ProductoID` → `Lookup Vendedor–Tienda` → `Conditional Split` (reglas de negocio)

### Reglas — candidata a HechoVentas

- Estado definitivo
- Cantidad > 0
- Precio y costo > 0
- Fecha válida
- Cabecera válida

### Rechazos

- Sin cabecera
- Vendedor ≠ tienda
- Producto desconocido

Una línea inválida no elimina las otras líneas válidas del ticket; marca el ticket como **parcial**.

*Fuente: Proyecto 1 · RetailMax · joins, cardinalidad y unidad de rechazo*

---

## 09 · Paso 7: los cálculos deben ser verificables línea por línea

### Derived Column · DECIMAL, no FLOAT

| Campo | Fórmula |
| --- | --- |
| `ImporteBruto` | `Cantidad × PrecioUnitario` |
| `DescuentoImporte` | `ROUND(ImporteBruto × DescuentoPct, 0)` |
| `ImporteNeto` | `ImporteBruto − DescuentoImporte` |
| `CostoTotalReferencia` | `Cantidad × CostoUnitarioReferencia` |
| `MargenEstimado` | `ImporteNeto − CostoTotalReferencia` |

### Pruebas mínimas

1. Descuento cero
2. Con descuento
3. Caso de redondeo

### Identidades de control

- Bruto − Descuento = Neto
- Neto − Costo = Margen estimado

*Fuente: Proyecto 1 · RetailMax · reglas de cálculo y redondeo*

---

## 10 · Paso 8: las metas son otro hecho, no otra columna

| | Incorrecto | Correcto |
| --- | --- | --- |
| **Modelo** | Meta mensual repetida en cada línea de venta | `DimTienda` + `DimMes` → `HechoMetas` (1 fila / tienda–mes); `HechoVentas` (1 fila / línea válida) |
| **Resultado** | Línea 1 · $100 + Línea 2 · $100 + Línea 3 · $100 = **$300 falsos** | Meta registrada una sola vez |

**Clave de metas:** `TiendaID + Periodo`

Compara ventas y metas solo después de agregar ventas a tienda–mes.

- Valida tiendas, mes y duplicados exactos.
- Conflicto de importe → revisión, no suma automática.

*Fuente: Proyecto 1 · RetailMax · HechoMetas y granularidad*

---

## 11 · Paso 9: carga dimensiones primero; hechos después

### Secuencia de carga

1. **Dimensiones:** Cliente · Producto · Tienda · Vendedor · Fecha
2. **Lookup de claves:** resuelve claves sustitutas; no encontradas → rechazo
3. **Hechos:** `HechoVentas` + `HechoMetas`

Destino recomendado: OLE DB · Fast Load

### Puntos de conciliación

1. Claves únicas en dimensiones
2. Joins no aumentan filas
3. Sin referencias inválidas
4. Anuladas fuera de KPI
5. Metas no repetidas

*Fuente: Proyecto 1 · RetailMax; Microsoft Learn · OLE DB Destination*

---

## 12 · Paso 10: el Control Flow hace la carga repetible

### `00_CONTROL.dtsx`

`Preparar lote` (Execute SQL) → `01 · RAW` → `02 · STG` → `03 · DIM` → `04 · HECHOS` → `Cerrar lote`

| Parámetros | Logging | Idempotencia |
| --- | --- | --- |
| Rutas · conexiones · LoteID · ambiente | Inicio/fin · filas · errores · duración | Recarga de staging o `MERGE` por clave + lote |

> **Prueba decisiva:** ejecuta dos veces con los mismos archivos: filas y montos no deben aumentar.

*Fuente: Proyecto 1 · RetailMax; Microsoft Learn · Data Flow Task y SSISDB*

---

## 13 · Cierre: el ETL está listo cuando los conteos cierran

### Criterios de aceptación

- ✓ Dimensiones con claves únicas
- ✓ Anuladas no afectan indicadores
- ✓ Joins muchos-a-uno no multiplican filas
- ✓ Metas aparecen una vez por tienda–mes
- ✓ Hechos sin referencias inválidas
- ✓ Rechazos conservan origen y motivo
- ✓ Bruto − descuento = neto
- ✓ Segunda carga no duplica
- ✓ Neto − costo = margen estimado
- ✓ Cobertura incompleta queda advertida

### Entregables

Proyecto SSIS · scripts SQL · catálogo de reglas · conciliación · diagrama dimensional

### Fuentes

Proyecto 1 · RetailMax | Microsoft Learn: Data Flow, OLE DB Destination, SSIS Catalog

*Guía práctica preparada para el caso RetailMax*
