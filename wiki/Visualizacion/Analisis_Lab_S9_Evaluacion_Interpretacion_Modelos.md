---
tags:
  - visualizacion
  - laboratorio
  - metricas-de-evaluacion
  - machine-learning
  - pca
aliases:
  - "Lab S9 Visualización"
  - "Laboratorio Sesión 9 Visualización"
  - "Evaluación e Interpretación Heart Disease"
asignatura: "Visualización"
tipo: laboratorio
created: 2026-10-10
---

# Laboratorio 9 — Visualización para Clasificación, Predicción y Explicabilidad (SHAP)

> Guía práctica y análisis del laboratorio de evaluación e interpretación de modelos sobre el dataset Heart Disease: diagnóstico de regresión, curvas ROC, matrices de confusión, proyección PCA con fronteras de decisión y explicabilidad con valores SHAP. Asignatura EIN092B (G5 - Sesión 9).

---

## 1. Contexto y Objetivos del Laboratorio

El laboratorio aborda un problema biomédico de alta relevancia: la predicción y clasificación de afecciones cardiovasculares utilizando el dataset clásico **Heart Disease** (UCI / Kaggle).

### Objetivos
1. **Inspección exploratoria visual** de variables numéricas y categóricas.
2. **Evaluación de modelos de regresión** mediante métricas cuantitativas (MAE, MSE) y gráficos de diagnóstico (real vs. predicho, distribución de residuos).
3. **Evaluación de modelos de clasificación binaria** mediante curvas ROC/AUC, matrices de confusión y ajuste dinámico de umbrales clínicos.
4. **Proyección en baja dimensionalidad (PCA)** para visualizar agrupamientos, separabilidad y fronteras de decisión.
5. **Interpretación y explicabilidad con SHAP**, comparando un modelo lineal (Regresión Logística) frente a un modelo no lineal basado en instancias (KNN).

---

## 2. Preparación de Datos y Pipeline

El conjunto de datos consta de 270 a 303 pacientes con 13 atributos fisiológicos y de laboratorio:

```python
headers = [
    'age', 'sex', 'chest_pain', 'blood_p', 'serum', 'blood_s', 'electro',
    'max_heart', 'angina', 'oldpeak', 'slope', 'vessel', 'thal', 'disease'
]
```

### 2.1 Preprocesamiento Clave
1. **Mapeo Categórico:** Conversión de códigos numéricos a etiquetas legibles (ej. tipo de dolor de pecho: angina típica, atípica, no anginoso, asintomático).
2. **One-Hot Encoding:** Expansión binaria de variables nominales con `pd.get_dummies(..., dtype=float)`.
3. **Partición de Datos:** División 70% entrenamiento y 30% prueba con **estratificación** según la presencia de patología (`stratify=y_cls`) y semilla fija (`random_state=42`).
4. **Prevención de Data Leakage:** Ajuste de `StandardScaler()` exclusivamente sobre el conjunto de entrenamiento (`fit`), aplicando luego la transformación (`transform`) a prueba y validación.

---

## 3. Tarea 1: Predicción de Presión Sanguínea (Regresión)

Se plantea predecir la presión sanguínea en reposo (`blood_p`) a partir del resto de variables fisiológicas.

### 3.1 Modelos Evaluados
- **Linear Regression & Ridge Regression ($\alpha = 10.0$):** Modelos lineales con regularización $L_2$ para mitigar colinealidad.
- **Random Forest Regressor ($n=200, \text{depth}=5$):** Ensamble no lineal de árboles de decisión.
- **K-Nearest Neighbors Regressor ($k=10$):** Predicción basada en el promedio de los vecinos más cercanos.

### 3.2 Gráficos de Diagnóstico Visual
- **Dispersión Real vs. Predicho:** Permite observar la correlación a lo largo de la diagonal $y = x$. Puntos que se alejan hacia abajo representan subestimaciones en presiones altas; puntos por encima indican sobreestimaciones en presiones bajas.
- **Residuos vs. Valor Predicho:** Se verifica la hipótesis de homocedasticidad. La ausencia de curvaturas o embudos evidencia que no existen relaciones no lineales severas omitidas.
- **Histograma de Residuos:** Inspecciona que los errores se centren en cero con distribución aproximadamente normal.
- **Validación Cruzada ($K=5$):** Boxplot de MAE y MSE por fold que refleja la estabilidad del modelo frente a variaciones en la muestra.

---

## 4. Tarea 2: Clasificación de Enfermedad Cardíaca

Se evalúa la predicción binaria de presencia (`disease=1`) o ausencia (`disease=0`) de cardiopatía.

### 4.1 Comparativa de Modelos: KNN vs. Regresión Logística

| Métrica | K-Nearest Neighbors ($k=7$) | Regresión Logística |
|---|:---:|:---:|
| **Accuracy** | ~0.80 – 0.84 | ~0.84 – 0.88 |
| **Precision** | Aceptable | Alta |
| **Recall (Sensibilidad)** | Moderado | Elevado |
| **AUC-ROC** | Menor suavidad | Curva continua y regular |

- **Diferencia en Curvas ROC:** La curva ROC de KNN presenta saltos discretos tipo escalón debido a que las probabilidades predichas provienen de la fracción discreta de vecinos ($\frac{m}{k}$ con $k=7$), mientras que la regresión logística entrega probabilidades continuas derivadas de la función sigmoide.

### 4.2 Ajuste del Umbral Clínico de Decisión

Por defecto, los clasificadores usan un umbral de $0.5$. Sin embargo, en diagnóstico médico:
- **Costo de un Falso Negativo (FN):** Un paciente enfermo es dado de alta sin tratamiento oportuno (riesgo vital grave).
- **Costo de un Falso Positivo (FP):** Se indica un examen complementario adicional a un paciente sano.

> [!IMPORTANT]
> Al reducir el umbral de decisión (por ejemplo de $0.50$ a $0.30$–$0.35$), se incrementa la **Sensibilidad por sobre el 90%**, capturando prácticamente todos los pacientes enfermos a costa de un incremento controlado en falsas alarmas (reducción moderada de especificidad).

### 4.3 Reducción Dimensional (PCA) y Fronteras de Decisión

1. **Proyección 2D:** Se ajusta un PCA de 2 componentes principales sobre el espacio estandarizado. Al graficar las clases reales vs. las predicciones de KNN y LR, se observa que los errores se concentran en la zona de solapamiento central (región de alta ambigüedad fisiológica).
2. **Fronteras de Decisión (`DecisionBoundaryDisplay`):**
   - **Regresión Logística:** Genera una frontera de decisión hiperplana (lineal) recta en el espacio 2D.
   - **KNN:** Genera islas y contornos irregulares no lineales, adaptándose localmente a la densidad de los datos vecinos.
3. **Efecto del Número de Componentes ($k$):**
   - La curva de varianza explicada acumulada muestra que se requieren entre 8 y 10 componentes para explicar más del 80% de la varianza.
   - Evaluar el AUC en función de $k$ demuestra que reducir a 2 componentes sacrifica poder predictivo respecto al dataset completo, aunque permite la inspección visual.

---

## 5. Tarea 3: Explicabilidad con SHAP

### 5.1 Configuración de Explicadores
- **Regresión Logística:** Se emplea `shap.LinearExplainer(lr, X_train_std)` calculando exactamente los valores SHAP en el espacio de *log-odds*.
- **KNN:** Se utiliza `shap.Explainer(knn.predict_proba, background)` empleando un subconjunto de referencia de 100 muestras del conjunto de entrenamiento.

### 5.2 Interpretación Global (Beeswarm & Bar Plot)
- **Variables Críticas Identificadas:**
  - `oldpeak` (depresión del segmento ST inducida por ejercicio): valores elevados empujan fuertemente hacia la presencia de patología.
  - `max_heart` (frecuencia cardíaca máxima alcanzada): valores bajos se correlacionan con mayor riesgo de enfermedad.
  - `chest_pain` y defectos en `thal`: fuerte peso diagnóstico consistente con la literatura médica.
- **Ranking vs. Magnitudes:** Como la regresión logística explica en *log-odds* y KNN en *probabilidad*, las magnitudes numéricas directas no son directamente comparables entre modelos, pero los **rankings de importancia relativa** sí coinciden en las variables dominantes.

### 5.3 Explicación Local (Waterfall Plot)
- **Paciente Bien Clasificado:** Muestra la suma acumulativa de contribuciones $\phi_i$ que elevan la predicción desde el valor base $\mathbb{E}[f(X)]$ hasta superar el umbral con certeza.
- **Paciente Mal Clasificado (Falso Positivo o Falso Negativo):** Permite aislar exactamente qué variables atípicas confundieron al modelo (por ejemplo, un paciente de edad avanzada con dolor atípico pero sin alteración en el segmento ST).

### 5.4 Dependencia de Variables (`shap.plots.scatter`)
- En **Regresión Logística**, el scatter de SHAP para cualquier variable muestra una relación estrictamente lineal o monotónica con pendiente fija.
- En **KNN**, el scatter exhibe fluctuaciones, discontinuidades y respuestas no lineales locales, capturando interacciones sutiles del vecindario.

---

## Véase también
- [[_MOC|MOC Visualización]]
- [[04_Evaluacion_Modelos_Clasificacion_Regresion|C9 — Teoría de Evaluación de Modelos y Curvas ROC]]
- [[Metricas de Evaluacion]]
- [[PCA]]
- [[Machine Learning]]
