# Data Science y Machine Learning: Guía Completa

---

## 1. Histogramas en Imágenes

Un histograma de imagen muestra **con qué frecuencia aparece cada nivel de brillo** (intensidad) en una imagen.

- Cada imagen tiene píxeles con valores de gris entre 0 (negro) y 255 (blanco).
- `h(k) = nₖ` → cuántos píxeles tienen exactamente el nivel de gris `k`.
- `P(k) = nₖ / n` → versión normalizada; se interpreta como la **probabilidad** de que un píxel tenga ese nivel.

> Ejemplo: si un histograma está cargado a la izquierda, la imagen es oscura. Si está a la derecha, es clara. Si está disperso, tiene alto contraste.

Son muy eficientes y se usan en segmentación de imágenes en tiempo real.

---

## 2. ¿Qué es Data Science?

La Ciencia de Datos combina **estadística, matemáticas y programación** para extraer conocimiento útil de los datos.

```
Datos crudos → Análisis → Patrones → Decisiones / Soluciones
```

### Habilidades necesarias

| Habilidad | Para qué sirve |
|---|---|
| Matemática y estadística | Seleccionar técnicas, interpretar resultados |
| Manipulación de datos | Limpiar, organizar y preparar datasets |
| Programación | Implementar modelos y automatizar procesos |
| Conocimiento del dominio | Entender el contexto del problema |
| Comunicación | Explicar resultados a audiencias no técnicas |

---

## 3. Metodología de un Proyecto de Data Science

En la práctica, el proceso es **iterativo**: se repiten etapas según los resultados obtenidos.

### Paso 1 — Definir el alcance

- ¿Qué problema se quiere resolver?
- ¿Cuál es la variable objetivo (lo que queremos predecir)?
- ¿Cuál es la estrategia de trabajo?

### Paso 2 — Comprensión de los datos

- Explorar los datos disponibles.
- Hablar con expertos del dominio.
- Entender el contexto del problema.

### Paso 3 — Recolección de datos

- Obtener los datos desde las fuentes necesarias (APIs, bases de datos, archivos, web scraping, etc.).

### Paso 4 — Preparación de los datos

Es la etapa que más tiempo consume en la práctica (~70-80% del proyecto).

- Manejar valores faltantes (eliminar o imputar).
- Eliminar duplicados.
- Detectar y tratar outliers.
- Corregir formatos.
- Normalizar o estandarizar variables.
- **Ingeniería de características**: crear nuevas variables útiles a partir de las existentes.
- Análisis exploratorio (EDA) para entender patrones y anomalías.

### Paso 5 — Análisis y Modelado

El núcleo del proyecto: construir el modelo que aprende de los datos.

- Identificar patrones en los datos.
- Seleccionar el algoritmo adecuado según el problema:

| Algoritmo | Tipo | Uso típico |
|---|---|---|
| Regresión lineal | Supervisado | Predecir valores numéricos |
| Random Forest | Supervisado | Clasificación y regresión robusta |
| SVM | Supervisado | Clasificación con márgenes claros |
| Deep Learning | Supervisado | Imágenes, texto, audio |
| Clustering (K-Means) | No supervisado | Agrupar datos sin etiquetas |

### Paso 6 — Evaluación del modelo

- Medir el desempeño con métricas adecuadas:
  - **Regresión**: RMSE, MAE, R²
  - **Clasificación**: Precisión, Recall, F1-score
- Verificar que el modelo **generaliza** bien (no solo memoriza).
- Comparar distintos modelos entre sí.

### Paso 7 — Interpretación

- ¿Qué significan los resultados?
- ¿Qué variables tienen más peso?
- ¿Son los resultados coherentes con el dominio?

### Paso 8 — Publicación y Presentación

- Visualizar los hallazgos.
- Elaborar informes.
- Comunicar resultados de forma clara a distintas audiencias (técnica y no técnica).

---

## 4. CRISP-DM

Metodología estándar de la industria para proyectos de minería de datos.

```
Comprensión     →   Comprensión    →   Preparación
del negocio         de los datos       de los datos
                                            ↓
   Despliegue   ←   Evaluación     ←   Modelado
```

Es cíclico: los resultados de una etapa pueden llevar a regresar a una anterior.

---

## 5. Introducción a Machine Learning

### ¿Qué es?

Es un campo de la IA que desarrolla algoritmos capaces de **aprender de los datos** sin ser programados con reglas explícitas. En vez de decirle al programa qué hacer, le muestras ejemplos y él aprende la regla.

### Conceptos clave

| Término | Definición |
|---|---|
| Features (X) | Variables de entrada (las columnas del dataset) |
| Etiqueta / Target (Y) | Lo que queremos predecir |
| Función f | El modelo: relaciona X con Y |
| Hipótesis (H) | Conjunto de posibles funciones que el modelo podría aprender |
| Algoritmo de aprendizaje | El método que ajusta f para minimizar el error |

---

## 6. Tipos de Problemas en ML

### Según el tipo de salida

- **Regresión**: la salida es un número continuo. Ej: predecir el precio de una casa.
- **Clasificación**: la salida es una categoría. Ej: ¿es spam o no spam?
  - Si hay solo dos clases → **clasificación binaria**.

### Según el tipo de aprendizaje

#### Supervisado

- Entrenas el modelo con datos **etiquetados** (cada ejemplo ya tiene la respuesta correcta).
- El modelo aprende a mapear entradas → salidas.
- Ejemplos: regresión, clasificación.

#### No supervisado

- No hay etiquetas. El modelo busca **patrones ocultos** por sí solo.
- Ejemplos: clustering (agrupar clientes similares), reducción de dimensionalidad (PCA).

---

## 7. Generalización y Overfitting

### Generalización

La capacidad del modelo de predecir **correctamente datos nuevos** que nunca ha visto.

### Overfitting (sobreajuste)

Ocurre cuando el modelo **memoriza los datos de entrenamiento** en vez de aprender patrones generales. Funciona perfecto en entrenamiento pero falla en datos nuevos.

```
Entrenamiento: 99% precisión  ← parece bien
Test (datos nuevos): 55%      ← overfitting
```

**Cómo evitarlo**: más datos, regularización, validación cruzada, modelos más simples.

---

## 8. Modelos Paramétricos vs No Paramétricos

### Paramétricos

Asumen una forma funcional fija de antemano (ej: una línea recta en regresión lineal).

- Simples y rápidos de entrenar.
- Riesgo: si la forma asumida no se ajusta a los datos, el modelo falla.

### No paramétricos

No asumen ninguna forma específica. Se adaptan a los datos.

- Más flexibles y potentes.
- Necesitan **más datos** para funcionar bien.
- Ejemplos: árboles de decisión, KNN.

---

## 9. Precisión vs Interpretabilidad

Existe un trade-off fundamental en ML:

```
Más simple    →  Más interpretable  →  Menos preciso
Más complejo  →  Menos interpretable →  Más preciso
```

| Modelo | Interpretabilidad | Precisión |
|---|---|---|
| Regresión lineal | Alta | Baja-Media |
| Árbol de decisión | Alta | Media |
| Random Forest | Media | Alta |
| Red neuronal profunda | Muy baja | Muy alta |

En contextos regulados (salud, finanzas) la interpretabilidad suele ser obligatoria.

---

## 10. Inferencia vs Predicción

### Inferencia

- El objetivo es **entender** qué variables afectan al resultado y cómo.
- Se prefieren modelos interpretables.
- Ejemplo: ¿Qué factores influyen en que un cliente abandone el servicio?

### Predicción

- El objetivo es **predecir** valores futuros con la mayor precisión posible.
- Se permiten modelos complejos aunque sean cajas negras.
- Ejemplo: ¿Este cliente va a abandonar el servicio el próximo mes?

---

## 11. Maldición de la Dimensionalidad

Fenómeno que ocurre al trabajar con **muchas variables (dimensiones)**.

- A más dimensiones, el espacio de datos crece exponencialmente.
- Los datos se vuelven muy **dispersos**: cada punto queda lejos de todos los demás.
- Los modelos necesitan **muchos más datos** para cubrir ese espacio.
- Dificulta la generalización.

> Solución habitual: reducción de dimensionalidad (PCA, t-SNE) o selección de características (FSS, LASSO).

---

## 12. Sesgo y Varianza

Dos fuentes de error en cualquier modelo de ML.

### Sesgo (Bias)

Error por **simplificar demasiado** el modelo. El modelo no captura la complejidad real de los datos.

- Modelo demasiado simple → alto sesgo → **underfitting**.

### Varianza

Sensibilidad excesiva a los datos de entrenamiento. Pequeños cambios en los datos producen modelos muy distintos.

- Modelo demasiado complejo → alta varianza → **overfitting**.

### Trade-off sesgo-varianza

```
                    Error total
                   /            \
              Sesgo²          Varianza

Modelo simple:    alto sesgo   + baja varianza
Modelo complejo:  bajo sesgo   + alta varianza
Modelo ideal:     equilibrio entre ambos
```

El objetivo del entrenamiento es encontrar ese equilibrio para lograr la mejor **generalización** posible.

---

## Resumen del Flujo Completo

```
PROBLEMA DE NEGOCIO
        ↓
Recolección de datos
        ↓
Preparación y limpieza (EDA, outliers, normalización)
        ↓
Elección del tipo de problema (regresión / clasificación / clustering)
        ↓
Selección del modelo (paramétrico / no paramétrico, simple / complejo)
        ↓
Entrenamiento y evaluación (generalización, sesgo-varianza)
        ↓
Interpretación y presentación de resultados
```
