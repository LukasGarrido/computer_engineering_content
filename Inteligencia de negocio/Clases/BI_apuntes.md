# Business Intelligence — Apuntes Completos de Estudio

> Documento consolidado a partir de cuatro materiales de clase:
> 1. **Clase_1.pdf** — "Business Intelligence" 
> 2. **Clase_2.pdf** — "Inteligencia de Negocios" (2026, Semestre 2) — De los datos a la decisión: DSS, BI, machine learning y arquitecturas analíticas modernas.
> 3. **Lab_Clase_2.pdf** — "BI en acción: áreas, componentes y ciclo de vida" (Clase 2, Carrera de Ciencia de Datos, sesión práctica de 3 horas)
> 4. **De un MER a un Modelo Dimensional.pdf** — Clase práctica de Inteligencia de Negocios, caso aplicado: Empresa de Energía "Energía Sur"

---

# PARTE 1 — CLASE 1: "Business Intelligence"

## 1.1 Portada
- Título: **Business Intelligence**
- Autora: Alexandra Matus Gacitúa
- Cargo/formación: Ingeniería Informática | Mg. Tecnologías de la Información
- Contacto: Alexandra.matus@usm.cl

## 1.2 Ejemplos ilustrativos de empresas reales (¿cómo toman decisiones?)

### Amazon (slide 02)
- **Idea central:** Cada visita al sitio genera datos que alimentan la siguiente decisión comercial.
- **Qué decide:** Qué producto mostrar a cada visitante, a qué precio, y desde qué bodega despacharlo.
- **Qué datos usa:** Búsquedas, clics, carritos, historial de compra, stock y tiempos logísticos de cada centro de distribución.
- **Cómo decide:** Recomendación, precios dinámicos y pronóstico de demanda que repone inventario antes de la compra.
- **Frase clave:** "La decisión no la toma la intuición: la toma el dato, y se corrige todos los días."

### Mercado Libre (slide 03)
- **Idea central:** Un marketplace debe decidir en segundos en quién confiar y qué mostrar.
- **Qué decide:** Qué publicaciones destacar, qué vendedores son confiables, y a qué usuarios ofrecer crédito.
- **Qué datos usa:** Búsquedas y compras, reputación y reclamos, seguimiento de envíos e historial de pagos.
- **Cómo decide:** Buscadores y recomendadores, modelos antifraude y evaluación crediticia con datos transaccionales.
- **Frase clave:** "La confianza del marketplace se sostiene en datos, no en percepciones."

### Coca-Cola (slide 04)
- **Idea central:** No vende directo al consumidor: sus decisiones dependen de integrar datos de terceros (embotelladores/distribuidores).
- **Qué decide:** Cuánto producir, dónde distribuir y cómo ejecutar cada punto de venta.
- **Qué datos usa:** Ventas de embotelladores y distribuidores, desempeño por canal, estacionalidad, clima y campañas.
- **Cómo decide:** Consolida a sus socios en un repositorio común y proyecta la demanda por región, canal y formato.
- **Frase clave:** "Eso es Business Intelligence: convertir datos dispersos en una decisión mejor."

> **Patrón común de los 3 casos:** siempre hay una estructura de análisis "Qué decide → Qué datos usa → Cómo decide", que resume el ciclo completo de BI aplicado a un negocio real.

## 1.3 ¿Qué es Business Intelligence? (slide 05)

### Definición de Gartner
> Conjunto de metodologías, procesos, arquitecturas y tecnologías que transforman datos operacionales en bruto en información significativa y accionable, para habilitar decisiones estratégicas, tácticas y operativas.

### Definición práctica
- BI consiste en **capturar datos, organizarlos, analizarlos y convertirlos en decisiones concretas** para el negocio.
- Es decir: menos discusión sobre qué número es correcto y más tiempo dedicado a decidir qué hacer con él.

### Flujo conceptual
```
Capturar → Organizar → Analizar → Decidir
```

## 1.4 ¿Por qué surge Business Intelligence? (slide 06)

### Problemas que le dieron origen
- Información duplicada en distintos sistemas.
- Múltiples bases de datos sin integración.
- Datos inconsistentes entre áreas.
- Reportes diferentes para un mismo indicador.
- Decisiones lentas por falta de información.
- Exceso de planillas Excel manuales.

### El síntoma más común
- Cada área construye su propia versión de los números y nadie sabe cuál es la correcta.
- **El costo no es tecnológico: es la pérdida de confianza en la información.**

## 1.5 Ejemplo: ¿cuál es la cifra correcta? (slide 07)

El problema de las múltiples verdades, ilustrado con un ejemplo de ventas reportadas de forma distinta por cada área:
- **Ventas informa:** $1.250 millones
- **Finanzas informa:** $1.180 millones
- **Gerencia informa:** $1.310 millones

**Pregunta:** ¿Cuál es correcto?

**Conclusión:** BI busca una única versión de la verdad — **Single Source of Truth (SSOT)**.

## 1.6 Objetivos de Business Intelligence (slide 08)

Para qué se implementa BI:
- Apoyar decisiones
- Detectar oportunidades
- Reducir riesgos
- Automatizar reportes
- Descubrir patrones
- Pronosticar ventas
- Medir indicadores

**Conclusión:** Todos estos objetivos convergen en un mismo fin: **decidir mejor y más rápido**.

## 1.7 Niveles de decisión en la organización (slide 09)

Cada nivel de la organización necesita información distinta:

| Nivel | Quién | Tipo de información |
|---|---|---|
| **Estratégico** | Alta Gerencia | Visión de largo plazo, tendencias y proyecciones |
| **Táctico** | Jefaturas y Supervisores | Seguimiento mensual, comparaciones y desviaciones |
| **Operacional** | Usuarios del negocio | Detalle diario, transacciones y control de gestión |

**Idea clave:** La misma solución BI debe servir a los tres niveles, pero con distinto grado de detalle (esto se relaciona con el concepto de "granularidad" que se ve más adelante).

## 1.8 Evolución hacia la Inteligencia de Negocios (línea de tiempo tecnológica, slide 10)

Cada etapa amplía la capacidad de convertir datos en decisiones:

| Década | Sigla/Nombre | Descripción |
|---|---|---|
| **1960s** | **TPS** — Sistemas transaccionales | Mainframe y procesos por lotes: registran las operaciones diarias. |
| **1970s** | **MIS** — Sistemas de información de gestión | Bases de datos relacionales: reportes periódicos para las jefaturas. |
| **1980s** | **DSS** — Sistemas de apoyo a decisiones | Modelos y planillas: simulaciones "qué pasaría si". |
| **1985–1990** | **EIS** — Sistemas de información ejecutiva | Tableros con los indicadores clave para la alta dirección. |
| **1990s** | **Business Intelligence** | Data warehouse, ETL y OLAP: una sola versión de la verdad, con informes y dashboards. |
| **2000s** | **Big Data** | Hadoop, NoSQL y nube: volumen, velocidad y variedad de datos no estructurados. |
| **2010s** | **Machine Learning** | Modelos predictivos: del reporte del pasado a la anticipación del futuro. |
| **2020s** | **Inteligencia Artificial** | IA generativa y analítica aumentada: consultas en lenguaje natural y decisiones en tiempo real. |

---

# PARTE II — Componentes principales de una solución BI

## 1.9 Arquitectura de referencia de una solución BI (slide 11-12)

Elementos principales (flujo de izquierda a derecha):

```
Fuentes → Integración → Almacenamiento → Análisis → Explotación
```

- **Fuentes:** OLTP, ERP/CRM, APIs, logs, IoT.
- **Integración:** Extracción, limpieza, transformación, carga.
- **Almacenamiento:** Staging, DW (Data Warehouse), data marts, ODS.
- **Análisis:** Motor OLAP, cubos, capa semántica.
- **Explotación:** Tableros, informes, self-service.

**Capa transversal** (aplica a todas las capas): metadatos, catálogo de datos, seguridad y control de acceso, linaje, orquestación y monitoreo.

**Puntos críticos:**
- El flujo es **unidireccional**: cada capa desacopla la operación transaccional del análisis.
- El punto crítico de diseño es la **integración**: concentra entre el **60% y el 80%** del esfuerzo del proyecto.

## 1.10 1. Fuentes de Datos (slide 13)

El origen de todo el proceso. Categorías:
- **Sistemas de negocio:** ERP · CRM · POS · RRHH
- **Datos operativos:** Sensores IoT · APIs · Archivos CSV · Excel
- **Bases de datos:** SQL · Oracle · PostgreSQL · MongoDB
- **Canales digitales:** Redes sociales · Web · E-commerce

**Regla:** Mientras más diversas son las fuentes, más crítico es el proceso de integración.

## 1.11 2. ETL: Extract, Transform, Load (slide 14)

```
Extract → Transform → Load
```

Actividades típicas de la transformación:
- Eliminar registros duplicados.
- Homologar nombres y códigos.
- Corregir errores de captura.
- Convertir monedas y unidades.
- Integrar múltiples sistemas.

**¿Por qué es la etapa crítica?**
El ETL concentra la mayor parte del esfuerzo de un proyecto BI. **Un dashboard elegante construido sobre datos sucios entrega decisiones equivocadas con apariencia de rigor.**

## 1.12 ELT: el enfoque moderno (slide 15)

```
Extract → Load → Transform
```

Características:
- Los datos se cargan primero, sin transformar.
- La transformación ocurre dentro del Data Warehouse.
- Escala mejor con grandes volúmenes.
- Aprovecha el poder de cómputo de la nube.

**ETL vs. ELT:**
- **ETL** transforma antes de cargar y funciona bien con volúmenes acotados.
- **ELT** carga primero y transforma después: es el estándar en arquitecturas cloud.

## 1.13 Calidad de datos y gobierno (slide 16)

### Las 6 dimensiones de calidad de datos
| Dimensión | Definición |
|---|---|
| **Exactitud** | El valor refleja la realidad que representa. |
| **Completitud** | Ausencia de nulos en atributos obligatorios. |
| **Consistencia** | Sin contradicciones entre sistemas y períodos. |
| **Oportunidad** | Disponible dentro de la ventana de decisión. |
| **Unicidad** | Una sola entidad por registro; sin duplicados. |
| **Validez** | Conforme a dominios, formatos y reglas de negocio. |

### Gobierno de datos
- **Propiedad y custodia explícitas:** el *data owner* responde por el dato; el *data steward* responde por su calidad diaria.
- **Gestión de datos maestros (MDM):** un identificador único de cliente, producto y proveedor para todo el ecosistema.
- **Linaje y metadatos:** trazabilidad de origen a indicador; requisito para auditoría y para el análisis de impacto.

## 1.14 3. Data Warehouse (slide 17)

**Definición:** El repositorio corporativo. Sus 5 características clave (según Inmon):

| Característica | Explicación |
|---|---|
| **Variante en el tiempo** | Conserva la historia: cada registro es válido en un horizonte temporal. |
| **Integrado** | Nomenclatura, unidades y codificación homogéneas entre fuentes. |
| **Consistente** | Definiciones únicas y homologadas para toda la organización. |
| **No volátil** | Se carga y se consulta; no se actualiza transaccionalmente. |
| **Temático** | Organizado por asunto de negocio, no por aplicación. |

**Modelo integrado (dimensiones típicas):** Ventas · Clientes · Productos · Tiempo · Sucursales · Empleados.
Todas las áreas comparten las mismas dimensiones y definiciones.

## 1.15 Modelado dimensional: hechos y dimensiones (slide 18)

**Esquema en estrella:** una tabla de hechos rodeada de dimensiones desnormalizadas.

```
                DIM_TIEMPO
                    |
DIM_CLIENTE — HECHO_VENTAS — DIM_PRODUCTO
                    |
                DIM_TIENDA
```

- **HECHO_VENTAS** contiene: unidades · monto neto · descuento. Granularidad: línea de boleta.
- **Tabla de hechos:** métricas numéricas aditivas y claves foráneas. **Declarar la granularidad** —el nivel de detalle de cada fila— es **la primera y más determinante decisión del diseño**.
- **Dimensiones:** atributos descriptivos que dan contexto al hecho y definen los ejes de filtrado, agrupación y jerarquía.

## 1.16 4. Data Mart (slide 19)

**Definición:** Un subconjunto del Data Warehouse. Cada área del negocio accede a la porción de información que necesita, sin navegar todo el repositorio corporativo.

Ejemplos:
- **Data Mart Comercial:** Ventas, clientes, canales y cumplimiento de metas.
- **Data Mart Finanzas:** Márgenes, costos, presupuesto y rentabilidad.
- **Data Mart RRHH:** Dotación, rotación, ausentismo y desempeño.

**Advertencia:** Un Data Mart mal gobernado vuelve a crear silos: **debe derivar siempre del Data Warehouse**.

## 1.17 5. Cubos OLAP (slide 20)

Analizar desde múltiples perspectivas. Ejemplo de jerarquía de análisis de ventas:

```
Ventas → por ciudad → por vendedor → por producto → por fecha → por cliente
```

### Operaciones OLAP
| Operación | Descripción |
|---|---|
| **Roll-up** | Agrega subiendo por una jerarquía: de día a mes (o de comuna a región). |
| **Drill-down** | Desagrega hacia el detalle para explicar una desviación observada. |
| **Slice** | Fija una dimensión y obtiene un subcubo menor. |
| **Dice** | Restringe varias dimensiones con un rango de valores. |
| **Pivot** | Rota los ejes para mirar las mismas medidas de otro modo. |
| **Drill-through** | Baja hasta la transacción de origen en el sistema operacional. |

**Concepto de cubo:** organiza medidas a lo largo de ejes dimensionales; cada celda es una agregación precalculada o resuelta al vuelo.

## 1.18 Implementaciones OLAP y rendimiento (slide 21)

| Aspecto | ROLAP | MOLAP | HOLAP |
|---|---|---|---|
| **Almacenamiento** | Tablas relacionales del DW | Estructuras multidimensionales propietarias | Detalle relacional, agregados multidimensionales |
| **Escalabilidad** | Alta; limitada por el motor SQL | Menor: el cubo crece de forma explosiva | Equilibrada |
| **Tiempo de respuesta** | Variable, depende de índices y agregados | Muy rápido sobre agregados precalculados | Rápido en agregados, aceptable en detalle |
| **Latencia de datos** | Cercana a la carga del DW | Requiere reprocesar el cubo | Intermedia |

**Otros conceptos de optimización:**
- **Índices y particionado:** bitmap para baja cardinalidad; particiones por fecha para "podar" el escaneo.
- **Vistas materializadas:** agregados persistidos y reescritura automática de consultas frecuentes.
- **Almacenamiento columnar:** compresión por columna y lectura selectiva — el estándar analítico actual.

## 1.19 Ecosistema de repositorios analíticos (slide 22)

| Repositorio | Descripción |
|---|---|
| **Data mart** | Subconjunto departamental del DW, con modelo dimensional acotado a un proceso de negocio. |
| **ODS** (Operational Data Store) | Almacén operacional de baja latencia, con datos casi en tiempo real e historia mínima. |
| **Data lake** | Repositorio de dato crudo en su formato nativo, con esquema aplicado en la lectura (schema-on-read). |
| **Lakehouse** | Formatos de tabla abiertos que aportan transacciones y esquema sobre el lago. |

### Criterios de decisión arquitectónica
- **Naturaleza del dato:** si el esquema es estable y el uso recurrente, el modelo dimensional sigue siendo superior.
- **Latencia exigida:** cargas por lotes nocturnas vs. micro-lotes o streaming continuo con ventanas de minutos.
- **Perfil de consumo:** consulta gobernada y repetible vs. exploración abierta de científicos de datos.
- **Costo total:** el lago abarata el almacenamiento, pero traslada el costo a la gobernanza y al cómputo de consulta.

## 1.20 6. Dashboards y 7. KPIs (slide 24)

### Dashboards
- KPIs e indicadores en un solo lugar.
- Alertas y semáforos de gestión.
- Gráficos comparativos y de tendencia.
- Mapas y análisis geográfico.

### KPIs (ejemplos)
Ventas · Margen · Rentabilidad · Tiempo promedio · NPS · Rotación · Inventario.

**Idea clave:** "Un dashboard no es el proyecto: es su **resultado visible**."

## 1.21 Capa de explotación: del indicador al tablero (slide 25)

| Elemento | Descripción |
|---|---|
| **Indicadores (KPI)** | Métrica ligada a un objetivo, con fórmula, dueño, meta y frecuencia definidos. **Sin meta no hay indicador, sólo una cifra.** |
| **Capa semántica** | Traduce tablas físicas a conceptos de negocio y centraliza la definición de las métricas para toda la organización. |
| **Tableros y reportes** | Tablero para monitoreo continuo; informe para análisis puntual. Cada objeto responde a una pregunta explícita. |

### Buenas prácticas de visualización
- Elegir el gráfico según la tarea: comparación, composición, distribución o evolución.
- Maximizar la razón dato-tinta: sin rejillas, sombras ni efectos superfluos.
- Jerarquía visual explícita: lo primero que se ve es lo que importa decidir.
- Contexto obligatorio: toda cifra con su meta y su variación.

## 1.22 Arquitectura completa — caso integrado (slide 26)

```
Fuentes (ERP, CRM, Excel, IoT, RRSS, API)
    → ETL
    → Data Warehouse
    → Data Mart
    → Modelo Estrella
    → Power BI
    → Dashboard
    → Gerencia
```

**Conclusión:** El valor no está en ninguna capa aislada, sino en que **todas conversen entre sí**.

## 1.23 Tipos de datos que alimentan BI (slide 27)

| Categoría | Ejemplos |
|---|---|
| **Estructurados** | SQL Server, Oracle, PostgreSQL, MySQL |
| **Semiestructurados** | JSON, XML, CSV, Logs |
| **No estructurados** | Videos, Audios, Correos, PDF, Imágenes, Redes sociales |

**Dato clave:** Hoy la mayor parte del dato disponible en una empresa **no está estructurado**.

## 1.24 El ciclo de vida del dato — Jerarquía DIKW (slide 28)

```
1. Dato → 2. Información → 3. Conocimiento → 4. Decisión → 5. Acción → 6. Valor
```

Es la jerarquía **DIKW** (Data, Information, Knowledge, Wisdom): cada capa reduce el volumen y aumenta el valor; **la acción cierra el ciclo**.

## 1.25 Actividad práctica: la veterinaria "Patitas" (slides 29-31)

### Contexto (slide 29)
Actividad en parejas: del dato crudo a la decisión.

**Encargo:** La dueña de la veterinaria quiere saber cuánto factura cada veterinario por especie, mes a mes, y hoy nadie puede responderlo. Se entrega una planilla plana con columnas: N.° visita, Fecha, RUT propietario, Propietario, Teléfono, Dirección, Mascota, Especie, Raza, Veterinario, Motivo de consulta, Diagnóstico, Tratamiento.

**Datos de ejemplo de la planilla (10 filas):** incluyen mascotas de distintos propietarios (Ana Pérez, Carlos Díaz, Beatriz Silva), especies (Perro, Gato), veterinarios (Dr. Soto, Dra. Rojas), con motivos de consulta como vacunación, dolor en pata, falta de apetito, control dental, tos, picazón, vómitos.

**Tarea previa:** anotar en la planilla al menos tres problemas de calidad de datos detectados (ej.: direcciones escritas de forma distinta como "Av. Central 450" vs. "Avenida Central 450"; teléfono con typo 987654321 vs 987654323/987654432; nombres de especie/raza con codificación como "01-Labrador").

### Paso 1: armar el modelo relacional (slide 30)
**10 minutos — Normalizar: una entidad, una tabla.**

1. **Identificar entidades:** ¿Qué cosas distintas aparecen mezcladas en la planilla? Nombrarlas.
2. **Definir claves primarias:** asignar a cada tabla un identificador único y estable.
3. **Conectar las tablas:** ¿qué tabla apunta a cuál? Dibujar las relaciones.
4. **Eliminar repeticiones:** cada dato una sola vez; corregir nombres escritos de distintas formas.

**Entregable:** Un diagrama con las tablas, sus campos, la clave primaria de cada una y las relaciones entre ellas.

**Pista:** deberían aparecer alrededor de **cinco tablas**, y **las atenciones son el centro de todo**. Si un dato se repite en muchas filas, probablemente merece una tabla propia (ej.: Propietarios, Mascotas, Veterinarios, Diagnósticos/Tratamientos, Atenciones).

### Paso 2: del relacional al modelo estrella (slide 31)
**10 minutos — Diseño dimensional para análisis.**

1. **Elegir el hecho:** ¿qué evento del negocio se quiere medir y con qué frecuencia ocurre? (En este caso: la atención/consulta veterinaria).
2. **Definir las métricas:** ¿qué se suma, cuenta o promedia en ese evento? (ej.: monto facturado, cantidad de atenciones).
3. **Definir las dimensiones:** ¿por qué criterios se querrá filtrar y agrupar los resultados? (veterinario, especie, mes, propietario, tipo de tratamiento).
4. **Formular tres preguntas de negocio** que el modelo deba poder responder.

**Puesta en común:** 5 minutos, cada pareja presenta su modelo estrella y las preguntas que resuelve.

**Criterio de logro:** responder las tres preguntas **sin volver a abrir la planilla original**.

## 1.26 Ejemplo empresarial: una cadena de retail (slide 32)

De la caja registradora a la gerencia:

| Sistema origen | → | Dominio de datos |
|---|---|---|
| POS | → | Ventas |
| ERP | → | Inventario |
| CRM | → | Clientes |
| E-commerce | → | Google Analytics |
| Facebook Ads | → | Excel |

Todo converge en: **Power BI → Gerencia**

## 1.27 Caso de estudio: cadena de supermercados (slide 33)

**Contexto:** Las ventas disminuyen — ¿qué necesita saber la gerencia?

**¿Qué información necesita?**
- Ventas por sucursal
- Ventas por producto
- Ventas por hora
- Productos más vendidos
- Clientes frecuentes
- Rentabilidad
- Stock
- Promociones

**¿En qué sistemas existen esos datos?**
ERP · CRM · POS · Inventario · RRHH · Excel · Web

## 1.28 Actividad en equipos (slide 34)

**30 minutos — Trabajo colaborativo.**

Cada equipo elige una empresa: Banco · Clínica · Universidad · Retail · Aerolínea · Minera.

**Y responde:**
- ¿Qué decisiones toma diariamente?
- ¿Qué datos necesita y dónde se generan?
- ¿Qué indicadores mediría?
- ¿Cómo sería su arquitectura BI y qué áreas consumirían la información?

## 1.29 Conclusiones (slide 35)

> Business Intelligence no consiste únicamente en crear dashboards.
>
> Es una disciplina que integra tecnologías, procesos, personas y metodologías para transformar datos dispersos en información confiable que apoye decisiones estratégicas. Una solución BI requiere una arquitectura completa que abarca desde las fuentes de datos y los procesos ETL/ELT hasta los modelos analíticos y la visualización, con el objetivo final de generar valor para el negocio.

**Fórmula síntesis:** Tecnologías + procesos + personas = información confiable para decidir.

## 1.30 Ideas para llevarse de la sesión (síntesis final)

| # | Idea | Explicación |
|---|---|---|
| 01 | **BI es una arquitectura, no una herramienta** | El tablero es la punta visible de una cadena de integración, modelado y gobierno. |
| 02 | **La granularidad define el modelo** | Declarar el grano de la tabla de hechos condiciona todas las decisiones posteriores. |
| 03 | **La calidad se diseña, no se corrige** | Los controles pertenecen al flujo de integración, no al informe final. |
| 04 | **La latencia se ajusta a la decisión** | No existe una arquitectura óptima universal: depende de la ventana de acción. |

## 1.31 Próximas unidades del curso

Como primera sesión para estudiantes de último año, esta clase establece una base conceptual sólida y prepara el terreno para:
- Modelamiento dimensional
- Procesos ETL
- Data Warehouse
- Power BI
- Minería de datos
- Analítica avanzada

---

# PARTE 2 — CLASE 2: "Inteligencia de Negocios"

## 2.1 Portada
- **2026 · Semestre 2**
- Título: **Inteligencia de Negocios**
- Subtítulo: De los datos a la decisión: DSS, BI, machine learning y arquitecturas analíticas modernas.

## 2.2 Temario completo (slide 2)

1. Componentes de un DSS
2. Ciclo de vida de los datos
3. Análisis inteligente de datos
4. Business Intelligence (BI)
5. Machine learning y minería de datos
6. Proceso KDD
7. Arquitectura de un data warehouse
8. Del data lake al lakehouse
9. Modelamiento multidimensional
10. Soluciones y tipos de OLAP
11. Problemáticas de la extracción de conocimiento
12. Cierre y síntesis

---

## MÓDULO 1 — Fundamentos: DSS y ciclo de vida de los datos

### 2.3 Componentes principales de un DSS (slide 4)

**DSS = Decision Support System (Sistema de Apoyo a la Decisión).**

| Componente | Descripción | Ejemplo |
|---|---|---|
| **Base de datos** | Datos internos y externos, históricos y actuales. | Ventas, datos de mercado. |
| **Modelo de decisión** | Modelos y algoritmos que interpretan datos y recomiendan acciones. | Pronóstico, simulación. |
| **Motor de análisis** | Ejecuta los cálculos que convierten datos en información útil. | Optimización. |
| **Interfaz de usuario** | Permite consultar, explorar y visualizar. | Dashboards, análisis ad-hoc. |
| **Comunicación** | Comparte hallazgos y habilita la decisión colaborativa. | Reportes automatizados. |

### 2.4 Ciclo de vida de los datos (slide 5)

Representado como un ciclo circular: **Collect → Store → Process → Analyze → Share → Archive** (y vuelve a empezar).

- **Captura:** recolección desde las fuentes; definir formatos y frecuencia.
- **Almacenamiento:** en el data warehouse o sistemas relacionados.
- **Procesamiento y transformación:** limpieza y preparación para el análisis.
- **Análisis y consulta:** generación de información útil a partir del dato transformado.
- **Reportes y visualización:** informes y paneles según los requisitos del usuario.
- **Mantenimiento, archivado y eliminación:** datos vigentes, históricos y cumplimiento normativo.

---

## MÓDULO 2 — Análisis inteligente de datos

### 2.5 ¿Qué es el análisis inteligente de datos? (slide 7)

- Combina **inteligencia artificial, aprendizaje automático y estadística** para interpretar datos complejos.
- Descubre patrones, predice y recomienda acciones.
- A diferencia del análisis tradicional (**descriptivo y reactivo**), entrega recomendaciones **proactivas y automatizadas**.
- Hoy se apoya en modelos de lenguaje e IA generativa.

### 2.6 Objetivos del análisis inteligente de datos (slide 8)

| Objetivo | Descripción |
|---|---|
| **Descubrimiento de patrones** | Identificar patrones y relaciones ocultas que no son evidentes a simple vista. |
| **Predicción** | Usar datos históricos para anticipar eventos futuros o comportamientos. |
| **Automatización de decisiones** | Decidir de forma automática o semi-automática mediante algoritmos. |
| **Optimización** | Mejorar procesos y sistemas con recomendaciones basadas en datos. |

### 2.7 Técnicas del análisis inteligente de datos (slide 9)

| Técnica | Descripción |
|---|---|
| **Aprendizaje supervisado** | Entrenado con datos etiquetados para predecir sobre datos nuevos: regresión, clasificación, redes neuronales. |
| **Aprendizaje no supervisado** | Descubre patrones y estructuras en datos sin etiquetar: clustering, reducción de dimensionalidad. |
| **Aprendizaje reforzado** | Aprende decidiendo y recibiendo recompensas o penalizaciones: control y optimización. |
| **Análisis predictivo** | Anticipa resultados futuros: series temporales, regresión, clasificación predictiva. |
| **Análisis prescriptivo** | Recomienda las mejores acciones: optimización de recursos, simulación de estrategias. |
| **NLP y redes complejas** | Interpreta texto no estructurado (sentimiento, asistentes) y analiza interacciones en redes. |

### 2.8 Aplicaciones del análisis inteligente de datos (slide 10)

| Área | Aplicaciones |
|---|---|
| **Negocios** | Marketing: segmentación y personalización. Riesgos: fraude. Operaciones: inventarios y demanda. |
| **Salud** | Diagnóstico predictivo con datos clínicos y genéticos; detección de anomalías en imágenes médicas. |
| **Finanzas** | Previsión de tendencias de mercado e identificación de transacciones sospechosas. |
| **Recursos Humanos** | Análisis de currículos, predicción de desempeño y gestión de talento y retención. |

### 2.9 Desafíos y consideraciones (slide 11)

| Desafío | Solución |
|---|---|
| **Calidad de los datos** | Datos incompletos o sesgados llevan a conclusiones erróneas → limpieza y validación robustas. |
| **Interpretación de resultados** | Los modelos complejos son difíciles de explicar → visualización e IA explicable (XAI). |
| **Privacidad y seguridad** | Se maneja información sensible → anonimización, control de acceso y cumplimiento. |
| **Escalabilidad** | Los volúmenes crecen de forma continua → arquitecturas distribuidas y nube. |

---

## MÓDULO 3 — Inteligencia de Negocios (BI)

### 2.10 ¿Qué es Business Intelligence? (slide 13)

- Combina **análisis de negocios, minería, visualización, herramientas e infraestructura de datos.**
- Es el conjunto de tecnologías, procesos y prácticas que permiten analizar datos para decidir.
- Implica una vista integral de todos los datos de la organización.
- Busca impulsar el cambio, eliminar ineficiencias y adaptarse rápido al mercado.

### 2.11 Evolución del BI (slide 14)

| Etapa | Periodo | Descripción |
|---|---|---|
| **01 BI tradicional** | 1960–1980 | Sistema para compartir información entre organizaciones; se consolida con los modelos informáticos, operado por equipos de TI. |
| **02 BI moderno** | — | Análisis de autoservicio, datos gobernados en plataformas confiables, autonomía del usuario de negocio y rapidez para obtener información. |
| **03 BI con IA generativa** | — | Asistentes que permiten consultar los datos en lenguaje natural y generar explicaciones automáticas. |

### 2.12 OLAP y DSS dentro del BI (slide 15)

| Concepto | Descripción |
|---|---|
| **OLAP** | Sistemas que permiten consultar y analizar datos desde múltiples perspectivas en tiempo real, sobre grandes volúmenes. |
| **DSS** | Sistemas que apoyan la toma de decisiones empresariales analizando datos y presentando información relevante. |
| **Rol en BI** | Ambos son componentes esenciales: BI los combina con prácticas y tecnologías para transformar datos en valor. |

### 2.13 Conceptos clave de BI (slide 16)

| Concepto | Descripción | Ejemplo |
|---|---|---|
| **Data warehousing** | Repositorio centralizado que integra datos de múltiples fuentes. | Ventas, finanzas y operaciones. |
| **ETL / ELT** | Procesos que mueven y transforman los datos hacia el repositorio analítico. | — |
| **Reporting** | Informes y visualizaciones que hacen comprensible la información. | Ventas mensuales. |
| **Dashboards** | Vista consolidada de KPIs y métricas para monitoreo en tiempo real. | — |
| **Análisis predictivo y prescriptivo** | Anticipa eventos y recomienda acciones. | Demanda, cadena de suministro. |
| **Análisis aumentado con IA** | Preguntar a los datos en lenguaje natural, resúmenes automáticos, análisis de sentimiento. | — |

### 2.14 Elementos clave de BI (slide 17)

| Elemento | Descripción |
|---|---|
| **Fuentes de datos** | Orígenes diversos: bases de datos, archivos, aplicaciones y servicios. |
| **Integración de datos** | Combinar datos de distintas fuentes para crear un conjunto coherente. |
| **Calidad de datos** | Asegurar que los datos sean precisos, completos y consistentes. |
| **Acceso del usuario** | Facilitar que los usuarios autorizados accedan a los datos y análisis que necesitan. |

### 2.15 Cómo el BI agrega valor (slide 18)

| Beneficio | Descripción |
|---|---|
| **Mejores decisiones** | Visibilidad completa de datos y KPIs; informes y paneles que facilitan interpretar información compleja. |
| **Tendencias y oportunidades** | Identifica tendencias de mercado y ventas, y descubre nuevas oportunidades de negocio. |
| **Operaciones optimizadas** | Detecta ineficiencias en los procesos y mejora la asignación de recursos. |
| **Menor riesgo** | Anticipa y mitiga riesgos con análisis predictivo y monitorea el cumplimiento normativo. |
| **Experiencia del cliente** | Segmenta y personaliza ofertas según comportamiento y preferencias. |
| **Mejor servicio** | Entrega información relevante sobre interacciones y necesidades de los clientes. |

---

## MÓDULO 4 — Machine learning y minería de datos

### 2.16 Machine learning y minería de datos (slide 22)

| Concepto | Descripción |
|---|---|
| **Aprendizaje automático (ML)** | Rama de la IA que permite aprender de los datos y predecir o decidir sin ser programado explícitamente. Se entrena con datos y generaliza patrones. |
| **Minería de datos** | Proceso de descubrir patrones y conocimientos útiles en grandes conjuntos mediante estadística, algoritmos de ML y visualización. |

### 2.17 Tipos de aprendizaje automático (slide 23)

| Tipo | Descripción | Algoritmos |
|---|---|---|
| **Supervisado** | Usa datos etiquetados y aprende a mapear entradas a salidas. | Regresión lineal, árboles de decisión, SVM, redes neuronales. |
| **No supervisado** | Busca estructuras o patrones en datos sin etiquetar. | K-means, clustering jerárquico, PCA. |
| **Por refuerzo** | Decide interactuando con un entorno y recibiendo recompensas. | Q-learning, Deep Q-Networks. |
| **Semi y auto-supervisado** | Combinan pocos datos etiquetados con grandes volúmenes sin etiquetar: base de los modelos fundacionales actuales. | — |

### 2.18 Técnicas de minería de datos (slide 24)

| Técnica | Descripción | Ejemplos de algoritmos |
|---|---|---|
| **Clasificación** | Asigna una etiqueta a un dato nuevo. | Árboles de decisión, Naive Bayes, redes neuronales. |
| **Regresión** | Predice un valor numérico continuo. | Regresión lineal y polinómica. |
| **Clustering** | Agrupa datos por similitud, sin etiquetas previas. | K-means, clustering jerárquico. |
| **Asociación** | Descubre relaciones entre variables. | Reglas de asociación (Apriori). |
| **Detección de anomalías** | Identifica datos fuera del patrón (errores, fraude). | Modelos estadísticos, isolation forest. |
| **Reducción de dimensionalidad** | Simplifica el conjunto conservando la información relevante. | Análisis de componentes principales (PCA). |

### 2.19 Relación con la estadística (slide 25)

- La estadística provee la **base teórica** de muchas técnicas de ML y minería de datos.
- **Inferencia estadística:** sustenta predicciones y clasificaciones, como la estimación de parámetros en regresión lineal.
- **Modelos estadísticos:** la regresión logística y los árboles de decisión se basan en principios estadísticos.
- **Pruebas de hipótesis y ANOVA:** validan modelos y evalúan su desempeño.

### 2.20 Tipos de analítica (slide 26)

| Tipo | Pregunta que responde | Técnicas |
|---|---|---|
| **Descriptiva** | Qué pasó | Estadística descriptiva y visualización; explora y prepara los datos para el modelado. |
| **Diagnóstica** | Por qué pasó | Correlación y minería de datos; identifica patrones y relaciones históricas. |
| **Predictiva** | Qué pasará | Regresión, clasificación y machine learning; base de los modelos de predicción. |
| **Prescriptiva** | Qué hacer | Optimización y simulación para recomendar acciones que mejoren resultados. |
| **Cognitiva** | (Simula razonamiento) | Redes neuronales profundas y procesamiento del lenguaje natural. |

### 2.21 Minería de datos y proceso KDD (slide 27)

- **Minería de datos:** técnica para descubrir patrones, correlaciones y tendencias útiles en grandes conjuntos de datos.
- **KDD (Knowledge Discovery in Databases):** proceso integral que va desde la selección y el preprocesamiento hasta la presentación y el uso del conocimiento.
- **La minería de datos es una etapa dentro del proceso KDD.**

---

## MÓDULO 6 — Arquitectura de un data warehouse

### 2.22 Del data warehouse al lakehouse (slide 32)

- Crear un repositorio analítico implica **cuatro etapas**: análisis, diseño, implementación y mantenimiento.
- Hoy el data warehouse convive con data lakes y arquitecturas lakehouse.
- La plataforma se elige según **volumen, latencia y costo:** cloud, on-premises o híbrida.

### 2.23 Construir el repositorio analítico (slide 33)

| Etapa | Actividades |
|---|---|
| **01 Análisis** | Entrevistar stakeholders, definir objetivos y KPIs, e inventariar fuentes evaluando su calidad y formato. |
| **02 Diseño** | Modelado conceptual, lógico y físico; arquitectura estrella o copo de nieve sobre plataformas cloud o lakehouse; flujos ETL/ELT e interfaz de reporting. |
| **03 Implementación** | Configurar el entorno (BigQuery, Snowflake, Databricks, Redshift, Fabric), desarrollar y validar los flujos, construir y probar informes con los usuarios. |
| **04 Mantenimiento y optimización** | Monitorear rendimiento y calidad, escalar con el volumen y la demanda, capacitar usuarios y sostener el soporte. |

### 2.24 Modelamiento multidimensional (slide 34)

- Técnica de diseño de data warehouses que organiza los datos para facilitar el análisis y la consulta eficiente.
- Organiza los datos en **cubos**, permitiendo verlos desde múltiples perspectivas de negocio.
- Es esencial en BI: habilita consultas complejas sobre grandes volúmenes de datos.
- Se adapta a las necesidades del negocio y soporta la toma de decisiones.

### 2.25 Elementos del modelo multidimensional (slide 35)

| Elemento | Descripción | Ejemplo |
|---|---|---|
| **Cubos de datos** | Estructuras que organizan datos en múltiples dimensiones y medidas, permitiendo consultas rápidas. | — |
| **Dimensiones** | Perspectivas de análisis con atributos propios. | Tiempo, ubicación, producto, cliente. |
| **Medidas** | Datos cuantitativos analizados. | Ventas, ingresos, costos, unidades vendidas. |
| **Jerarquías** | Niveles de detalle dentro de una dimensión. | Año > trimestre > mes > día. |
| **Tablas de hechos** | Contienen las medidas y las claves foráneas hacia las dimensiones. | Ventas diarias, órdenes. |
| **Dimensiones conformadas** | Dimensiones usadas de forma consistente entre cubos, para un análisis coherente entre áreas. | — |

### 2.26 Esquemas de modelado (slide 36)

| Esquema | Descripción |
|---|---|
| **Estrella** | Tabla de hechos central rodeada de dimensiones. Simple y eficiente para consultas. |
| **Copo de nieve** | Dimensiones normalizadas en varios niveles. Menos redundancia, más complejidad. |
| **Galaxia** | Varios esquemas estrella que comparten dimensiones conformadas. |

### 2.27 Pasos del modelado multidimensional (slide 37)

| Paso | Descripción |
|---|---|
| **01 Definir requisitos** | Qué información importa, cómo se analizará y qué KPIs y métricas se deben calcular. |
| **02 Diseñar el esquema** | Elegir entre estrella, copo de nieve o galaxia según necesidad de rendimiento y normalización. |
| **03 Dimensiones y medidas** | Definir dimensiones, atributos y jerarquías; establecer las métricas clave y la tabla de hechos. |
| **04 Implementar y validar** | Desplegar el cubo o modelo semántico, configurar la carga ETL/ELT y verificar resultados. |
| **05 Documentar y capacitar** | Registrar decisiones de diseño y enseñar a usar el modelo y las herramientas de BI. |

---

## MÓDULO 11 — Problemáticas de la extracción automática de conocimiento (slide 39)

| Problema | Descripción | Solución |
|---|---|---|
| **Calidad de los datos** | Datos incompletos o erróneos degradan el conocimiento. | Limpieza, validación y observabilidad. |
| **Volumen y complejidad** | Alta dimensionalidad dificulta el análisis. | Reducción de dimensionalidad y procesamiento distribuido. |
| **Overfitting y underfitting** | El modelo se sobreajusta o no captura los patrones. | Validación cruzada y ajuste de hiperparámetros. |
| **Interpretabilidad** | Los modelos complejos son difíciles de explicar. | IA explicable y modelos interpretables. |
| **Privacidad y sesgo** | Riesgos legales y sesgos amplificados por el modelo. | Anonimización y auditoría de datos y modelos. |
| **Escalabilidad** | Procesar grandes volúmenes con eficiencia. | Arquitecturas escalables y procesamiento distribuido. |

## 2.28 Síntesis del curso (última slide)

> De los datos a la decisión: capturar y gobernar el dato, modelarlo para el análisis, aplicar técnicas inteligentes y comunicar el conocimiento para decidir mejor.

---

# PARTE 3 — LAB CLASE 2: "BI en acción: áreas, componentes y ciclo de vida"

## 3.1 Portada
- **Inteligencia de Negocios · Clase 2**
- Título: **BI en acción: áreas, componentes y ciclo de vida**
- Carrera de Ciencia de Datos · Sesión de 3 horas con ejercicios prácticos
- Docente: Alexandra D. Matus Gacitúa

## 3.2 Objetivos de aprendizaje

Al finalizar la sesión serás capaz de:

| # | Objetivo | Descripción |
|---|---|---|
| 01 | **Explicar el rol de BI** | Describir cómo se aplica la inteligencia de negocios en marketing, finanzas, recursos humanos y operaciones. |
| 02 | **Identificar componentes** | Distinguir los datos, los procesos y las herramientas que forman un sistema de BI y cómo se relacionan. |
| 03 | **Aplicar el ciclo de vida** | Situar un requerimiento real dentro de las fases del ciclo de vida de un proyecto de BI. |
| 04 | **Diseñar una solución** | Proponer indicadores, fuentes y visualizaciones para un caso de negocio concreto. |

## 3.3 Repaso rápido: ¿qué es BI? (conexión con la Clase 1)

### Definición operativa
- Conjunto de datos, procesos y tecnologías.
- Convierte datos crudos en decisiones.
- Foco en el pasado y el presente del negocio.

### Qué NO es BI
- No es solo un dashboard bonito.
- No reemplaza el criterio del negocio.
- No predice por sí solo: **eso es analítica avanzada**.

### Escalera del valor
- Dato → información → conocimiento
- Descriptivo → diagnóstico
- Predictivo → prescriptivo

### Pregunta de activación (5 min, actividad)
Piensa en la última compra en línea que hiciste. ¿Qué decisiones tomó la empresa gracias a tus datos, antes, durante y después de esa compra? Anota tres y compártelas con tu compañero de al lado.

---

## BLOQUE 1 — BI en las áreas funcionales

**Temas:** Marketing · Finanzas · Recursos Humanos · Operaciones

### 3.4 Una misma plataforma, cuatro conversaciones

| Área | Pregunta central |
|---|---|
| **Marketing** | ¿A quién le hablo y con qué retorno? |
| **Finanzas** | ¿Cómo se comporta el dinero del negocio? |
| **Recursos Humanos** | ¿Quién sostiene la operación y cómo está? |
| **Operaciones** | ¿Cómo entrego mejor, más rápido y más barato? |

**Idea clave:** La diferencia no está en la tecnología, sino en las **preguntas de negocio** y en los indicadores que cada área necesita responder.

> Todo el bloque usa un **caso transversal de agencia/operador de viajes** para ejemplificar cada área.

### 3.5 BI en Marketing (Área funcional 1 de 4)

**Preguntas típicas:**
- ¿Qué campañas venden más pasajes y paquetes por peso invertido?
- ¿Qué perfiles de viajero tienen mayor valor de vida (CLV)?
- ¿En qué paso del buscador se cae la reserva?

**Indicadores clave:**
- CAC, ROAS y conversión de búsqueda a reserva.
- Ticket promedio por pasajero y anticipación de compra.
- Recompra anual y churn del programa de viajero frecuente.

**Ejemplo — Agencia de viajes:**
Una agencia cruza las búsquedas del sitio con el historial de reservas y las campañas de correo. Descubre que quienes buscan destinos de playa entre marzo y mayo compran, en promedio, 90 días antes y aceptan mejor los paquetes con traslado incluido. Reordena el calendario de campañas y deja de premiar el clic para premiar el margen por pasajero.

### 3.6 BI en Finanzas (Área funcional 2 de 4)

**Preguntas típicas:**
- ¿Qué destinos o sucursales destruyen margen?
- ¿Cómo se desvía la ejecución respecto del presupuesto?
- ¿Cómo afecta el tipo de cambio al margen de cada paquete?

**Indicadores clave:**
- Margen por reserva, por destino y por canal de venta.
- Ingreso por pasajero y comisión efectiva del proveedor.
- Anticipos, cancelaciones y desviación presupuestaria.

**Ejemplo — Cierre mensual de un operador turístico:**
El equipo de control de gestión dedicaba cinco días a consolidar planillas de cada sucursal y de cada operador mayorista. Al centralizar las reservas y el libro mayor en un modelo único, el margen por destino queda disponible el día 2 y la discusión pasa de "¿este número está bien?" a "¿por qué el Caribe cayó tres puntos?". El valor no fue el gráfico: fue recuperar tres días de análisis.

### 3.7 BI en Recursos Humanos (Área funcional 3 de 4)

**Preguntas típicas:**
- ¿Qué sucursales y call centers concentran la rotación?
- ¿Cuánto demora y cuánto cuesta cubrir un ejecutivo de ventas?
- ¿La dotación acompaña la estacionalidad de la demanda?

**Indicadores clave:**
- Rotación voluntaria por sucursal y por temporada.
- Tiempo y costo de contratación de ejecutivos.
- Ausentismo, clima y horas de capacitación en destinos.

**Ejemplo — Rotación en ejecutivos de venta:**
Al cruzar turnos, antigüedad, metas comerciales y evaluaciones, una agencia detecta que la rotación se dispara entre el mes 3 y el mes 5 en las sucursales con mayor carga de temporada alta. La intervención no fue subir sueldos, sino rediseñar el acompañamiento del primer trimestre y la dotación estacional. **Atención:** estos datos son sensibles y exigen anonimización y control de acceso.

### 3.8 BI en Operaciones (Área funcional 4 de 4)

**Preguntas típicas:**
- ¿Dónde están los cuellos de botella en la emisión de reservas?
- ¿Qué cupos de hotel o vuelo quedan sin vender?
- ¿Cumplimos los itinerarios y traslados comprometidos?

**Indicadores clave:**
- Ocupación de cupos y asientos vendidos frente a bloqueados.
- Puntualidad de traslados y cumplimiento de itinerario.
- Tiempo de emisión, reclamos y tasa de incidencias por viaje.

**Ejemplo — Traslados y llegadas:**
Un receptivo combina GPS de sus vans, itinerarios de vuelos y reclamos de pasajeros. El tablero muestra que el 70% de los atrasos en traslados ocurre con vuelos que aterrizan entre 17 y 20 horas en temporada alta. Reprograman conductores y ventanas de recogida, y la puntualidad sube sin sumar un solo vehículo. **La frecuencia de actualización es crítica: un dato diario llega tarde.**

### 3.9 El mismo dato, cuatro lecturas (síntesis del Bloque 1)

| Área | Pregunta de negocio | Indicador | Fuente de datos habitual |
|---|---|---|---|
| **Marketing** | ¿Qué canal trae viajeros rentables? | ROAS · CLV | CRM, motor de reservas, campañas y sitio web |
| **Finanzas** | ¿Qué destino pierde margen? | Margen por reserva · Presupuesto | ERP, libro mayor, contratos con proveedores |
| **RR.HH.** | ¿Por qué se van los ejecutivos? | Rotación · Ausentismo | Sistema de personas, turnos y metas comerciales |
| **Operaciones** | ¿Por qué fallan los traslados? | Puntualidad · Ocupación de cupos | Itinerarios, GPS, reclamos y cupos contratados |

**Regla práctica:** si no puedes escribir la pregunta de negocio en una frase, todavía no estás listo para construir el tablero.

### 3.10 Ejercicio 1 · Del área a la pregunta

**Trabajo en grupos de 3 · 25 minutos**

**Instrucciones:**
1. Elijan una empresa que conozcan (retail, banco, delivery, universidad).
2. Formulen dos preguntas de negocio por cada área funcional: 8 en total.
3. Para cada pregunta definan el indicador que la responde y la fuente de datos.
4. Marquen con una estrella la pregunta que hoy la empresa NO puede responder.
5. Preparen 2 minutos de presentación.

**Entregable:**
- Una tabla de 8 filas: pregunta, indicador, fuente.
- Formato libre: planilla o papelógrafo.

**Se evalúa:**
- Claridad de la pregunta.
- Coherencia pregunta–indicador.
- Realismo de la fuente de datos.

**Sugerencia:** roten los roles dentro del grupo — quien escribe, quien cuestiona y quien presenta.

---

## BLOQUE 2 — Componentes de un sistema de BI

**Temas:** Datos · Procesos · Herramientas

### 3.11 Los tres componentes (ninguno funciona sin los otros dos)

| Componente | Rol | Incluye |
|---|---|---|
| **DATOS** | La materia prima | Fuentes internas y externas · Estructurados y no estructurados · Calidad, definición y linaje |
| **PROCESOS** | La transformación | Extracción, carga y transformación · Modelado dimensional · Gobierno, seguridad y calidad |
| **HERRAMIENTAS** | La entrega | Almacenamiento y motor analítico · Visualización y autoservicio · Orquestación y monitoreo |

**Idea clave:** Un sistema de BI falla por su eslabón más débil: **datos sucios con la mejor herramienta siguen siendo datos sucios.**

### 3.12 Componente 1 · Datos (la materia prima del sistema)

**Origen:**
- Internos: ERP, CRM, POS, RR.HH.
- Externos: INE, precios, clima, redes.
- Generados: encuestas, sensores.

**Naturaleza:**
- Estructurados: tablas y transacciones.
- Semiestructurados: JSON, logs, XML.
- No estructurados: texto, imagen, audio.

**Temporalidad:**
- Histórico para tendencias.
- Casi en tiempo real para operación.
- Instantáneas o snapshots.

**Las 6 dimensiones de calidad que debes exigir:**
Exactitud · Completitud · Consistencia · Oportunidad · Unicidad · Validez.

### 3.13 Componente 2 · Procesos (cómo el dato se vuelve confiable)

**Las 5 etapas:**
1. **Extraer** — Conectar y leer las fuentes.
2. **Transformar** — Limpiar, unificar, calcular.
3. **Cargar** — Depositar en el modelo.
4. **Modelar** — Hechos y dimensiones.
5. **Publicar** — Entregar y monitorear.

**ETL frente a ELT:**
- **ETL:** se transforma antes de cargar. Control estricto, típico en bodegas tradicionales.
- **ELT:** se carga primero y se transforma en el destino. Aprovecha la potencia de la nube.
- La elección depende del **volumen, la latencia y el costo**, no de la moda.

**Gobierno de datos:**
- Diccionario y definiciones únicas de cada métrica.
- Roles y permisos: quién ve qué.
- Trazabilidad o linaje del dato de punta a punta.
- Ciclo de vida, retención y anonimización.

### 3.14 Componente 3 · Herramientas (el stack tecnológico por capas)

| Capa | Contenido |
|---|---|
| **Fuentes** | ERP · CRM · POS · APIs · archivos planos · sensores |
| **Integración** | Herramientas de ETL/ELT y orquestación de flujos |
| **Almacenamiento** | Bodega de datos, lago de datos o arquitectura mixta |
| **Análisis y modelo** | Motor semántico, cubos, SQL, capas de métricas |
| **Visualización** | Tableros, reportes, alertas y autoservicio |

**Cómo elegir la herramienta:**
- Volumen y variedad de datos.
- Latencia que exige la decisión.
- Competencias del equipo que la operará.
- Costo total de propiedad, no solo licencias.
- Integración con los sistemas existentes.
- Gobierno, seguridad y trazabilidad del dato.

### 3.15 Dónde se va el esfuerzo real (distribución típica de un proyecto de BI)

| Fase del proyecto | % del esfuerzo |
|---|---|
| Levantamiento de requerimientos | 15% |
| **Integración y limpieza de datos** | **40%** |
| Modelado de datos | 20% |
| Visualización y tableros | 15% |
| Adopción y capacitación | 10% |

**Lectura:**
- El dashboard es la punta del iceberg.
- La integración concentra el mayor riesgo del proyecto.

**Implicancia:**
- Planifica el doble de tiempo del que crees para los datos.
- La adopción se diseña, no se espera.

### 3.16 Ejercicio 2 · Mapa de componentes

**Trabajo en grupos de 3 · 20 minutos**

**Caso:** agencia de viajes con 40 sucursales y venta web.
La gerencia quiere un tablero diario de reservas, margen por destino y cumplimiento de meta por sucursal. Hoy cada sucursal envía una planilla por correo los lunes, el motor de reservas web es independiente del sistema de las sucursales y no existe un catálogo único de destinos ni de proveedores.

**Parte A · Datos**
- ¿Qué fuentes necesitan?
- ¿Qué granularidad mínima?
- ¿Qué problemas de calidad anticipan?

**Parte B · Procesos**
- ¿ETL o ELT y por qué?
- ¿Con qué frecuencia se actualiza?
- ¿Quién define "reserva confirmada"?

**Parte C · Herramientas**
- ¿Qué capas del stack necesitan?
- ¿Qué ve el gerente y qué el jefe de sucursal?
- ¿Qué NO comprarían todavía?

**Entregable:** un diagrama en una hoja con las tres capas y las decisiones justificadas en una línea cada una.

---

## BLOQUE 3 — Ciclo de vida de la inteligencia de negocios

**Tema:** De la pregunta de negocio al valor sostenido en el tiempo.

### 3.17 Las seis fases del ciclo de vida (es un ciclo, no una línea recta)

| # | Fase | Descripción |
|---|---|---|
| 01 | **Planificación** | Definir el problema, el alcance, los actores y el caso de negocio. |
| 02 | **Requerimientos** | Levantar preguntas, indicadores, roles y criterios de éxito. |
| 03 | **Diseño** | Arquitectura, modelo de datos, definición de métricas y prototipos. |
| 04 | **Desarrollo** | Construir integraciones, modelo, tableros y pruebas de calidad. |
| 05 | **Despliegue** | Poner en producción, capacitar y gestionar la adopción. |
| 06 | **Evolución** | Monitorear uso y valor, ajustar, ampliar y depurar. |

**Idea clave:** Cada iteración debería durar **semanas, no años**: entregar valor temprano es la mejor estrategia de adopción.

### 3.18 Qué se entrega en cada fase y su criterio de salida

| Fase | Entregable principal | Criterio de salida |
|---|---|---|
| **Planificación** | Caso de negocio y alcance | El patrocinador firma el objetivo y el presupuesto |
| **Requerimientos** | Catálogo de preguntas e indicadores | Cada indicador tiene dueño, fórmula y fuente |
| **Diseño** | Modelo dimensional y prototipo | El usuario reconoce sus números en el prototipo |
| **Desarrollo** | Flujos, modelo y tableros probados | Las pruebas de calidad y la conciliación cuadran |
| **Despliegue** | Producción, manual y capacitación | Los usuarios entran sin que nadie se lo recuerde |
| **Evolución** | Backlog priorizado y métricas de uso | El tablero cambia decisiones, no solo se mira |

### 3.19 Errores frecuentes y cómo evitarlos (lecciones de proyectos reales)

| Error | Síntoma | Contramedida |
|---|---|---|
| **Empezar por la herramienta** | Comprar la licencia antes de saber qué pregunta se responde. | Parte siempre por la decisión que quieres mejorar. |
| **Métricas sin dueño** | Tres áreas calculan "venta" de forma distinta y nadie cede. | Diccionario único, con dueño y fórmula publicada. |
| **El proyecto de un año** | Se entrega tarde y el negocio ya cambió de prioridad. | Iteraciones cortas con valor visible cada pocas semanas. |
| **Ignorar la adopción** | El tablero existe, pero todos siguen usando su planilla. | Capacitación, rituales de uso y medición del uso real. |

### 3.20 Ejercicio 3 · Del requerimiento al plan (taller integrador)

**25 minutos · Grupos de 3**

**Encargo del gerente:** *"Necesito saber por qué estamos perdiendo clientes y lo necesito para el directorio del próximo mes."* Ese es todo el requerimiento que recibieron.

| Paso | Instrucción |
|---|---|
| **Paso 1** | Traduzcan el encargo en tres preguntas de negocio medibles. |
| **Paso 2** | Definan indicadores, fuentes y granularidad para cada pregunta. |
| **Paso 3** | Ubiquen las tareas en las seis fases del ciclo de vida. |
| **Paso 4** | Declaren dos riesgos y qué harían para mitigarlos. |

**Entregable final:**
- Una lámina con el plan por fases.
- Tres preguntas con su indicador.
- Dos riesgos con mitigación.
- Presentación de 3 minutos.

### 3.21 Cómo se evalúan los ejercicios (rúbrica formativa de la sesión)

| Criterio | Logrado | En desarrollo | Inicial |
|---|---|---|---|
| **Pregunta de negocio** | Específica, medible y accionable | Clara pero general | Confunde pregunta con reporte |
| **Indicador y fuente** | Coherentes y con granularidad definida | Coherentes sin detalle de fuente | Indicador sin fuente asociada |
| **Uso del ciclo de vida** | Ubica tareas y criterios de salida | Reconoce fases sin secuenciar | Omite fases clave |
| **Riesgos y supuestos** | Identifica riesgos con mitigación | Menciona riesgos generales | No los declara |

### 3.22 Síntesis y trabajo para la próxima clase

**Tres ideas para llevarse:**
- BI cambia de preguntas según el área, no de naturaleza.
- Datos, procesos y herramientas son un solo sistema: el eslabón débil manda.
- El ciclo de vida es iterativo y termina en el uso, no en la entrega.

**Tarea para la próxima sesión:**
- Elige una organización real y documenta 5 indicadores con su fuente.
- Identifica en qué fase del ciclo de vida está su capacidad analítica.
- Entrega: una lámina, formato libre, al inicio de la clase 3.

**Clase práctica (próxima sesión):**
Arquitectura de datos para BI: bodegas de datos, lagos de datos y modelado dimensional. Llevarán el caso de la agencia de viajes a un modelo de hechos y dimensiones concreto.

---

# PARTE 4 — CASO PRÁCTICO: "De un MER a un Modelo Dimensional"

> Clase práctica de Inteligencia de Negocios · Caso aplicado: **Empresa de Energía "Energía Sur"**

## 4.1 Portada

- Título: **De un MER a un Modelo Dimensional**
- Caso aplicado: Empresa de Energía **"Energía Sur"**
- Tipo de sesión: Clase práctica de Inteligencia de Negocios

## 4.2 El objetivo: convertir datos en preguntas respondibles

- **Competencia a desarrollar:** transformar un modelo operacional normalizado (MER) en un modelo dimensional orientado al análisis.
- El modelo dimensional organiza los datos en **hechos medibles** y **dimensiones descriptivas**.
- **Ruta de trabajo del ejercicio:**

```
Preguntas de negocio → Proceso → Grano → Hechos → Dimensiones → Métricas → Validación
```

> **Idea clave:** no se comienza dibujando tablas; se comienza entendiendo **qué decisión debe apoyar el modelo**.

## 4.3 MER y modelo dimensional: necesidades distintas

| Modelo entidad–relación (MER) | Modelo dimensional |
|---|---|
| Registra operaciones y mantiene integridad transaccional. | Facilita análisis, filtros, agrupaciones y tendencias. |
| Normaliza entidades para reducir redundancia. | Prioriza una estructura clara para consultar y resumir. |
| Sigue relaciones del proceso operativo. | Centra el análisis en hechos y sus dimensiones. |

**Contexto del caso — Energía Sur:**
El MER distribuye la información entre clientes, medidores, lecturas, consumo, facturas, pagos e interrupciones. El modelo dimensional debe **reorganizarla alrededor de eventos que la gerencia quiera medir**.

## 4.4 Paso 1 — Traducir la necesidad gerencial a preguntas

| Necesidad | Pregunta analítica |
|---|---|
| **Consumo por zona** | ¿Cuántos kWh se consumen por zona, mes y tipo de cliente? |
| **Tipos de clientes** | ¿Cómo cambia el consumo entre clientes residenciales, comerciales e industriales? |
| **Evolución mensual** | ¿Cuál es la tendencia del consumo y su variación mes a mes? |
| **Facturación y pagos** | ¿Cuánto se factura, cuánto se recauda y cuál es la morosidad? |
| **Interrupciones** | ¿Cuántos cortes ocurren y cuánto duran por zona? |

**Decisión de alcance para el ejercicio:** comenzar con el proceso de **consumo energético** y después extender el modelo a facturación, pagos e interrupciones.

## 4.5 Paso 2 — Elegir el proceso principal: consumo energético

El proceso principal seleccionado es **registrar y analizar el consumo de energía por medidor**.

```
Medidor → LecturaMedidor → Consumo
```

El evento analítico es la **lectura** que permite calcular o registrar los kWh consumidos durante un periodo. Cliente, instalación, dirección, zona, tarifa y tiempo aportan el contexto para analizar ese evento.

**¿Por qué no elegir "toda la empresa" como un único hecho?**
Consumo, facturación, pagos e interrupciones son eventos distintos. Mezclarlos produciría duplicaciones y una granularidad ambigua.

## 4.6 Paso 3 — Declarar el grano antes de diseñar

**Grano propuesto:** una fila de `FactConsumo` representa el consumo registrado para un medidor, una instalación y una fecha o periodo de lectura.

> El grano debe ser **atómico y único**. Si se agregan filas mensuales junto con filas diarias en la misma tabla, se mezclan niveles de detalle y las sumas pueden duplicarse.

| Elemento | Decisión para Energía Sur |
|---|---|
| **Evento** | Lectura/registro de consumo |
| **Nivel temporal** | Día de lectura y periodo de consumo |
| **Entidad medida** | Medidor asociado a una instalación |
| **Unidad principal** | kWh consumidos |
| **Clave candidata** | Medidor + fecha_lectura + periodo |

## 4.7 Paso 4 — Diseñar la tabla de hechos `FactConsumo`

| Columna | Tipo | Propósito |
|---|---|---|
| `sk_fecha` | Clave foránea | Conecta con DimTiempo |
| `sk_cliente` | Clave foránea | Permite analizar por cliente y segmento |
| `sk_instalacion` | Clave foránea | Permite analizar el punto de suministro |
| `sk_medidor` | Clave foránea | Identifica el equipo que registró la lectura |
| `sk_zona` | Clave foránea | Permite comparar zonas de distribución |
| `sk_tarifa` | Clave foránea | Permite analizar el plan tarifario |
| `lectura_actual` | Medida base | Lectura acumulada al momento del registro |
| `lectura_anterior` | Medida base | Lectura de referencia |
| `kwh_consumidos` | Medida aditiva | Energía consumida en el grano definido |
| `cantidad_lecturas` | Medida técnica | Valor 1 para contar registros válidos |

**Clave primaria técnica sugerida:** `sk_fecha + sk_medidor + periodo`, o una clave sustituta de hecho más una restricción de unicidad.

## 4.8 Paso 5 — Transformar entidades en dimensiones

| Entidades del MER | Dimensión propuesta | Atributos analíticos |
|---|---|---|
| Cliente + TipoCliente | `DimCliente` | nombre, tipo_cliente, segmento |
| Dirección + ZonaDistribución | `DimUbicacion` | calle, comuna, ciudad, región, zona |
| Instalación | `DimInstalacion` | fecha_instalacion, estado, cliente, ubicación |
| Medidor | `DimMedidor` | numero_medidor, modelo, instalación |
| Tarifa | `DimTarifa` | nombre_tarifa, valor_kwh, tipo_cliente |
| Fecha de lectura / periodo | `DimTiempo` | día, mes, trimestre, semestre, año, semana |

**Regla práctica:** las dimensiones describen y permiten filtrar o agrupar; **no deben contener las métricas principales del evento**.

**Observación de integración:** el MER no muestra `id_zona` en Instalación/Dirección ni `id_tarifa` en Consumo/Lectura. Para que esas dimensiones sean analizables, el proceso ETL debe **derivar la relación desde una fuente confiable** o solicitarla al sistema operacional.

## 4.9 Paso 6 — Crear una `DimTiempo` reutilizable

| Atributo | Ejemplo |
|---|---|
| `sk_fecha` | 20260825 |
| `fecha` | 25-08-2026 |
| `día` | 25 |
| `mes` | 8 |
| `nombre_mes` | Agosto |
| `trimestre` | T3 |
| `semestre` | S2 |
| `año` | 2026 |
| `semana` | 35 |

La clave sustituta `sk_fecha` facilita relaciones estables y permite que una misma dimensión de fecha sea **reutilizada por consumo, facturación, pagos e interrupciones**.

Se recomienda ordenar `nombre_mes` por `mes` y definir jerarquías como:
**Año → Trimestre → Mes → Día**

## 4.10 Paso 7 — Ensamblar el esquema estrella

**Tabla central:** `FactConsumo`
**Dimensiones conectadas:** `DimTiempo`, `DimCliente`, `DimInstalacion`, `DimMedidor`, `DimUbicacion` y `DimTarifa`.

```
                    DimTiempo
              (fecha, mes, trimestre, año, semana)
                         |
DimCliente                                      DimInstalacion
(tipo, segmento)                              (estado, fecha instalación)
        \                                              /
         \                                            /
          \                FactConsumo                /
           ── → Grano: medidor + fecha/periodo ← ──
          /                kWh, lecturas               \
         /                                               \
        /                                                 \
DimMedidor                                           DimUbicacion
(número, modelo)                                (comuna, ciudad, región, zona)
                         |
                    DimTarifa
                 (nombre, valor kWh)
```

La tabla de hechos conserva **claves y medidas**; las dimensiones aportan el contexto. Las relaciones esperadas son **uno a muchos** desde cada dimensión hacia `FactConsumo`.

## 4.11 Paso 8 — Convertir preguntas en métricas

| Pregunta de negocio | Medida o cálculo |
|---|---|
| ¿Cuánto consumo hubo? | `SUM(FactConsumo[kwh_consumidos])` |
| ¿Cuál es el consumo promedio por lectura? | `AVERAGE(FactConsumo[kwh_consumidos])` |
| ¿Cuántas lecturas válidas se registraron? | `SUM(FactConsumo[cantidad_lecturas])` |
| ¿Cuál es el consumo por cliente? | Consumo total / `DISTINCTCOUNT(DimCliente[id_cliente])` |
| ¿Cómo varía el consumo mes a mes? | `(Consumo actual − Consumo anterior) / Consumo anterior` |
| ¿Cuál es el costo energético estimado? | `SUM(kwh_consumidos × valor_kwh)` |

**Ejemplos de lectura del modelo:**
- Filtrar `DimUbicacion[zona]` permite analizar el consumo por zona.
- Agrupar por `DimTiempo[nombre_mes]` muestra la evolución mensual.
- Segmentar por `DimCliente[tipo_cliente]` compara residenciales, comerciales e industriales.

## 4.12 Una empresa, varios procesos: no mezclar granos

Para responder todo el caso, se recomienda una **constelación de hechos** con tablas separadas:

| Proceso | Tabla de hechos | Grano sugerido | Medidas ejemplo |
|---|---|---|---|
| Consumo | `FactConsumo` | Un medidor por fecha/periodo | kWh, lecturas |
| Facturación | `FactFactura` | Una factura por cliente | monto_total, saldo |
| Pagos | `FactPago` | Un pago por factura y fecha | monto_pagado, cantidad_pagos |
| Interrupciones | `FactInterrupcion` | Un corte por instalación | duración_horas, cantidad_cortes |

Cada hecho puede compartir **dimensiones conformadas** como `DimTiempo`, `DimCliente` y `DimUbicacion`. El desafío es **justificar el grano de cada proceso** y evitar sumar hechos de distinta naturaleza como si fueran equivalentes.

**Limitación del MER:** la entidad `Técnico` no está relacionada con una entidad de actividad técnica. Para analizar el desempeño de técnicos se requiere una entidad adicional, por ejemplo `ActividadTecnica`.

## 4.13 Cierre: del evento operativo a la decisión

**Secuencia que debe recordarse:**

1. Formular preguntas de negocio.
2. Elegir un proceso medible.
3. Declarar el grano en una frase.
4. Diseñar la tabla de hechos con claves y medidas.
5. Convertir entidades descriptivas en dimensiones.
6. Crear métricas y validar que respondan las preguntas.
7. Separar procesos cuando sus granos sean diferentes.

**Producto esperado del ejercicio:**
Un esquema estrella, el diccionario de columnas, la dimensión tiempo, al menos cinco medidas y una justificación escrita de las decisiones.

> **Frase de cierre:** Un buen modelo dimensional no solo organiza tablas; hace explícita la forma en que la empresa mide su negocio.

### Referencias citadas en la clase
1. Microsoft Learn — *"Comprender el esquema de estrella y su importancia para Power BI"*
2. Ralph Kimball — *"Keep to the Grain in Dimensional Modeling"*
3. Databricks — *"¿Qué es el esquema en estrella?"*

---

# APÉNDICE — Glosario integrado de términos clave (de las 4 clases)

| Término | Definición breve |
|---|---|
| **BI (Business Intelligence)** | Conjunto de metodologías, procesos, arquitecturas y tecnologías que convierten datos en bruto en información accionable para decidir. |
| **DSS (Decision Support System)** | Sistema de apoyo a la decisión: combina base de datos, modelo de decisión, motor de análisis, interfaz y comunicación. |
| **TPS** | Sistema Transaccional (1960s): registra operaciones diarias. |
| **MIS** | Sistema de Información de Gestión (1970s): reportes periódicos desde bases relacionales. |
| **EIS** | Sistema de Información Ejecutiva (1985-1990): tableros para alta dirección. |
| **ETL** | Extract, Transform, Load — se transforma antes de cargar. |
| **ELT** | Extract, Load, Transform — se carga primero, se transforma en el destino (estándar cloud). |
| **Data Warehouse (DW)** | Repositorio corporativo: integrado, consistente, no volátil, variante en el tiempo, temático. |
| **Data Mart** | Subconjunto departamental del DW. |
| **ODS (Operational Data Store)** | Almacén operacional de baja latencia, casi tiempo real. |
| **Data Lake** | Repositorio de dato crudo, esquema aplicado en la lectura. |
| **Lakehouse** | Combina lago + transacciones/esquema tipo warehouse. |
| **OLAP** | Online Analytical Processing: análisis multidimensional mediante cubos. |
| **ROLAP / MOLAP / HOLAP** | Variantes de implementación OLAP: relacional, multidimensional, híbrida. |
| **Cubo OLAP** | Estructura de datos organizada en dimensiones y medidas. |
| **Roll-up / Drill-down / Slice / Dice / Pivot / Drill-through** | Operaciones sobre cubos OLAP. |
| **Modelo dimensional / Esquema estrella** | Tabla de hechos rodeada de dimensiones. |
| **Esquema copo de nieve** | Dimensiones normalizadas en varios niveles. |
| **Esquema galaxia / Constelación de hechos** | Varios esquemas estrella con dimensiones conformadas compartidas. |
| **Tabla de hechos** | Contiene métricas numéricas aditivas y claves foráneas a dimensiones. |
| **Granularidad / Grano** | Nivel de detalle de cada fila de la tabla de hechos; debe ser atómico y único. |
| **Dimensión** | Atributo descriptivo que da contexto y permite filtrar/agrupar. |
| **Dimensión conformada** | Dimensión compartida de forma consistente entre distintas tablas de hechos. |
| **Clave sustituta (surrogate key, `sk_`)** | Clave técnica que facilita relaciones estables entre hechos y dimensiones. |
| **KPI** | Indicador clave de desempeño, ligado a un objetivo, con fórmula, dueño, meta y frecuencia. |
| **Single Source of Truth (SSOT)** | Única versión de la verdad para toda la organización. |
| **DIKW** | Jerarquía Dato → Información → Conocimiento → Decisión → Acción → Valor. |
| **KDD (Knowledge Discovery in Databases)** | Proceso integral de descubrimiento de conocimiento, del cual la minería de datos es una etapa. |
| **Machine Learning (ML)** | Rama de la IA que aprende de los datos sin programación explícita. |
| **Minería de datos** | Descubrir patrones, correlaciones y tendencias en grandes conjuntos de datos. |
| **Aprendizaje supervisado / no supervisado / por refuerzo** | Tipos de ML según el uso de etiquetas y retroalimentación. |
| **Clustering** | Agrupación de datos por similitud sin etiquetas (ej. K-means). |
| **PCA** | Análisis de Componentes Principales, técnica de reducción de dimensionalidad. |
| **Analítica descriptiva/diagnóstica/predictiva/prescriptiva/cognitiva** | Escalera de madurez analítica: qué pasó → por qué → qué pasará → qué hacer → simula razonamiento humano. |
| **Gobierno de datos** | Data owner, data steward, MDM, linaje, seguridad. |
| **MDM (Master Data Management)** | Gestión de datos maestros: identificador único de cliente/producto/proveedor. |
| **XAI (Explainable AI)** | IA explicable: hace comprensibles los modelos complejos. |
| **Overfitting / Underfitting** | Sobreajuste (el modelo memoriza en vez de generalizar) / subajuste (no capta los patrones). |
| **MER (Modelo Entidad-Relación)** | Modelo operacional normalizado que registra transacciones y mantiene integridad referencial; base de partida para derivar un modelo dimensional. |
