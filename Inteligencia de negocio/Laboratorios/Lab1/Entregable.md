
## EJERCICIO 1 — EMPRESA AGRÍCOLA "AGROTECH"

### 1. Análisis del negocio 

**Descripción del problema**: AGROTECH actualmente no tiene una visión clara de como se comporta su producción agrícola, no tiene claridad de cual de sus cultivo tuvo mejor rendimiento, ni mucho menos de su calidad de producción. 

**Proceso de negocio seleccionado**: Proceso de **Cosecha** (producción agrícola). Es el proceso operativo que genera los eventos medibles (kg cosechados, calidad, merma, horas trabajadas) y es la base para luego analizar comercialización.

**Objetivo del análisis**: Desarrollar una idea BI para poder analizar la productividad agrícola y el comportamiento de la producción, medir y comparar la productividad y calidad de la producción agrícola por campo, parcela, cultivo, variedad y temporada, para apoyar decisiones de planificación agrícola y asignación de recursos.

### 2. Tabla hechos

`DetalleCosecha` es la única que cumple las tres condiciones de forma directa: tiene las medidas reales (kg, calidad, merma) que la gerencia quiere analizar.
Algunos autores (ej. Kimball) recomiendan nombrar la fact table según el **proceso de negocio** (`Fact_Cosecha`) en vez del nombre técnico de la tabla origen (`DetalleCosecha`), porque es más claro para el usuario de negocio.

### 3. Indicación de dimensiones 

| Dimensión         | PK           | Atributos                                                                              | Descripción                                                                 |
| ----------------- | ------------ | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Dim_Tiempo**    | id_tiempo    | fecha, día, nombre_día, semana, mes, nombre_mes, trimestre, semestre, año              | Fecha de la cosecha, permite análisis temporal                              |
| **Dim_Parcela**   | id_parcela   | superficie_parcela, ubicación_parcela, nombre_campo, ubicación_campo, superficie_campo | Parcela cosechada, con atributos del campo denormalizados (evita snowflake) |
| **Dim_Variedad**  | id_variedad  | nombre_variedad, nombre_cultivo, tipo_cultivo                                          | Variedad cosechada, con atributos de Cultivo denormalizados                 |
| **Dim_Temporada** | id_temporada | nombre_temporada, fecha_inicio, fecha_fin                                              | Temporada agrícola en la que ocurre la cosecha                              |

### 4. Modelo dimensional (estrella)

<img width="797" height="443" alt="image" src="https://github.com/user-attachments/assets/7fe55509-6266-4aaf-98d7-efc771621469" />

### 5. Preguntas de negocio

- ¿Cuál fue el rendimiento (kg cosechados) por parcela durante una temporada específica?
- ¿Qué variedad de cultivo tuvo mayor volumen cosechado en un trimestre determinado?
- ¿Cómo varía el porcentaje de merma promedio por campo?
- ¿Cuál es la tendencia mensual del total de kg cosechados durante el año?
- ¿Qué parcelas presentan menor rendimiento (kg/hora trabajada)?
- ¿Cuál es la producción total por semestre para cada tipo de cultivo?
- ¿Qué campo mostró mayor crecimiento de producción respecto a la temporada anterior?
- ¿Cuántas horas trabajadas se registraron por semana en cada campo?
- ¿Cuál es la calidad promedio de la cosecha por variedad y temporada?
- ¿Qué parcelas requieren mayor cantidad de trabajadores por evento de cosecha?

### 6. Relación pregunta -> modelo

| Pregunta | Dimensiones utilizadas | Medidas utilizadas |
| :--- | :--- | :--- |
| ¿Cuál fue el rendimiento (kg cosechados) por parcela durante una temporada específica? | Dim_Parcela, Dim_Temporada | cantidad_kg |
| ¿Qué variedad de cultivo tuvo mayor volumen cosechado en un trimestre determinado? | Dim_Variedad, Dim_Tiempo | cantidad_kg |
| ¿Cómo varía el porcentaje de merma promedio por campo? | Dim_Parcela | porcentaje_merma |
| ¿Cuál es la tendencia mensual del total de kg cosechados durante el año? | Dim_Tiempo | cantidad_kg |
| ¿Qué parcelas presentan menor rendimiento (kg/hora trabajada)? | Dim_Parcela | cantidad_kg, horas_trabajadas_totales |
| ¿Cuál es la producción total por semestre para cada tipo de cultivo? | Dim_Variedad, Dim_Tiempo | cantidad_kg |
| ¿Qué campo mostró mayor crecimiento de producción respecto a la temporada anterior? | Dim_Parcela, Dim_Temporada | cantidad_kg |
| ¿Cuántas horas trabajadas se registraron por semana en cada campo? | Dim_Parcela, Dim_Tiempo | horas_trabajadas_totales |
| ¿Cuál es la calidad promedio de la cosecha por variedad y temporada? | Dim_Variedad, Dim_Temporada | calidad |
| ¿Qué parcelas requieren mayor cantidad de trabajadores por evento de cosecha? | Dim_Parcela | cantidad_trabajadores |

### 7. Justificación

`Fact_DetalleCosecha` cumple las condiciones de una tabla de hechos porque registra un evento medible y repetible (cada cosecha realizada sobre una parcela), contiene medidas numéricas aditivas (kg cosechados, horas trabajadas, merma) y crece de forma continua en el tiempo. `Dim_Parcela`, `Dim_Variedad`, `Dim_Temporada` y `Dim_Tiempo` son dimensiones porque son entidades relativamente estables que dan contexto al hecho ("¿dónde?", "¿qué se cosechó?", "¿cuándo?"), y se usan como criterios de filtro y agrupación en el análisis. Campo y Cultivo se denormalizan dentro de `Dim_Parcela` y `Dim_Variedad` respectivamente para evitar un esquema copo de nieve innecesario. El grano elegido —un registro por detalle de cosecha— es el más fino disponible con medidas propias en el MER: un grano más agregado (por temporada) impediría responder preguntas a nivel de parcela o fecha específica, y uno más fino (por trabajador) rompería la aditividad de los kilos cosechados.

---
## EJERCICIO 2 — EMPRESA DE TELECOMUNICACIONES "CONECTA"

### 1.Análisis del negocio 

**Descripción del problema:** Conecta no tiene visibilidad clara sobre cómo consumen sus servicios los clientes (Internet, TV, telefonía), lo que dificulta detectar patrones de uso, anticipar saturación de red y evaluar el desempeño comercial de cada plan.

**Proceso de negocio seleccionado:** **Consumo de servicios**. Es el proceso que genera el mayor volumen de eventos medibles y repetibles (cada cliente consume servicio todos los días), y es la base para luego analizar ingresos, calidad y soporte.

**Objetivo del análisis:** Se desea implementar una solución de BI para analizar el comportamiento de los clientes, calidad del servicio y soporte técnico. Medir y comparar el consumo de servicios por cliente, plan y ubicación a lo largo del tiempo, para apoyar decisiones comerciales y de capacidad de red.
### 2.Tabla hechos


### 3.Indicacion de dimensiones 


### 4. Modelo dimensional (estrella)


### 5.Preguntas de negocio

- ¿Cuál es el consumo total de datos por cliente en un mes?
- ¿Qué plan genera mayor consumo promedio diario?
- ¿Cómo varía el consumo total por región/ciudad?
- ¿Qué segmento de clientes consume más servicio?
- ¿Cuál es la tendencia de consumo mensual durante el año?
- ¿Qué contratos muestran consumo decreciente en los últimos 3 meses?
- ¿Cuál es el consumo promedio por trimestre según plan?
- ¿Qué clientes superan el consumo esperado para su plan contratado?
- ¿Cuál es el día de la semana con mayor consumo total?
- ¿Cómo se compara el consumo entre clientes nuevos (<6 meses) y antiguos?

- 
---

## EJERCICIO 3 — EMPRESA DE ENTRETENIMIENTO "EVENTIA"

### 1.Análisis del negocio 

**Problema:** Eventia no puede medir fácilmente el desempeño comercial de sus eventos: qué tan bien se venden las entradas, qué canales funcionan mejor, ni cómo varía la ocupación de los recintos.

**Proceso de negocio seleccionado:** **Venta de entradas**. Es el proceso transaccional central que genera ingresos y refleja el comportamiento comercial de los eventos.

**Objetivo del análisis:** Medir el volumen e ingresos de venta de entradas por evento, cliente, tipo de entrada y canal, a lo largo del tiempo, para optimizar la comercialización.

### 2.Tabla hechos


### 3.Indicacion de dimensiones 


### 4. Modelo dimensional (estrella)


### 5.Preguntas de negocio

- ¿Cuál es el evento con mayor cantidad de entradas vendidas en el mes?
- ¿Qué canal de venta genera mayores ingresos?
- ¿Cuál es la ocupación (%) de cada recinto por evento?
- ¿Qué tipo de entrada (VIP, general) es más vendido?
- ¿Cómo varían las ventas según el tramo etario del cliente?
- ¿Cuál es el ingreso total por trimestre para eventos deportivos vs. conciertos?
- ¿Qué eventos presentan mayor descuento promedio aplicado?
- ¿Cuál es el ticket promedio de compra por cliente?
- ¿Qué ciudad concentra mayor volumen de ventas de entradas?
- ¿Cómo evoluciona la venta de entradas en las semanas previas a un evento?
