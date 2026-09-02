
## EJERCICIO 1 — EMPRESA AGRÍCOLA "AGROTECH"

### 1.Análisis del negocio 

**Descripción del problema**: AGROTECH actualmente no tiene una visión clara de como se comporta su producción agrícola, no tiene claridad de cual de sus cultivo tuvo mejor rendimiento, ni mucho menos de su calidad de producción. 

**Proceso de negocio seleccionado**: Proceso de **Cosecha** (producción agrícola). Es el proceso operativo que genera los eventos medibles (kg cosechados, calidad, merma, horas trabajadas) y es la base para luego analizar comercialización

**Objetivo del análisis**: Desarrollar una idea BI para poder analizar la productividad agrícola y el comportamiento de la producción, medir y comparar la productividad y calidad de la producción agrícola por campo, parcela, cultivo, variedad y temporada, para apoyar decisiones de planificación agrícola y asignación de recursos.

### 2.Tabla hechos

`DetalleCosecha` es la única que cumple las tres condiciones de forma directa: tiene las medidas reales (kg, calidad, merma) que la gerencia quiere analizar.
Algunos autores (ej. Kimball) recomiendan nombrar la fact table según el **proceso de negocio** (`Fact_Cosecha`) en vez del nombre técnico de la tabla origen (`DetalleCosecha`), porque es más claro para el usuario de negocio.

### 3.Indicacion de dimensiones 

| Dimensión         | PK           | Atributos                                                                              | Descripción                                                                 |
| ----------------- | ------------ | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Dim_Tiempo**    | id_tiempo    | fecha, día, nombre_día, semana, mes, nombre_mes, trimestre, semestre, año              | Fecha de la cosecha, permite análisis temporal                              |
| **Dim_Parcela**   | id_parcela   | superficie_parcela, ubicación_parcela, nombre_campo, ubicación_campo, superficie_campo | Parcela cosechada, con atributos del campo denormalizados (evita snowflake) |
| **Dim_Variedad**  | id_variedad  | nombre_variedad, nombre_cultivo, tipo_cultivo                                          | Variedad cosechada, con atributos de Cultivo denormalizados                 |
| **Dim_Temporada** | id_temporada | nombre_temporada, fecha_inicio, fecha_fin                                              | Temporada agrícola en la que ocurre la cosecha                              |
**id_tiempo, fecha, día, nombre_día, semana, mes, nombre_mes, trimestre, semestre, año — cumple el mínimo pedido.**

### 4. Modelo dimensional (estrella)


### 5.Preguntas de negocio

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
---

## EJERCICIO 2 — EMPRESA DE TELECOMUNICACIONES "CONECTA"

### 1.Análisis del negocio 
*Descripción del problema - Proceso de negocio seleccionado - Objetivo del análisis*


### 2.Tabla hechos


### 3.Indicacion de dimensiones 


### 4. Modelo dimensional (estrella)


### 5.Preguntas de negocio