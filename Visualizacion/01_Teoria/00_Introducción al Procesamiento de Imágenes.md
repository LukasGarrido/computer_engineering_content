# Introducción al Procesamiento de Imágenes

**Curso:** EIN092B - Visualización **Autor:** Jorge Portilla — Depto. de Electrónica e Informática, Universidad Técnica Federico Santa María, Concepción, Chile

---

## 1. Tipos de imágenes en visión por computador

La presentación parte diferenciando cómo se representa la información visual según la cantidad de "canales" o bandas que tiene una imagen:

- **Escala de grises:** cada píxel almacena un único valor que representa la intensidad luminosa (sin información de color). Es la representación más simple y económica en memoria.
- **RGB (Red, Green, Blue):** cada píxel se representa mediante tres valores (rojo, verde, azul). Es el formato más usado en visión por computador porque imita cómo el ojo humano percibe el color mediante tres tipos de receptores.
- **Imágenes multiespectrales:** capturan más de 10 bandas (canales) del espectro electromagnético, más allá del rango visible.
- **Imágenes hiperespectrales:** capturan más de 100 bandas, permitiendo un análisis mucho más fino de las propiedades espectrales de una escena (por ejemplo, para medir temperatura de llama o composición de materiales).

La imagen ilustrativa del vehículo (con sensores LIDAR/cámaras en el techo) muestra la idea clave: **lo que el ojo humano ve como una imagen "normal", la cámara en realidad lo capta como una matriz de números** (valores de intensidad por píxel). Esa matriz numérica es la verdadera "materia prima" con la que trabajan los algoritmos de procesamiento de imágenes.

---

## 2. Imágenes a color: profundidad de bits

Se introduce el concepto de **píxel** (picture element, "elemento de imagen"), la unidad mínima de una imagen digital, y se compara el costo en bits según el tipo de imagen:

|Tipo de imagen|Canales|Bits por píxel (bpp)|
|---|---|---|
|Escala de grises|1|8 bpp|
|Color (RGB)|3|24 bpp|
|Color + transparencia (RGBA)|4|32 bpp|

Es decir, una imagen a color ocupa 3 veces más memoria que una en escala de grises, y si además se guarda el canal alfa (transparencia), ocupa 4 veces más.

También se muestra la imagen clásica de prueba "Lenna" en escala de grises y en color, junto con sus **histogramas**: en escala de grises hay un solo histograma (niveles de 0 a 255), mientras que en color hay tres histogramas superpuestos, uno por cada canal (R, G, B), cada uno mostrando cómo se distribuyen las intensidades de ese canal en la imagen.

---

## 3. Modelo de color RGB

### 3.1 Fundamento fisiológico

El modelo RGB (Red, Green, Blue) se basa en cómo funciona la visión humana. La retina posee:

- **Conos:** células fotorreceptoras sensibles al color, con tres tipos que responden preferentemente a longitudes de onda cortas (azul, ~445 nm), medias (verde, ~535 nm) y largas (rojo, ~575 nm).
- **Bastones:** células mucho más sensibles a la luz (pero no al color), responsables de la visión en condiciones de poca luz (visión nocturna o escotópica), con un pico de sensibilidad alrededor de 498 nm.

Como el ojo humano interpreta el color como combinaciones de estas tres señales (rojo, verde, azul), los sistemas digitales imitan este principio combinando tres canales primarios.

### 3.2 El cubo RGB

El espacio de color RGB se representa geométricamente como un **cubo unitario**, donde cada eje corresponde a la intensidad de un canal (normalizada entre 0 y 1):

- El vértice (0,0,0) es el **negro** (ausencia de luz).
- El vértice (1,1,1) es el **blanco** (máxima intensidad en los tres canales).
- Los demás vértices corresponden a los colores primarios (rojo, verde, azul) y sus combinaciones secundarias (cian, magenta, amarillo).
- La **diagonal** que une el negro con el blanco, formada por puntos del tipo (i, i, i) —es decir, con las tres componentes iguales—, recorre exactamente todos los **niveles de gris**. Esto tiene sentido: si los tres canales tienen la misma intensidad, no hay dominancia de ningún color y el resultado es un tono neutro de gris.

El modelo RGB es **aditivo**: se parte de negro (ausencia de luz) y se van sumando cantidades de rojo, verde y azul para producir el resto de los colores (a diferencia de modelos sustractivos como CMYK usados en impresión).

### 3.3 Atributos perceptuales del color

Independientemente del modelo RGB, un color se puede describir mediante tres atributos perceptuales:

- **Brillo (brightness):** la intensidad general del color. El blanco es más brillante que el gris.
- **Matiz (Hue):** es lo que coloquialmente llamamos "el color" en sí (rojo, verde, azul, etc.). Está asociado a la longitud de onda dominante en la mezcla de luz, y es lo que nos permite distinguir y nombrar un color.
- **Saturación:** mide la pureza del color, es decir, cuánta luz blanca está "diluyendo" el matiz. Un color totalmente saturado no tiene mezcla de blanco (por ejemplo, un azul puro tiene saturación máxima); un punto blanco puro tiene saturación 0, porque no hay matiz dominante.

Estos tres atributos son la base de modelos de color alternativos al RGB, como HSV o HSL, que separan explícitamente el matiz, la saturación y el brillo (útiles, por ejemplo, para segmentar objetos por color de forma más robusta que en RGB).

---

## 4. Corrección Gamma

### 4.1 La transformación

La corrección gamma es una transformación **no lineal** aplicada a la intensidad de cada píxel, definida como:

```
q(x, y) = p(x, y)^γ
```

donde `p(x, y)` es la intensidad de entrada (normalizada al intervalo [0, 1]) y `q(x, y)` es la intensidad de salida. El parámetro **γ (gamma)** controla el efecto:

- **γ = 1:** no hay cambio, la imagen permanece igual.
- **γ < 1:** la imagen se **aclara** (se incrementa el brillo, especialmente en las zonas oscuras/sombras).
- **γ > 1:** la imagen se **oscurece** (se reduce el brillo en las sombras).

### 4.2 Consideraciones prácticas

- Antes de aplicar la función, los valores de píxel (típicamente en el rango 0-255) deben normalizarse al intervalo [0, 1], ya que la función potencia se define correctamente en ese rango.
- Como calcular `pow()` para cada píxel es computacionalmente costoso (especialmente en C++), en la práctica es más eficiente **precalcular una tabla de transformación** (lookup table, LUT) con los 256 valores posibles de entrada y sus correspondientes salidas, y luego simplemente consultar esa tabla para cada píxel en lugar de recalcular la potencia.

### 4.3 Aplicación: contraste

Se usa principalmente para **mejorar el contraste de forma controlada**. Los ejemplos del documento muestran:

- Una **resonancia magnética (RM)** de una columna vertebral fracturada, donde se aplican valores de γ = 0.6, 0.4 y 0.3, aclarando progresivamente la imagen y revelando detalles que estaban ocultos en zonas oscuras.
- Un conjunto de **cortes de resonancia cerebral** con γ variando entre 0.4 y 2.5, mostrando visualmente cómo valores menores a 1 aclaran la imagen y valores mayores a 1 la oscurecen.

Esta técnica es especialmente valiosa en imágenes médicas, donde ajustar el contraste puede hacer visibles estructuras anatómicas que de otro modo pasarían desapercibidas.

---

## 5. Histogramas

### 5.1 Definición

El histograma de una imagen cuenta cuántos píxeles tienen cada nivel de intensidad:

```
h(k) = n_k
```

donde `k` es un nivel de gris (entre 0 y L, siendo L el máximo nivel, típicamente 255) y `n_k` es el número de píxeles con ese valor.

También se define la versión **normalizada**:

```
p(k) = n_k / n
```

con `n` el número total de píxeles. Esta versión normalizada puede interpretarse como un **estimador de la probabilidad** de que un píxel elegido al azar tenga el nivel de gris `k`.

### 5.2 Utilidad

Los histogramas son herramientas fundamentales porque son **simples y de bajo costo computacional**, lo que los hace ideales para tareas como **segmentación de imágenes en tiempo real** (por ejemplo, separar un objeto del fondo según su distribución de intensidades).

### 5.3 Histograma en color

Para una imagen RGB se puede calcular un histograma por canal (R, G, B) por separado, lo que permite ver cómo se distribuye la intensidad de cada color. El documento muestra el ejemplo de la imagen "Lenna": los histogramas RGB en escala normal y en **escala logarítmica** (que permite visualizar mejor las frecuencias bajas, que quedarían aplastadas en una escala lineal), comparados con el histograma equivalente de la versión en escala de grises.

---

## 6. Filtros espaciales

### 6.1 Concepto de convolución

Un **filtro espacial** es una operación que se aplica a la **vecindad** de cada píxel (no al píxel de forma aislada), mediante la operación matemática de **convolución**. Se le llama indistintamente máscara, filtro, kernel o ventana.

La convolución consiste en:

1. Colocar el kernel (una matriz pequeña, por ejemplo 3x3) centrado sobre cada píxel de la imagen.
2. Multiplicar cada valor del kernel por el valor del píxel correspondiente en la imagen.
3. Sumar todos esos productos.
4. El resultado es el nuevo valor del píxel central en la imagen de salida.

Este proceso se repite desplazando el kernel por toda la imagen ("input" convolucionado con "kernel" produce el "output").

### 6.2 Complejidad computacional

Para una imagen de tamaño M×N y un kernel de tamaño u×v, el pseudocódigo recorre:

- Cada fila de la imagen (excluyendo bordes en la versión simple).
- Cada columna de la imagen.
- Cada fila del kernel.
- Cada columna del kernel.

Esto da una **complejidad total de M × N × u × v** operaciones. Es decir, el costo crece linealmente con el tamaño de la imagen y con el tamaño del kernel (y cuadráticamente si el kernel es cuadrado, u=v). Por convención, el tamaño del kernel suele ser impar, para que exista un píxel central bien definido.

### 6.3 Filtros de suavizado (smoothing)

Los filtros de suavizado (o de promedio) se usan para **difuminar (blur)** la imagen o **eliminar ruido**. Su efecto es promediar (de forma ponderada) los píxeles vecinos, reduciendo las transiciones abruptas de intensidad.

Dos ejemplos clásicos:

- **Filtro promedio 3x3:** todos los coeficientes son 1, y se normaliza multiplicando por 1/9.
- **Filtro gaussiano 3x3:** los coeficientes siguen una forma de campana (más peso al centro), normalizado por 1/16.

**¿Por qué deben estar normalizados?** Porque la suma de los coeficientes multiplicada por el factor de normalización debe dar 1. Esto garantiza que la **luminosidad promedio de la imagen no cambie** tras aplicar el filtro (la imagen no se aclara ni se oscurece artificialmente, solo se suaviza).

### 6.4 Otros kernels espaciales

El documento muestra varios kernels 3x3 típicos y su efecto:

- **Paso alto (sharpening):** resalta bordes y detalles finos, aumentando el contraste donde hay cambios rápidos de intensidad (kernel con -1 alrededor y un valor alto, ej. 5, en el centro).
- **Detección de bordes:** un kernel tipo Laplaciano (con -1 en los ocho vecinos y 8 en el centro) que resalta fuertemente los contornos de los objetos.
- **Relieve (emboss):** un kernel asimétrico (valores negativos de un lado, positivos del otro) que produce un efecto de relieve/3D, ya que su característica principal es justamente esa asimetría direccional.

Se muestran también ejemplos visuales aplicados a una fotografía real (un callejón), donde se aprecia cómo el filtro promedio y el gaussiano difuminan la imagen, el paso alto y la detección de bordes resaltan contornos, y el filtro de relieve genera un efecto de textura en relieve.

### 6.5 Filtro gaussiano en detalle

El filtro gaussiano deriva sus coeficientes de la función gaussiana 2D centrada en el origen:

```
G(x, y) = (1 / (2π σ²)) · e^(-(x² + y²) / (2σ²))
```

Su propiedad clave es que es **isotrópico**: su efecto es el mismo en todas las direcciones, porque la fórmula depende únicamente de la distancia euclidiana `r = √(x² + y²)` al centro, no de la orientación. Gráficamente, esto se traduce en que el filtro forma un patrón de **círculos concéntricos** de igual valor (como una campana de revolución). Al ser invariante a la rotación del sistema de coordenadas, se dice que la respuesta del filtro es la misma sin importar la dirección.

En la práctica, el parámetro σ (desvío estándar) puede configurarse de forma independiente en cada eje, permitiendo suavizados asimétricos si fuera necesario. El ejemplo muestra un kernel gaussiano 5x5 con σ = 1, donde los coeficientes decrecen suavemente desde el centro (0.159) hacia los bordes (0.003).

### 6.6 Filtro mediano

A diferencia de los filtros anteriores (que son **lineales**, pues son sumas ponderadas), el filtro mediano es **no lineal**:

- En vez de promediar los píxeles de la vecindad, ordena todos sus valores y toma el **valor central (mediana)** de esa secuencia ordenada.
- Es "no sesgado por outliers": si hay un valor extremo (por ejemplo, ruido tipo "sal y pimienta", con píxeles completamente blancos o negros aislados), ese valor no afecta tanto al resultado como lo haría en un promedio, porque simplemente queda relegado a un extremo de la lista ordenada y no participa en el cálculo salvo que domine la vecindad.

Ejemplo del documento: para la vecindad

```
200 203 255
180 190 208
150   0 195
```

el conjunto ordenado es {0, 150, 180, 190, 195, 200, 203, 208, 255}, y la mediana (valor central de 9 elementos) es **195**. Nótese cómo el valor atípico "0" prácticamente no influye en el resultado, mientras que en un filtro promedio sí distorsionaría fuertemente el valor de salida.

En OpenCV esta operación se implementa con la función `medianBlur(src, dst, ksize)`, donde `ksize` es el tamaño (impar, mayor que 1) de la ventana cuadrada.

El ejemplo visual con una resonancia cerebral con ruido tipo "sal y pimienta" muestra cómo el filtro mediano elimina ese ruido de forma mucho más efectiva que el filtro promedio (que tiende a "esparcir" el ruido en vez de eliminarlo), preservando mejor los bordes de las estructuras.

---

## 7. Segmentación: Umbralización (Thresholding) de Otsu

### 7.1 Idea general

La **umbralización** es una técnica de segmentación que separa una imagen en dos regiones (fondo y objeto) según un valor de intensidad umbral. En OpenCV:

```
cv::threshold(src, dst, threshold, max_value, type);
```

En la umbralización **global simple**, el usuario debe elegir manualmente el valor de umbral. El **método de Otsu**:

```
cv::threshold(im_gray, img_bw, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);
```

es también un método global, pero **elige automáticamente el umbral óptimo**, sin intervención manual. Está pensado para imágenes con histograma **bimodal** (dos picos bien diferenciados, uno correspondiente al fondo y otro al objeto).

### 7.2 Formulación matemática

El método busca dividir el histograma en dos clases, C0 (fondo) y C1 (objeto), eligiendo el umbral `k` que **maximiza la varianza entre clases**.

Se definen:

- **Probabilidad acumulada** hasta el nivel k: `w(k) = Σ p(i)` para i=1 hasta k. Representa la proporción de píxeles de la imagen con intensidad menor o igual a k.
- **Media acumulada** hasta el nivel k: `μ(k) = Σ i·p(i)` para i=1 hasta k.

A partir de esto:

- Probabilidad de la clase fondo: `w0 = w(k)`
- Probabilidad de la clase objeto: `w1 = 1 - w(k)`
- Media del fondo: `μ0 = μ(k) / w(k)`
- Media del objeto: `μ1 = (μT - μ(k)) / (1 - w(k))`, donde μT es la media total de la imagen.

El objetivo es maximizar la **varianza entre clases**:

```
σ²_b(k) = w0 · w1 · (μ0 - μ1)²
```

Tras un desarrollo algebraico (usando que w0 + w1 = 1 y μT = μ0·w0 + μ1·w1), esta expresión se puede simplificar a una forma equivalente y más eficiente de calcular:

```
σ²_B = w0 · w1 · (μ1 - μ0)²
```

Esta versión simplificada solo requiere las medias y probabilidades acumuladas, lo que permite implementarla de forma muy eficiente recorriendo el histograma una sola vez y probando cada posible umbral k.

### 7.3 Ejemplo numérico

El documento incluye un ejemplo simplificado con un histograma de 6 niveles de gris (0 a 5), dividiendo en fondo (niveles 0-1) y objeto (niveles 2-5):

- `Wb = (9+6)/36 = 0.42` (proporción del fondo)
- `Wf = (4+5+8+4)/36 = 0.58` (proporción del objeto)
- `μb = (9×0 + 6×1)/(9+6) = 0.4` (media del fondo)
- `μf = (4×2 + 5×3 + 8×4 + 4×4)/(4+5+8+4) = 3.57` (media del objeto)
- `σ²_B = Wb · Wf · (μb - μf)² = 2.44`

Este cálculo se repetiría para cada posible umbral k, y el método de Otsu elige el k que da el valor máximo de σ²_B.

### 7.4 Ventajas y desventajas

**Ventajas:**

- Es automático, no requiere ajustar manualmente el umbral.
- Es rápido y eficiente en imágenes bimodales (histograma con dos picos bien definidos).
- Funciona bien cuando hay buen contraste entre el objeto y el fondo.

**Desventajas:**

- No funciona bien en imágenes con distribución **unimodal** (sin picos bien separados).
- Es **sensible a iluminación no uniforme** (si la imagen tiene zonas con brillo desigual, el umbral global puede fallar en algunas regiones).
- No está pensado para segmentar **múltiples clases**: solo puede dividir la imagen en dos regiones.

### 7.5 Ejemplo visual

El documento compara la umbralización con un valor global fijo (127) versus el umbral automático de Otsu (102) sobre la clásica imagen "cameraman". Ambos métodos logran separar razonablemente al operador de cámara del fondo, aunque con diferencias en el detalle capturado.

Un segundo ejemplo, más revelador, usa la misma imagen pero con el **brillo reducido**: en ese caso, el umbral **global fijo (127) falla completamente**, produciendo una imagen totalmente negra (porque ningún píxel supera ese umbral tras oscurecer la imagen), mientras que **Otsu se adapta automáticamente** a la nueva distribución de intensidades y logra seguir segmentando correctamente la figura del fotógrafo. Esto ilustra de forma muy clara la principal ventaja práctica de Otsu frente a un umbral fijo: su capacidad de adaptarse a los cambios de iluminación de la imagen (dentro de los límites de una distribución bimodal razonable).

---

## Resumen general del documento

La presentación recorre, de forma progresiva, los pilares básicos del procesamiento digital de imágenes:

1. **Representación de la imagen:** desde escala de grises hasta datos hiperespectrales, y cómo se codifica en bits.
2. **Modelo de color RGB:** su base fisiológica, su geometría (el cubo de color) y los atributos perceptuales (brillo, matiz, saturación).
3. **Transformaciones de intensidad:** la corrección gamma como herramienta de ajuste de contraste no lineal.
4. **Análisis estadístico de la imagen:** histogramas, como base para muchas técnicas posteriores.
5. **Filtrado espacial:** la convolución como operación fundamental, sus filtros de suavizado (promedio, gaussiano, mediano) y sus filtros de realce (paso alto, detección de bordes, relieve), junto con su costo computacional.
6. **Segmentación:** el método de Otsu como técnica automática y eficiente de umbralización basada en el histograma, con su formulación matemática completa y sus limitaciones prácticas.

En conjunto, estos temas conforman la base conceptual típica de un primer acercamiento al procesamiento de imágenes, sirviendo de fundamento para técnicas más avanzadas de visión por computador.