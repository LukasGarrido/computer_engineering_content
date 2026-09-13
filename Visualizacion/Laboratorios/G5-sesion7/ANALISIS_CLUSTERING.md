# Laboratorio 7 — Análisis Completo de Técnicas de Agrupación de Datos
## K-Means, DBSCAN y GMM sobre Fashion-MNIST

---

## Tabla de Contenidos

1. [Dataset: Fashion-MNIST](#1-dataset-fashion-mnist)
2. [Preprocesamiento y Reducción de Dimensionalidad (PCA)](#2-preprocesamiento-y-reducción-de-dimensionalidad-pca)
3. [Glosario de Términos Clave](#3-glosario-de-términos-clave)
4. [Sección 4.1 — K-Means Clustering](#4-sección-41--k-means-clustering)
5. [Sección 4.2 — DBSCAN](#5-sección-42--dbscan)
6. [Sección 4.3 — Gaussian Mixture Models (GMM)](#6-sección-43--gaussian-mixture-models-gmm)
7. [Comparativa Global de los Tres Algoritmos](#7-comparativa-global-de-los-tres-algoritmos)
8. [Conclusiones Finales](#8-conclusiones-finales)

---

## 1. Dataset: Fashion-MNIST

### ¿Qué es Fashion-MNIST?

Fashion-MNIST es un dataset de referencia creado por Zalando Research como reemplazo directo del clásico MNIST de dígitos escritos a mano. Contiene:

- **70 000 imágenes** en escala de grises de 28×28 píxeles (60 000 entrenamiento + 10 000 test).
- **10 clases** de prendas y accesorios:

| Etiqueta | Clase          |
|----------|----------------|
| 0        | Camiseta/Top   |
| 1        | Pantalón       |
| 2        | Jersey/Suéter  |
| 3        | Vestido        |
| 4        | Abrigo         |
| 5        | Sandalia       |
| 6        | Camisa         |
| 7        | Zapatilla      |
| 8        | Bolso          |
| 9        | Botín          |

### Carga y Submuestra Utilizada

Cada imagen es un vector de **784 características** (28×28 píxeles aplanados). Los valores de píxel se normalizan al rango [0, 1] dividiendo entre 255.

Para mantener tiempos de cómputo razonables, el laboratorio trabaja con una **submuestra aleatoria de 10 000 imágenes**:

```
Subset: (10000, 784)
```

### ¿Por qué se normaliza a [0, 1]?

La normalización es crítica porque:
- **K-Means y DBSCAN** usan distancias (euclídea, manhattan, etc.). Sin normalizar, las distancias estarían dominadas por magnitud absoluta, no por similitud visual.
- **GMM** asume distribuciones gaussianas; escalar evita que dimensiones con valores grandes dominen la estimación de covarianzas.

---

## 2. Preprocesamiento y Reducción de Dimensionalidad (PCA)

### ¿Por qué aplicar PCA antes de clustering?

Con 784 dimensiones, los algoritmos de clustering sufren la **"maldición de la dimensionalidad"** (*curse of dimensionality*):

- En espacios de alta dimensión, las distancias entre todos los puntos tienden a igualarse, haciendo que nociones como "vecindad" o "centroide" pierdan significado.
- El coste computacional es muy elevado.

El laboratorio usa dos variantes de PCA:

| PCA | n_components | Uso |
|-----|-------------|-----|
| `pca_2d` | 2 | Visualización 2D de clusters |
| `pca_30` | 30 | Entrada para DBSCAN y GMM (~70-80% varianza retenida) |

### ¿Qué es PCA?

**Análisis de Componentes Principales (PCA)** encuentra las direcciones ortogonales de máxima varianza en los datos. Al proyectar sobre las primeras `k` componentes, se obtiene la mejor representación de rango `k` en términos de mínimo error de reconstrucción (MSE).

- **PC1:** captura la mayor fuente de variación en el dataset.
- **PC2:** segunda mayor fuente, ortogonal a PC1.

En el espacio PCA 2D de Fashion-MNIST, las 10 clases **no son perfectamente linealmente separables**: prendas visualmente similares (camisa vs. abrigo, sandalia vs. zapatilla) se solapan en la proyección.

---

## 3. Glosario de Términos Clave

| Término | Definición |
|---------|-----------|
| **Clustering** | Técnica de aprendizaje no supervisado que agrupa datos similares sin etiquetas previas. |
| **Centroide** | Punto medio de un cluster; en K-Means es la media aritmética de todos sus miembros. |
| **Inercia / SSE** | Suma de cuadrados de las distancias de cada punto a su centroide. Mide compacidad de los clusters. |
| **n_iter** | Número de iteraciones que el algoritmo necesitó para converger. |
| **eps (ε)** | En DBSCAN: radio máximo para considerar que dos puntos son vecinos. |
| **min_samples** | En DBSCAN: mínimo de vecinos en radio eps para que un punto sea "core point". |
| **Core point** | Punto con al menos `min_samples` vecinos dentro de radio `eps`. Semilla de un cluster. |
| **Border point** | Punto con menos de `min_samples` vecinos pero dentro del radio de un core point. |
| **Noise / Ruido** | Punto que no es core ni border: no pertenece a ningún cluster (etiqueta = -1). |
| **BIC** | Bayesian Information Criterion. Penaliza la verosimilitud por el nro. de parámetros. Menor es mejor. |
| **AIC** | Akaike Information Criterion. Similar al BIC con penalización menor. Menor es mejor. |
| **Verosimilitud** | En GMM: qué tan bien el modelo explica los datos observados. |
| **Asignación dura** | Cada punto pertenece a exactamente un cluster (K-Means, DBSCAN). |
| **Asignación suave** | Cada punto tiene probabilidades de pertenecer a cada componente (GMM). |
| **covariance_type** | En GMM: forma de la matriz de covarianza de cada componente gaussiana. |
| **Método del codo** | Técnica gráfica para elegir K: buscar el punto donde SSE vs. K deja de bajar abruptamente. |
| **k-distancias** | Distancias al k-ésimo vecino más cercano ordenadas. Su "codo" sugiere un buen valor de `eps`. |
| **PCA** | Principal Component Analysis. Reducción de dimensionalidad por proyección en ejes de máxima varianza. |
| **k-means++** | Inicialización de K-Means que distribuye centroides iniciales de forma esparcida para acelerar convergencia. |

---

## 4. Sección 4.1 — K-Means Clustering

### ¿Cómo funciona K-Means?

K-Means es un algoritmo iterativo de dos pasos:
1. **Asignación:** cada punto se asigna al centroide más cercano.
2. **Actualización:** cada centroide se recalcula como la media de sus puntos asignados.

Se repite hasta que las asignaciones no cambien (convergencia). El resultado depende fuertemente de la inicialización.

---

### 4.1.1 Benchmarking de Estrategias de Inicialización

Se compararon tres estrategias de inicialización con K = 10 (igual al número de clases reales):

| Estrategia | Inercia | Tiempo (s) | Iteraciones |
|-----------|---------|-----------|------------|
| `random` | 318 473.97 | 0.9017 | 85 |
| `k-means++` | 318 474.31 | 1.4085 | 63 |
| `pca-init` | 320 120.44 | 0.5084 | 44 |

#### Análisis Detallado

**Inicialización `random`:**
- Selecciona K centroides iniciales al azar del dataset.
- Logra la **mejor inercia final** (318 473.97), pero requiere **85 iteraciones** para converger.
- Con `n_init=4` se ejecuta 4 veces y conserva el mejor resultado: la repetición compensa la aleatoriedad.
- **Desventaja:** puede quedar atrapado en óptimos locales sin la repetición.

**Inicialización `k-means++`:**
- Algoritmo de Arthur & Vassilvitskii (2007). Primer centroide aleatorio; los siguientes se eligen con probabilidad proporcional a la distancia al centroide más cercano ya seleccionado.
- **Objetivo:** distribuir los centroides iniciales de forma esparcida para cubrir mejor el espacio.
- Inercia casi idéntica a `random` (318 474.31), converge en solo **63 iteraciones**.
- Tarda más tiempo (1.41s) porque la propia inicialización requiere calcular distancias. En datasets más grandes esta diferencia se compensa ampliamente.

**Inicialización `pca-init`:**
- Usa los primeros 10 componentes principales como centroides iniciales. Es determinista, por lo que solo se necesita `n_init=1`.
- Converge en **44 iteraciones** y en el **menor tiempo** (0.51s).
- La inercia final es ligeramente mayor (320 120.44): encuentra un óptimo local diferente.
- **¿Por qué converge tan rápido?** Los componentes PCA capturan las principales fuentes de variación; son buenos candidatos a centroides representativos, por lo que el algoritmo parte ya cercano a la solución final.

#### Conclusión del Benchmarking K-Means

- Para **máxima calidad** (menor inercia): `random` o `k-means++` (similares).
- Para **máxima velocidad** con calidad aceptable: `pca-init`.
- En la práctica, `k-means++` es el default de scikit-learn por su buen equilibrio.

---

### 4.1.2 Visualización con PCA 2D

Se proyectaron los 10 000 puntos a 2D con PCA y se ejecutó K-Means sobre esta proyección. El gráfico side-by-side muestra:

- **Panel izquierdo — Etiquetas reales:** las 10 clases se solapan considerablemente en 2D, reflejando que no son linealmente separables con sólo 2 componentes.
- **Panel derecho — Clusters K-Means:** los centroides (✕ negro) dividen el espacio en regiones de Voronoi (partición convexa).

**Observación clave:** K-Means divide el espacio en regiones convexas, pero Fashion-MNIST tiene clases con formas no convexas y solapamiento real. Clases visualmente similares (camisa vs. abrigo, sandalia vs. zapatilla) tienden a mezclarse en el mismo cluster.

---

### 4.1.3 Método del Codo (SSE vs. K)

Se ejecutó K-Means para K ∈ {1, …, 15} y se graficó la inercia (SSE):

**Comportamiento observado:**
- La inercia decrece **monotónicamente** con K (siempre se puede reducir añadiendo más clusters).
- Se busca un "codo": el punto donde la tasa de disminución cambia drásticamente.
- En Fashion-MNIST, el codo es **suave y difuso**, no pronunciado como en datasets sintéticos.
- El codo se observa aproximadamente en **K ≈ 8–12**, consistente con K=10 clases reales aunque sin señal perfectamente clara.

**¿Por qué el codo no marca exactamente K=10?**

1. **Clases similares visualmente:** camisa (6) y abrigo (4) comparten muchas características visuales. K-Means tiende a fusionarlas o dividirlas de forma distinta a las etiquetas humanas.
2. **Supuesto de esfericidad:** K-Means minimiza SSE, lo que implícitamente asume clusters esféricos y de tamaño similar. Las categorías de Fashion-MNIST no cumplen este supuesto.
3. **La inercia siempre baja:** con K=784 (un punto por cluster), la inercia sería 0. El codo es una heurística, no una garantía.

---

## 5. Sección 4.2 — DBSCAN

### ¿Cómo funciona DBSCAN?

**DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) es un algoritmo basado en densidad local:

1. Para cada punto, cuenta cuántos vecinos hay dentro del radio `eps`.
2. Un punto con ≥ `min_samples` vecinos es un **core point** (núcleo de cluster).
3. Los puntos alcanzables desde un core point (directa o transitivamente) forman un cluster.
4. Los puntos que no pertenecen a ningún cluster son **ruido** (label = -1).

**Ventajas sobre K-Means:**
- No requiere especificar K a priori.
- Puede encontrar clusters de formas arbitrarias (no sólo esféricos).
- Identifica automáticamente outliers/ruido.

**Desventajas:**
- Muy sensible a `eps` y `min_samples`.
- Dificultad con clusters de densidad variable.
- Escala mal en alta dimensión (por eso se usa PCA primero).

### Preprocesamiento: PCA con 30 componentes

```python
pca_30 = PCA(n_components=30, random_state=0)
X_train_pca = pca_30.fit_transform(X)   # shape: (10000, 30)
```

**¿Por qué 30 componentes?** Balance entre retener suficiente información (~70-80% de varianza) y reducir la dimensionalidad para que las distancias euclídeas sean más significativas.

---

### 4.2.1 Configuración Base (eps=3.0, min_samples=10)

| Métrica | Valor |
|---------|-------|
| Clusters encontrados | **2** |
| Porcentaje de ruido | **14.86%** |

**Interpretación:** Con estos parámetros, DBSCAN encuentra sólo 2 grandes clusters. Esto indica que la densidad del dataset es bastante uniforme en el espacio PCA-30: casi todos los puntos se conectan en pocos "super-grupos" de alta densidad. El 14.86% de puntos son outliers que no alcanzan la densidad mínima requerida.

**¿Por qué no 10 clusters?** Fashion-MNIST en el espacio PCA no tiene 10 regiones claramente separadas por densidad. Las fronteras entre clases son continuas, sin "vacíos" de densidad suficientes para que DBSCAN las separe.

---

### 4.2.2 Sensibilidad al Parámetro `eps` (con min_samples=10 fijo)

| eps | n_clusters | noise_pct |
|-----|-----------|-----------|
| 0.5 | 0 | 100.00% |
| 1.0 | 1 | 99.76% |
| 1.5 | 11 | 89.91% |
| 2.0 | 15 | 66.22% |
| **2.5** | **10** | **34.83%** |
| 3.0 | 2 | 14.86% |
| 4.0 | 1 | 2.10% |
| 5.0 | 1 | 0.33% |
| 7.0 | 1 | 0.00% |
| 10.0 | 1 | 0.00% |

**Análisis por rangos:**

- **eps muy pequeño (0.5–1.0):** El radio de vecindad es tan pequeño que casi ningún punto tiene suficientes vecinos → todos son ruido. Con eps=0.5, el 100% son ruido.

- **eps intermedio bajo (1.5–2.0):** Se fragmenta en muchos clusters pequeños (11–15). Las regiones densas se detectan pero los "puentes" entre clases no existen. Alto porcentaje de ruido (66–90%).

- **eps ≈ 2.5 (zona de interés):** Se obtienen exactamente **10 clusters** con 34.83% de ruido. Es el valor más cercano al número real de clases, aunque el ruido sigue siendo alto.

- **eps=3.0:** Los clusters se fusionan en sólo 2 mega-clusters. Los "puentes" de densidad entre clases vecinas ya conectan regiones que antes estaban separadas.

- **eps grande (4.0+):** Todo el dataset se funde en 1 cluster. El ruido desaparece porque cualquier distancia entre vecinos queda dentro del radio.

**Conclusión:** `eps` controla el "grano" de la partición. La "ventana" donde se obtiene un resultado útil (~10 clusters) es estrecha (entre 2.0 y 2.5 en este caso).

---

### 4.2.3 Sensibilidad al Parámetro `min_samples` (con eps=3.0 fijo)

| min_samples | n_clusters | noise_pct |
|------------|-----------|-----------|
| 2 | 69 | 8.32% |
| 5 | 7 | 11.17% |
| **10** | **2** | **14.86%** |
| 15 | 4 | 18.16% |
| 20 | 3 | 20.45% |
| 30 | 4 | 26.07% |
| 50 | 2 | 37.93% |

**Análisis:**

- **min_samples muy bajo (2):** Casi cualquier par de puntos cercanos forma un cluster → **69 micro-clusters** en su mayoría no significativos. Poco ruido porque casi cualquier punto califica como core point.

- **min_samples=5:** Reducción drástica a 7 clusters. Se requiere algo más de densidad para ser core point.

- **min_samples=10 (baseline):** 2 grandes clusters con 14.86% de ruido.

- **min_samples alto (15–50):** El ruido aumenta monotónicamente (de 18% a 38%) porque muchos puntos no tienen suficientes vecinos. El número de clusters varía entre 2 y 4 (no es monótono porque la topología de las regiones densas cambia).

**Patrón general de los hiperparámetros:**

| Cambio | Efecto en clusters | Efecto en ruido |
|--------|-------------------|----------------|
| eps ↑ | ↓ (fusión) | ↓ |
| eps ↓ | ↑ (fragmentación) | ↑ |
| min_samples ↑ | ↓ (menos core points) | ↑ |
| min_samples ↓ | ↑ (más core points) | ↓ |

---

### 4.2.4 Impacto de la Métrica de Distancia

| Métrica | eps usado | n_clusters | noise_pct |
|---------|----------|-----------|-----------|
| `euclidean` | 3.00 | 2 | 14.86% |
| `manhattan` | 10.00 | 14 | 43.69% |
| `cosine` | 0.05 | 7 | 39.35% |

**Análisis:**

- **Distancia euclídea (L2):** mide distancia en línea recta. La más natural después de PCA (componentes son ortogonales). Resultados más compactos.

- **Distancia manhattan (L1 / taxicab):** suma de diferencias absolutas por dimensión. Necesita eps=10.0 porque las distancias L1 son globalmente mayores que L2 en 30 dimensiones. La fragmentación en más clusters (14) sugiere que L1 separa mejor algunas regiones, aunque a costa de mucho ruido (43.69%).

- **Similitud coseno:** mide el ángulo entre vectores (ignora magnitud). eps=0.05 en escala coseno (0=idéntico, 2=opuesto). Útil cuando importa la orientación del vector más que su longitud. Produce 7 clusters con 39.35% de ruido.

**Nota importante:** al cambiar la métrica, `eps` debe reajustarse porque está expresado en las unidades de esa métrica. No existe un `eps` universal válido para todas las métricas.

---

### 4.2.5 Heurística k-Distancias para Elegir `eps`

El método consiste en:
1. Calcular la distancia al k-ésimo vecino más cercano para cada punto (con k = min_samples).
2. Ordenar estas distancias de menor a mayor.
3. Graficar y buscar el "codo" de la curva.

```python
k = 10
neighbors = NearestNeighbors(n_neighbors=k).fit(X_train_pca)
distances, _ = neighbors.kneighbors(X_train_pca)
k_distances = np.sort(distances[:, -1])
```

**¿Por qué funciona?**
- Puntos dentro de clusters tienen su k-ésimo vecino muy cerca → distancias bajas.
- Puntos en fronteras o baja densidad tienen su k-ésimo vecino lejos → distancias altas.
- El codo separa estas dos poblaciones y señala un `eps` natural.

En Fashion-MNIST (espacio PCA-30), el codo es moderadamente visible alrededor de **eps ≈ 2.5–3.0**, consistente con los resultados experimentales.

---

### 4.2.6 Visualización 2D Final (eps=3.0, min_samples=10)

En el scatterplot 2D:
- **Puntos grises** = ruido (~1 486 puntos, 14.86% del total).
- **Puntos coloreados** = los 2 clusters principales.

**Comparación con K-Means:**
- K-Means asigna todos los puntos obligatoriamente y produce 10 grupos bien delimitados.
- DBSCAN detecta ruido real pero con estos parámetros identifica sólo 2 grandes manchas.
- Las clases visualmente similares (sandalia/zapatilla, camisa/abrigo) forman regiones continuas de alta densidad que DBSCAN no puede separar sin un `eps` más pequeño (que a su vez incrementa el ruido drásticamente).

---

## 6. Sección 4.3 — Gaussian Mixture Models (GMM)

### ¿Cómo funciona un GMM?

Un **Modelo de Mezcla Gaussiana** modela los datos como superposición de K distribuciones gaussianas multivariadas. El ajuste se realiza con el algoritmo **EM (Expectation-Maximization)**:

1. **E-step:** calcular la probabilidad de que cada punto pertenezca a cada componente.
2. **M-step:** actualizar los parámetros (pesos, medias, covarianzas) para maximizar la verosimilitud.

---

### 4.3.1 GMM con K=10 Componentes (covariance_type='full')

**Tamaños de clusters GMM vs. K-Means:**

| Cluster | GMM | K-Means (k-means++) |
|---------|-----|---------------------|
| 0 | 1 587 | 1 249 |
| 1 | 1 216 | 1 103 |
| 2 | **415** | 1 188 |
| 3 | 1 209 | 1 262 |
| 4 | 1 085 | 1 538 |
| 5 | 789 | 388 |
| 6 | 947 | 408 |
| 7 | 838 | 1 684 |
| 8 | 1 460 | 459 |
| 9 | **454** | 721 |

**Observaciones:**
- GMM produce clusters de **tamaño más heterogéneo** que K-Means: rango 415–1587 vs. 388–1684.
- Dos clusters muy pequeños (415 y 454 puntos) probablemente corresponden a clases con forma muy distintiva (bolso, botín).
- K-Means tiende a equilibrar mejor los tamaños porque minimiza distancias con supuesto de covarianza esférica igual para todos.
- GMM detecta la geometría de cada grupo de forma independiente gracias a su matriz de covarianza propia.

---

### 4.3.2 Benchmarking de `covariance_type`

El tipo de covarianza determina la **forma que puede adoptar cada componente gaussiana**:

| covariance_type | Descripción | Flexibilidad | BIC (menor = mejor) |
|----------------|-------------|-------------|---------------------|
| `spherical` | Una sola varianza escalar por componente (esferas). Similar a K-Means. | Baja | Mayor |
| `diag` | Diagonal: varianza independiente por dimensión (elipsoides alineados con ejes). | Media | Intermedio |
| `tied` | Todas las componentes comparten la misma covarianza full. | Media | Intermedio |
| `full` | Cada componente tiene su propia covarianza completa (elipsoides arbitrarios). | Alta | Menor |

**¿Por qué mayor flexibilidad no siempre es mejor?**
Con más parámetros, el modelo puede sobreajustar. El BIC penaliza el número de parámetros, por lo que el modelo "ganador" no es siempre el más flexible, sino el que mejor equilibra ajuste y parsimonia.

`full` típicamente obtiene el menor BIC porque puede adaptarse a la forma real de cada cluster. En Fashion-MNIST, las categorías de ropa tienen distribuciones asimétricas y orientaciones distintas en el espacio PCA, lo que favorece covarianzas completas.

---

### 4.3.3 BIC / AIC vs. K

Se entrenaron GMMs con K ∈ {2, …, 15} para seleccionar el número óptimo de componentes:

**¿Qué son BIC y AIC?**

```
BIC = ln(n) · p - 2·ln(L_max)
AIC = 2·p    - 2·ln(L_max)
```

donde n = muestras, p = parámetros del modelo, L_max = verosimilitud máxima.

Ambos **penalizan la complejidad** (término `p`) y **premian el ajuste** (término `-2·ln(L_max)`).

**Comportamiento esperado / observado:**
- Ambas curvas disminuyen al principio: más componentes → mejor ajuste de los datos.
- En algún punto, la penalización por complejidad supera la ganancia → curva sube o se estabiliza.
- El **mínimo** indica el K "óptimo" según cada criterio.
- AIC tiende a seleccionar K más grandes (penaliza menos la complejidad que BIC).
- BIC es más conservador y suele elegir K menores.

**Comparación con el método del codo de K-Means:**

| Criterio | K-Means SSE | GMM BIC/AIC |
|---------|-------------|-------------|
| Comportamiento | Siempre decrece | Tiene mínimo |
| Selección de K | Heurístico (codo visual) | Estadístico (mínimo) |
| Información probabilística | No | Sí |

**En este dataset**, el mínimo de BIC se espera cerca de K=10, aunque puede variar con la submuestra y el tipo de covarianza. AIC suele preferir K ligeramente mayores.

---

### 4.3.4 Asignación Suave (Soft Assignment)

Una de las ventajas más importantes de GMM es la **asignación probabilística**:

```
Observación con asignación dominante:
[0.   0.   0.   0.   0.   0.   1.   0.   0.   0.]   → 100% en componente 6

Observación con asignación ambigua:
[0.   0.   0.   0.   0.   0.21 0.   0.   0.79 0.]   → 79% comp. 8, 21% comp. 5
```

**Interpretación:**

- **Asignación dominante (P=1.00):** el punto está en el núcleo denso de la componente 6. La imagen visual es una prenda claramente reconocible y sin ambigüedad.

- **Asignación ambigua (Top2=[0.79, 0.21]):** el punto está en la zona de superposición entre dos gaussianas. La imagen visual es probablemente una prenda limítrofe (p. ej., una camisa que se asemeja a un abrigo, o un botín que recuerda a una zapatilla).

**¿Por qué es útil la asignación suave?**

| Aplicación | Uso de la probabilidad de pertenencia |
|-----------|--------------------------------------|
| Detección de ambigüedad | Identificar puntos en zonas de frontera para revisión manual |
| Recomendación | Un ítem puede "pertenecer" parcialmente a varias categorías |
| Anomalías | Un punto con probabilidad máxima muy baja podría ser outlier |
| Contraste con K-Means | K-Means sólo da la etiqueta del cluster, sin "confianza" |

---

## 7. Comparativa Global de los Tres Algoritmos

| Característica | K-Means | DBSCAN | GMM |
|---------------|---------|--------|-----|
| **Tipo de asignación** | Dura | Dura + ruido | Suave (probabilística) |
| **K requerido a priori** | Sí | No | Sí |
| **Maneja outliers** | No | Sí (etiqueta -1) | Parcialmente (baja prob.) |
| **Forma de clusters** | Esférica (Voronoi) | Arbitraria | Elíptica (flexible) |
| **Sensibilidad a params** | Media (K) | Alta (eps, min_samples) | Media-Alta (K, cov. type) |
| **Base probabilística** | No | No | Sí |
| **Criterio selección K** | Codo SSE (heurístico) | k-distancias (heurístico) | BIC/AIC (estadístico) |
| **Velocidad** | Rápido | Lento en alta dimensión | Moderado |
| **Clusters encontrados** | 10 (forzado K=10) | 2 (eps=3.0, ms=10) | 10 (forzado K=10) |

### Resultados Numéricos Resumidos

| Algoritmo | Configuración | Clusters | Ruido |
|-----------|--------------|---------|-------|
| K-Means (`random`) | K=10, n_init=4 | 10 | 0% |
| K-Means (`k-means++`) | K=10, n_init=4 | 10 | 0% |
| K-Means (`pca-init`) | K=10, n_init=1 | 10 | 0% |
| DBSCAN | eps=2.5, ms=10 | **10** | 34.83% |
| DBSCAN | eps=3.0, ms=10 | 2 | 14.86% |
| GMM (`full`) | K=10 | 10 | 0% |

---

## 8. Conclusiones Finales

### Sobre el Dataset

Fashion-MNIST es **desafiante para clustering no supervisado** porque:
1. Las 10 clases no son linealmente separables en el espacio original (784D).
2. Clases visualmente similares (camisa/abrigo, sandalia/zapatilla) tienen representaciones muy cercanas en el espacio de píxeles.
3. La proyección PCA captura varianza global pero no necesariamente la información más discriminativa entre clases.
4. Esto explica por qué ningún algoritmo recupera perfectamente las 10 clases reales sin supervisión.

### Sobre K-Means

- Es el algoritmo más rápido y sencillo de usar en este contexto.
- Con K=10 y cualquier inicialización, obtiene 10 grupos, pero no necesariamente alineados con las 10 clases reales.
- La inicialización **PCA** converge en menos iteraciones; **k-means++** y **random** alcanzan mejor inercia final.
- El método del codo sugiere K ≈ 10 pero la señal es difusa en este dataset (clases solapadas, formas no esféricas).

### Sobre DBSCAN

- Extremadamente sensible a `eps` y `min_samples`: un cambio pequeño en `eps` puede pasar de 0% a 100% de ruido.
- El único valor que produce ~10 clusters (`eps=2.5`) genera 34.83% de ruido, lo que es muy alto.
- La calibración de hiperparámetros requiere tanto esfuerzo como elegir K en K-Means.
- La heurística k-distancias ayuda a calibrar `eps` de forma más sistemática.
- La métrica de distancia afecta significativamente los resultados; `euclidean` en el espacio PCA-30 es la más natural.
- Fue diseñado para clusters de densidad uniforme y formas arbitrarias; Fashion-MNIST tiene densidad continua sin separaciones claras.

### Sobre GMM

- Ofrece la mayor flexibilidad conceptual: distribuciones elípticas y asignación probabilística.
- El BIC/AIC proporciona un criterio de selección de K con fundamento estadístico sólido.
- La asignación suave es la característica más diferenciadora: permite medir la "confianza" de cada asignación y detectar puntos ambiguos en zonas frontera.
- `covariance_type='full'` es el más flexible y obtiene el menor BIC, pero también el más costoso computacionalmente.

### Recomendación Práctica

| Objetivo | Algoritmo recomendado |
|---------|----------------------|
| K grupos compactos y rápidos | **K-Means con k-means++** |
| Detección de outliers + forma irregular | **DBSCAN** (calibrar eps con k-distancias) |
| Confianza en la asignación + selección estadística de K | **GMM con BIC** |
| Cualquier algoritmo | Aplicar **PCA primero** para reducir dimensionalidad |

La reducción de dimensionalidad con **PCA** es prácticamente obligatoria antes de aplicar cualquiera de los tres algoritmos en datos de alta dimensión como imágenes de 784 píxeles.

---

*Documento generado a partir de `lab7_clustering.ipynb` — G05, Sesión 7.*  
*Dataset: Fashion-MNIST — submuestra de 10 000 muestras del conjunto de entrenamiento.*  
*Librerías: scikit-learn, numpy, matplotlib, pandas.*
