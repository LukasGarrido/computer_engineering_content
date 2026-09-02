# K-Nearest Neighbors y K-Means: Explicación Detallada
**EIN087B - Ciencia de Datos | UTFSM**

---

## Tabla de Contenidos
1. [Distancia de Minkowski](#1-distancia-de-minkowski)
2. [K-Means Clustering](#2-k-means-clustering)
3. [Inercia (kmeans.inertia_)](#3-inercia-kmeansinertia_)
4. [Método del Codo (Elbow Method)](#4-método-del-codo-elbow-method)
5. [K-Means++](#5-k-means)
6. [MiniBatch K-Means](#6-minibatch-k-means)
7. [K-Nearest Neighbors (KNN)](#7-k-nearest-neighbors-knn)
8. [KNN Regressor](#8-knn-regressor)
9. [Comparativa Final: KNN vs K-Means](#9-comparativa-final-knn-vs-k-means)

---

## 1. Distancia de Minkowski

### ¿Qué es?
La **distancia de Minkowski** es una generalización de las distancias Euclidiana y Manhattan. Es la métrica base que usan muchos algoritmos de machine learning (incluyendo KNN) para medir qué tan "lejos" están dos puntos en el espacio de características.

### Fórmula

$$d_{Minkowski}(P_1, P_2) = \left( |x_2 - x_1|^p + |y_2 - y_1|^p \right)^{\frac{1}{p}}$$

Donde **p** es un parámetro que controla el tipo de distancia calculada.

### Casos especiales según el valor de p

| Valor de p | Nombre | Fórmula | Descripción |
|---|---|---|---|
| `p = 1` | **Manhattan** | $\|x_{a1} - x_{b1}\| + \|x_{a2} - x_{b2}\|$ | Suma de diferencias absolutas. Camino en cuadrícula (como en una ciudad). |
| `p = 2` | **Euclidiana** | $\sqrt{(x_{a1}-x_{b1})^2 + (x_{a2}-x_{b2})^2}$ | Línea recta entre dos puntos. La más intuitiva. |
| `p → ∞` | **Chebyshev** | $\max\{\|x_{a1} - x_{b1}\|, \|x_{a2} - x_{b2}\|\}$ | Toma el máximo de las diferencias absolutas entre coordenadas. |

### Derivación de la distancia Chebyshev
Cuando `p → ∞`, uno de los términos domina al otro. Si `a = |x2 - x1|` y `b = |y2 - y1|`, y suponemos `a ≥ b`:

$$d_\infty = \lim_{p \to \infty}(a^p + b^p)^{1/p} \approx \lim_{p \to \infty}(a^p)^{1/p} = a = \max(a, b)$$

> **Intuición visual:** Imagina que p controla la "forma" del espacio. Con p=1 te mueves en ángulos rectos, con p=2 en línea recta, y con p=∞ solo importa la dimensión donde los puntos más difieren.

---

## 2. K-Means Clustering

### ¿Qué es?
K-Means es un algoritmo de **aprendizaje no supervisado** que agrupa observaciones en **K clusters**, donde cada observación pertenece al cluster cuyo centroide (punto central) está más cercano.

- **Objetivo:** Minimizar la suma de distancias entre los puntos y su centroide de cluster.
- **Tipo:** Clustering / Particionamiento.
- **Requiere:** Definir K (número de clusters) de antemano.

### Pasos del Algoritmo

```
1. Elegir el número de clusters K
2. Seleccionar K puntos aleatorios como centroides iniciales
3. Asignar cada punto al centroide más cercano (distancia euclidiana)
4. Recalcular los centroides como la media de todos los puntos asignados a ese cluster
5. Repetir pasos 3 y 4 hasta que los centroides no cambien (convergencia)
```

### Ilustración del proceso

**Iteración 0 — Inicialización:**
```
Datos sin etiquetar → Se seleccionan 3 centroides al azar (puntos rojos)
```

**Iteración 1 — Asignación:**
```
Cada punto se asigna al centroide más cercano
→ Se forman 3 grupos (rojo, verde, azul)
```

**Iteración 2 — Actualización:**
```
Se recalcula la posición de cada centroide como la MEDIA de los puntos de su cluster
→ Los centroides se mueven
```

**Iteración N — Convergencia:**
```
Los centroides dejan de moverse → El algoritmo terminó
```

### Ejemplo concreto (del PDF)
Con un dataset sintético (`make_blobs`) de 1000 ejemplos y 2 características:
- Se definen **K = 3** clusters.
- Se inicializan centroides aleatoriamente.
- Tras varias iteraciones, los 3 clusters quedan bien separados en el espacio 2D.

---

## 3. Inercia (kmeans.inertia_)

### Definición
La **inercia** mide qué tan bien están agrupados los puntos dentro de sus clusters. Se define como la **Suma de los Errores al Cuadrado (SSE)**:

$$SSE = \sum_{i=1}^{n} \min_{c \in \{1,...,K\}} \| x_i - \mu_c \|^2$$

Donde:
- `n` = número de puntos de datos
- `K` = número de clusters
- `x_i` = vector de características del punto i
- `µ_c` = centroide del cluster c
- `||x_i - µ_c||²` = distancia al cuadrado del punto i al centroide c

### Interpretación

| Inercia | Significado |
|---|---|
| **Baja** | Los puntos están **cerca** de su centroide → Clusters compactos y bien definidos ✅ |
| **Alta** | Los puntos están **lejos** de su centroide → Clusters dispersos o mal formados ❌ |

> **Nota importante:** A medida que aumenta K, la inercia siempre disminuye. Con K igual al número de puntos, la inercia sería 0 (cada punto es su propio cluster). Por eso necesitamos el Método del Codo para elegir K óptimo.

---

## 4. Método del Codo (Elbow Method)

### ¿Para qué sirve?
Ayuda a identificar el **K óptimo** sin necesidad de conocer las etiquetas reales de los datos.

### Procedimiento
1. Entrenar K-Means para distintos valores de K (ej: K = 1, 2, 3, ..., 10).
2. Registrar la inercia (SSE) para cada K.
3. Graficar K vs. SSE.
4. Buscar el **"codo"**: el punto donde la reducción de la inercia se vuelve menos pronunciada.

### Interpretación del gráfico

```
SSE
│ ●
│  ●
│    ●
│      ●  ← CODO (K óptimo)
│        ● ● ● ● ●
└────────────────────── K
  1  2  3  4  5  6 ...
```

En el ejemplo del PDF, el codo aparece en **K = 3**, lo que indica que 3 es el número óptimo de clusters para ese dataset.

> **Limitación:** El codo no siempre es obvio. En datos reales puede ser difuso y requerir criterios adicionales (como el índice Silhouette).

---

## 5. K-Means++

### El problema con K-Means clásico
La calidad del clustering depende **fuertemente** de la inicialización de los centroides. Una mala inicialización puede llevar a:
- Convergencia en mínimos locales.
- Clusters de baja calidad.

### Solución: K-Means++
Introduce una estrategia de inicialización **inteligente**:

```
1. Seleccionar el PRIMER centroide aleatoriamente.
2. Para cada punto restante, calcular D(x): distancia mínima al centroide más cercano ya elegido.
3. Seleccionar el SIGUIENTE centroide con probabilidad proporcional a D(x)²:

         D(x)²
P(x) = ─────────────────
        Σ D(x)² (todos los puntos)

4. Repetir hasta tener K centroides.
```

### Ventaja clave
Los puntos **más alejados** de los centroides actuales tienen **mayor probabilidad** de ser elegidos como nuevos centroides. Esto garantiza que los centroides iniciales estén bien distribuidos por todo el espacio de datos.

### Comparación práctica (sobre dataset de dígitos manuscritos)

| Método de inicialización | Tiempo | Inercia | Homogeneidad | V-Measure | Silhouette |
|---|---|---|---|---|---|
| **k-means++** | 0.050s | 69,545 | 0.598 | 0.621 | 0.152 |
| **Random** | 0.064s | 69,735 | 0.681 | 0.701 | 0.170 |
| **PCA-based** | 0.017s | 69,513 | 0.600 | 0.622 | 0.162 |

#### Métricas de evaluación explicadas:
- **Homogeneidad:** ¿Cada cluster contiene solo puntos de una misma clase?
- **Completitud:** ¿Todos los puntos de una clase están en el mismo cluster?
- **V-Measure:** Media armónica de homogeneidad y completitud (balance entre ambas).
- **ARI (Adjusted Rand Index):** Similitud entre la agrupación obtenida y una de referencia, ajustada por azar.
- **AMI (Adjusted Mutual Information):** Similar al ARI pero basado en información mutua.
- **Silhouette:** Qué tan similar es un punto a su propio cluster vs. otros clusters. Va de -1 a 1 (valores cercanos a 1 son mejores).

---

## 6. MiniBatch K-Means

### Motivación
K-Means estándar recalcula los centroides en **cada iteración sobre TODOS los datos**, lo cual es computacionalmente costoso para datasets grandes.

### Solución: MiniBatchKMeans
En lugar de usar todos los datos, usa **mini-batches** (subconjuntos aleatorios) en cada iteración.

### Algoritmo

```
1. Tomar un mini-batch aleatorio del dataset.
2. Asignar cada muestra del mini-batch al centroide más cercano.
3. Actualizar los centroides (pero solo a partir del mini-batch actual).
4. Repetir hasta convergencia o número máximo de iteraciones.
```

### Fórmula de actualización de centroides

$$C_{t+1} = C_t + \frac{1}{N_i}(x_i - C_t)$$

Donde:
- `C_t` = posición actual del centroide en iteración t
- `C_{t+1}` = nueva posición del centroide
- `x_i` = punto del mini-batch asignado al centroide
- `N_i` = número de puntos asignados al centroide hasta la iteración i

> Esta actualización es **incremental**: el cambio en el centroide se vuelve más pequeño a medida que se procesan más puntos, estabilizando su posición con el tiempo.

### Diferencia clave respecto a K-Means

| Característica | K-Means | MiniBatchKMeans |
|---|---|---|
| Datos usados por iteración | **Todos** | **Mini-batch (subconjunto)** |
| Velocidad | Más lento | **Más rápido** |
| Calidad del resultado | Mejor | Ligeramente inferior |
| Actualización de centroides | Media de todos los puntos del cluster | Promedio acumulado incremental |

---

## 7. K-Nearest Neighbors (KNN)

### Concepto fundamental
KNN es un algoritmo de **aprendizaje supervisado** (a diferencia de K-Means que es no supervisado). Puede usarse tanto para **clasificación** como para **regresión**.

### Características principales
- **No paramétrico:** No asume ninguna forma funcional para los datos.
- **Lazy learning:** No hay fase de entrenamiento real; el modelo simplemente memoriza todos los datos de entrenamiento.
- **Instancia-based:** La predicción se basa en la similitud con instancias almacenadas.

### ¿Cómo funciona? (Clasificación)

```
Dado un punto nuevo x₀ a clasificar:

1. CALCULAR DISTANCIA entre x₀ y TODOS los puntos del set de entrenamiento.
2. SELECCIONAR los K puntos más cercanos (vecinos más cercanos → N₀).
3. ASIGNAR la clase más frecuente entre esos K vecinos.
```

### Fórmula matemática
La probabilidad estimada de que `x₀` pertenezca a la clase `j` es:

$$\Pr(Y = j \mid X = x_0) = \frac{1}{K} \sum_{i \in N_0} \mathbb{1}(y_i = j)$$

Donde `I(y_i = j)` es 1 si el vecino `i` pertenece a la clase `j`, y 0 en caso contrario.

La clasificación final asigna `x₀` a la clase con mayor probabilidad estimada.

### Ejemplo visual (K=3)
```
Datos de entrenamiento:
  ★ ★ ★  (Clase A)
  ▲ ▲ ▲  (Clase B)
     ?    (Punto nuevo)

Con K=3, los 3 vecinos más cercanos son:
  1 × ★ (Clase A)
  2 × ▲ (Clase B)

→ Voto mayoritario: Clase B (2 votos vs 1)
→ El punto se clasifica como Clase B
```

### Elección del parámetro K

| K pequeño (ej: K=1) | K grande (ej: K=20) |
|---|---|
| Alta sensibilidad a outliers | Menor efecto de outliers |
| Fronteras de decisión complejas | Fronteras de decisión más suaves |
| Posible overfitting | Posible underfitting |
| Alta varianza | Alto sesgo |

> Del ejemplo con el dataset de vino tinto: K=1 tiene el mayor accuracy (≈0.67) pero es muy sensible a outliers. Se elige **K=12** como balance (accuracy ≈ 0.59).

### Parámetros relevantes en scikit-learn

```python
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(
    n_neighbors=12,       # Número de vecinos (K)
    metric='minkowski',   # Métrica de distancia (por defecto)
    p=2                   # p=2 → distancia Euclidiana; p=1 → Manhattan
)
```

### Ventajas y desventajas

**Ventajas:**
- Simple de entender e implementar.
- No requiere suposiciones sobre la distribución de los datos.
- Naturalmente multi-clase.

**Desventajas:**
- **Costoso computacionalmente:** en inferencia debe calcular distancias a TODOS los puntos de entrenamiento.
- **Sensible a outliers** (especialmente con K pequeño).
- **Maldición de la dimensionalidad:** con muchas features, las distancias pierden significado.
- El tamaño del modelo crece con el dataset (se almacenan todos los datos).

### Ordenamiento de vecinos: Bubble Sort y Merge Sort
Para encontrar los K vecinos más cercanos, se necesita ordenar las distancias. El PDF menciona dos algoritmos de ordenamiento usados en este contexto:

**Bubble Sort:** Compara pares adyacentes e intercambia si están en el orden incorrecto. Sencillo pero O(n²).

**Merge Sort:** Divide recursivamente el arreglo en mitades, ordena cada mitad y las combina. Más eficiente: O(n log n).

---

## 8. KNN Regressor

### Diferencia con KNN Clasificador
En lugar de asignar una **clase**, el KNN Regressor predice un **valor numérico continuo**.

### Proceso

```
1. Calcular distancias entre el punto nuevo y los puntos de entrenamiento.
2. Seleccionar los K puntos más cercanos.
3. El valor predicho = MEDIA (o promedio ponderado) de los valores de esos K vecinos.
```

### Consideraciones
- **K pequeño:** Captura más ruido (alta varianza).
- **K grande:** Predicción demasiado general (alto sesgo).
- Se puede usar distancia Euclidiana, Manhattan o Minkowski.

---

## 9. Comparativa Final: KNN vs K-Means

| Característica | K-Means | KNN |
|---|---|---|
| **Tipo de aprendizaje** | No supervisado | Supervisado |
| **Tarea** | Clustering | Clasificación / Regresión |
| **Requiere etiquetas** | ❌ No | ✅ Sí |
| **Fase de entrenamiento** | Iterativa (ajuste de centroides) | Ninguna (lazy learning) |
| **Fase de inferencia** | Asignar al centroide más cercano | Calcular distancias a todos los puntos |
| **Parámetro K** | Número de clusters | Número de vecinos |
| **Métrica de distancia** | Euclidiana (por defecto) | Minkowski / Euclidiana / Manhattan |
| **Sensibilidad a outliers** | Media | Alta (con K pequeño) |
| **Escalabilidad** | MiniBatch mejora esto | Baja (crece con el dataset) |

---

## Resumen de Conceptos Clave

```
DISTANCIA DE MINKOWSKI
  p=1 → Manhattan (bloques de ciudad)
  p=2 → Euclidiana (línea recta) ← más usada
  p=∞ → Chebyshev (diferencia máxima)

K-MEANS (no supervisado)
  → Agrupa datos en K clusters
  → Minimiza SSE (inercia)
  → Método del Codo para elegir K
  → K-Means++ mejora la inicialización
  → MiniBatchKMeans acelera el cómputo

KNN (supervisado)
  → Clasifica/predice según los K vecinos más cercanos
  → No requiere entrenamiento (lazy)
  → Sensible a K, outliers y dimensionalidad
  → KNN Regressor predice valores continuos
```

---

*Documento generado a partir de la presentación "K-nearest Neighbors and K-means Algorithms" — EIN087B Ciencia de Datos, UTFSM.*
