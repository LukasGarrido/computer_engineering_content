# Visualización de Datos — Errores Comunes y Distracciones (versión ampliada)

**Curso:** EIN092B – Visualización
**Referencias principales:** Stephen Few, *Show Me the Numbers* (2ª ed., 2012) · Edward Tufte, *The Visual Display of Quantitative Information* (1983) · Cleveland & McGill, "Graphical Perception" (1984) · Alberto Cairo, *How Charts Lie* (2019) · Claus Wilke, *Fundamentals of Data Visualization* (2019)

> **Cómo usar este documento.** La versión original describía casos. Esta versión mantiene esos casos, pero añade lo que faltaba: **la teoría que explica por qué un gráfico falla**, **cómo corregirlo**, **reglas prácticas**, **código de ejemplo**, **una lista de verificación** y **ejercicios con respuestas**. Está organizado para que puedas pasar de "reconocer el error" a "evitarlo en tus propios gráficos".

---

## 0. Ideas base (léelas primero)

Casi todos los errores de las secciones siguientes se explican con cinco ideas.

### 0.1 Un gráfico es un argumento, no un adorno
Todo gráfico responde una pregunta ("¿quién vende más?", "¿cómo evolucionó X?", "¿se relacionan A y B?"). Si no puedes decir la pregunta en una frase, el gráfico probablemente sobra o está mal elegido.

### 0.2 No todas las codificaciones visuales se leen igual de bien
Cleveland y McGill (1984) ordenaron las tareas perceptuales según la **precisión** con que las personas estimamos valores:

| Precisión | Codificación | Ejemplo |
|---|---|---|
| 1 (mejor) | Posición sobre una escala común | Puntos en un scatter, barras con la misma base |
| 2 | Posición en escalas no alineadas | Paneles separados con ejes distintos |
| 3 | Longitud | Barras |
| 4 | Ángulo / pendiente | Porciones de pie, inclinación de una línea |
| 5 | Área | Burbujas, treemaps |
| 6 (peor) | Volumen, color (saturación/tono) | Barras 3D, mapas de calor |

**Consecuencia:** si quieres que se comparen valores con precisión, usa posición o longitud (puntos y barras). Los pies (ángulo) y las burbujas (área) sirven para aproximaciones, no para comparaciones finas. Los errores 3D, de pie y de radio/área de más abajo son casos directos de esta jerarquía.

### 0.3 Relación datos-tinta y "Lie Factor" (Tufte)
- **Data-ink ratio:** la mayor parte de la "tinta" del gráfico debería representar datos. Rejillas pesadas, sombras, fondos, íconos y texturas son *chartjunk* si no aportan información.
- **Lie Factor:** `tamaño del efecto mostrado en el gráfico ÷ tamaño del efecto en los datos`. Lo ideal es cercano a 1. Un eje truncado o un radio mal escalado lo disparan (ver ejemplos más abajo).

### 0.4 Atributos preatentivos: lo que el cerebro ve antes de pensar
Color, tamaño, posición, orientación y forma se detectan en menos de ~250 ms. Úsalos **para destacar lo importante** (una barra en color fuerte, el resto en gris). Si todo está destacado, nada lo está.

### 0.5 Principios de Gestalt útiles
- **Proximidad:** lo cercano se percibe como grupo (junta lo que quieres comparar).
- **Similitud:** mismo color/forma = misma categoría (por eso un color debe significar una sola cosa).
- **Continuidad:** una línea sugiere secuencia. Conectar categorías nominales con líneas crea una "tendencia" que no existe.

---

## 1. Percepción visual: por qué el color y el contexto no son neutros

Tres ilusiones clásicas muestran que el cerebro no mide valores absolutos, sino que **interpreta en relación con el contexto**.

### 1.1 Tablero de Adelson (contraste simultáneo)
Los cuadros A y B tienen **exactamente el mismo gris**, pero B, dentro de la sombra, parece más claro. El cerebro "corrige" por la sombra que infiere en la escena.

**En visualización:** una barra o región de un mapa puede parecer más clara u oscura según los colores vecinos.

**Qué hacer:**
- Sobre un mismo gráfico, usa **fondo uniforme y neutro** (blanco o gris muy claro).
- Evita rodear marcas de color con otras marcas de color muy distintas en luminosidad.
- Si el valor exacto importa, **añade la etiqueta numérica** en vez de depender solo del color.

### 1.2 Patrón de textura (insensibilidad a la orientación)
Un cambio sutil de orientación en un patrón denso pasa inadvertido, mientras que un cambio de color o brillo se nota de inmediato.

**En visualización:** no uses textura, rayado o cambios sutiles de orientación para distinguir categorías que deben detectarse rápido. Usa **posición, longitud o color**.

### 1.3 Efecto Bezold (asimilación cromática)
La misma línea se ve grisácea sobre amarillo y amarillenta sobre gris: el fondo "contamina" al elemento que lo cruza.

**En visualización:** líneas delgadas y texto pequeño son los más vulnerables. Prefiere **líneas más gruesas**, y **alto contraste** entre elemento y fondo.

### 1.4 Reglas prácticas de color que se derivan de estas ilusiones

| Tipo de dato | Paleta recomendada | Ejemplo |
|---|---|---|
| Ordenado, de menos a más | **Secuencial**: un solo tono de claro a oscuro | Esperanza de vida, casos por 100 000 hab. |
| Con punto medio significativo | **Divergente**: dos tonos que se juntan en un neutro | Variación respecto al plan (rojo/gris/azul) |
| Categorías sin orden | **Cualitativa**: colores distinguibles, **máx. 6–8** | Regiones, tipos de producto |

Además:
- **Accesibilidad:** ~8 % de los hombres tiene daltonismo (sobre todo rojo-verde). No dependas solo de rojo vs. verde; combina con etiquetas, formas o luminosidad distinta. Herramientas: *ColorBrewer*, *Viridis*, *Coblis* (simulador).
- **Color con sentido semántico:** si una categoría se llama "naranja" o "verde", que lo sea (ver 3.C).
- **Un color = un significado** en todo el documento (si "2023" es azul en un gráfico, que no sea rojo en el siguiente).
- **Contraste de texto:** ratio mínimo 4,5:1 (recomendación WCAG).

---

## 2. Taxonomía: elegir el gráfico según la tarea analítica (Stephen Few)

**Idea central:** primero se define la **pregunta**, luego el gráfico. Nunca al revés.

### 2.1 Tabla de decisión rápida

| Tarea / pregunta | Gráfico recomendado | Evitar | Consejo clave |
|---|---|---|---|
| **Ranking** ("¿quién es mayor?") | Barras ordenadas de mayor a menor (horizontales si los nombres son largos) | Pie, radar | Ordena por valor, no alfabéticamente |
| **Comparación nominal** (categorías sin orden) | Barras (o puntos) | Líneas | El orden es libre: elige uno lógico y explícito |
| **Correlación** (dos variables numéricas) | Dispersión (scatter) + línea de tendencia opcional | Barras enfrentadas como recurso principal | Con muchos puntos: transparencia o *hexbin* |
| **Desviación** (vs. plan o referencia) | Barras desde una línea base cero; líneas; puntos+línea | Barras sin línea de referencia visible | Marca la referencia (0 % o el plan) claramente |
| **Distribución** (¿cómo se reparten los valores?) | Histograma, polígono de frecuencia, box plot, violín | Barras de promedios sin dispersión | Muestra dispersión, no solo el promedio |
| **Geoespacial** | Símbolos proporcionales, coroplético, flujo | Coroplético con valores absolutos | Normaliza (por población, por área) |
| **Parte a todo** | Barras apiladas 100 %, treemap, pie/dona (solo pocas partes) | Pie con más de 5 partes o que no suman 100 % | Si necesitas comparar partes con precisión, usa barras |
| **Serie de tiempo** | Líneas (con o sin puntos); barras para pocos períodos | Categorías nominales unidas por líneas | Eje temporal con intervalos regulares |

### 2.2 Detalles que enriquecen cada tarea

**Ranking y comparación nominal**
- Las barras funcionan porque comparamos **longitudes con una base común**. Por eso **las barras deben partir de cero** (ver 3.A).
- Si hay muchas categorías (>15) o etiquetas largas, usa barras horizontales o un **gráfico de puntos (dot plot)**.
- Un gráfico de **"lollipop"** (palito con punto) es una alternativa más limpia cuando hay muchas barras.

**Correlación**
- Correlación no implica causalidad. Ejemplo clásico: ventas de helados y ahogamientos suben juntas en verano; la causa común es el calor.
- Con muchos puntos superpuestos usa transparencia; con una tercera variable, color o tamaño (con moderación).

**Desviación**
- Ejemplo: ventas reales vs. plan. Barras hacia arriba (sobre el plan) en un color y hacia abajo (bajo el plan) en otro; la línea cero es la referencia.
- Alternativa útil: **bullet graph** (Few) para comparar valor real, meta y rangos de desempeño en poco espacio.

**Distribución**
- **Histograma:** el ancho del intervalo (*bin*) cambia la forma; prueba varios anchos.
- **Polígono de frecuencia:** mejor que barras para superponer 2 o 3 distribuciones.
- **Box plot:** mediana, cuartiles Q1–Q3 (50 % central), bigotes y valores atípicos. Ejemplo: salarios de dos áreas con la misma mediana pero una con mucha más dispersión: el promedio las muestra "iguales", el box plot no.

**Geoespacial**
- **Coroplético:** ideal para tasas o densidades (casos por 100 000 hab.), **no** para conteos absolutos (los estados grandes o poblados siempre "ganan").
- **Símbolos proporcionales:** el **área** (no el radio) debe ser proporcional al valor.

**Parte a todo**
- Barras simples → buenas para comparar magnitudes; barras apiladas → muestran la composición; agrupadas → comparan cada categoría entre períodos pero pierden el total.
- En barras apiladas solo el primer segmento (el de la base) se compara con precisión; los demás "flotan". Si el foco es comparar una categoría intermedia, usa barras agrupadas o *small multiples*.

**Series de tiempo**
- Líneas transmiten continuidad y tendencia. Barras: válidas para pocos períodos discretos.
- Para muchas series, usa **small multiples** (un mini-gráfico por serie con el mismo eje).

### 2.3 Otros gráficos útiles que conviene conocer

| Gráfico | Para qué sirve |
|---|---|
| **Small multiples** (múltiplos pequeños) | Comparar muchas series sin saturar; mismos ejes en todos los paneles |
| **Slopegraph** | Comparar dos momentos (antes/después, 1995 vs. 2017) por categoría |
| **Sparkline** | Tendencia mínima dentro de una tabla o texto |
| **Heatmap** | Patrones en matrices (día × hora), con paleta secuencial |
| **Waterfall (cascada)** | Cómo se compone un cambio total (ingresos → costos → utilidad) |
| **Dot plot / lollipop** | Rankings con muchas categorías o valores lejos de cero |

---

## 3. Catálogo de errores en visualizaciones reales

En lugar de recorrer los 28 casos en orden, esta versión los **agrupa por tipo de error**, que es lo que realmente conviene aprender. Cada grupo tiene: *qué pasa*, *por qué engaña*, *cómo corregirlo* y *casos del material original*.

### Grupo A. Ejes y escalas

#### A1. Eje Y truncado en barras
**Casos:** 3.10 (delitos en NYC, eje desde 94 000), 3.11 (ráfagas de viento).

**Por qué engaña:** en las barras, el ojo compara **longitudes**. Si se recorta la base, la proporción visual deja de coincidir con la proporción real.

**Ejemplo numérico (Lie Factor):**
- Datos: 100 y 107 → diferencia real de **7 %**.
- Con eje desde 95, las barras miden 5 y 12 → la segunda parece **140 % más grande**.
- Lie Factor = 140 / 7 = **20**. El gráfico exagera el cambio 20 veces.

**Cómo corregir:**
- Barras: **siempre desde cero**.
- Si lo que importa es un cambio pequeño, muestra la **variación** (por ejemplo, +7,5 %) o usa un **gráfico de líneas / puntos**, donde un eje no cero es aceptable (con eje claramente rotulado).

> **Matiz:** truncar el eje es aceptable en **líneas y puntos** (donde se compara posición, no longitud), no en barras.

#### A2. Eje Y invertido
**Caso:** 3.26 (*Gun deaths in Florida*, Reuters). Es un ejemplo famoso: el diseño con el eje invertido evoca sangre goteando, y la curva "sube" justo cuando las muertes bajan.

**Por qué engaña:** la convención universal es que *arriba = más*. Invertirla contradice la intuición; muchos lectores no leen los números del eje.

**Cómo corregir:** mantener la convención. Si hay una razón fuerte (ej.: rankings donde el 1 va arriba, profundidad en el mar), **avisarlo explícitamente** en el título o en el eje.

#### A3. Doble eje Y
**Caso:** 3.27 (letalidad COVID en Suecia por edad: 0–1,25 % vs. 0–40 %).

**Por qué engaña:** con dos escalas, una barra que mide "lo mismo" en pantalla puede representar cifras 32 veces distintas (40 / 1,25). Además, quien dibuja puede elegir escalas para que las líneas "se crucen" y sugieran una relación inexistente.

**Cómo corregir:**
- Un único eje común (aunque las barras chicas se vean pequeñas: **esa es la realidad de los datos**).
- Si las magnitudes son muy distintas, usa **dos paneles apilados** que compartan el eje X.
- Si lo importante es la forma, **indexa las series a 100** en un mismo punto de partida.
- Usa escala logarítmica solo si el público la entiende y se rotula.

#### A4. Escalas distintas en gráficos vecinos
**Casos:** 3.5 (BBC: casos 0–100 000 vs. muertes 0–1 750) y 3.18 (superficies del coronavirus, ejes 0–25 vs. 0–20).

**Por qué engaña:** dos gráficos lado a lado invitan a comparar sus formas o longitudes; si los ejes difieren, la comparación es falsa. En 3.5 hay además un problema de **contexto**: las muertes se retrasan semanas respecto de los casos, por lo que "muertes estables" no significa "casos sin efecto".

**Cómo corregir:**
- Si se van a comparar, **mismos ejes** (small multiples).
- Si no pueden coincidir (unidades distintas), **separarlos claramente** y señalarlo en el título/subtítulo.
- Añadir la explicación del rezago cuando sea relevante.

---

### Grupo B. Elección incorrecta del tipo de gráfico

#### B1. Pie/dona con datos que **no suman 100 %**
**Casos:** 3.13 (50 % + 35 % = 85 %, pero dibujado 50/50), 3.14 (73 + 69 + 46 = **188 %**), 3.15 (69 + 38 + 35 + 32 + 31 = **205 %**).

**Por qué engaña:** un pie **promete** que las partes forman un todo. Si son respuestas múltiples o porcentajes independientes, esa promesa es falsa; y si además se dibuja con ángulos que no corresponden a los números (3.13), el engaño es doble.

**Prueba rápida antes de usar un pie:** ¿las partes son **exclusivas** y **suman 100 %**? Si la respuesta es no → **barras**.

**Cómo corregir:** barras horizontales ordenadas, cada una con su porcentaje. Cambiar el título a algo como "% de encuestados que eligió cada cambio (respuesta múltiple)".

#### B2. Pie con demasiadas categorías
**Casos:** 3.22 (≈30 porciones), 3.21 (10 frutas).

**Por qué falla:** el ángulo es una codificación poco precisa (nivel 4 de la jerarquía) y con porciones diminutas es ilegible.

**Regla práctica:** pie/dona solo con **2 a 5 partes** y una comparación aproximada (*"más de la mitad"*). Para lo demás, barras ordenadas.

#### B3. Pie usado para un proceso o una progresión
**Casos:** 3.16 (siembra de maíz, 4 pies por semana), 3.3 (pie con 4 años iguales, sin datos).

**Por qué falla:**
- 3.16: el avance semanal es **una variable en el tiempo**, no partes de un todo, y cuatro pies separados impiden comparar.
- 3.3: es **decoración pura**, ocupa espacio sin transmitir datos.

**Cómo corregir:**
- 3.16 → **un solo gráfico de líneas** (semana en X, % sembrado en Y) con dos líneas: "año actual" y "promedio de 5 años".
- 3.3 → eliminar el gráfico o reemplazarlo por un dato real (número de vehículos faltantes por año en barras).

#### B4. Líneas entre categorías nominales
**Caso:** 3.2 (*How couples met*: trabajo, bar, online, colegio…, unidas con líneas).

**Por qué engaña:** una línea sugiere continuidad y orden ("de trabajo a bar hay una pendiente"), pero esas categorías no tienen ninguno. Además el orden del eje es arbitrario, así que la "forma" de la línea cambia si se reordena.

**Cómo corregir:** barras agrupadas (1995 vs. 2017) **ordenadas por valor**, o un **slopegraph** si lo que interesa es el cambio entre las dos fechas.

#### B5. Donas duplicadas para un valor complementario
**Caso:** 3.1 (dona 86 % hombres y dona 14 % mujeres).

**Por qué es ineficiente:** con dos categorías, el segundo valor es el complemento del primero: dos gráficos repiten la misma información y obligan a comparar entre dos figuras separadas.

**Cómo corregir:** una sola **barra apilada al 100 %**, o simplemente el texto "86 % hombres · 14 % mujeres". Para dos valores, un número grande suele bastar.

#### B6. Pie con pocas categorías, pero diferencia pequeña
**Caso:** 3.6 (Quinnipiac: 45 % a favor, 51 % en contra, 4 % NS/NR).

**Observación:** aquí los datos sí suman 100 %, y el pie es un uso *aceptable*. El límite es perceptual: distinguir 45 % de 51 % con ángulos es difícil. Si la diferencia es el titular, **barras** la muestran con claridad. Además, verifica que los ángulos estén dibujados con software de datos y no "a mano".

---

### Grupo C. Uso del color

#### C1. Demasiados colores
**Casos:** 3.4 (16 colores, uno por año), 3.19 (~50 líneas, una por estado).

**Por qué falla:** más de 6–8 colores no se distinguen ni se recuerdan; el lector va y viene entre leyenda y gráfico ("visual lookup").

**Cómo corregir:**
- **Resaltado selectivo:** una o pocas series en color, el resto en gris.
- **Etiquetado directo** al final de cada línea (sin leyenda).
- **Small multiples:** un panel por estado/año.
- Si el color es redundante con la posición (3.4: los años ya están ordenados), usa **un solo color** o una **rampa secuencial** de un mismo tono.

#### C2. Color que contradice el nombre
**Casos:** 3.20 (leyenda "Orange" en teal, "Green" en rojo), 3.21 (naranjas en verde lima).

**Cómo corregir:** si la categoría tiene un color natural (naranja, banana, verde), úsalo. Cuando no lo tenga, evita colores con nombre en las etiquetas.

#### C3. Paleta inadecuada para el tipo de dato
**Caso:** 3.7 (esperanza de vida con verdes y azul-morado mezclados).

**Por qué falla:** el dato es ordenado (bajo → alto), pero la paleta no tiene un orden natural de luminosidad.

**Cómo corregir:** **una sola gama secuencial** (por ejemplo, azul claro → azul oscuro). El más oscuro = valor más alto. Usar ColorBrewer o Viridis.

#### C4. Intervalos desiguales o valores absolutos en mapas
**Caso:** 3.8 (MSNBC: casos COVID en categorías 1 000+, 100 000+, 500 000+, 1 000 000+).

**Por qué engaña:**
1. Los conteos absolutos reflejan **el tamaño de la población** más que el riesgo (California siempre parecerá peor que Vermont).
2. Los intervalos son muy desiguales y las etiquetas "X+" se superponen (un estado con 600 000 encaja en 100 000+ y 500 000+).

**Cómo corregir:** mapear **casos por 100 000 hab.** con intervalos definidos con lógica (cuantiles o cortes redondos, no traslapados: 0–99, 100–199, 200–299…).

---

### Grupo D. Decoración, 3D y sobrecarga (*chartjunk*)

#### D1. Barras en 3D
**Casos:** 3.23 (frutas por mes), 3.24 (perfil de hipermetilación en cáncer).

**Por qué falla:**
- **Perspectiva:** las barras del fondo se ven más pequeñas y la base de cada una no está alineada con el eje.
- **Oclusión:** las barras delanteras esconden las de atrás (más grave en 3.24, con decenas de filas y columnas).
- Agrega **una dimensión visual sin agregar información**.

**Cómo corregir:** barras 2D agrupadas; si hay dos dimensiones categóricas (tipo de cáncer × gen), un **heatmap** con paleta secuencial es el reemplazo natural.

#### D2. Sobrecarga de codificaciones en un mismo símbolo
**Caso:** 3.25 (caritas con tamaño, forma, expresión y color para 4–5 variables).

**Por qué falla:** cada atributo visual se lee con distinta precisión y el lector no puede "decodificar" cuatro variables simultáneas. La originalidad estética gana; la comprensión pierde.

**Cómo corregir:** **una variable principal por gráfico**; el resto en paneles adicionales (small multiples) o en tooltips (versión interactiva). Regla útil: **máx. 2–3 codificaciones simultáneas** por gráfico.

#### D3. Exceso de números sobre un mapa de calor
**Caso:** 3.9 (mapa NDFD con cientos de valores encima del color).

**Por qué falla:** el color ya comunica el patrón; los números lo tapan.

**Cómo corregir:** mostrar números solo en puntos clave (máximos, mínimos, ciudades relevantes) o dejar el valor exacto para la interacción.

#### D4. Pictogramas de llenado
**Caso:** 3.28 (tazas de café rellenas según %).

**Por qué falla:** el nivel de llenado de una forma irregular no es proporcional al valor (una taza más ancha arriba se "llena" más rápido de lo que sube el %). Nuestro ojo no calcula bien áreas y volúmenes.

**Cómo corregir:** una **barra simple** con la etiqueta; el ícono puede acompañar como adorno pequeño, sin transportar el dato.

---

### Grupo E. Tamaño de símbolos y proporcionalidad

#### E1. Círculos dimensionados por radio en vez de por área
**Caso:** 3.17 (mapa de casos en España).

**Ejemplo numérico:**
- Región A: 100 casos; región B: 400 casos (4 veces más).
- Si el **radio** es proporcional al valor: radio 1 vs. 4 → **área 1 vs. 16** (el círculo B parece 16 veces mayor).
- Correcto: el **área** proporcional al valor → radio ∝ √valor (radio 1 vs. 2).

**Cómo corregir:** `r = k · √valor` (ver el código de la sección 4). Incluir una **leyenda con círculos de referencia** (por ejemplo, 100, 500, 1 000).

---

### Grupo F. Calidad de los datos antes de graficar

#### F1. Datos sin limpiar
**Caso:** 3.22 (Zelda: "BOTW", "Botw", "botw", "Breath of the Wild"… como categorías separadas).

**Por qué falla:** respuestas de texto libre equivalentes se cuentan por separado, fragmentando la información.

**Cómo corregir (proceso previo):**
1. Convertir a minúsculas y quitar espacios/puntuación.
2. Crear una tabla de equivalencias (*BOTW* = *Breath of the Wild*).
3. Agrupar y recontar.
4. Categoría "Otros" para valores <2–3 %.
5. Graficar con **barras ordenadas**.

#### F2. Barras que no coinciden con sus etiquetas
**Caso:** 3.12 (recaudación por candidato; totales y alturas no calzan).

**Aprendizaje general:** antes de publicar, verificar que **la altura de cada barra coincida con el número que dice representar**, que todos los grupos tengan la misma cantidad de períodos y que el eje sea común. Si faltan datos, indicar explícitamente "sin datos".

> **Nota sobre el análisis original:** en los casos 3.1, 3.6 y 3.12 la descripción original era ambigua o especulativa. Aquí se reformuló lo que sí se puede afirmar con seguridad (redundancia, límite perceptual del pie, verificación de consistencia). Revisa siempre el gráfico original antes de concluir que "hay un error".

---

## 4. Recetas prácticas (Python / matplotlib)

### 4.1 Barras siempre desde cero, ordenadas y con etiquetas directas
```python
import matplotlib.pyplot as plt

paises = ["Rusia", "Rep. Checa", "Eslovaquia", "EAU", "Arabia S.", "Egipto"]
ventas = [420, 310, 290, 250, 180, 120]

# Ordenar de mayor a menor
datos = sorted(zip(ventas, paises), reverse=True)
v, p = zip(*datos)

fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(p, v, color="#4C72B0")
ax.invert_yaxis()                  # el mayor arriba
ax.set_xlim(left=0)                # NUNCA truncar la base
for y, val in enumerate(v):
    ax.text(val + 5, y, val, va="center")   # etiqueta directa
ax.set_title("Unidades vendidas por país")
for lado in ["top", "right"]:
    ax.spines[lado].set_visible(False)   # menos "tinta" innecesaria
plt.show()
```

### 4.2 Resaltar una serie y atenuar el resto (en vez de 50 colores)
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
for estado, serie in datos_por_estado.items():
    ax.plot(serie.index, serie.values, color="lightgray", lw=1)
# Destacar solo el/los de interés
for estado in ["Texas", "Nueva York"]:
    s = datos_por_estado[estado]
    ax.plot(s.index, s.values, lw=2.5, label=estado)
    ax.text(s.index[-1], s.values[-1], f" {estado}", va="center")
ax.set_title("Casos acumulados por 100 000 hab.")
```

### 4.3 Small multiples con ejes comunes
```python
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 3, figsize=(10, 5), sharex=True, sharey=True)
for ax, (nombre, serie) in zip(axs.flat, series.items()):
    ax.plot(serie.index, serie.values)
    ax.set_title(nombre, fontsize=10)
```

### 4.4 Círculos proporcionales por área (no por radio)
```python
import numpy as np
import matplotlib.pyplot as plt

casos = np.array([100, 400, 1024])
tamano = 40 * casos            # 's' en scatter = ÁREA en puntos²
plt.scatter(x, y, s=tamano, alpha=0.5)   # ✔ área proporcional al valor
# ✘ Incorrecto: s = (k * casos)**2  → hace el radio proporcional al valor
```

### 4.5 Normalizar antes de mapear
```python
df["casos_100k"] = df["casos"] / df["poblacion"] * 100_000
# Usar 'casos_100k' (no 'casos') para colorear el mapa coroplético
```

---

## 5. Lista de verificación antes de publicar un gráfico

**Propósito**
- [ ] ¿Puedo decir en una frase la pregunta que responde?
- [ ] ¿El título comunica el mensaje ("Las ventas cayeron 12 % en Q3"), no solo el tema ("Ventas")?

**Tipo de gráfico**
- [ ] ¿El tipo de gráfico corresponde a la tarea (ranking, tiempo, distribución…)?
- [ ] Si es pie/dona: ¿las partes son exclusivas y suman 100 %? ¿hay ≤ 5 partes?
- [ ] ¿No hay líneas uniendo categorías sin orden?
- [ ] ¿Evité el 3D?

**Ejes y escalas**
- [ ] ¿Las barras parten de **cero**?
- [ ] ¿Sin eje invertido ni doble eje (o están claramente justificados y rotulados)?
- [ ] ¿Los gráficos que se comparan tienen la misma escala?
- [ ] ¿Ejes con unidades y rótulos claros?

**Color y diseño**
- [ ] ¿≤ 6–8 colores? ¿Un color = un significado?
- [ ] ¿Paleta adecuada (secuencial / divergente / cualitativa)?
- [ ] ¿Se lee bien para personas daltónicas y en escala de grises?
- [ ] ¿Quité rejillas, bordes, sombras y fondos innecesarios?
- [ ] ¿Destaco lo importante y atenúo el resto?

**Datos**
- [ ] ¿Datos limpios y categorías consolidadas?
- [ ] ¿Normalicé (por población, por área, por habitante) cuando comparo regiones?
- [ ] ¿Las etiquetas coinciden con lo que se ve?
- [ ] ¿Cité la fuente y el período?

**Prueba final:** muéstraselo a alguien que no conozca el tema durante 10 segundos. Si no puede decir cuál es el mensaje, rediseña.

---

## 6. Ejercicios con respuestas

**Ejercicio 1.** Un gráfico de barras muestra ventas de 2022 = 520 y 2023 = 540, con el eje Y comenzando en 500. La segunda barra parece 2 veces más alta que la primera. **¿Cuál es el Lie Factor aproximado?**
*Respuesta:* cambio real = 20/520 ≈ 3,8 %. Alturas mostradas: 20 y 40 → +100 %. Lie Factor ≈ 100 / 3,8 ≈ **26**.

**Ejercicio 2.** Una encuesta pregunta "¿qué herramientas usa?" con respuesta múltiple: Excel 80 %, Python 45 %, Tableau 30 %. Un compañero propone un pie. **¿Qué respondes?**
*Respuesta:* los porcentajes suman 155 %; no son partes de un todo. Usa **barras horizontales ordenadas** y aclara "respuesta múltiple".

**Ejercicio 3.** Un mapa de burbujas muestra Madrid (1 024 casos) y Murcia (256 casos). **¿Cómo debe ser la relación de radios?**
*Respuesta:* valores en razón 4:1 → radios en razón √4 : 1 = **2:1**. Si Madrid tiene radio 4 veces mayor, su área es 16 veces mayor: error.

**Ejercicio 4.** Tienes 12 líneas (un país por línea) en un solo gráfico y nadie distingue nada. **Da tres soluciones.**
*Respuesta:* (1) resaltar 1–3 países y el resto en gris; (2) etiquetar directamente las líneas; (3) small multiples con ejes comunes.

**Ejercicio 5.** Detecta **tres** errores posibles: "Gráfico 3D de barras, eje Y desde 90 a 110, colores rojo/verde, dos ejes Y."
*Respuesta:* 3D (distorsión/oclusión), eje truncado (Lie Factor alto), rojo/verde (daltonismo) y doble eje (comparación engañosa).

**Ejercicio 6 (aplicado).** Elige un gráfico de un diario o red social esta semana y complétalo: (a) pregunta que responde, (b) tipo de gráfico y si es adecuado, (c) errores según la lista de la sección 5, (d) versión corregida (boceto).

---

## 7. Glosario mínimo

| Término | Definición |
|---|---|
| **Chartjunk** | Elementos decorativos que no aportan información (Tufte). |
| **Data-ink ratio** | Proporción de la "tinta" del gráfico dedicada a mostrar datos. |
| **Lie Factor** | Efecto mostrado ÷ efecto real. Lo ideal es cercano a 1. |
| **Preatentivo** | Atributo visual que se detecta sin esfuerzo consciente (color, tamaño, posición). |
| **Small multiples** | Serie de gráficos pequeños con la misma escala y estructura, uno por categoría. |
| **Coroplético** | Mapa donde las regiones se colorean según un valor. |
| **Overplotting** | Puntos superpuestos que ocultan la densidad real. |
| **Binning** | Agrupar valores continuos en intervalos (histograma). |

---

## 8. Resumen final

1. **La percepción no es neutral:** contraste simultáneo, textura y asimilación cromática muestran que el contexto altera lo que vemos. Diseña con fondos neutros, contraste alto y etiquetas.
2. **El gráfico se elige por la tarea** (ranking, correlación, distribución, tiempo…), y **por la precisión perceptual**: posición y longitud > ángulo > área > volumen.
3. **Los errores se agrupan en seis familias:** ejes y escalas, tipo de gráfico incorrecto, color, decoración/3D, tamaño de símbolos y calidad de datos.
4. **Reglas de oro:**
   - Barras desde cero.
   - Nunca 3D.
   - Pie solo si son ≤5 partes que suman 100 %.
   - Color con sentido y con moderación.
   - Área (no radio) para círculos.
   - Normaliza antes de comparar regiones.
   - Un gráfico = un mensaje.
5. **Ética:** un gráfico engañoso no siempre es intencional, pero el efecto sobre el lector es el mismo. Verifica siempre antes de publicar.

### Lecturas recomendadas
- Stephen Few, *Show Me the Numbers* (2012).
- Alberto Cairo, *How Charts Lie* (2019).
- Edward Tufte, *The Visual Display of Quantitative Information* (1983).
- Claus Wilke, *Fundamentals of Data Visualization* (2019, gratuito en línea).
- Cole Nussbaumer Knaflic, *Storytelling with Data* (2015).
- Recursos: ColorBrewer (colorbrewer2.org), *Data Viz Project*, *From Data to Viz*.
