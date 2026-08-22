# Resumen Base — EIN087B Ciencia de Datos
**Universidad Técnica Federico Santa María · Prof. Jorge Portilla G. · Concepción**

---

## Índice

1. [Introducción a la Ciencia de Datos](#1-introducción-a-la-ciencia-de-datos)
2. [Introducción a Machine Learning](#2-introducción-a-machine-learning)
3. [Procesamiento y Visualización de Datos](#3-procesamiento-y-visualización-de-datos)
4. [Regresión Lineal y Logística](#4-regresión-lineal-y-logística)
5. [Selección de Características](#5-selección-de-características)
6. [Métricas de Evaluación](#6-métricas-de-evaluación)

---

## 1. Introducción a la Ciencia de Datos

### El problema de la información

A lo largo del tiempo, la humanidad ha generado una cantidad de información que crece de forma exponencial. Este crecimiento hace cada vez más difícil almacenarla, procesarla y utilizarla de forma eficiente. Como respuesta surge la **Ciencia de Datos**, cuyo objetivo es organizar, gestionar y transformar grandes volúmenes de datos en conocimiento útil para la toma de decisiones.

### La Ley de Moore y sus límites

La Ley de Moore establece que el número de transistores en un microprocesador se duplica aproximadamente cada dos años, implicando un aumento proporcional en capacidad de procesamiento. Sin embargo, este crecimiento ha encontrado límites físicos — principalmente el calor generado al reducir el tamaño de los transistores — lo que ha impulsado nuevas estrategias como la **computación paralela** y arquitecturas más eficientes (GPUs, TPUs).

### El ecosistema de conceptos: IA, ML y Data Science

Estos tres conceptos están relacionados pero tienen enfoques distintos y forman una jerarquía:

**Inteligencia Artificial (IA):** el campo más amplio. Busca desarrollar sistemas capaces de simular capacidades humanas como el razonamiento, el aprendizaje y la toma de decisiones. No es inherentemente dependiente de datos en su concepto teórico, pero en la práctica todos los sistemas inteligentes modernos se construyen a partir de ellos.

**Machine Learning (Aprendizaje Automático):** una rama de la IA que se centra en algoritmos que aprenden a partir de datos sin necesidad de ser programados explícitamente para cada tarea. Los algoritmos ajustan parámetros internos con el objetivo de mejorar su desempeño en una tarea específica.

**Data Science (Ciencia de Datos):** campo interdisciplinario que combina estadística, informática y conocimiento del dominio para extraer conocimiento útil a partir de grandes volúmenes de datos, tanto estructurados (bases de datos) como no estructurados (texto, imágenes).

### Metodología CRISP-DM

CRISP-DM (Cross-Industry Standard Process for Data Mining) es la metodología estándar para proyectos de ciencia de datos. Define seis fases que forman un ciclo iterativo donde los resultados de fases posteriores pueden llevar de regreso a fases anteriores:

1. **Comprensión del negocio:** identificar el problema, definir la variable objetivo y establecer la estrategia.
2. **Comprensión de los datos:** analizar los datos disponibles, comunicarse con expertos del dominio.
3. **Preparación de los datos:** limpiar, transformar e integrar los datos para el modelado.
4. **Modelado:** seleccionar y aplicar algoritmos; ajustar hiperparámetros.
5. **Evaluación:** validar resultados, verificar que el modelo responde realmente el objetivo de negocio.
6. **Despliegue (Deployment):** llevar el modelo a producción. Incluye una flecha de retroalimentación de vuelta a la fase 1, porque el modelo en producción genera nueva información sobre si el problema sigue siendo el mismo.

### Habilidades necesarias en un Data Scientist

Un científico de datos necesita combinar cinco áreas: matemática y estadística, manipulación de datos, programación, conocimiento del dominio del problema y comunicación para explicar resultados a distintas audiencias.

---

## 2. Introducción a Machine Learning

### ¿Qué es aprender de datos?

El objetivo del ML es aprender una función `f` que relacione entradas con salidas a partir de datos observados. Los conceptos fundamentales son:

- **Features (X):** variables de entrada, numéricas o categóricas.
- **Variable objetivo (Y):** lo que se quiere predecir o estimar.
- **Función f:** la relación entre X e Y que el modelo aprende.
- **Hipótesis (H):** el conjunto de todas las posibles funciones que el algoritmo puede considerar.
- **Algoritmo de aprendizaje:** el método que busca dentro de H la función que mejor ajusta los datos, minimizando una función de costo.

### Tipos de aprendizaje

**Aprendizaje supervisado:** usa datos etiquetados — cada ejemplo tiene tanto la entrada X como la respuesta correcta Y. Se divide en **regresión** (Y continua) y **clasificación** (Y discreta).

**Aprendizaje no supervisado:** no usa etiquetas. El algoritmo busca patrones ocultos. Las tareas principales son **clustering** y **reducción de dimensionalidad**.

### Modelos paramétricos vs. no paramétricos

**Modelos paramétricos:** asumen una forma funcional específica. Son simples, eficientes y fáciles de interpretar, pero si la forma asumida no corresponde a la realidad, el modelo tendrá alto sesgo sin importar cuántos datos se usen.

**Modelos no paramétricos:** no asumen ninguna forma específica. Son más flexibles y pueden capturar relaciones complejas, pero requieren más datos y son más difíciles de interpretar.

### Inferencia vs. predicción

**Inferencia:** el objetivo es entender la relación entre variables. Se prefieren modelos interpretables.

**Predicción:** el objetivo es predecir valores futuros con la mayor precisión posible. Se aceptan modelos más complejos y menos interpretables.

### Generalización, Overfitting y Underfitting

**Generalización:** capacidad de un modelo de predecir correctamente datos nuevos no vistos durante el entrenamiento. Es el objetivo real del ML.

**Overfitting (sobreajuste):** el modelo memoriza los datos de entrenamiento — incluido el ruido — pero falla en datos nuevos. Ocurre cuando el modelo es demasiado complejo para la cantidad de datos disponibles.

**Underfitting (subajuste):** el modelo es demasiado simple para capturar los patrones reales. Falla tanto en entrenamiento como en prueba.

### El trade-off sesgo-varianza

**Sesgo (Bias):** error causado por suposiciones demasiado fuertes o un modelo demasiado simple. Un modelo con alto sesgo no captura los patrones relevantes independientemente de cuántos datos se tengan.

**Varianza:** sensibilidad excesiva a pequeñas variaciones en los datos de entrenamiento. Un modelo con alta varianza aprende el ruido específico del conjunto de entrenamiento y no generaliza.

La relación es inevitable: reducir el sesgo (usando modelos más complejos) tiende a aumentar la varianza, y viceversa. El objetivo es encontrar el punto de equilibrio donde el error total es mínimo.

### La maldición de la dimensionalidad

A medida que aumenta el número de features, el espacio de datos crece exponencialmente. Los datos disponibles se vuelven progresivamente más dispersos, las métricas de distancia pierden significado, y los modelos pierden capacidad de generalización. Este fenómeno justifica la importancia de la selección de características y la reducción de dimensionalidad.

### Precisión vs. interpretabilidad

Los modelos simples son muy interpretables pero pueden perder precisión en problemas complejos. Los modelos complejos son muy precisos pero funcionan como cajas negras. La elección depende del objetivo: si el modelo debe explicarse a reguladores o usuarios, la interpretabilidad puede ser más importante que la precisión máxima.

---

## 3. Procesamiento y Visualización de Datos

### Conceptos estadísticos fundamentales

**Variable:** característica o atributo medido en los datos.

**Distribución:** describe cómo se reparten los valores de una variable dentro de su rango posible.

**Observación:** un conjunto de valores registrados para una instancia — normalmente una fila en un dataset.

**Correlación:** relación entre dos variables que indica cómo cambian conjuntamente. Va de −1 a 1.

### Medidas de tendencia central y dispersión

**Media (promedio):** valor central de un conjunto de datos. Es sensible a outliers.

**Mediana:** valor que divide los datos en dos mitades iguales. Es robusta frente a outliers.

**Desviación estándar:** mide qué tan dispersos están los datos respecto a la media.

**Varianza:** el cuadrado de la desviación estándar. Matemáticamente conveniente pero menos interpretable directamente.

### Covarianza y correlación

**Covarianza:** mide cómo cambian dos variables juntas. Su magnitud depende de las unidades de medida.

- Covarianza positiva → ambas variables aumentan juntas.
- Covarianza negativa → una sube cuando la otra baja.
- Covarianza cercana a cero → no hay relación lineal clara.

**Correlación:** la covarianza normalizada por las desviaciones estándar de ambas variables. Queda en el rango [−1, 1] y es adimensional, lo que permite comparar directamente pares de variables con distintas escalas.

**Matriz de covarianza:** generaliza la covarianza a múltiples variables simultáneamente. Es cuadrada, simétrica, y su diagonal contiene las varianzas individuales de cada variable.

### Problemas comunes en los datos

- **Valores faltantes:** filas donde alguna variable no tiene valor registrado.
- **Registros duplicados:** filas idénticas que distorsionan el análisis.
- **Valores inconsistentes:** misma entidad con formatos distintos (ej. "Chile", "chile", "CL").
- **Ruido:** datos erróneos causados por errores de medición o captura.
- **Errores de formato:** fechas mal formateadas, números almacenados como texto.

### Manejo de valores faltantes

Eliminar filas con valores faltantes es la estrategia más simple, pero introduce un riesgo importante: si los datos faltantes no son completamente aleatorios — es decir, si hay un patrón en qué filas tienen valores ausentes — la eliminación puede sesgar el dataset hacia una subpoblación particular y hacer que el modelo no represente bien la realidad completa.

La alternativa es la **imputación**: reemplazar los valores faltantes con un valor estimado. Para variables numéricas, las opciones más comunes son la media (cuando la distribución es aproximadamente normal y no hay outliers extremos) y la mediana (más robusta en presencia de outliers). Para variables categóricas, se usa la **moda** — el valor más frecuente de esa variable. La mediana es preferible a la media cuando la distribución de la variable es asimétrica o contiene valores extremos, porque la media puede ser arrastrada significativamente por esos extremos mientras que la mediana permanece estable.

### Variables categóricas y Dummy Variables

Los algoritmos de ML requieren entradas numéricas y no pueden trabajar directamente con etiquetas de texto. Las **dummy variables** (o variables indicadoras) resuelven esto convirtiendo una variable categórica en múltiples columnas binarias (0/1), una por cada categoría. Por ejemplo, una columna "Género" con valores "Hombre"/"Mujer" se convierte en una columna "Género_Mujer" con valores 0 o 1.

Es importante usar el parámetro `drop_first=True` al crear dummies para evitar la **multicolinealidad perfecta**: si hay N categorías y se crean N columnas binarias, la última siempre puede deducirse de las demás (si todas son 0, la última es necesariamente 1), lo que hace la matriz de features singulares. Eliminar una de las columnas rompe esa redundancia perfecta sin perder información.

### Selección de filas con condiciones (loc vs. iloc)

En el análisis exploratorio es fundamental poder filtrar datos según condiciones lógicas. `loc` selecciona filas y columnas usando **etiquetas** del índice y permite aplicar condiciones booleanas (`df.loc[df["columna"] == valor]`). `iloc` selecciona usando **posiciones numéricas** (primera, segunda, tercera fila...). La diferencia importa cuando el índice del DataFrame no es el entero predeterminado: `loc[1]` siempre buscará la fila con etiqueta 1, mientras que `iloc[1]` siempre devolverá la segunda fila independientemente de su etiqueta.

### Discretización de variables continuas

La discretización convierte una variable continua (como la edad) en rangos o grupos categóricos (niños, adolescentes, adultos, etc.). Esto permite analizar comportamientos diferenciados entre grupos, aplicar condiciones lógicas más significativas y construir variables más interpretables. Una técnica común es `pd.cut()`, que asigna cada valor a un intervalo definido por los extremos de los rangos. La elección de los rangos debe estar guiada por el conocimiento del dominio.

### Normalización y estandarización

Muchos algoritmos de ML son sensibles a la escala de las variables. Una variable con rango [0, 1000] puede dominar a otra con rango [0, 1] aunque ambas sean igualmente informativas.

**Normalización Min-Max:** escala cada variable al rango [0, 1]: `X_norm = (X − min) / (max − min)`. Es útil cuando se conocen los límites naturales de la variable.

**Estandarización (Z-score):** `X_z = (X − media) / std`. Transforma los datos para que tengan media 0 y desviación estándar 1. Es el preprocesamiento estándar para algoritmos basados en distancias (KNN, SVM) y gradientes.

Cuando se aplica normalización sobre una **matriz** (múltiples variables simultáneamente), el parámetro `axis=0` indica que las estadísticas (mínimo, máximo, media, std) se calculan **por columna** — es decir, cada variable se normaliza según su propia distribución. Usar `axis=1` calcularía las estadísticas por fila, normalizando cada observación respecto a sus propios valores, lo que distorsionaría la interpretación y haría que los valores de distintas filas ya no fueran comparables entre sí.

Las **operaciones vectorizadas** sobre arrays de NumPy son significativamente más eficientes que los loops fila por fila porque se ejecutan en código compilado de bajo nivel (C/Fortran) que procesa grandes bloques de datos en memoria de forma continua, aprovechando optimizaciones del procesador. Un loop en Python agrega sobrecarga por cada iteración en el intérprete, lo que lo hace mucho más lento a medida que crece el dataset.

### Detección de outliers

**Z-score:** mide cuántas desviaciones estándar está un punto de la media. Puntos con |Z| > 3 suelen considerarse outliers. Funciona bien para distribuciones aproximadamente normales.

**Rango intercuartílico (IQR):** la distancia entre Q1 (25%) y Q3 (75%). Valores fuera de `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]` se consideran atípicos. Más robusto que el Z-score porque no depende de la media.

**Métodos basados en densidad (DBSCAN):** identifican como outliers los puntos con muy pocos vecinos cercanos en el espacio de features.

**Isolation Forest:** aísla puntos construyendo árboles aleatorios. Los outliers son más fáciles de aislar (requieren menos divisiones) y reciben puntuaciones de anomalía más altas.

### El Boxplot

Herramienta gráfica que resume visualmente la distribución de una variable en cinco números: mínimo no atípico, Q1, mediana, Q3 y máximo no atípico. Los outliers aparecen como puntos individuales más allá de los bigotes. Permite comparar distribuciones de múltiples variables o grupos de forma compacta.

### Distribuciones importantes

**Gaussiana (normal):** forma de campana simétrica alrededor de la media. Muchos fenómenos naturales la siguen aproximadamente, y muchos algoritmos asumen implícitamente normalidad en los errores.

**Uniforme:** todos los valores dentro de un intervalo tienen exactamente la misma probabilidad.

**Binomial:** modela el número de éxitos en una serie de ensayos independientes con dos posibles resultados y probabilidad de éxito constante. Es una extensión de la distribución de Bernoulli (un solo ensayo) a múltiples ensayos.

### Análisis exploratorio: gráficos y su interpretación

El **scatter plot (gráfico de dispersión)** entre dos variables continuas permite detectar visualmente si existe una relación lineal o no lineal entre ellas, si hay outliers extremos, y si la relación es homogénea en todo el rango o solo en ciertos tramos. En el contexto de regresión, un scatter plot entre la variable independiente y la dependiente es el primer paso para validar que la suposición de linealidad es razonable.

El **mapa de calor de la matriz de correlación** muestra simultáneamente la correlación entre todos los pares de variables del dataset. Valores cercanos a 1 o −1 (colores intensos) indican relaciones fuertes; valores cercanos a 0 (colores claros) indican ausencia de relación lineal. Este gráfico permite identificar de un vistazo qué variables están más relacionadas con el objetivo y qué pares de variables son redundantes entre sí (alta correlación mutua).

El **gráfico de la línea de regresión** superpone la recta ajustada sobre los datos observados. La pendiente de esa recta es el coeficiente β₁ del modelo — indica cuánto cambia Y por cada unidad de X. Si los puntos se distribuyen aleatoriamente alrededor de la línea sin un patrón sistemático, el modelo lineal es apropiado. Si hay una curvatura sistemática (los residuos forman un arco o un patrón), sugiere que la relación no es lineal y puede ser necesario transformar las variables.

El **gráfico de predicción vs. valor real** compara en un scatter plot lo que el modelo predijo (eje Y) contra lo que realmente ocurrió (eje X). Un modelo perfecto produce todos los puntos sobre la diagonal y = x. Puntos que se desvían sistemáticamente en alguna zona (por ejemplo, el modelo sobreestima sistemáticamente los valores bajos y subestima los altos) revelan sesgos estructurales que las métricas numéricas pueden enmascarar.

El **boxplot de métricas de validación cruzada** muestra la distribución de los resultados a través de los K pliegues. Una caja angosta indica que el modelo es estable y consistente entre pliegues; una caja amplia o con outliers indica alta varianza en el desempeño, lo que puede señalar que el modelo es sensible a qué datos específicos quedan en entrenamiento y cuáles en prueba. Esta variabilidad es una señal de advertencia sobre la confiabilidad de la estimación promedio.

### CPU vs. GPU para procesamiento de datos

La CPU (Central Processing Unit) tiene pocos núcleos potentes optimizados para tareas secuenciales y lógica compleja. La GPU (Graphics Processing Unit) tiene miles de núcleos simples diseñados para ejecutar la misma operación sobre muchos datos simultáneamente — esto es el paralelismo masivo.

En ciencia de datos, **pandas** ejecuta las operaciones en CPU. **cuDF** (del ecosistema RAPIDS de NVIDIA) ofrece una API casi idéntica a pandas pero ejecuta las operaciones en GPU. Las operaciones que más se benefician del paralelismo de la GPU son las que tienen estructura regular y pueden vectorizarse: filtrado, groupby y joins sobre millones de filas.

Sin embargo, la GPU no siempre es más rápida. En datasets pequeños, el costo de **transferir datos entre la memoria RAM (CPU) y la VRAM (GPU)** puede superar los beneficios del paralelismo. Además, la VRAM de la GPU es significativamente menor que la RAM del sistema, lo que limita el tamaño del dataset que puede procesarse completamente en GPU. Las operaciones que dependen de lógica Python arbitraria o funciones personalizadas complejas no pueden ejecutarse en GPU y tampoco se benefician de cuDF.

La **cardinalidad** de una columna (número de valores únicos) afecta directamente el costo de operaciones como groupby: mayor cardinalidad implica más grupos que gestionar, lo que puede reducir la ventaja de la GPU en esa operación específica.

---

## 4. Regresión Lineal y Logística

### ¿Qué hace una regresión?

Modela la relación entre una variable dependiente Y (lo que se quiere predecir) y una o más variables independientes X (lo que se usa para predecir). En la realidad no se conoce la función exacta que relaciona X con Y, y el objetivo es aproximarla a partir de datos observados.

### Modelo lineal

`f(x) = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ`

- `β₀` es el intercepto: el valor base cuando todas las variables son 0.
- `βᵢ` indica cuánto cambia Y cuando Xᵢ aumenta en una unidad, manteniendo todo lo demás constante.

En forma matricial: `f(X) = βᵀX`. Se llama "lineal" porque es una combinación lineal de las variables, no porque necesariamente produzca una recta en los datos.

### Función de costo

`J(β) = ½ Σ (f(xₘ) − yₘ)²`

Mide qué tan mal lo está haciendo el modelo. El cuadrado hace que los errores positivos y negativos no se cancelen, y que los errores grandes sean penalizados más que los pequeños.

### Solución analítica (Ecuación Normal)

`β = (XᵀX)⁻¹ XᵀY`

Calcula directamente los coeficientes óptimos. El problema es que requiere invertir la matriz XᵀX, lo que es costoso computacionalmente para datasets grandes (escala O(n³)) y puede no existir si hay multicolinealidad perfecta.

### Descenso del Gradiente

`β ← β − α · ∂J/∂β`

Donde `α` es la **tasa de aprendizaje**. Si α es muy grande el algoritmo puede divergir; si es muy pequeño converge muy lentamente. El gradiente para cada coeficiente es `∂J/∂βᵢ = (f(x) − y) · xᵢ`: si el error es grande, el ajuste es grande; si la variable xᵢ es muy influyente, su coeficiente recibe mayor actualización.

Tres variantes: **Batch** (todos los datos, más estable), **SGD** (un ejemplo a la vez, más rápido pero ruidoso), **Mini-batch** (subconjunto pequeño, compromiso estándar en deep learning).

### Multicolinealidad

Ocurre cuando dos o más variables de entrada están altamente correlacionadas entre sí. La matriz XᵀX se vuelve casi singular y los coeficientes se vuelven inestables. No afecta la capacidad predictiva del modelo, pero sí destruye la interpretabilidad de los coeficientes individuales.

Una variable puede parecer muy relevante cuando se analiza sola (alta correlación con el objetivo, alto F-score), pero dejar de ser estadísticamente significativa dentro de un modelo multivariado porque otra variable ya captura la misma información. Esto explica por qué los métodos filter (que evalúan variables individualmente) y los métodos OLS (que evalúan la contribución condicionada a las demás variables) pueden dar rankings distintos.

### p-values y significancia estadística en OLS

OLS (Ordinary Least Squares) no solo ajusta los coeficientes sino que también entrega un **p-value** para cada uno, que mide la probabilidad de observar un coeficiente tan grande como el encontrado si en realidad esa variable no tuviera ningún efecto sobre Y. Un p-value < 0.05 indica que la variable es **estadísticamente significativa** — su efecto probablemente no es producto del azar — condicionado a la presencia de las demás variables en el modelo.

El **Condition Number** del modelo OLS es un indicador de multicolinealidad. Un valor alto (> 30, y especialmente > 1000) indica que la matriz de features está mal condicionada — pequeñas variaciones en los datos producen grandes cambios en los coeficientes — lo que señala un problema serio de multicolinealidad que puede requerir eliminar variables o aplicar regularización.

### Regularización

Técnica para controlar el sobreajuste añadiendo una penalización a la función de costo:

**Ridge (L2):** `J = Error + λ Σ βᵢ²`. Reduce todos los coeficientes hacia cero pero nunca los hace exactamente cero. Es ideal cuando hay muchas variables correlacionadas porque distribuye el peso entre ellas. Al comparar los coeficientes de regresión lineal ordinaria vs. Ridge, los de Ridge siempre tendrán menor magnitud, pero ninguno llegará a cero.

**Lasso (L1):** `J = Error + λ Σ |βᵢ|`. Puede llevar coeficientes exactamente a cero, realizando **selección automática de variables**. Es especialmente útil cuando se sospecha que solo unas pocas variables son realmente importantes y el resto son ruido. Las variables que Lasso elimina (coeficiente = 0) tienden a coincidir con variables que otros métodos también identifican como de baja importancia, aunque no siempre: el contexto de todas las variables juntas puede cambiar qué se considera redundante.

El parámetro **α** (o λ) controla la intensidad de la regularización. α = 0 es regresión sin regularización; α muy grande hace todos los coeficientes cercanos a cero. El valor óptimo de α generalmente difiere entre Ridge y Lasso porque las penalizaciones tienen escalas efectivas distintas — L1 actúa más agresivamente sobre los coeficientes pequeños y requiere valores de α más pequeños para lograr el mismo nivel de regularización que L2.

### Diagnóstico del modelo: QQ Plot

Para validar que un modelo de regresión es estadísticamente confiable, se analiza la distribución de los **residuos**. El supuesto fundamental es que los residuos siguen una distribución normal.

El **QQ Plot** grafica los cuantiles de los residuos observados contra los cuantiles teóricos de una distribución normal. Si los puntos siguen una línea recta diagonal, los residuos son normales y el modelo es estadísticamente válido. Desviaciones sistemáticas (curvas en los extremos, forma de S) indican no normalidad.

Un modelo podría mostrar un buen R² global pero tener errores grandes y sistemáticos en ciertos puntos específicos. Esto sugiere que el modelo funciona bien en promedio pero falla en subpoblaciones o rangos de valores concretos — una limitación que el R² solo no puede revelar y que requiere analizar los residuos individualmente.

### Métricas de regresión

**MSE (Mean Squared Error):** promedio de los errores al cuadrado. Penaliza fuertemente los errores grandes. La función `cross_val_score` de sklearn lo devuelve en negativo porque la convención de la biblioteca es que "mayor es mejor", y para el MSE menor es mejor, por lo que se niega para mantener la consistencia. Al interpretar los resultados hay que tomar el negativo del valor reportado.

**RMSE:** raíz cuadrada del MSE. Tiene las mismas unidades que la variable objetivo, facilitando la interpretación.

**R² (Coeficiente de Determinación):** mide qué proporción de la varianza total de Y es explicada por el modelo. Un modelo perfecto tiene R² = 1; un modelo que siempre predice la media tiene R² = 0. Puede ser negativo si el modelo es peor que predecir siempre la media.

Una alta variabilidad en los resultados de validación cruzada (los scores de distintos pliegues son muy distintos entre sí) indica que el modelo es inestable — su desempeño depende significativamente de qué datos específicos quedan en entrenamiento. Esto puede ser señal de sobreajuste, de insuficiente cantidad de datos, o de que el dataset tiene subpoblaciones muy distintas entre sí.

### Regresión Logística

La regresión lineal no funciona bien para clasificación porque puede predecir valores fuera del rango [0, 1]. La regresión logística aplica la **función sigmoide** a la combinación lineal:

`p = 1 / (1 + e^(−βᵀx))`

El resultado es siempre una probabilidad entre 0 y 1. Las propiedades clave de la función sigmoide: cuando z = 0 la probabilidad es exactamente 0.5 (punto de máxima incertidumbre); cuando z tiende a +∞ la probabilidad tiende a 1; cuando z tiende a −∞ tiende a 0. El umbral de clasificación estándar es 0.5, pero puede ajustarse según el costo relativo de los tipos de error.

**Entrenamiento por Log-Verosimilitud:** maximiza la probabilidad de observar los datos dados los parámetros. Para los ejemplos positivos (y=1) se maximiza log(p); para los negativos (y=0) se maximiza log(1−p). El gradiente tiene la misma forma que en regresión lineal: `∂ℓ/∂β = (y − f(x))·x`.

**Relación con redes neuronales:** la regresión logística es esencialmente una red neuronal de una sola capa sin capas ocultas. Las redes neuronales profundas son extensiones que apilan múltiples capas de estas transformaciones.

### Validación Cruzada

**Hold-out:** divide los datos en entrenamiento (ej. 80%) y prueba (20%). Simple pero sensible a cómo queden distribuidos los datos en la división.

**K-Fold Cross Validation:** divide el dataset en K partes iguales. El modelo se entrena K veces, usando cada vez un pliegue distinto como prueba. El error reportado es el promedio de los K resultados. Más robusto porque todos los datos participan tanto en entrenamiento como en evaluación. Es la estimación más confiable del error de generalización real porque minimiza el efecto del azar en la división específica.

---

## 5. Selección de Características

### ¿Por qué es necesaria?

Incluir demasiadas variables en un modelo no siempre mejora su desempeño. Las variables irrelevantes o redundantes pueden aumentar el sobreajuste, ralentizar el entrenamiento, dificultar la interpretación y agravar la maldición de la dimensionalidad.

### Categorías de métodos

#### Métodos de Filtro

Evalúan la relevancia de cada variable de forma independiente usando propiedades estadísticas — sin involucrar ningún algoritmo de ML. Son rápidos y generales, pero no consideran interacciones entre variables.

- **Missing Value Ratio:** eliminar variables con demasiados datos faltantes.
- **Correlación de Pearson con el objetivo:** variables con mayor correlación absoluta con Y tienden a ser más informativas. El signo indica la dirección (positiva o negativa), pero no la importancia relativa. Una limitación es que una variable puede tener alta correlación individual con el objetivo pero ser redundante si ya está capturada por otra variable.
- **f_regression / F-score:** evalúa la relación lineal entre cada variable y el objetivo mediante un test estadístico F. Variables con alta correlación suelen presentar alto F-score y bajo p-value. Al igual que la correlación, evalúa cada variable de forma independiente sin considerar interacciones. Puede ocurrir que seleccionar las K variables con mayor F-score empeore el modelo respecto a usar todas las variables, porque ese subconjunto puede no cubrir aspectos relevantes que las variables descartadas sí aportaban en conjunto.
- **OLS p-values:** evalúa la contribución de cada variable **condicionada** a la presencia de todas las demás. Una variable puede parecer muy relevante individualmente pero tener p-value alto en OLS si su información ya está contenida en otras variables del modelo. Al contrario, el umbral de 0.05 es una convención estadística, no una regla estricta — debe complementarse con evaluación empírica del modelo.
- **Information Gain, Chi-square Test, Fisher's Score.**

#### Métodos Envolventes (Wrappers)

Usan un algoritmo de ML como "evaluador" de los subconjuntos de variables. Más precisos que los filtros porque consideran las interacciones entre variables y el comportamiento específico del algoritmo, pero mucho más costosos computacionalmente.

- **Forward Selection:** comienza con ninguna variable y va añadiendo de a una la que más mejora el modelo.
- **Backward Elimination:** comienza con todas y va eliminando de a una la menos significativa. Existe una versión clásica basada en p-values (estadística) y una versión moderna basada en métricas de desempeño con validación cruzada. La segunda es preferible porque está alineada con optimizar la capacidad predictiva real. Forward y backward pueden seleccionar subconjuntos distintos porque el orden de incorporación/eliminación afecta qué combinaciones se evalúan — es posible que una variable que parece irrelevante sola sea importante en presencia de otras, y viceversa.
- **Recursive Feature Elimination (RFE):** entrena el modelo, identifica las variables menos importantes según los pesos del modelo, las elimina, y repite recursivamente. A diferencia de forward/backward (que evalúan el desempeño del modelo en cada paso), RFE se basa en los coeficientes o importancias internas del modelo para decidir qué eliminar, lo que puede llevar a selecciones distintas.
- **Stepwise Selection:** combina forward y backward dinámicamente — agrega variables que mejoran el modelo y elimina variables que dejan de ser útiles. Su ventaja sobre forward o backward puros es que puede corregir decisiones previas: una variable agregada en un paso anterior puede eliminarse si deja de ser útil tras incorporar otras variables.

#### Métodos Integrados (Embedded)

La selección ocurre durante el propio proceso de entrenamiento. Combinan las ventajas de los filtros (eficiencia) y los wrappers (considera el algoritmo específico).

- **Lasso (L1):** puede llevar exactamente a cero los coeficientes de las variables menos relevantes, eliminándolas del modelo automáticamente. Las variables que Lasso elimina no siempre coinciden exactamente con las que los métodos wrapper descartan, porque Lasso opera en el espacio de todos los coeficientes simultáneamente mientras que los wrappers construyen el subconjunto de forma incremental.
- **Ridge (L2):** reduce todos los coeficientes pero no los lleva a cero. Útil cuando hay multicolinealidad.
- **Random Forest Importance:** calcula la importancia como la reducción total de impureza que produce cada variable a lo largo de todos los árboles.

### Ridge vs. Lasso: la diferencia geométrica

La restricción L2 (Ridge) define una esfera en el espacio de coeficientes. Al buscar el mínimo del error sobre esa esfera, es poco probable que la solución toque exactamente un eje (coeficiente = 0).

La restricción L1 (Lasso) define un rombo (en 2D) o un hiperoctaedro (en dimensiones superiores). Sus esquinas están exactamente sobre los ejes, y el mínimo del error tiende a caer en esas esquinas — produciendo coeficientes exactamente cero.

### El baseline como punto de referencia

Antes de aplicar cualquier método de selección de características, es fundamental establecer un **baseline**: un modelo entrenado con todas las variables disponibles sin ningún proceso de selección. El baseline sirve como punto de comparación para cuantificar si los métodos de feature selection efectivamente mejoran el desempeño o no. Si ningún método de selección supera el baseline, eso no significa necesariamente que la selección fue incorrecta — puede significar que el dataset tiene variables que son complementarias y el modelo las necesita todas, o que la reducción de varianza por eliminar variables no compensa la pérdida de información.

---

## 6. Métricas de Evaluación

### ¿Por qué no basta el accuracy?

El accuracy (proporción de predicciones correctas) es engañoso en presencia de **clases desbalanceadas**. Un modelo que siempre predice la clase mayoritaria puede tener 95% de accuracy en un dataset 95%-5%, sin haber aprendido nada útil. Se necesitan métricas más informativas.

### Estrategias de validación

**Hold-out:** divide el dataset en entrenamiento (ej. 75%) y prueba (25%). Simple y rápido, pero el resultado puede variar según la división específica.

**K-Fold Cross Validation:** divide el dataset en K partes iguales. El modelo se entrena K veces, cada vez con un pliegue distinto como prueba. El resultado final es el promedio de las K evaluaciones. Da una estimación más robusta y menos dependiente del azar de la división.

### La Matriz de Confusión

Herramienta fundamental para entender exactamente dónde falla un clasificador binario:

|  | Predicho Positivo | Predicho Negativo |
|---|---|---|
| **Real Positivo** | Verdadero Positivo (TP) | Falso Negativo (FN) |
| **Real Negativo** | Falso Positivo (FP) | Verdadero Negativo (TN) |

- **TP:** el modelo predijo positivo y era correcto.
- **TN:** el modelo predijo negativo y era correcto.
- **FP (Error Tipo I):** el modelo predijo positivo pero era negativo — falsa alarma.
- **FN (Error Tipo II):** el modelo predijo negativo pero era positivo — caso perdido.

La importancia relativa de FP vs FN depende del dominio. En diagnóstico médico de una enfermedad grave, un FN (decirle a un enfermo que está sano) es mucho más costoso que un FP.

### Métricas derivadas de la matriz de confusión

**Accuracy:** `(TP + TN) / total` — útil solo cuando las clases están balanceadas.

**Precision:** `TP / (TP + FP)` — de todos los que el modelo clasificó como positivos, ¿cuántos realmente lo eran? Alta precision = pocas falsas alarmas.

**Recall (Sensibilidad):** `TP / (TP + FN)` — de todos los casos realmente positivos, ¿cuántos detectó el modelo? Alto recall = pocos casos perdidos.

**Specificity (Especificidad):** `TN / (TN + FP)` — capacidad de detectar correctamente los casos negativos.

**F1-Score:** `2 × (Precision × Recall) / (Precision + Recall)` — promedio armónico entre precision y recall. Preferida cuando hay clases desbalanceadas porque penaliza los modelos que sacrifican mucho una métrica para maximizar la otra.

### El trade-off Precision–Recall

Precision y recall están en tensión y están controlados por el **umbral de clasificación**. Subir el umbral (ser más exigente para clasificar como positivo) aumenta la precision pero reduce el recall. Bajarlo aumenta el recall pero reduce la precision.

### Parámetros vs. Hiperparámetros

**Parámetros:** valores que el modelo aprende automáticamente durante el entrenamiento (ej. los coeficientes β de una regresión lineal).

**Hiperparámetros:** valores que se deben definir manualmente antes de entrenar (ej. K en KNN, profundidad de un árbol, C en SVM, α en Ridge/Lasso). No se aprenden de los datos — se eligen mediante búsqueda y validación cruzada.

### Estrategias de búsqueda de hiperparámetros

**Grid Search:** prueba exhaustivamente todas las combinaciones de una grilla de valores definida. Garantiza encontrar la mejor combinación dentro de la grilla, pero el costo crece exponencialmente con el número de hiperparámetros.

**Random Search:** selecciona combinaciones aleatorias dentro de un rango. Empíricamente más eficiente porque no todas las combinaciones son igualmente prometedoras.

### Curva ROC y AUC

La **curva ROC** visualiza el desempeño de un clasificador a lo largo de todos los posibles umbrales de decisión:

- **Eje Y:** Tasa de Verdaderos Positivos (Recall).
- **Eje X:** Tasa de Falsos Positivos (1 − Especificidad).

**AUC (Area Under the Curve):**

- **AUC = 1.0:** clasificador perfecto.
- **AUC = 0.5:** clasificador sin valor predictivo (equivale a lanzar una moneda).
- **AUC < 0.5:** el modelo está invirtiendo las clases sistemáticamente.

La interpretación probabilística del AUC: representa la probabilidad de que, dado un ejemplo positivo y uno negativo elegidos al azar, el modelo asigne mayor probabilidad al positivo. Es independiente del umbral elegido, lo que la hace útil para comparar modelos.

---

*Resumen elaborado a partir de los apuntes y laboratorios del curso EIN087B — Ciencia de Datos, UTFSM Concepción.*
