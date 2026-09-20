# Visualización de Datos — Errores Comunes y Distracciones

**Curso:** EIN092B - Visualización **Referencia bibliográfica principal:** Stephen Few, _Show Me the Numbers_, 2nd Ed., 2012.

Este documento aborda tres grandes bloques: (1) ejercicios de percepción visual que muestran cómo el cerebro puede "engañarse" al interpretar imágenes, (2) una taxonomía de tipos de gráficos según la tarea analítica que resuelven (clasificación de Stephen Few), y (3) una extensa galería de ejemplos reales de visualizaciones con errores o elementos distractores, que sirven como ejercicio de análisis crítico.

---

## 1. Ejercicios de percepción visual

Antes de hablar de gráficos, la presentación muestra varias **ilusiones ópticas clásicas**. El objetivo es demostrar que la percepción humana del color, el brillo y los patrones **no es un proceso neutro**: el cerebro interpreta la información visual en función del contexto que la rodea, lo cual tiene implicancias directas para el diseño de visualizaciones (un mal uso del color o del contexto visual puede llevar a conclusiones erróneas).

### 1.1 El tablero de ajedrez de Adelson (contraste simultáneo)

Se presenta la clásica ilusión del tablero de ajedrez con un cilindro que proyecta una sombra. La pregunta es: **¿los cuadros A y B son del mismo color?**

- **A simple vista**, el cuadro A (fuera de la sombra) parece mucho más oscuro que el cuadro B (dentro de la sombra).
- **En realidad, ambos cuadros tienen exactamente el mismo valor de gris.**
- Esto se comprueba en la segunda diapositiva, donde se coloca una franja continua de color que conecta ambos cuadros: al eliminar el contexto (la sombra y el patrón de tablero circundante), se observa que el color es idéntico.

Este fenómeno se conoce como **contraste simultáneo**: el cerebro interpreta el brillo de una región no de forma absoluta, sino **relativa a su entorno inmediato**. Como el cuadro B está "dentro de una sombra" (según la interpretación que hace el cerebro de la escena 3D), el sistema visual compensa y lo percibe más claro de lo que realmente es.

**Implicancia para visualización de datos:** el color de un elemento en un gráfico (una barra, una región de un mapa) puede percibirse de forma distinta según los colores que lo rodeen, lo cual puede distorsionar comparaciones si no se diseña con cuidado.

### 1.2 Patrón de textura (ilusión tipo Ouchi/laberinto)

Se muestra una imagen compuesta por un patrón denso de líneas curvas tipo "laberinto" o "huella dactilar", y se pregunta: **¿existe alguna diferencia en el patrón?**

- A primera vista, el patrón parece uniforme en toda la imagen.
- En la siguiente diapositiva se destaca (con líneas azules) una **región sutil donde el patrón cambia de orientación**, algo que resulta muy difícil de detectar sin ayuda visual.

Esto ilustra que el sistema visual humano es **muy sensible a algunos tipos de cambios (como color o brillo) pero relativamente insensible a otros** (como cambios sutiles en la orientación o densidad de una textura), lo que es relevant al elegir qué codificación visual usar para representar una variable (por ejemplo, usar color en lugar de textura para diferencias que deben notarse rápidamente).

### 1.3 Ilusión de color de línea (efecto Bezold / asimilación cromática)

Se muestra una imagen dividida en dos mitades de fondo (amarillo y gris), cada una atravesada por una línea en forma de "X". Se pregunta: **¿es el mismo color de línea?**

- La línea sobre el fondo amarillo parece **más clara/grisácea**, mientras que la misma línea sobre el fondo gris parece **más amarillenta/verdosa**.
- En la diapositiva siguiente se extrae una muestra de la línea de ambos lados y se coloca junto a la imagen, mostrando que **ambas líneas tienen exactamente el mismo color**.

Este efecto se conoce como **asimilación cromática (efecto Bezold)**: el color de fondo "contamina" perceptualmente el color de un elemento que se superpone a él, en dirección opuesta al contraste simultáneo (aquí el color se "mezcla" con el fondo en lugar de destacarse por contraste).

**Conclusión de esta sección:** estas tres ilusiones (contraste simultáneo, insensibilidad a ciertos patrones y asimilación cromática) demuestran que **el color y el contexto visual no son "neutros"** al comunicar datos, y que un diseñador de visualizaciones debe ser consciente de estos efectos perceptuales para evitar generar interpretaciones erróneas, incluso sin intención.

---

## 2. Taxonomía de gráficos según la tarea analítica (Stephen Few)

Basándose en el libro _Show Me the Numbers_ de Stephen Few, el documento organiza los tipos de gráficos según **el tipo de pregunta o relación analítica** que buscan responder, no solo según su forma visual. Esta es una idea central en visualización de datos: **el tipo de gráfico debe elegirse en función de la tarea**, no al revés.

### 2.1 Clasificación (Ranking)

Cuando el objetivo es **ordenar categorías** según una magnitud (por ejemplo, ventas por país), se recomienda el uso de **gráficos de barras**, ya sea verticales u horizontales. El ejemplo muestra unidades vendidas por país (Rusia, República Checa, Eslovaquia, Emiratos Árabes Unidos, Arabia Saudita, Egipto), ordenadas de mayor a menor, tanto en formato de barras verticales como horizontales.

### 2.2 Comparación nominal

Cuando las categorías **no tienen un orden inherente** (por ejemplo, regiones geográficas: Norte, Sur, Este, Oeste), también se recomienda el uso de **barras**, pero a diferencia del ranking, aquí el orden de las categorías es arbitrario (se puede alfabetizar, ordenar por magnitud, o mantener un orden lógico como geográfico).

### 2.3 Correlación

Para mostrar la **relación entre dos variables numéricas** (por ejemplo, altura vs. salario de empleados), se recomienda:

- **Diagramas de dispersión (scatter plots)**, con puntos individuales y opcionalmente una **línea de tendencia** que resuma la relación.
- Alternativamente, se puede usar un gráfico de **barras enfrentadas** (back-to-back bars) que compara ambas variables lado a lado para cada individuo, aunque es menos efectivo que el scatter plot para detectar correlación.

### 2.4 Desviación

Cuando se quiere mostrar **cuánto se desvía un valor respecto de un punto de referencia** (por ejemplo, ventas reales vs. plan, o variación porcentual mes a mes), se pueden usar:

- **Barras** que se extienden hacia arriba o hacia abajo desde una línea base de cero (ej. "Actual to Plan Variance", con barras rojas para valores por encima del plan y grises para valores por debajo).
- **Líneas**, útiles para mostrar variación porcentual en el tiempo respecto a un valor de referencia (ej. cambio porcentual mes a mes respecto al mes anterior).
- **Puntos y líneas**, para comparar cada mes contra un valor fijo de referencia (ej. ventas mensuales comparadas con enero).

### 2.5 Distribución

Para mostrar cómo se **distribuyen los valores** de una variable, existen varias sub-categorías:

**a) Distribución única o de frecuencia:**

- **Histograma:** usa barras para mostrar la frecuencia de ocurrencia agrupada en intervalos (bins).
- **Polígono de frecuencia:** usa una línea que conecta los puntos medios de cada intervalo, en lugar de barras. Es útil para comparar múltiples distribuciones superpuestas, ya que las líneas se superponen mejor visualmente que las barras.

**b) Distribución múltiple (rango de valores a través de categorías o tiempo):**

- **Rango con barras:** cada barra representa el rango entre un valor mínimo y máximo (ej. rango salarial por año).
- **Rango con barras y puntos:** se añade un punto (por ejemplo, la mediana) dentro de cada barra de rango.
- **Rango con barras y líneas:** se añade una línea que conecta las medianas a través de las categorías, permitiendo ver la tendencia de la mediana además del rango.

**c) Box plot (gráfico de cajas):** Es una forma más completa y estandarizada de representar una distribución, mostrando:

- El **valor mínimo y máximo** (extremos de los "bigotes").
- El **rango intercuartílico (percentil 25 a percentil 75)**, representado por la caja, que contiene el 50% central de los valores ("midspread").
- La **mediana** (percentil 50), marcada dentro de la caja.

Este tipo de gráfico permite ver de un vistazo tanto la tendencia central como la dispersión y posibles asimetrías de los datos.

### 2.6 Geoespacial

Cuando los datos tienen una componente geográfica, existen distintas formas de representarlos:

- **Mapa de símbolos proporcionales:** usa puntos de distinto tamaño ubicados en su posición geográfica, donde el tamaño del símbolo representa la magnitud de una variable (ej. ventas por ciudad).
- **Mapa relleno (choropleth):** colorea regiones completas (países, estados) según el valor de una variable, usando una escala de color o intensidad.
- **Mapa de flujo:** usa líneas (a menudo con grosor variable) para representar movimiento o flujo entre ubicaciones geográficas (ej. trayectorias de tormentas).

### 2.7 Visualización "Parte a todo" (Part-to-whole)

Este tipo de gráfico se usa para **comparar la composición de un todo**, es decir, cómo las partes contribuyen al total, ya sea en un momento dado o a través de distintas categorías/tiempo. Ejemplos mencionados: **donut chart, marimekko chart, pie chart y stacked bar graph (barras apiladas)**.

Se muestran ejemplos con datos de ventas por región (Norte, Sur, Este, Oeste):

- **Barras simples**, mostrando el porcentaje que cada región aporta al total de ventas — útil para comparar magnitudes individuales pero no comunica directamente la idea de "parte de un todo".
- **Barras apiladas (stacked bars)**, que sí comunican directamente cómo las partes se combinan para formar el 100% del total, y permiten además comparar esa composición a través del tiempo (por trimestre, Q1-Q4).
- También se contrastan barras apiladas versus **barras agrupadas (clustered bars)**: las apiladas muestran la composición del total, mientras que las agrupadas facilitan comparar cada categoría individualmente entre trimestres, pero pierden la noción de "total".

### 2.8 Series de tiempo

Para mostrar la **evolución de una variable a través del tiempo**, se presentan tres alternativas equivalentes con los mismos datos de ventas mensuales:

- **Líneas:** conecta los valores mes a mes, siendo la forma más común y efectiva de mostrar tendencia temporal.
- **Líneas y puntos:** añade marcadores en cada punto de dato sobre la línea, útil cuando se quiere resaltar valores individuales además de la tendencia general.
- **Barras:** cada mes se representa como una barra independiente; es una alternativa válida, aunque generalmente las líneas comunican mejor la idea de tendencia continua que las barras.

---

## 3. Ejercicio: errores y distracciones en visualizaciones reales

La última y más extensa sección del documento presenta una **galería de más de 25 visualizaciones reales** (extraídas de medios de noticias, encuestas, estudios y redes sociales) con la consigna: _"¿Existe algún error o distracción en las siguientes visualizaciones?"_. A continuación se describe cada ejemplo y el problema de diseño que ilustra.

### 3.1 Gráficos de dona "GENDER" (86% Male / 14% Female)

Dos gráficos de dona de distinto tamaño representan 86% y 14%. **Problema:** aunque cada gráfico dona muestra correctamente su propio porcentaje mediante el arco relleno, el **tamaño físico de los dos círculos es idéntico**, cuando en realidad, al representar magnitudes tan distintas, podría (o no) esperarse una diferenciación visual adicional; además, comparar dos "donas" separadas dificulta la comparación directa entre ambos valores, en contraste con lo sencillo que sería un solo gráfico de barras o una sola dona con dos segmentos.

### 3.2 "How couples met 1995-2017" (gráfico de líneas)

Gráfico de líneas comparando cómo se conocieron las parejas en 1995 vs. 2017, para distintas categorías (trabajo, bar/restaurante, en línea, colegio, familia, amigos). **Problema:** las categorías del eje X no tienen un orden lógico claro (no están ordenadas ni alfabéticamente ni por magnitud), y al usar líneas para conectar categorías que son **nominales** (sin relación de orden o continuidad entre sí, como "Bar/restaurante" y "Online"), se sugiere visualmente una tendencia o progresión que no existe realmente entre esas categorías. Este es un caso clásico de mal uso de gráfico de líneas para datos categóricos nominales, que deberían representarse con barras.

### 3.3 Gráfico circular "shortage of vehicles for conveying inmates" (Nigeria)

Un pie chart dividido en cuatro secciones aparentemente iguales, etiquetadas 2016, 2017, 2018 y 2019, acompañando un texto sobre escasez de vehículos. **Problema:** el gráfico circular no representa ninguna magnitud real asociada a cada año (no hay valores numéricos visibles ni relación clara entre el tamaño de cada "porción" y algún dato); las cuatro porciones parecen artificialmente iguales (25% cada una), lo cual sugiere que el gráfico fue usado solo como elemento decorativo sin comunicar información cuantitativa real. Es un ejemplo de **chartjunk**: un gráfico que ocupa espacio pero no aporta valor informativo genuino.

### 3.4 "Clinical phase trends, 2007-22" (barras agrupadas por año)

Gráfico de barras agrupadas mostrando el número de fármacos en cada fase clínica (I, II, III), con una barra por cada año entre 2007 y 2022 (16 colores distintos). **Problema:** usar **16 colores diferentes** para distinguir los años hace prácticamente imposible identificar qué color corresponde a qué año sin consultar constantemente la leyenda; además, dentro de cada fase, las barras ya están ordenadas cronológicamente, por lo que el color es redundante con la posición y solo añade complejidad visual innecesaria (demasiadas categorías para una codificación por color, que idealmente debería limitarse a unas 6-8 categorías distinguibles).

### 3.5 "Case numbers rising" / "Daily deaths remain stable" (BBC, COVID-19)

Dos gráficos de área/línea del Reino Unido, uno de casos diarios y otro de muertes diarias, colocados uno al lado del otro. **Problema:** aunque cada gráfico individualmente está bien construido, **usan escalas verticales completamente distintas** (0-100,000 para casos vs. 0-1,750 para muertes) sin un eje compartido o normalización, lo que puede llevar a una comparación visual engañosa entre "forma" de ambas curvas si el lector no presta atención cuidadosa a los ejes; el titular "Daily deaths remain stable" puede sugerir una desconexión entre el aumento de casos y las muertes, cuando en realidad podría deberse simplemente a un desfase temporal natural entre contagio y fallecimiento, no mencionado explícitamente.

### 3.6 "Do you support or oppose building a wall" (Quinnipiac Poll)

Gráfico circular con tres porciones: 45% Support, 51% Oppose, 4% Don't know/NA. **Problema:** aunque en este caso particular los porcentajes sí suman 100% (45+51+4=100), el ángulo visual de cada segmento no siempre corresponde exactamente a la proporción esperada, un error común en pie charts hechos "a mano" o con herramientas de diseño gráfico en lugar de software de visualización de datos, donde los ángulos pueden dibujarse de forma aproximada y no proporcional exacta a los datos reales.

### 3.7 "Life expectancy at birth" (mapa de EE.UU. por estado)

Mapa coroplético de EE.UU. con 4 categorías de color representando rangos de esperanza de vida. **Problema:** el rango de colores (verde oscuro, verde claro, azul oscuro, morado claro) no sigue una escala secuencial intuitiva (por ejemplo, de claro a oscuro para indicar de menor a mayor), sino que combina dos gamas de color distintas (verdes y azules/morados) para representar una variable que es en realidad continua y ordinal, lo cual puede dificultar la interpretación rápida de qué colores representan valores más altos o más bajos.

### 3.8 Mapa MSNBC "38,227,970 CONFIRMED CASES"

Mapa de EE.UU. coloreado por rangos de casos COVID-19 (1,000+, 100,000+, 500,000+, 1,000,000+ casos). **Problema:** los rangos de la leyenda **no son mutuamente excluyentes ni proporcionales al tamaño de cada estado**: un estado pequeño con 100,000 casos y uno grande con 100,000 casos se pintan igual, sin normalizar por población; además, los rangos usan intervalos muy desiguales (1,000 a 100,000, luego 100,000 a 500,000, etc.), lo que distorsiona la interpretación visual de la gravedad relativa entre estados.

### 3.9 Mapa de temperatura NDFD (2.5 km, julio 2022)

Mapa meteorológico con **cientos de números superpuestos** sobre un mapa de calor de temperatura. **Problema:** el exceso de etiquetas numéricas satura visualmente el mapa, dificultando distinguir el patrón general de temperatura que ya está codificado por color; es un ejemplo de **sobrecarga de información (chartjunk / exceso de precisión)**, donde añadir demasiado detalle numérico compite con, en lugar de complementar, la codificación visual principal (el color).

### 3.10 "Major and Violent Crime Has Increased" (NYC, barras 2017-2021)

Gráfico de barras del alcalde de NYC mostrando delitos graves por año, donde el eje Y comienza en 94,000 en lugar de 0. **Problema clásico y muy citado:** al **truncar el eje Y** (no partir desde cero), una diferencia relativamente pequeña en términos porcentuales (7.5% más delitos que en 2020, según el propio gráfico) se representa visualmente como un salto dramático y desproporcionado en la altura de la última barra, exagerando la magnitud real del cambio. Este es uno de los errores más comunes y potencialmente más engañosos en visualización de datos con barras.

### 3.11 "Forecast Wind Gusts" (pronóstico del tiempo, barras)

Gráfico de barras de un pronóstico meteorológico mostrando ráfagas de viento por hora (27, 26, 26, 25, 25, 26, 27 mph). **Problema:** de forma similar al ejemplo anterior, el eje Y parece no partir de cero (las barras para valores muy similares, como 25 y 27, muestran diferencias de altura desproporcionadamente grandes en relación con la diferencia real de solo 2 mph), lo cual exagera visualmente variaciones que en términos absolutos son mínimas.

### 3.12 "BERNIE SANDERS... $34.5M" (gráfico de barras, candidatos demócratas)

Gráfico de barras trimestrales de fondos recaudados por distintos candidatos, con el monto total superpuesto como etiqueta. **Problema:** las **alturas de las barras no corresponden de forma consistente con los valores etiquetados**: por ejemplo, Warren aparece con $24.6M pero sus barras visibles parecen más bajas que las de Buttigieg con $24.8M, sugiriendo que la escala del eje Y no es consistente entre candidatos, o que faltan datos/barras para completar la comparación (a Warren le falta al menos una barra visible respecto a los otros tres candidatos), generando una comparación visual poco fiable.

### 3.13 "VOTERS TRUST TRUMP OVER CLINTON" (gráfico circular 50%/35%)

Gráfico circular dividido en dos mitades exactas (aparentemente 50/50 visualmente) pero etiquetado como 50% Trump y 35% Clinton. **Problema evidente:** **50% + 35% = 85%**, no 100%; sin embargo, el círculo está dividido visualmente en dos mitades iguales, lo que sugiere gráficamente una proporción de 50/50, contradiciendo los números reales indicados. Esto **exagera visualmente la ventaja de un candidato sobre otro**, ya que el 35% debería ocupar una porción visualmente mucho menor que la mitad del círculo. Es un caso flagrante de manipulación (intencional o no) mediante gráfico circular.

### 3.14 "BIGGEST FUTURE CHANGES IN THE WORKPLACE" (gráfico tipo pie con 73%, 69%, 46%)

Gráfico en forma de pie/dona dividido en tres segmentos etiquetados 73%, 69% y 46%. **Problema:** al sumar los tres porcentajes (73+69+46 = 188%), es evidente que **no representan partes de un mismo todo**, sino resultados de **preguntas independientes de una encuesta** donde los encuestados podían elegir múltiples opciones. Usar un gráfico circular (que visualmente implica "partes de un 100%") para datos que en realidad son porcentajes independientes de respuestas múltiples es un uso incorrecto del tipo de gráfico, que debería haberse representado con barras independientes.

### 3.15 "L'Outaouais championne de l'anglais au travail" (pie chart con 69%, 38%, 35%, 32%, 31%)

Similar al caso anterior: un gráfico circular con cinco regiones y sus respectivos porcentajes de trabajadores que usan principalmente inglés. **Problema:** la suma de los porcentajes (69+38+35+32+31 = 205%) confirma que estos valores corresponden a **proporciones independientes por región** (cada región analizada por separado), no a partes de un total combinado, por lo que un gráfico circular es completamente inapropiado — de nuevo, se necesitarían barras independientes por región.

### 3.16 "PERCENTAGE OF CORN PLANTED IN OHIO" (cuatro gráficos circulares por semana)

Cuatro pie charts que muestran el avance de siembra de maíz (4%, 9%, 22%, 33%) comparado con un promedio de 5 años (47%, 62%, 78%, 90%). **Problema:** cada gráfico circular representa un **porcentaje de avance como si fuera un "todo" de 100%**, pero en realidad se trata de una progresión temporal (una sola variable que avanza semana a semana) mejor representada con un gráfico de líneas o de barras que muestre la evolución en el tiempo y la comparación directa año actual vs. promedio histórico en un solo gráfico, en lugar de fragmentar la información en cuatro gráficos circulares separados y de difícil comparación visual conjunta.

### 3.17 "CASOS DE CORONAVIRUS COVID-19 EN ESPAÑA" (mapa con círculos proporcionales)

Mapa de España con círculos de distinto tamaño por comunidad autónoma, representando número de casos. **Problema:** es común en este tipo de mapas que el tamaño del círculo se calcule proporcional al **radio** en lugar de al **área** del círculo; como el área de un círculo crece con el cuadrado del radio, esto **exagera visualmente las diferencias** entre regiones con muchos y pocos casos (Madrid con 1024 casos parece desproporcionadamente más grande en relación a otras regiones de lo que correspondería si el área fuese realmente proporcional al valor).

### 3.18 "How long can Coronavirus last on different surfaces" (Economic Times, dos gráficos de barras)

Dos gráficos de barras horizontales con distintas escalas de eje X (0-25 para el primero, 0-20 para el segundo), agrupando superficies distintas. **Problema:** al usar **dos escalas diferentes** para dos conjuntos de barras que en el diseño aparecen visualmente similares (incluso podrían percibirse como parte de un mismo conjunto comparativo), existe riesgo de que el lector compare visualmente longitudes de barras entre ambos grupos sin notar que las escalas del eje X son distintas, lo cual llevaría a conclusiones erróneas sobre la duración relativa del virus en distintas superficies.

### 3.19 "CUMULATIVE CASES PER 100,000: ALL STATES" (gráfico de líneas, EE.UU.)

Gráfico de líneas con aproximadamente 45-50 líneas de distinto color, una por cada estado de EE.UU. **Problema:** el número de series (colores) es demasiado alto para que una leyenda de color pueda ser útil; es prácticamente imposible distinguir qué línea corresponde a qué estado sin pasar el cursor sobre cada una (en una versión interactiva) o sin usar técnicas alternativas como **etiquetado directo de las líneas más relevantes**, resaltado selectivo (highlighting) de una o pocas series de interés, o **pequeños múltiplos** (small multiples) en lugar de superponer todas las series en un solo gráfico.

### 3.20 Leyenda "Category" con colores mal asignados (Null, Green, Orange, Red, Yellow)

Una leyenda donde el ítem "Null" está coloreado en naranja, mientras que el ítem "Orange" está coloreado en un tono verde-azulado (teal), y el ítem "Green" está coloreado en rojo. **Problema evidente:** existe una **discordancia entre el nombre de la categoría y el color asignado a ella** — el color "Orange" no es naranja, y el color "Green" no es verde — lo cual genera confusión inmediata y contradice las expectativas naturales del lector sobre qué color debería representar cada etiqueta con nombre de color.

### 3.21 "Top 10 Fruits as Percentage of Total Fruit Ads" (pie chart)

Gráfico circular con 10 categorías de frutas (manzanas, aguacates, arándanos, uvas, mangos, etc.), cada una con un color asignado arbitrariamente. **Problema:** similar al ejemplo anterior, los colores no corresponden de forma intuitiva a las frutas que representan (por ejemplo, "Oranges" — naranjas — no está representado con color naranja, sino con verde lima), lo que desaprovecha una oportunidad natural de hacer la visualización más intuitiva mediante una codificación de color coherente con el significado de las categorías.

### 3.22 "Which game(s) have you played the most?" (encuesta Zelda, pie chart con ~30 categorías)

Un gráfico circular con aproximadamente 30 porciones diminutas, la mayoría correspondientes a variantes de escritura de la misma respuesta ("BOTW", "Botw", "botw", "Breath of the Wild", "Breath of The Wild", "Zelda: BOTW", etc.). **Problema doble:** (1) hay un claro problema de **limpieza de datos** previo a la visualización, ya que respuestas de texto libre equivalentes no fueron normalizadas/agrupadas antes de graficar, generando decenas de categorías redundantes; y (2) un pie chart con tantas categorías (muchas de ellas minúsculas) es completamente inadecuado, ya que resulta imposible distinguir o comparar visualmente porciones tan pequeñas — un gráfico de barras ordenado, junto con la limpieza previa de los datos, sería muchísimo más efectivo.

### 3.23 Gráfico de barras 3D de frutas por mes (Jan-Apr, Lemons/Oranges/Bananas/Apples)

Gráfico de barras en **perspectiva 3D**, con cuatro grupos de frutas por cada mes. **Problema clásico:** los gráficos de barras en 3D introducen **distorsión de perspectiva**: las barras en el fondo pueden parecer más pequeñas de lo que realmente son debido al efecto de profundidad, y resulta difícil leer con precisión el valor exacto de cada barra contra el eje Y, ya que la posición de la base de cada barra varía según su profundidad aparente en la escena 3D. El 3D en gráficos de barras casi nunca aporta información adicional real y sí introduce ambigüedad en la lectura de los valores.

### 3.24 "A CpG Island Hypermethylation Profile of Human Cancer" (gráfico de barras 3D, muy denso)

Un gráfico de barras 3D extremadamente denso, con decenas de tipos de cáncer en un eje y decenas de genes en otro eje, generando un "bosque" de barras de distintas alturas y colores. **Problema:** además de la distorsión de perspectiva propia de los gráficos 3D (mencionada en el ejemplo anterior), aquí se suma una **sobrecarga extrema de información**: con tantas barras superpuestas, muchas quedan **ocultas detrás de otras** (oclusión), haciendo imposible leer con precisión la mayoría de los valores individuales del gráfico.

### 3.25 "DEATH PENALTY EXECUTIONS SINCE 1976" (mapa con emoticonos/caritas)

Mapa de EE.UU. donde cada estado contiene un ícono de cara (sonriente, neutral, triste) cuyo tamaño, expresión y color codifican simultáneamente múltiples variables (proporción racial, edad promedio, número de ejecuciones, método utilizado). **Problema:** este es un ejemplo extremo de **sobrecarga de codificación visual**: se intentan comunicar hasta 4-5 variables distintas simultáneamente a través de un solo ícono (tamaño del óvalo, expresión facial, color de la cara, símbolo interno), lo que hace prácticamente imposible extraer información precisa y comparable de un vistazo. Es un ejemplo de **chartjunk** elaborado, donde el diseño prioriza la originalidad estética sobre la claridad y precisión analítica.

### 3.26 "Gun deaths in Florida" (Reuters, eje Y invertido)

Gráfico de área/línea sobre muertes por armas de fuego en Florida, donde el **eje Y está invertido** (0 arriba, 1000 abajo), de modo que la línea "sube" visualmente cuando el número de muertes en realidad **disminuye**. **Problema muy sutil y peligroso:** invertir el eje Y sin una razón clara y sin una advertencia explícita al lector puede provocar una interpretación exactamente opuesta a la realidad: en este gráfico, una caída real en los homicidios con armas (873 a 721) se percibe visualmente como una "elevación" o mejora dramática de la línea, cuando la lectura correcta requiere que el lector primero entienda que el eje está invertido — algo que muchos lectores no notarán a primera vista.

### 3.27 "Covid19 fatality rates per age group" (Suecia, doble eje Y)

Gráfico de barras con **dos ejes Y distintos**: uno para el grupo etario 0-69 años (escala 0% a 1.25%) en color negro, y otro para el grupo 70+ años (escala 0% a 40%) en color celeste. **Problema:** usar dos escalas completamente distintas en el mismo gráfico para comparar grupos etarios **distorsiona la comparación visual real** entre ambos grupos: la barra negra del grupo 60-69 parece casi tan alta como las barras celestes de 70+, cuando en términos de magnitud real la tasa de fatalidad del grupo de mayores es muchísimo más alta (hasta 30 veces mayor). Este es un ejemplo clásico de cómo el **doble eje Y** puede ser usado (intencionalmente o no) para minimizar visualmente diferencias que en realidad son muy grandes.

### 3.28 "Consumption of espresso-based drinks" (infografía con tazas)

Infografía donde el nivel de llenado de cada ícono de taza representa el porcentaje de consumo de cada tipo de bebida (Cappuccino 33%, Latte 33%, Cold Brew 28%, etc.). **Problema:** codificar un porcentaje mediante el **nivel de llenado de un ícono con forma irregular** (una taza) es una forma de codificación visual poco precisa: a diferencia de una barra simple (que tiene una relación lineal directa entre longitud y valor), el volumen o área "llenada" dentro de la forma de una taza no necesariamente corresponde de forma lineal y exacta al porcentaje indicado, dificultando la comparación precisa entre bebidas (por ejemplo, comparar visualmente 18% de Macchiato vs. 18% de Americano, cuyas tazas tienen formas distintas).

---

## Resumen general del documento

Este material recorre tres niveles complementarios del análisis crítico de visualizaciones de datos:

1. **Percepción visual:** mediante ilusiones ópticas clásicas (contraste simultáneo, insensibilidad a ciertos patrones, asimilación cromática), se demuestra que el color y el contexto visual afectan la interpretación de una imagen de forma no siempre consciente ni controlable por el espectador, lo cual obliga a un diseñador de datos a ser especialmente cuidadoso con el uso del color y el contexto.
    
2. **Taxonomía de gráficos según tarea analítica (Stephen Few):** se presenta un marco de referencia para elegir el tipo de gráfico correcto según la pregunta que se busca responder — clasificación/ranking, comparación nominal, correlación, desviación, distribución (única, múltiple, box plot), geoespacial, parte a todo, y series de tiempo — enfatizando que la elección del gráfico debe basarse en la naturaleza de los datos y la pregunta analítica, no en preferencias estéticas.
    
3. **Galería de errores comunes en visualizaciones reales:** una revisión extensa de casos reales (medios de noticias, encuestas, estudios científicos, redes sociales) que ilustra los errores más frecuentes en la práctica, entre ellos: **ejes truncados o invertidos**, **uso de gráficos circulares para datos que no suman 100% o que no son partes de un todo**, **exceso de categorías o colores que saturan la leyenda**, **codificación de color incoherente con el significado de las categorías**, **gráficos 3D que distorsionan la percepción de magnitud**, **doble eje Y que distorsiona comparaciones entre series**, **datos sin limpiar que generan categorías redundantes**, **símbolos con tamaño no proporcional al área real**, y **sobrecarga de codificación visual (chartjunk)**.
    

En conjunto, el documento busca desarrollar una mirada crítica para **identificar y evitar** estos errores comunes, tanto al momento de crear visualizaciones propias como al momento de interpretar visualizaciones ajenas encontradas en medios, informes o redes sociales.