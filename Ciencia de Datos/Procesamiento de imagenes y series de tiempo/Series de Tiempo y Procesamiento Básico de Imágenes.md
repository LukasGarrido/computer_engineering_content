
> Apuntes ampliados — EIN087B, Ciencia de Datos

---

## Parte 1: Análisis de Series de Tiempo

### 1.1 ¿Qué es una serie de tiempo y por qué es diferente?

En la mayoría de los problemas de Ciencia de Datos que vemos a lo largo de un curso (regresión, clasificación con árboles, SVM, etc.), las observaciones son **independientes entre sí** y no tienen un orden intrínseco: si mezclamos las filas de un dataset de precios de casas, el problema sigue siendo exactamente el mismo.

Una **serie de tiempo** rompe esa suposición:

$${y_t}_{t=1}^{T} = y_1, y_2, y_3, \dots, y_T$$

- Cada observación $y_t$ está asociada a un instante específico $t$.
- El **orden importa**: si mezclamos los datos, perdemos información esencial.
- El valor de $y$ en el futuro depende no solo de variables externas $x$, sino también de **su propia historia**.

**Ejemplos típicos por dominio:**

|Dominio|Ejemplo de serie de tiempo|
|---|---|
|Climatología|Temperatura diaria, precipitaciones mensuales|
|Finanzas|Precio de una acción, tasa de interés|
|Marketing|Ventas mensuales, demanda de un producto|
|Ingeniería|Lecturas de sensores industriales (vibración, temperatura)|
|Salud|Ritmo cardíaco, curva de contagios de una epidemia|

### 1.2 El dataset de referencia: AirPassengers

A lo largo de toda la unidad se usa un dataset clásico: el **número mensual de pasajeros aéreos** (en miles) entre enero de 1949 y diciembre de 1960 (144 observaciones), disponible en `statsmodels`.

**Por qué es un buen ejemplo:**

- Tiene una **tendencia creciente** clara (cada vez vuela más gente).
- Tiene una **estacionalidad anual** muy marcada (picos en ciertos meses, probablemente vacaciones de verano del hemisferio norte).
- La amplitud de los picos **crece con el tiempo** — esto será clave para decidir entre modelo aditivo y multiplicativo más adelante.

**El problema de negocio:** una aerolínea quiere predecir cuántos pasajeros tendrá el próximo mes para planificar su operación (personal, vuelos, combustible). Es un problema de regresión donde $y$ = pasajeros del mes, pero **no hay variables independientes $x$ obvias** — toda la información disponible está en la propia serie.

---

### 1.3 El enfoque ingenuo y la motivación de la Media Móvil

#### Enfoque ingenuo (Naive Forecast)

La predicción más simple posible: el próximo valor será igual al último observado.

$$\hat{y}_{t+1} = y_t$$

- ✅ Computacionalmente gratis.
- ❌ Muy inexacto si hay cambios bruscos o estacionalidad (ej. predecir diciembre usando noviembre falla si diciembre siempre tiene un pico de ventas).

**Mejora natural:** en lugar de usar un solo valor pasado, promediar varios. Así nace la **Media Móvil**.

#### Media Móvil (Moving Average, MA)

$$\hat{y}_t = \frac{1}{n}\sum_{i=1}^{n} y_{t-i}$$

- Calcula el promedio de los últimos $n$ valores.
- La ventana de tamaño $n$ se desliza a lo largo de la serie.
- **Útil para:** suavizar ruido, visualizar la tendencia local.
- **Limitación:** no modela estacionalidad ni tendencia a largo plazo de forma explícita; es solo un suavizado.

**¿Por qué ventana = 12 en AirPassengers?**

No es arbitrario: como los datos son mensuales y el patrón se repite **cada 12 meses**, una ventana de 12 promedia exactamente un ciclo completo, eliminando el efecto estacional y dejando ver la tendencia "pura".

> **Detalle técnico:** con 144 observaciones y ventana 12, solo se pueden calcular 132 medias móviles reales (se "pierden" los primeros 11-12 puntos porque no hay suficiente historia para promediar).

#### Extender la Media Móvil para predecir el futuro

La fórmula original solo nos da el promedio de datos _ya observados_. Pero podemos usarla para predecir el mes 145:

$$\hat{y}_{145} = \frac{1}{12}\sum_{i=1}^{12} y_{144-i+1}$$

El truco para seguir prediciendo (mes 146, 147, ...) es **reemplazar valores reales faltantes por valores ya predichos**:

$$\hat{y}_t = \frac{1}{12}\sum_{i=1}^{12} \tilde{y}_{t-i}$$

donde $\tilde{y}_{t-i}$ puede ser un dato real (si existe) o una predicción anterior.

**⚠️ Punto importante:** a medida que el horizonte de predicción crece, usamos cada vez **más predicciones y menos datos reales**. El valor número 13 del horizonte futuro ya es un promedio de 12 valores que _a su vez_ eran promedios. Esto produce un efecto de "regresión a la media": las predicciones tienden a aplanarse y perder la variabilidad/tendencia real de la serie.

#### Variantes mencionadas (mejoras sobre MA simple)

- **Media Móvil Ponderada (WMA):** asigna pesos distintos a cada punto de la ventana (por ejemplo, dar más peso a los datos más recientes).
- **Suavizado Exponencial:** los pesos decrecen exponencialmente hacia el pasado, dando mayor relevancia a lo reciente sin descartar por completo la historia antigua.

A pesar de estas mejoras, **siguen siendo predictores de corto plazo**. Lo verdaderamente valioso del concepto de media móvil es que **captura la tendencia central** de la serie — y esa idea es la base de la siguiente sección: la descomposición.

---

### 1.4 Descomposición de Series de Tiempo

#### Idea central

Una serie de tiempo puede entenderse como la combinación de varios componentes "ocultos" que, sumados o multiplicados, generan los datos que observamos.

|Componente|Símbolo|Descripción|Ejemplo|
|---|---|---|---|
|**Tendencia**|$T_t$|Evolución a largo plazo (crecimiento, caída, estable)|Aumento sostenido de pasajeros año tras año|
|**Estacionalidad**|$S_t$|Patrón que se repite en intervalos regulares y _predecibles_|Pico de pasajeros cada julio/agosto|
|**Componente cíclica**|$C_t$|Oscilaciones de largo plazo, _sin periodicidad fija_|Recesiones económicas|
|**Residuo**|$R_t$|Lo que sobra: ruido, eventos no explicados|Una huelga inesperada que reduce vuelos un mes|

**Visualización de patrones típicos:**

- Error puramente aleatorio sin patrón reconocible.
- Tendencia curvilínea (cuadrática o exponencial).
- Tendencia lineal creciente.
- Patrón estacional puro (sube y baja repetitivo).
- Patrón estacional + crecimiento lineal (lo más parecido a AirPassengers).

#### 🔑 Estacionalidad vs. Ciclos: una distinción clave

Es muy común confundir estos dos conceptos, pero la diferencia tiene implicaciones prácticas importantes para el modelado:

||**Estacionalidad**|**Ciclos**|
|---|---|---|
|Periodicidad|Fija y conocida (ej. cada 12 meses, cada 7 días)|Irregular, sin período fijo|
|¿Predecible solo con $t$?|Sí — sabemos cuándo ocurrirá|No — depende de factores externos|
|Ejemplos|Ventas de fin de año, temperatura por estación|Ciclos económicos, crisis, eventos políticos|
|Cómo se modela|Explícitamente, como un componente $S_t$|Generalmente termina mezclado en el residuo $R_t$|

> **¿Por qué importa?** Si tratamos un ciclo económico como si fuera estacionalidad (asumiendo que se repetirá exactamente igual cada cierto número de meses), nuestras predicciones de largo plazo pueden ser muy erróneas. Distinguir ambos evita errores de interpretación.

---

### 1.5 Modelo Aditivo de Descomposición

**Supuesto:** los componentes se **suman** para formar la serie observada.

$$y_t = T_t + S_t + R_t$$

**¿Cuándo usar este modelo?** Cuando la **amplitud de la estacionalidad es aproximadamente constante** a lo largo del tiempo, sin importar el nivel de la tendencia. Por ejemplo: si las ventas suben siempre "+50 unidades" en diciembre, sin importar si el negocio está en su año 1 o en su año 10.

#### Cálculo manual paso a paso

**1. Estacionalidad ($S_t$):** se promedia cada mes (enero, febrero, ..., diciembre) a través de todos los años disponibles.

$$S_t = \frac{1}{N}\sum_{j=1}^{N} y_{t+12(j-1)}, \quad t=1,\dots,12$$

donde $N$ es el número de años. Esto produce **12 valores** (uno por mes) que se repiten cíclicamente a lo largo de toda la serie.

**Ejemplo concreto:** si tenemos 12 años de datos, $S_{\text{enero}}$ es el promedio de los 12 valores de enero (uno de cada año). Lo mismo para febrero, marzo, etc.

**2. Tendencia ($T_t$):** primero se "quita" la estacionalidad restándola de la serie original ($y_t - S_t$), y luego se aplica una media móvil sobre esa serie desestacionalizada:

$$T_t = \frac{1}{k}\sum_{i=0}^{k-1} (y_{t+i} - S_{t+i})$$

con $k$ el tamaño de la ventana (típicamente $k=12$).

**3. Residuo ($R_t$):** lo que queda después de remover tendencia y estacionalidad:

$$R_t = y_t - T_t - S_t$$

#### Predicción con el modelo aditivo

Para proyectar 24 meses hacia adelante:

1. Se ajusta una **regresión lineal** sobre la componente de tendencia ya calculada (usando `np.polyfit`), obteniendo una pendiente (`slope`) y un intercepto (`intercept`).
2. Para cada mes futuro $i$, se calcula la tendencia proyectada: `trend_projection = slope * i + intercept`.
3. Se le suma la estacionalidad correspondiente a ese mes (usando `i % 12` para "ciclar" entre los 12 valores estacionales).

```python
# Regresión lineal para calcular la tendencia futura
x = np.arange(len(trend) - (window_size - 1))
slope, intercept = np.polyfit(x, trend[window_size-1:], 1)

predictions = []  # Predicciones para los próximos 24 meses
for i in range(len(data), len(data) + 24):
    trend_projection = slope * i + intercept
    predictions.append(trend_projection + monthly_avg[i % 12])
```

**Resultado visual:** la predicción sigue una línea de tendencia creciente con oscilaciones estacionales superpuestas de **amplitud constante** — pero en AirPassengers los picos reales crecen con el tiempo, así que el modelo aditivo subestima los picos más recientes.

---

### 1.6 Modelo Multiplicativo de Descomposición

**Supuesto:** los componentes se **multiplican**.

$$y_t = T_t \times S_t \times R_t$$

**¿Cuándo usar este modelo?** Cuando la amplitud de la estacionalidad **crece proporcionalmente con la tendencia** — es decir, cuanto más grande es el "nivel base" de la serie, más grandes son también los picos y valles estacionales. Este es exactamente el caso de AirPassengers: en 1949 los picos eran de unas decenas de pasajeros extra, pero en 1960 son de cientos.

#### Cálculo manual paso a paso

**1. Estacionalidad ($S_t$):** igual que en el modelo aditivo, se promedia cada mes a través de los años, generando 12 valores que se repiten.

**2. Tendencia ($T_t$):**

- Se **divide** la serie por la estacionalidad para "desestacionalizar": $y_t / S_t$.
- Se aplica una media móvil sobre esa serie desestacionalizada.

**3. Residuo ($R_t$):**

$$R_t = \frac{y_t}{T_t \times S_t}$$

#### Predicción con el modelo multiplicativo

La diferencia clave respecto al aditivo: en lugar de **sumar** la estacionalidad a la tendencia proyectada, se **multiplica**.

```python
x = np.arange(len(trend) - (window_size - 1))
slope, intercept = np.polyfit(x, trend[window_size-1:], 1)

predictions = []
for i in range(len(data), len(data) + 24):
    trend_projection = slope * i + intercept
    seasonality_projection = monthly_avg[i % 12]
    # En el modelo multiplicativo, la predicción es tendencia * estacionalidad
    prediction = trend_projection * seasonality_projection
    predictions.append(prediction)
```

#### Comparación Aditivo vs. Multiplicativo

|Aspecto|Modelo Aditivo|Modelo Multiplicativo|
|---|---|---|
|Fórmula|$y_t = T_t + S_t + R_t$|$y_t = T_t \times S_t \times R_t$|
|Amplitud estacional|Constante|Proporcional a la tendencia|
|Predicción futura|tendencia + estacionalidad|tendencia × estacionalidad|
|Mejor para AirPassengers|❌ (subestima picos recientes)|✅ (los picos crecen junto con la tendencia, más realista)|

> **Conclusión del material:** el modelo multiplicativo logra capturar el incremento en la magnitud de la estacionalidad, generando predicciones que "coinciden con la intuición" — es decir, los picos futuros se ven proporcionalmente más grandes que los picos actuales, tal como ha venido ocurriendo en los datos históricos.

---

### 1.7 Modelos Autorregresivos (AR)

#### Concepto

Un modelo **AR(p)** asume que el valor actual depende **linealmente** de sus $p$ valores pasados (rezagos o _lags_):

$$\hat{y}_t = \phi_0 + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \dots + \phi_p y_{t-p}$$

donde:

- $\hat{y}_t$: valor predicho en el instante $t$.
- $y_{t-1}, \dots, y_{t-p}$: valores pasados (rezagos).
- $\phi_0, \dots, \phi_p$: parámetros del modelo (se **aprenden** del histórico).

#### Diferencia entre AR y Media Móvil Ponderada

A primera vista parecen lo mismo (ambos combinan valores pasados con pesos), pero hay diferencias importantes:

||Media Móvil Ponderada (WMA)|Modelo AR|
|---|---|---|
|¿Cómo se eligen los pesos?|Se definen manualmente (heurística)|Se **aprenden** minimizando el Error Cuadrático Medio (MSE)|
|¿Los pesos suman 1?|Generalmente sí|No es necesario|
|¿Tiene intercepto?|No|Sí ($\phi_0$)|

#### Implementación práctica con `LinearRegression`

La idea es transformar el problema de series de tiempo en un problema de **regresión supervisada estándar**, usando el truco de la **ventana deslizante**:

```python
# Función para transformar los datos para el modelo AR:
# construye vectores X usando valores y rezagados.
def transform_data(data, lags):
    X, y = [], []
    for i in range(lags, len(data)):
        X.append(data[i-lags:i])
        y.append(data[i])
    return np.array(X), np.array(y)

# lags = 12, siguiendo la lógica de la estacionalidad anual
lags = 12
X, y = transform_data(data, lags)

model = LinearRegression()
model.fit(X, y)

# Predicción iterativa, un paso adelante en cada iteración
predictions = []
input_data = list(data[-lags:])
for i in range(24):  # predecir 24 meses hacia adelante
    prediction = model.predict([input_data[-lags:]])
    predictions.append(prediction[0])
    input_data.append(prediction[0])  # se usa la predicción como nuevo "dato"
```

**Punto clave:** al igual que en la media móvil extendida, este proceso es **iterativo y recursivo** — cada nueva predicción depende de las predicciones anteriores. Esto significa que los errores se pueden **acumular y amplificar** a medida que el horizonte crece.

#### ⚠️ Limitación fundamental: Estacionariedad

El modelo AR **asume que la serie es estacionaria**. Una serie es estacionaria si:

- Su **media** y **varianza** son aproximadamente constantes en el tiempo.
- **No** muestra tendencia ni estacionalidad persistente.

AirPassengers **no** es estacionaria (tiene tendencia creciente clara). ¿Qué pasa entonces?

- **A corto plazo (≈2 años):** el modelo AR funciona razonablemente bien, porque dentro de esa ventana los cambios de tendencia son pequeños.
- **A largo plazo:** si extendemos la proyección mucho más allá, **la tendencia real de los datos no queda bien representada**. El modelo tiende a generar oscilaciones que crecen artificialmente o se desestabilizan, porque está intentando "extrapolar" un comportamiento que asumió constante.

#### Solución: Diferenciación

La **diferenciación** transforma una serie no estacionaria en (aproximadamente) estacionaria, analizando **variaciones entre periodos consecutivos** en lugar de valores absolutos:

$$\Delta Y_t = Y_t - Y_{t-1}$$

- Permite mitigar el efecto de tendencias y estacionalidades.
- Se puede aplicar **más de una vez**: el "grado de diferenciación" indica cuántas veces se aplicó esta transformación.
- Una vez la serie diferenciada es (más) estacionaria, se entrena un AR sobre ella.
- Para volver a la escala original, se **acumulan** las diferencias predichas sumándolas progresivamente al último valor real conocido.

```python
differenced_data = [data[i] - data[i-1] for i in range(1, len(data))]

X, y = transform_data(differenced_data, 12)  # lags = 12
model = LinearRegression()
model.fit(X, y)  # Modelo AR sobre datos diferenciados

predictions_diff = []
input_data = list(differenced_data[-lags:])
last_original_value = data[-1]
predictions = []

for i in range(96):  # horizonte de predicción
    prediction_diff = model.predict([input_data[-lags:]])
    predictions_diff.append(prediction_diff[0])

    # Recuperar la escala original sumando la diferencia predicha
    new_value = last_original_value + prediction_diff
    predictions.append(new_value[0])
    last_original_value = new_value
    input_data.append(prediction_diff[0])
```

**Resultado observado:** incluso con diferenciación, al proyectar muy lejos en el futuro (96 meses, 8 años), las oscilaciones tienden a crecer de forma poco realista. La diferenciación ayuda con la estacionariedad, pero **no es una solución mágica** para el largo plazo con un modelo lineal simple.

---

### 1.8 Evaluación rigurosa de modelos de series de tiempo

#### El problema con la "evaluación visual"

Mirar un gráfico y decir "la predicción sigue la tendencia" **no es una medida rigurosa**. Necesitamos una métrica cuantitativa.

#### La regla de oro: respetar el orden cronológico

A diferencia de datos no temporales (donde podemos hacer _train/test split_ aleatorio), en series de tiempo:

> ❌ **NUNCA** mezclar aleatoriamente los datos de entrenamiento y prueba. ✅ El conjunto de prueba debe ser **el segmento final** de la serie (el "futuro" relativo al entrenamiento).

**En AirPassengers:** se entrena con los primeros 132 meses (11 años) y se predicen/evalúan los **últimos 12 meses** (el último año).

#### Métrica: RMSE (Raíz del Error Cuadrático Medio)

$$RMSE = \sqrt{\frac{1}{n}\sum_{t=1}^{n}(\hat{Y}_t - Y_t)^2}$$

- Está en las **mismas unidades** que la variable original (miles de pasajeros), lo que la hace fácil de interpretar.
- **Penaliza más los errores grandes** que los pequeños (por el cuadrado), lo cual es útil porque generalmente nos preocupan más los errores grandes en producción.
- Permite **comparar modelos de forma objetiva**.

#### Resultados comparativos obtenidos

|Modelo|RMSE (conjunto de prueba)|
|---|---|
|AR sin diferenciar|**20.76**|
|AR con diferenciación|21.50|
|Random Forest (walk-forward, MAE)|23.11|

**Interpretación:**

- A corto plazo (1 año), el AR **sin diferenciar** ajusta ligeramente mejor que el diferenciado.
- Esto sugiere que para este horizonte específico, la pérdida de información al diferenciar (y la posterior reconstrucción acumulativa) no compensa la ganancia en estacionariedad.
- **Pero ojo:** esto no significa que la diferenciación sea inútil en general — simplemente no hay datos suficientes para validar si ayudaría a horizontes más largos (más de un año).

---

### 1.9 Modelos estadísticos avanzados (panorama, sin profundizar)

El curso menciona estos modelos para dar contexto, pero **no los desarrolla en profundidad** porque el foco está en avanzar hacia Machine Learning:

|Modelo|Descripción breve|
|---|---|
|**ARIMA**|Combina **A**utoRegresión + **I**ntegración (diferenciación) + **M**edia móvil (en los residuos)|
|**SARIMA**|ARIMA + componente estacional explícita (la "S" de _Seasonal_)|
|**SARIMAX**|SARIMA + variables **eXógenas** (datos externos a la serie)|
|**Prophet**|Modelo aditivo de Meta/Facebook, soporta múltiples estacionalidades y eventos especiales (feriados, lanzamientos, etc.)|

> **Variable exógena:** una variable que no forma parte del proceso generador de la serie, pero que puede influir en su comportamiento. Ejemplos: precio del combustible (afecta demanda de vuelos), vacaciones escolares, PIB mensual, eventos deportivos, festividades.

Estos modelos están "en la frontera" entre estadística clásica y ML, ya que requieren entrenar parámetros, pero su estructura matemática sigue siendo predominantemente estadística.

---

### 1.10 Machine Learning para Series de Tiempo

#### El truco fundamental: la ventana deslizante (Sliding Window)

Para usar algoritmos de ML clásico (KNN, SVM, Random Forest, etc.) — que están diseñados para datos tabulares "sin orden" — necesitamos **reformular** el problema de serie temporal como un problema de aprendizaje supervisado tradicional:

- **Entrada (features):** valores anteriores de la serie $(y_{t-1}, y_{t-2}, \dots, y_{t-n})$
- **Salida (target):** el valor siguiente $y_t$

**Ejemplo concreto:** con ventana de 12 meses, cada "ejemplo de entrenamiento" es:

> _"Dados los meses 1 al 12, predice el mes 13"_ _"Dados los meses 2 al 13, predice el mes 14"_ ... y así sucesivamente.

> **Importante:** estos modelos **no modelan la dinámica temporal de forma explícita** (no "saben" qué es el tiempo), pero pueden capturar patrones locales si se entrenan correctamente, ya que ven los valores pasados como simples features numéricas.

#### Random Forest con Validación Walk-Forward

Esta es una de las técnicas más importantes del material para evaluar modelos de ML en series de tiempo de forma realista.

**Paso 1 — Transformación supervisada:** ventana deslizante de 12 meses → predecir el mes siguiente.

**Paso 2 — Walk-Forward Validation**, que simula cómo funcionaría el modelo en producción real:

1. Entrenar el modelo con **todos los datos disponibles hasta el momento actual**.
2. Predecir el siguiente mes.
3. Una vez que el dato real de ese mes esté disponible, **añadirlo al historial**.
4. Re-entrenar (o actualizar) el modelo con el historial ampliado.
5. Repetir el proceso para el siguiente mes.

**¿Por qué es mejor que un split fijo train/test?**

|Ventaja|Explicación|
|---|---|
|Evita _data leakage_|El modelo nunca "ve" información del futuro al hacer cada predicción|
|Evaluación paso a paso|Obtenemos una métrica de error por cada predicción individual, no solo un número global|
|Mayor validez externa|Refleja fielmente cómo se comportaría el sistema si se desplegara en producción real, donde cada mes llegan nuevos datos|

**Resultado:** Random Forest con walk-forward obtuvo un **MAE = 23.11**, comparable (aunque ligeramente peor) que los modelos AR del orden de 20-21.

---

### 1.11 Redes Neuronales para Series de Tiempo (panorama)

Los modelos clásicos (Random Forest, KNN, Regresión Lineal) tienen una limitación estructural: requieren transformar la serie en **ventanas estáticas** y, aunque pueden capturar patrones locales, **no retienen memoria** de la secuencia ni modelan explícitamente "el tiempo" como concepto.

**Alternativas basadas en redes neuronales:**

|Arquitectura|Idea clave|
|---|---|
|**LSTM** (Long Short-Term Memory)|Red recurrente diseñada específicamente para aprender **dependencias de largo plazo** mediante "puertas" de memoria|
|**GRU** (Gated Recurrent Unit)|Variante simplificada y más eficiente de LSTM|
|**CNNs temporales**|Detectan patrones locales (similares a "filtros") de forma eficiente sobre la dimensión temporal|
|**Transformers para series de tiempo**|Modelan relaciones **globales** entre todos los puntos de la secuencia, sin necesidad de procesar paso a paso (sin recurrencia)|

**Ventajas generales sobre modelos clásicos/lineales:**

- Mayor capacidad para generalizar **patrones complejos no lineales**.
- El tiempo se modela **directamente** como parte del aprendizaje (no es solo una "feature más").
- Mayor adaptabilidad a múltiples frecuencias, estacionalidades simultáneas y ruido.

---

### 1.12 Resumen del flujo conceptual — Series de Tiempo

```
Enfoque ingenuo (y_t+1 = y_t)
        ↓
Media Móvil (suaviza, captura tendencia central)
        ↓
Descomposición (Tendencia + Estacionalidad + Residuo)
   ├── Modelo Aditivo (estacionalidad constante)
   └── Modelo Multiplicativo (estacionalidad ∝ tendencia)
        ↓
Modelos Autorregresivos AR(p) (pesos aprendidos vía regresión)
   └── Diferenciación (para abordar no-estacionariedad)
        ↓
Evaluación rigurosa: train = pasado, test = futuro, métrica RMSE
        ↓
ML clásico (Random Forest + ventana deslizante + walk-forward validation)
        ↓
Deep Learning (LSTM, GRU, CNN temporales, Transformers)
```

---

---

## Parte 2: Procesamiento Básico de Imágenes

### 2.1 Tipos de imágenes en Visión por Computadora (CV)

Una imagen digital es, fundamentalmente, una **matriz de números**. Lo que para un humano es "una foto de un auto" es para la computadora una grilla de valores numéricos (intensidades de píxel).

|Tipo de imagen|Canales|Bits por píxel (bpp)|Descripción|
|---|---|---|---|
|**Escala de grises**|1|8 bpp (256 niveles, 0-255)|Solo intensidad luminosa, sin información de color|
|**RGB**|3 (Rojo, Verde, Azul)|24 bpp|El estándar más común en CV|
|**RGBA**|4 (RGB + Alpha/transparencia)|32 bpp|Color + canal de transparencia|
|**Multiespectral**|>10 bandas|Variable|Captura más allá del espectro visible (ej. infrarrojo cercano)|
|**Hiperespectral**|>100 bandas|Variable|Cientos de bandas espectrales muy estrechas|

**Ejemplos de aplicación de imágenes multi/hiperespectrales:**

- **Multiespectral:** medición de temperatura y emisividad de llamas (análisis térmico mediante cámara multiespectral + espectrómetro).
- **Hiperespectral:** dataset "Indian Pines" — 220 bandas espectrales usadas para **clasificar tipos de cobertura del suelo** (cultivos de maíz, soja, pastizales, bosques, etc.) a partir de imágenes satelitales/aéreas.

> **Punto clave:** mientras más bandas tiene una imagen, más información espectral contiene (útil para distinguir materiales que se ven "iguales" en RGB pero reflejan luz de forma distinta en otras longitudes de onda), pero también aumenta drásticamente el volumen de datos a procesar.

---

### 2.2 El Modelo RGB

**RGB** = **R**ed (Rojo), **G**reen (Verde), **B**lue (Azul).

**Fundamento biológico:** la retina humana tiene fotorreceptores tipo **conos** sensibles a tres rangos de longitud de onda que corresponden aproximadamente a:

- Azul (~445 nm)
- Verde (~535 nm)
- Rojo (~575 nm)

Además existen los **bastones**, células muy sensibles a la luz pero que no distinguen color — son responsables de la visión nocturna (escotópica).

**Por qué importa para CV:** dado que nuestra percepción del color se basa en la combinación de solo tres "canales", representar las imágenes digitales con tres canales (R, G, B) es suficiente para reproducir la inmensa mayoría de los colores que percibimos.

---

### 2.3 Corrección Gamma

#### Concepto

La corrección gamma es una transformación **no lineal** que se aplica a los valores de intensidad de los píxeles, típicamente de la forma:

$$I_{\text{salida}} = I_{\text{entrada}}^{\gamma}$$

(con los valores normalizados, generalmente en el rango [0,1]).

#### Efecto del parámetro γ

|Valor de γ|Efecto|
|---|---|
|$\gamma > 1$|**Aclara** la imagen (realza detalles en zonas oscuras)|
|$\gamma < 1$|**Oscurece** la imagen (realza detalles en zonas claras)|
|$\gamma = 1$|Sin cambio|

#### Ejemplo de aplicación práctica: imágenes médicas

Se mostró el ejemplo de una **resonancia magnética (RM) de una columna vertebral fracturada**, aplicando $\gamma = 0.6, 0.4, 0.3$. También se mostró un cerebro con valores de $\gamma$ entre 0.4 y 2.5.

**¿Por qué es útil en medicina?** Una resonancia magnética en bruto puede tener zonas demasiado oscuras donde hay estructuras importantes (como una fractura) que son difíciles de distinguir a simple vista. Aplicar la corrección gamma adecuada puede **resaltar esas estructuras** sin necesidad de volver a tomar la imagen, facilitando el diagnóstico visual.

> **Punto clave:** la corrección gamma es una de las transformaciones de **realce de imagen** más simples y baratas computacionalmente, y suele ser un primer paso de preprocesamiento antes de aplicar algoritmos más complejos (segmentación, detección de bordes, etc.).

---

### 2.4 Histogramas de Imágenes

#### Definición

El histograma de una imagen cuenta cuántos píxeles tienen cada nivel de intensidad:

$$h(k) = n_k$$

donde $k \in {0, \dots, L}$ representa un nivel de gris (para $L$ niveles posibles, ej. 256 para 8 bits) y $n_k$ es el número de píxeles de la imagen con ese valor.

#### Versión normalizada (función de densidad empírica)

$$p(k) = \frac{n_k}{n}$$

donde $n$ es el número total de píxeles. $p(k)$ puede interpretarse como un **estimador de la probabilidad** de que un píxel cualquiera de la imagen tenga el nivel de gris $k$.

#### ¿Para qué sirven los histogramas?

- **Análisis de iluminación/contraste:** un histograma "amontonado" hacia un extremo indica una imagen muy oscura o muy clara; un histograma bien distribuido sugiere buen contraste.
- **Segmentación en tiempo real:** son herramientas **simples y de bajo costo computacional**, ideales para sistemas que necesitan procesar video en vivo.
- **Comparación de imágenes/regiones:** si dos regiones tienen histogramas muy similares, probablemente representan el mismo tipo de objeto/textura/material (ver sección 2.5).

#### Histogramas en imágenes a color (RGB)

En lugar de un solo histograma, se calculan **tres histogramas independientes**, uno por canal (R, G, B). Esto permite analizar la distribución de cada componente de color por separado — por ejemplo, una imagen con tonos cálidos tendrá histogramas de R y G desplazados hacia valores altos, mientras que el de B se concentrará en valores bajos.

> **Tip práctico:** a veces es útil graficar los histogramas en **escala logarítmica** (eje Y), porque algunos valores (como el negro puro = 0) pueden tener frecuencias muy altas que "aplastan" visualmente el resto de la distribución en escala lineal.

---

### 2.5 Comparación de Histogramas: Distancia de Bhattacharyya

#### Fórmula

$$D_B(h_1, h_2) = \sqrt{1 - \sum_{i=1}^{N} \sqrt{h_1^{(i)} \times h_2^{(i)}}}$$

donde $N$ es el número de _bins_ de los histogramas (ambos **normalizados**) y $h_j^{(i)}$ es el valor del bin $i$ del histograma $j$.

#### Interpretación

|Valor de $D_B$|Significado|
|---|---|
|Cercano a **0**|Los histogramas son **muy similares** (probablemente representan contenido parecido)|
|Cercano a **1**|Los histogramas son **muy diferentes**|

#### Implementación (C++)

```cpp
// La Distancia de Bhattacharyya, para histogramas normalizados
double BhattacharyyaDistance(float *h1, float *h2, int N) {
    double D = 0.0;
    for (int i = 0; i < N; i++) {
        D += sqrt(h1[i] * h2[i]);
    }
    return D - 1 < 0 ? sqrt(1 - D) : 0.0;
}
```

#### Aplicación: clasificar/buscar regiones similares

En el ejemplo de la imagen "Lena": se selecciona una **región de interés (ROI)** pequeña (un pequeño parche de la imagen), se calcula su histograma, y luego se **desliza una ventana** sobre toda la imagen calculando el histograma de cada parche y comparándolo con el de la ROI usando la distancia de Bhattacharyya.

El resultado es un **mapa de calor (heatmap)** donde:

- Zonas oscuras (distancia baja) = regiones con distribución de intensidades **parecida** a la ROI original.
- Zonas claras (distancia alta) = regiones muy distintas.

> **Aplicación práctica:** este tipo de técnica permite encontrar regiones "similares" en una imagen sin necesidad de modelos complejos de deep learning — útil para tareas como detección de texturas repetidas, búsqueda de patrones, o como paso de preprocesamiento antes de un clasificador más sofisticado.

---

### 2.6 Segmentación de Imágenes

#### Definición

> Particionar una imagen en **múltiples segmentos** (conjuntos de píxeles), generalmente agrupando píxeles que comparten alguna propiedad (intensidad, color, textura) [Shapiro and Stockman, 2001].

**Aplicaciones típicas:**

- Segmentación de movimiento (ej. detectar qué píxeles cambiaron entre dos frames de video).
- Separar un objeto de interés del fondo (ej. aislar un tumor en una imagen médica, o un producto en una línea de empaque).

#### Segmentación binaria por umbralización (Thresholding)

El método más simple de segmentación: convertir una imagen en escala de grises a una imagen **binaria** (solo dos valores: 0 o `max_value`) según si cada píxel supera o no un umbral.

**Función de OpenCV:**

```cpp
cv::threshold(src, dst, threshold, max_value, type);
```

|Parámetro|Significado|
|---|---|
|`src`, `dst`|Imágenes de entrada y salida (un solo canal — escala de grises)|
|`threshold`|El valor umbral de corte|
|`max_value`|Valor a asignar a los píxeles que cumplen la condición|
|`type`|Tipo de umbralización (ver tabla siguiente)|

#### Tipos de umbralización

|`type`|Nombre|Comportamiento|
|---|---|---|
|0|**Binario**|Si $píxel > threshold$ → `max_value`; si no → `0`|
|1|**Binario Invertido**|Si $píxel > threshold$ → `0`; si no → `max_value`|
|2|**Truncado**|Si $píxel > threshold$ → `threshold` (se "recorta" el valor); si no → sin cambio|
|3|**Umbral a Cero**|Si $píxel > threshold$ → sin cambio; si no → `0`|
|4|**Umbral a Cero Invertido**|Si $píxel > threshold$ → `0`; si no → sin cambio|

**Ejemplo conceptual con una señal sinusoidal:**

Imaginemos una señal (o fila de píxeles) que sube y baja como una onda. Al aplicar un umbral (línea horizontal de corte):

- **Binario:** todo lo que está por encima de la línea se convierte en "100% blanco", todo lo de abajo en "0% negro" → genera una onda cuadrada.
- **Binario Invertido:** exactamente lo opuesto — lo de arriba se vuelve negro, lo de abajo blanco.
- **Truncado:** los picos que sobrepasan la línea se "aplanan" al nivel del umbral, pero los valles permanecen iguales.
- **Umbral a Cero:** los valles (por debajo del umbral) se convierten en cero, pero los picos mantienen su forma original.

> **Punto clave:** la elección del **umbral correcto** es crítica y depende mucho de la imagen específica. Un umbral mal elegido puede hacer que la segmentación binaria pierda información relevante (ej. partes del objeto de interés que quedan fuera) o incluya ruido del fondo.

---

### 2.7 Resumen del flujo conceptual — Procesamiento de Imágenes

```
Tipos de imagen (Grises / RGB / Multiespectral / Hiperespectral)
        ↓
Modelo RGB (basado en percepción humana del color)
        ↓
Corrección Gamma (realce de brillo/contraste no lineal)
        ↓
Histogramas (distribución de intensidades; base para análisis simple)
        ↓
Comparación de Histogramas (Distancia de Bhattacharyya)
   └── permite encontrar/clasificar regiones similares
        ↓
Segmentación (particionar la imagen en regiones)
   └── Umbralización binaria (5 variantes según OpenCV)
```

---

## Conclusiones generales

1. **El orden importa:** tanto en series de tiempo (orden temporal) como en histogramas espaciales (distribución de píxeles), el análisis exploratorio inicial (medias móviles, histogramas) sienta las bases para técnicas más sofisticadas.
    
2. **De lo simple a lo complejo:** en ambos temas el material sigue una progresión deliberada — empezar con métodos baratos e interpretables (naive forecast, umbralización) antes de pasar a modelos que requieren entrenamiento (AR, Random Forest) y finalmente a deep learning (LSTM, CNNs).
    
3. **La validación correcta es crucial:** en series de tiempo, **nunca** mezclar aleatoriamente entrenamiento y prueba — siempre respetar el orden cronológico y usar walk-forward validation cuando sea posible.
    
4. **Elegir el modelo según la estructura de los datos:** modelo aditivo vs. multiplicativo depende de si la estacionalidad es constante o crece con la tendencia; el tipo de umbralización depende de qué parte de la imagen (picos, valles, o ambos) interesa preservar.