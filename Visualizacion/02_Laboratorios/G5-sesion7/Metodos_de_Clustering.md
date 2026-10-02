# Métodos de Clustering: K-Means, DBSCAN y GMM

**Curso:** EIN092B - Visualización

---
## 1. K-Means

### 1.1 Idea central

K-Means es un **método basado en distancia al centroide**: cada cluster se representa por un punto central (el *centroide*, el promedio de todos los puntos que pertenecen a ese grupo), y cada observación se asigna al cluster cuyo centroide le quede más cerca.

### 1.2 Supuestos implícitos

- **Clusters de forma esférica:** como la asignación se basa en la distancia euclidiana al centroide, K-Means funciona mejor cuando los grupos reales tienen una forma redondeada (circular en 2D, esférica en más dimensiones). Si un cluster tiene forma alargada, en "media luna" o anidada dentro de otro, K-Means tiende a cortarlo de forma incorrecta.
- **Clusters de tamaño similar:** el algoritmo tiende a repartir los puntos de forma relativamente pareja entre los K grupos, por lo que le cuesta identificar correctamente un cluster mucho más pequeño (o disperso) que otro.
- **Número de clusters K conocido de antemano:** a diferencia de DBSCAN, K-Means **necesita que el usuario le diga cuántos grupos buscar** antes de ejecutarlo. Elegir mal el valor de K puede fusionar grupos reales o dividir un grupo en dos.

### 1.3 Algoritmo (paso a paso)

1. **Elegir K** (el número de clusters) y posicionar K centroides iniciales, usualmente de forma aleatoria entre los datos.
2. **Asignación:** cada punto se asigna al centroide más cercano (típicamente usando distancia euclidiana).
3. **Actualización:** cada centroide se recalcula como el promedio de todos los puntos que le fueron asignados.
4. **Repetir** los pasos 2 y 3 hasta que las asignaciones ya no cambien (convergencia) o se alcance un número máximo de iteraciones.

Matemáticamente, K-Means busca minimizar la **suma de distancias cuadradas** entre cada punto y el centroide de su cluster (la *inercia* o *WCSS*, Within-Cluster Sum of Squares):

```
J = Σ (i=1 a K) Σ (x en cluster i) ||x − μᵢ||²
```

donde μᵢ es el centroide del cluster i.

### 1.4 Cómo elegir K

Como K debe fijarse antes de correr el algoritmo, se usan heurísticas como:

- **Método del codo (elbow method):** graficar la inercia (J) en función de K, y elegir el punto donde la curva deja de bajar bruscamente (el "codo").
- **Coeficiente de silueta (silhouette score):** mide qué tan bien separado está cada punto respecto a clusters vecinos; se elige el K que maximiza este puntaje.

### 1.5 Ventajas y desventajas

| Ventajas | Desventajas |
|---|---|
| Simple, rápido y escala bien a datasets grandes | Requiere definir K de antemano |
| Fácil de interpretar (el centroide resume cada grupo) | Asume clusters esféricos y de tamaño similar |
| Converge en pocas iteraciones | Sensible a la posición inicial de los centroides (puede converger a un óptimo local distinto en cada corrida) |
| Funciona bien cuando los clusters realmente son compactos y separados | No maneja bien outliers: un punto atípico puede desplazar significativamente un centroide |
| | Asignación "dura": cada punto pertenece a un único cluster, sin medida de incertidumbre |

---

## 2. DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

### 2.1 Idea central

DBSCAN es un **método basado en densidad**: en lugar de definir clusters por su cercanía a un centroide, define un cluster como una **región del espacio donde los puntos están densamente agrupados**, separada de otras regiones por zonas de baja densidad. Fue propuesto por Ester et al. (1996).

### 2.2 Conceptos clave

DBSCAN necesita dos parámetros:

- **ε (epsilon):** el radio de vecindad alrededor de cada punto.
- **MinPts:** el número mínimo de puntos que debe haber dentro de ese radio ε para considerar una región como "densa".

Con esos dos parámetros, cada punto se clasifica en una de tres categorías:

- **Punto núcleo (core point):** tiene al menos MinPts vecinos dentro de su radio ε (incluyéndose a sí mismo).
- **Punto borde (border point):** no cumple el mínimo de vecinos por sí solo, pero está dentro del radio ε de un punto núcleo.
- **Punto de ruido (noise / outlier):** no es núcleo ni borde de ningún cluster — queda sin asignar a ningún grupo.

Un cluster se forma conectando puntos núcleo que son vecinos entre sí (y los puntos borde que cuelgan de ellos), de forma similar a cómo se "expande" una mancha de tinta por una región densa.

### 2.3 Algoritmo (paso a paso)

1. Elegir ε y MinPts.
2. Para cada punto no visitado, contar cuántos vecinos tiene dentro del radio ε.
3. Si tiene al menos MinPts vecinos, se marca como punto núcleo y se crea un nuevo cluster (o se une a uno existente), expandiéndose a todos sus vecinos alcanzables por densidad (vecinos de vecinos, mientras sigan siendo núcleos).
4. Los puntos que caen dentro del radio de un núcleo pero no son núcleo ellos mismos se marcan como borde, y se asignan a ese cluster.
5. Los puntos que no cumplen ninguna de las condiciones anteriores quedan marcados como **ruido**.

### 2.4 Por qué no necesita K de antemano

El número de clusters **emerge naturalmente** de la estructura de densidad de los datos y de los parámetros ε/MinPts: el algoritmo simplemente va conectando regiones densas, y cuantas "islas" de densidad resulten determinan cuántos clusters se forman. Esto es una diferencia fundamental respecto a K-Means.

### 2.5 Ventajas y desventajas

| Ventajas | Desventajas |
|---|---|
| No requiere especificar el número de clusters K | Requiere elegir ε y MinPts, que no siempre son intuitivos de definir |
| Puede encontrar clusters de **forma arbitraria** (no solo esféricos: espirales, medias lunas, etc.) | Le cuesta manejar clusters con **densidades muy distintas** entre sí (un único ε puede ser adecuado para un cluster denso y demasiado pequeño/grande para otro) |
| Identifica explícitamente los **outliers** como "ruido", en vez de forzarlos dentro de algún cluster | Puede ser más lento que K-Means en datasets muy grandes, según la implementación |
| Robusto frente a la forma de los grupos | La elección de ε es sensible a la escala de los datos (conviene normalizar las variables primero) |

---

## 3. GMM (Gaussian Mixture Models)

### 3.1 Idea central

GMM es un **método probabilístico**: en vez de asignar cada punto a un único cluster de forma definitiva, asume que los datos fueron generados por una **mezcla de K distribuciones gaussianas** (normales multivariadas), cada una con su propia media (centro) y matriz de covarianza (forma y orientación). El algoritmo estima los parámetros de esas K gaussianas y, para cada punto, calcula la **probabilidad** de pertenecer a cada una de ellas.

### 3.2 Formulación

La densidad de probabilidad de un punto x bajo una mezcla de K gaussianas es:

```
p(x) = Σ (k=1 a K) πₖ · N(x | μₖ, Σₖ)
```

donde:

- **πₖ** es el peso (proporción) del cluster k en la mezcla, con Σπₖ = 1.
- **N(x | μₖ, Σₖ)** es la densidad gaussiana con media μₖ y matriz de covarianza Σₖ.

Los parámetros (πₖ, μₖ, Σₖ para cada k) se estiman habitualmente con el **algoritmo EM (Expectation-Maximization)**:

1. **Paso E (Expectation):** con los parámetros actuales, calcular para cada punto la probabilidad (responsabilidad) de pertenecer a cada gaussiana.
2. **Paso M (Maximization):** con esas probabilidades, recalcular los parámetros (medias, covarianzas y pesos) de cada gaussiana para maximizar la verosimilitud de los datos.
3. Repetir E y M hasta convergencia.

### 3.3 Asignación "suave" vs. "dura"

Esta es la diferencia conceptual más importante frente a K-Means:

- **K-Means (asignación dura):** cada punto pertenece a **un único cluster**, el del centroide más cercano. No hay noción de "cuán seguro" está el modelo de esa asignación.
- **GMM (asignación suave / probabilística):** cada punto recibe un **vector de probabilidades**, una por cada cluster (por ejemplo, 70% cluster 1, 25% cluster 2, 5% cluster 3). Esto permite expresar la incertidumbre cuando un punto está en una zona ambigua, entre dos grupos.

Si se necesita una asignación final única, normalmente se elige el cluster con mayor probabilidad (esto se conoce como *hard assignment* derivado de un modelo *soft*), pero la información probabilística completa queda disponible si se necesita.

### 3.4 Flexibilidad de forma

Gracias a que cada gaussiana tiene su propia **matriz de covarianza** (no solo su media), GMM puede modelar clusters:

- **Elípticos**, no solo esféricos (a diferencia de K-Means).
- **De distinto tamaño y orientación** entre sí, porque cada componente gaussiana tiene sus propios parámetros independientes.

De hecho, K-Means puede entenderse como un **caso particular** de GMM, donde se fuerza a que todas las covarianzas sean iguales, esféricas y con asignación dura en vez de probabilística.

### 3.5 Ventajas y desventajas

| Ventajas | Desventajas |
|---|---|
| Asignación probabilística (suave), captura incertidumbre | Sigue requiriendo especificar K de antemano |
| Modela clusters elípticos, de distinto tamaño y orientación | Supone que los datos siguen distribuciones gaussianas — si la forma real es muy distinta (ej. forma de anillo), el ajuste será pobre |
| Marco probabilístico riguroso, permite usar criterios como AIC/BIC para elegir K | Puede converger a óptimos locales según la inicialización, igual que K-Means |
| Generaliza a K-Means (más flexible) | Computacionalmente más costoso que K-Means |

---

## 4. Comparación general

| Característica | K-Means | DBSCAN | GMM |
|---|---|---|---|
| Enfoque | Distancia al centroide | Densidad de puntos | Probabilístico (mezcla de gaussianas) |
| Forma de clusters asumida | Esférica, tamaño similar | Arbitraria | Elíptica (tamaño y orientación variables) |
| ¿Requiere K de antemano? | Sí | No | Sí |
| Tipo de asignación | Dura (única) | Dura, + categoría de "ruido" | Suave (probabilística) |
| Maneja outliers explícitamente | No | Sí (los marca como ruido) | No directamente (se les puede asignar baja probabilidad en todos los clusters) |
| Sensibilidad a inicialización | Alta | No aplica (es determinista dado ε y MinPts) | Alta |
| Costo computacional | Bajo | Medio | Medio-alto |
| Cuándo conviene usarlo | Grupos compactos, redondeados y de tamaño parecido, dataset grande | Grupos de forma irregular, presencia de outliers, número de clusters desconocido | Grupos con formas elípticas o superpuestas, se necesita incertidumbre de la asignación |

---

## 5. Cómo elegir entre los tres

1. **¿Sospechas que hay outliers que no deberían forzarse dentro de ningún grupo?** → DBSCAN.
2. **¿No sabes cuántos clusters hay y la forma de los grupos puede ser irregular?** → DBSCAN.
3. **¿Los grupos son razonablemente redondeados, de tamaño similar, y priorizas velocidad y simplicidad?** → K-Means.
4. **¿Necesitas saber qué tan "segura" es cada asignación, o los clusters pueden tener formas elípticas / solaparse entre sí?** → GMM.
5. **¿Tienes un dataset muy grande y necesitas algo rápido como primera aproximación?** → Empieza con K-Means (usando el método del codo o silueta para elegir K) y, si los resultados no son satisfactorios, prueba DBSCAN o GMM según el problema que observes.
