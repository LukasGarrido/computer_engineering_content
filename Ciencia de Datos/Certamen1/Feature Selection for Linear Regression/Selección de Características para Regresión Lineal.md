
Este documento detalla las técnicas para seleccionar las variables más importantes en un modelo de regresión, mejorando la precisión y reduciendo la complejidad (sobreajuste).

---

## 1. ¿Qué es Feature Selection?

Es el proceso de reducir el número de variables de entrada al desarrollar un modelo predictivo. Su objetivo es:
* Simplificar los modelos para hacerlos más interpretables.
* Reducir el tiempo de entrenamiento.
* Evitar la "maldición de la dimensionalidad".
* Mejorar la generalización reduciendo el **Overfitting**.

---

## 2. Técnicas de Selección de Características

El documento clasifica las técnicas supervisadas en tres categorías principales:

### A. Métodos de Filtro (Filters)
Se basan en las características estadísticas de los datos, independientemente del algoritmo de aprendizaje.
* **Missing Value Ratio:** Eliminar variables con demasiados datos faltantes.
* **Information Gain:** Mide la reducción de entropía.
* **Chi-square Test:** Evalúa la independencia entre variables.
* **Fisher's Score:** Clasifica variables según su poder discriminatorio.

### B. Métodos Envolventes (Wrappers)
Utilizan un algoritmo de aprendizaje específico como "caja negra" para evaluar subconjuntos de variables.
* **Forward Selection:** Comienza sin variables y añade la mejor una a una.
* **Backward Elimination:** Comienza con todas y elimina la menos significativa.
* **Recursive Feature Elimination (RFE):** Elimina variables de forma recursiva basándose en los pesos del modelo.

### C. Métodos Integrados (Embedded)
La selección ocurre durante el proceso de entrenamiento del modelo.
* **Lasso (Regularización L1):** Puede reducir los coeficientes de algunas variables a cero, eliminándolas efectivamente.
* **Ridge (Regularización L2):** Reduce los coeficientes pero no los hace cero (mantiene todas las variables pero con menos peso).
* **Random Forest Importance:** Calcula la importancia basada en la disminución de la impureza en los nodos.



---

## 3. Regularización: Ridge vs. Lasso

La regularización añade una penalización a la función de pérdida para evitar que los coeficientes crezcan demasiado.

* **Ridge ($L2$):** Añade el cuadrado de la magnitud de los coeficientes. Es ideal cuando hay muchas variables relacionadas entre sí (multicolinealidad).
* **Lasso ($L1$):** Añade el valor absoluto de la magnitud. Es útil para la **selección automática de variables** ya que descarta las menos importantes.



---

## 4. Diagnóstico del Modelo: QQ Plots

Para validar que un modelo de regresión es confiable, se analizan los **residuos** (la diferencia entre el valor real y el predicho).

* **QQ Plot (Quantile-Quantile Plot):** Es una herramienta visual para verificar el supuesto de **normalidad**.
* **Interpretación:** Si los puntos siguen una línea recta diagonal, los residuos son normales. Si hay curvas en los extremos o forma de S, existen desviaciones sistemáticas que requieren transformar los datos (ej. aplicar logaritmo) o usar modelos robustos.



---

## 5. Ejemplo de Código (Scikit-Learn)

### Implementación de Recursive Feature Elimination (RFE)
```python
from sklearn.datasets import make_regression
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression

# Generar datos de ejemplo
X, y = make_regression(n_samples=100, n_features=10, n_informative=5)

# Definir el modelo base
model = LinearRegression()

# Configurar RFE para seleccionar las 5 mejores variables
selector = RFE(model, n_features_to_select=5, step=1)
selector = selector.fit(X, y)

# Ver cuáles fueron seleccionadas
print("Variables seleccionadas:", selector.support_)
print("Ranking de variables:", selector.ranking_)