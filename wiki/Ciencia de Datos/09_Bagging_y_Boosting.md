# Bagging y Boosting — Guía Detallada
**EIN087B - Ciencia de Datos | Universidad Técnica Federico Santa María**

---

## 1. Errores en Machine Learning

Antes de entender Bagging y Boosting, es fundamental conocer los tres tipos de error que afectan a los modelos de ML:

| Tipo de error | Descripción | Causa |
|---|---|---|
| **Bias (Sesgo)** | Error por suposiciones demasiado fuertes del modelo | Modelo muy simple (underfitting) |
| **Variance (Varianza)** | Sensibilidad a pequeñas variaciones en los datos de entrenamiento | Modelo muy complejo (overfitting) |
| **Noise (Ruido)** | Error inherente a los datos | Irreducible, no depende del modelo |

### Relación Sesgo–Varianza

La relación entre sesgo y varianza está directamente vinculada a la **complejidad del modelo**:

- **Baja complejidad** → Alto sesgo, baja varianza → *Underfitting*
- **Alta complejidad** → Bajo sesgo, alta varianza → *Overfitting*

El objetivo es encontrar el punto de equilibrio ("sweet spot") donde ambos errores son mínimos.

> **¿Cómo ayudan Bagging y Boosting?**
> - **Bagging** → Reduce la **varianza**
> - **Boosting** → Reduce el **sesgo** (y también puede ayudar con la varianza)

---

## 2. Métodos Basados en Árboles

### ¿Qué son?

Los métodos basados en árboles dividen el espacio de predictores en regiones rectangulares, y para cada región se predice el **promedio** (regresión) o la **clase mayoritaria** (clasificación) de las observaciones de entrenamiento que caen en ella.

Son simples e interpretables, pero suelen tener **menor precisión** que otros métodos avanzados. Por eso se combinan mediante Bagging, Random Forests y Boosting.

---

## 3. Árboles de Regresión

### Funcionamiento

Un árbol de regresión divide el espacio de predictores en `J` regiones no superpuestas `R1, R2, ..., RJ`. Para toda observación en una región `Rj`, la predicción es:

$$\hat{y}_{R_j} = \text{promedio de } y_i \text{ para } i \in R_j$$

### Ejemplo: Dataset Hitters

Se construye un árbol para predecir `log(salario)` de jugadores de béisbol usando `Years` (años jugados) y `Hits` (hits del año anterior). Las tres regiones resultantes son:

| Región | Condición | Salario estimado |
|---|---|---|
| R1 | `Years < 4.5` | e^5.107 ≈ **$165,174** |
| R2 | `Years ≥ 4.5` y `Hits < 117.5` | e^5.999 ≈ **$402,834** |
| R3 | `Years ≥ 4.5` y `Hits ≥ 117.5` | e^6.740 ≈ **$845,346** |

**Interpretación:**
- `Years` es el factor más importante: los jugadores con poca experiencia ganan menos.
- Para jugadores con menos de 4.5 años, los hits tienen poco impacto.
- Entre jugadores experimentados, más hits se traducen en mayor salario.

### Estructura del Árbol

- **Nodos internos**: puntos de división (ej. `Years < 4.5`)
- **Hojas / Nodos terminales**: regiones finales (R1, R2, R3)
- **Ramas**: conexiones entre nodos

---

## 4. Construcción del Árbol: División Binaria Recursiva

Dado que considerar todas las posibles particiones es computacionalmente inviable, se utiliza un enfoque **voraz (greedy) top-down**:

### Procedimiento

1. Se comienza con todos los datos en una sola región.
2. Se selecciona el predictor `Xj` y punto de corte `s` que generan las dos regiones:

$$R_1(j,s) = \{X \mid X_j < s\}, \quad R_2(j,s) = \{X \mid X_j \geq s\}$$

3. Se elige la combinación `(j, s)` que minimiza el RSS residual:

$$\sum_{i \in R_1} (y_i - \hat{y}_{R_1})^2 + \sum_{i \in R_2} (y_i - \hat{y}_{R_2})^2$$

4. Se repite el proceso **iterativamente** sobre las regiones existentes, hasta cumplir un criterio de parada (ej. menos de 5 observaciones por nodo).

> **Limitación:** La división binaria recursiva solo puede generar particiones **paralelas a los ejes**, por lo que ciertas estructuras complejas no pueden representarse exactamente.

---

## 5. Poda del Árbol (Tree Pruning)

Un árbol grande puede **sobreajustar** los datos de entrenamiento. La solución es construir primero un árbol grande `T0` y luego podarlo.

### Cost Complexity Pruning

Se busca el subárbol `T ⊆ T0` que minimice la función objetivo:

$$\sum_{m=1}^{|T|} \sum_{i \in R_m} (y_i - \hat{y}_{R_m})^2 + \alpha |T|$$

Donde:
- `|T|` = número de nodos terminales
- `α ≥ 0` = parámetro de regularización (penaliza la complejidad)

**Interpretación de α:**
- `α = 0` → árbol completo `T0`
- `α` grande → subárboles más pequeños

### Algoritmo Completo

1. **Crecer** el árbol completo con división binaria recursiva.
2. **Podar** con cost complexity pruning para obtener una secuencia de subárboles según `α`.
3. **Seleccionar α** mediante validación cruzada de K pliegues (se minimiza el MSE promedio).
4. **Retornar** el subárbol correspondiente al α óptimo.

---

## 6. Árboles de Clasificación

Son análogos a los de regresión, pero predicen una **respuesta categórica**. En cada nodo terminal se predice la **clase más frecuente**.

### Criterios de División

Como el RSS no aplica para respuestas categóricas, se usan otras métricas:

#### Tasa de error de clasificación
$$E = 1 - \max_k \hat{p}_{mk}$$
Poco sensible para construir árboles.

#### Índice de Gini
$$G = \sum_{k=1}^{K} \hat{p}_{mk}(1 - \hat{p}_{mk})$$
Mide la **impureza del nodo**. Valores pequeños indican que la mayoría pertenece a una sola clase.

#### Entropía
$$D = -\sum_{k=1}^{K} \hat{p}_{mk} \log \hat{p}_{mk}$$
Mide la **incertidumbre** de la distribución de clases.

> **Práctica recomendada:**
> - Para **crecer** el árbol → usar Gini o Entropía (más sensibles a la pureza)
> - Para **podar** el árbol → usar tasa de error (relacionada con el desempeño final)

---

## 7. Árboles vs. Modelos Lineales

| Característica | Modelo Lineal | Árbol de Decisión |
|---|---|---|
| Frontera de decisión | Lineal | Paralela a los ejes (no lineal) |
| Rendimiento si la frontera es lineal | Mejor | Peor |
| Rendimiento si la frontera es no lineal | Peor | Mejor |
| Interpretabilidad | Alta | Alta |

---

## 8. Métodos de Ensamble (Ensemble Methods)

Un método de ensamble combina múltiples modelos simples (**weak learners**) para construir un modelo más robusto y preciso.

---

## 9. Bagging (Bootstrap Aggregating)

### Idea Central

Promediar predicciones **reduce la varianza**. Si se tienen B predicciones individuales:

$$\hat{f}_{bag}(x) = \frac{1}{B} \sum_{b=1}^{B} \hat{f}_b(x)$$

### Procedimiento para Regresión

1. Generar `B` muestras bootstrap del conjunto de entrenamiento (muestreo con reemplazo).
2. Entrenar un árbol **profundo y sin podar** para cada muestra.
3. Promediar las `B` predicciones.

> Cada árbol tiene alta varianza pero bajo sesgo. Promediarlos **reduce la varianza** sin aumentar el sesgo.

### Procedimiento para Clasificación

En lugar de promediar, se realiza **votación mayoritaria**: la clase más votada entre los `B` árboles es la predicción final.

### Ventajas

- Se pueden usar cientos o miles de árboles **sin riesgo de sobreajuste**.
- El número de árboles `B` no es un hiperparámetro sensible.

### Estimación OOB (Out-of-Bag)

Dado que cada muestra bootstrap usa ~2/3 de los datos, el ~1/3 restante (**OOB**) puede usarse para estimar el error de prueba **sin validación cruzada**:

- Para cada observación `i`, se predice usando solo los árboles donde fue OOB (~B/3 árboles).
- Se promedia (regresión) o se vota por mayoría (clasificación).
- Con `B` suficientemente grande, el error OOB ≈ error de leave-one-out CV.

---

## 10. Random Forests

### Mejora sobre Bagging: Descorrelación de Árboles

Random Forest agrega un paso clave: en **cada división** de cada árbol, solo se considera un subconjunto aleatorio de `m` predictores (en lugar de los `p` disponibles).

$$m \approx \sqrt{p}$$

### ¿Por qué funciona?

- Si hay un predictor muy dominante, en Bagging todos los árboles lo usarán como primera división → árboles muy correlacionados → el promedio no reduce mucho la varianza.
- Con Random Forest, al limitar a `m` predictores, los árboles se **descorrelacionan** → el promedio reduce más la varianza.

### Comparación de rendimiento

| Método | Comportamiento |
|---|---|
| Single Tree | ~45.7% error de clasificación |
| Bagging (m = p) | Mejora respecto a un solo árbol |
| Random Forest (m < p) | Mejora adicional sobre Bagging |

> Si `m = p`, Random Forest equivale a Bagging.

---

## 11. Boosting

### Idea Central

A diferencia del Bagging, en Boosting los árboles se construyen **secuencialmente**, donde cada árbol corrige los errores del modelo anterior.

- **No** usa muestreo bootstrap.
- Cada árbol se ajusta a los **residuos** del modelo actual: `ri = yi − f̂(xi)`
- Se usan árboles pequeños (**stumps**) para evitar sobreajuste.
- El aprendizaje se regula con un parámetro de contracción `λ`.

### Algoritmo de Boosting para Regresión

```
Parámetros: B (número de árboles), d (profundidad), λ (shrinkage)

1. Inicializar: f̂(x) = 0, ri = yi para todo i
2. Para b = 1, ..., B:
   a) Ajustar árbol f̂b con d divisiones a los residuos {ri}
   b) Actualizar modelo: f̂(x) ← f̂(x) + λ·f̂b(x)
   c) Actualizar residuos: ri ← ri − λ·f̂b(xi)
3. Resultado final: f̂(x) = Σ λ·f̂b(x)
```

### Hiperparámetros Clave

| Parámetro | Descripción | Notas |
|---|---|---|
| **B** (número de árboles) | Más árboles → mejor ajuste, posible overfitting | Elegir con validación cruzada |
| **λ** (shrinkage) | Velocidad de aprendizaje | Típicamente 0.01 o 0.001; menor λ requiere mayor B |
| **d** (divisiones por árbol) | Complejidad de cada árbol | d=1 genera stumps (modelos aditivos) |

> El sobreajuste en Boosting ocurre **lentamente** a medida que crece B.

---

## 12. Comparación General

| Característica | Bagging | Random Forest | Boosting |
|---|---|---|---|
| Construcción | Paralela | Paralela | Secuencial |
| Muestreo | Bootstrap | Bootstrap | Sin remuestreo |
| Predictores por split | Todos (p) | Subconjunto (m) | Todos (p) |
| Reduce | Varianza | Varianza | Sesgo (y varianza) |
| Riesgo de overfitting | Bajo | Bajo | Moderado (controlar B y λ) |
| Interpretabilidad | Baja | Baja | Baja |

---

## 13. Resumen Visual del Flujo

```
Datos originales
     │
     ├──── BAGGING ────────────► Bootstrap x B ──► B árboles profundos ──► Promedio/Votación
     │
     ├──── RANDOM FOREST ──────► Bootstrap x B ──► B árboles (m < p) ───► Promedio/Votación
     │
     └──── BOOSTING ───────────► Árbol 1 sobre residuos ──► Árbol 2 sobre nuevos residuos ──► ... ──► Suma ponderada
```

---

*Material basado en la clase EIN087B - Ciencia de Datos, Prof. Jorge Portilla G., UTFSM, Concepción.*
