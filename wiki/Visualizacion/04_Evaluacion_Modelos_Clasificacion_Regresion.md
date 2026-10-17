---
tags:
  - visualizacion
  - teoria
  - metricas-de-evaluacion
  - machine-learning
aliases:
  - "Evaluación de Modelos de Clasificación y Regresión"
  - "C9 Visualización"
  - "Curva ROC y SHAP"
asignatura: "Visualización"
tipo: teoria
created: 2026-10-10
---

# Evaluación e Interpretación de Algoritmos de Clasificación y Regresión

> Técnicas de evaluación cuantitativa y visual de modelos de aprendizaje supervisado, curvas ROC/AUC, validación cruzada y explicabilidad mediante valores SHAP. Apuntes correspondientes a la Sesión 9 (C9) — EIN092B (Prof. Jorge Portilla).

---

## 1. Fundamentos de la Evaluación y Groundtruth

En el aprendizaje supervisado, el rendimiento de un modelo se evalúa contrastando sus predicciones frente a una verdad predefinida de referencia:

- **Groundtruth:** Información recolectada y etiquetada a priori que representa la condición real u objetiva para resolver un problema.
- Permite cuantificar objetivamente la discrepancia entre el valor observado y el predicho por el algoritmo.
- En problemas continuos (regresión), mide distancias o errores numéricos. En problemas discretos (clasificación), cuenta aciertos y fallos por categoría.

---

## 2. Clasificación Binaria: Matriz de Confusión y Métricas

En clasificación binaria, las predicciones del modelo se clasifican en cuatro categorías fundamentales frente al groundtruth:

| Concepto | Sigla | Definición |
|---|:---:|---|
| **Verdadero Positivo** | **TP** | El modelo detecta una condición real (evento positivo en la realidad y predicho como positivo). |
| **Falso Negativo** | **FN** | El modelo no detecta una condición real existente (positivo real predicho como negativo). Error tipo II. |
| **Falso Positivo** | **FP** | El modelo reporta una situación irreal (negativo real predicho como positivo). Falsa alarma / Error tipo I. |
| **Verdadero Negativo** | **TN** | El modelo descarta correctamente un caso no existente (negativo en la realidad y predicho como negativo). |

### 2.1 Matriz de Confusión (Confusion Matrix)

Es una herramienta visual matricial que organiza las instancias clasificadas:
- Filas: Clases reales (Groundtruth).
- Columnas: Clases predichas por el modelo (o transpuestas, según convención).
- **Ventaja clave:** Permite diagnosticar de inmediato si el modelo se confunde entre clases específicas, y evita el sesgo de la exactitud global cuando las clases están desbalanceadas (por ejemplo: si una clase minoritaria tiene 10 muestras y la mayoritaria 990, predecir siempre la clase mayoritaria da 99% de exactitud pero 0% de sensibilidad).

### 2.2 Métricas de Rendimiento

A partir de TP, TN, FP y FN se definen:

$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$
*Capacidad del modelo de no clasificar erróneamente un negativo como positivo (evitar falsas alarmas).*

$$\text{Sensitivity (Sensibilidad / Recall / TPR)} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
*Capacidad de encontrar y capturar todos los casos positivos reales en el dataset.*

$$\text{Specificity (Especificidad / TNR)} = \frac{\text{TN}}{\text{TN} + \text{FP}}$$
*Tasa de verdaderos negativos contra todo lo que no debía generar respuesta.*

$$\text{F-score (F1)} = 2 \cdot \frac{\text{Precision} \cdot \text{Sensitivity}}{\text{Precision} + \text{Sensitivity}}$$
*Media armónica entre precisión y sensibilidad; penaliza desequilibrios extremos entre ambas.*

$$\text{Accuracy (Exactitud)} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}$$
*Proporción global de predicciones correctas.*

---

## 3. Curvas ROC y Área Bajo la Curva (AUC)

La **Curva ROC** (*Receiver Operating Characteristic*) es una representación gráfica del rendimiento de un clasificador binario a medida que varía su umbral de decisión.

- **Eje Y:** True Positive Rate ($\text{TPR} = \text{Sensibilidad}$).
- **Eje X:** False Positive Rate ($\text{FPR} = 1 - \text{Especificidad} = \frac{\text{FP}}{\text{FP} + \text{TN}}$).

```text
TPR (Sensibilidad)
1.0 ┌───────────────────* Ideal (0,1)
    │                  /
    │              . ' 
    │          . '      Curva ROC típica
    │      . '          (AUC > 0.5)
    │  . '
    │'  Línea diagonal del azar (AUC = 0.5)
0.0 └───────────────────
    0.0               1.0  FPR (1 - Especificidad)
```

### 3.1 Construcción de la Curva ROC Paso a Paso

Para modelos probabilísticos (que devuelven $P(y=1|x)$), la curva se traza ordenando las probabilidades predichas de mayor a menor y evaluando cada probabilidad como un posible umbral de corte:

1. Se ordenan las instancias por su probabilidad decreciente.
2. Cada valor único de probabilidad se toma como un umbral $\tau$.
3. Si la probabilidad predicha $\ge \tau$, la predicción es $1$; en caso contrario, $0$.
4. Se calculan TPR y FPR para cada umbral y se unen los puntos en el plano $(0,0)$ a $(1,1)$.

### 3.2 Área Bajo la Curva (AUC)

- **AUC = 1.0:** Clasificador perfecto (distingue todas las muestras positivas de las negativas sin solapamiento).
- **AUC = 0.5:** Clasificador aleatorio (equivalente a lanzar una moneda).
- **Elección de Umbral de Operación:** En medicina, un falso negativo (paciente enfermo no diagnosticado) es crítico, por lo que suele fijarse un umbral que garantice alta sensibilidad ($\ge 90\%$), sacrificando especificidad si es necesario.

---

## 4. Selección de Modelos y Ajuste de Hiperparámetros

- **Grid Search:** Búsqueda exhaustiva sobre una malla predefinida de combinaciones de hiperparámetros.
- **GridSearchCV:** Integra Grid Search con validación cruzada ($K$-fold), evaluando cada combinación de hiperparámetros en múltiples particiones de entrenamiento y validación para evitar sobreajuste (*overfitting*).

---

## 5. Explicabilidad e Interpretabilidad con SHAP

Un modelo con alta exactitud no necesariamente es confiable si funciona como una "caja negra". La explicabilidad permite responder **por qué** el modelo tomó una decisión específica.

### 5.1 Valores Shapley (SHAP — SHapley Additive exPlanations)

Basados en la teoría de juegos cooperativos, calculan la contribución marginal de cada característica $i$ respecto a todos los subconjuntos posibles de variables $F$:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f(S \cup \{i\}) - f(S) \right]$$

Propiedad de **aditividad y eficiencia**:
$$f(x) = \phi_0 + \sum_{i=1}^{|F|} \phi_i$$
Donde $\phi_0 = \mathbb{E}[f(X)]$ es el valor base promedio esperado sobre el conjunto de referencia (*background*).

### 5.2 Tipos de Explicaciones Visuales

1. **Explicación Local (Waterfall Plot):**
   - Muestra cómo cada variable empuja la predicción de una muestra individual desde el valor base $\mathbb{E}[f(X)]$ hasta el resultado final $f(x)$.
   - Barras rojas suman al valor de salida; barras azules restan.
2. **Explicación Global (Beeswarm Plot):**
   - Cada punto es un paciente / muestra individual.
   - Eje X: Valor SHAP (impacto en la salida).
   - Color: Valor de la variable original (rojo = alto, azul = bajo).
   - Permite ver rápidamente si valores altos de una variable aumentan o disminuyen el riesgo.
3. **Importancia Global de Variables (Bar Plot):**
   - Grafica el promedio de los valores absolutos de SHAP: $\text{mean}(|\phi_i|)$.

### 5.3 Consideraciones y Limitaciones

- **SHAP explica el modelo, no la causalidad:** Una variable con alto valor SHAP indica que el algoritmo se apoya en ella para decidir, pero no prueba causalidad biológica o física directa.
- **Modelos no calibrados o con mal rendimiento:** Si el modelo generaliza mal, sus explicaciones carecen de valor. Primero se debe validar (K-Fold, ROC) y luego interpretar.
- **Multicolinealidad:** Si dos variables están altamente correlacionadas, su importancia suele dividirse entre ambas.

---

## 6. Técnicas de Validación Cruzada (Cross-Validation)

Evaluar un modelo sobre una partición fija de entrenamiento/prueba introduce alta incertidumbre estadística si el dataset es pequeño o moderado.

| Método | Funcionamiento | Cuándo usarlo |
|---|---|---|
| **Hold-out** | División única (ej. 75% train / 25% test o val). | Datasets muy grandes donde el costo computacional de reentrenar es prohibitivo. |
| **K-Fold** | Divide los datos en $K$ subconjuntos iguales. Itera $K$ veces, entrenando en $K-1$ y evaluando en el restante. | Método estándar para estimar el error medio de prueba y variabilidad entre folds. |
| **Leave-One-Out (LOOCV)** | Caso extremo donde $K = N$ (tamaño de la muestra). | Datasets muy pequeños; alto costo computacional en modelos lentos. |
| **K-Fold Estratificado** | Preserva la proporción relativa de cada clase en cada uno de los $K$ pliegues. | Problemas de clasificación con clases desbalanceadas. |

---

## Véase también
- [[_MOC|MOC Visualización]]
- [[Analisis_Lab_S9_Evaluacion_Interpretacion_Modelos|Lab S9 — Evaluación e Interpretación de Modelos]]
- [[Metricas de Evaluacion]]
- [[Machine Learning]]
- [[Regresion Lineal]]
- [[PCA]]
