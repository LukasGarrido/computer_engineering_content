# Resumen Completo — EIN087B Ciencia de Datos

**Universidad Técnica Federico Santa María · Prof. Jorge Portilla G. · Concepción**

---

## Índice

1. [Support Vector Machines (SVM)](https://claude.ai/chat/05fd3a26-f11e-4f40-ade7-580cbcdd26ec#1-support-vector-machines)
2. [KNN y K-Means](https://claude.ai/chat/05fd3a26-f11e-4f40-ade7-580cbcdd26ec#2-knn-y-k-means)
3. [Bagging y Boosting](https://claude.ai/chat/05fd3a26-f11e-4f40-ade7-580cbcdd26ec#3-bagging-y-boosting)
4. [Series de Tiempo y Procesamiento de Imágenes](https://claude.ai/chat/05fd3a26-f11e-4f40-ade7-580cbcdd26ec#4-series-de-tiempo-y-procesamiento-de-im%C3%A1genes)
5. [Grafos en Ciencia de Datos](https://claude.ai/chat/05fd3a26-f11e-4f40-ade7-580cbcdd26ec#5-grafos-en-ciencia-de-datos)
6. [Deployment de Modelos](https://claude.ai/chat/05fd3a26-f11e-4f40-ade7-580cbcdd26ec#6-deployment-de-modelos)

---

## 1. Support Vector Machines

### La jerarquía conceptual

Las SVM no son un único algoritmo sino una familia de tres clasificadores relacionados, cada uno una extensión del anterior:

**Maximal Margin Classifier (MMC)** → solo funciona con datos perfectamente separables linealmente. Busca el hiperplano que maximiza el margen entre clases. Es el caso ideal pero muy frágil en datos reales.

**Support Vector Classifier (SVC)** → extiende el MMC permitiendo "violaciones suaves" del margen mediante variables de holgura ξᵢ y un parámetro de penalización C. Ya tolera ruido y no separabilidad perfecta.

**Support Vector Machine (SVM)** → extiende el SVC aplicando el truco del kernel para manejar fronteras de decisión no lineales, proyectando implícitamente los datos a espacios de alta dimensión.

### El hiperplano

Un hiperplano es una frontera de decisión generalizada: en 2D es una línea (`β₀ + β₁X₁ + β₂X₂ = 0`), en 3D es un plano, en N dimensiones es una variedad de N−1 dimensiones. La posición de cualquier punto respecto al hiperplano se determina por el signo del resultado de la ecuación: positivo → una clase, negativo → la otra.

### El Maximal Margin Classifier en detalle

El margen es la distancia mínima desde cualquier punto de entrenamiento al hiperplano. El MMC maximiza ese margen resolviendo:

**Minimizar:** `½ ‖w‖²` **Sujeto a:** `yᵢ(w·xᵢ + b) ≥ 1` para todo punto i

La restricción garantiza que cada punto esté al lado correcto con al menos distancia 1. El `½` es conveniencia matemática. La normalización `Σβⱼ² = 1` garantiza que las distancias no dependan de la escala.

Los **vectores de soporte** son los puntos que están justo sobre las líneas del margen. Son los únicos que realmente definen el hiperplano — mover cualquier otro punto no lo afecta. Estos puntos son especialmente importantes porque determinar la posición y orientación de la frontera: mover uno de ellos puede cambiar completamente la solución encontrada por el modelo.

**Formulación dual (Lagrangiana):** el problema primal se transforma al dual para resolverlo eficientemente. La solución depende únicamente de productos internos `xᵢ·xⱼ`, lo que luego permite sustituirlos por kernels. Las condiciones KKT aseguran que `αᵢ > 0` solo para los vectores de soporte, y `w = Σαᵢyᵢxᵢ`.

**Limitación fundamental:** si los datos no son perfectamente separables, el sistema de restricciones no tiene solución factible. Ahí entra el SVC.

### El Support Vector Classifier (margen blando)

Introduce variables de holgura ξᵢ que permiten que ciertos puntos estén en el lado incorrecto del margen:

|Valor de ξᵢ|Interpretación|
|---|---|
|ξᵢ = 0|Punto correctamente fuera del margen|
|0 < ξᵢ ≤ 1|Punto dentro del margen pero en el lado correcto del hiperplano|
|ξᵢ > 1|Punto en el lado incorrecto del hiperplano (error de clasificación)|

El parámetro **C** controla cuánto se penalizan esas violaciones. En términos prácticos, un C pequeño hace al modelo más suave (más tolerante, margen amplio, mayor generalización) y un C grande hace al modelo más rígido (menos tolerante, margen estrecho, mayor riesgo de sobreajuste). C se elige mediante validación cruzada.

Una observación importante sobre los vectores de soporte y C: cuando C es pequeño y el margen es muy amplio, más puntos quedan dentro del margen o en el lado incorrecto, por lo que el número de vectores de soporte aumenta. Cuando C es grande y el margen es estrecho, pocos puntos son vectores de soporte. Observar cuántos vectores de soporte utiliza el modelo puede ayudar a interpretar la complejidad del modelo, el nivel de regularización efectivo y posibles señales de sobreajuste.

### El truco del kernel

En lugar de transformar explícitamente los datos a un espacio de alta dimensión (costoso), se calcula directamente el producto interno en ese espacio mediante una función kernel `K(xᵢ, xⱼ)`. La función de clasificación queda `f(x) = β₀ + Σαᵢ K(x, xᵢ)`.

Un punto clave de la intuición del truco del kernel es que **seleccionar un kernel equivale a seleccionar la geometría del espacio de representación**: con un kernel lineal el espacio sigue siendo el mismo; con un kernel polinómico el espacio tiene curvatura polinómica; con RBF el espacio tiene dimensión infinita y permite fronteras arbitrariamente complejas.

**Kernel lineal:** `K(x,y) = x·y` — equivale al SVC estándar. Cuantifica similitud mediante correlación de Pearson. Adecuado cuando los datos son aproximadamente separables linealmente o el espacio original ya contiene suficiente información.

**Kernel polinómico:** `K(x,y) = (1 + γ x·y)^d` — captura interacciones entre features de grado d. A medida que aumenta el grado del polinomio, la frontera puede volverse más compleja, aumentando también el riesgo de sobreajuste.

**Kernel RBF/Gaussiano:** `K(x,y) = exp(−γ‖x−y‖²)` — mapea a dimensión infinita, muy flexible, el más usado en la práctica. γ controla cuánto influye cada punto vecino. Es especialmente útil cuando la relación entre clases es compleja o no existe una separación lineal clara. El parámetro γ por defecto en sklearn usa `γ = 1 / (n_features × σ²(X))`.

**Kernel sigmoide:** construye fronteras basadas en una función sigmoidal. Tiene una formulación relacionada con redes neuronales tempranas. Aunque es menos utilizado que RBF o polinómico, puede ser útil en algunos problemas específicos.

**Kernels personalizados:** ciertas implementaciones permiten definir funciones kernel propias. Esto permite diseñar métricas de similitud específicas para el dominio del problema o incorporar conocimiento experto directamente en la estructura del modelo.

### La función de decisión como medida de confianza

La función de decisión `f(x) = w·x + b` no solo indica a qué clase pertenece un punto, sino también **qué tan lejos está del hiperplano**. Un punto con valor cercano a 0 es ambiguo (está en la frontera); un punto con valor alto en magnitud está bien clasificado y lejos de la frontera. Esta propiedad es útil para evaluar la certeza del modelo en cada predicción individual.

### El preprocesamiento es crítico en SVM

Las SVM son sensibles a la escala de los datos porque la distancia al hiperplano depende directamente de los valores numéricos de las features. Features con rangos muy distintos harán que el modelo ignore las de rango pequeño. Por esto, **normalizar los datos con StandardScaler antes de entrenar una SVM es un paso obligatorio**, no opcional.

### Grid Search y optimización de hiperparámetros

Dado que los hiperparámetros de las SVM (`C`, `gamma`, `degree`, `coef0`) interactúan entre sí y su efecto depende de los datos específicos, se usa **Grid Search con validación cruzada** (`GridSearchCV`) para explorar el espacio de hiperparámetros de forma sistemática. La búsqueda suele hacerse en dos etapas: primero una búsqueda amplia para identificar regiones prometedoras, y luego un refinamiento alrededor de los mejores valores encontrados. La primera búsqueda puede descartar kernels enteros o regiones del espacio, haciendo la segunda búsqueda mucho más eficiente.

### Accuracy vs. interpretación geométrica

En SVM, las métricas numéricas (accuracy, precision, recall) no reemplazan la interpretación geométrica de la frontera de decisión. La geometría de la frontera y el comportamiento del margen son igualmente importantes para comprender qué está aprendiendo el modelo. Un modelo con alta accuracy pero con una frontera visualmente irregular puede estar sobreajustando de formas que las métricas no detectan.

### Resumen comparativo

|Concepto|MMC|SVC|SVM|
|---|---|---|---|
|Frontera de decisión|Lineal|Lineal suave|No lineal (kernel)|
|Viola el margen|No|Sí (controla C)|Sí (controla C)|
|Maneja datos no separables|No|Sí|Sí|
|Usa kernels|No|No|Sí|

---

## 2. KNN y K-Means

### Distancia de Minkowski — la base de ambos algoritmos

`d(P₁, P₂) = (|x₂−x₁|^p + |y₂−y₁|^p)^(1/p)`

Con p=1 → Distancia Manhattan (camino en cuadrícula). Con p=2 → Distancia Euclidiana (línea recta, la más usada). Con p→∞ → Distancia Chebyshev (máxima diferencia entre coordenadas).

### K-Means Clustering (aprendizaje no supervisado)

Agrupa datos en K clusters minimizando la Suma de Errores al Cuadrado (SSE / Inercia):

`SSE = Σᵢ min_c ‖xᵢ − µc‖²`

**Algoritmo estándar:** (1) elegir K; (2) inicializar K centroides al azar; (3) asignar cada punto al centroide más cercano; (4) recalcular cada centroide como la media de sus puntos asignados; (5) repetir 3-4 hasta convergencia.

**Método del Codo:** se entrena K-Means para K=1,2,...,10, se grafica la inercia vs K, y se busca el "codo" donde la reducción de inercia se vuelve marginal. Indica el K óptimo.

**K-Means++:** mejora la inicialización seleccionando cada centroide nuevo con probabilidad proporcional a D(x)² (distancia al centroide más cercano ya elegido). Distribuye mejor los centroides iniciales y evita mínimos locales malos.

**MiniBatch K-Means:** usa subconjuntos aleatorios de datos en cada iteración. Mucho más rápido para datasets grandes, con calidad ligeramente inferior. La actualización del centroide es incremental: `C_{t+1} = Ct + (1/Nᵢ)(xᵢ − Ct)`.

**Métricas de evaluación de clustering:** Homogeneidad, Completitud, V-Measure (media armónica de ambas), Silhouette (de −1 a 1, cercano a 1 es mejor), ARI y AMI.

### K-Nearest Neighbors — KNN (aprendizaje supervisado)

Algoritmo perezoso (lazy): no hay fase de entrenamiento real. Memoriza todos los datos y en inferencia calcula distancias a todos los puntos.

**Para clasificación:** dado un punto nuevo x₀, se calculan las distancias a todos los puntos de entrenamiento, se seleccionan los K más cercanos (N₀), y se asigna la clase más frecuente: `Pr(Y=j|X=x₀) = (1/K) Σᵢ∈N₀ 𝟙(yᵢ=j)`.

**Para regresión (KNN Regressor):** el valor predicho es la media de los K vecinos más cercanos.

**Elección de K:** K pequeño → alta varianza, fronteras complejas, sensible a outliers. K grande → alto sesgo, fronteras suaves. Se elige con validación cruzada.

**Limitaciones:** costoso en inferencia O(n) por predicción; sufre la maldición de la dimensionalidad; el tamaño del modelo crece con el dataset.

### Comparativa final

|Característica|K-Means|KNN|
|---|---|---|
|Tipo|No supervisado|Supervisado|
|Tarea|Clustering|Clasificación / Regresión|
|Requiere etiquetas|No|Sí|
|Entrenamiento|Iterativo|Ninguno (lazy)|
|Inferencia|Asignar al centroide más cercano|Calcular distancias a todos|

---

## 3. Bagging y Boosting

### El problema de fondo: error en ML

Todo modelo de ML comete tres tipos de error:

**Bias (sesgo):** error por suposiciones demasiado fuertes → modelo simple → underfitting. **Varianza:** sensibilidad excesiva a pequeñas variaciones en los datos → modelo complejo → overfitting. **Ruido:** error inherente a los datos, irreducible.

El objetivo es encontrar el equilibrio ("sweet spot") donde bias y varianza son mínimos. Bagging reduce varianza; Boosting reduce sesgo (y puede también reducir varianza).

### Árboles de decisión — la base

Los árboles dividen el espacio de predictores en regiones rectangulares mediante **división binaria recursiva (greedy, top-down)**: en cada paso se elige el predictor Xⱼ y punto de corte s que minimizan el RSS (regresión) o el índice de Gini / Entropía (clasificación).

Para evitar sobreajuste se usa **Cost Complexity Pruning**: se construye un árbol grande T₀ y luego se poda minimizando `RSS + α|T|`, donde α es el parámetro de regularización elegido por validación cruzada.

En clasificación, los criterios de división son:

- **Índice de Gini:** `G = Σ p̂mk(1−p̂mk)` — mide impureza del nodo.
- **Entropía:** `D = −Σ p̂mk log(p̂mk)` — mide incertidumbre.

### ¿Por qué los árboles individuales son inestables?

Un árbol de decisión es muy sensible a pequeñas variaciones en los datos de entrenamiento: cambios en pocas muestras pueden alterar completamente la estructura del árbol y la posición de sus divisiones. Esto los hace presentar alta varianza. Los métodos ensemble existen precisamente para resolver este problema combinando múltiples modelos débiles en uno más robusto.

### Ensemble Learning

Un método de ensamble combina múltiples modelos simples (**weak learners**) para construir un predictor más robusto y preciso. La idea central es que la combinación de varios modelos débiles puede producir un modelo fuerte. Existen dos grandes familias con lógicas opuestas:

### Bagging (Bootstrap Aggregating)

**Idea:** promediar muchas predicciones reduce la varianza. `f̂_bag(x) = (1/B) Σ f̂_b(x)`.

La reducción de varianza se puede expresar formalmente: si cada modelo tiene varianza `Var(X)`, el promedio de B modelos independientes tiene varianza `Var(X)/n`. A medida que B crece, la varianza disminuye y la estabilidad mejora.

**Procedimiento:** (1) generar B muestras bootstrap con reemplazo; (2) entrenar un árbol profundo sin podar en cada muestra; (3) promediar (regresión) o votar por mayoría (clasificación).

**Características principales:** entrenamiento paralelo (los modelos son independientes entre sí), funciona especialmente bien con modelos inestables como los árboles, y reduce principalmente la varianza sin afectar el sesgo.

**Estimación OOB:** cada muestra bootstrap usa ~2/3 de los datos; el ~1/3 restante permite estimar el error sin validación cruzada adicional.

### Random Forests

Agrega al Bagging que en cada división de cada árbol solo se considera un subconjunto aleatorio de `m ≈ √p` predictores. Esto descorrelaciona los árboles y hace que el promedio reduzca más la varianza. Si m = p, equivale a Bagging.

### Boosting

**Idea central:** construir árboles secuencialmente, donde cada árbol corrige los residuos del modelo anterior. Los modelos no son independientes — cada iteración depende del desempeño previo. El objetivo es enfocarse progresivamente en las muestras difíciles de clasificar.

**Características principales:** entrenamiento secuencial (los modelos son dependientes entre sí), reduce principalmente el sesgo, y puede producir modelos altamente precisos aunque con mayor sensibilidad al ruido que Bagging.

**Algoritmo general:**

1. Inicializar `f̂(x) = 0`, `rᵢ = yᵢ`
2. Para b = 1, ..., B: ajustar árbol sobre residuos; actualizar `f̂(x) ← f̂(x) + λ·f̂_b(x)`; actualizar residuos
3. Resultado: `f̂(x) = Σ λ·f̂_b(x)`

### AdaBoost

AdaBoost asigna **pesos a las muestras** en lugar de trabajar con residuos. Inicialmente todas las muestras tienen el mismo peso. Después de cada clasificador, las muestras mal clasificadas aumentan su peso y las bien clasificadas disminuyen su influencia relativa, forzando al siguiente clasificador a prestar más atención a los ejemplos difíciles.

La importancia de cada clasificador individual se calcula como `αt = ½ ln((1−εt)/εt)`, donde εt es su tasa de error. Un clasificador con error bajo recibe mayor peso en la predicción final. Si todos los clasificadores recibieran el mismo peso (αt constante), el boosting perdería su mecanismo de corrección enfocada: equivaldría a un voto igualitario sin aprendizaje progresivo, y perdería la ventaja de enfocarse en los ejemplos difíciles.

### Gradient Boosting

En lugar de re-ponderizar muestras como AdaBoost, Gradient Boosting optimiza directamente una función de pérdida construyendo cada árbol sobre los **gradientes del error residual**. Esto lo hace más general que AdaBoost (puede optimizar cualquier función de pérdida diferenciable, no solo clasificación binaria) y suele producir modelos más precisos. El riesgo de sobreajuste existe y se controla principalmente mediante la tasa de aprendizaje (`learning_rate`) y el número de árboles B.

### El parámetro `stratify` en la división train/test

Cuando se divide un dataset en conjuntos de entrenamiento y prueba, el parámetro `stratify` garantiza que la proporción de cada clase sea la misma en ambos subconjuntos que en el dataset original. Sin él, una división aleatoria podría, por azar, concentrar la mayoría de los ejemplos de una clase en el conjunto de entrenamiento y dejar al modelo sin ejemplos representativos para evaluar. En datasets desbalanceados esto es especialmente crítico: si hay pocas muestras de la clase minoritaria, pueden terminar todas en el conjunto de entrenamiento y la evaluación sería engañosa.

### El desbalance de clases y su impacto en las métricas

Un dataset desbalanceado (muchas más muestras de una clase que de otra) puede inflar artificialmente el accuracy: un modelo que siempre predice la clase mayoritaria puede tener accuracy del 90% en un dataset 90%-10%, sin haber aprendido nada útil. Por eso, en presencia de desbalance, métricas como **precision**, **recall** y **F1-score** son más informativas que el accuracy solo. La matriz de confusión también es esencial, ya que muestra exactamente qué tipos de errores comete el modelo (falsos positivos vs. falsos negativos).

### Correlación entre features y su impacto en los modelos

Cuando dos o más features están altamente correlacionadas, aportan información redundante al modelo. En árboles de decisión esto puede llevar a que el modelo elija arbitrariamente entre ellas en cada división, generando inestabilidad. En Random Forests, la selección aleatoria de m predictores ayuda a mitigar este problema al forzar que distintos árboles usen distintas features correlacionadas. En Gradient Boosting, la correlación puede generar sobreestimación de la importancia de ciertas variables.

### Comparativa general

|Característica|Bagging|Random Forest|Boosting|
|---|---|---|---|
|Construcción|Paralela|Paralela|Secuencial|
|Muestreo|Bootstrap|Bootstrap|Sin remuestreo|
|Predictores por split|Todos (p)|Subconjunto (m)|Todos (p)|
|Reduce|Varianza|Varianza|Sesgo (y varianza)|
|Riesgo de overfitting|Bajo|Bajo|Moderado|
|Sensibilidad al ruido|Menor|Menor|Mayor|

---

## 4. Series de Tiempo y Procesamiento de Imágenes

### Parte 1 — Series de Tiempo

#### ¿Qué las hace especiales?

A diferencia de los datasets clásicos donde las observaciones son i.i.d. (independientes e idénticamente distribuidas), en una serie de tiempo `{yₜ}`:

- Cada observación está asociada a un instante t específico.
- El **orden importa**: mezclar las filas destruye la información.
- El valor futuro depende de su propia historia.

#### Los componentes de una serie de tiempo

|Componente|Símbolo|Descripción|
|---|---|---|
|Tendencia|Tₜ|Evolución a largo plazo (crecimiento, caída)|
|Estacionalidad|Sₜ|Patrón que se repite en intervalos fijos y predecibles|
|Ciclo|Cₜ|Oscilaciones de largo plazo sin periodicidad fija|
|Residuo|Rₜ|Ruido e irregularidades no explicadas|

**Estacionalidad vs. ciclos:** la estacionalidad tiene periodicidad fija y conocida (se modela explícitamente); los ciclos tienen periodicidad irregular y generalmente terminan en el residuo.

#### Modelos de descomposición

**Modelo Aditivo:** `yₜ = Tₜ + Sₜ + Rₜ` — usar cuando la amplitud de la estacionalidad es constante independientemente del nivel de la tendencia.

**Modelo Multiplicativo:** `yₜ = Tₜ × Sₜ × Rₜ` — usar cuando la amplitud de la estacionalidad **crece proporcionalmente** con la tendencia. Es el más común en datos de consumo energético, ventas, tráfico web y producción industrial.

#### Media Móvil

`ŷₜ = (1/n) Σᵢ₌₁ⁿ yₜ₋ᵢ`

El tamaño de la ventana controla el trade-off entre sensibilidad y suavizado: ventanas pequeñas (MA_7) son más reactivas y siguen mejor los cambios recientes, pero conservan más ruido; ventanas grandes (MA_30) revelan la tendencia de largo plazo pero pierden detalle de corto plazo. Una ventana de n=365 para datos diarios eliminaría completamente la estacionalidad anual, dejando solo la tendencia pura.

Para predecir más allá de los datos observados se usan las predicciones anteriores como sustituto de los datos reales — lo que produce una "regresión a la media" en horizontes largos, ya que la media de una ventana que incluye cada vez más predicciones tiende a estabilizarse.

#### Modelos Autorregresivos AR(p)

`ŷₜ = φ₀ + φ₁yₜ₋₁ + ... + φₚyₜ₋ₚ`

Los pesos φ se **aprenden** minimizando el MSE, a diferencia de la media móvil donde los pesos son fijos e iguales. El parámetro `p` (número de lags) determina cuántos valores pasados considera el modelo. Si se usan muy pocos lags, el modelo no captura dependencias de largo plazo y subajusta. Si se usan demasiados, puede sobreajustar y se vuelve inestable.

La **intuición** del modelo AR es simple: si hoy el consumo eléctrico es alto y ayer también fue alto, es razonable esperar que mañana siga siendo relativamente alto. El modelo formaliza esa intuición aprendiendo automáticamente cuánto influye cada observación pasada.

La diferencia conceptual con la media móvil es importante: la media móvil asigna igual importancia a todas las observaciones de la ventana, mientras que el modelo AR aprende pesos distintos para cada lag, permitiéndole descubrir que algunos rezagos (como el del mismo día de la semana pasada) son más predictivos que otros.

**Supuesto crítico:** estacionariedad (media y varianza constantes). Solución para series no estacionarias: **diferenciación** `ΔYₜ = Yₜ − Yₜ₋₁`.

#### Diferenciación

La diferenciación transforma la serie analizando variaciones entre períodos en lugar de valores absolutos. Una diferencia positiva significa que el valor creció respecto al período anterior; una diferencia negativa significa que cayó. La diferenciación elimina tendencias determinísticas y convierte una serie no estacionaria en una que sí lo es (aproximadamente), permitiendo aplicar modelos AR con mayor validez estadística. Tras predecir las diferencias, se reconstruye la serie original acumulándolas desde el último valor observado.

#### Fuga de datos (Data Leakage) en series temporales

La fuga de datos ocurre cuando información del futuro se filtra en el entrenamiento. En series temporales es especialmente riesgosa porque puede dar una falsa sensación de precisión. Los errores más comunes son: usar variables exógenas que ya incluyen valores futuros, normalizar toda la serie con estadísticas calculadas sobre el conjunto completo (usando la media global en lugar de solo la del pasado), y mezclar observaciones de entrenamiento y prueba sin respetar la secuencia temporal. La validación walk-forward es la técnica recomendada para evitar estos problemas.

#### Métricas de evaluación de series de tiempo

Además del RMSE, en series de tiempo se usan:

- **MAE (Mean Absolute Error):** `(1/n) Σ|ŷₜ − yₜ|` — error promedio en las mismas unidades que la variable. Menos sensible a errores grandes que el RMSE.
- **MAPE (Mean Absolute Percentage Error):** `(1/n) Σ|ŷₜ − yₜ|/yₜ × 100` — error porcentual promedio. Permite comparar modelos sobre series con distintas escalas.
- **R²:** proporción de la varianza de la serie que el modelo explica. Un R² cercano a 1 indica buen ajuste; uno negativo indica que el modelo es peor que predecir siempre la media.

#### Prophet

Prophet es una biblioteca desarrollada por Meta para realizar pronósticos de series temporales. Modela la serie como `y(t) = g(t) + s(t) + h(t) + εt` donde:

- `g(t)` = **tendencia** (lineal o logística, con detección automática de cambios de tendencia llamados _changepoints_).
- `s(t)` = **estacionalidad** (modelada mediante series de Fourier, puede ser diaria, semanal y anual simultáneamente).
- `h(t)` = **eventos especiales** (feriados, campañas, shocks externos definidos por el usuario como regresores binarios).
- `εt` = error aleatorio.

A diferencia de los modelos AR, Prophet **no requiere diferenciación previa** porque modela la tendencia directamente. Otra ventaja clave es que maneja datos faltantes de forma nativa y genera automáticamente intervalos de confianza (`yhat_lower`, `yhat_upper`). El campo `yhat` es la predicción puntual; los intervalos representan la incertidumbre del modelo en cada punto. Prophet es muy utilizado en forecasting empresarial precisamente por su facilidad de uso y capacidad de incorporar conocimiento del dominio (feriados, eventos) sin necesidad de ingeniería de features manual.

#### Resumen comparativo de métodos

|Método|Supuesto|Maneja tendencia|Maneja estacionalidad|Intervalo de confianza|
|---|---|---|---|---|
|Media Móvil|Ninguno|No|No|No|
|AR(p)|Estacionariedad|No directamente|No directamente|No|
|ARD|Estacionariedad (diferenciada)|Sí (mediante diff)|No directamente|No|
|Prophet|Aditivo/multiplicativo|Sí|Sí (múltiple)|Sí|

---

### Parte 2 — Procesamiento Básico de Imágenes

#### Tipos de imagen

Una imagen digital es una **matriz de números**. Escala de grises: 1 canal, 8 bpp (0-255). RGB: 3 canales, 24 bpp. RGBA: 4 canales con transparencia. Multiespectral: >10 bandas, captura más allá del visible. Hiperespectral: >100 bandas.

#### Corrección Gamma

`I_salida = I_entrada^γ`. γ < 1 aclara (realza zonas oscuras). γ > 1 oscurece (realza zonas claras). Muy útil en imágenes médicas para resaltar estructuras difíciles de ver.

#### Histogramas

`h(k) = nₖ` cuenta cuántos píxeles tienen cada nivel de intensidad k. La versión normalizada `p(k) = nₖ/n` es un estimador de la distribución de intensidades. En RGB: tres histogramas independientes.

#### Distancia de Bhattacharyya

`D_B(h₁, h₂) = √(1 − Σᵢ √(h₁⁽ⁱ⁾ × h₂⁽ⁱ⁾))`. Compara dos histogramas normalizados. D_B ≈ 0 → muy similares; D_B ≈ 1 → muy diferentes.

#### Segmentación por umbralización (Thresholding)

Convierte una imagen en escala de grises a binaria según si cada píxel supera un umbral. Los cinco tipos en OpenCV: Binario, Binario Invertido, Truncado, Umbral a Cero, y Umbral a Cero Invertido.

---

## 5. Grafos en Ciencia de Datos

### ¿Qué es un grafo y por qué importa?

Un grafo `G = (V, E)` modela relaciones entre entidades: V son los **nodos** (entidades) y E son las **aristas** (relaciones). Tanto nodos como aristas pueden tener propiedades (atributos clave-valor).

**¿Por qué supera al ML clásico en ciertos problemas?** El ML tradicional asume observaciones i.i.d. Los grafos capturan la dependencia entre observaciones (la estructura relacional), que es información crucial en redes sociales, rutas, moléculas, redes de fraude, etc. El valor de los grafos está en las **relaciones**, no solo en los atributos individuales de cada entidad.

### Tipos de grafos

**Dirigidos (dígrafos):** relaciones con dirección → Twitter/Instagram (seguir ≠ ser seguido). La regla práctica: si se puede preguntar "¿de quién a quién?", usar dirigido; si solo importa que están conectados, usar no dirigido.

**No dirigidos:** relaciones simétricas → Facebook (amistad es mutua).

**Ponderados:** aristas con valor numérico → mapas de carreteras (distancia o tiempo). Los pesos pueden representar distancia, costo, duración, fuerza de relación, probabilidad de transmisión o riesgo, dependiendo del dominio.

**Bipartitos:** hay dos tipos de nodos y las conexiones solo ocurren entre tipos distintos (ej. usuarios-productos en sistemas de recomendación).

**Multigrafos:** pueden existir múltiples conexiones entre los mismos nodos, representando distintos tipos de relación.

### Representaciones del grafo

Un mismo grafo puede representarse de tres formas equivalentes, cada una útil para distintos propósitos:

- **Lista de adyacencia:** para cada nodo, lista sus vecinos directos. Útil para navegación y algoritmos de búsqueda.
- **Matriz de adyacencia:** matriz cuadrada donde la celda (i,j) vale 1 si existe arista entre i y j. Útil para álgebra lineal y detección de patrones globales.
- **Lista de aristas:** tabla de pares (origen, destino, peso). Útil para carga de datos tabulares y construcción eficiente del grafo.

La elección entre representaciones depende del tamaño del problema y del tipo de análisis. Para redes muy grandes (millones de nodos), la lista de aristas es la más eficiente en memoria.

### Conceptos clave

**Grado de un nodo:** número de aristas que inciden en él. En un grafo no dirigido, cada arista cuenta dos veces para el grado total de la red (una por cada extremo). Por eso, en grafos no dirigidos todos los grados son múltiplos de 2. Grado 0 = nodo aislado. Grado 1 = callejón sin salida (dead-end). Los nodos de grado alto son hubs — intersecciones muy conectadas o personas muy influyentes.

**Camino mínimo:** el camino entre dos nodos cuya suma de pesos sea mínima.

**Componente conexa:** subconjunto de nodos donde existe camino entre cualquier par. Una red puede tener múltiples componentes desconectadas entre sí (ej. islas sin conexión terrestre en una red vial).

**Centralidad:**

- **Degree Centrality:** número de conexiones directas. Mide importancia local.
- **Betweenness Centrality:** cuántas veces un nodo actúa como "puente" en caminos mínimos entre otros pares. Nodos con alta intermediación controlan el flujo de información; eliminarlos desconectaría la red.
- **PageRank:** relevancia iterativa basada en la calidad (no solo cantidad) de las conexiones entrantes. Un nodo es importante si sus vecinos también son importantes.

### Algoritmos esenciales

**Detección de comunidades:** Algoritmo de Louvain (optimiza modularidad), Connected Components.

**Caminos mínimos — Algoritmo de Dijkstra:** encuentra el camino más corto desde un nodo origen a todos los demás en grafos con pesos no negativos. Es el núcleo de GPS como Waze o Google Maps. La versión **SSSP (Single Source Shortest Path)** calcula simultáneamente el camino mínimo desde un origen a _todos_ los demás nodos del grafo.

Una consecuencia importante del SSSP: además de las distancias mínimas, el algoritmo retorna el **predecesor** de cada nodo en su camino óptimo. Conectando cada nodo con su predecesor se construye el **árbol de caminos mínimos** — el subgrafo mínimo que conecta el origen con todos los nodos alcanzables a través de sus rutas óptimas.

### Nodos inalcanzables en SSSP

En grafos no completamente conexos, algunos nodos no tienen camino desde el origen. Las implementaciones eficientes (especialmente en GPU) suelen asignar el valor máximo representable del tipo de dato (`np.finfo(np.float32).max`) en lugar de `Inf` o `NaN`, por eficiencia computacional. Estos valores deben filtrarse antes de calcular estadísticas, ya que de lo contrario sesgarían drásticamente los resultados.

### Distintos criterios de optimización en redes

La pregunta "¿desde dónde conviene partir?" tiene varias respuestas válidas dependiendo del objetivo:

- **Minimizar el tiempo máximo (MinMax):** ideal para servicios críticos donde el peor caso no puede superar un límite (ej. transporte de órganos para trasplante).
- **Minimizar la suma total de tiempos:** maximiza eficiencia operacional global, lo mejor para centros de distribución logísticos.
- **Minimizar la distancia al punto más lejano:** criterio geométrico puro, no considera velocidades.

Estos tres criterios generalmente no producen el mismo nodo óptimo.

### Hipergrafos

Un hipergrafo es una extensión del grafo donde las aristas pueden conectar más de dos nodos simultáneamente. En la práctica de análisis de datos, un hipergrafo se construye cuando cada registro de una tabla involucra múltiples entidades a la vez. Existen dos enfoques:

- **Fila como nodo hub:** cada registro se convierte en un nodo central conectado a todas sus entidades. Más denso y útil para ver co-ocurrencias.
- **Conexiones directas:** las entidades se conectan directamente entre sí según reglas explícitas, sin nodo intermedio. Más limpio para responder preguntas del tipo "¿qué vulnerabilidades usa este atacante?".

### Propagación en grafos — Modelo SIR

La estructura de un grafo afecta directamente cómo se propagan fenómenos (epidemias, rumores, fallos, fraudes). El modelo SIR (Susceptible-Infectado-Recuperado) ilustra esto: los nodos tienen tres estados, y los infectados intentan contagiar a sus vecinos con cierta probabilidad en cada paso de tiempo. La topología de la red — quién está conectado con quién — determina la velocidad y cobertura del contagio. Nodos con alta centralidad de grado actúan como super-propagadores.

### Graph Neural Networks (GNNs)

Usan **Message Passing**: cada nodo recopila información de sus vecinos, la agrega y actualiza su propio estado. Tras varias capas, cada nodo tiene un embedding que codifica sus atributos y su entorno estructural.

**Tipos de predicciones:** a nivel de nodo (clasificar un usuario como bot o humano), a nivel de arista / link prediction (predecir si se formará una conexión nueva, ej. recomendación de amigos), y a nivel de grafo completo (determinar si una molécula es tóxica).

### Visualización con encodings semánticos

En grafos grandes, la visualización solo es útil si cada atributo visual tiene una razón explícita. Los encodings más comunes son: **color por rol o categoría** (rojo para atacantes, verde para víctimas), **tamaño proporcional a una métrica** (nodos más activos ocupan más espacio visual), **color de arista por variable continua** (degradado temporal que muestra cuándo ocurrieron las conexiones), e **íconos por tipo de entidad** para reforzar el rol sin depender solo del color. Una visualización bien diseñada puede leerse analíticamente sin documentación adicional.

### Ecosistema tecnológico

**Análisis:** NetworkX (Python, pequeña-mediana escala), igraph (alta performance). **Aceleración GPU:** cuGraph (NVIDIA RAPIDS), con aceleraciones de 10× a 100× sobre NetworkX en CPU para grafos grandes. **Visualización interactiva:** Graphistry (WebGL, permite explorar redes de millones de nodos con zoom, filtros y selección). **GNNs:** PyTorch Geometric (PyG), Deep Graph Library (DGL). **Bases de datos:** Neo4j (lenguaje Cypher), Amazon Neptune, Google Graph Database.

---

## 6. Deployment de Modelos

### El deployment no es el fin, es el inicio de un ciclo

Un modelo que solo vive en un notebook no genera valor. El deployment es llevarlo al mundo real donde recibirá datos nuevos y deberá entregar predicciones útiles, rápidas y confiables.

**CRISP-DM** incluye el Deployment con una flecha de retroalimentación de vuelta a Business Understanding: el modelo en producción genera información nueva sobre si está funcionando, si el negocio cambió, si los datos cambiaron.

### La analogía de Hinton: el modelo de entrenamiento ≠ el modelo de producción

Un modelo de ML tiene dos fases con objetivos distintos:

**En entrenamiento (larval):** se optimiza para aprender lo máximo posible. Se usan arquitecturas enormes, GPUs potentes, mucha memoria, sin preocupación por la eficiencia.

**En producción (adulto):** se optimiza para ser rápido, liviano y eficiente en el hardware disponible (que puede ser un microcontrolador con kilobytes de memoria).

Técnicas para convertir el modelo larval en adulto:

- **Destilación de conocimiento:** entrenar un modelo pequeño (estudiante) para imitar el comportamiento de un modelo grande (maestro).
- **Cuantización:** reducir la precisión numérica de los pesos (ej. de float32 a int8).
- **Poda (pruning):** eliminar conexiones o neuronas que aportan poco al resultado.

### Edge vs. Cloud

**Despliegue Edge:** el modelo corre en el dispositivo local (Raspberry Pi, Arduino, Nvidia Jetson). Ventajas: tiempo real, sin necesidad de conectividad, bajo consumo. Desventajas: recursos muy limitados.

**Despliegue Cloud (AWS, GCP, Azure):** el modelo corre en servidores remotos potentes. Ventajas: escalabilidad masiva, modelo grande sin comprimir. Desventajas: requiere conexión estable, latencia de red, costos de infraestructura.

Muchas aplicaciones reales usan **ambos en combinación**.

### Hardware para inferencia

**CPU:** pocos núcleos potentes, ideal para tareas secuenciales. **GPU:** miles de núcleos simples, modelo SIMT (Single Instruction, Multiple Threads), ideal para multiplicaciones matriciales. El hardware más usado en inferencia. **FPGA:** chip reconfigurable después de fabricado. **TPU (Google) / NPU:** aceleradores específicos para redes neuronales.

**CPU vs GPU:** la CPU optimiza latencia baja por tarea secuencial; la GPU optimiza throughput total mediante paralelismo masivo.

### Toolchains: del entrenamiento al hardware final

Flujo general: `Entrenamiento (PyTorch) → ONNX → Optimización específica → Hardware final`

**ONNX** (Open Neural Network Exchange): formato intermedio estándar, "idioma universal" entre frameworks de entrenamiento y herramientas de inferencia.

**Herramientas de optimización:** TensorRT (NVIDIA, para GPUs), Vitis AI (Xilinx, para FPGAs), TensorFlow Lite (dispositivos móviles), ONNX Runtime (multiplataforma).

### TinyML — llevando modelos a microcontroladores

Los microcontroladores tienen memoria en KB. TinyML aplica destilación + cuantización + poda para crear modelos que quepan.

Un árbol de decisión es naturalmente liviano para embeber: es solo una secuencia de comparaciones `if-else`, sin operaciones de punto flotante complejas. Herramientas como `micromlgen` convierten modelos de scikit-learn directamente a código C embebible.

### Diseño digital y HDL

Para deployments en FPGA los lenguajes HDL (SystemVerilog) **no son lenguajes de programación**: describen circuitos, no instrucciones secuenciales. El código HDL se **sintetiza** (convierte en circuito físico), no se compila.

> **"El software no obedece las leyes de la física, el hardware sí."**

---

_Resumen elaborado a partir de los apuntes y laboratorios del curso EIN087B — Ciencia de Datos, UTFSM Concepción._