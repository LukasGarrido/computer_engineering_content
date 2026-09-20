# Análisis de Componentes Principales (PCA)

**Curso:** EIN092B - Visualización **Autor:** Jorge Portilla — Depto. de Electrónica e Informática, Universidad Técnica Federico Santa María, Concepción, Chile

Este documento desarrolla en profundidad los contenidos sobre **Análisis de Componentes Principales (PCA)**, una de las técnicas más importantes de reducción de dimensionalidad, junto con su comparación con **t-SNE**, otra técnica no lineal orientada específicamente a la visualización de datos de alta dimensión.

---

## 1. Introducción: la maldición de la dimensionalidad

El documento parte presentando el concepto de **"Curse of Dimensionality"** (maldición de la dimensionalidad), que aborda los desafíos que emergen al trabajar con conjuntos de datos de **alta dimensionalidad** (es decir, con muchas variables o características).

### Problemas asociados a la alta dimensionalidad

- **Dispersión de datos:** a medida que aumenta el número de dimensiones, los datos tienden a "esparcirse" en el espacio, haciendo que las nociones de distancia y densidad pierdan significado.
- **Difícil interpretación y visualización:** los seres humanos no podemos visualizar directamente más de 3 dimensiones.
- **Mayor complejidad computacional:** los algoritmos suelen requerir más recursos (tiempo y memoria) a medida que crece el número de variables.

### Pregunta central

El enfoque principal que motiva estas técnicas es: **¿cómo determinar el número óptimo de dimensiones para representar un conjunto de datos, sin perder la información relevante?**

### Estrategias de reducción de dimensionalidad mencionadas

- **Análisis de Componentes Principales (PCA)** — el foco central de este documento.
- **Análisis Discriminante Lineal (LDA).**
- **T-Distributed Stochastic Neighbor Embedding (t-SNE)** — también desarrollado en la segunda mitad del documento.
- Otras técnicas relevantes no detalladas.

### Objetivos de PCA

PCA es presentado como una **herramienta para el análisis de datos en alta dimensión**, que permite **reducir el número de dimensiones manteniendo la información relevante**. Sus aplicaciones incluyen:

- **Compresión de datos** sin pérdida significativa de información.
- **Eliminación de redundancias** en imágenes y selección de características.
- **Descripción de regiones independiente de la rotación** del objeto o escena.

Se ilustra este punto con el dataset clásico _Iris_ de scikit-learn, un ejemplo estándar de cómo PCA puede usarse para explorar visualmente conjuntos de datos multivariados.

---

## 2. Conceptos básicos: varianza, covarianza y matriz de covarianza

Antes de definir PCA formalmente, el documento repasa las herramientas estadísticas necesarias para entenderlo.

### 2.1 Varianza

La **varianza** mide qué tan dispersos están los valores de una variable respecto a su media:

```
var(x) = σx² = (1/n) · Σ(xi − μx)²
```

### 2.2 Covarianza

La **covarianza** representa la tasa de cambio conjunta entre dos variables aleatorias:

```
Cov(x, y) = (1/n) · Σ(xi − μx)(yi − μy)
```

El documento incluye una figura con tres nubes de puntos que ilustran los tres casos posibles:

- **Cov(x, y) < 0:** cuando una variable aumenta, la otra tiende a disminuir (relación inversa).
- **Cov(x, y) = 0:** no existe relación lineal aparente entre las variables.
- **Cov(x, y) > 0:** ambas variables tienden a aumentar o disminuir juntas (relación directa).

### 2.3 Matriz de covarianza

Dado un vector de variables aleatorias x = {x₁, ..., xₙ}, la **matriz de covarianza** Cx es una matriz N×N donde cada elemento cᵢⱼ corresponde a la covarianza entre las variables i y j. Por ejemplo, para un vector con tres variables x = {x, y, z}:

```
       [ σx²        Cov(x,y)   Cov(x,z) ]
Cx  =  [ Cov(x,y)   σy²        Cov(y,z) ]
       [ Cov(x,z)   Cov(y,z)   σz²      ]
```

Propiedades importantes:

- **Cx es una matriz simétrica** (porque Cov(x,y) = Cov(y,x)).
- La diagonal contiene las varianzas individuales de cada variable, ya que Cov(x, x) = σx².
- También puede definirse de forma matricial equivalente como:

```
Cx = E[(x − μx)(x − μx)ᵀ] = (1/n) · Σ(xₖxₖᵀ − μxμxᵀ)
```

### 2.4 Vectores y valores propios

Este es el concepto matemático central sobre el cual se construye PCA.

**Definición:** dada una transformación lineal A y un vector x distinto de cero, x es un **vector propio (eigenvector)** de esa transformación si cumple:

```
Ax = λx
```

donde **λ (lambda)** es un **valor propio (eigenvalue)** escalar asociado a ese vector propio. Es decir, cuando la transformación A se aplica sobre su vector propio, el resultado es el mismo vector simplemente **escalado** por λ, sin cambiar de dirección.

**Ejemplo numérico del documento:**

- Un vector "no propio": al aplicar la matriz `[[3,1],[1,2]]` sobre el vector `[1,1]`, se obtiene `[4,3]`, que **no** es un múltiplo escalar del vector original (cambió de dirección).
- Un vector "propio": al aplicar la misma matriz sobre el vector `[1,1]` (en otro ejemplo con valores ajustados), se obtiene `[4,4] = 4·[1,1]`, es decir, el resultado sí es un múltiplo escalar (λ=4) del vector original — su dirección no cambia, solo su magnitud.

Para el ejemplo geométrico desarrollado con la matriz `[[3,1],[1,2]]`, se obtienen dos pares (valor propio, vector propio):

- λ₁ = 3,61 con vector propio ≈ [−0,85; 0,52]
- λ₂ = 1,36 con vector propio ≈ [0,52; −0,85]

### 2.5 Propiedades de los vectores y valores propios

- Los valores y vectores propios **siempre vienen en pares**.
- Solo existen para **matrices cuadradas**.
- Requieren que las filas sean **linealmente independientes** (relacionado con el rango de la matriz).
- Los **vectores propios de una matriz de transformación simétrica son ortogonales entre sí**.
- Los vectores propios representan los **ejes del nuevo espacio** que genera la transformación.
- Se **normalizan** para generar un espacio ortogonal (es decir, se convierten en vectores de longitud 1).
- Calcular vectores propios se vuelve **computacionalmente costoso** para matrices de alta dimensionalidad.
- Existen métodos iterativos especializados para su cálculo (método QR, método de la potencia, entre otros), implementados y optimizados en librerías como **NumPy**, **SciPy** y programas como **MATLAB**.

---

## 3. Análisis de Componentes Principales (PCA)

### 3.1 Definición formal

PCA se define como una **transformación lineal ortogonal** que mapea los datos originales a un nuevo sistema de coordenadas, de tal forma que:

- La **mayor varianza** de cualquier proyección de los datos se encuentra en la **primera componente principal (PC1)**.
- La **segunda mayor varianza** se encuentra en la **segunda componente (PC2)**.
- Y así sucesivamente para las componentes restantes.

### 3.2 Formulación matemática

PCA transforma un vector original x = [x₁, x₂, ..., xN] en un nuevo vector y mediante:

```
y = A(x − μx)
```

donde:

- **μx** es el vector de medias de los datos originales.
- **A** es la matriz cuyas filas son los **vectores propios** de la matriz de covarianza Cx, **ordenados de mayor a menor** según su valor propio asociado.

Como Cx es simétrica y real, se garantiza matemáticamente la existencia de N vectores propios ortogonales entre sí (Noble and Daniels, 1988).

### 3.3 Reconstrucción de los datos originales

Como los vectores de A son ortogonales, se cumple que A⁻¹ = Aᵀ, por lo que es posible recuperar x a partir de y de forma exacta:

```
x = Aᵀy + μx
```

Sin embargo, la utilidad práctica de PCA está en la **reducción de dimensionalidad**: si se forma una matriz reducida **Aₖ**, usando solo los **k** vectores propios con mayores valores propios (con k < N), la transformación resultante es de orden k×N, y los vectores y resultantes tienen longitud k (en lugar de N). En este caso, la reconstrucción será **inexacta** (aproximada):

```
x̂ = Aₖᵀy + μx
```

### 3.4 Error de reconstrucción (MSE)

El **error cuadrático medio (MSE)** entre los datos reconstruidos x̂ y los datos originales x está dado por la suma de los valores propios **descartados** (los que no se usaron en la reconstrucción):

```
MSE = Σⱼ λⱼ (j=1 a n) − Σⱼ λⱼ (j=1 a k)
```

donde λ = λ₁, ..., λₙ corresponde al conjunto completo de valores propios, ordenados de mayor a menor. Esto tiene una interpretación intuitiva muy importante: **cuanto mayor sea la suma de los valores propios que se descartan al reducir la dimensionalidad, mayor será el error de reconstrucción**. Por eso PCA prioriza conservar las componentes con los valores propios más grandes, ya que estas son las que más contribuyen a explicar la varianza (y por tanto la información) de los datos originales.

---

## 4. Ejemplo paso a paso para calcular PCA

El documento desarrolla un ejemplo completo y didáctico, usando datos sintéticos generados a partir de una distribución normal multivariante con 3 características, definida por:

```
μx1 = [10, 10, 10]

       [ 3,5   −1,6  −1,6 ]
Cx1 =  [ −1,6   3,5  −1,6 ]
       [ −1,6  −1,6   3,5 ]
```

Se generan **1000 muestras** con dimensión 1000×3.

### Paso 1: Restar la media (centrar / estandarizar)

Al restar μx a los datos, se **centra el espacio en las medias**, de modo que la media de los datos estandarizados queda en cero (μx = E[x] = 0). El documento muestra dos gráficos de dispersión comparando los "Datos Originales" (centrados alrededor de valores cercanos a 10) versus los "Datos estandarizados" (centrados en 0), confirmando visualmente el efecto de este paso.

### Paso 2: Calcular la matriz de covarianza

A partir de los datos, se calcula empíricamente:

```
      [  1,0    −0,47   −0,42 ]
Cx =  [ −0,47    1,0    −0,48 ]
      [ −0,42   −0,48    1,0  ]
```

### Paso 3: Calcular valores y vectores propios de la matriz de covarianza

Se obtienen tres pares de valores y vectores propios (inicialmente en un orden arbitrario):

```
eigval = [5,1;  0,3;  5,1]
```

y luego se **ordenan de forma descendente** según el valor propio, de modo que el valor propio más grande corresponde a la **primera componente principal (PC1)**:

```
eigval = [5,1;  5,1;  0,3]
```

Puntos clave de este paso:

- El **número de vectores propios es igual al número de características** originales del dataset.
- **Cada vector propio representa una dirección de variabilidad** en el espacio de los datos.

### Paso 4: Selección del número de componentes y cálculo de la varianza

Se inspecciona la **varianza explicada por cada componente** (proporcional a su valor propio), obteniendo en este ejemplo:

```
varianza = [0,48;  0,48;  0,02]
```

El documento incluye un gráfico de "Varianza vs. Número de componentes", que muestra cómo la varianza acumulada explicada crece rápidamente con las primeras componentes y luego se satura. En este ejemplo, se decide **conservar 2 de las 3 componentes** (los dos primeros vectores propios), ya que juntas explican el 96% de la varianza total (0,48+0,48), dejando fuera solo el 2% restante.

### Paso 5: Transformar los datos usando los vectores propios

Se calcula el **producto punto** entre los vectores propios seleccionados y los datos originales (centrados), obteniendo así la representación transformada de los datos en el nuevo espacio de menor dimensión (por ejemplo, PC1 y PC2).

### Paso 6: Recuperar los datos originales a partir de la representación reducida

El documento presenta tres visualizaciones lado a lado:

1. **Datos originales:** la nube de puntos en el espacio de características originales (Característica 1 vs. Característica 2).
2. **Datos transformados:** la misma nube de puntos proyectada en el nuevo espacio de componentes principales (PC1 vs. PC2).
3. **Datos reconstruidos (n_comp = 2), MSE = 0,11:** los datos originales reconstruidos a partir de solo 2 componentes, mostrando visualmente que la reconstrucción es muy similar a los datos originales, con un error cuadrático medio bajo (0,11), consistente con haber descartado solo la componente con menor valor propio (la que aportaba apenas 0,02 de varianza).

Finalmente, se incluye una **visualización 3D** de los datos después de restar la media, mostrando simultáneamente las tres características originales (Característica 1, 2 y 3) junto con las direcciones de PC1, PC2 y PC3 superpuestas sobre la nube de puntos, ilustrando geométricamente cómo los ejes de las componentes principales se alinean con las direcciones de mayor variabilidad de los datos.

---

## 5. Aplicación de PCA: Eigenfaces

Una de las aplicaciones clásicas y más ilustrativas de PCA en el estado del arte es la técnica de **Eigenfaces**, usada históricamente en reconocimiento facial.

### 5.1 Dataset

Se utiliza el **dataset ATT**, compuesto por **400 imágenes de rostros** con dimensión de **128×128 píxeles** cada una (es decir, cada imagen es un vector de 16.384 dimensiones antes de aplicar PCA).

### 5.2 ¿Qué son las Eigenfaces?

Al calcular la matriz de covarianza del conjunto de imágenes de rostros y obtener sus vectores propios, estos vectores propios —cuando se reinterpretan como imágenes— tienen una apariencia de **rostros borrosos**, y por eso reciben el nombre de **"Eigenfaces"**.

- **Eigenfaces con valores propios más altos:** el documento muestra 6 eigenfaces (de un total de 200) correspondientes a los valores propios más grandes. Estas imágenes muestran patrones faciales reconocibles y borrosos, ya que **la mayor parte de la información del conjunto de datos está contenida en las eigenfaces con mayores valores propios asociados**.
- **Eigenfaces con valores propios más bajos:** en contraste, se muestran eigenfaces asociadas a los valores propios más pequeños (aunque mayores a cero), las cuales tienen una apariencia de **ruido puro**, sin ningún patrón facial reconocible. Estas pueden considerarse como **ruido desde el punto de vista de clasificación**, ya que aportan muy poca información útil.

### 5.3 Varianza explicada en el dataset de rostros

Se presentan dos gráficos de "Varianza vs. Número de componentes" (uno con escala hasta 10.000 componentes y otro con zoom hasta 200 componentes), ambos mostrando el patrón típico de PCA: la varianza acumulada crece muy rápidamente con las primeras componentes y luego se **satura**, acercándose asintóticamente a 1.0 (100% de la varianza). Esto confirma el mensaje central: **usando pocas componentes principales se pueden obtener buenos resultados en problemas de clasificación**, ya que la mayoría de la información relevante está concentrada en un número reducido de componentes.

### 5.4 Reconstrucción de rostros con distinto número de componentes

Se muestra una comparación visual de:

- La **media** de los rostros (μx) y los primeros 4 vectores propios (A₁, A₂, A₃, A₄), junto con un vector propio de orden alto (A₁₀₀), que como se esperaba, se ve como ruido.
- La **reconstrucción de un rostro individual** (xᵢ) usando distintos números de componentes: **50, 100 y 200**. A medida que aumenta el número de componentes usadas en la reconstrucción, la imagen reconstruida se vuelve progresivamente más nítida y fiel al rostro original, ilustrando el trade-off entre compresión (menos componentes) y fidelidad de la reconstrucción (más componentes).

### 5.5 Conclusiones de PCA

El documento cierra esta sección con un resumen de puntos clave:

- PCA es una **transformación lineal ortogonal**, catalogada como una **técnica de aprendizaje no supervisado**.
- Es posible **reconstruir los datos originales** (de forma aproximada) a partir de los datos transformados.
- El **Algoritmo Hebbiano Generalizado (GHA)** es mencionado como un método **adaptativo** para realizar PCA **sin necesidad de calcular explícitamente los valores y vectores propios**, aprendiendo, por ejemplo, solo 8 componentes sin tener que calcular el resto.
- Las características obtenidas mediante PCA pueden usarse como **entrada (features) para alimentar otros algoritmos y modelos** de aprendizaje automático, orientados a resolver problemas de regresión y clasificación.

---

## 6. t-SNE (t-distributed Stochastic Neighbor Embedding)

La segunda mitad del documento presenta **t-SNE**, otra técnica de reducción de dimensionalidad, pero con un enfoque y propósito distinto al de PCA.

### 6.1 Origen y propósito

t-SNE fue desarrollado por **Laurens van der Maaten y Geoffrey Hinton en 2008**. Es una herramienta **específicamente diseñada para la visualización y exploración de datos de alta dimensionalidad**.

### 6.2 Diferencias clave respecto a PCA

- **Preservación de estructura local:** t-SNE intenta conservar la estructura local de los datos — es decir, la vecindad de baja dimensión (tras la reducción) debe ser lo más parecida posible a la vecindad original en alta dimensión. Esto **no necesariamente ocurre con PCA**, que se enfoca en preservar la varianza global, no las relaciones locales de vecindad.
- **Separación no lineal:** a diferencia de PCA (que es una transformación estrictamente lineal), **t-SNE permite separar datos que no pueden separarse linealmente**, gracias a que es un método no lineal.
- **Uso casi exclusivo para visualización:** a diferencia de PCA, t-SNE **casi solo se utiliza para visualización**, y **no es fácil integrar nuevos puntos de datos** una vez calculada la proyección (es decir, no es directamente aplicable a datos nuevos como sí lo es PCA mediante la matriz de transformación A).

### 6.3 Comparación visual: PCA vs. t-SNE en el dataset MNIST

El documento incluye una comparación muy ilustrativa usando el dataset **MNIST** (imágenes de dígitos manuscritos del 0 al 9):

- **PCA 2D para MNIST:** al proyectar los dígitos a solo 2 dimensiones usando PCA, se observa una nube de puntos donde los distintos dígitos (representados por colores) están **mezclados y con fronteras difusas** entre clases, aunque se aprecian algunas agrupaciones parciales (por ejemplo, el color naranja se agrupa más hacia un extremo).
- **t-SNE 2D para MNIST:** al aplicar t-SNE, los mismos dígitos se separan en **clusters mucho más claros y compactos**, con fronteras bien definidas entre los distintos dígitos. Esto ilustra de forma muy directa la principal ventaja de t-SNE sobre PCA para tareas de **visualización exploratoria**: al ser no lineal y enfocarse en preservar relaciones de vecindad local, logra revelar la estructura de clústeres subyacente de forma mucho más nítida que una proyección puramente lineal como PCA.

### 6.4 Fundamento de SNE (Stochastic Neighbor Embedding)

t-SNE se basa en el método SNE original. El nombre se descompone en dos ideas:

- **Stochastic (estocástico):** la función objetivo que optimiza el algoritmo **no es convexa**, lo que significa que los resultados pueden variar según la inicialización aleatoria del algoritmo (no siempre converge a la misma solución).
- **Neighbor Embedding (incrustación de vecinos):** el objetivo es mapear los puntos del espacio original de alta dimensión hacia un espacio de baja dimensión, **preservando al máximo la estructura de vecindad** de los datos.

### 6.5 Pasos generales del algoritmo SNE

1. Calcular la **probabilidad** de que un punto considere a otro como vecino, en el **espacio original de alta dimensión**.
2. Colocar los puntos en un **espacio reducido** (2D o 3D) y definir probabilidades de vecindad también allí.
3. **Comparar ambas distribuciones** de vecindades: los puntos que eran cercanos en el espacio original deben seguir siéndolo en el espacio reducido, y los que eran lejanos deben mantenerse separados.
4. **Ajustar iterativamente** las posiciones en el espacio reducido: los puntos cercanos se atraen entre sí, y los puntos lejanos se repelen, hasta lograr una configuración estable.

### 6.6 Idea básica y medición de distancia entre distribuciones

- t-SNE codifica la información de vecindad de alta dimensión como una **distribución de probabilidad**.
- La intuición se puede pensar como un **recorrido aleatorio** entre puntos de datos: existe una **alta probabilidad de saltar o conectar** con un punto cercano.
- t-SNE calcula la **distancia euclidiana** entre cada par de puntos en el espacio original de alta dimensión, y a partir de esas distancias construye una distribución de probabilidad que mide la **similitud** entre los puntos (los puntos más cercanos tienen mayor probabilidad de ser considerados vecinos).
- Para medir qué tan distintas son la distribución de vecindad en el espacio original y en el espacio reducido, se utiliza la **divergencia de Kullback-Leibler (KL)**, una medida estándar para cuantificar la diferencia entre dos distribuciones de probabilidad. En t-SNE, la divergencia KL se usa como **función de costo** a minimizar durante la optimización.

### 6.7 Intuición general de t-SNE

- El objetivo es tomar un conjunto de datos en un espacio de alta dimensión y encontrar una representación de esos mismos puntos en un espacio de dimensión inferior, típicamente un plano 2D.
- El algoritmo **no es lineal** y se adapta a los datos subyacentes, realizando **diferentes transformaciones en distintas regiones** del espacio — esta flexibilidad, aunque poderosa, puede ser también **una fuente importante de confusión** al interpretar los resultados (por ejemplo, las distancias entre clústeres en el resultado de t-SNE no siempre tienen un significado cuantitativo directo).

### 6.8 El hiperparámetro Perplexity

t-SNE posee un parámetro ajustable llamado **perplexity**, que representa un **equilibrio entre los aspectos locales y globales** de los datos. Conceptualmente, es una **suposición sobre el número de vecinos cercanos** que tiene cada punto, y puede interpretarse como un **trade-off entre preservar la estructura local o global** en la representación reducida.

**Valores recomendados por los autores originales:** entre **5 y 50**.

- **Perplexity ajusta el ancho de la distribución gaussiana** utilizada para calcular la similitud de cada punto con sus vecinos.
- **Valores bajos de perplexity (ej. 5-10):** el algoritmo se enfoca en vecinos muy cercanos, detectando relaciones en patrones locales muy finos.
- **Valores altos de perplexity (ej. 30-50):** permiten abarcar un mayor rango de vecinos, ayudando a capturar estructuras de mayor escala (patrones globales) en los datos.

### 6.9 Otros hiperparámetros de t-SNE

- **Tasa de aprendizaje (learning rate):** controla el tamaño de los pasos de optimización. Un valor bajo puede llevar a una convergencia lenta. Valores recomendados: **10 a 1000**.
- **Número de iteraciones:** por lo general, entre **250 y 5000** iteraciones.
- **Dimensionalidad de salida:** el espacio objetivo de la proyección, típicamente **2D o 3D**.

### 6.10 Requisitos prácticos y comportamiento inesperado

- Para asegurar el correcto funcionamiento del algoritmo, el valor de **perplexity debe ser menor que el número de puntos** en el dataset; en caso contrario, las implementaciones pueden comportarse de forma inesperada.
- Para valores de perplexity **fuera del rango recomendado** por los autores (5-50), los gráficos resultantes también pueden tener comportamientos inesperados o poco interpretables.

### 6.11 Ejemplo visual: efecto del parámetro Perplexity

El documento incluye una figura (basada en el artículo interactivo "How to Use t-SNE Effectively", distill.pub, 2016) que muestra el mismo conjunto de datos sintético (dos grupos de puntos, en azul y naranja) proyectado con t-SNE usando **distintos valores de perplexity: 2, 5, 30, 50 y 100**. Se observa cómo:

- Con **perplexity muy baja (2)**, los datos se fragmentan en múltiples grupos pequeños y dispersos, sin una estructura clara.
- Con valores **intermedios (5-30)**, comienzan a aparecer agrupaciones más coherentes.
- Con **perplexity más alta (50-100)**, los dos grupos originales tienden a mostrarse de forma más compacta y diferenciada, aunque con formas distintas entre ejecuciones.

Esta figura refuerza el mensaje central: **la variación del parámetro perplexity puede dar lugar a visualizaciones drásticamente distintas que muestran estructuras diferentes**, por lo que interpretar un resultado de t-SNE sin explorar varios valores de perplexity puede llevar a conclusiones engañosas sobre la verdadera estructura de los datos.

### 6.12 Desventajas de t-SNE

- **No es determinista:** no siempre produce resultados similares en ejecuciones sucesivas (a diferencia de PCA, que sí es determinista).
- **Requiere sintonización de hiperparámetros** relacionados con el proceso de optimización (perplexity, tasa de aprendizaje, número de iteraciones).
- Como consecuencia de ambos puntos anteriores, t-SNE se usa **principalmente para visualizar datos**, y **no para alimentar modelos de aprendizaje automático** (a diferencia de PCA, cuyas componentes sí se usan frecuentemente como features de entrada para otros modelos).

### 6.13 Limitaciones adicionales de t-SNE

- **No funciona bien para reducción de dimensionalidad general** cuando la dimensión objetivo de la representación es superior a 2D o 3D (a diferencia de PCA, que puede reducir a cualquier número de dimensiones k).
- También sufre de la **maldición de la dimensionalidad**, ya que t-SNE emplea distancias euclidianas entre vecinos cercanos, las cuales pierden significado en espacios de muy alta dimensión.
- Múltiples hiperparámetros (perplexity, número de iteraciones, entre otros) **deben elegirse manualmente**, sin una forma automática y universal de determinarlos.

---

## 7. Representaciones 2D y 3D de datasets públicos

La última sección del documento presenta ejemplos de proyecciones t-SNE aplicadas a dos datasets reales conocidos, extraídos de la página oficial de Laurens van der Maaten (creador de t-SNE):

### 7.1 Dataset Olivetti

Muestra una proyección t-SNE en 2D de un conjunto de **imágenes de rostros** (dataset Olivetti), donde cada punto del gráfico de dispersión está representado directamente por una **miniatura de la imagen del rostro correspondiente**, en lugar de un punto genérico. Esto permite apreciar visualmente cómo t-SNE agrupa rostros similares (misma persona, poses o expresiones similares) en regiones cercanas del espacio 2D reducido.

### 7.2 Dataset Netflix

Muestra una proyección t-SNE en 2D del catálogo de **películas y series de Netflix**, donde cada punto está etiquetado con el **título** de la obra correspondiente (en distintos colores). Los títulos que son temáticamente o narrativamente similares tienden a agruparse en regiones cercanas del espacio reducido, ilustrando cómo t-SNE puede usarse para explorar visualmente similitudes en catálogos de contenido a partir de sus características subyacentes (por ejemplo, género, actores, palabras clave, etc.).

### 7.3 Recurso adicional

El documento cierra remitiendo a la página oficial de Laurens van der Maaten (https://lvdmaaten.github.io/tsne/), que contiene detalles sobre implementaciones de t-SNE en distintos lenguajes de programación y más ejemplos de su aplicación a diversos conjuntos de datos.

---

## Resumen general del documento

Esta presentación desarrolla, de manera progresiva y con fuerte enfoque matemático y visual, dos de las técnicas más importantes de reducción de dimensionalidad en ciencia de datos:

1. **Fundamentos matemáticos:** varianza, covarianza, matriz de covarianza, y el concepto de vectores y valores propios, como base necesaria para entender PCA.
    
2. **PCA (Análisis de Componentes Principales):** una transformación lineal ortogonal que reordena los ejes del espacio de datos según la varianza que explican, permitiendo reducir dimensionalidad con una pérdida de información cuantificable (MSE) y reconstruir aproximadamente los datos originales. Se desarrolla un ejemplo numérico paso a paso completo (generación de datos, centrado, cálculo de covarianza, cálculo y selección de valores/vectores propios, transformación y reconstrucción), y se ilustra con la aplicación clásica de **Eigenfaces** para reconocimiento facial.
    
3. **t-SNE:** una técnica no lineal, estocástica y centrada exclusivamente en visualización, que preserva relaciones de vecindad local en lugar de varianza global, siendo capaz de revelar estructuras de clústeres mucho más claras que PCA (como se demuestra comparando ambas técnicas sobre el dataset MNIST), a costa de mayor costo computacional, falta de determinismo, y la necesidad de ajustar cuidadosamente hiperparámetros como **perplexity**.
    
4. **Ejemplos aplicados:** se cierra el documento con ejemplos reales de proyecciones t-SNE sobre datasets públicos (Olivetti y Netflix), mostrando el uso práctico de estas técnicas para la exploración visual de datos complejos de alta dimensión.
    

En conjunto, el documento ofrece una introducción completa —tanto teórica como práctica— a las dos técnicas de reducción de dimensionalidad más utilizadas en visualización y análisis exploratorio de datos, destacando cuándo conviene usar cada una según el objetivo (compresión y modelado con PCA, versus exploración visual con t-SNE).