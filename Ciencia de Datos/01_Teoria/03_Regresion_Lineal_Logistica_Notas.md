# Regresión Lineal y Logística: Guía Completa

---

## 1. ¿Qué es la Regresión?

La regresión busca **modelar la relación** entre una variable que queremos predecir y las variables que usamos para predecirla.

- **Variable dependiente (Y)**: lo que queremos predecir.
- **Variables independientes (X)**: lo que usamos como entrada.

> Ejemplo: predecir el **tiempo de entrega** a partir de la distancia y el número de paquetes.
> ```
> Tiempo ≈ f(distancia, paquetes)
> ```

En la realidad no conocemos la función exacta que relaciona X con Y, así que la **aproximamos a partir de datos**.

---

## 2. El Modelo Lineal

La forma más simple de aproximar esa función es una **combinación lineal** de las variables:

```
f(x) = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ
```

### ¿Qué significa cada término?

| Término | Nombre | Significado |
|---|---|---|
| β₀ | Intercepto | Valor base cuando todas las X son 0 |
| βᵢ | Coeficiente | Cuánto influye cada variable en Y |
| xᵢ | Feature | Variable de entrada |

### Ejemplo concreto

```
Tiempo = 2 + 0.5 × distancia + 3 × paquetes
```

- Siempre hay **2 minutos** de tiempo base.
- Cada **km adicional** suma 0.5 min.
- Cada **paquete adicional** suma 3 min.

### ¿Por qué "lineal"?

Porque los coeficientes β multiplican linealmente a las variables. No hay exponentes ni interacciones. Esto lo hace simple e interpretable.

---

## 3. Representación Matricial

Cuando tienes muchos datos y muchas variables, se escribe de forma compacta:

```
f(x) = βᵀ x
```

- **β** es un vector con todos los coeficientes.
- **x** es un vector con todos los valores de entrada.

Usar matrices permite calcular todo de forma eficiente y es la base de la implementación en código.

---

## 4. Función de Costo

Para entrenar el modelo necesitamos medir qué tan mal estamos prediciendo. La función de costo más usada es el **Error Cuadrático Medio (MSE)**:

```
J(β) = (1/2) Σ (f(xₘ) - yₘ)²
```

- Compara cada predicción `f(xₘ)` con el valor real `yₘ`.
- Eleva al cuadrado para penalizar errores grandes más que pequeños.
- El factor 1/2 es solo para simplificar la derivada matemáticamente.

El objetivo del entrenamiento es **minimizar J(β)**: encontrar los β que hagan las predicciones más cercanas a la realidad.

---

## 5. Solución Analítica (Ecuación Normal)

Si derivamos J(β) e igualamos a cero, obtenemos la solución exacta de una sola vez:

```
β = (XᵀX)⁻¹ XᵀY
```

**Ventaja**: solución exacta, sin iteraciones.

**Desventajas**:
- Muy costoso computacionalmente con muchas variables (invertir una matriz grande es lento).
- La inversa puede no existir si hay variables redundantes (multicolinealidad).

> En la práctica se usa solo para datasets pequeños.

---

## 6. Descenso del Gradiente

La alternativa más usada: en vez de calcular la solución de una vez, **ajustamos los parámetros poco a poco**.

```
β ← β - α × ∂J/∂β
```

- `α` (alpha) es la **tasa de aprendizaje**: qué tan grandes son los pasos.
- Se repite hasta que el error deja de bajar.

**Intuición**: imagina que estás en una montaña con niebla y quieres bajar al valle. En cada paso, sientes hacia dónde baja el terreno (el gradiente) y das un paso en esa dirección.

### Tasa de aprendizaje α

| α muy grande | α muy pequeña |
|---|---|
| Salta por encima del mínimo | Converge muy lento |
| Puede diverger | Funciona bien pero tarda |

---

## 7. El Gradiente

El gradiente indica **en qué dirección y cuánto** ajustar cada coeficiente:

```
∂J/∂βᵢ = (f(x) - y) × xᵢ
```

- Si el **error es grande** → el ajuste es grande.
- Si la **variable xᵢ es importante** (valor alto) → mayor impacto en el ajuste.

---

## 8. Tipos de Descenso del Gradiente

| Tipo | Datos usados | Estabilidad | Velocidad |
|---|---|---|---|
| **Batch** | Todos los datos por iteración | Alta | Lento en datasets grandes |
| **Stochastic (SGD)** | Un dato por iteración | Ruidosa | Muy rápido |
| **Mini-batch** | Un subconjunto (ej. 32 datos) | Intermedia | El más usado en práctica |

---

## 9. Multicolinealidad

Ocurre cuando **dos o más variables de entrada están muy correlacionadas** entre sí.

> Ejemplo: incluir "altura en cm" y "altura en metros" al mismo tiempo.

**Consecuencias**:
- Los coeficientes β se vuelven inestables (cambian mucho con pequeñas variaciones en los datos).
- Dificulta la interpretación: no sabemos a cuál variable atribuir el efecto.

**Solución**: regularización (Ridge o Lasso) o eliminar una de las variables correlacionadas.

---

## 10. Regularización: Ridge y Lasso

Agregan una **penalización** a la función de costo para evitar coeficientes demasiado grandes (sobreajuste).

### Ridge (L2)

```
J = error + λ Σ βᵢ²
```

- Penaliza coeficientes grandes.
- **Reduce** los coeficientes pero no los elimina.
- Ideal cuando todas las variables son relevantes.

### Lasso (L1)

```
J = error + λ Σ |βᵢ|
```

- Penaliza el valor absoluto de los coeficientes.
- Puede llevar coeficientes exactamente a **cero** → **selección automática de variables**.
- Ideal cuando sospechas que muchas variables no aportan nada.

### ¿Qué es λ (lambda)?

Controla la intensidad de la penalización:
- λ = 0 → sin regularización (regresión normal).
- λ muy grande → todos los coeficientes tienden a 0 (modelo demasiado simple).

---

## 11. Métricas de Evaluación

### MSE — Error Cuadrático Medio
Promedio de los errores al cuadrado. Penaliza errores grandes.
```
MSE = (1/n) Σ (ŷ - y)²
```

### RMSE — Raíz del MSE
Misma unidad que Y, más interpretable.
```
RMSE = √MSE
```

### R² — Coeficiente de Determinación
Qué porcentaje de la variabilidad de Y explica el modelo.
```
R² ∈ [0, 1]   →   1 = perfecto,  0 = no explica nada
```

> Un R² de 0.85 significa que el modelo explica el 85% de la variación en Y.

---

## 12. Limitaciones de la Regresión Lineal

- No sirve bien para **clasificación** (predecir categorías).
- Asume una relación **lineal** entre X e Y; falla con relaciones curvas o complejas.
- Sensible a **outliers** (los errores al cuadrado los amplifican).
- Requiere que las variables sean **independientes** entre sí (problema de multicolinealidad).

---

## 13. Regresión Logística (para Clasificación)

Cuando Y es una **categoría** (sí/no, spam/no spam, etc.), la regresión lineal no funciona bien porque puede dar valores fuera de [0, 1]. La solución es aplicar la **función sigmoide** a la salida lineal:

```
p = 1 / (1 + e^(−βᵀx))
```

Esto convierte cualquier número real en una **probabilidad** entre 0 y 1.

- Si p ≥ 0.5 → clase 1.
- Si p < 0.5 → clase 0.

---

## 14. La Función Sigmoide

```
σ(z) = 1 / (1 + e^(−z))
```

| Valor de z | Salida σ(z) |
|---|---|
| z → −∞ | ≈ 0 |
| z = 0 | = 0.5 |
| z → +∞ | ≈ 1 |

- Siempre produce valores entre 0 y 1.
- Es suave y derivable → compatible con descenso del gradiente.

---

## 15. Entrenamiento: Log-Verosimilitud

En logística no se minimiza el MSE sino que se **maximiza la log-verosimilitud**: la probabilidad de que el modelo haya generado exactamente los datos observados.

```
ℓ(β) = Σ [ y·log(p) + (1−y)·log(1−p) ]
```

- Si `y = 1` y `p ≈ 1` → término alto (bien predicho).
- Si `y = 1` y `p ≈ 0` → término muy bajo (penalización fuerte).

En la práctica se **minimiza la pérdida logarítmica** (log-loss), que es el negativo de la log-verosimilitud.

---

## 16. Comparación: Lineal vs Logística

| Característica | Regresión Lineal | Regresión Logística |
|---|---|---|
| Tipo de salida | Número continuo | Probabilidad [0, 1] |
| Problema | Regresión | Clasificación |
| Función de salida | Identidad | Sigmoide |
| Función de costo | MSE | Log-loss |
| Interpretación β | Cambio en Y | Cambio en log-odds |

---

## 17. Conexión con Redes Neuronales

Una neurona artificial es esencialmente una regresión logística:

```
y = σ(wᵀx + b)
```

- `w` = pesos (equivalente a β).
- `b` = sesgo (equivalente a β₀).
- `σ` = función de activación (sigmoide u otras).

Una **red neuronal** apila muchas de estas neuronas en capas, lo que le permite aprender relaciones mucho más complejas.

---

## 18. Validación Cruzada

Para medir el desempeño **real** del modelo (su capacidad de generalizar) se usan técnicas de validación.

### Hold-out

Divide los datos una vez:
```
Datos → 80% Entrenamiento | 20% Test
```
Simple pero depende mucho de cómo se hizo la división.

### K-Fold Cross Validation

Divide los datos en K partes iguales y rota el conjunto de test:

```
Iteración 1: [Test][Train][Train][Train][Train]
Iteración 2: [Train][Test][Train][Train][Train]
...
Iteración K: [Train][Train][Train][Train][Test]
```

- Se entrena K veces y se promedia el error.
- Más robusto que hold-out.
- K=5 o K=10 son los valores más comunes.

**Ventaja**: usa todos los datos tanto para entrenar como para evaluar, dando una estimación más confiable del error real.

---

## Resumen General

```
DATOS
  ↓
Modelo lineal: f(x) = β₀ + β₁x₁ + ... + βₙxₙ
  ↓
Función de costo: mide el error (MSE)
  ↓
Optimización: descenso del gradiente ajusta los β
  ↓
Regularización (Ridge/Lasso): evita sobreajuste
  ↓
Evaluación: MSE, R², validación cruzada
  ↓
¿Salida continua?  → Regresión Lineal
¿Salida categórica? → Regresión Logística (+ sigmoide)
```

| Concepto | Para qué sirve |
|---|---|
| Coeficientes β | Cuantifican el efecto de cada variable |
| Descenso del gradiente | Método iterativo de aprendizaje |
| Ridge / Lasso | Controlan sobreajuste y multicolinealidad |
| Sigmoide | Convierte salida lineal en probabilidad |
| K-Fold CV | Estima el error real del modelo |
