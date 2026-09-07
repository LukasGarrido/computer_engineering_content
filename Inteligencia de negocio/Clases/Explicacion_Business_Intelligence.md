# Business Intelligence — Explicación de los contenidos de la clase

Este documento explica, sección por sección, los conceptos que aparecen en la presentación "Business Intelligence" de la asignatura de Ingeniería Civil Informática. La idea es entender **por qué** se presenta cada contenido y **cómo se conecta** con el resto del curso, no solo enumerar qué dice cada diapositiva.

---

## 1. Los tres casos iniciales: Amazon, Mercado Libre y Coca-Cola

La clase parte con tres ejemplos de empresas reales antes de dar ninguna definición formal. Esto es intencional: en vez de partir de la teoría, se muestra primero *cómo se ve BI en la práctica*, para que el concepto abstracto que viene después tenga sentido.

Los tres casos se presentan siguiendo la misma estructura de tres preguntas:
- **Qué decide** la empresa (la decisión de negocio concreta).
- **Qué datos usa** para tomar esa decisión.
- **Cómo decide** (con qué mecanismo o tecnología convierte esos datos en la decisión).

**Amazon** ilustra un caso de decisiones en tiempo real orientadas al cliente: qué producto mostrar, a qué precio y desde qué bodega despacharlo, usando datos de comportamiento (búsquedas, clics, historial) y logísticos. La idea clave que deja este ejemplo es que la decisión "se corrige todos los días": no es un análisis que se hace una vez, sino un proceso continuo.

**Mercado Libre** ilustra un caso de **confianza automatizada**: un marketplace no puede verificar manualmente a cada vendedor o comprador, así que usa datos (reputación, reclamos, historial de pagos) para decidir en quién confiar y a quién ofrecer crédito. El mensaje es que la confianza, en estos modelos de negocio, se sostiene con datos y no con percepciones subjetivas.

**Coca-Cola** ilustra un caso distinto: una empresa que **no vende directamente al consumidor final**, sino a través de embotelladores y distribuidores. Por eso su desafío de BI no es solo analizar sus propios datos, sino **integrar datos de terceros** (sus socios) para poder decidir cuánto producir y dónde distribuir. Este ejemplo es el puente hacia la definición formal, porque cierra con la frase: "Eso es Business Intelligence: convertir datos dispersos en una decisión mejor."

En conjunto, los tres casos muestran que BI no es una sola tecnología, sino un patrón que se repite en industrias distintas: capturar datos de distintas fuentes y convertirlos en una decisión de negocio.

---

## 2. Definición de Business Intelligence

Se presentan dos definiciones complementarias:

- La **definición de Gartner** (la referencia estándar de la industria), que describe BI como un conjunto de metodologías, procesos, arquitecturas y tecnologías que transforman datos operacionales en información significativa y accionable, para habilitar decisiones en distintos niveles (estratégico, táctico y operativo). Esta definición es amplia a propósito: deja claro que BI no es "una herramienta" sino un ecosistema de procesos y tecnologías.

- La **definición práctica**, más simple: BI consiste en capturar, organizar, analizar y convertir datos en decisiones concretas. La frase que resume la utilidad de esto es clave: BI busca que haya "menos discusión sobre qué número es correcto y más tiempo dedicado a decidir qué hacer con él". Es decir, el valor de BI no está en tener más datos, sino en reducir el tiempo perdido discutiendo si los datos son confiables.

Esto se resume en el flujo **Capturar → Organizar → Analizar → Decidir**, que es la lógica que atraviesa toda la presentación y que se retomará más adelante como el "ciclo de vida del dato".

---

## 3. Por qué surge Business Intelligence

Esta sección explica el **origen histórico y organizacional** del problema que BI viene a resolver. Antes de que existieran soluciones de BI, las empresas enfrentaban problemas típicos de crecimiento desordenado de sus sistemas de información:

- Información duplicada en distintos sistemas.
- Múltiples bases de datos que no se comunican entre sí.
- Datos inconsistentes entre áreas (por ejemplo, ventas y finanzas calculan las cosas de forma distinta).
- Reportes diferentes para un mismo indicador.
- Decisiones lentas porque nadie tiene la información a tiempo.
- Uso excesivo de planillas Excel manuales, que son propensas a errores y no están centralizadas.

El punto importante que se destaca es el **síntoma más común**: cada área termina construyendo su propia versión de los números, y nadie sabe cuál es la correcta. La clase deja explícito que el problema de fondo **no es tecnológico**, sino de **pérdida de confianza en la información**. Esto prepara el terreno para el siguiente slide, que muestra un ejemplo concreto de este problema.

---

## 4. El ejemplo de "¿cuál es la cifra correcta?"

Este slide es una ilustración directa del problema anterior: tres áreas distintas (Ventas, Finanzas y Gerencia) informan tres cifras de venta diferentes para lo que debería ser el mismo número. Esto no es un error aislado, sino el resultado natural de tener sistemas y definiciones desconectadas.

De aquí se introduce uno de los conceptos más importantes de BI: el de **Single Source of Truth** (única versión de la verdad). La idea es que, sin importar quién consulte el dato o desde qué área, debería obtenerse siempre el mismo número, porque hay una sola fuente autorizada y consistente. Este concepto es la motivación central detrás de construir un Data Warehouse, que se explica más adelante.

---

## 5. Objetivos de Business Intelligence

Aquí se listan los fines prácticos para los que se implementa una solución de BI: apoyar decisiones, detectar oportunidades, reducir riesgos, automatizar reportes, descubrir patrones, pronosticar ventas y medir indicadores.

Lo importante de este slide no es memorizar la lista, sino entender la frase de cierre: **todos estos objetivos convergen en un mismo fin, que es decidir mejor y más rápido**. Es decir, cada objetivo individual (automatizar un reporte, detectar un patrón) es un medio, no un fin en sí mismo; el fin siempre es mejorar la calidad y velocidad de la toma de decisiones.

---

## 6. Niveles de decisión en la organización

Esta sección explica que una misma solución de BI debe servir a **tres niveles distintos** dentro de una organización, cada uno con necesidades de información diferentes:

- **Nivel estratégico** (alta gerencia): necesita visión de largo plazo, tendencias y proyecciones. Piensa en años.
- **Nivel táctico** (jefaturas y supervisores): necesita seguimiento mensual, comparaciones y desviaciones respecto a metas. Piensa en meses.
- **Nivel operacional** (usuarios del negocio): necesita el detalle diario, las transacciones y el control de gestión inmediato. Piensa en días.

La idea central es que **el mismo dato de base** (por ejemplo, ventas) debe poder consumirse con distinto nivel de detalle según quién lo use: un gerente no necesita ver cada transacción individual, pero un supervisor de sucursal sí. Este es un principio de diseño importante que después se conecta con los cubos OLAP (que permiten "subir" o "bajar" el nivel de detalle sobre el mismo dato).

---

## 7. Evolución hacia la Inteligencia de Negocios (línea de tiempo)

Esta línea de tiempo explica **cómo se llegó** a lo que hoy entendemos como BI, mostrando que no es una tecnología que apareció de la nada, sino la evolución de varias generaciones de sistemas:

- **1960s – TPS (Sistemas Transaccionales):** sistemas de mainframe que simplemente registran las operaciones diarias (por ejemplo, una venta o un pago). Son el punto de partida: generan el dato crudo.
- **1970s – MIS (Sistemas de Información de Gestión):** con la llegada de las bases de datos relacionales, se empiezan a generar reportes periódicos para las jefaturas, en base a esos datos transaccionales.
- **1980s – DSS (Sistemas de Apoyo a Decisiones):** aparecen modelos y planillas de simulación, del tipo "qué pasaría si", que permiten explorar escenarios en vez de solo mirar el pasado.
- **1985-1990 – EIS (Sistemas de Información Ejecutiva):** se crean tableros con indicadores clave pensados específicamente para la alta dirección, un antecedente directo de los dashboards actuales.
- **1990s – Business Intelligence propiamente tal:** aparece el concepto de Data Warehouse, los procesos ETL y las tecnologías OLAP, con el objetivo explícito de lograr una sola versión de la verdad, mediante informes y dashboards.
- **2000s – Big Data:** con tecnologías como Hadoop, NoSQL y la nube, el foco se traslada al volumen, la velocidad y la variedad de datos, incluyendo datos no estructurados que antes no se podían aprovechar.
- **2010s – Machine Learning:** el análisis deja de ser solo descriptivo (qué pasó) y pasa a ser predictivo, con modelos que anticipan el futuro en vez de solo reportar el pasado.
- **2020s – Inteligencia Artificial:** con IA generativa y analítica aumentada, se llega a consultas en lenguaje natural y decisiones en tiempo real.

El mensaje de fondo es que **cada etapa no reemplaza a la anterior, sino que amplía la capacidad de convertir datos en decisiones**. Un Data Warehouse sigue siendo relevante hoy aunque exista Big Data e IA, porque resuelven problemas distintos.

---

## 8. Arquitectura de referencia de una solución BI

A partir de aquí, la presentación entra en la **Parte II: componentes principales de una solución BI**, que es el núcleo técnico del curso. Se presenta una arquitectura de referencia compuesta por cinco capas, organizadas como un flujo unidireccional:

1. **Fuentes:** de dónde vienen los datos (OLTP, ERP/CRM, APIs, logs, IoT).
2. **Integración:** dónde se extraen, limpian, transforman y cargan los datos.
3. **Almacenamiento:** dónde se guardan de forma organizada (staging, Data Warehouse, data marts, ODS).
4. **Análisis:** dónde se procesan analíticamente (motores OLAP, cubos, capa semántica).
5. **Explotación:** dónde se consumen (tableros, informes, self-service).

Todas estas capas están atravesadas por una **capa transversal** de metadatos, catálogo de datos, seguridad, linaje, orquestación y monitoreo — es decir, elementos de gobierno que no pertenecen a una sola etapa, sino que aplican a todas.

Dos ideas clave de este slide:
- El flujo es **unidireccional**: cada capa existe justamente para **desacoplar** la operación transaccional del día a día del análisis histórico, de modo que analizar datos no afecte el rendimiento de los sistemas que operan el negocio.
- La **integración es el punto crítico**: se indica explícitamente que concentra entre el 60% y el 80% del esfuerzo de un proyecto BI. Esto justifica por qué el resto de la clase le dedica tanto espacio al ETL/ELT.

---

## 9. Fuentes de datos

Se detallan los tipos de fuentes que alimentan un sistema BI: sistemas de negocio (ERP, CRM, POS, RRHH), datos operativos (sensores IoT, APIs, archivos CSV/Excel), bases de datos (SQL, Oracle, PostgreSQL, MongoDB) y canales digitales (redes sociales, web, e-commerce).

La conclusión de este slide es simple pero importante: **mientras más diversas son las fuentes, más crítico se vuelve el proceso de integración**. No es lo mismo integrar dos bases de datos con la misma estructura que integrar un ERP, una API externa y archivos Excel con formatos distintos.

---

## 10. ETL: Extract, Transform, Load

Se explica el proceso clásico de integración de datos, compuesto por tres etapas:

- **Extract (Extraer):** obtener los datos desde las fuentes originales.
- **Transform (Transformar):** limpiar y preparar los datos — eliminar duplicados, homologar nombres y códigos, corregir errores de captura, convertir monedas y unidades, integrar múltiples sistemas.
- **Load (Cargar):** llevar los datos ya transformados al repositorio de destino (típicamente el Data Warehouse).

La idea central que se enfatiza es que el ETL es la **etapa crítica** de todo el proyecto, y se usa una frase muy directa para explicarlo: "un dashboard elegante construido sobre datos sucios entrega decisiones equivocadas con apariencia de rigor". Es decir, no importa cuán bien se vea el resultado final si los datos de base están mal limpiados: el problema no se nota a simple vista, pero la decisión que se tome será errónea.

---

## 11. ELT: el enfoque moderno

Se presenta una variante del proceso anterior, que invierte el orden: **Extract → Load → Transform**. En este enfoque, los datos se cargan primero sin transformar, y la transformación ocurre **dentro** del Data Warehouse (o del sistema de destino), aprovechando su capacidad de cómputo.

Ventajas que se mencionan: escala mejor con grandes volúmenes de datos y aprovecha el poder de cómputo de la nube.

La comparación final resume la diferencia de uso: **ETL** funciona bien con volúmenes acotados porque transforma antes de cargar; **ELT** es el estándar en arquitecturas cloud porque carga primero y transforma después, aprovechando la capacidad de procesamiento masivo de las plataformas modernas.

---

## 12. Calidad de datos y gobierno

Esta sección profundiza en **qué significa que un dato sea de calidad**, definiendo seis dimensiones concretas:

- **Exactitud:** el valor refleja fielmente la realidad que representa.
- **Completitud:** no hay valores nulos en atributos que son obligatorios.
- **Consistencia:** no hay contradicciones entre sistemas ni entre distintos períodos de tiempo.
- **Oportunidad:** el dato está disponible dentro de la ventana de tiempo en que se necesita para decidir.
- **Unicidad:** cada entidad real está representada por un solo registro, sin duplicados.
- **Validez:** el dato cumple con los dominios, formatos y reglas de negocio definidos.

Además, se introduce el concepto de **gobierno de datos**, que no es solo un tema técnico sino organizacional:
- Debe existir una **propiedad y custodia explícitas**: el *data owner* es responsable del dato (a nivel de negocio), mientras que el *data steward* es responsable de su calidad en el día a día (a nivel operativo).
- La **gestión de datos maestros (MDM)** busca que exista un identificador único para entidades clave como cliente, producto o proveedor, válido para toda la organización, evitando que cada sistema tenga su propia versión de esa entidad.
- El **linaje y los metadatos** permiten trazar el camino desde el dato de origen hasta el indicador final, lo cual es indispensable para auditorías y para entender el impacto de un cambio en los datos.

El mensaje implícito de esta sección es que la calidad de datos **no se soluciona automáticamente con tecnología**; requiere procesos y responsabilidades claras dentro de la organización.

---

## 13. Data Warehouse

Se define el Data Warehouse (DW) como el **repositorio corporativo** central de una solución BI, y se explican sus cinco propiedades clásicas (definición de Bill Inmon):

- **Variante en el tiempo:** conserva la historia; cada registro es válido dentro de un horizonte temporal específico (no se sobrescribe sin dejar rastro).
- **Integrado:** usa nomenclatura, unidades y codificación homogéneas entre las distintas fuentes que lo alimentan.
- **Consistente:** tiene definiciones únicas y homologadas para toda la organización (esto conecta directamente con el problema de "las múltiples verdades" visto antes).
- **No volátil:** se carga y se consulta, pero no se actualiza de forma transaccional como una base de datos operativa.
- **Temático:** está organizado por asunto de negocio (ventas, clientes, productos), no por la aplicación de la que provienen los datos.

Se menciona un modelo integrado de ejemplo con dimensiones comunes: Ventas, Clientes, Productos, Tiempo, Sucursales, Empleados — todas las áreas de la organización comparten estas mismas dimensiones y definiciones, lo cual es justamente lo que permite tener una única versión de la verdad.

---

## 14. Modelado dimensional: hechos y dimensiones

Aquí se introduce el **modelo de datos** que se usa típicamente dentro de un Data Warehouse para hacer análisis: el **esquema en estrella**, formado por una tabla de hechos rodeada de tablas de dimensiones.

- La **tabla de hechos** contiene las métricas numéricas y aditivas del negocio (por ejemplo: unidades vendidas, monto neto, descuento) junto con las claves foráneas que la conectan a las dimensiones. Se destaca que declarar la **granularidad** —es decir, qué representa exactamente cada fila de la tabla de hechos (por ejemplo, "una línea de boleta")— es la **decisión de diseño más determinante** de todo el modelo, porque condiciona qué preguntas se podrán responder después.
- Las **dimensiones** (Tiempo, Producto, Cliente, Tienda en el ejemplo) son los atributos descriptivos que dan contexto al hecho: son los ejes por los cuales se puede filtrar, agrupar y crear jerarquías de análisis.

Este modelo es el que hace posible que, más adelante, se pueda "cortar" la información de tantas formas distintas mediante los cubos OLAP.

---

## 15. Data Mart

Se define el Data Mart como un **subconjunto** del Data Warehouse, enfocado en un área específica del negocio (por ejemplo: Data Mart Comercial, Data Mart Finanzas, Data Mart RRHH). La idea es que cada área acceda solo a la porción de información que necesita, sin tener que navegar todo el repositorio corporativo completo.

Se hace una advertencia importante: **un Data Mart mal gobernado vuelve a crear silos** de información, el mismo problema que BI busca resolver. Por eso, un Data Mart siempre debe **derivar del Data Warehouse** (y no construirse de forma independiente), para no perder la consistencia y la única versión de la verdad.

---

## 16. Cubos OLAP y sus operaciones

Se presenta el concepto de **cubo OLAP** (Online Analytical Processing), que organiza las medidas del negocio (por ejemplo, ventas) a lo largo de varios ejes dimensionales (ciudad, vendedor, producto, fecha, cliente). Cada celda del cubo representa una agregación, ya sea precalculada o resuelta al momento de la consulta.

Se explican cinco (y en el segundo slide, seis) operaciones que se pueden hacer sobre un cubo:

- **Roll-up:** agrega subiendo por una jerarquía (por ejemplo, de día a mes, o de comuna a región).
- **Drill-down:** lo contrario — desagrega hacia el detalle, útil para explicar por qué ocurrió una desviación observada en un número agregado.
- **Slice:** fija el valor de una dimensión y obtiene un subcubo más pequeño (por ejemplo, "solo el mes de marzo").
- **Dice:** restringe varias dimensiones simultáneamente mediante rangos de valores (por ejemplo, "marzo a mayo, solo región Metropolitana").
- **Pivot:** rota los ejes para presentar las mismas medidas desde otra perspectiva (cambiar qué dimensión va en filas y cuál en columnas).
- **Drill-through:** baja hasta la transacción original en el sistema operacional, es decir, atraviesa todas las capas de agregación hasta llegar al dato crudo.

Estas operaciones son justamente lo que permite que la **misma** solución BI sirva a los tres niveles de decisión vistos antes (estratégico, táctico, operacional): un gerente puede quedarse en el nivel agregado (roll-up), mientras que un analista puede hacer drill-down hasta el detalle.

---

## 17. Implementaciones OLAP y rendimiento

Se comparan tres formas de implementar tecnológicamente un motor OLAP:

- **ROLAP** (Relational OLAP): almacena los datos en tablas relacionales del Data Warehouse. Tiene alta escalabilidad (limitada por el motor SQL), pero el tiempo de respuesta es variable, dependiendo de índices y agregados.
- **MOLAP** (Multidimensional OLAP): usa estructuras multidimensionales propietarias. Es muy rápido sobre agregados precalculados, pero escala peor porque el cubo puede crecer de forma explosiva en tamaño.
- **HOLAP** (Hybrid OLAP): combina ambos enfoques — detalle en formato relacional, agregados en formato multidimensional — logrando un equilibrio entre escalabilidad y velocidad.

También se mencionan técnicas de optimización que se usan en la práctica: **índices y particionado** (por ejemplo, índices bitmap para columnas de baja cardinalidad, o particiones por fecha para reducir el volumen escaneado en cada consulta), **vistas materializadas** (agregados ya calculados y guardados, que se reutilizan automáticamente cuando conviene), y **almacenamiento columnar**, que se señala como el estándar analítico actual porque permite comprimir por columna y leer solo las columnas necesarias para una consulta.

---

## 18. Ecosistema de repositorios analíticos

Se amplía el panorama más allá del Data Warehouse clásico, presentando otros tipos de repositorios que coexisten en arquitecturas modernas:

- **Data Mart:** ya explicado — subconjunto departamental del DW.
- **ODS (Operational Data Store):** almacén operacional de baja latencia, con datos casi en tiempo real, pero con historia mínima (no está pensado para guardar años de datos, sino para tener el estado más actual posible).
- **Data Lake:** repositorio donde el dato se guarda **crudo**, en su formato nativo, y el esquema se aplica recién en el momento de la lectura (a diferencia del DW, donde el esquema se define antes de cargar).
- **Lakehouse:** un enfoque más reciente que combina ambos mundos, usando formatos de tabla abiertos que aportan transacciones y esquema sobre el lago de datos, buscando la flexibilidad del lago con parte de la disciplina del warehouse.

Se entregan criterios para decidir qué arquitectura usar en cada caso:
- **Naturaleza del dato:** si el esquema es estable y el uso es recurrente, el modelo dimensional (DW) sigue siendo superior.
- **Latencia exigida:** cargas por lotes nocturnas versus micro-lotes o streaming en ventanas de minutos.
- **Perfil de consumo:** consultas gobernadas y repetibles (típico de negocio) versus exploración abierta de científicos de datos.
- **Costo total:** el lago abarata el almacenamiento, pero traslada ese ahorro a un mayor costo en gobernanza y en cómputo de consulta.

La idea de fondo es que **no existe una única arquitectura correcta**: la elección depende del tipo de dato, la urgencia de la decisión y quién va a consumir la información.

---

## 19. Dashboards y KPIs

Se llega a la **capa visible** de todo el proceso: la que efectivamente ve el negocio. Un dashboard integra KPIs e indicadores en un solo lugar, con alertas y semáforos de gestión, gráficos comparativos y de tendencia, y en algunos casos mapas o análisis geográfico.

Se listan ejemplos de KPIs típicos: Ventas, Margen, Rentabilidad, Tiempo promedio, NPS, Rotación, Inventario.

La frase clave de este slide es: **"un dashboard no es el proyecto: es su resultado visible"**. Esto refuerza toda la lógica de la arquitectura vista antes — el dashboard es solo la última capa (explotación) de un proceso mucho más largo que incluye fuentes, integración, almacenamiento y análisis. Un error común es pensar que "hacer BI" es simplemente construir un dashboard bonito, cuando en realidad ese dashboard depende de todo lo anterior para ser confiable.

---

## 20. Capa de explotación: del indicador al tablero

Este slide profundiza en tres elementos de la capa de explotación:

- **Indicadores (KPI):** se define formalmente que un KPI es una métrica ligada a un objetivo, con fórmula, dueño, meta y frecuencia definidos. Se enfatiza que **"sin meta no hay indicador, sólo una cifra"** — es decir, un número por sí solo no es un KPI si no está comparado contra un objetivo.
- **Capa semántica:** traduce las tablas físicas de la base de datos a conceptos de negocio comprensibles, y centraliza la definición de las métricas para toda la organización (esto es otra forma de asegurar la única versión de la verdad, ahora a nivel de "cómo se define cada métrica", no solo de "dónde vive el dato").
- **Tableros y reportes:** se distingue entre un **tablero**, pensado para el monitoreo continuo, y un **informe**, pensado para un análisis puntual. Cada objeto debe responder a una pregunta explícita del negocio.

Se agregan buenas prácticas de visualización: elegir el tipo de gráfico según la tarea (comparación, composición, distribución o evolución), maximizar la razón dato-tinta (evitar rejillas, sombras o efectos decorativos que no aportan información), mantener una jerarquía visual explícita (lo primero que se ve debe ser lo más importante para decidir), y siempre dar contexto: toda cifra debe mostrarse junto a su meta y su variación.

---

## 21. Arquitectura completa (caso integrado)

Este slide condensa todo lo anterior en un solo flujo de extremo a extremo, usando un ejemplo concreto:

Fuentes (ERP, CRM, Excel, IoT, RRSS, API) → ETL → Data Warehouse → Data Mart → Modelo Estrella → Power BI → Dashboard → Gerencia.

La frase de cierre resume la idea central de toda la unidad: **"el valor no está en ninguna capa aislada, sino en que todas conversen entre sí"**. Ninguna de las capas vistas (fuentes, integración, almacenamiento, análisis, explotación) genera valor por sí sola; el valor aparece cuando el flujo completo funciona de forma coherente.

---

## 22. Tipos de datos que alimentan BI

Se clasifican los datos en tres categorías:

- **Estructurados:** datos con un esquema fijo y predecible, típicamente en bases de datos relacionales (SQL Server, Oracle, PostgreSQL, MySQL).
- **Semiestructurados:** tienen cierta organización, pero no un esquema rígido de tabla (JSON, XML, CSV, logs).
- **No estructurados:** no tienen una estructura predefinida (videos, audios, correos, PDF, imágenes, redes sociales).

El punto que se destaca es que **hoy la mayor parte del dato disponible en una empresa no está estructurado**, lo cual es relevante porque las técnicas clásicas de BI (Data Warehouse, modelo dimensional) fueron pensadas originalmente para datos estructurados, y por eso han tenido que evolucionar (Data Lake, Big Data) para poder aprovechar también estos otros tipos de datos.

---

## 23. El ciclo de vida del dato (jerarquía DIKW)

Se presenta la jerarquía **DIKW** (Data, Information, Knowledge, Wisdom, adaptada aquí como seis etapas): **Dato → Información → Conocimiento → Decisión → Acción → Valor**.

La explicación clave es que **cada capa reduce el volumen de datos pero aumenta su valor**: un dato crudo por sí solo vale poco, pero al procesarlo, contextualizarlo, analizarlo y finalmente actuar sobre él, se genera valor real para el negocio. La **acción** es la que cierra el ciclo — es decir, todo el proceso de BI no tiene sentido si no termina finalmente en una acción concreta sobre el negocio.

Esto conecta directamente con la definición práctica de BI vista al inicio (Capturar → Organizar → Analizar → Decidir): es esencialmente la misma idea, expresada con distinto nivel de detalle.

---

## 24. Actividad: la veterinaria "Patitas"

Esta es una actividad práctica en la que se entrega una planilla de datos desordenados de una clínica veterinaria (con visitas, propietarios, mascotas, veterinarios y diagnósticos mezclados en una sola tabla), y se pide resolverla en dos pasos:

**Paso 1 — Modelo relacional:** identificar las distintas entidades que están mezcladas en la planilla (por ejemplo: propietarios, mascotas, veterinarios, visitas), definir una clave primaria para cada una, conectar las tablas entre sí y eliminar los datos repetidos. Esto pone en práctica el concepto de **normalización**: cada entidad debe vivir en su propia tabla, y cada dato debe registrarse una sola vez.

**Paso 2 — Modelo estrella:** a partir del modelo relacional ya limpio, se pide transformar los datos a un modelo dimensional: elegir el hecho a medir (por ejemplo, cada visita o atención), definir las métricas (qué se suma, cuenta o promedia), definir las dimensiones (por qué criterios se querrá filtrar y agrupar) y formular preguntas de negocio que el modelo debería poder responder sin volver a mirar la planilla original.

Esta actividad hace tangible, con un caso pequeño, todo lo que se explicó de forma teórica en las secciones de modelado dimensional (hechos, dimensiones, granularidad) y calidad de datos.

---

## 25. Ejemplo empresarial: cadena de retail

Se muestra un ejemplo más del mundo real, mapeando cada sistema operacional de una cadena de retail con el tipo de información que produce: POS → Ventas, ERP → Inventario, CRM → Clientes, E-commerce → Google Analytics, Facebook Ads → Excel, y todo esto convergiendo finalmente en Power BI para la Gerencia. Es una forma simple de mostrar cómo la arquitectura teórica vista antes se traduce a herramientas concretas que existen en una empresa real.

---

## 26. Caso de estudio: cadena de supermercados

Se plantea un problema abierto: las ventas están disminuyendo, y se pregunta qué información necesitaría la gerencia para entender por qué. Se listan posibles necesidades de información (ventas por sucursal, por producto, por hora, productos más vendidos, clientes frecuentes, rentabilidad, stock, promociones) y se pregunta en qué sistemas existiría cada uno de esos datos (ERP, CRM, POS, Inventario, RRHH, Excel, Web).

Este caso funciona como puente hacia la actividad final, practicando el ejercicio de "traducir" una pregunta de negocio en necesidades de datos concretas y sus fuentes.

---

## 27. Actividad en equipos

Actividad de cierre de la clase: cada equipo elige una empresa de una lista (Banco, Clínica, Universidad, Retail, Aerolínea, Minera) y debe responder cuatro preguntas: qué decisiones toma diariamente, qué datos necesita y dónde se generan, qué indicadores mediría, y cómo sería su arquitectura BI y qué áreas consumirían la información.

Esta actividad es, en esencia, una repetición del ejercicio con el que empezó la clase (los casos de Amazon, Mercado Libre y Coca-Cola), pero ahora hecha por los propios estudiantes, para consolidar que puedan aplicar el marco de análisis (qué decide / qué datos usa / cómo decide) a cualquier industria.

---

## 28. Conclusiones

Se cierra la clase reforzando la idea central: **Business Intelligence no consiste únicamente en crear dashboards**. Es una disciplina que integra tecnologías, procesos, personas y metodologías para transformar datos dispersos en información confiable que apoye decisiones estratégicas. Una solución BI completa requiere una arquitectura que abarca desde las fuentes de datos y los procesos ETL/ELT hasta los modelos analíticos y la visualización final.

La fórmula resumen que se entrega es: **Tecnologías + procesos + personas = información confiable para decidir.**

---

## 29. Ideas para llevarse de la sesión

Se entregan cuatro ideas de síntesis, que funcionan como los puntos más importantes de toda la clase:

1. **BI es una arquitectura, no una herramienta:** el tablero es solo la punta visible de una cadena que incluye integración, modelado y gobierno de datos.
2. **La granularidad define el modelo:** declarar qué representa cada fila de la tabla de hechos condiciona todas las decisiones de diseño posteriores.
3. **La calidad se diseña, no se corrige:** los controles de calidad deben estar en el flujo de integración (ETL/ELT), no aplicarse recién al final sobre el informe.
4. **La latencia se ajusta a la decisión:** no existe una arquitectura óptima universal — depende de qué tan rápido se necesita la información para poder actuar sobre ella.

---

## 30. Próximas unidades del curso

Se cierra indicando que esta primera clase estableció la base conceptual, y que las siguientes unidades profundizarán en los temas técnicos que aquí solo se introdujeron: **Modelamiento dimensional, Procesos ETL, Data Warehouse, Power BI, Minería de datos y Analítica avanzada**.
