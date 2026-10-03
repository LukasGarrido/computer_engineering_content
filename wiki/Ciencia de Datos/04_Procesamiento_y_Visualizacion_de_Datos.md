# Análisis de Datos: Guía Completa

---

## 1. Conceptos Fundamentales

Antes de analizar cualquier dataset, necesitas entender sus componentes básicos:

- **Variable**: Una característica medible, como edad, salario o temperatura. Es una *columna* en tu dataset.
- **Observación**: Un registro completo de datos, equivalente a una *fila* en tu dataset (ej. los datos de una persona).
- **Distribución**: Cómo se reparten los valores de una variable. ¿Están concentrados en el centro? ¿Dispersos? ¿Sesgados?
- **Correlación**: El grado en que dos variables cambian juntas. Si una sube cuando la otra sube, están correlacionadas positivamente.

---

## 2. Procesamiento de Datos (Data Cleaning)

Los datos reales casi nunca llegan limpios. Antes de analizar, hay que prepararlos.

### Problemas comunes

| Problema | Ejemplo |
|---|---|
| Valores faltantes | Una celda vacía en la columna "edad" |
| Duplicados | La misma fila registrada dos veces |
| Valores inconsistentes | "Chile", "chile", "CL" para el mismo país |
| Ruido / errores | Una edad de 450 años |
| Errores de formato | Una fecha como "31-13-2024" |

### Cómo solucionarlos

- **Valores faltantes**: Eliminar la fila, o reemplazar con la media/mediana/moda.
- **Duplicados**: Detectar y eliminar filas idénticas.
- **Inconsistencias**: Estandarizar texto (minúsculas, abreviaciones uniformes).
- **Errores de formato**: Convertir fechas, números y textos al tipo correcto.

---

## 3. Normalización y Estandarización

Dos técnicas para poner variables en una escala comparable.

### Normalización

Ajusta los valores a un rango definido, generalmente **[0, 1]**.

```
valor_normalizado = (x - min) / (max - min)
```

Útil cuando necesitas que todos los valores estén en el mismo intervalo.

### Estandarización (Z-score)

Transforma los datos para que tengan **media = 0** y **desviación estándar = 1**.

```
z = (x - μ) / σ
```

- Centra los datos en torno a cero.
- Permite comparar variables con distintas unidades.
- Muy usada en algoritmos de Machine Learning (SVM, KNN, regresión).

> **¿Cuándo usar cada una?** Si el algoritmo asume distribución normal → estandarización. Si necesitas valores acotados → normalización.

---

## 4. Transformación de Variables

Modificar variables para que sean más útiles en el análisis.

- **Codificación de categóricas**: Convertir texto a números. Ej. `["Rojo", "Azul", "Verde"]` → `[0, 1, 2]` o con *one-hot encoding*.
- **Conversión de tipos**: Transformar una cadena de texto `"2024-01-01"` a un tipo fecha real.
- **Discretización**: Agrupar valores continuos en rangos. Ej. edad → `[0-18, 19-35, 36-60, 60+]`.

---

## 5. Medidas de Tendencia Central y Dispersión

Describen el comportamiento general de los datos con un solo número.

### Tendencia central

- **Media (μ)**: El promedio aritmético. Sensible a outliers.
- **Mediana**: El valor central al ordenar los datos. Robusta ante outliers.
- **Moda**: El valor más frecuente.

### Dispersión

- **Varianza (σ²)**: Promedio de las distancias al cuadrado respecto a la media. Mide qué tan "esparcidos" están los datos.
- **Desviación estándar (σ)**: La raíz cuadrada de la varianza. Está en las mismas unidades que los datos.
  - Baja → datos concentrados cerca de la media.
  - Alta → datos muy dispersos.

---

## 6. Covarianza y Correlación

Miden la relación entre dos variables.

### Covarianza

Indica si dos variables cambian juntas y en qué dirección.

| Valor | Significado |
|---|---|
| Positiva | Ambas variables aumentan juntas |
| Negativa | Una sube cuando la otra baja |
| ≈ 0 | No hay relación lineal clara |

**Problema**: depende de las unidades de medida, por lo que no es comparable entre distintos pares de variables.

### Correlación

Es la covarianza *normalizada*. Siempre está entre **−1 y 1**.

| Valor | Significado |
|---|---|
| +1 | Relación lineal positiva perfecta |
| 0 | Sin relación lineal |
| −1 | Relación lineal negativa perfecta |

**Ventaja sobre la covarianza**: es adimensional y permite comparar directamente distintos pares de variables.

> Ejemplo: edad y años de experiencia suelen tener correlación positiva alta (~0.9).

### Matriz de Covarianza

Una tabla que muestra la covarianza entre todas las variables del dataset a la vez.

- Es **simétrica**: `Cov(X,Y) = Cov(Y,X)`
- La **diagonal** contiene las varianzas de cada variable.
- Muy usada en PCA (Análisis de Componentes Principales).

---

## 7. Detección de Outliers

Los outliers son valores atípicos que se alejan mucho del comportamiento general.

### ¿Por qué importan?

- Pueden ser errores de medición o registro.
- Distorsionan la media y la desviación estándar.
- Afectan negativamente a muchos modelos de ML.

### Métodos de detección

**Z-score (método de distancia)**
Mide cuántas desviaciones estándar se aleja un valor de la media.
```
z = (x - μ) / σ
```
Si `|z| > 3`, el valor se considera outlier.

**IQR (Rango Intercuartílico)**
Basado en el boxplot:
```
Límite inferior = Q1 - 1.5 × IQR
Límite superior = Q3 + 1.5 × IQR
```

**Métodos avanzados**
- **DBSCAN**: detecta puntos con pocos vecinos (baja densidad local).
- **Isolation Forest**: algoritmo de ML que aísla anomalías eficientemente.

---

## 8. Boxplot

Herramienta visual que resume la distribución de una variable en 5 números clave.

```
     |-----|=========|=========|-----|   o
     min   Q1      mediana    Q3   max  outlier

     └───── bigote ─┘└─── IQR ───┘└─bigote─┘
```

| Componente | Qué representa |
|---|---|
| Mediana (Q2) | Valor central del 50% de los datos |
| Q1 | 25% de los datos están por debajo |
| Q3 | 75% de los datos están por debajo |
| IQR | Q3 − Q1: el 50% central de los datos |
| Bigotes | Extensión de los datos no atípicos |
| Puntos externos | Outliers |

---

## 9. Distribuciones de Probabilidad

Describen cómo se reparten los valores de una variable aleatoria.

### Distribución Normal (Gaussiana)

La más importante en estadística.

- Forma de **campana simétrica**.
- La mayoría de los datos se concentran alrededor de la media.
- Se define completamente con solo dos parámetros: media (μ) y desviación estándar (σ).
- Regla empírica: ~68% de los datos están a ±1σ, ~95% a ±2σ, ~99.7% a ±3σ.

### Distribución Uniforme

Todos los valores tienen la **misma probabilidad** dentro de un intervalo.

- Completamente plana, sin picos.
- Ejemplo: lanzar un dado justo → cada cara tiene probabilidad 1/6.

### Distribución de Bernoulli

Modela un **único experimento** con dos resultados posibles: éxito (1) o fracaso (0).

- Parámetro: probabilidad de éxito `p`.
- Ejemplo: lanzar una moneda una vez.

### Distribución Binomial

Extiende a Bernoulli para **múltiples ensayos independientes**.

- Cuenta cuántos éxitos ocurren en `n` ensayos.
- Parámetros: número de ensayos `n` y probabilidad de éxito `p`.
- Ejemplo: ¿cuántas caras obtengo si lanzo una moneda 10 veces?

> **Relación**: Bernoulli es un caso especial de Binomial con `n = 1`.

---

## Resumen Visual

```
DATOS CRUDOS
    ↓
Procesamiento (limpieza, duplicados, formatos)
    ↓
Transformación (codificación, discretización)
    ↓
Normalización / Estandarización
    ↓
Análisis exploratorio (media, varianza, correlación, boxplot, outliers)
    ↓
DATOS LISTOS PARA MODELAR
```
