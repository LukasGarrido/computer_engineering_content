# Regresión Lineal y Logística — Explicación Completa

## 1. Introducción

La regresión es uno de los métodos más utilizados en estadística y aprendizaje automático.

### ¿Qué hace realmente?
Busca modelar la relación entre variables:
- Variable dependiente (lo que queremos predecir): Y
- Variables independientes (lo que usamos para predecir): X

### Ejemplo
Queremos predecir el tiempo de entrega:
- X1 = distancia
- X2 = número de paquetes

Entonces:
Tiempo ≈ f(distancia, paquetes)

### ¿Por qué es importante?
Porque en la realidad:
- No conocemos la función exacta
- Necesitamos aproximarla a partir de datos

---

## 2. Modelo Lineal

El modelo más simple es:

f(x) = β0 + β1x1 + β2x2 + ... + βn xn

### ¿Qué significa cada término?

- β0: intercepto (valor base cuando todo es 0)
- βi: cuánto influye cada variable
- xi: variables de entrada

### Ejemplo concreto

Tiempo = 2 + 0.5 * distancia + 3 * paquetes

Interpretación:
- Siempre hay 2 minutos base
- Cada km agrega 0.5 min
- Cada paquete agrega 3 min

### ¿Por qué es lineal?
Porque es una combinación lineal de variables.

---

## 3. Representación Matricial

f(x) = βᵀ x

### ¿Por qué usar matrices?
- Simplifica cálculos
- Permite trabajar con muchos datos
- Hace eficiente la optimización

---

## 4. Función de Costo

J(β) = (1/2) Σ (f(xm) - ym)^2

### ¿Qué significa?
- Mide el error entre predicción y valor real
- Penaliza errores grandes

### ¿Por qué minimizarla?
Porque buscamos el modelo que menos se equivoque

---

## 5. Solución Analítica

β = (XᵀX)^(-1) XᵀY

### ¿Por qué funciona?
Porque se obtiene al derivar el error y encontrar el mínimo.

### Problema
- Costoso computacionalmente
- Puede no existir la inversa

---

## 6. Descenso del Gradiente

β = β - α * gradiente

### Idea
Ir ajustando los parámetros poco a poco para minimizar el error.

### Ejemplo intuitivo
Como bajar una montaña buscando el punto más bajo.

---

## 7. Gradiente

∂J/∂βi = (f(x) - y) * xi

### Interpretación
- Error grande → ajuste grande
- Variable importante → mayor impacto

---

## 8. Tipos de Gradiente

### Batch
- Usa todos los datos
- Más estable

### Stochastic (SGD)
- Usa un dato a la vez
- Más rápido
- Más ruidoso

---

## 9. Curse of Dimensionality

### Problema
Muchísimas variables → espacio enorme → pocos datos útiles

### Consecuencia
Se necesitan muchos datos para aprender bien

---

## 10. Multicolinealidad

### ¿Qué es?
Variables muy correlacionadas

### Problema
- Coeficientes inestables
- Difícil interpretación

---

## 11. Regresión Ridge (L2)

J = error + λ Σ β²

### ¿Por qué?
Evitar coeficientes grandes y sobreajuste

### Efecto
Modelo más estable

---

## 12. Regresión Lasso (L1)

J = error + λ Σ |β|

### Característica clave
Puede eliminar variables (coeficientes = 0)

---

## 13. Métricas

### MSE
Promedio de errores al cuadrado

### R²
Qué tanto explica el modelo

---

## 14. Limitaciones de Regresión Lineal

No sirve bien para:
- Clasificación
- Relaciones no lineales

---

## 15. Regresión Logística

Se usa para clasificación

p = 1 / (1 + e^(-βᵀx))

### ¿Por qué?
Convierte resultados en probabilidades

---

## 16. Función Sigmoide

- Valores entre 0 y 1
- Suave y continua

---

## 17. Entrenamiento (Log-Verosimilitud)

ℓ(β) = Σ [ y log(p) + (1-y) log(1-p) ]

### ¿Por qué?
Maximiza la probabilidad de observar los datos

---

## 18. Gradiente en Logística

∂ℓ/∂β = (y - f(x)) x

---

## 19. Comparación

### Regresión Lineal
- Predice valores continuos

### Regresión Logística
- Predice probabilidades

---

## 20. Redes Neuronales

y = σ(wᵀx + b)

Es una extensión de la regresión logística

---

## 21. Validación Cruzada

### Hold-out
Divide datos en entrenamiento y prueba

### K-Fold
Divide en K partes y rota el entrenamiento

### Ventaja
Mejor estimación del error real

---

## 22. Idea General

El objetivo es:
- Modelar relaciones
- Minimizar error
- Generalizar bien

---

## Resumen

- Regresión lineal: ajustar una recta
- Gradiente: método de aprendizaje
- Ridge/Lasso: evitar sobreajuste
- Logística: clasificación
- Validación: medir desempeño real