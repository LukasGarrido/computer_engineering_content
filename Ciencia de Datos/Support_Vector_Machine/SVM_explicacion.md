# Support Vector Machine (SVM)
> Resumen de la clase EIN087B – Ciencia de Datos · Prof. Jorge Portilla G. · UTFSM

---

## 1. ¿Qué es una SVM?

Las **Máquinas de Soporte Vectorial** (Support Vector Machines) son algoritmos de aprendizaje supervisado usados para **clasificación** y **regresión**. Son ampliamente utilizadas en reconocimiento de patrones, análisis de imágenes y procesamiento de lenguaje natural.

Fueron desarrolladas en los años 90 por **Vladimir N. Vapnik** y sus colegas, publicadas formalmente en 1995.

La SVM es una generalización del **clasificador de margen máximo** (Maximal Margin Classifier), extendido mediante el **Support Vector Classifier (SVC)**, que a su vez se amplía con la SVM completa usando kernels.

---

## 2. Hiperplano

Un **hiperplano** es una frontera de decisión que separa puntos de datos de diferentes clases en un espacio de alta dimensión.

- En **2D**: es una línea → β₀ + β₁X₁ + β₂X₂ = 0
- En **3D**: es un plano
- En **N dimensiones**: tiene (N–1) dimensiones → β₀ + β₁X₁ + … + βₚXₚ = 0

### Posición de un punto respecto al hiperplano

Un punto X puede estar:
- **Sobre el hiperplano**: la ecuación = 0
- **A un lado**: la ecuación > 0
- **Al otro lado**: la ecuación < 0

Esto permite usarlo como **regla de clasificación**: el signo del resultado indica la clase.

---

## 3. Maximal Margin Classifier (MMC)

Cuando los datos son linealmente separables, existen infinitos hiperplanos posibles. El **MMC** elige el hiperplano que está **más alejado** de todas las observaciones de entrenamiento.

- La **distancia mínima** de cualquier observación al hiperplano se llama **margen**.
- El MMC maximiza ese margen.
- Los puntos más cercanos al hiperplano (sobre las líneas punteadas del margen) se llaman **vectores de soporte (SV)**.
- El hiperplano solo depende de los SV: mover otros puntos no lo afecta (siempre que no crucen el margen).

### Problema de optimización del MMC

$$\max_{\beta_0, \beta_1, \ldots, \beta_p, M} M$$

Sujeto a:
$$\sum_{j=1}^{p} \beta_j^2 = 1$$
$$y_i(\beta_0 + \beta_1 x_{i1} + \cdots + \beta_p x_{ip}) \geq M \quad \forall i$$

La normalización garantiza que las distancias no dependan de un factor de escala.

> **Limitación:** Si las clases no son perfectamente separables, el problema no tiene solución con M > 0.

---

## 4. Support Vector Classifier (SVC)

El SVC es una extensión del MMC que permite **violaciones suaves del margen** ("soft margin"), tolerando que algunas observaciones estén en el lado incorrecto.

### ¿Por qué es necesario?

El MMC es muy sensible a observaciones individuales (puede cambiar drásticamente si se agrega un solo punto) y tiende al **sobreajuste**.

### Problema de optimización del SVC

$$\max_{\beta_0, \ldots, \beta_p, \xi_1, \ldots, \xi_n, M} M$$

Sujeto a:
$$\sum_{j=1}^{p} \beta_j^2 = 1$$
$$y_i(\beta_0 + \beta_1 x_{i1} + \cdots + \beta_p x_{ip}) \geq M(1 - \xi_i) \quad \forall i$$
$$\xi_i \geq 0, \quad \sum_{i=1}^{n} \xi_i \leq C$$

### Variables de holgura ξᵢ

| Valor de ξᵢ | Interpretación |
|---|---|
| ξᵢ = 0 | Observación en el lado correcto del margen |
| 0 < ξᵢ ≤ 1 | Observación violó el margen (lado incorrecto del margen, pero lado correcto del hiperplano) |
| ξᵢ > 1 | Observación en el lado incorrecto del hiperplano (error de clasificación) |

### El parámetro C

- **C = 0**: equivale al MMC (sin violaciones).
- **C pequeño**: margen más estrecho, menos tolerancia → mayor varianza, posible sobreajuste.
- **C grande**: margen más amplio, más tolerancia → menor varianza, mejor generalización.
- C se elige mediante **validación cruzada** y controla el **trade-off sesgo-varianza**.

---

## 5. Support Vector Machine (SVM)

La SVM extiende el SVC para manejar **fronteras de decisión no lineales** mediante el uso de **kernels**.

### Idea clave: el truco del kernel

En lugar de calcular productos internos directamente:
$$\langle x_i, x_{i'} \rangle = \sum_{j=1}^{p} x_{ij} x_{i'j}$$

Se reemplaza por una función kernel:
$$\Omega(x_i, x_{i'})$$

Un **kernel** cuantifica la similitud entre dos observaciones, pero puede hacerlo en espacios de muy alta dimensión de forma eficiente (sin calcular explícitamente las coordenadas en ese espacio).

La función de clasificación queda:
$$f(x) = \beta_0 + \sum_{i=1}^{n} \alpha_i \, \Omega(x, x_i)$$

---

## 6. Tipos de Kernels

### Kernel Lineal

$$\Omega(x_i, x_{i'}) = \sum_{j=1}^{p} x_{ij} x_{i'j}$$

Equivale al SVC estándar. Cuantifica similitud mediante correlación de Pearson.

---

### Kernel Polinómico

$$\Omega(x_i, x_{i'}) = \left(1 + \gamma \sum_{j=1}^{p} x_{ij} x_{i'j}\right)^d$$

- **d**: grado del polinomio (controla la complejidad de la frontera).
- **γ**: influencia de los términos de interacción.
- Útil cuando los datos tienen estructura polinómica.

---

### Kernel de Base Radial (RBF / Gaussiano)

$$\Omega(x_i, x_{i'}) = \exp\left(-\gamma \sum_{j=1}^{p} (x_{ij} - x_{i'j})^2\right)$$

- Mapea los datos a un espacio de **dimensión infinita**.
- Captura patrones complejos y no lineales.
- Es el **kernel por defecto** en `sklearn.svm.SVC`.
- El parámetro γ por defecto en sklearn usa la escala:

$$\gamma = \frac{1}{n_{\text{features}} \cdot \sigma^2(X)}$$

---

### Kernel Sigmoide

Otro kernel popular para datos con estructuras similares a redes neuronales.

---

## 7. Comparación de los tres clasificadores

| Concepto | MMC | SVC | SVM |
|---|---|---|---|
| Frontera de decisión | Lineal | Lineal (suave) | No lineal (via kernel) |
| Viola el margen | No | Sí (controlado por C) | Sí (controlado por C) |
| Maneja datos no separables | No | Sí | Sí |
| Usa kernels | No | No | Sí |

---

## 8. Ejemplo numérico de clasificación

Dado el hiperplano: `f(x) = 1.5·x₁ + 1.5·x₂ – 8/3`

Para clasificar el punto **(2, 2)**:

```
f(2,2) = 1.5(2) + 1.5(2) – 2.67 = 6 – 2.67 ≈ 3.33
```

Como f(2,2) > 0 → el punto pertenece a la **clase +1**.

---

## 9. Resumen general

```
Datos linealmente separables
        ↓
  Maximal Margin Classifier (MMC)
        ↓ (si hay ruido o no separabilidad perfecta)
  Support Vector Classifier (SVC)  ← agrega margen suave (C)
        ↓ (si la frontera es no lineal)
  Support Vector Machine (SVM)     ← agrega kernels (RBF, polinómico, etc.)
```

Las SVM son poderosas porque:
- Solo dependen de un subconjunto pequeño de puntos (**vectores de soporte**).
- Funcionan bien en espacios de alta dimensión.
- Son flexibles gracias al truco del kernel.
