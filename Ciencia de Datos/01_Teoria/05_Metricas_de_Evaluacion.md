
Este documento resume los conceptos fundamentales sobre la evaluación de algoritmos de Machine Learning, basándose en la guía de la Universidad Técnica Federico Santa María.

---

## 1. Estrategias de Validación de Modelos

Para medir qué tan bien generaliza un modelo, se utilizan técnicas de división de datos:

* **Hold-out (Conjunto de prueba):** Se divide el dataset en dos partes:
    * **Entrenamiento ($S_{train}$):** Para ajustar los parámetros del modelo.
    * **Validación/Prueba ($S_{cv}$):** Para evaluar el rendimiento en datos no vistos. (Ej: 75% entrenamiento, 25% prueba).
* **K-Fold Cross Validation:** Se divide el dataset en $K$ partes iguales. El modelo se entrena $K$ veces, usando cada vez un pliegue distinto como conjunto de prueba y los demás como entrenamiento. Se reporta el promedio de los resultados.

---

## 2. Evaluación de Clasificación

### La Matriz de Confusión
Es la herramienta base para entender dónde falla un clasificador binario:

| | Predicho Positivo | Predicho Negativo |
|---|---|---|
| **Real Positivo** | Verdadero Positivo (TP) | Falso Negativo (FN) |
| **Real Negativo** | Falso Positivo (FP) | Verdadero Negativo (TN) |

### Métricas Derivadas
* **Precision (Precisión):** ¿De todos los que predije como positivos, cuántos lo eran?  
    $Precision = \frac{TP}{TP + FP}$
* **Sensitivity / Recall (Sensibilidad):** ¿De todos los casos reales positivos, cuántos detectó el modelo?  
    $Recall = \frac{TP}{TP + FN}$
* **Specificity (Especificidad):** Capacidad del modelo para detectar los casos negativos.  
    $Specificity = \frac{TN}{TN + FP}$
* **F1-Score:** Promedio armónico entre Precision y Recall. Útil cuando hay clases desbalanceadas.

---

## 3. Curva ROC y AUC

La **Curva ROC** (Receiver Operating Characteristic) es una representación gráfica del rendimiento de un clasificador:
* **Eje Y:** Tasa de Verdaderos Positivos (Sensibilidad).
* **Eje X:** Tasa de Falsos Positivos ($1 - Especificidad$).

**AUC (Area Under the Curve):**
* Representa la probabilidad de que el modelo clasifique un ejemplo positivo aleatorio por encima de uno negativo aleatorio.
* **AUC = 1.0:** Clasificador perfecto.
* **AUC = 0.5:** Clasificador aleatorio (sin valor predictivo).

---

## 4. Optimización de Modelos

### Parámetros vs. Hiperparámetros
* **Parámetros:** Se aprenden durante el entrenamiento (ej. pesos en una regresión).
* **Hiperparámetros:** Se definen manualmente antes de entrenar (ej. valor de $K$ en KNN o profundidad de un árbol).

### Estrategias de Búsqueda
1.  **Grid Search:** Prueba exhaustivamente todas las combinaciones posibles de una lista de valores definida.
2.  **Random Search:** Selecciona combinaciones aleatorias dentro de un rango, siendo más eficiente en términos de tiempo de cómputo.

---

## 5. Ejemplo de Código (Scikit-Learn)

### Generación de Curva ROC
```python
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# y_true: valores reales, y_scores: probabilidades del modelo
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], linestyle='--') # Línea base aleatoria
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()