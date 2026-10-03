# Resumen — Inteligencia de Negocios (BI)

Este documento resume los cuatro materiales de la unidad: **Clase 1 (Business Intelligence)**, **Clase 2 (teoría: DSS, análisis inteligente, ML/minería de datos, arquitectura DW)**, **Laboratorio de la Clase 2 (taller práctico)** y **De OLTP a OLAP (modelado dimensional, metodología Kimball)**.

---

## 1. Clase 1 — Business Intelligence: qué es y su arquitectura

**Casos iniciales (Amazon, Mercado Libre, Coca-Cola):** muestran BI en la práctica antes de la teoría, usando el marco *qué decide / qué datos usa / cómo decide*. Conclusión: BI es un patrón repetido en industrias distintas — convertir datos dispersos en una decisión mejor.

**Definición de BI:** combina la definición de **Gartner** (metodologías, procesos, arquitecturas y tecnologías que transforman datos operacionales en información accionable) con una definición práctica: **Capturar → Organizar → Analizar → Decidir**. El valor de BI está en reducir la discusión sobre qué número es correcto.

**Por qué surge BI:** el problema no es tecnológico sino de **pérdida de confianza en la información** (sistemas duplicados, reportes distintos, Excel descentralizado). El ejemplo de "¿cuál es la cifra correcta?" (Ventas, Finanzas y Gerencia con tres cifras distintas) introduce el concepto de **Single Source of Truth**, motivación central del Data Warehouse.

**Objetivos y niveles de decisión:** todos los objetivos de BI convergen en decidir mejor y más rápido. Existen tres niveles organizacionales — **estratégico** (años), **táctico** (meses) y **operacional** (días) — que consumen el mismo dato con distinto nivel de detalle.

**Evolución histórica:** TPS (1960s) → MIS (1970s) → DSS (1980s) → EIS (1985-90) → BI/DW/ETL/OLAP (1990s) → Big Data (2000s) → Machine Learning (2010s) → IA generativa (2020s). Cada etapa amplía, no reemplaza, a la anterior.

**Arquitectura de referencia (5 capas):** Fuentes → Integración → Almacenamiento → Análisis → Explotación, atravesadas por gobierno de datos (metadatos, catálogo, seguridad, linaje). La **integración concentra 60-80% del esfuerzo** de un proyecto BI.

**ETL vs. ELT:** ETL (Extract-Transform-Load) transforma antes de cargar, bueno para volúmenes acotados; ELT (Extract-Load-Transform) carga primero y transforma dentro del DW, estándar en arquitecturas cloud. Frase clave: *"un dashboard elegante sobre datos sucios entrega decisiones equivocadas con apariencia de rigor."*

**Calidad de datos (6 dimensiones):** exactitud, completitud, consistencia, oportunidad, unicidad, validez. **Gobierno de datos:** data owner (negocio) vs. data steward (operativo), MDM (identificador único por entidad), linaje y metadatos.

**Data Warehouse (Bill Inmon):** variante en el tiempo, integrado, consistente, no volátil, temático.

**Modelado dimensional:** esquema en estrella = tabla de hechos (métricas aditivas + FK) + dimensiones (contexto para filtrar/agrupar). La **granularidad** (qué representa una fila) es la decisión de diseño más determinante.

**Data Mart:** subconjunto del DW por área de negocio; debe derivar del DW (nunca construirse aparte) para no recrear silos.

**Cubos OLAP y operaciones:** roll-up, drill-down, slice, dice, pivot, drill-through — permiten que la misma solución sirva a los tres niveles de decisión.

**Implementaciones OLAP:** ROLAP (relacional, escalable), MOLAP (multidimensional, rápido pero menos escalable), HOLAP (híbrido). Optimización: índices/particionado, vistas materializadas, almacenamiento columnar.

**Ecosistema de repositorios:** Data Mart, ODS (baja latencia, poca historia), Data Lake (esquema en la lectura), Lakehouse (combina ambos). No hay una arquitectura única correcta: depende del dato, la latencia, el consumo y el costo.

**Dashboards y KPIs:** *"un dashboard no es el proyecto: es su resultado visible."* Un KPI requiere fórmula, dueño, meta y frecuencia — *"sin meta no hay indicador, sólo una cifra."* La capa semántica traduce tablas físicas a conceptos de negocio.

**Arquitectura integrada:** Fuentes → ETL → DW → Data Mart → Modelo Estrella → Power BI → Dashboard → Gerencia. *"El valor no está en ninguna capa aislada, sino en que todas conversen entre sí."*

**Tipos de datos:** estructurados, semiestructurados, no estructurados (hoy la mayoría del dato empresarial es no estructurado).

**Ciclo DIKW:** Dato → Información → Conocimiento → Decisión → Acción → Valor; cada capa reduce volumen pero aumenta valor.

**Conclusión de la clase:** BI no es solo dashboards; es tecnologías + procesos + personas = información confiable para decidir. Ideas clave: BI es arquitectura no herramienta; la granularidad define el modelo; la calidad se diseña, no se corrige; la latencia se ajusta a la decisión.

---

## 2. Clase 2 (teoría) — De los datos a la decisión

Amplía el marco conceptual: sitúa a BI dentro de los DSS, el análisis inteligente de datos, el machine learning y la minería de datos.

### Módulo 1 — DSS y ciclo de vida del dato
Un **DSS** tiene 5 componentes: base de datos, modelo de decisión, motor de análisis, interfaz de usuario, comunicación. BI **incorpora** un DSS (junto con OLAP), no lo reemplaza.

**Ciclo de vida del dato (6 etapas):** Captura → Almacenamiento → Procesamiento/transformación → Análisis y consulta → Reportes y visualización → Mantenimiento, archivado y eliminación (nueva respecto a la Clase 1, conecta con normativas de protección de datos).

### Módulo 2 — Análisis inteligente de datos
Combina IA, ML y estadística para pasar de lo descriptivo/reactivo a lo **proactivo y automatizado**. Objetivos: descubrir patrones, predecir, automatizar decisiones, optimizar. Técnicas: aprendizaje supervisado, no supervisado, reforzado, análisis predictivo, prescriptivo, NLP y redes complejas. Aplicaciones por industria (negocios, salud, finanzas, RRHH). Desafíos: calidad de datos, interpretación (XAI), privacidad/seguridad, escalabilidad.

### Módulo 3 — Business Intelligence (redefinición)
BI combina análisis de negocios, minería de datos, visualización, herramientas e infraestructura. **Evolución del rol del usuario:** BI tradicional (dependiente de TI) → BI moderno (self-service) → BI con IA generativa (lenguaje natural). **OLAP y DSS son componentes dentro de BI** — jerarquía clave: DSS y OLAP son piezas; BI es el marco integrador. Elementos clave: fuentes, integración, calidad, acceso del usuario. Valor: mejores decisiones, tendencias, operaciones optimizadas, menor riesgo, mejor experiencia y servicio al cliente.

### Módulo 4 — Machine learning y minería de datos
**ML** = técnica que aprende de datos sin programación explícita. **Minería de datos** = proceso de descubrir patrones (más amplio, puede usar ML o estadística). Tipos de ML: supervisado (regresión, árboles, SVM, redes neuronales), no supervisado (K-means, PCA), por refuerzo (Q-learning), semi/auto-supervisado (base de los modelos fundacionales/LLMs). Técnicas de minería: clasificación, regresión, clustering, asociación (Apriori), detección de anomalías, reducción de dimensionalidad. Relación con estadística: ML se apoya en inferencia estadística, no la reemplaza.

**Tipos de analítica (progresión):** Descriptiva ("qué pasó") → Diagnóstica ("por qué pasó") → Predictiva ("qué pasará") → Prescriptiva ("qué hacer") → Cognitiva (simula razonamiento humano, IA generativa).

**Minería de datos y KDD:** la minería de datos es solo **una etapa** dentro del proceso KDD (Knowledge Discovery in Databases), que abarca desde la selección/preprocesamiento hasta la presentación del conocimiento.

### Módulo 6 — Arquitectura de un Data Warehouse
Capas: Raw Data → Staging → Warehouse → Analytics (OLAP/semántica) → Presentation (data marts), rodeadas de seguridad, calidad, metadatos, linaje. Consumidores: BI, analítica avanzada, ML, reporting, self-service.

**Construir el repositorio analítico (4 etapas):**
1. **Análisis:** entrevistar stakeholders, definir KPIs, inventariar fuentes.
2. **Diseño:** modelado conceptual/lógico/físico, elegir estrella/copo de nieve, ETL/ELT, reporting.
3. **Implementación:** configurar plataforma (BigQuery, Snowflake, Databricks, Redshift, Fabric), desarrollar y validar.
4. **Mantenimiento:** monitorear rendimiento/calidad, escalar, capacitar.

**Modelamiento multidimensional (profundización):** elementos — cubos, dimensiones, medidas, **jerarquías** (habilitan roll-up/drill-down), tablas de hechos, **dimensiones conformadas** (usadas de forma consistente entre cubos).

**Esquemas:** Estrella (simple, redundante), Copo de nieve (normalizado, más joins), Galaxia/constelación (varios esquemas estrella con dimensiones conformadas — típico de un DW corporativo).

**Pasos del modelado (5):** definir requisitos → diseñar esquema → dimensiones y medidas → implementar y validar → documentar y capacitar.

**Problemáticas de la extracción de conocimiento:** calidad de datos, volumen/complejidad, **overfitting/underfitting**, interpretabilidad, privacidad/sesgo (puede **amplificarse**), escalabilidad.

**Síntesis final:** *"Capturar y gobernar el dato, modelarlo para el análisis, aplicar técnicas inteligentes y comunicar el conocimiento para decidir mejor."*

---

## 3. Laboratorio Clase 2 — BI en acción (taller práctico)

Taller de 3 horas (carrera de Ciencia de Datos) con caso transversal: una **agencia de viajes**. Objetivos: explicar el rol de BI por área, identificar componentes, aplicar el ciclo de vida, diseñar una solución.

**Repaso:** BI mira el **pasado y presente** (no predice por sí solo). Qué NO es BI: no es solo un dashboard bonito, no reemplaza el criterio humano, no predice (eso es analítica avanzada).

### Bloque 1 — BI en las áreas funcionales
Misma plataforma, preguntas distintas por área:
- **Marketing:** "¿A quién le hablo y con qué retorno?" — KPI: CAC, ROAS, conversión. Ejemplo: pasar de optimizar clics a optimizar margen por pasajero.
- **Finanzas:** "¿Cómo se comporta el dinero?" — KPI: margen por reserva, desviación presupuestaria. Ejemplo: de 5 días consolidando planillas a día 2; *"el valor no fue el gráfico: fue recuperar tres días de análisis."*
- **RRHH:** "¿Quién sostiene la operación?" — KPI: rotación, tiempo/costo de contratación. Ejemplo: rotación se dispara entre mes 3-5; solución fue rediseñar el acompañamiento, no subir sueldos.
- **Operaciones:** "¿Cómo entrego mejor, más rápido y más barato?" — KPI: ocupación, puntualidad. Ejemplo: 70% de atrasos en vuelos 17-20h; la frecuencia de actualización es crítica (un dato diario llega tarde).

Regla práctica: *"si no puedes escribir la pregunta de negocio en una frase, todavía no estás listo para construir el tablero."*

### Bloque 2 — Componentes de un sistema de BI
Tres componentes: **Datos** (origen interno/externo/generado; naturaleza estructurada/semi/no estructurada; temporalidad histórica/tiempo real/snapshot), **Procesos** (Extraer → Transformar → Cargar → **Modelar** → **Publicar** — versión ampliada del ETL clásico), **Herramientas** (stack por capas: fuentes, integración, almacenamiento, análisis, visualización).

*"Un sistema de BI falla por su eslabón más débil: datos sucios con la mejor herramienta siguen siendo datos sucios."*

**Distribución típica del esfuerzo:** requerimientos 15% · **integración y limpieza 40%** · modelado 20% · visualización 15% · adopción 10%. *"El dashboard es la punta del iceberg."*

### Bloque 3 — Ciclo de vida del proyecto BI (6 fases, es un ciclo, no una línea recta)
1. **Planificación** → caso de negocio (avanza cuando el patrocinador firma).
2. **Requerimientos** → catálogo de indicadores (avanza cuando cada uno tiene dueño, fórmula, fuente).
3. **Diseño** → modelo dimensional/prototipo (avanza cuando el usuario reconoce sus números).
4. **Desarrollo** → flujos y tableros probados (avanza cuando las pruebas de calidad cuadran).
5. **Despliegue** → producción (avanza con adopción real, sin recordatorio).
6. **Evolución** → backlog priorizado; éxito = *"el tablero cambia decisiones, no solo se mira."*

**Errores frecuentes:** empezar por la herramienta; métricas sin dueño (el problema de las "múltiples verdades"); el proyecto de un año (iterar corto en su lugar); ignorar la adopción.

**Síntesis del taller:**
1. "BI cambia de preguntas según el área, no de naturaleza."
2. "Datos, procesos y herramientas son un solo sistema: el eslabón débil manda."
3. "El ciclo de vida es iterativo y termina en el uso, no en la entrega."

---

## 4. De OLTP a OLAP — Modelado dimensional (metodología Kimball)

### Parte 1 · Caso Retail "Casa Norte"
Cadena de 42 tiendas + canal online, ERP OLTP normalizado (14 tablas), lento para analizar. Objetivo: DW dimensional que responda en segundos.

**OLTP vs. OLAP:** registrar la operación (normalizado, 3FN, muchos JOIN) vs. analizar el negocio (desnormalizado, esquema estrella, guarda historia con SCD, optimizado para lectura/agregación).

**Ralph Kimball:** autor de *The Data Warehouse Toolkit*; enfoque **bottom-up** (data marts incrementales), arquitectura **bus** (dimensiones conformadas), alternativa práctica al enfoque normalizado de Bill Inmon.

**Los 4 pasos de Kimball:**
1. **Elegir el proceso de negocio:** un evento medible = una tabla de hecho (nunca por departamento o informe). Caso: Venta y Reposición/Inventario.
2. **Declarar la granularidad:** "una fila de esta tabla representa ______", siempre al nivel más atómico, un solo grano por tabla. Caso: línea de boleta / producto-tienda-día.
3. **Identificar dimensiones:** quién, qué, dónde, cuándo, cómo — se desnormalizan con jerarquías y se conforman entre procesos.
4. **Identificar los hechos (medidas):** preferir aditivas, marcar semi-aditivas (stock), incluir dimensiones degeneradas (nro. de boleta).

**Regla de oro:** nunca elegir dimensiones/medidas antes de declarar el grano.

**Hecho vs. dimensión vs. descarte:** hecho = evento con fecha y valores numéricos sumables; dimensión = contexto (tabla maestra, pocos registros); se descarta lo técnico/sin valor analítico (usuarios, auditoría).

**Modelo final:** `fact_ventas` (grano: línea de boleta) + `fact_inventario_diario` (grano: producto/tienda/día), unidas por **dimensiones conformadas** (Tiempo, Producto, Tienda) — matriz bus. Un solo DW con arquitectura bus (nunca dos DW separados) permite drill-across y evita silos ("stovepipes"). Los hechos no se relacionan directamente entre sí; se conectan vía dimensiones compartidas. Cada hecho + sus dimensiones forma un **data mart** dentro del mismo DW (Comercial, Operaciones).

**Ejercicio "Gimnasio Vitalis":** aplica los 4 pasos a un caso nuevo (contratos y accesos por torniquete), reforzando la práctica con dimensiones conformadas (tiempo, socio, sucursal) y medidas semi-aditivas.

### Parte 2 · Caso Energía "Energía Sur"
Transforma un **MER** (modelo entidad-relación) en modelo dimensional siguiendo la ruta: preguntas de negocio → proceso → grano → hechos → dimensiones → métricas → validación.

- **Proceso elegido:** consumo energético por medidor.
- **Grano:** una fila de `FactConsumo` = un medidor, una instalación, una fecha/periodo de lectura.
- **Tabla de hechos:** claves foráneas a Tiempo, Cliente, Instalación, Medidor, Zona, Tarifa; medidas: lectura actual/anterior, kWh consumidos (aditiva), cantidad de lecturas.
- **Dimensiones:** DimCliente, DimUbicacion, DimInstalacion, DimMedidor, DimTarifa, DimTiempo (reutilizable, con jerarquía Año→Trimestre→Mes→Día).
- **Métricas:** consumo total, promedio, por cliente, variación mensual, costo estimado.
- **Constelación de hechos futura:** FactConsumo, FactFactura, FactPago, FactInterrupcion, compartiendo dimensiones conformadas (Tiempo, Cliente, Ubicación) — sin mezclar granos de procesos distintos.

**Cierre común a ambos casos:** formular preguntas → elegir proceso → declarar grano → diseñar tabla de hechos → convertir entidades en dimensiones → crear y validar métricas → separar procesos con granos distintos. *"Un buen modelo dimensional no solo organiza tablas; hace explícita la forma en que la empresa mide su negocio."*

---

## Hilo conductor de toda la unidad

1. **Clase 1** explica la **arquitectura** de una solución BI (fuentes → ETL → DW → OLAP → dashboards) y por qué existe (problema de la "única versión de la verdad").
2. **Clase 2 (teoría)** amplía el marco: BI convive con DSS, análisis inteligente, ML y minería de datos, todo unido por el mismo propósito de decidir mejor.
3. **El laboratorio** lleva esa teoría a la práctica con un caso realista (agencia de viajes), aplicando áreas funcionales, componentes (datos/procesos/herramientas) y el ciclo de vida de un proyecto BI.
4. **De OLTP a OLAP** entrega la técnica concreta —metodología de Kimball— para pasar de un modelo transaccional (OLTP) a un modelo dimensional (OLAP) mediante los 4 pasos: proceso, grano, dimensiones y hechos, aplicados en dos industrias distintas (retail y energía).
