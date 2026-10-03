# Inteligencia de Negocios — Explicación de los contenidos de la Clase 2

Esta clase (2026, Semestre 2) es la continuación de la unidad introductoria de BI. Mientras la primera clase se centró en la arquitectura y los componentes de una solución BI (fuentes, ETL, Data Warehouse, OLAP, dashboards), esta segunda clase da un paso hacia atrás y hacia adelante al mismo tiempo: hacia atrás, situando a BI dentro de un concepto más amplio (los DSS y el ciclo de vida del dato); y hacia adelante, conectando BI con machine learning, minería de datos y el proceso KDD. El subtítulo de la clase lo resume bien: **"de los datos a la decisión"**.

A continuación se explica cada módulo del temario.

---

## Módulo 1 — Fundamentos: DSS y ciclo de vida de los datos

### Componentes principales de un DSS

Antes de hablar de BI, la clase retoma el concepto de **DSS (Decision Support System / Sistema de Soporte a la Decisión)**, que en la Clase 1 apareció solo como un punto en la línea de tiempo histórica (años 80). Aquí se explica **de qué está hecho** un DSS, descomponiéndolo en cinco componentes:

- **Base de datos:** los datos internos y externos, históricos y actuales, que alimentan el sistema (por ejemplo, ventas o datos de mercado).
- **Modelo de decisión:** los modelos y algoritmos que interpretan esos datos y generan una recomendación (por ejemplo, un modelo de pronóstico o de simulación).
- **Motor de análisis:** el componente que ejecuta los cálculos necesarios para convertir datos en información útil (por ejemplo, optimización).
- **Interfaz de usuario:** lo que permite consultar, explorar y visualizar los resultados (dashboards, análisis ad-hoc).
- **Comunicación:** el mecanismo que comparte los hallazgos y habilita que la decisión se tome de forma colaborativa (por ejemplo, reportes automatizados).

La idea importante aquí es que un DSS **no es solo un dashboard ni solo una base de datos**: es la combinación de estos cinco elementos trabajando juntos. Este desglose es relevante porque, como se verá más adelante, BI en realidad **incorpora** un DSS como uno de sus componentes (junto con OLAP), no lo reemplaza.

### Ciclo de vida de los datos

Se presenta un ciclo de seis etapas por las que pasa un dato desde que se genera hasta que deja de ser útil:

1. **Captura:** recolección desde las fuentes, definiendo formatos y frecuencia de captura.
2. **Almacenamiento:** guardar los datos en el data warehouse o en sistemas relacionados.
3. **Procesamiento y transformación:** limpieza y preparación de los datos para que puedan analizarse (esto es, en esencia, el ETL/ELT visto en la clase anterior).
4. **Análisis y consulta:** generación de información útil a partir del dato ya transformado.
5. **Reportes y visualización:** construcción de informes y paneles según lo que necesite cada usuario.
6. **Mantenimiento, archivado y eliminación:** gestión de qué datos siguen vigentes, cuáles pasan a ser históricos, y cumplimiento de normativas que exigen eliminar o conservar cierta información.

Esta es una versión más detallada y operativa del ciclo DIKW (Dato → Información → Conocimiento → Decisión → Acción → Valor) visto en la Clase 1. Mientras el DIKW explica el **valor conceptual** que gana un dato en cada etapa, este ciclo de vida explica el **proceso técnico y de gestión** por el que atraviesa el dato en la práctica, incluyendo una etapa que antes no se mencionaba explícitamente: qué pasa con el dato cuando ya no es necesario (archivado y eliminación), lo cual conecta con temas de cumplimiento normativo (por ejemplo, leyes de protección de datos).

---

## Módulo 2 — Análisis inteligente de datos

Este módulo introduce un concepto nuevo respecto a la Clase 1: el **análisis inteligente de datos**, presentado explícitamente como una evolución de lo descriptivo y reactivo hacia lo proactivo y automatizado.

### ¿Qué es el análisis inteligente de datos?

Se define como la combinación de **inteligencia artificial, aprendizaje automático y estadística** para interpretar datos complejos. Sus capacidades principales son descubrir patrones, predecir resultados y recomendar acciones. La diferencia clave respecto al análisis tradicional (que la Clase 1 asociaba a dashboards y reportes descriptivos) es que este tipo de análisis entrega **recomendaciones proactivas y automatizadas**, en vez de solo mostrar lo que ya ocurrió. Se menciona también que hoy este análisis se apoya cada vez más en modelos de lenguaje e IA generativa, lo cual conecta con la etapa "2020s – Inteligencia Artificial" de la línea de tiempo vista en la Clase 1.

### Objetivos del análisis inteligente de datos

Se listan cuatro objetivos, que en cierto modo son una versión más "inteligente" de los objetivos de BI vistos en la clase anterior:

- **Descubrimiento de patrones:** identificar relaciones ocultas que no son evidentes a simple vista.
- **Predicción:** usar datos históricos para anticipar eventos o comportamientos futuros.
- **Automatización de decisiones:** decidir de forma automática o semi-automática mediante algoritmos (esto va más allá de lo que hacía un DSS clásico, que apoyaba a una persona a decidir, pero no decidía por sí mismo).
- **Optimización:** mejorar procesos y sistemas con recomendaciones basadas en datos.

### Técnicas del análisis inteligente de datos

Se presentan seis técnicas o enfoques:

- **Aprendizaje supervisado:** se entrena con datos ya etiquetados para luego predecir sobre datos nuevos (regresión, clasificación, redes neuronales).
- **Aprendizaje no supervisado:** descubre patrones y estructuras en datos que no tienen etiquetas (clustering, reducción de dimensionalidad).
- **Aprendizaje reforzado:** aprende tomando decisiones y recibiendo recompensas o penalizaciones según el resultado (usado en control y optimización).
- **Análisis predictivo:** anticipa resultados futuros mediante series temporales, regresión o clasificación predictiva.
- **Análisis prescriptivo:** no solo predice, sino que recomienda las mejores acciones a tomar (optimización de recursos, simulación de estrategias).
- **NLP y redes complejas:** interpreta texto no estructurado (análisis de sentimiento, asistentes conversacionales) y analiza interacciones dentro de redes.

Esta lista funciona como un mapa general de técnicas que se profundizarán con más detalle más adelante, en el Módulo 4 (Machine learning y minería de datos).

### Aplicaciones del análisis inteligente de datos

Se muestran ejemplos concretos por industria, en el mismo estilo que los casos de Amazon, Mercado Libre y Coca-Cola de la Clase 1, pero ahora organizados por sector en vez de por empresa:

- **Negocios:** segmentación y personalización en marketing, detección de fraude en gestión de riesgos, optimización de inventarios y demanda en operaciones.
- **Salud:** diagnóstico predictivo usando datos clínicos y genéticos, y detección de anomalías en imágenes médicas.
- **Finanzas:** previsión de tendencias de mercado e identificación de transacciones sospechosas.
- **Recursos humanos:** análisis de currículos, predicción de desempeño y gestión de talento y retención.

### Desafíos y consideraciones

Se listan cuatro desafíos, cada uno con su solución asociada:

- **Calidad de los datos:** datos incompletos o sesgados generan conclusiones erróneas; se soluciona con limpieza y validación robustas (este desafío ya se había visto en la Clase 1, en la sección de gobierno de datos, pero ahora se aplica específicamente al contexto de modelos de IA/ML, donde un dato sesgado no solo genera un reporte incorrecto, sino un modelo que aprende mal).
- **Interpretación de resultados:** los modelos complejos (como redes neuronales) son difíciles de explicar; la solución mencionada es la visualización y la **IA explicable (XAI)**, un concepto nuevo que no aparecía en la Clase 1.
- **Privacidad y seguridad:** al manejar información sensible, se requiere anonimización, control de acceso y cumplimiento normativo.
- **Escalabilidad:** los volúmenes de datos crecen constantemente, lo que exige arquitecturas distribuidas y en la nube.

---

## Módulo 3 — Inteligencia de Negocios (BI)

Este módulo retoma directamente el tema central de la Clase 1, pero con una mirada distinta: en vez de explicar la arquitectura capa por capa, se enfoca en **redefinir qué es BI** dentro del marco más amplio que se viene construyendo (DSS, ciclo de vida del dato, análisis inteligente), y en explicar su evolución y el valor que aporta.

### ¿Qué es Business Intelligence?

Se ofrece una definición que combina varios elementos vistos por separado en la Clase 1: BI combina **análisis de negocios, minería de datos, visualización, herramientas e infraestructura de datos**. Se reafirma que es el conjunto de tecnologías, procesos y prácticas que permiten analizar datos para decidir, e implica una **vista integral de todos los datos de la organización** (esto es equivalente al concepto de "Single Source of Truth" visto antes). Se agrega un matiz nuevo: BI busca **impulsar el cambio, eliminar ineficiencias y adaptarse rápido al mercado** — es decir, no se presenta solo como una herramienta de control, sino como una capacidad de adaptación organizacional.

### Evolución del BI

Se presenta una evolución de BI en tres etapas, que es más simple que la línea de tiempo tecnológica de la Clase 1 (TPS, MIS, DSS, EIS, BI, Big Data, ML, IA), pero complementaria — se enfoca en cómo cambió el **rol del usuario** frente a los datos, no en qué tecnología existía:

- **BI tradicional (1960–1980):** un sistema para compartir información entre organizaciones, operado por equipos de TI. El usuario de negocio dependía de especialistas técnicos para obtener sus reportes.
- **BI moderno:** aparece el análisis de autoservicio (*self-service*), con datos gobernados en plataformas confiables, lo que da autonomía al usuario de negocio y permite obtener información mucho más rápido, sin depender tanto de TI.
- **BI con IA generativa:** la etapa más reciente, donde aparecen asistentes que permiten consultar los datos en lenguaje natural y generar explicaciones automáticas — el usuario ya no necesita saber SQL ni construir un dashboard manualmente para obtener una respuesta.

### OLAP y DSS dentro del BI

Este es uno de los slides más importantes para entender **cómo se conecta esta clase con la anterior**: se explica que tanto OLAP como DSS son **componentes esenciales dentro de BI**, y que BI los combina con prácticas y tecnologías adicionales para transformar datos en valor. Esto aclara la relación jerárquica entre los conceptos: un DSS es un sistema de apoyo a decisiones (visto en el Módulo 1), OLAP es la tecnología de análisis multidimensional (vista en la Clase 1), y **BI es el marco más amplio que integra ambos**, junto con la infraestructura de datos, los procesos de gobierno y las herramientas de visualización.

### Conceptos clave de BI

Se repasan seis conceptos, la mayoría ya vistos en la Clase 1 pero ahora resumidos como un glosario compacto:

- **Data warehousing:** el repositorio centralizado que integra datos de múltiples fuentes.
- **ETL / ELT:** los procesos que mueven y transforman los datos hacia el repositorio analítico.
- **Reporting:** informes y visualizaciones que hacen comprensible la información.
- **Dashboards:** vista consolidada de KPIs y métricas para monitoreo en tiempo real.
- **Análisis predictivo y prescriptivo:** anticipar eventos y recomendar acciones (por ejemplo, en demanda o cadena de suministro) — este concepto conecta directamente con lo visto en el Módulo 2.
- **Análisis aumentado con IA:** poder preguntarle a los datos en lenguaje natural, generar resúmenes automáticos o hacer análisis de sentimiento — la aplicación práctica de la etapa "BI con IA generativa" mencionada arriba.

### Elementos clave de BI

Se listan cuatro elementos que deben existir para que BI funcione: **fuentes de datos** diversas (bases de datos, archivos, aplicaciones, servicios), **integración de datos** (combinar esas fuentes en un conjunto coherente), **calidad de datos** (asegurar precisión, completitud y consistencia) y **acceso del usuario** (que las personas autorizadas puedan llegar a los datos y análisis que necesitan). Estos cuatro elementos son, en esencia, una síntesis de la arquitectura completa vista en la Clase 1 (fuentes → integración → almacenamiento con calidad → explotación con acceso de usuario), pero presentados como requisitos, no como capas técnicas.

### Cómo el BI agrega valor

Se presentan seis formas en que BI genera valor concreto para una organización:

- **Mejores decisiones:** gracias a la visibilidad completa de datos y KPIs, con informes y paneles que facilitan interpretar información compleja.
- **Tendencias y oportunidades:** identificar tendencias de mercado y ventas, descubriendo nuevas oportunidades de negocio.
- **Operaciones optimizadas:** detectar ineficiencias en los procesos y mejorar la asignación de recursos.
- **Menor riesgo:** anticipar y mitigar riesgos con análisis predictivo, y monitorear el cumplimiento normativo.
- **Experiencia del cliente:** segmentar y personalizar ofertas según el comportamiento y las preferencias del cliente.
- **Mejor servicio:** entregar información relevante sobre las interacciones y necesidades de los clientes.

Este slide funciona como el "para qué sirve todo esto" del módulo, cerrando el círculo que empezó con la definición formal de BI.

---

## Módulo 4 — Machine learning y minería de datos

Este módulo profundiza técnicamente en lo que el Módulo 2 solo esbozó de forma general ("análisis inteligente de datos"). Aquí se entra en el detalle de **qué es** machine learning, **qué es** minería de datos, y **cómo se relacionan** entre sí y con la estadística.

### Machine learning y minería de datos

Se distinguen ambos conceptos, que suelen confundirse:

- **Aprendizaje automático (Machine Learning):** una rama de la inteligencia artificial que permite aprender de los datos y predecir o decidir **sin ser programado explícitamente** para cada caso. El sistema se entrena con datos y generaliza patrones a partir de ellos.
- **Minería de datos:** el proceso de descubrir patrones y conocimientos útiles en grandes conjuntos de datos, utilizando estadística, algoritmos de machine learning y visualización.

La diferencia sutil entre ambos es que **machine learning es una técnica** (un tipo de algoritmo que aprende), mientras que **minería de datos es un proceso** (una actividad más amplia que puede usar machine learning, pero también estadística tradicional u otras herramientas) orientado específicamente a **descubrir conocimiento** dentro de datos ya existentes.

### Tipos de aprendizaje automático

Se profundiza en los tipos de aprendizaje mencionados de forma más breve en el Módulo 2, ahora con ejemplos de algoritmos concretos:

- **Supervisado:** usa datos etiquetados para aprender a mapear entradas a salidas. Algoritmos típicos: regresión lineal, árboles de decisión, SVM (máquinas de soporte vectorial), redes neuronales.
- **No supervisado:** busca estructuras o patrones en datos que no tienen etiquetas. Algoritmos típicos: K-means, clustering jerárquico, PCA (análisis de componentes principales).
- **Por refuerzo:** el sistema decide interactuando con un entorno y recibiendo recompensas o penalizaciones según el resultado de sus acciones. Algoritmos típicos: Q-learning, Deep Q-Networks.
- **Semi y auto-supervisado:** combina una pequeña cantidad de datos etiquetados con grandes volúmenes de datos sin etiquetar. Se destaca que este enfoque es la **base de los modelos fundacionales actuales** (los grandes modelos de lenguaje, por ejemplo), lo cual conecta con el punto de "IA generativa" mencionado varias veces en la clase.

### Técnicas de minería de datos

Se presentan seis técnicas específicas de minería de datos, que en la práctica se apoyan en los tipos de aprendizaje automático recién descritos:

- **Clasificación:** asigna una etiqueta a un dato nuevo (árboles de decisión, Naive Bayes, redes neuronales).
- **Regresión:** predice un valor numérico continuo (regresión lineal y polinómica).
- **Clustering:** agrupa datos por similitud, sin etiquetas previas (K-means, clustering jerárquico).
- **Asociación:** descubre relaciones entre variables mediante reglas de asociación (por ejemplo, el algoritmo Apriori, usado clásicamente en "análisis de la canasta de compra").
- **Detección de anomalías:** identifica datos que se salen del patrón normal, útil para detectar errores o fraude (modelos estadísticos, isolation forest).
- **Reducción de dimensionalidad:** simplifica un conjunto de datos conservando la información relevante (análisis de componentes principales, PCA).

Nótese que clasificación y regresión son técnicas de minería de datos que típicamente usan aprendizaje **supervisado**, mientras que clustering y reducción de dimensionalidad usan aprendizaje **no supervisado** — es decir, este slide es, en la práctica, una aplicación concreta de los tipos de aprendizaje vistos justo antes.

### Relación con la estadística

Este slide es importante porque conecta el machine learning con una disciplina mucho más antigua: la **estadística**, dejando claro que no son cosas separadas sino que una se apoya en la otra:

- La estadística provee la **base teórica** de muchas técnicas de ML y minería de datos.
- La **inferencia estadística** sustenta predicciones y clasificaciones, como ocurre en la estimación de parámetros de una regresión lineal.
- **Modelos estadísticos** como la regresión logística y los árboles de decisión se basan en principios estadísticos clásicos.
- **Pruebas de hipótesis y ANOVA** se usan para validar modelos y evaluar su desempeño.

El mensaje de fondo es que machine learning **no reemplaza** a la estadística, sino que la utiliza y la extiende: muchos algoritmos "modernos" de ML son, en el fondo, aplicaciones prácticas de conceptos estadísticos que existen desde hace décadas.

### Tipos de analítica

Se presenta una clasificación de cinco tipos de analítica, organizados según la pregunta que responden — esta es una forma muy útil de ordenar todo lo visto hasta ahora en un solo esquema progresivo:

- **Descriptiva — "Qué pasó":** usa estadística descriptiva y visualización; explora y prepara los datos para el modelado. Es el tipo de análisis más básico, asociado a los dashboards y reportes vistos en la Clase 1.
- **Diagnóstica — "Por qué pasó":** usa correlación y minería de datos para identificar patrones y relaciones históricas que expliquen un resultado.
- **Predictiva — "Qué pasará":** usa regresión, clasificación y machine learning; es la base de los modelos de predicción.
- **Prescriptiva — "Qué hacer":** usa optimización y simulación para recomendar acciones que mejoren los resultados.
- **Cognitiva:** simula el razonamiento humano usando redes neuronales profundas y procesamiento del lenguaje natural; es el nivel más avanzado, y conecta con la idea de IA generativa mencionada repetidamente en la clase.

Esta progresión (descriptiva → diagnóstica → predictiva → prescriptiva → cognitiva) es en el fondo la misma idea que la línea de tiempo tecnológica de la Clase 1 (TPS/MIS → DSS → EIS/BI → Big Data → Machine Learning → IA), pero expresada como **niveles de sofisticación del análisis** en vez de como hitos históricos.

### Minería de datos y proceso KDD

Se cierra el módulo formalizando la relación entre minería de datos y un proceso más amplio llamado **KDD (Knowledge Discovery in Databases / Descubrimiento de Conocimiento en Bases de Datos)**:

- La **minería de datos** es la técnica específica para descubrir patrones, correlaciones y tendencias útiles en grandes conjuntos de datos.
- El **KDD** es el proceso integral completo, que va desde la selección y el preprocesamiento de los datos hasta la presentación y el uso final del conocimiento obtenido.
- El punto clave es que **la minería de datos es solo una etapa dentro del proceso KDD**, no el proceso completo — es decir, minar datos (aplicar el algoritmo) es apenas una parte de un flujo mucho más largo que incluye preparar los datos antes y comunicar/usar los resultados después.

---

## Módulo 6 — Arquitectura de un data warehouse

Nota: el temario salta del módulo 4 al módulo 6 (no hay contenido explícito de un "módulo 5" en las diapositivas provistas), pero el contenido continúa de forma natural.

Este módulo retoma el Data Warehouse visto en la Clase 1, pero ahora con una arquitectura más detallada, mostrando explícitamente las capas por las que pasa el dato desde que ingresa hasta que llega a los consumidores finales: **Raw Data Layer** (datos crudos e inmutables) → **Staging Layer** (datos limpiados y conformados) → **Warehouse Layer** (datos normalizados) → **Analytics Layer** (capa OLAP/semántica) → **Presentation Layer** (data marts y vistas), todo esto rodeado de procesos transversales de seguridad, calidad de datos, metadatos, linaje y monitoreo — una versión más granular de la "capa transversal" mencionada en la Clase 1.

Del lado de la entrada están las **fuentes de datos** (bases de datos operacionales, aplicaciones en la nube, archivos planos y logs, dispositivos IoT, APIs de terceros), y del lado de la salida están los **consumidores de datos**: Business Intelligence, analítica avanzada, machine learning, reporting y analítica de autoservicio. Esto deja explícito que un Data Warehouse bien diseñado no solo alimenta dashboards de BI, sino también modelos de machine learning y análisis avanzado — cerrando el círculo entre los Módulos 3 y 4 de esta misma clase.

### Del data warehouse al lakehouse

Se explica que construir un repositorio analítico implica cuatro etapas generales: **análisis, diseño, implementación y mantenimiento** (estas se detallan en el siguiente slide). Se señala que, en la práctica actual, el Data Warehouse **convive** con Data Lakes y arquitecturas Lakehouse (conceptos ya introducidos en la Clase 1), y que la elección de plataforma depende del **volumen, la latencia y el costo**, pudiendo optarse por infraestructura en la nube, on-premises (dentro de la propia empresa) o una combinación híbrida de ambas.

### Construir el repositorio analítico

Se detallan las cuatro etapas mencionadas arriba, ahora con actividades concretas en cada una:

1. **Análisis:** entrevistar a los stakeholders (interesados del negocio), definir los objetivos y KPIs que se quieren medir, e inventariar las fuentes de datos disponibles evaluando su calidad y formato.
2. **Diseño:** hacer el modelado conceptual, lógico y físico del repositorio; decidir entre arquitectura en estrella o en copo de nieve, sobre plataformas cloud o lakehouse; diseñar los flujos ETL/ELT y la interfaz de reporting.
3. **Implementación:** configurar el entorno tecnológico concreto (se mencionan herramientas reales como BigQuery, Snowflake, Databricks, Redshift o Fabric), desarrollar y validar los flujos de datos, y construir y probar los informes junto a los usuarios finales.
4. **Mantenimiento y optimización:** monitorear el rendimiento y la calidad del sistema en el tiempo, escalar la infraestructura según crece el volumen y la demanda, capacitar a los usuarios y sostener el soporte técnico.

Este flujo de cuatro etapas es, en esencia, un ciclo de vida de proyecto (similar a un ciclo de desarrollo de software), aplicado específicamente a la construcción de un Data Warehouse — algo que en la Clase 1 se mencionaba solo de forma implícita al hablar de la arquitectura, pero que aquí se convierte en una metodología explícita de trabajo.

---

## Modelamiento multidimensional (continuación del Módulo 6)

Esta sección retoma y profundiza el modelo de hechos y dimensiones visto en la Clase 1, ahora con más nivel de detalle técnico.

Se define el modelamiento multidimensional como una **técnica de diseño de data warehouses** que organiza los datos para facilitar el análisis y la consulta eficiente. Organiza los datos en **cubos**, permitiendo verlos desde múltiples perspectivas de negocio (esto es exactamente el cubo OLAP visto en la Clase 1). Se destaca que es esencial en BI porque habilita consultas complejas sobre grandes volúmenes de datos, y que se adapta a las necesidades específicas de cada negocio.

### Elementos del modelo multidimensional

Se detallan seis elementos, algunos ya vistos y otros nuevos respecto a la Clase 1:

- **Cubos de datos:** estructuras que organizan datos en múltiples dimensiones y medidas, permitiendo consultas rápidas.
- **Dimensiones:** las perspectivas de análisis, con sus propios atributos (tiempo, ubicación, producto, cliente).
- **Medidas:** los datos cuantitativos que se analizan (ventas, ingresos, costos, unidades vendidas) — equivalente a lo que la Clase 1 llamaba "métricas numéricas y aditivas" de la tabla de hechos.
- **Jerarquías:** los niveles de detalle dentro de una misma dimensión (por ejemplo, año > trimestre > mes > día). Este concepto es clave porque es justamente lo que permite hacer roll-up y drill-down en un cubo OLAP.
- **Tablas de hechos:** contienen las medidas junto con las claves foráneas hacia las dimensiones (por ejemplo, ventas diarias, órdenes).
- **Dimensiones conformadas:** un concepto nuevo respecto a la Clase 1 — son dimensiones que se usan de forma **consistente entre distintos cubos**, permitiendo un análisis coherente entre distintas áreas de la organización. Esto es, en el fondo, otra forma de asegurar la "única versión de la verdad": si el Data Mart de Ventas y el de Finanzas usan la misma dimensión "Cliente" (con las mismas definiciones), sus análisis serán comparables entre sí.

### Esquemas de modelado

Se presentan tres tipos de esquema para organizar un modelo dimensional, ampliando lo visto en la Clase 1 (que solo mencionaba el esquema en estrella):

- **Estrella:** una tabla de hechos central rodeada de dimensiones sin normalizar. Es simple y eficiente para hacer consultas, aunque implica cierta redundancia de datos.
- **Copo de nieve:** las dimensiones se normalizan en varios niveles (por ejemplo, la dimensión Producto se separa en Producto → Categoría → Familia, en tablas distintas). Esto reduce la redundancia de datos, pero aumenta la complejidad de las consultas, porque hay que hacer más uniones (joins) entre tablas.
- **Galaxia (o constelación de hechos):** varios esquemas en estrella que comparten dimensiones conformadas entre sí. Es el esquema típico de un Data Warehouse corporativo completo, donde conviven varios procesos de negocio (ventas, inventario, finanzas) que comparten ciertas dimensiones comunes (como Tiempo o Cliente).

### Pasos del modelado multidimensional

Se detalla un proceso de cinco pasos para construir un modelo multidimensional concreto:

1. **Definir requisitos:** qué información importa, cómo se va a analizar, y qué KPIs y métricas deben calcularse.
2. **Diseñar el esquema:** elegir entre estrella, copo de nieve o galaxia, según las necesidades de rendimiento y normalización del proyecto.
3. **Dimensiones y medidas:** definir formalmente las dimensiones, sus atributos y jerarquías, y establecer cuáles son las métricas clave y la tabla de hechos.
4. **Implementar y validar:** desplegar el cubo o modelo semántico, configurar la carga ETL/ELT correspondiente, y verificar que los resultados sean correctos.
5. **Documentar y capacitar:** registrar las decisiones de diseño tomadas (para que queden como referencia futura) y enseñar a los usuarios a usar el modelo y las herramientas de BI asociadas.

Este flujo de cinco pasos es una versión más específica del "Diseño" y la "Implementación" mencionados en el proceso general de construcción del repositorio analítico visto un poco antes — aquí aplicado exclusivamente a la parte de modelado dimensional.

---

## Problemáticas de la extracción automática de conocimiento

Este bloque cierra el contenido técnico de la clase retomando, de forma más específica y aplicada a machine learning, los desafíos que ya se habían mencionado en el Módulo 2 para el análisis inteligente de datos en general. Aquí se presentan seis problemáticas concretas del proceso de extraer conocimiento automáticamente (es decir, de todo lo visto en minería de datos, ML y KDD):

- **Calidad de los datos:** datos incompletos o erróneos degradan el conocimiento extraído. Solución: limpieza, validación y observabilidad de los datos.
- **Volumen y complejidad:** una alta dimensionalidad (muchas variables) dificulta el análisis. Solución: reducción de dimensionalidad y procesamiento distribuido.
- **Overfitting y underfitting:** dos problemas opuestos de los modelos — el *overfitting* ocurre cuando el modelo se ajusta demasiado a los datos de entrenamiento y no generaliza bien a datos nuevos; el *underfitting* ocurre cuando el modelo es demasiado simple y no logra capturar los patrones reales. Solución: validación cruzada y ajuste de hiperparámetros.
- **Interpretabilidad:** los modelos complejos (como redes neuronales profundas) son difíciles de explicar. Solución: IA explicable (XAI) y uso de modelos más interpretables cuando sea posible.
- **Privacidad y sesgo:** existen riesgos legales asociados al manejo de datos sensibles, y los sesgos presentes en los datos pueden verse **amplificados** por el modelo entrenado sobre ellos. Solución: anonimización y auditoría tanto de los datos como de los modelos.
- **Escalabilidad:** procesar grandes volúmenes de datos de forma eficiente. Solución: arquitecturas escalables y procesamiento distribuido.

Nótese que estas problemáticas son, en gran parte, una versión ampliada de los "Desafíos y consideraciones" vistos en el Módulo 2, pero con dos elementos nuevos y específicos de machine learning: **overfitting/underfitting** (un problema técnico propio del entrenamiento de modelos) y la idea de que el **sesgo puede amplificarse** (no solo existir) cuando un modelo aprende de datos sesgados.

---

## Cierre y síntesis

La clase cierra con una síntesis que conecta todos los módulos en una sola frase-resumen: **"De los datos a la decisión: capturar y gobernar el dato, modelarlo para el análisis, aplicar técnicas inteligentes y comunicar el conocimiento para decidir mejor."**

Esta frase final resume la estructura completa de la clase:
- **Capturar y gobernar el dato** → Módulo 1 (DSS y ciclo de vida de los datos) y Módulo 6 (arquitectura del Data Warehouse).
- **Modelarlo para el análisis** → modelamiento multidimensional (cubos, dimensiones, esquemas estrella/copo de nieve/galaxia).
- **Aplicar técnicas inteligentes** → Módulo 2 (análisis inteligente de datos) y Módulo 4 (machine learning y minería de datos).
- **Comunicar el conocimiento para decidir mejor** → Módulo 3 (Business Intelligence, reporting, dashboards).

En conjunto, esta segunda clase amplía el mapa conceptual entregado en la Clase 1: si la primera clase explicó **la arquitectura de una solución BI** (de las fuentes al dashboard), esta segunda clase explica **el marco conceptual más amplio en el que BI existe** — mostrando que BI convive con, y se apoya en, los DSS, el análisis inteligente de datos, el machine learning y la minería de datos, todos unidos por un mismo propósito: convertir datos en mejores decisiones.
