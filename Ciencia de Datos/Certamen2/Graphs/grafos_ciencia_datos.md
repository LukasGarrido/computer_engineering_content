# Grafos en Ciencia de Datos: Guía Completa

Los **grafos** son una de las herramientas más poderosas y avanzadas en la ciencia de datos moderna. Mientras que las bases de datos tradicionales organizan la información en estructuras rígidas de filas y columnas (tablas), los grafos se enfocan en las **relaciones** inherentes entre los datos. 

Si alguna vez te has preguntado cómo Netflix te recomienda una serie, cómo Google Maps encuentra la ruta más rápida, o cómo las entidades bancarias detectan redes complejas de fraude financiero, la respuesta subyace en la teoría y aplicación de grafos.

---

## 1. ¿Qué es un Grafo? (Componentes Básicos)

Un grafo es una estructura matemática abstracta que se utiliza para modelar relaciones de par a par entre objetos. Consta de dos elementos fundamentales:

1. **Nodos (o Vértices):** Representan las entidades u objetos del dominio (por ejemplo: usuarios, ciudades, páginas web, productos, proteínas).
2. **Aristas (o Enlaces):** Representan las relaciones, interacciones o conexiones entre dichos nodos (por ejemplo: "es amigo de", "viajó a", "enlazó a", "compró", "interactúa con").

Tanto los nodos como las aristas pueden contener **propiedades** (atributos en forma de clave-valor). Por ejemplo, un nodo de tipo "Persona" puede tener las propiedades `Edad`, `Nombre` y `País`, mientras que una arista de tipo "Amigo de" puede incluir la propiedad `Desde qué año` o `Nivel de interacción`.

### Clasificación de Grafos según sus Conexiones

* **Grafos Dirigidos (Dígrafos):** Las relaciones tienen un sentido o dirección única. Se representan con flechas.
  * *Ejemplo:* Twitter o Instagram. Si el Usuario A sigue al Usuario B ($A \rightarrow B$), no significa automáticamente que el Usuario B siga al Usuario A.
* **Grafos No Dirigidos:** Las relaciones son simétricas y bidireccionales por naturaleza.
  * *Ejemplo:* Facebook o LinkedIn. Si el Usuario A es amigo del Usuario B ($A \leftrightarrow B$), la conexión es mutua.
* **Grafos Ponderados:** Las aristas tienen un "peso", costo o valor numérico asignado que cuantifica la relación.
  * *Ejemplo:* Un mapa de carreteras. Los nodos son ciudades y las aristas son las carreteras; el peso de la arista representa la distancia en kilómetros o el tiempo de viaje.

---

## 2. ¿Por qué son cruciales en Ciencia de Datos?

En los enfoques tradicionales de Machine Learning, a menudo se asume que las observaciones (filas) son **independientes e idénticamente distribuidas (i.i.d.)**. Sin embargo, en el mundo real, los datos están interconectados y el contexto lo es todo.

Los grafos permiten a los científicos de datos:
* **Capturar topologías complejas:** Modelar sistemas interdependientes como cadenas de suministro globales, redes de energía o interacciones moleculares sin perder la información relacional.
* **Ingeniería de Características Avanzada (Feature Engineering):** Extraer métricas estructurales de la posición de un nodo en la red (ej. su nivel de conectividad) y utilizarlas como variables de entrada para modelos predictivos tradicionales (como XGBoost o Random Forest), incrementando drásticamente su precisión.
* **Superar las limitaciones de SQL:** Las consultas que requieren múltiples niveles de separación (ej. "los amigos de los amigos de mis amigos") son computacionalmente prohibitivas en bases de datos relacionales tradicionales debido a los costosos *JOINs*, mientras que en bases de datos de grafos se resuelven mediante simples recorridos de punteros.

---

## 3. Algoritmos de Grafos Esenciales

Para extraer valor y conocimiento de una estructura de grafo, se emplean algoritmos especializados clasificados en tres grandes familias:

### A. Algoritmos de Centralidad e Importancia
Identifican cuáles son los nodos más influyentes o críticos dentro de la red.
* **PageRank:** Desarrollado originalmente por Google, mide la relevancia de un nodo de manera iterativa en función de la cantidad y la calidad (importancia) de los nodos que lo enlazan.
* **Grado de Centralidad (Degree Centrality):** El cálculo más simple; cuenta el número de conexiones directas que posee un nodo.
* **Centralidad de Intermediación (Betweenness Centrality):** Mide cuántas veces un nodo actúa como "puente" en el camino más corto entre todos los demás pares de nodos. Los nodos con alta intermediación controlan el flujo de información.

### B. Detección de Comunidades (Agrupación / Clustering)
Identifican grupos o subestructuras de nodos que están densamente conectados entre sí, pero escasamente conectados con el resto de la red.
* **Algoritmo de Louvain:** Basado en la optimización de la *modularidad*, es altamente escalable y agrupa nodos de forma jerárquica para descubrir estructuras comunitarias ocultas.
* **Connected Components:** Identifica subgrafos aislados donde todos los nodos están conectados entre sí por algún camino.

### C. Caminos Mínimos y Recorridos (Pathfinding)
Calculan la ruta más eficiente entre nodos evaluando los pesos de las aristas.
* **Algoritmo de Dijkstra:** Encuentra el camino más corto desde un nodo origen a todos los demás nodos en un grafo con pesos no negativos. Es el núcleo detrás de los sistemas de navegación GPS como Waze o Google Maps.

---

## 4. El Siguiente Nivel: Graph Neural Networks (GNN)

El estado del arte en la intersección de grafos y la Inteligencia Artificial es el **Deep Learning sobre Grafos** mediante las *Graph Neural Networks* (Redes Neuronales de Grafos).

A diferencia de las Redes Neuronales Convolucionales (CNN) diseñadas para imágenes (mallas regulares de píxeles) o las Redes Recurrentes/Transformers diseñadas para secuencias de texto, las GNNs procesan topologías irregulares y dinámicas.

### ¿Cómo funcionan?
Utilizan un mecanismo llamado **Message Passing** (Paso de Mensajes). Cada nodo recopila información (características) de sus vecinos directos, la agrega mediante funciones matemáticas y actualiza su propio estado de forma iterativa. Al cabo de varias capas, cada nodo posee una representación vectorial (*embedding*) que codifica tanto sus propios atributos como la estructura de su entorno.

### Tipos de Predicciones con GNNs:
1. **A nivel de Nodo:** Clasificar una entidad (ej. identificar si un usuario de una red social es un bot o una cuenta legítima).
2. **A nivel de Arista (Link Prediction):** Predecir si existirá una conexión en el futuro (ej. sugerir conexiones en LinkedIn o productos altamente probables de adquirir juntos).
3. **A nivel de Grafo completo:** Clasificar o agrupar el grafo entero (ej. determinar si una estructura molecular química específica es tóxica o tiene potencial curativo).

---

## 5. Casos de Uso en la Industria

| Industria / Sector | Aplicación del Grafo | Impacto de Negocio |
| :--- | :--- | :--- |
| **E-commerce & Streaming** | Motores de recomendación basados en grafos bapartitos (Usuarios - Productos). | Incremento del *Click-Through Rate* (CTR) y personalización hiperprecisa. |
| **Finanzas e Inteligencia** | Detección de fraude (redes de lavado de dinero, esquemas Ponzi, anillos de fraude de identidad sintética). | Bloqueo en tiempo real de transacciones sospechosas mediante patrones de comportamiento de red. |
| **Ciberseguridad** | Mapas de infraestructura de red y análisis de dependencias de software. | Identificación instantánea del radio de impacto de una brecha de seguridad (*blast radius*). |
| **Biomedicina y Farmacia** | Modelado de interacciones fármaco-blanco y redes biológicas de proteínas. | Reducción de años de investigación en el descubrimiento de nuevos medicamentos y terapias. |
| **Logística y Transporte** | Optimización de flotas de entrega y diseño de rutas de última milla. | Reducción drástica de costos operativos y huella de carbono. |

---

## 6. Ecosistema Tecnológico para Científicos de Datos

Si deseas comenzar a implementar grafos en tus proyectos, estas son las herramientas estándar de la industria:

* **Librerías de Python (Análisis y Exploración):**
  * `NetworkX`: Excelente para manipulación de grafos de tamaño pequeño a mediano, cálculo de métricas y algoritmos estándar.
  * `igraph`: Alternativa de alto rendimiento escrita en C con interfaz para Python, óptima para grafos más grandes.
* **Frameworks de Graph Deep Learning (GNNs):**
  * `PyTorch Geometric (PyG)`: La librería líder basada en PyTorch para construir y entrenar redes neuronales de grafos.
  * `Deep Graph Library (DGL)`: Framework robusto compatible con múltiples backends (PyTorch, TensorFlow).
* **Bases de Datos de Grafos (Almacenamiento Empresarial):**
  * `Neo4j`: La base de datos orientada a grafos más popular del mercado, que utiliza el lenguaje de consulta intuitivo *Cypher*.
  * `Amazon Neptune` / `Google Graph Database`: Soluciones en la nube totalmente gestionadas.

## 7. Laboratorio de grafos 
### 1. Conceptos fundamentales de grafos
Un grafo es una estructura matemática que modela relaciones entre objetos 

Formalmente, un grafo $G$ se define como un par $G = (V, E)$, donde:
- $V$ es un conjunto de **nodos** (o vértices): los objetos que queremos modelar.
- $E$ es un conjunto de **aristas** (o edges): las relaciones entre pares de nodos.

### 2. Tipos de grafos
| Tipo | Descripción | Ejemplo |
|------|-------------|--------|
| **No dirigido** | Las aristas no tienen dirección; la relación es simétrica | Red de amistades |
| **Dirigido** (dígrafo) | Las aristas tienen dirección: $(u, v) \neq (v, u)$ | Twitter (seguir) |
| **Ponderado** | Cada arista tiene un peso numérico asociado | Carreteras (distancia, tiempo) |
| **No ponderado** | Todas las aristas valen igual | Hiperenlaces web |

### 3. Conceptos clave 
**Grado de un nodo (*degree*):** El número de aristas que inciden en un nodo. En un grafo no dirigido, indica cuántos vecinos directos tiene ese nodo. Un nodo con grado alto es una intersección muy conectada; con grado 1 es un callejón sin salida.

**Camino (*path*):** Una secuencia de nodos $v_1, v_2, \ldots, v_k$ tal que existe una arista entre cada par consecutivo. La longitud del camino es la suma de los pesos de sus aristas (en grafos ponderados) o simplemente el número de aristas (en no ponderados).

**Camino mínimo (*shortest path*):** El camino de menor coste total entre dos nodos. En una red de carreteras, puede significar la ruta más corta en kilómetros o la más rápida en tiempo.

**Distancia entre dos nodos:** La longitud del camino mínimo entre ellos. Si no hay camino (el grafo no es conexo), la distancia es infinita.

**Componente conexa:** Un subconjunto de nodos tal que existe un camino entre cualquier par. Una red de carreteras puede tener nodos aislados (islas sin conexión terrestre), que forman componentes separadas.

![[Pasted image 20260613223746.png]]

**Centralidad (*centrality*)** Familia de métricas que cuantifican la importancia de un nodo dentro de la red. Algunas de las más usadas son: 
- Centralidad de grado (_Degree Centrality_) para nodos con más conexiones directas
- Centralidad de intermediación (_Betweenness Centrality_) para nodos que aparecen en muchos caminos mínimos y cuya eliminación desconectaría la red
- PageRank para nodos que son importantes porque sus vecinos también lo son.


# Análisis Exhaustivo de Arquitectura y Flujo Técnico: Taller de Grafos en Ciencia de Datos

Este documento presenta un desglose de ingeniería y análisis didáctico del Jupyter Notebook provisto. El objetivo es documentar cada componente matemático, algorítmico, estructural y de infraestructura de datos sin restricciones de longitud, sirviendo como guía técnica completa de la actividad.

---

## 1. Introducción y Planteamiento del Problema Logístico

El taller se estructura alrededor de una pregunta clásico de optimización en redes físicas y logística de operaciones: **"Dada una red de carreteras real, ¿desde qué punto conviene partir si quiero llegar lo más rápido posible a todos los demás lugares de la red?"**. 

Esta premisa sirve como hilo conductor para resolver problemas reales en la ciencia de datos aplicada, tales como:
* El diseño de cadenas de suministro (ubicación óptima de centros de distribución).
* El análisis de resiliencia de infraestructura crítica frente a fallos locales o bloqueos de rutas.
* El modelado de la eficiencia del transporte público y privado a escala macroscópica.

El reto principal que plantea el notebook es metodológico y computacional: pasar del análisis académico de redes pequeñas de juguete al procesamiento de datos viales a escala de un país entero (Gran Bretaña), abordando las limitaciones de la CPU tradicional a través de arquitecturas de hardware acelerado (GPUs).

---

## 2. Fundamentos Teóricos de la Teoría de Grafos Aplicada

El marco teórico del notebook define matemáticamente un grafo como un par ordenado:

$$G = (V, E)$$

Donde:
* **$V$ (Vértices o Nodos):** Representan entidades individuales discretas. En el contexto vial, equivalen a intersecciones, rotondas, finales de calle o bifurcaciones geográficas.
* **$E$ (Aristas o Enlaces):** Representan relaciones o conexiones entre pares de nodos. Aquí equivalen a segmentos físicos de carreteras, calles, avenidas o autopistas que permiten el flujo vehicular.

### Clasificación y Propiedades Estructurales del Grafo del Taller
El notebook guía al usuario a través de la identificación de las características específicas del grafo vial:

* **Grafo No Dirigido (Undirected Graph):** Se asume que el tráfico puede fluir en ambos sentidos de la vía. Matemáticamente, si existe una arista $(u, v) \in E$, automáticamente implica la existencia de la arista inversa $(v, u) \in E$ con idénticas propiedades de conectividad.
* **Grafo Ponderado o Valorado (Weighted Graph):** Las aristas no representan únicamente una conexión lógica binaria ($0$ o $1$), sino que llevan asociado un costo o "peso" ($W$). El notebook maneja dos funciones de peso distintas para la misma topología de red:
  1. $W(e) = \text{Longitud física en metros (parámetro espacial)}$.
  2. $W(e) = \text{Tiempo estimado de viaje en segundos (parámetro dinámico/temporal)}$.

### Glosario de Métricas Críticas Tratadas
El notebook introduce y calcula varias métricas clave para diagnosticar la salud y comportamiento de la red:

1. **Grado de un Nodo ($k_i$):** En grafos no dirigidos, es el número total de aristas conectadas directamente al nodo $i$. En redes viales reales, un grado alto identifica intersecciones de alta complejidad (ej. rotondas principales con múltiples salidas o cruces de autopistas).
2. **Camino (*Path*):** Una secuencia finita de aristas que conecta una serie de nodos distintos sin repetir vértices intermedios.
3. **Camino Mínimo (*Shortest Path*):** El camino entre un nodo origen $s$ y un nodo destino $t$ tal que la suma de los pesos de las aristas que lo componen sea mínima:
   $$\min \sum_{e \in \text{camino}} W(e)$$
4. **Componente Conexa (*Connected Component*):** Un subógrafo en el cual cualquier par de nodos está conectado entre sí mediante al menos un camino. Si un grafo tiene nodos aislados o islas físicas sin puentes, se generan múltiples componentes conexas.
5. **Métricas de Centralidad:**
   * **Centralidad de Grado (*Degree Centrality*):** Importancia basada únicamente en la cantidad de vecinos directos.
   * **Centralidad de Intermediación (*Betweenness Centrality*):** Mide cuántas veces un nodo actúa como "puente" o paso obligatorio a lo largo de los caminos mínimos entre todos los demás pares de nodos de la red. Es crucial para identificar cuellos de botella en el tráfico.
   * **PageRank:** Algoritmo de centralidad por vectores propios (adaptado originalmente por Google para páginas web) que asigna relevancia a un nodo si está conectado a otros nodos que a su vez son altamente relevantes.

---

## 3. Desglose del Conjunto de Datos (Dataset Splitting)

La infraestructura vial del ejercicio está distribuida en cuatro archivos estructurados en formato CSV. La separación limpia de los datos físicos espaciales y los dinámicos permite realizar análisis comparativos avanzados:

### 1. `road_nodes.csv` (Atributos de Vértices)
Contiene la geolocalización de las intersecciones. 
* **Estructura típica de columnas:** `node_id` (identificador único del nodo), `east` (coordenada este en el sistema de proyección geográfica local), `north` (coordenada norte) y `type` (clasificación del tipo de intersección).
* **Propósito en el flujo:** Esencial para mapear las coordenadas espaciales finales durante la etapa de visualización interactiva.

### 2. `road_graph.csv` (Topología y Distancia Métrica)
Contiene la lista de adyacencia base parametrizada por distancia física.
* **Estructura típica de columnas:** `src` (nodo origen), `dst` (nodo destino) y `length` (longitud real del segmento vial expresada en metros).
* **Propósito en el flujo:** Define la conectividad estructural pura y sirve para computar rutas óptimas orientadas al ahorro de combustible por kilometraje recorrido.

### 3. `road_graph_speed.csv` (Topología Dinámica y Tiempo de Viaje)
Mismo esqueleto estructural que el archivo anterior, pero incorporando las variables de velocidad de las vías.
* **Estructura típica de columnas:** `src` (nodo origen), `dst` (nodo destino) y `length_s` (tiempo de tránsito estimado en segundos).
* **Propósito en el flujo:** Calcula el costo de tiempo. Permite evaluar la velocidad promedio permitida o estimada en cada tramo (por ejemplo, autopistas de alta velocidad frente a calles residenciales estrechas).

### 4. `node_graph_map.csv` (Normalización de Índices)
Tabla técnica de traducción e indexación.
* **Estructura típica de columnas:** `node_id` (cadenas de caracteres largas o identificadores alfanuméricos originales de la base de datos geográfica) y `graph_id` (números enteros secuenciales basados en cero: $0, 1, 2, \dots$).
* **Propósito en el flujo:** **Optimización de memoria crítica**. Los motores de cálculo de grafos eficientes (como cuGraph) requieren índices enteros contiguos para mapear arrays en memoria de GPU sin desperdiciar direccionamiento de punteros. Esta tabla traduce el "nombre" real del nodo a su representación matemática compacta interna.

---

## 4. Comparativa de la Pila de Software (Software Stack)

El notebook expone de manera práctica el cambio de paradigma entre la computación secuencial en CPU y el paralelismo masivo en GPU:


### NetworkX (Métricas en CPU)
* **Ventajas:** Extremadamente maduro, API rica en funciones y algoritmos complejos, documentación robusta.
* **Desventajas:** Escalamiento ineficiente. Las estructuras de datos internas están basadas en diccionarios anidados de Python. Para redes de cientos de miles de nodos y millones de aristas, el consumo de memoria RAM se dispara exponencialmente y algoritmos con complejidad temporal superior a lineal (como Dijkstra u operaciones de centralidad global) pueden tardar horas o incluso colgar el entorno de ejecución por *Out Of Memory* (OOM).

### cuGraph (Ecosistema RAPIDS de NVIDIA)
* **Ventajas:** Diseñado desde cero para la analítica de grafos a gran escala en hardware de procesamiento paralelo. Utiliza estructuras de arrays primitivas y optimizadas directamente en la memoria de la tarjeta gráfica (VRAM) mediante CUDA. Un algoritmo SSSP o un cálculo de centralidad global que toma minutos o decenas de minutos en CPU se resuelve aquí en milisegundos o pocos segundos (aceleraciones de entre **10× y 100×**).
* **Desventajas:** Requiere obligatoriamente hardware dedicado de arquitectura NVIDIA, y su API, aunque similar a la de NetworkX, está más restringida a algoritmos de alta demanda de paralelismo.

### Graphistry (Visualización Interactiva)
* **Ventajas:** Delegación de la carga de renderizado al motor WebGL del navegador del cliente empleando la GPU local. Permite explorar de forma fluida, hacer zoom, arrastrar nodos y aplicar filtros dinámicos en tiempo real sobre grafos con decenas de miles de elementos interactivos concurrentes, algo imposible con gráficos de imágenes estáticas tipo PNG generadas por Matplotlib o Seaborn.

---

## 5. Análisis del Pipeline de Ejecución Paso a Paso

El notebook ejecuta un flujo de trabajo lineal estructurado en cinco fases principales:

### Fase 1: Preparación del Entorno de Ejecución
1. El script detecta el entorno de hardware y descarga las dependencias del ecosistema RAPIDS de NVIDIA mediante scripts bash automatizados.
2. Se importan las librerías principales (`sys`, `warnings`, `cudf`, `cugraph`, `cupy`, `graphistry`).

### Fase 2: Ingesta de Datos y Construcción del Objeto Grafo
1. Carga de los archivos CSV usando `cudf.read_csv()`, lo que posiciona los datos directamente en la memoria de la GPU, evitando los cuellos de botella de transferencia de bus.
2. Mapeo e indexación: Se cruzan las tablas de aristas con la tabla `node_graph_map.csv` para asegurar que las columnas de origen (`src`) y destino (`dst`) contengan índices numéricos enteros secuenciales limpios.
3. **Instanciación en cuGraph:** Se crea un objeto de tipo grafo no dirigido (`cugraph.Graph(directed=False)`) o directo según la fase del laboratorio. Se le añaden las aristas especificando qué columnas representan el origen, el destino y el atributo de peso (`weight`).

### Fase 3: Análisis Estructural Inicial y Estadísticas de Grado
1. **Extracción de la distribución de grados:** Ejecución del método `G.degree()` que genera un DataFrame con el ID de cada nodo y su cantidad de conexiones directas.
2. **Filtrado de los nodos top conectados:** Utilizando funciones optimizadas como `deg_df.nlargest(10, 'degree')`, el sistema identifica cuáles son los hubs viales o intersecciones críticas de la isla.
3. **Detección de bucles (self-loops):** Identificación de aristas anómalas o particulares cuyo nodo origen coincide exactamente con su nodo destino (`src == dst`), eliminándolas o analizándolas por separado según las necesidades de la red viales.
4. **Cálculo de Centralidad de Intermediación:** Ejecución de submuestreos para computar qué nodos se interponen con mayor frecuencia en los flujos globales de transporte.

### Fase 4: Cómputo de Caminos Mínimos (Algoritmo SSSP)
El corazón algorítmico del taller ejecuta el análisis SSSP (*Single Source Shortest Path*).



1. **Selección del punto de origen:** En el ejercicio guiado se escoge estratégicamente el nodo con el mayor grado de la red para evaluar su eficiencia global.
2. **Ejecución de Dijkstra en GPU:** Se invoca la función `cugraph.sssp(G, source=nodo_elegido)`. El motor calcula simultáneamente el costo de viaje más bajo posible desde ese nodo origen hacia **absolutamente todos** los demás nodos de la red viales.
3. El proceso se repite en dos instancias separadas:
   * Instancia A: Grafo ponderado por metros (`road_graph.csv`).
   * Instancia B: Grafo ponderado por segundos de viaje (`road_graph_speed.csv`).
4. **Tratamiento de Nodos Inalcanzables:** El algoritmo devuelve un valor numérico infinito o un marcador nulo (`NaN` / `inf`) para aquellos nodos a los cuales es físicamente imposible acceder desde el origen elegido. El notebook enseña a filtrar y aislar estos registros, explicando que corresponden a subcomponentes desconectadas (por ejemplo, islas británicas menores o territorios aislados que no cuentan con puentes ni transbordadores modelados dentro del dataset).

### Fase 5: Visualización de Resultados y Exportación del Árbol de Caminos Mínimos
1. Los resultados tabulares del SSSP (distancias y tiempos calculados) se unifican mediante operaciones de unión (*joins*) con las coordenadas espaciales de `road_nodes.csv`.
2. Se extrae el **Árbol de Caminos Mínimos** (*Shortest Path Tree*): Un subconjunto del grafo original que contiene todas las aristas estrictamente necesarias para conectar el nodo origen con todos los destinos alcanzables optimizando el peso seleccionado.
3. Los datos consolidados se envían a los servidores de Graphistry mediante credenciales e inicialización de su API de desarrollo (`graphistry.register()`).
4. Se configuran las propiedades visuales: El notebook parametriza los nodos para que cambien de tonalidad cromática (ej. degradados de verde a rojo) basándose en la distancia temporal o espacial calculada, permitiendo identificar de un vistazo las zonas geográficas periféricas o "aisladas" del país respecto al punto de origen.

---

## 6. Análisis Técnico del Cuestionario de Evaluación (Actividades)

Al cierre de la sesión práctica, el notebook desafía a los estudiantes mediante tres preguntas analíticas fundamentales pensadas para conectar los datos duros arrojados por el código con la teoría pura y las decisiones de negocio de la vida real:

### Pregunta 1: Distribución de Grados y Topología Vial
> *“Al analizar los grados de los nodos, vimos que todos son múltiplos de 2. ¿Por qué es así en un grafo no dirigido? ¿Qué significaría que un nodo tuviera grado 1 en esta red de carreteras? ¿Y grado 0?”*

* **Explicación del fenómeno (Múltiplos de 2):** Al modelar una red vial real como un grafo no dirigido a partir de datos estructurados para simular tráfico bidireccional, por cada conexión física que se procesa en el código, el sistema inserta dos aristas lógicas en las estructuras de adyacencia de la GPU (una de ida: $A \rightarrow B$ y otra de vuelta: $B \rightarrow A$). Debido a esto, cada camino físico que interactúa con un nodo añade un factor de $+2$ a su grado total de adyacencia interna.
* **Significado de Grado = 1:** En esta configuración de modelado (donde la bidireccionalidad duplica las aristas), un grado absoluto igual a $1$ rompería la simetría bidireccional. Si se habla de una sola vía física de entrada y salida, su grado lógico interno computado sería $2$. Un nodo con grado real impar o igual a $1$ denotaría un callejón sin salida unidireccional (una calle por la que se puede entrar pero no salir en coche, o viceversa), o bien un error de consistencia o asimetría en la limpieza previa de la base de datos vial.
* **Significado de Grado = 0:** Representa un nodo totalmente aislado del sistema viales. Geográficamente equivale a un punto de control, una coordenada errónea, o una micro-isla deshabitada registrada en el catastro cartográfico pero que carece por completo de cualquier segmento de calle o carretera que la conecte con el resto del continente.

### Pregunta 2: Distancia Geométrica vs. Tiempo de Tránsito
> *“Ejecutamos el SSSP con dos grafos distintos: uno con pesos de longitud y otro con pesos de tiempo de viaje. Puede que el camino más corto en distancia no sea el mismo que el más rápido. ¿En qué situación real podría ocurrir que el camino más corto en kilómetros sea más lento que una ruta más larga? ¿En qué situaciones podría dársele prioridad a uno o al otro al momento de diseñar una ruta?”*

* **Situaciones de Discrepancia Real:** Una ruta geométrica en línea recta o con menos kilómetros puede resultar drásticamente más lenta debido a factores como:
  * **Límites de velocidad y jerarquía vial:** Cruzar centros urbanos densos con semáforos, pasos de peatones y límites de $30\text{ km/h}$, frente a rodear la ciudad por una autopista de circunvalación libre que duplica la distancia física pero permite circular constantemente a $120\text{ km/h}$.
  * **Topografía y condiciones técnicas:** Carreteras secundarias de montaña con curvas cerradas pronunciadas que obligan a marchar a baja velocidad, frente a autopistas llanas bien pavimentadas.
  * **Congestión y tráfico dinámico:** Cuellos de botella en horas punta.
* **Criterios de Priorización en Diseño de Rutas:**
  * **Prioridad al Tiempo (Ruta más rápida):** Logística de entrega urgente (e-commerce con envíos en el mismo día), vehículos de servicios de emergencia (ambulancias, bomberos) o transporte de pasajeros de negocios donde el costo del tiempo supera al del combustible.
  * **Prioridad a la Distancia (Ruta más corta):** Gestión de flotas de camiones de carga pesada muy restringidos por el consumo de combustible por kilómetro, transportes especiales con tarifas tasadas por distancia recorrida, o flotas de vehículos eléctricos urbanos que buscan maximizar la autonomía de sus baterías aprovechando el frenado regenerativo en tráfico lento.

### Pregunta 3: Criterios de Centralidad Logística para Distribución
> *“Retomemos la pregunta inicial: ¿desde dónde conviene partir si quiero llegar rápido a todos los demás lugares de la red? En el taller elegimos el nodo de mayor grado como punto de partida. Pero 'conviene partir' puede interpretarse de varias maneras: Minimizar el tiempo máximo hasta cualquier otro punto (minmax). Minimizar la suma total de tiempos a todos los demás. Minimizar la distancia al punto más lejano de la red. ¿Estas tres interpretaciones darían el mismo nodo óptimo? ¿Hay una que te parezca más relevante para, por ejemplo, ubicar un centro de distribución logístico? Justifica...”*

* **¿Coinciden los Nodos Óptimos?: No.** Cada una de estas interpretaciones formales de optimización responde a una función matemática de costo distinta, lo que típicamente genera nodos solución diferentes en redes complejas:
  1. **Minimizar el tiempo máximo (*MinMax* o Centro del Grafo):** Busca un nodo cuya peor ruta posible sea lo menos mala posible. Ideal para mitigar riesgos extremos.
  2. **Minimizar la suma total de tiempos (Mediana del Grafo / Centralidad de Cercanía):** Maximiza la eficiencia promedio del sistema global.
  3. **Minimizar la distancia geométrica al punto más lejano:** Se enfoca puramente en la métrica espacial restrictiva, ignorando las velocidades de las autopistas.
* **Criterio Más Relevante para un Centro de Distribución Logístico:**
  * La opción más competitiva comercialmente suele ser **minimizar la suma total de tiempos a todos los destinos** (enfoque de la Mediana del Grafo o Centralidad de Cercanía). La rentabilidad de una empresa de distribución depende del costo operativo acumulado de todas sus entregas diarias. Minimizar la sumatoria global de los tiempos se traduce directamente en un menor consumo de combustible global, menores costos de horas de trabajo para los choferes y una rotación de inventario mucho más ágil.
  * *Excepción Crítica:* Si el centro logístico distribuye productos altamente perecederos (como órganos para trasplantes, medicamentos críticos o hielo seco), o si cuenta con contratos de SLA (Acuerdos de Nivel de Servicio) punitivos donde retrasarse más allá de un límite con un cliente lejano genera quiebras contractuales, entonces el enfoque **MinMax** pasa a ser prioritario para asegurar que ningún cliente quede fuera del rango de tiempo máximo de supervivencia del producto.
```