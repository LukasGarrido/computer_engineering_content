*Entrega 1 - 2*
- Inteligencia de negocio 
- Octavio Valencia - Lukas Garrido
- Paralelo 701

---
# 1.Análisis del negocio
## Historia

SaludVital es un centro medico privado que provee servicios de atención **ambulatoria** a pacientes de la Región del Bio Bio. Inicio como un pequeño centro de atención medica, el cual actualmente lleva 8 años operando. En sus inicios contaba solamente con cierto servicios, como: Medicina general, Pediatría, Ginecología, Traumatología.

Debido a la alta demanda, cuenta con **10 especialidades medicas** y mas de 20 profesionales. Actualmente, el centro SaludVital atiende aproximadamente 2000 consultas mensuales. La reserva de horas se realiza de manera presencial en recepción, por teléfono, vía sitio web o a través de su aplicación móvil.

A pesar de este crecimiento, la arquitectura de los sistemas de información actuales no fue diseñada para un análisis multidimensional de los datos, lo que limita la explotación estratégica de su volumen de información. 

--- 
# Situación actual

Actualmente, SaludVital cuenta con un sistema que no satisface el análisis multidimensional de los datos. Esta limitación genera diversos problemas, como: información distribuida, Pacientes duplicados, Especialidades inconsistentes, etc. 

---
## Actores

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
## Procesos

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
## Problemas

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
## Objetivos

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

# 2.Reglas de negocio

## Catalogo de reglas

*Un catalogo de reglas de negocio es una lista ordenada y documentada que recopila las condiciones, restricciones, políticas y normas bajo las cuales opera una organización*

*Al analizar `SALUDVITAL_2BaseDatos.xlsx`, se detectó que la tabla `03_ESPECIALIDADES`esta errónea (es una copia exacta de `02_MEDICOS` ), por lo que RN01 para deducir las 10 especialidades a partir de las prestaciones, garantizando la integridad del modelo dimensional.*

### 1. Reglas sobre Limpieza y Estructura de Datos (ETL)

| **ID**   | **Regla**                                                                                                                                                                                                                                                                                               | **Impacto**                          |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| **RN01** | **Reconstrucción de Especialidades:** Dado que la tabla `03_ESPECIALIDADES` contiene datos erróneos (duplica `02_MEDICOS` ), los registros de `03_ESPECIALIDADES` deben ser deducidos y construidos durante el ETL extrayendo los códigos únicos (`EspecialidadID`) desde la tabla "`04_PRESTACIONES`". | Proceso ETL / Dimensión Especialidad |
| **RN02** | **Normalización de Nombres:** Cualquier variación tipográfica o error de escritura en especialidades detectada en fuentes anexas (ej. _Trauma, TRAUMATOLOGIA_) debe estandarizarse a su nombre **maestro** deducido (ej. "Traumatología").                                                              | Proceso ETL / Limpieza de Datos      |
| **RN03** | **Unificación de Pacientes:** Los registros duplicados de pacientes con diferencias de capitalización, puntuación o abreviaturas (ej. _Juan Pérez vs JUAN PEREZ_) deben consolidarse bajo un único `PacienteID`.                                                                                        | Proceso ETL / Dimensión Paciente     |

### 2. Reglas Operativas y de Atención

| **ID**   | **Regla**                                                                                                                                                              | **Impacto**                                           |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **RN04** | **Atenciones Efectivas:** Una reserva solo se considera como "atención efectiva" (y genera prestaciones realizadas) si su `EstadoReserva` es estrictamente "Atendida". | KPI (Atenciones realizadas, Tasa de atención)         |
| **RN05** | **Inasistencias y Cancelaciones:** Las reservas en estado "Cancelada", "Pendiente" o "No asistió" no generan ingresos ni prestaciones.                                 | KPI (Ingresos, Tasa de inasistencia)                  |
| **RN06** | **Horas Perdidas:** Exclusivamente el estado "No asistió" se contabilizará negativamente para evaluar el desempeño de la utilización de horas del profesional médico.  | KPI (Utilización de horas / Dashboard Gestión Médica) |

### 3. Reglas Financieras y de Modelo Dimensional

| **ID**   | **Regla**                                                                                                                                                                                                                                  | **Impacto**                          |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------ |
| **RN07** | **Cálculo de Ingresos:** Los ingresos se calculan sumando el valor monetario (`Valor` en la tabla PRESTACIONES) únicamente de las atenciones con estado "Atendida".                                                                        | Medidas DAX / KPI Ingresos           |
| **RN08** | **Granularidad del Hecho Principal:** El nivel más detallado de la tabla de hechos corresponde a la **prestación individual realizada** dentro de una atención, vinculando al paciente, el médico, la especialidad, la reserva y la fecha. | Modelo Dimensional (Tabla de Hechos) |
