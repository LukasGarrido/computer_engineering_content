---
tags:
  - inteligencia-de-negocio
  - proyecto
  - saludvital
  - etl
  - data-warehouse
aliases:
  - "SaludVital"
  - "Proyecto SaludVital"
  - "SaludVital BI"
asignatura: "Inteligencia de Negocio"
tipo: proyecto
created: 2026-10-08
---

# SaludVital
- Inteligencia de negocio 
- Octavio Valencia - Lukas Garrido
- Paralelo 701
- *Entrega 1 - 2 - 3 - 4 - 5 - 6 (ETL)*
- GitHub : [https://github.com/LukasGarrido/computer_engineering_content/blob/master/Inteligencia%20de%20negocio/PROYECTO_SaludVital/PROYECTO%20SALUDVITAL%20-%20An%C3%A1lisis%20del%20negocio.md](https://github.com/LukasGarrido/computer_engineering_content/blob/master/wiki/Inteligencia%20de%20Negocio/Proyecto_SaludVital_Analisis.md)
---
## Índice

- [1. Análisis del negocio](#1-anlisis-del-negocio)
  - [1.1. Historia](#11-historia)
- [2. Situación actual](#2-situacin-actual)
  - [2.1. Actores](#21-actores)
  - [2.2. Procesos](#22-procesos)
  - [2.3. Problemas](#23-problemas)
  - [2.4. Objetivos](#24-objetivos)
- [3. Reglas de negocio](#3-reglas-de-negocio)
  - [3.1. Catalogo de reglas](#31-catalogo-de-reglas)
    - [3.1.1. Reglas sobre Limpieza y Estructura de Datos (ETL)](#311-reglas-sobre-limpieza-y-estructura-de-datos-etl)
    - [3.1.2. Reglas Operativas y de Atención](#312-reglas-operativas-y-de-atencin)
    - [3.1.3. Reglas Financieras y de Modelo Dimensional](#313-reglas-financieras-y-de-modelo-dimensional)
- [4. Requerimientos BI](#4-requerimientos-bi)
  - [4.1. Matriz de requerimientos](#41-matriz-de-requerimientos)
- [5. Perfilamiento de datos](#5-perfilamiento-de-datos)
  - [5.1. Alcance y fuente](#51-alcance-y-fuente)
  - [5.2. Perfilamiento por tabla](#52-perfilamiento-por-tabla)
  - [5.3. Resumen de hallazgos de calidad](#53-resumen-de-hallazgos-de-calidad)
  - [5.4. Integridad referencial](#54-integridad-referencial)
- [6. Modelo dimensional](#6-modelo-dimensional)
  - [6.1. Proceso de negocio y granularidad](#61-proceso-de-negocio-y-granularidad)
  - [6.2. Tablas de hechos](#62-tablas-de-hechos)
  - [6.3. Dimensiones](#63-dimensiones)
  - [6.4. Esquema y relaciones](#64-esquema-y-relaciones)
  - [6.5. Medidas](#65-medidas)
- [7. ETL](#7-etl)
  - [7.1. Introducción y propósito](#71-introduccion-y-proposito)
    - [7.1.1. Objetivos del ETL](#711-objetivos-del-etl)
  - [7.2. Arquitectura y flujo de procesamiento](#72-arquitectura-y-flujo-de-procesamiento)
  - [7.3. Matriz de mapeo origen a destino](#73-matriz-de-mapeo-origen-a-destino)
    - [7.3.1. Tablas de dimensiones](#731-tablas-de-dimensiones)

---

# 1. Análisis del negocio
## 1.1. Historia

SaludVital es un centro medico privado que provee servicios de atención **ambulatoria** a pacientes de la Región del Bio Bio. Inicio como un pequeño centro de atención medica, el cual actualmente lleva 8 años operando. En sus inicios contaba solamente con cierto servicios, como: Medicina general, Pediatría, Ginecología, Traumatología.

Debido a la alta demanda, cuenta con **10 especialidades medicas** y mas de 20 profesionales. Actualmente, el centro SaludVital atiende aproximadamente 2000 consultas mensuales. La reserva de horas se realiza de manera presencial en recepción, por teléfono, vía sitio web o a través de su aplicación móvil.

A pesar de este crecimiento, la arquitectura de los sistemas de información actuales no fue diseñada para un análisis multidimensional de los datos, lo que limita la explotación estratégica de su volumen de información. 

--- 
# 2. Situación actual

Actualmente, SaludVital cuenta con un sistema que no satisface el análisis multidimensional de los datos. Esta limitación genera diversos problemas, como: información distribuida, Pacientes duplicados, Especialidades inconsistentes, etc. 

---
## 2.1. Actores

Internos:

1. Paciente – solicita y recibe atención médica, reserva/cancela horas.
2. Médico / Profesional de salud – otorga la atención y registra el detalle de la consulta.
3. Personal de recepción – gestiona reservas presenciales/telefónicas y confirma asistencia.
4. Dirección / Administración – toma decisiones estratégicas y evalúa desempeño.
5. Área de Sistemas / TI – administra los sistemas de información del centro.
6. Área de Facturación/Finanzas – gestiona cobros e ingresos por atenciones.

Externos:

1. Sitio web de reservas – canal digital para agendar horas.
2. Aplicación móvil – canal alternativo de reserva y gestión de horas.
3. Call center / Central telefónica – canal telefónico de reserva.
---
## 2.2. Procesos

- Reserva de hora médica (presencial, telefónica, web, app).
- Registro y actualización de datos del paciente.
- Confirmación de hora.
- Atención médica (consulta, diagnóstico, indicaciones).
- Cancelación / reprogramación de hora.
- Registro de asistencia (Atendida, Cancelada, No asistió, Pendiente).
- Facturación de la atención.
- Generación de reportes mensuales (manual).
- Gestión de especialidades y profesionales.

---
## 2.3. Problemas

1. Información distribuida: La información de pacientes, médicos y atenciones se encuentra en diferentes fuentes.
2. Pacientes duplicados: Existen pacientes registrados más de una vez debido a diferencias en sus datos. Ejemplo: 
	- Juan Pérez 
	- Juan A. Pérez 
	- JUAN PEREZ 
	- Juan Pérez
3. Especialidades inconsistentes: Algunas especialidades aparecen con diferentes nombres: 
	- Traumatología 
	- Traumatologia 
	- TRAUMATOLOGIA 
	- Trauma
4. Horas no concretadas: No todas las reservas terminan en una atención efectiva. Existen estados como: 
	- Atendida 
	- Cancelada 
	- No asistió 
	- Pendiente.
5. Reportes manuales: La dirección actualmente recibe informes mensuales preparados manualmente.
6. Dificultad para evaluar desempeño: No existe una visión consolidada de:
	- Demanda por especialidad
	- Utilización de horas
	- Atenciones por médico
	- Cancelaciones
	- Inasistencias
	- Ingresos
---
## 2.4. Objetivos

**Objetivo General:** El objetivo del proyecto es diseñar e implementar una solución de inteligencia de negocios. La cual debe permitir analizar las atenciones medicas de SaludVital, optimizando la toma de decisiones.

**Objetivos específicos:** 
1. Analizar el negocio: Estudiar la trayectoria y modelo de atención de SaludVital.
2. Identificar actores y procesos: Mapear quiénes interactúan con el centro, y las operaciones.
3. Identificar entidades: Reconocer los objetivos.
4. Definir reglas de negocio: Establecer los limites y políticas que rigen el flujo de datos. 
5. Analizar la calidad de los datos: Diagnosticar la información actual para identificar problemas de consistencia, registros duplicados, campos nulos y datos dispersos.
6. Identificar indicadores relevantes: Seleccionar las métricas clave de desempeño.
7. Definir requerimientos BI: Identificar y levantar las necesidades de información que tienen los directivos para tomar decisiones basadas en los datos.
8. Determinar la granularidad del hecho: 
9. Diseñar un modelo dimensional: Estructurar la base de datos analítica mediante esquemas.
10. Implementar procesos ETL: Diseñar los flujos de Extracción, Transformación y Limpieza de datos desde los sistemas origen hacia el destino.
11. Construir un Data Mart: Crear base de datos optimizada para el área de salud.
12. Crear medidas DAX: Programar los cálculos y fórmulas dinámicas necesarios a la hora de analizar métricas agregadas en la herramienta de reporte.
13. Diseñar un dashboard: Desarrollar un panel de control interactivo y visual para monitorear los indicadores principales de forma intuitiva.
14. Analizar los resultados: Interpretar los hallazgos y patrones descubiertos en los dashboards para entender el desempeño real del centro médico.
15. Proponer recomendaciones: Formular acciones estratégicas y de mejora continua basadas en la evidencia obtenida del análisis de datos.

---

# 3. Reglas de negocio

## 3.1. Catalogo de reglas

*Un catalogo de reglas de negocio es una lista ordenada y documentada que recopila las condiciones, restricciones, políticas y normas bajo las cuales opera una organización*

*Al analizar `SALUDVITAL_2BaseDatos.xlsx`, se detectó que la tabla `03_ESPECIALIDADES`esta errónea (es una copia exacta de `02_MEDICOS` ), por lo que RN01 para deducir las 10 especialidades a partir de las prestaciones, garantizando la integridad del modelo dimensional.*

### 3.1.1. Reglas sobre Limpieza y Estructura de Datos (ETL)

| **ID**   | **Regla**                                                                                                                                                                                                                                                                                               | **Impacto**                          |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| **RN01** | **Reconstrucción de Especialidades:** Dado que la tabla `03_ESPECIALIDADES` contiene datos erróneos (duplica `02_MEDICOS` ), los registros de `03_ESPECIALIDADES` deben ser deducidos y construidos durante el ETL extrayendo los códigos únicos (`EspecialidadID`) desde la tabla "`04_PRESTACIONES`". | Proceso ETL / Dimensión Especialidad |
| **RN02** | **Normalización de Nombres:** Cualquier variación tipográfica o error de escritura en especialidades detectada en fuentes anexas (ej. _Trauma, TRAUMATOLOGIA_) debe estandarizarse a su nombre **maestro** deducido (ej. "Traumatología").                                                              | Proceso ETL / Limpieza de Datos      |
| **RN03** | **Unificación de Pacientes:** Los registros duplicados de pacientes con diferencias de capitalización, puntuación o abreviaturas (ej. _Juan Pérez vs JUAN PEREZ_) deben consolidarse bajo un único `PacienteID`.                                                                                        | Proceso ETL / Dimensión Paciente     |

### 3.1.2. Reglas Operativas y de Atención

| **ID**   | **Regla**                                                                                                                                                              | **Impacto**                                           |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **RN04** | **Atenciones Efectivas:** Una reserva solo se considera como "atención efectiva" (y genera prestaciones realizadas) si su `EstadoReserva` es estrictamente "Atendida". | KPI (Atenciones realizadas, Tasa de atención)         |
| **RN05** | **Inasistencias y Cancelaciones:** Las reservas en estado "Cancelada", "Pendiente" o "No asistió" no generan ingresos ni prestaciones.                                 | KPI (Ingresos, Tasa de inasistencia)                  |
| **RN06** | **Horas Perdidas:** Exclusivamente el estado "No asistió" se contabilizará negativamente para evaluar el desempeño de la utilización de horas del profesional médico.  | KPI (Utilización de horas / Dashboard Gestión Médica) |

### 3.1.3. Reglas Financieras y de Modelo Dimensional

| **ID**   | **Regla**                                                                                                                                                                                                                                  | **Impacto**                          |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------ |
| **RN07** | **Cálculo de Ingresos:** Los ingresos se calculan sumando el valor monetario (`Valor` en la tabla PRESTACIONES) únicamente de las atenciones con estado "Atendida".                                                                        | Medidas DAX / KPI Ingresos           |
| **RN08** | **Granularidad del Hecho Principal:** El nivel más detallado de la tabla de hechos corresponde a la **prestación individual realizada** dentro de una atención, vinculando al paciente, el médico, la especialidad, la reserva y la fecha. | Modelo Dimensional (Tabla de Hechos) |

---

# 4. Requerimientos BI

## 4.1. Matriz de requerimientos

| ID                           | Pregunta                                                                        | Indicador                       | Dimensión              | Prioridad |
| ---------------------------- | ------------------------------------------------------------------------------- | ------------------------------- | ---------------------- | --------- |
| **Demanda**                  |                                                                                 |                                 |                        |           |
| RQ01                         | ¿Cuántas reservas se realizan mensualmente?                                     | Total de Reservas               | Tiempo                 | Alta      |
| RQ02                         | ¿Cuál es la especialidad más solicitada?                                        | Total de Reservas               | Especialidad           | Alta      |
| RQ03                         | ¿Qué días de la semana presentan mayor demanda?                                 | Total de Reservas               | Tiempo (Día de semana) | Media     |
| RQ04                         | ¿Cómo evoluciona la demanda de horas durante el año?                            | Total de Reservas               | Tiempo (Mes)           | Alta      |
| **Atención**                 |                                                                                 |                                 |                        |           |
| RQ05                         | ¿Qué porcentaje de reservas termina en una atención efectiva?                   | Tasa de Atención                | Tiempo, Especialidad   | Alta      |
| RQ06                         | ¿Cuál es la tasa de inasistencia por especialidad?                              | Tasa de Inasistencia            | Especialidad           | Alta      |
| RQ07                         | ¿Cuál es la tasa de cancelación de horas?                                       | Tasa de Cancelación             | Tiempo                 | Media     |
| RQ08                         | ¿Cuántas horas se pierden mensualmente por inasistencia?                        | Horas Perdidas                  | Tiempo, Médico         | Alta      |
| **Médicos / Gestión médica** |                                                                                 |                                 |                        |           |
| RQ09                         | ¿Qué médicos atienden más pacientes?                                            | Atenciones Realizadas           | Médico                 | Alta      |
| RQ10                         | ¿Cuál es el ranking de profesionales por atenciones realizadas?                 | Atenciones Realizadas           | Médico                 | Media     |
| RQ11                         | ¿Cuál es el nivel de utilización de horas por médico?                           | Utilización de Horas            | Médico, Tiempo         | Alta      |
| RQ12                         | ¿Qué especialidad concentra más profesionales y mayor carga de atención?        | Atenciones Realizadas           | Especialidad, Médico   | Media     |
| **Pacientes**                |                                                                                 |                                 |                        |           |
| RQ13                         | ¿Qué comunas concentran más pacientes atendidos?                                | Atenciones Realizadas           | Paciente (Comuna)      | Media     |
| RQ14                         | ¿Qué pacientes utilizan con mayor frecuencia los servicios?                     | Frecuencia de Atención          | Paciente               | Media     |
| RQ15                         | ¿Cómo se distribuye la cartera de pacientes por previsión (Fonasa/Isapre)?      | Total de Pacientes              | Paciente (Previsión)   | Baja      |
| RQ16                         | ¿Cómo evoluciona la base de pacientes atendidos en el tiempo?                   | Pacientes Atendidos             | Tiempo                 | Media     |
| **Ingresos**                 |                                                                                 |                                 |                        |           |
| RQ17                         | ¿Cuáles son los ingresos totales por período?                                   | Ingresos                        | Tiempo                 | Alta      |
| RQ18                         | ¿Qué especialidades generan mayores ingresos?                                   | Ingresos                        | Especialidad           | Alta      |
| RQ19                         | ¿Cuál es el ingreso promedio por atención?                                      | Ingreso Promedio por Atención   | Especialidad, Médico   | Media     |
| RQ20                         | ¿Qué prestaciones son las más solicitadas y más rentables?                      | Ingresos, Total de Prestaciones | Prestación             | Media     |
| **Especialidades**           |                                                                                 |                                 |                        |           |
| RQ21                         | ¿Cuántas especialidades activas tiene el centro y cuál es su carga de atención? | Total de Atenciones             | Especialidad           | Media     |
| RQ22                         | ¿Qué especialidad presenta mayor crecimiento de demanda interanual?             | Total de Reservas               | Especialidad, Tiempo   | Baja      |
| RQ23                         | ¿Cómo se compara la tasa de atención entre especialidades?                      | Tasa de Atención                | Especialidad           | Media     |
| RQ24                         | ¿Qué especialidades requieren más profesionales para cubrir su demanda?         | Utilización de Horas            | Especialidad, Médico   | Baja      |

---

# 5. Perfilamiento de datos

## 5.1. Alcance y fuente

El perfilamiento se realizó sobre el archivo `SALUDVITAL_2BaseDatos.xlsx`, que contiene 7 tablas: 
- `01_PACIENTES`
- `02_MEDICOS`
- `03_ESPECIALIDADES`
- `04_PRESTACIONES`
- `05_RESERVAS`
- `06_ATENCIONES` 
- `07_DETALLE_ATENCION`.
Se analizaron nulos, duplicados, consistencia de categorías e integridad referencial entre tablas.

## 5.2. Perfilamiento por tabla

| Tabla                 | Filas | Columnas | Hallazgos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| --------------------- | ----- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_PACIENTES`        | 33    | 7        | 30/33 completos (90,9%); **P031–P033** vacíos salvo el ID. Columna `Unnamed: 1` (columna B) 100% nula, descartar en ETL. Sin duplicados exactos de nombre completo, pero varios nombres/apellidos se repiten entre personas distintas ("Pérez" x5, "Soto"/"Rojas"/"González"/"Silva" x4) → deduplicar siempre por nombre completo, no por partes. Distribución pareja: FONASA/Isapre 15-15, F/M 15-15, edad 28-57 años (prom. 41,6).                                                                                 |
| `02_MEDICOS`          | 10    | 3        | Sin nulos ni `MedicoID` duplicados. 10 médicos, uno por especialidad (`E01`–`E10`), consistente con el negocio.                                                                                                                                                                                                                                                                                                                                                                                                      |
| `03_ESPECIALIDADES`   | 10    | 3        | La tabla es una copia exacta (byte a byte) de `02_MEDICOS`, mismas columnas (`MedicoID`, `Medico`, `EspecialidadID`) y mismos valores. No contiene un catálogo real de especialidades. Esta es la base de **RN01**: la dimensión de especialidad debe reconstruirse desde `04_PRESTACIONES`.                                                                                                                                                                                                                         |
| `04_PRESTACIONES`     | 15    | 4        | Sin nulos ni duplicados. Contiene **10 `EspecialidadID` únicos** (`E01`–`E10`), lo que valida que sí es posible deducir el catálogo completo de las 10 especialidades desde esta tabla, tal como indicamos en RN01. Nombres de especialidad ya vienen estandarizados en esta fuente (no se observan variantes tipo "Trauma"/"TRAUMATOLOGIA" en `04_PRESTACIONES`, esas variantes descritas en el análisis del negocio, corresponden a fuentes anexas/históricas fuera de este extracto y siguen cubiertas por RN02). |
| `05_RESERVAS`         | 30    | 6        | Sin nulos ni `ReservaID` duplicados. `EstadoReserva` solo presenta 3 valores en este extracto: **Atendida (22), No asistió (4), Cancelada (4)**, el estado "Pendiente" mencionado en el proceso de negocio no aparece en la muestra actual, por lo que el modelo y el ETL deben contemplarlo igualmente como estado válido futuro. No se detectaron reservas duplicadas (mismo paciente, médico, fecha y hora).                                                                                                      |
| `06_ATENCIONES`       | 22    | 5        | Sin nulos ni duplicados. Cada `ReservaID` referenciado aparece una sola vez (relación 1 a 1 con Reserva). Las 22 atenciones corresponden exactamente a las 22 reservas en estado "Atendida" — consistente con RN04.                                                                                                                                                                                                                                                                                                  |
| `07_DETALLE_ATENCION` | 22    | 5        | Sin nulos ni duplicados. Cada atención tiene exactamente un detalle asociado (`Cantidad = 1` en todos los casos) y el `ValorUnitario` coincide en el 100% de los casos con el `Valor` maestro de `04_PRESTACIONES` (no se detectaron precios inconsistentes).                                                                                                                                                                                                                                                        |

## 5.3. Resumen de hallazgos de calidad

| Problema detectado                                                                                                                 | Tabla / Campo                                | Evidencia                                                 | Regla de negocio asociada | Acción de limpieza (ETL)                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | --------------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tabla de especialidades corrupta (copia de Médicos)                                                                                | `03_ESPECIALIDADES`                          | Igual fila a fila a `02_MEDICOS`                          | RN01                      | Descartar `03_ESPECIALIDADES`; construir `DIM_ESPECIALIDAD` desde `EspecialidadID` único de `04_PRESTACIONES`                                    |
| Columna vacía sin uso                                                                                                              | `01_PACIENTES.Unnamed: 1`                    | 33/33 nulos                                               | —                         | Excluir la columna en la extracción                                                                                                              |
| Registros de paciente incompletos/huérfanos                                                                                        | `01_PACIENTES` (P031, P032, P033)            | Todos los campos nulos salvo el ID                        | —                         | Poner en cuarentena / excluir de `DIM_PACIENTE` hasta validar con el sistema origen; registrar como incidencia de calidad                        |
| Estado "Pendiente" no representado en la muestra                                                                                   | `05_RESERVAS.EstadoReserva`                  | Solo 3 de los 4 estados del proceso aparecen en los datos | RN05, RN06                | Modelar igualmente los 4 estados posibles en `DIM_ESTADO_RESERVA`, para no perder cobertura cuando aparezcan en producción                       |
| Riesgo de pacientes/especialidades duplicados por variantes de escritura (descrito en el negocio, no reproducido en este extracto) | Fuentes anexas de Pacientes / Especialidades | Ejemplos narrados en el análisis del negocio              | RN02, RN03                | Mantener normalización (mayúsculas/tildes/espacios) y matching difuso como control preventivo del ETL, aun si el extracto actual no lo evidencia |

No se detectaron: valores nulos en las tablas transaccionales (`RESERVAS`, `ATENCIONES`, `DETALLE_ATENCION`), llaves primarias duplicadas, ni precios inconsistentes entre `DETALLE_ATENCION` y `PRESTACIONES`.

## 5.4. Integridad referencial

| Relación verificada                                           | Resultado                                           |
| ------------------------------------------------------------- | --------------------------------------------------- |
| `RESERVAS.PacienteID` → `PACIENTES.PacienteID`                | Sin huérfanos                                       |
| `RESERVAS.MedicoID` → `MEDICOS.MedicoID`                      | Sin huérfanos                                       |
| `ATENCIONES.ReservaID` → `RESERVAS.ReservaID`                 | Sin huérfanos, relación 1 a 1                       |
| Reservas "Atendida" ↔ existencia de Atención                  | Coincidencia exacta (22 = 22), consistente con RN04 |
| `DETALLE_ATENCION.AtencionID` → `ATENCIONES.AtencionID`       | Sin huérfanos, toda atención tiene detalle          |
| `DETALLE_ATENCION.PrestacionID` → `PRESTACIONES.PrestacionID` | Sin huérfanos                                       |
| `MEDICOS.EspecialidadID` / `PRESTACIONES.EspecialidadID`      | Consistentes entre sí (E01–E10 en ambas)            |

**Conclusión del perfilamiento:** las tablas transaccionales (Reservas, Atenciones, Detalle) están limpias, los problemas de calidad detectados en la fuente disponible (excel) se concentran en las tablas maestras (`03_ESPECIALIDADES` corrupta, columna residual y registros incompletos en `PACIENTES`). Los problemas narrados en el análisis del negocio (pacientes duplicados, especialidades con variantes de escritura) deben tratarse como riesgos del proceso operativo real vigentes para el diseño de RN02/RN03 aunque no se manifiesten en este extracto acotado.

---

# 6. Modelo dimensional

## 6.1. Proceso de negocio y granularidad

**Proceso de negocio analizado:** el ciclo de atención médica ambulatoria, desde la reserva de hora hasta la prestación efectivamente realizada y facturada.

**Hecho principal:** la prestación realizada dentro de una atención médica (RN08).

**Granularidad del hecho principal:** una fila representa **una prestación individual realizada dentro de una atención**, asociada a un paciente, un médico, una especialidad, una reserva y una fecha.

Para responder también a las preguntas de demanda y efectividad (RQ01–RQ08), que necesitan contar **todas** las reservas, incluidas las que no generan prestación (Cancelada, No asistió, Pendiente), se define una **constelación de hechos** con dos tablas de hechos que comparten dimensiones conformadas (Paciente, Médico, Especialidad, Tiempo):

1. `FACT_RESERVAS` — grano: una fila por reserva (soporta demanda, tasa de atención/inasistencia/cancelación, utilización de horas).
2. `FACT_PRESTACIONES` — grano: una fila por prestación realizada (soporta ingresos y granularidad clínica de detalle), y solo contiene reservas en estado "Atendida" (RN04, RN07).

## 6.2. Tablas de hechos

**`FACT_RESERVAS`**

| Campo                     | Tipo         | Descripción                                          |
| ------------------------- | ------------ | ---------------------------------------------------- |
| ReservaID (PK degenerada) | Texto        | Identificador de la reserva                          |
| PacienteKey (FK)          | Entero       | → `DIM_PACIENTE`                                     |
| MedicoKey (FK)            | Entero       | → `DIM_MEDICO`                                       |
| EstadoKey (FK)            | Entero       | → `DIM_ESTADO_RESERVA`                               |
| FechaKey (FK)             | Entero       | → `DIM_TIEMPO` (fecha de la reserva)                 |
| HoraReserva               | Hora         | Hora agendada                                        |
| EsAtendida                | Booleano/0-1 | Bandera derivada (1 si EstadoReserva = "Atendida")   |
| EsInasistencia            | Booleano/0-1 | Bandera derivada (1 si EstadoReserva = "No asistió") |

**`FACT_PRESTACIONES`**

| Campo | Tipo | Descripción |
|---|---|---|
| DetalleID (PK degenerada) | Texto | Identificador del detalle de atención |
| AtencionID / ReservaID (degenerada) | Texto | Trazabilidad a la atención/reserva origen |
| PacienteKey (FK) | Entero | → `DIM_PACIENTE` |
| MedicoKey (FK) | Entero | → `DIM_MEDICO` |
| EspecialidadKey (FK) | Entero | → `DIM_ESPECIALIDAD` |
| PrestacionKey (FK) | Entero | → `DIM_PRESTACION` |
| FechaKey (FK) | Entero | → `DIM_TIEMPO` (fecha de la atención) |
| Cantidad | Entero | Unidades de la prestación |
| ValorUnitario | Numérico | Valor cobrado por unidad |
| IngresoLinea | Numérico | Cantidad × ValorUnitario |

## 6.3. Dimensiones

| Dimensión | Llave | Atributos principales | Origen |
|---|---|---|---|
| `DIM_PACIENTE` | PacienteKey | PacienteID, Nombre, Comuna, FechaNacimiento, Edad, Previsión, Sexo | `01_PACIENTES` (excluyendo columna vacía y registros incompletos) |
| `DIM_MEDICO` | MedicoKey | MedicoID, Nombre, EspecialidadID (atributo de referencia) | `02_MEDICOS` |
| `DIM_ESPECIALIDAD` | EspecialidadKey | EspecialidadID, NombreEspecialidad (estandarizado) | Deducida de `04_PRESTACIONES` (RN01) + normalización (RN02) |
| `DIM_PRESTACION` | PrestacionKey | PrestacionID, NombrePrestación, EspecialidadID, ValorListado | `04_PRESTACIONES` |
| `DIM_ESTADO_RESERVA` | EstadoKey | Atendida / Cancelada / No asistió / Pendiente | `05_RESERVAS` (catálogo fijo de 4 estados) |
| `DIM_TIEMPO` | FechaKey | Fecha, Día, Mes, Nombre Mes, Trimestre, Año, Día de semana, Es fin de semana | Calendario generado |

## 6.4. Esquema y relaciones

```mermaid
erDiagram
    DIM_PACIENTE ||--o{ FACT_RESERVAS : "realiza"
    DIM_MEDICO ||--o{ FACT_RESERVAS : "atiende"
    DIM_ESTADO_RESERVA ||--o{ FACT_RESERVAS : "clasifica"
    DIM_TIEMPO ||--o{ FACT_RESERVAS : "fecha"

    DIM_PACIENTE ||--o{ FACT_PRESTACIONES : "recibe"
    DIM_MEDICO ||--o{ FACT_PRESTACIONES : "otorga"
    DIM_ESPECIALIDAD ||--o{ FACT_PRESTACIONES : "clasifica"
    DIM_PRESTACION ||--o{ FACT_PRESTACIONES : "detalla"
    DIM_TIEMPO ||--o{ FACT_PRESTACIONES : "fecha"
    DIM_ESPECIALIDAD ||--o{ DIM_MEDICO : "especializa"
    DIM_ESPECIALIDAD ||--o{ DIM_PRESTACION : "agrupa"
```

## 6.5. Medidas

| KPI                                  | Fórmula (lógica DAX)                                                                     | Tabla de hechos                   |
| ------------------------------------ | ---------------------------------------------------------------------------------------- | --------------------------------- |
| KPI1 — Total de reservas             | `COUNTROWS(FACT_RESERVAS)`                                                               | FACT_RESERVAS                     |
| KPI2 — Atenciones realizadas         | `CALCULATE(COUNTROWS(FACT_RESERVAS), EstadoReserva = "Atendida")`                        | FACT_RESERVAS                     |
| KPI3 — Tasa de atención              | `Atenciones realizadas / Total de reservas`                                              | FACT_RESERVAS                     |
| KPI4 — Tasa de inasistencia          | `CALCULATE(COUNTROWS(FACT_RESERVAS), EstadoReserva="No asistió") / Total de reservas`    | FACT_RESERVAS                     |
| KPI5 — Ingresos                      | `SUM(FACT_PRESTACIONES[IngresoLinea])` (solo reservas Atendida, por RN07)                | FACT_PRESTACIONES                 |
| KPI6 — Ingreso promedio por atención | `Ingresos / Atenciones realizadas`                                                       | FACT_PRESTACIONES / FACT_RESERVAS |
| KPI7 — Utilización de horas          | `1 - (Horas "No asistió" / Total de horas agendadas)` (RN06: solo "No asistió" penaliza) | FACT_RESERVAS                     |
| Tasa de cancelación (complementario) | `CALCULATE(COUNTROWS(FACT_RESERVAS), EstadoReserva="Cancelada") / Total de reservas`     | FACT_RESERVAS                     |


---

# 7. ETL
*Documentación del proceso completo de Extracción, Transformación y Carga*(ETL)

## 7.1. Introducción y propósito

El proceso ETL es el encargado de convertir la información dispersa de SaludVital (planillas Excel con 7 tablas y 142 filas en total) en un **Data Mart dimensional**, que alimente el modelo semántico y el dashboard en Power BI. Su diseño se deriva directamente de los hallazgos de la sección 5 y de las reglas de negocio de la sección 3.

### 7.1.1 Objetivos del ETL

1. Consolidar en un solo destino las fuentes distribuidas (Problema 1).
2. Corregir o aislar los problemas de calidad detectados: especialidades inconsistentes, pacientes duplicados o incompletos, columnas residuales (Problemas 2 y 3).
3. Cargar únicamente atenciones efectivas en el hecho de prestaciones, y todas las reservas, con su estado, en el hecho de reservas (Problema 4, RN04–RN07).
4. Dejar trazabilidad de cada registro rechazado o corregido, de modo que los reportes dejen de depender de preparación manual (Problema 5).

**Decisiones de diseño**

| Decisión            | Definición                                                                                   | Justificación                                                                                                       |
| ------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Estrategia de carga | _Full refresh_ (truncar y recargar) en esta etapa                                            | Volumen mínimo (142 filas), simplifica la idempotencia. Queda preparado para carga incremental por fecha de reserva |
| Capas               | Origen (Excel) → Staging (`STG_*`) → Data Mart (`DIM_*`, `FACT_*`)                           | Separa la copia fiel del origen de los datos ya depurados                                                           |
| Claves              | Claves sustitutas (_surrogate keys_) enteras en cada dimensión, `-1` = miembro "Desconocido" | Evita perder hechos ante relaciones inválidas y desacopla el DW de los IDs del origen                               |
| Orden de carga      | Dimensiones primero, luego hechos                                                            | Los hechos requieren las claves sustitutas ya generadas                                                             |
| Manejo de errores   | Cuarentena + registro de errores, nunca se elimina un registro sin dejar evidencia           | Cumple el requisito de explicar toda diferencia entre origen y destino                                              |
| Herramienta         | Por definir por el equipo (Python/pandas + base relacional, SSIS o Power Query)              | La lógica documentada es independiente de la herramienta                                                            |

---
## 7.2. Arquitectura y flujo de procesamiento

```mermaid
flowchart LR
    A["ORIGEN<br/>Excel · 7 hojas"] --> B["EXTRACCIÓN<br/>Staging STG_*"]
    B --> C["LIMPIEZA<br/>Normalización y validación"]
    C --> D["TRANSFORMACIÓN<br/>Derivación de campos y dimensiones"]
    D --> E["INTEGRACIÓN<br/>Claves sustitutas y joins"]
    E --> F["CARGA<br/>Data Mart DIM_* / FACT_*"]
    C -.-> Q[("Cuarentena y<br/>ETL_ERROR_LOG")]
    E -.-> Q
    F -.-> L[("ETL_LOG_EJECUCION")]
```

| Etapa                 | Qué ocurre                                                                                                                                                                                                                                                                   | Reglas y hallazgos que aplica           | Salida                                                                                                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **1. Origen**         | Se utiliza el libro `SaludVital_BaseDatos.xlsx` con las hojas `01_PACIENTES`, `02_MEDICOS`, `03_ESPECIALIDADES`, `04_PRESTACIONES`, `05_RESERVAS`, `06_ATENCIONES` y `07_DETALLE_ATENCION`                                                                                   | Alcance definido en 5.1                 | Archivo fuente de solo lectura                                                                               |
| **2. Extracción**     | Lectura de cada hoja hacia una tabla de staging idéntica al origen, agregando columnas de auditoría (`FechaCarga`, `ArchivoOrigen`, `NroFila`). Se excluye la columna `Unnamed: 1` de `01_PACIENTES`. `03_ESPECIALIDADES` se lee pero **no se usa** para poblar el Data Mart | Hallazgo 5.3 (columna vacía), RN01      | `STG_PACIENTES`, `STG_MEDICOS`, `STG_PRESTACIONES`, `STG_RESERVAS`, `STG_ATENCIONES`, `STG_DETALLE_ATENCION` |
| **3. Limpieza**       | Eliminación de espacios sobrantes, estandarización de mayúsculas/tildes, validación de llaves primarias y de catálogos, cuarentena de registros incompletos (P031–P033), consolidación de pacientes duplicados                                                               | RN02, RN03, controles DQ01–DQ12 (7.4.1) | Datos depurados + registros en cuarentena                                                                    |
| **4. Transformación** | Derivación de campos (`EsAtendida`, `EsInasistencia`, `IngresoLinea`, `Edad`, `FechaKey`), construcción de `DIM_ESPECIALIDAD` desde `04_PRESTACIONES`, generación del calendario `DIM_TIEMPO` y del catálogo fijo `DIM_ESTADO_RESERVA`                                       | RN01, RN04–RN07                         | Datos listos para modelar                                                                                    |
| **5. Integración**    | Asignación de claves sustitutas, uniones `Reservas ⟶ Atenciones ⟶ Detalle ⟶ Prestaciones`, resolución de claves foráneas con miembro `-1` ante relaciones inválidas, uso de dimensiones conformadas por ambos hechos                                                         | RN08, integridad referencial 5.4        | `DIM_*` y `FACT_*` en memoria o en tablas temporales                                                         |
| **6. Carga**          | Carga ordenada de dimensiones y hechos, validaciones de conciliación y registro de la ejecución                                                                                                                                                                              | 7.4.4                                   | Data Mart poblado + `ETL_LOG_EJECUCION`                                                                      |

**Orden de ejecución de la carga**

1. `DIM_TIEMPO`, `DIM_ESTADO_RESERVA`, `DIM_ESPECIALIDAD`
2. `DIM_PACIENTE`, `DIM_MEDICO`, `DIM_PRESTACION` (las dos últimas dependen de `DIM_ESPECIALIDAD`)
3. `FACT_RESERVAS`
4. `FACT_PRESTACIONES`
5. Validaciones post-carga y cierre del log

---
## 7.3. Matriz de mapeo origen a destino (Source-to-Target Mapping)

### 7.3.1. Tablas de dimensiones

**`DIM_PACIENTE`** — origen: `01_PACIENTES`

| Campo destino   | Origen            | Transformación                                                                                                             | Regla |
| --------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------- | ----- |
| PacienteKey     | —                 | Clave sustituta autoincremental, `-1` = "Paciente desconocido"                                                             | —     |
| PacienteID      | `PacienteID`      | Mayúsculas, corresponde al ID del registro sobreviviente tras la deduplicación                                             | RN03  |
| Nombre          | `Nombre`          | Espacios múltiples colapsados, formato _Title Case_ conservando tildes (el origen trae nombre y apellido en un solo campo) | RN03  |
| Comuna          | `Comuna`          | _Title Case_, nulo → "Sin informar"                                                                                        | —     |
| FechaNacimiento | `FechaNacimiento` | Se conserva como fecha                                                                                                     | —     |
| Edad            | `FechaNacimiento` | Campo calculado: años cumplidos a la fecha de ejecución del ETL                                                            | —     |
| Previsión       | `Prevision`       | Estandarizar a "Fonasa" / "Isapre" (el origen trae `FONASA` e `Isapre`)                                                    | —     |
| Sexo            | `Sexo`            | `F`/`M` → "Femenino"/"Masculino"                                                                                           | —     |

_Filtros:_ se excluye la columna `Unnamed: 1` (100% nula) y se envían a cuarentena P031–P033 (todos los campos nulos salvo el ID). Ninguno de esos tres pacientes tiene reservas, por lo que no generan claves `-1` en los hechos.

**`DIM_MEDICO`** — origen: `02_MEDICOS`

| Campo destino   | Origen           | Transformación                                               | Regla |
| --------------- | ---------------- | ------------------------------------------------------------ | ----- |
| MedicoKey       | —                | Clave sustituta autoincremental, `-1` = "Médico desconocido" | —     |
| MedicoID        | `MedicoID`       | Mayúsculas                                                   | —     |
| Nombre          | `Medico`         | Se conserva el tratamiento (Dr./Dra.)                        | —     |
| EspecialidadID  | `EspecialidadID` | Mayúsculas (atributo de referencia)                          | —     |
| EspecialidadKey | —                | Búsqueda en `DIM_ESPECIALIDAD` por `EspecialidadID`          | RN01  |

**`DIM_ESPECIALIDAD`** — origen: `04_PRESTACIONES` (**no** `03_ESPECIALIDADES`)

| Campo destino      | Origen                            | Transformación                                                                                                             | Regla |
| ------------------ | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----- |
| EspecialidadKey    | —                                 | Clave sustituta autoincremental                                                                                            | —     |
| EspecialidadID     | `04_PRESTACIONES.EspecialidadID`  | `DISTINCT` tras normalizar (esperados 10 valores: E01–E10)                                                                 | RN01  |
| NombreEspecialidad | Tabla auxiliar `MAP_ESPECIALIDAD` | Se asigna el nombre maestro por `EspecialidadID`, cualquier variante de escritura se resuelve con `MAP_ALIAS_ESPECIALIDAD` | RN02  |

Ninguna tabla del origen contiene el nombre de la especialidad: `02_MEDICOS` solo trae el código y `03_ESPECIALIDADES` es una copia de médicos. Por eso el ETL usa dos tablas auxiliares (_seed_). Los nombres maestros se dedujeron de `04_PRESTACIONES.Prestacion` (por ejemplo, `PR003 Consulta Traumatología` pertenece a `E03`) y de los cuatro servicios históricos del centro.

|EspecialidadID|NombreMaestro|Evidencia en `04_PRESTACIONES`|
|---|---|---|
|E01|Medicina General|PR001 Consulta Medicina General, PR011 Control Médico|
|E02|Pediatría|PR002 Consulta Pediátrica, PR012 Control Pediátrico|
|E03|Traumatología|PR003 Consulta Traumatología, PR013 Control Traumatología|
|E04|Ginecología|PR004 Consulta Ginecológica|
|E05|Cardiología|PR005 Consulta Cardiología|
|E06|Dermatología|PR006 Consulta Dermatología, PR014 Procedimiento Dermatológico|
|E07|Neurología|PR007 Consulta Neurología|
|E08|Oftalmología|PR008 Consulta Oftalmología|
|E09|Endocrinología|PR009 Consulta Endocrinología|
|E10|Kinesiología|PR010 Sesión Kinesiología, PR015 Evaluación Kinesiológica|

| Alias detectado (ejemplos del negocio)     | Se estandariza a   |
| ------------------------------------------ | ------------------ |
| `Trauma`, `Traumatologia`, `TRAUMATOLOGIA` | Traumatología      |


Si aparece un `EspecialidadID` sin nombre en `MAP_ESPECIALIDAD`, la carga se detiene (severidad crítica) para no publicar una especialidad sin nombre.

**`DIM_PRESTACION`** — origen: `04_PRESTACIONES`

| Campo destino    | Origen           | Transformación                                    | Regla |
| ---------------- | ---------------- | ------------------------------------------------- | ----- |
| PrestacionKey    | —                | Clave sustituta autoincremental                   | —     |
| PrestacionID     | `PrestacionID`   | Mayúsculas                                        | —     |
| NombrePrestacion | `Prestacion`     | —                                                 | —     |
| EspecialidadID   | `EspecialidadID` | Normalizado, además se resuelve `EspecialidadKey` | RN01  |
| ValorListado     | `Valor`          | Convertir a numérico, validar `Valor ≥ 0`         | RN07  |

**`DIM_ESTADO_RESERVA`** — origen: catálogo fijo (el valor de `05_RESERVAS.EstadoReserva` se valida contra él)

|EstadoKey|EstadoReserva|Observación|
|---|---|---|
|1|Atendida|Única que genera prestaciones e ingresos (RN04, RN07)|
|2|Cancelada|No genera ingresos (RN05)|
|3|No asistió|Única que cuenta como hora perdida (RN06)|
|4|Pendiente|No aparece en el extracto, pero se modela por el proceso de negocio|

La comparación se hace sobre el texto normalizado (minúsculas, sin tildes, sin espacios sobrantes) para que, por ejemplo, `no asistio` coincida con "No asistió".

**`DIM_TIEMPO`** — origen: calendario generado

|Campo destino|Origen|Transformación|
|---|---|---|
|FechaKey|Fecha|Entero `AAAAMMDD`|
|Fecha, Día, Mes, Trimestre, Año|Fecha|Descomposición de la fecha|
|Nombre Mes, Día de semana|Fecha|Nombres en español (Enero…, Lunes…)|
|Es fin de semana|Día de semana|1 si es sábado o domingo|

_Rango:_ desde el 1 de enero del año de la primera reserva hasta el 31 de diciembre del año de la última. Con los datos actuales las reservas van del 05-01-2026 al 03-02-2026, por lo que el calendario cubre todo 2026.

### 7.3.2. Tablas de hechos

**`FACT_RESERVAS`** — grano: una fila por reserva · origen: `05_RESERVAS`

| Campo destino  | Origen          | Transformación / lookup                                                                                                              | Regla     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------- |
| ReservaID      | `ReservaID`     | Mayúsculas (PK degenerada)                                                                                                           | —         |
| PacienteKey    | `PacienteID`    | Búsqueda en tabla puente `MAP_PACIENTE` (ID origen → clave del sobreviviente). Sin coincidencia → `-1` y registro en `ETL_ERROR_LOG` | RN03      |
| MedicoKey      | `MedicoID`      | Búsqueda en `DIM_MEDICO`. Sin coincidencia → `-1` y registro en log                                                                  | —         |
| EstadoKey      | `EstadoReserva` | Normalizar y buscar en `DIM_ESTADO_RESERVA`. Fuera de catálogo → cuarentena                                                          | RN04–RN06 |
| FechaKey       | `FechaReserva`  | Convertir a `AAAAMMDD`                                                                                                               | —         |
| HoraReserva    | `HoraReserva`   | Convertir a formato `HH:MM` (el origen trae hora de Excel)                                                                           | —         |
| EsAtendida     | `EstadoReserva` | `1` si es "Atendida", `0` en otro caso                                                                                               | RN04      |
| EsInasistencia | `EstadoReserva` | `1` si es "No asistió", `0` en otro caso                                                                                             | RN06      |

**`FACT_PRESTACIONES`** — grano: una fila por prestación realizada · origen: `07_DETALLE_ATENCION` integrado con las demás tablas

`06_ATENCIONES.Diagnostico` y `Observacion` no se cargan: son datos clínicos que ninguna pregunta de negocio (RQ01–RQ24) requiere.

| Campo destino          | Origen                        | Transformación / lookup                                                                                          | Regla |
| ---------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------- | ----- |
| DetalleID              | `d.DetalleID`                 | Trim y mayúsculas (PK degenerada)                                                                                | —     |
| AtencionID / ReservaID | `d.AtencionID`, `a.ReservaID` | Se conservan como atributos degenerados para trazabilidad                                                        | RN08  |
| PacienteKey            | `r.PacienteID`                | Búsqueda en `MAP_PACIENTE`, sin coincidencia → `-1`                                                              | RN03  |
| MedicoKey              | `r.MedicoID`                  | Búsqueda en `DIM_MEDICO`                                                                                         | —     |
| EspecialidadKey        | `p.EspecialidadID`            | Búsqueda en `DIM_ESPECIALIDAD`. La especialidad se toma de la **prestación facturada**, no del médico (ver DQ13) | RN01  |
| PrestacionKey          | `d.PrestacionID`              | Búsqueda en `DIM_PRESTACION`                                                                                     | —     |
| FechaKey               | `a.FechaAtencion`             | Convertir a `AAAAMMDD` (coincide con `FechaReserva` en las 22 atenciones)                                        | —     |
| Cantidad               | `d.Cantidad`                  | Entero, validar `Cantidad > 0`                                                                                   | —     |
| ValorUnitario          | `d.ValorUnitario`             | Numérico, se usa el valor efectivamente cobrado y se compara con `p.Valor` como control                          | RN07  |
| IngresoLinea           | `Cantidad × ValorUnitario`    | Campo calculado                                                                                                  | RN07  |

---
## 7.4. Estrategia de calidad, excepciones y manejo de errores

### 7.4.1. Reglas de calidad aplicadas

| ID   | Control                                                                     | Tabla / campo                                            | Severidad   | Acción                                                                    | Origen del control |
| ---- | --------------------------------------------------------------------------- | -------------------------------------------------------- | ----------- | ------------------------------------------------------------------------- | ------------------ |
| DQ01 | La tabla es copia de `02_MEDICOS`                                           | `03_ESPECIALIDADES`                                      | Informativa | Descartar la tabla y construir `DIM_ESPECIALIDAD` desde `04_PRESTACIONES` | RN01, 5.3          |
| DQ02 | Columna 100% nula                                                           | `01_PACIENTES.Unnamed: 1`                                | Informativa | Excluir en la extracción                                                  | 5.3                |
| DQ03 | Registro con todos los campos nulos salvo el ID                             | `01_PACIENTES` (P031–P033)                               | Error       | Enviar a cuarentena y no cargar en `DIM_PACIENTE`                         | 5.3                |
| DQ04 | Estado fuera del catálogo de 4 valores                                      | `05_RESERVAS.EstadoReserva`                              | Error       | Enviar la reserva a cuarentena y alertar                                  | RN04–RN06          |
| DQ05 | Variantes de escritura de especialidad                                      | Fuentes anexas                                           | Corrección  | Normalizar con `MAP_ALIAS_ESPECIALIDAD`; alias desconocido → cuarentena   | RN02               |
| DQ06 | Paciente duplicado por diferencias de escritura                             | `01_PACIENTES`                                           | Corrección  | Consolidar bajo un único `PacienteID` (7.4.2)                             | RN03               |
| DQ07 | Llave primaria duplicada                                                    | Todas las tablas                                         | Crítica     | Detener la carga y reportar                                               | 5.2                |
| DQ08 | Clave foránea sin correspondencia                                           | `RESERVAS`, `ATENCIONES`, `DETALLE_ATENCION`             | Error       | Asignar `-1` en el hecho y registrar en el log                            | 5.4                |
| DQ09 | Reserva "Atendida" sin atención, o atención cuya reserva no está "Atendida" | `05_RESERVAS` / `06_ATENCIONES`                          | Error       | Excluir de `FACT_PRESTACIONES` y registrar                                | RN04               |
| DQ10 | `ValorUnitario` distinto de `Valor` maestro                                 | `07_DETALLE_ATENCION` / `04_PRESTACIONES`                | Advertencia | Cargar con `ValorUnitario` y registrar la diferencia                      | RN07               |
| DQ11 | `Cantidad ≤ 0` o valor negativo                                             | `07_DETALLE_ATENCION`, `04_PRESTACIONES`                 | Error       | Cuarentena del detalle                                                    | RN07               |
| DQ12 | Fecha u hora inválida o nula                                                | `05_RESERVAS`, `06_ATENCIONES`                           | Error       | Cuarentena del registro                                                   | —                  |
| DQ13 | Especialidad de la prestación distinta de la del médico                     | `07_DETALLE_ATENCION` / `04_PRESTACIONES` / `02_MEDICOS` | Advertencia | Cargar con la especialidad de la prestación y registrar (5 casos)         | Hallazgo nuevo     |

**DQ13 — Detalle del hallazgo.** En 5 de las 22 prestaciones realizadas la especialidad de la prestación no coincide con la del médico que atendió:

|DetalleID|Médico (especialidad)|Prestación facturada (especialidad)|
|---|---|---|
|DA003, DA017|M004 Dra. Marcela Rojas (E04 Ginecología)|PR003 Consulta Traumatología (E03)|
|DA007, DA014|M010 Dra. Valentina Pérez (E10 Kinesiología)|PR009 Consulta Endocrinología (E09)|
|DA022|M010 Dra. Valentina Pérez (E10 Kinesiología)|PR011 Control Médico (E01)|

El ETL **no corrige** estos registros porque no hay evidencia de cuál campo es el erróneo, los carga con la especialidad de la prestación (lo cobrado) y los deja registrados como advertencia. Consecuencia para el análisis: los ingresos por especialidad (`FACT_PRESTACIONES`) y las reservas por especialidad vía médico (`FACT_RESERVAS`) no sumarán lo mismo en esas especialidades.

### 7.4.2. Consolidación de pacientes duplicados (RN03)

En la base actual no hay duplicados (los 30 pacientes completos tienen nombre normalizado único), pero el negocio describe variantes como _Juan Pérez_, _Juan A. Pérez_ y _JUAN PEREZ_. El ETL incluye el control como medida preventiva:

1. **Normalizar** el nombre completo: minúsculas, sin tildes, sin puntuación, espacios colapsados y sin iniciales sueltas (`juan a perez` → `juan perez`).
2. **Generar la clave de comparación** con el nombre normalizado. Para no fusionar homónimos (en el perfilamiento "Pérez" aparece 5 veces entre personas distintas) se compara siempre el nombre completo y, cuando existan, se refuerza con sexo y edad o fecha de nacimiento.
3. **Elegir el sobreviviente:** el registro más completo y, en empate, el de menor `PacienteID`.
4. **Registrar la equivalencia** en la tabla puente `MAP_PACIENTE (PacienteID_origen → PacienteKey)`, de modo que las reservas de los IDs duplicados apunten al paciente consolidado.
5. Los pares con coincidencia parcial (similitud difusa sin coincidencia exacta) no se fusionan automáticamente: pasan a revisión manual.

La función de normalización y la clave de comparación están en el script de referencia (7.6): `normalizar()` y `clave_paciente()`.

`normalizar()` se reutiliza para especialidades (RN02) y para el estado de la reserva.

### 7.4.3. Manejo de excepciones y trazabilidad

**Niveles de severidad**

| Nivel       | Comportamiento                                     | Ejemplos                           |
| ----------- | -------------------------------------------------- | ---------------------------------- |
| Crítica     | Detiene la ejecución y no se carga nada            | Hoja faltante, PK duplicada (DQ07) |
| Error       | El registro va a cuarentena; la carga continúa     | DQ03, DQ04, DQ09, DQ11, DQ12       |
| Corrección  | El dato se corrige y se registra el valor original | DQ05, DQ06                         |
| Advertencia | Se carga el registro y se deja el aviso            | DQ10, DQ13                         |

**Tablas de control**

| Tabla               | Campos principales                                                                      | Uso                                                                     |
| ------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `ETL_LOG_EJECUCION` | EjecucionID, FechaInicio, FechaFin, Estado, FilasLeidas, FilasCargadas, FilasRechazadas | Una fila por ejecución del proceso                                      |
| `ETL_ERROR_LOG`     | EjecucionID, Tabla, Campo, ValorOriginal, CodigoDQ, Severidad, Accion, Fecha            | Detalle de cada incidencia                                              |
| `QUARANTINE_*`      | Copia del registro rechazado + CodigoDQ                                                 | Permite revisarlo y reprocesarlo una vez corregido en el sistema origen |

**Reprocesamiento:** como la carga es _full refresh_, volver a ejecutar el ETL con la fuente corregida produce el mismo resultado sin duplicar datos (proceso idempotente).

### 7.4.4. Validaciones post-carga (conciliación)

|Validación|Resultado obtenido con la base actual|
|---|---|
|Filas en `DIM_PACIENTE`|30 (33 menos 3 en cuarentena) más el miembro `-1`|
|Filas en `DIM_MEDICO`|10 más el miembro `-1`|
|Filas en `DIM_ESPECIALIDAD`|10|
|Filas en `DIM_PRESTACION`|15|
|Filas en `DIM_ESTADO_RESERVA`|4|
|Filas en `FACT_RESERVAS`|30 = filas de `05_RESERVAS` (22 Atendida, 4 No asistió, 4 Cancelada, 0 Pendiente)|
|Filas en `FACT_PRESTACIONES`|22 = detalles de atenciones "Atendida"|
|Suma de `IngresoLinea`|$805.000, igual a la suma de `Cantidad × ValorUnitario` del origen|
|Filas de hecho con clave `-1`|0|
|Incidencias en `ETL_ERROR_LOG`|3 errores DQ03 (P031–P033) y 5 advertencias DQ13|

Si alguna validación falla, la ejecución se marca como "Con errores" en `ETL_LOG_EJECUCION` y no se publica el Data Mart hasta revisar la diferencia.

---

## Véase también
- [[_MOC|MOC Inteligencia de Negocio]]
- [[01_Explicacion_Business_Intelligence|Fundamentos de Business Intelligence]]
- [[02_Explicacion_Clase2_BI|Data Warehouses y Bodegas de Datos]]
- [[03_Explicacion_OLTP_a_OLAP|De Sistemas OLTP a OLAP — Modelado Dimensional]]
- [[Lab03_VentasDW|Lab 03 — VentasDW]]
- [[Data Warehouse]]
- [[OLTP vs OLAP]]
- [[ETL]]


