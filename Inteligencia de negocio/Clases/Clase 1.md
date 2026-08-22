## Business Intelligence

### 1. Los casos iniciales (Amazon, Mercado Libre, Coca-Cola)

El documento no empieza con teoría, sino con ejemplos, porque quiere que entiendas BI desde la práctica antes de definirlo. La estructura de análisis que usa para cada empresa —**qué decide / qué datos usa / cómo decide**— es en realidad una plantilla mental que sirve para diagnosticar _cualquier_ organización, y de hecho la vuelves a usar tú mismo en la actividad final del curso.

- **Amazon** ilustra el caso más "puro": una empresa digital donde cada clic literalmente genera un dato que retroalimenta la siguiente decisión (qué mostrar, a qué precio). Es un ciclo casi instantáneo entre dato y decisión.
- **Mercado Libre** agrega un matiz importante: BI no solo sirve para optimizar ventas, sino para gestionar **confianza y riesgo** (reputación de vendedores, antifraude, crédito). Esto muestra que BI aplica a decisiones muy distintas entre sí, no solo comerciales.
- **Coca-Cola** es el caso más interesante conceptualmente porque **no vende directo al consumidor**. Sus datos no nacen en su propia operación, sino en terceros (embotelladores, distribuidores). Esto anticipa un problema central de BI: **integrar datos que vienen de fuera de la organización**, no solo de sistemas internos.

La frase de cierre de esta sección ("BI es convertir datos dispersos en una decisión mejor") es la definición operativa que usarás como hilo conductor de todo el resto del documento.

---

### 2. Definición de Business Intelligence

Se dan dos definiciones complementarias:

- **Gartner** (la definición "oficial", usada en la industria): BI es un **conjunto** de metodologías + procesos + arquitecturas + tecnologías. Es importante notar que la definición NO dice "un software". Esto es deliberado: mucha gente cree que BI = Power BI o Tableau, y el documento corrige eso desde el inicio.
- **Definición práctica**: se resume en cuatro verbos encadenados: **Capturar → Organizar → Analizar → Decidir**. Este flujo de 4 pasos es, en esencia, un resumen simplificado de toda la arquitectura que se explica más adelante (fuentes → integración/almacenamiento → análisis → explotación/decisión). O sea, esta es la "versión chica" del diagrama grande que viene después.

La idea de fondo que quieren que internalices: **el valor de BI no está en tener el dato, sino en que ese dato se traduzca en una acción**. Un dato que nadie usa para decidir no genera valor.

---

### 3. Por qué surge BI (el problema que resuelve)

Esta sección explica el **origen histórico/organizacional** de BI, no como tecnología sino como respuesta a un dolor real:

- **Información duplicada / bases sin integrar**: cada sistema (ventas, finanzas, RRHH) guarda su propia copia de datos similares, sin que se comuniquen entre sí.
- **Datos inconsistentes entre áreas**: como cada área tiene su propia fuente, los números divergen.
- **Reportes distintos para un mismo indicador**: el síntoma más visible de lo anterior.
- **Decisiones lentas**: si nadie confía en los números, las decisiones se demoran porque hay que "verificar" o discutir cuál cifra es la correcta.
- **Exceso de Excel manual**: sin una arquitectura formal, cada analista arma su propia planilla, lo que perpetúa el problema en vez de resolverlo.

El **punto clave conceptual** aquí (y se repite más adelante): _"el costo no es tecnológico, es la pérdida de confianza en la información"_. Esto es importante porque cambia el enfoque: BI no es un problema que se resuelve comprando una herramienta más potente, sino un problema de **gobierno y arquitectura de datos**.

#### El ejemplo de las "tres verdades" ($1.250M vs $1.180M vs $1.310M)

Este ejemplo es la ilustración perfecta del problema anterior: tres áreas, tres cifras distintas, para la _misma_ pregunta ("¿cuánto vendimos?"). Probablemente cada área calcula "ventas" con una definición ligeramente distinta (¿incluye devoluciones? ¿es venta facturada o venta pagada? ¿en qué fecha se contabiliza?). Esto conecta directamente con el concepto de **Single Source of Truth (SSOT)**: la meta de BI es que exista **una sola definición, un solo cálculo, una sola fuente** para cada indicador de negocio, de modo que ya no se discuta _cuál número es el correcto_, sino _qué hacer con él_.

---

### 4. Objetivos de BI

Se listan siete objetivos (apoyar decisiones, detectar oportunidades, reducir riesgos, automatizar reportes, descubrir patrones, pronosticar ventas, medir indicadores). No hay que memorizarlos como lista suelta; lo relevante es que **todos son manifestaciones de una misma cosa**: usar el dato para actuar mejor y más rápido. Algunos son más reactivos (medir indicadores, reducir riesgos) y otros más proactivos/predictivos (pronosticar, detectar oportunidades) — esto anticipa la distinción entre BI "tradicional" (mirar el pasado) y analítica avanzada/ML (anticipar el futuro), que se menciona en la línea de tiempo más adelante.

---

### 5. Niveles de decisión organizacional

Esta es una idea estructuralmente importante: **BI no es "una cosa" que se entrega igual a todos**. Distintos roles necesitan distinto nivel de detalle:

- **Nivel estratégico (alta gerencia):** necesita tendencias y proyecciones de largo plazo. No le sirve ver una transacción individual; necesita el panorama agregado.
- **Nivel táctico (jefaturas/supervisores):** necesita comparaciones y desviaciones mes a mes — un nivel intermedio de agregación, para ajustar operaciones a corto/mediano plazo.
- **Nivel operacional (usuarios del negocio):** necesita el detalle transaccional diario, para ejecutar y controlar el trabajo del día a día.

La frase clave: _"la misma solución BI debe servir a los tres niveles con distinto grado de detalle"_. Esto es un requisito de **diseño**: un buen data warehouse/modelo dimensional debe permitir tanto ver el detalle fino (drill-down) como el agregado (roll-up) — conceptos que se explican formalmente más adelante en la sección de OLAP.

---

### 6. Evolución histórica hacia BI (la línea de tiempo)

Esta línea de tiempo no es solo "cultura general" — te muestra que BI es la **acumulación progresiva de capacidades**, cada una resolviendo la limitación de la anterior:

- **1960s TPS (Transaction Processing Systems):** solo registran operaciones (mainframe, lotes). No hay análisis, solo registro.
- **1970s MIS (Management Information Systems):** ya hay bases de datos relacionales y reportes periódicos — primer paso hacia dar _información_ (no solo datos) a las jefaturas.
- **1980s DSS (Decision Support Systems):** aparece la simulación — "qué pasaría si cambio este parámetro" — un paso hacia el análisis activo, no solo el reporte pasivo.
- **1985-1990 EIS (Executive Information Systems):** tableros de indicadores clave para la alta dirección — el antecedente directo de los dashboards actuales.
- **1990s Business Intelligence propiamente tal:** aparecen el **Data Warehouse**, **ETL** y **OLAP** como conjunto integrado — es aquí donde se formaliza la idea de "una sola versión de la verdad" con informes y dashboards. Este es el núcleo técnico que el resto del documento desarrolla en detalle.
- **2000s Big Data:** cambia la naturaleza del dato (Hadoop, NoSQL, nube) — ahora hay que lidiar con **volumen, velocidad y variedad**, incluyendo datos no estructurados que el modelo relacional tradicional no maneja bien.
- **2010s Machine Learning:** el salto conceptual más importante — se pasa de _describir el pasado_ (reportes) a _predecir el futuro_ (modelos predictivos).
- **2020s IA generativa:** consultas en lenguaje natural sobre los datos, analítica "aumentada", decisiones en tiempo real.

**Idea de fondo:** cada etapa no reemplaza a la anterior, sino que **la arquitectura BI moderna (data warehouse, ETL/ELT, modelado dimensional) sigue siendo la base** sobre la cual se montan Big Data, ML e IA. Por eso el curso dedica tanto tiempo a explicar esa base técnica en la "Parte II".

---

### 7. Arquitectura de referencia de una solución BI (el corazón técnico)

Aquí empieza la parte más técnica y detallada del documento. La arquitectura se presenta como un flujo de capas **unidireccional** (los datos fluyen en una sola dirección, de las fuentes hacia el usuario final):

```
Fuentes → Integración → Almacenamiento → Análisis → Explotación
```

Cada capa **desacopla** la operación transaccional del análisis — es decir, los sistemas operacionales (donde ocurre la venta, la atención al cliente, etc.) quedan separados de los sistemas donde se analiza esa información. Esto es clave: **no se analiza directamente sobre las bases operacionales**, porque consultas analíticas pesadas podrían ralentizar o interferir con la operación diaria del negocio (por ejemplo, que un reporte gerencial lento haga que el sistema de caja de una tienda se congele).

Hay también una **capa transversal** que atraviesa todo el flujo: metadatos, catálogo de datos, seguridad/control de acceso, linaje (trazabilidad del dato) y orquestación/monitoreo. Esta capa no es "una etapa más" sino un conjunto de controles que aplican a _todas_ las etapas simultáneamente.

**El dato más importante de esta sección:** la integración concentra entre el **60% y 80% del esfuerzo** de un proyecto BI. Esto contradice la intuición de que "lo difícil es hacer el dashboard bonito" — en realidad, lo difícil (y lo que determina si el proyecto tiene éxito) es limpiar, unificar y preparar los datos _antes_ de llegar a la visualización.

---

### 8. Los componentes uno por uno

#### 8.1 Fuentes de datos

Son el punto de partida: sistemas de negocio (ERP, CRM, POS, RRHH), datos operativos (IoT, APIs, CSV, Excel), bases de datos (SQL, Oracle, PostgreSQL, MongoDB) y canales digitales (redes sociales, web, e-commerce). La regla enunciada es simple pero importante: **a mayor diversidad de fuentes, mayor complejidad de integración** — cada tipo de fuente tiene su propio formato, frecuencia de actualización y calidad, y todo eso hay que reconciliarlo.

#### 8.2 ETL (Extract, Transform, Load)

Es el proceso clásico donde:

1. **Extract:** se sacan los datos de las fuentes originales.
2. **Transform:** se limpian y transforman _antes_ de cargarlos — se eliminan duplicados, se homologan nombres/códigos (por ejemplo, que "Ana Pérez" y "A. Pérez" se traten como la misma persona), se corrigen errores de captura, se convierten monedas/unidades.
3. **Load:** se cargan ya limpios al destino (típicamente el Data Warehouse).

La frase clave para entender por qué esta etapa es crítica: _"un dashboard elegante construido sobre datos sucios entrega decisiones equivocadas con apariencia de rigor"_. Es decir, un dashboard bonito **no valida** la calidad del dato subyacente — de hecho, puede ser peligroso porque genera una falsa sensación de confiabilidad.

#### 8.3 ELT (el enfoque moderno)

Invierte el orden: **Extract → Load → Transform**. Los datos se cargan primero _sin_ transformar, y la transformación ocurre _dentro_ del Data Warehouse, aprovechando su poder de cómputo (especialmente en la nube). Esto escala mejor con grandes volúmenes de datos porque no hay que esperar a transformar todo antes de cargarlo — se puede paralelizar y aprovechar la infraestructura cloud.

**Cuándo usar cada uno:** ETL funciona bien con volúmenes acotados y es el enfoque "tradicional"; ELT es el estándar en arquitecturas cloud modernas porque desacopla la carga de la transformación y aprovecha mejor recursos elásticos.

#### 8.4 Calidad de datos y gobierno

Se definen seis dimensiones de calidad, cada una respondiendo una pregunta distinta sobre el dato:

- **Exactitud:** ¿el valor refleja la realidad? (¿el precio registrado es el precio real?)
- **Completitud:** ¿faltan datos obligatorios? (¿hay campos nulos que no deberían estarlo?)
- **Consistencia:** ¿el mismo dato se contradice entre sistemas o períodos? (esto es justamente el problema de las "tres verdades" visto antes)
- **Oportunidad:** ¿el dato está disponible a tiempo para la decisión que debe apoyar? (un dato perfecto pero tardío no sirve)
- **Unicidad:** ¿cada entidad aparece una sola vez, sin duplicados?
- **Validez:** ¿el dato cumple con los formatos/reglas de negocio esperados? (por ejemplo, que un RUT tenga el formato correcto)

**Gobierno de datos** — esto va más allá de la calidad técnica, hacia la **responsabilidad organizacional**:

- **Data owner:** responde por el dato (dueño de negocio).
- **Data steward:** responde por su calidad diaria (rol operativo).
- **MDM (Master Data Management):** asegura que exista un identificador único por cliente/producto/proveedor en toda la organización — evitando que "Cliente 123" en un sistema sea "Cliente ABC" en otro.
- **Linaje y metadatos:** permiten rastrear de dónde viene cada indicador (trazabilidad), lo cual es necesario para auditorías y para entender el impacto de un cambio en el origen.

---

#### 8.5 Data Warehouse (DW)

Se define con cinco propiedades clásicas (definición de Inmon, aunque el documento no lo nombra explícitamente):

- **Variante en el tiempo:** conserva historia — cada registro es válido dentro de un horizonte temporal (a diferencia de un sistema operacional que solo tiene el estado _actual_).
- **Integrado:** nomenclatura, unidades y codificación homogéneas entre fuentes (resuelve el problema de "Ana Pérez" vs "A. Pérez" a nivel estructural).
- **Consistente:** definiciones únicas para toda la organización (esto es, literalmente, el mecanismo que resuelve el problema de las "tres verdades").
- **No volátil:** se carga y se consulta, pero no se actualiza transaccionalmente como una base operacional (no se hace UPDATE constante como en un sistema de ventas en vivo).
- **Temático:** está organizado por asunto de negocio (ventas, clientes, productos) y no por aplicación de origen (no está organizado "como está en el ERP" sino como tiene sentido para el análisis).

El DW comparte un **modelo integrado** (Ventas, Clientes, Productos, Tiempo, Sucursales, Empleados) donde todas las áreas usan las mismas dimensiones y definiciones — este es el mecanismo concreto que materializa el "Single Source of Truth".

---

#### 8.6 Modelado dimensional: hechos y dimensiones (esquema en estrella)

Este es uno de los conceptos técnicos más importantes del documento. El **esquema en estrella** tiene:

- **Tabla de hechos (fact table):** contiene las **métricas numéricas aditivas** (cosas que tiene sentido sumar: unidades, monto neto, descuento) y las **claves foráneas** que conectan con las dimensiones. En el ejemplo: `HECHO_VENTAS` con granularidad "línea de boleta".
- **Dimensiones:** tablas con **atributos descriptivos** que dan contexto al hecho — en el ejemplo: `DIM_TIEMPO`, `DIM_PRODUCTO`, `DIM_CLIENTE`, `DIM_TIENDA`. Estas definen los ejes por los cuales puedes filtrar, agrupar o crear jerarquías (por ejemplo, dentro de `DIM_TIEMPO` puede haber jerarquía día → mes → año).

**Concepto crítico:** la **granularidad** (el nivel de detalle de cada fila de la tabla de hechos) es _"la primera y más determinante decisión del diseño"_. Por ejemplo, si el grano es "línea de boleta", puedes analizar hasta el nivel de un producto individual dentro de una compra; si el grano fuera "boleta completa", perderías esa capacidad de detalle. Una vez que decides el grano, **no puedes recuperar detalle que no capturaste** — de ahí su importancia.

Este concepto se aplicará directamente en la actividad práctica de la veterinaria "Patitas" más adelante.

---

#### 8.7 Data Mart

Es un **subconjunto** del Data Warehouse, dedicado a un área de negocio específica (Comercial, Finanzas, RRHH). La idea es que cada área acceda solo a la porción de información relevante para ella, sin tener que navegar todo el repositorio corporativo completo.

**Advertencia importante:** _"un Data Mart mal gobernado vuelve a crear silos"_. Es decir, si los data marts se construyen de forma independiente (cada área arma "su" data mart sin pasar por el DW central), se reproduce exactamente el problema original que BI intentaba resolver (datos inconsistentes entre áreas). Por eso la regla es que **el data mart siempre debe derivar del Data Warehouse**, nunca construirse en paralelo o de forma aislada.

---

#### 8.8 Cubos OLAP (On-Line Analytical Processing)

Un cubo organiza los datos a lo largo de **ejes dimensionales** (por ciudad, vendedor, producto, fecha, cliente), donde cada celda del cubo es una agregación (precalculada o calculada al vuelo). Las operaciones típicas sobre un cubo son:

- **Roll-up:** subir de nivel de detalle agregando (de día a mes, de comuna a región) — vas hacia lo más general.
- **Drill-down:** lo opuesto — bajas al detalle para explicar una desviación observada (por ejemplo, ves que las ventas de la región bajaron, y haces drill-down para ver qué comuna específica causó la caída).
- **Slice:** fijas el valor de **una** dimensión y obtienes un subcubo más pequeño (por ejemplo, "solo ventas de 2026").
- **Dice:** restringes **varias** dimensiones simultáneamente con un rango de valores (por ejemplo, "ventas de 2026, en la región sur, del producto X").
- **Pivot:** rotas los ejes para ver las mismas medidas desde otra perspectiva (cambiar filas por columnas).
- **Drill-through:** bajas hasta la **transacción original** en el sistema operacional — el nivel más profundo posible, saliendo incluso del cubo hacia el dato fuente.

Estas operaciones conectan directamente con la idea de "niveles de decisión" vista antes: roll-up sirve para nivel estratégico (visión agregada), drill-down/drill-through sirven para nivel operacional (investigar el detalle).

---

#### 8.9 Implementaciones OLAP: ROLAP, MOLAP, HOLAP

Son tres formas técnicas distintas de implementar el análisis multidimensional:

||ROLAP|MOLAP|HOLAP|
|---|---|---|---|
|Almacena en|Tablas relacionales del DW|Estructuras multidimensionales propias|Mezcla de ambas|
|Escalabilidad|Alta (limitada por el motor SQL)|Menor (el cubo crece explosivamente)|Equilibrada|
|Velocidad|Variable (depende de índices)|Muy rápido sobre agregados precalculados|Rápido en agregados, aceptable en detalle|

La idea es que hay un **trade-off** entre velocidad de respuesta y escalabilidad/flexibilidad: MOLAP es rapidísimo pero no escala bien con volúmenes enormes; ROLAP escala mejor pero depende de qué tan bien esté optimizada la base relacional; HOLAP busca un punto medio.

También se mencionan técnicas de optimización: **índices bitmap** (para columnas con pocos valores distintos), **particionado por fecha** (para no escanear toda la tabla), **vistas materializadas** (resultados precalculados) y **almacenamiento columnar** (el estándar actual, porque comprime mejor y permite leer solo las columnas necesarias en vez de filas completas).

---

#### 8.10 Ecosistema de repositorios: Data Mart, ODS, Data Lake, Lakehouse

- **Data Mart:** ya visto — subconjunto departamental del DW.
- **ODS (Operational Data Store):** repositorio de **baja latencia**, con datos casi en tiempo real pero con historia mínima (no guarda años de historia, sino el estado reciente/operacional).
- **Data Lake:** almacena el dato **crudo**, en su formato nativo, sin estructurarlo de antemano — el esquema se aplica recién **al momento de leer** ("schema-on-read", en contraste con el DW que aplica el esquema al momento de cargar, "schema-on-write").
- **Lakehouse:** combina lo mejor de ambos mundos — formatos de tabla abiertos que agregan transacciones y esquema (como en un DW) pero sobre la infraestructura flexible de un lago de datos.

**Criterios para elegir entre ellos:**

- Si el esquema es estable y el uso es recurrente → el modelo dimensional (DW) sigue siendo superior.
- Si necesitas datos casi en tiempo real → ODS o streaming, no cargas nocturnas por lotes.
- Si el consumo es exploración libre de científicos de datos → data lake; si es consulta gobernada y repetible → DW.
- El lago abarata el almacenamiento, pero **traslada el costo** hacia la gobernanza y el cómputo necesario para consultar (porque el dato no viene pre-organizado).

---

#### 8.11 Dashboards y KPIs (la capa de explotación)

Esta es la capa "visible" para el negocio — lo que finalmente ve un gerente o usuario. Pero el documento insiste en un punto conceptual importante: **"un dashboard no es el proyecto: es su resultado visible"**. Es decir, todo lo anterior (fuentes, ETL, DW, modelado, OLAP) es lo que hace posible que el dashboard tenga sentido — el dashboard sin esa base es solo una fachada.

**Componentes de esta capa:**

- **Indicadores (KPI):** una métrica ligada a un objetivo, con **fórmula, dueño, meta y frecuencia** definidos. La frase clave: _"sin meta no hay indicador, sólo una cifra"_ — es decir, un número sin un objetivo de referencia (¿es bueno o malo este valor?) no es realmente un KPI, es solo un dato suelto.
- **Capa semántica:** traduce las tablas físicas (nombres técnicos de columnas) a **conceptos de negocio** entendibles, y centraliza la definición de las métricas para toda la organización (otra vez, mecanismo para el Single Source of Truth).
- **Tableros y reportes:** se distingue entre **tablero** (para monitoreo continuo, se revisa repetidamente) e **informe** (para análisis puntual, se genera una vez para responder algo específico). Cada objeto debe responder a una **pregunta explícita** — no se construye un dashboard "porque sí", sino para responder algo concreto.

**Buenas prácticas de visualización mencionadas:**

- Elegir el tipo de gráfico según la tarea (comparación, composición, distribución, evolución) — no todos los gráficos sirven para todo.
- Maximizar la **razón dato-tinta**: minimizar elementos decorativos que no aportan información (rejillas, sombras, efectos).
- **Jerarquía visual explícita**: lo primero que el ojo capta debe ser lo más importante para decidir.
- **Contexto obligatorio**: toda cifra debe mostrarse junto a su meta y su variación (conecta con la idea de que un KPI sin meta no es realmente útil).

---

### 9. Arquitectura completa (caso integrado)

Se presenta un flujo end-to-end concreto:

```
Fuentes (ERP, CRM, Excel, IoT, RRSS, API) → ETL → Data Warehouse → Data Mart → Modelo Estrella → Power BI → Dashboard → Gerencia
```

Esto es literalmente el resumen visual de **todo** lo explicado en las secciones 7 y 8, mostrado como un solo pipeline. La frase de cierre resume la filosofía completa del documento: _"el valor no está en ninguna capa aislada, sino en que todas conversen entre sí"_ — ninguna pieza sirve de mucho por sí sola; el valor emerge de la integración del conjunto.

---

### 10. Tipos de datos que alimentan BI

Se clasifican en tres categorías:

- **Estructurados:** datos en tablas relacionales (SQL Server, Oracle, PostgreSQL, MySQL) — fáciles de modelar con esquemas fijos.
- **Semiestructurados:** tienen cierta organización pero no un esquema rígido tabular (JSON, XML, CSV, logs).
- **No estructurados:** sin estructura predefinida (videos, audios, correos, PDF, imágenes, redes sociales).

**Dato importante:** _"hoy la mayor parte del dato disponible en una empresa no está estructurado"_. Esto explica por qué han surgido tecnologías como Big Data/Data Lake — el modelo relacional tradicional (DW clásico) fue diseñado pensando en datos estructurados, y no maneja bien de forma nativa video, audio o texto libre.

---

### 11. El ciclo de vida del dato (jerarquía DIKW)

```
Dato → Información → Conocimiento → Decisión → Acción → Valor
```

Esta es la jerarquía **DIKW** (Data-Information-Knowledge-Wisdom, adaptada aquí). La idea conceptual es que **cada etapa reduce el volumen pero aumenta el valor**: tienes millones de filas de "dato" crudo, que se procesan hasta convertirse en unas pocas "decisiones" concretas, y finalmente en "acciones" que cierran el ciclo generando valor real para el negocio. Es, en cierto sentido, la versión más abstracta/filosófica del mismo flujo "Capturar → Organizar → Analizar → Decidir" visto en la definición práctica de BI (sección 2) y del pipeline técnico completo (sección 9). El documento usa tres formulaciones distintas del mismo concepto central, a distintos niveles de abstracción.

---

### 12. Actividad: la veterinaria "Patitas" (aplicación práctica)

Esta actividad busca que apliques dos conceptos técnicos vistos: **modelo relacional (normalización)** y **modelo dimensional (estrella)**, partiendo de una planilla plana de atenciones veterinarias que mezcla datos de propietario, mascota, veterinario y consulta en una sola tabla.

**Paso 1 — Modelo relacional:**

1. Identificar entidades distintas mezcladas en la planilla (probablemente: Propietario, Mascota, Veterinario, Diagnóstico/Tratamiento, y la Atención/Visita como tabla central).
2. Definir clave primaria para cada tabla.
3. Conectar las tablas mediante relaciones (claves foráneas).
4. Eliminar repeticiones — cada dato debe existir una sola vez (esto es literalmente **normalización**, y resuelve el mismo problema de "datos duplicados/inconsistentes" que motivó el nacimiento de BI en la sección 3). El documento incluso te pide anotar previamente **problemas de calidad de datos** en la planilla (por ejemplo, notarás que hay nombres de propietarios escritos distinto, un teléfono con typo, direcciones escritas de forma inconsistente — ejercicio directo de las dimensiones de calidad vistas en 8.4).

**Paso 2 — Modelo estrella:**

1. Elegir el **hecho** (el evento de negocio a medir — aquí sería "atención/consulta veterinaria").
2. Definir las **métricas** (qué se suma/cuenta/promedia — por ejemplo, cantidad de atenciones, o si hubiera montos, el monto facturado).
3. Definir las **dimensiones** (por qué criterios se quiere filtrar/agrupar — veterinario, especie, mes, tipo de tratamiento).
4. Formular tres preguntas de negocio que el modelo deba poder responder (por ejemplo: "¿cuánto factura cada veterinario por especie, mes a mes?" — la pregunta original de la dueña de la clínica).

El **criterio de éxito** es poder responder esas preguntas **sin volver a abrir la planilla original** — es decir, que el modelo dimensional efectivamente capture toda la información necesaria en una estructura consultable.

---

### 13. Ejemplo empresarial y caso de estudio (retail/supermercado)

Se refuerza el mismo patrón con un caso de retail:

```
POS → Ventas
ERP → Inventario
CRM → Clientes
E-commerce → Google Analytics
Facebook Ads → Excel
Power BI → Gerencia
```

Y el caso de estudio del supermercado plantea un problema real ("las ventas disminuyen, ¿qué necesita saber la gerencia?") y te pide mapear: qué información se necesita (ventas por sucursal/producto/hora, productos más vendidos, clientes frecuentes, rentabilidad, stock, promociones) contra en qué sistemas existen esos datos (ERP, CRM, POS, Inventario, RRHH, Excel, Web). Este ejercicio es, en esencia, la sección 8.1 (Fuentes de datos) aplicada a un caso concreto.

---

### 14. Actividad en equipos (empresas variadas)

Se pide elegir una empresa (Banco, Clínica, Universidad, Retail, Aerolínea, Minera) y responder las mismas cuatro preguntas estructurales que has visto aplicadas una y otra vez en el documento: qué decisiones toma, qué datos necesita y dónde se generan, qué indicadores mediría, y cómo sería su arquitectura BI. Es la consolidación final de todo el marco conceptual aplicado a un caso propio.

---

### 15. Conclusiones e ideas clave para llevarse

El documento cierra reforzando cuatro ideas de síntesis, cada una resumiendo una sección distinta del contenido:

1. **BI es una arquitectura, no una herramienta** → conecta con la sección 7 (arquitectura de referencia) y corrige la confusión común de creer que BI = Power BI.
2. **La granularidad define el modelo** → conecta con la sección 8.6 (modelado dimensional), reforzando que es la decisión de diseño más determinante.
3. **La calidad se diseña, no se corrige** → conecta con 8.2/8.4 (ETL y gobierno de datos): los controles de calidad deben estar en el flujo de integración, no parcheados al final en el informe.
4. **La latencia se ajusta a la decisión** → conecta con 8.10 (ecosistema de repositorios): no hay una arquitectura "óptima universal"; depende de qué tan rápido necesitas la información para poder actuar sobre ella.

---

### 16. Qué viene después en el curso

Esta primera clase es explícitamente conceptual/introductoria. Las unidades siguientes profundizarán técnicamente en: **Modelamiento dimensional**, **Procesos ETL**, **Data Warehouse**, **Power BI**, **Minería de datos** y **Analítica avanzada** — es decir, cada uno de los componentes que en esta clase se explicaron a nivel de "qué es y para qué sirve" se convertirá en su propia unidad de trabajo práctico y técnico más profundo.