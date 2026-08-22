# Análisis Detallado: Librería de Mapas — Introducción a los Datos Geoespaciales en Python

## Contexto general del notebook

Este notebook pertenece al curso **EIN092B Visualización 2024** y tiene como objetivo enseñar a **visualizar y manipular datos geoespaciales en Python**, usando tres bibliotecas principales:

- **GeoPandas**: extensión de pandas para trabajar con datos geográficos (polígonos, líneas, puntos).
- **Folium** (a través del método `.explore()`): permite crear mapas interactivos basados en Leaflet.js.
- **MapClassify**: biblioteca usada internamente por GeoPandas para clasificar datos numéricos en mapas coropléticos (aunque en este notebook no se usa explícitamente en profundidad, es la que habilita ciertos esquemas de color/clasificación).

A lo largo del notebook se trabaja con tres tipos de datos geométricos distintos: **polígonos** (países, distritos), **puntos** (ciudades) y **líneas** (ríos). Esto es intencional: es la forma clásica de introducir los tres tipos fundamentales de geometría en un Sistema de Información Geográfica (SIG).

A continuación se explica **cada celda, cada concepto y el porqué de cada decisión técnica**, en el mismo orden en que aparecen en el notebook.

---

## 1. Importación de librerías

```python
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import geopandas as gpd
```

**¿Por qué estas librerías?**

- `pandas` (`pd`): es la base de todo el análisis de datos tabular en Python. GeoPandas está construido *encima* de pandas, así que todo lo que se sabe de pandas (filtrado, `.head()`, `.mean()`, etc.) sigue funcionando.
- `numpy` (`np`): biblioteca de cálculo numérico. Aunque en este notebook no se usa de forma explícita mucho, suele acompañar cualquier análisis de datos porque pandas se apoya en ella internamente.
- `random`: módulo estándar de Python para generación de números aleatorios (no se explota a fondo en este notebook, probablemente quedó como utilidad general).
- `matplotlib.pyplot` (`plt`): la librería de graficación más usada en Python. GeoPandas usa matplotlib "por debajo" cuando llamamos a `.plot()`.
- `geopandas` (`gpd`): es la librería central del notebook. Extiende los `DataFrame` de pandas para que puedan almacenar y operar con geometrías (puntos, líneas, polígonos).

**Idea clave:** GeoPandas no reinventa la rueda. Reutiliza pandas para la parte tabular y matplotlib para la parte gráfica, y les añade una capa geoespacial. Esto es muy importante entenderlo porque significa que **todo el conocimiento previo de pandas es directamente aplicable** a un `GeoDataFrame`.

---

## 2. Importar datos geoespaciales

### El problema de los formatos SIG

Los datos geoespaciales no vienen en CSV normalmente. Vienen en formatos especializados porque necesitan almacenar, además de los datos "de tabla" (nombre del país, población, etc.), la **geometría** (forma exacta del país, calculada con coordenadas). Los formatos más comunes son:

- **Shapefile (.shp)**: formato desarrollado por ESRI, es en realidad un conjunto de varios archivos (`.shp`, `.shx`, `.dbf`, `.prj`, etc.) que juntos describen la geometría y los atributos.
- **GeoJSON (.geojson)**: formato basado en JSON, más liviano y legible por humanos, muy usado en la web.
- **GeoPackage**: formato basado en SQLite, pensado para reemplazar al shapefile con más flexibilidad.
- **PostGIS**: extensión espacial de PostgreSQL (una base de datos), usada cuando los volúmenes de datos son grandes o se necesita consultas SQL espaciales.

### La función clave: `geopandas.read_file()`

```python
countries = gpd.read_file(r"C:\Users\jorge\Downloads\ne_110m_admin_0_countries.zip")
countries = countries[['ADM0_A3', 'SOVEREIGNT', 'CONTINENT', 'POP_EST', 'GDP_MD', 'geometry']]
print(countries.head())
```

**¿Qué hace esta función?** `read_file()` es una función "inteligente": detecta automáticamente el formato del archivo (shapefile, GeoJSON, GeoPackage, etc.) y lo carga en un `GeoDataFrame`. Aquí se lee un archivo `.zip` que contiene un shapefile comprimido — GeoPandas puede leer directamente el zip sin necesidad de descomprimirlo manualmente, lo cual es una comodidad práctica.

**Los datos:** provienen de *Natural Earth* (naturalearthdata.com), una fuente pública y gratuita muy usada en cartografía porque ofrece datos del mundo a distintos niveles de detalle (110m, 50m, 10m — donde el número indica la escala de generalización, es decir, qué tan simplificadas están las geometrías; 110m es la versión más "gruesa"/simplificada, ideal para mapas del mundo completo donde no se necesita precisión de calle).

**Selección de columnas:** se seleccionan solo 6 de las muchas columnas que trae el shapefile original, porque los shapefiles de Natural Earth suelen traer decenas de atributos (códigos alternativos, nombres en otros idiomas, etc.) que no son necesarios para este ejercicio. Es una buena práctica quedarse solo con lo relevante:

| Columna | Significado |
|---|---|
| `ADM0_A3` | Código ISO Alpha-3 del país (ej: "CHL" para Chile, "ARG" para Argentina) |
| `SOVEREIGNT` | Nombre del país o estado soberano |
| `CONTINENT` | Continente al que pertenece |
| `POP_EST` | Población estimada |
| `GDP_MD` | PIB estimado, en millones de dólares |
| `geometry` | La forma geométrica del país (polígono) |

**¿Por qué `.head()` funciona igual que en pandas?** Porque, como se dijo antes, un `GeoDataFrame` **es** un `DataFrame` de pandas con una columna especial (`geometry`) y métodos adicionales. `.head()` no es un método geoespacial, es puro pandas, y funciona exactamente igual.

---

## 3. El Sistema de Coordenadas de Referencia (CRS)

```python
countries.crs
```

Este es uno de los **conceptos más importantes** de toda la geoinformática, y por eso el notebook le dedica tiempo.

### ¿Qué es un CRS?

Un **CRS (Coordinate Reference System)** es la "regla" que define cómo un par de números (por ejemplo, `-70.65, -33.45`) se traduce a una ubicación real sobre la superficie de la Tierra. La Tierra no es plana ni perfectamente esférica (es un geoide, una forma irregular achatada en los polos), así que existen múltiples formas matemáticas de "aplanarla" o representarla en coordenadas, y cada una tiene distintos usos, ventajas y distorsiones.

Sin un CRS, un conjunto de puntos como `(-70.6, -33.4)` no significa nada por sí solo: podría ser (longitud, latitud) en grados, o podría ser una coordenada en metros dentro de un sistema de proyección específico. El CRS le da **contexto e interpretación** a las coordenadas.

### `.crs` como atributo de consulta

`countries.crs` simplemente devuelve cuál es el CRS actual del `GeoDataFrame`, sin modificarlo. Es una forma de "preguntarle" al objeto en qué sistema de coordenadas están sus geometrías.

### `to_crs()`: reproyección

```python
countries = countries.to_crs(epsg=3857)
```

`to_crs()` **reproyecta** las geometrías: recalcula matemáticamente todas las coordenadas para expresarlas en un sistema de referencia distinto. Esto es distinto de simplemente "cambiar una etiqueta" — implica una transformación matemática real de cada punto de cada geometría.

**¿Por qué es necesario reproyectar?**

El notebook explica dos razones fundamentales:

1. **Cálculos precisos de distancia y área**: el CRS más común para almacenar datos geográficos es **EPSG:4326** (coordenadas en grados de latitud/longitud, el estándar GPS/WGS84). El problema es que un grado de longitud **no mide lo mismo en metros** dependiendo de en qué latitud estés (cerca del ecuador un grado de longitud son ~111 km, cerca de los polos son casi 0 km, porque los meridianos convergen). Esto significa que si calculas un área directamente sobre coordenadas en grados, el resultado **no tiene sentido físico real** (no está en una unidad interpretable como km² o m²). Por eso, antes de calcular áreas, se reproyecta a un sistema cuya unidad sea el **metro**.

2. **Representación visual correcta**: distintos mapas web (Google Maps, OpenStreetMap) usan una proyección estándar para mostrar el mundo, y a veces se necesita que los datos coincidan con esa proyección.

### Los códigos EPSG

**EPSG** significa *European Petroleum Survey Group*, la organización que originalmente creó y mantiene un catálogo estandarizado de sistemas de referencia espacial, cada uno identificado por un número único. Hoy este catálogo lo mantiene el **IOGP** (International Association of Oil & Gas Producers), pero el nombre "EPSG" se sigue usando como estándar de facto en toda la industria SIG.

Los dos códigos que aparecen en el notebook:

- **EPSG:4326 (WGS84)**: sistema de coordenadas geográficas en grados (latitud, longitud). Es el que usa el GPS. Es el CRS "por defecto" en el que suelen venir los datos crudos, pero **no es apto para medir distancias o áreas** directamente, porque sus unidades son grados angulares, no una unidad lineal.

- **EPSG:3857 (Web Mercator)**: proyección usada por casi todos los mapas web (Google Maps, OpenStreetMap, Mapbox). Sus unidades son **metros**, lo que la hace útil para cálculos de área/distancia aproximados a escala global, aunque distorsiona mucho las áreas cerca de los polos (por eso Groenlandia se ve "gigante" en Google Maps comparada con su tamaño real).

- **EPSG:3035** (mencionado más adelante, para los datos de París): es la proyección **ETRS89 / LAEA Europe**, diseñada específicamente para Europa. Es una proyección de **área equivalente** (Equal-Area), lo que significa que preserva las proporciones de área real — ideal precisamente para comparar el tamaño de distritos parisinos entre sí, que es justo lo que se hace en el ejercicio final.

**Lección conceptual importante:** no existe una proyección "perfecta" que preserve todo (forma, área, distancia, dirección) al mismo tiempo — es matemáticamente imposible aplanar una esfera sin distorsión (esto se conoce como el problema de la **proyección cartográfica**). Por eso se elige la proyección según el uso: Web Mercator para visualización web, proyecciones de área equivalente para comparar tamaños, proyecciones locales/UTM para mediciones precisas en una región pequeña.

---

## 4. Visualización básica: `.plot()` vs `.explore()`

```python
countries.plot()
countries.explore()
```

El notebook presenta **dos formas de visualizar** un `GeoDataFrame`, y es clave entender la diferencia:

### `.plot()` — Matplotlib (estático)

- Genera una imagen **estática** (no interactiva) usando matplotlib "por debajo".
- Es rápido, ligero, y perfecto para explorar los datos mientras se programa, o para generar figuras que van a un informe/paper.
- No permite hacer zoom, mover el mapa, ni hacer clic sobre las geometrías para ver información.

### `.explore()` — Folium / Leaflet.js (interactivo)

- Genera un **mapa interactivo** embebido en el notebook, basado en la librería JavaScript **Leaflet.js**, a través del wrapper de Python llamado **Folium**.
- Permite hacer zoom, desplazarse (pan), hacer clic en las geometrías para ver los valores de sus atributos (tooltips/popups), y se superpone sobre un mapa base real (como OpenStreetMap) para dar contexto geográfico (calles, ciudades, relieve, etc.).
- Es mucho más pesado computacionalmente y en tamaño de archivo (porque genera HTML+JS embebido), pero mucho más útil para *explorar* datos o para presentaciones/dashboards.

Por eso se instala folium justo después:

```python
!pip install folium
```

Esto es porque `.explore()` internamente **depende** de que folium esté instalado — GeoPandas no lo trae como dependencia obligatoria (es una dependencia "opcional") para no forzar a todos los usuarios a instalar una librería pesada si solo quieren usar `.plot()`.

**Uso posterior con color:**

```python
countries.explore("area", legend='False')
```

Aquí `.explore()` recibe el nombre de una columna (`"area"`), lo que hace que el mapa interactivo coloree cada país según el valor de esa columna — esto se llama un **mapa coroplético** (choropleth), un tipo de mapa donde el color de cada región representa un valor numérico (en este caso, el área del país). El parámetro `legend` controla si se muestra o no la leyenda de colores.

---

## 5. ¿Qué es un `GeoDataFrame`?

```python
type(countries)
```

Esto confirma que `countries` es efectivamente un objeto de tipo `geopandas.geodataframe.GeoDataFrame`.

### Anatomía de un GeoDataFrame

Un `GeoDataFrame` es, conceptualmente:

> Un `DataFrame` de pandas + una columna especial de geometría + métodos geoespaciales adicionales.

Puntos clave que explica el notebook:

1. **Tiene una columna `geometry`** (o el nombre que sea, pero siempre accesible vía el atributo `.geometry`) que contiene la información espacial — el equivalente a la propiedad "geometry" de un objeto GeoJSON.
2. **El resto de las columnas son atributos** — datos descriptivos normales, como en cualquier DataFrame (nombre, población, PIB, etc.).
3. El atributo `.geometry` **siempre** apunta a la columna geométrica activa, sin importar cómo se llame esa columna internamente. Esto da flexibilidad: podrías tener una columna llamada `"geom"` o `"shape"` y seguir accediendo a ella de forma uniforme con `.geometry`.
4. Tiene métodos extra para operaciones espaciales: cálculo de área, distancia, buffers (zonas de amortiguamiento alrededor de una geometría), intersecciones, uniones, etc. — el notebook menciona que estas se profundizarán en clases posteriores, aquí solo se usa el cálculo de área.

```python
countries.geometry
```

Esto devuelve una **GeoSeries**: es al `GeoDataFrame` lo que una `Series` es a un `DataFrame` en pandas — una sola "columna" pero especializada en geometría, con métodos propios para operaciones espaciales.

### Tipos de geometría

El notebook menciona los tipos fundamentales del estándar **Simple Features** (el estándar OGC que define cómo representar geometrías vectoriales):

- **Point**: un solo punto (x, y) — ideal para representar ciudades, sensores, ubicaciones puntuales.
- **LineString**: una secuencia de puntos conectados formando una línea — ideal para ríos, calles, rutas.
- **Polygon**: una forma cerrada — ideal para países, distritos, lagos, cualquier área.
- **MultiPoint / MultiLineString / MultiPolygon**: versiones "múltiples" de las anteriores, usadas cuando una sola entidad lógica está compuesta por varias piezas geométricas separadas. Por ejemplo, Chile como país es un `MultiPolygon` porque incluye el territorio continental **y** islas separadas (como Rapa Nui) que no están conectadas geométricamente al continente pero pertenecen al mismo registro/fila de datos.

Esta distinción entre "geometría simple" y "multi-geometría" es fundamental porque explica por qué, por ejemplo, un archivo de países puede tener una sola fila para "Chile" aunque su forma real esté compuesta por decenas de polígonos separados (islas, fiordos, etc.).

---

## 6. Cálculo de área y trabajo con atributos numéricos

```python
countries = countries.to_crs(epsg=3857)
areas = countries.geometry.area
countries['area'] = countries.geometry.area
countries['area_km2'] = countries['area'] / 1e6
```

**¿Por qué reproyectar antes de calcular el área?** Como se explicó en la sección de CRS, calcular `.area` sobre geometrías en EPSG:4326 (grados) da un número que no representa metros cuadrados reales — sería una cifra matemáticamente calculable pero físicamente sin sentido directo. Al reproyectar primero a EPSG:3857 (unidades en metros), `.geometry.area` devuelve directamente **metros cuadrados**.

**¿Por qué dividir por `1e6`?** Porque 1 kilómetro cuadrado = 1,000,000 de metros cuadrados (1 km = 1000 m, entonces 1 km² = 1000 m × 1000 m = 1,000,000 m²). Dividir por `1e6` (notación científica de 1,000,000) convierte el área de m² a km², una unidad mucho más interpretable para comparar tamaños de países.

**Nota conceptual importante que el notebook no menciona explícitamente pero es relevante:** EPSG:3857 (Web Mercator) **no preserva áreas de forma fiel** a escala global — distorsiona mucho cerca de los polos. Para un cálculo de área verdaderamente preciso a escala mundial se preferiría una proyección de área equivalente (equal-area), pero para fines didácticos e ilustrativos del notebook, Web Mercator es suficiente porque el objetivo es enseñar el flujo de trabajo (reproyectar → calcular), no obtener cifras de precisión científica.

---

## 7. Operaciones de pandas sobre datos geoespaciales

```python
mean_pop_est = countries['POP_EST'].mean()
max_pop_est = countries['POP_EST'].max()
min_pop_est = countries['POP_EST'].min()
```

Esta sección refuerza la idea central del notebook: **un GeoDataFrame sigue siendo un DataFrame**. Se puede aplicar `.mean()`, `.max()`, `.min()` sobre cualquier columna numérica exactamente igual que en pandas puro, sin que la presencia de la columna `geometry` interfiera.

### Filtrado booleano

```python
sur_america = countries[countries['CONTINENT'] == 'South America']
sur_america.plot(color='teal')
```

Esto es **indexación booleana**, un patrón fundamental de pandas: `countries['CONTINENT'] == 'South America'` genera una serie de valores `True`/`False` (uno por cada fila), y al usar esa serie como índice (`countries[...]`), se seleccionan solo las filas donde la condición es `True`. El resultado (`sur_america`) sigue siendo un `GeoDataFrame` completo, con su columna de geometría intacta, por lo que se puede graficar directamente.

---

## 8. Mapa coroplético personalizado con matplotlib

```python
fig, ax = plt.subplots(figsize=(10, 10))

sur_america.plot(column='POP_EST', cmap='bwr', legend=True,
                 legend_kwds={'label': "Población Estimada",
                              'orientation': "horizontal"}, ax=ax)

ax.set_title('Mapa de Sudamérica con Población Estimada', fontsize=15, fontweight='bold')

for x, y, label in zip(sur_america.geometry.centroid.x, sur_america.geometry.centroid.y, sur_america['SOVEREIGNT']):
    ax.text(x, y, label, fontsize=8, ha='center', color='darkblue', fontweight='bold')
```

Este bloque es más avanzado y combina varios conceptos:

**`fig, ax = plt.subplots(...)`**: es el patrón estándar de matplotlib orientado a objetos. `fig` es el "lienzo" completo, `ax` son los "ejes" (el área de dibujo específica). Se usa este patrón (en vez de simplemente `countries.plot()`) porque permite tener **control total** sobre la figura: agregar título, superponer capas, ajustar límites, etc. — cosas que serían más difíciles de controlar con la sintaxis simplificada.

**`column='POP_EST'`**: le dice a GeoPandas que coloree cada país (polígono) según el valor de la columna `POP_EST` — esto crea el mapa coroplético (mapa donde el color codifica una variable numérica).

**`cmap='bwr'`**: define el **mapa de colores** (colormap) a usar. `'bwr'` significa *blue-white-red* — un colormap divergente que va de azul a blanco a rojo. Este tipo de colormap es apropiado cuando hay un punto medio significativo (por ejemplo, para resaltar valores muy bajos en un extremo y muy altos en el otro).

**`legend=True` y `legend_kwds`**: activa la leyenda (barra de color) y personaliza su etiqueta ("Población Estimada") y orientación (horizontal en vez de vertical, que es el default).

**El bucle `for x, y, label in zip(...)`**: esta es la parte más interesante conceptualmente.

- `sur_america.geometry.centroid` calcula el **centroide** de cada polígono — es decir, el "centro de masa" geométrico de la forma. Esto es lo que usa GeoPandas para saber *dónde* poner una etiqueta de texto dentro de cada país, ya que no tendría sentido poner el texto en una esquina o fuera del polígono.
- `.centroid.x` y `.centroid.y` extraen las coordenadas x e y de ese punto central.
- `zip(...)` combina las tres listas (coordenada x, coordenada y, nombre del país) elemento por elemento, para poder iterar los tres a la vez.
- `ax.set_title(...)` agrega un título a la imagen del mapa.
- `ax.text(x, y, label, ...)` dibuja el texto (nombre del país) en la posición del centroide de cada país, con formato personalizado (tamaño de fuente, alineación horizontal centrada, color, negrita).

**¿Por qué es útil este patrón?** Porque `.plot()` por sí solo no etiqueta automáticamente las geometrías con texto — GeoPandas se enfoca en dibujar formas y colores, no en anotaciones textuales. Combinarlo con `ax.text()` en un bucle es la forma estándar de "anotar" un mapa estático con nombres.

---

## 9. Trabajando con distintos tipos de geometría: puntos y líneas

### Ciudades (puntos)

```python
cities = gpd.read_file(r"...\ne_110m_populated_places_simple.zip")
cities = cities[['name', 'geometry']]
cities.explore()
```

Este dataset representa cada ciudad como un único **Point** (punto), con coordenadas (longitud, latitud) que marcan su ubicación aproximada. A diferencia de los países (polígonos con área), un punto no tiene área ni perímetro — solo una ubicación.

### Ríos (líneas)

```python
rivers = gpd.read_file(r"...\ne_50m_rivers_lake_centerlines.zip")
rivers = rivers[['featurecla', 'name', 'geometry']]
rivers.explore()
print(rivers.geometry[0])
```

Aquí se nota el uso de la escala **50m** en vez de 110m (la usada para países) — esto es porque los ríos requieren más nivel de detalle para representarse de forma razonable (una línea muy simplificada perdería la forma serpenteante característica de un río), mientras que para un mapa mundial de países, 110m ya es suficiente.

`print(rivers.geometry[0])` muestra la representación en texto de la geometría del primer río — normalmente esto se ve como una cadena en formato **WKT** (Well-Known Text), por ejemplo algo como `LINESTRING (x1 y1, x2 y2, ...)`, que es el estándar textual para describir geometrías vectoriales.

---

## 10. Superposición de capas (layering)

```python
countries = gpd.read_file(...)  # se recarga porque antes se modificó (se reproyectó a metros)
```

**Nota importante del notebook:** aquí se vuelve a cargar `countries` desde el archivo original. Esto es porque antes se le aplicó `to_crs(epsg=3857)` de forma **destructiva** (sobreescribiendo la variable `countries`), por lo que su CRS ya no era el original (EPSG:4326) y no coincidía necesariamente con el de `rivers` y `cities`. Esta es una buena práctica a notar: cuando se reproyecta un GeoDataFrame y se sobreescribe la variable original, hay que tener cuidado de que siga siendo compatible con el resto del flujo de trabajo, o recargar los datos si es necesario.

### Combinar varias capas en un solo mapa

```python
ax = countries.plot(edgecolor='k', facecolor='none', figsize=(15, 10))
rivers.plot(ax=ax)
cities.plot(ax=ax, color='red')
ax.set(xlim=(-140, -20), ylim=(-60, 15))
```

Este es el patrón central para crear **mapas multicapa** en GeoPandas/matplotlib:

- Cada llamada a `.plot()` puede recibir el parámetro `ax=ax`, que le dice "no crees un gráfico nuevo, dibuja **sobre** este eje ya existente". Así se pueden apilar múltiples capas geoespaciales (países, ríos, ciudades) en la misma figura, cada una potencialmente con su propio estilo.
- `edgecolor='k', facecolor='none'`: dibuja los países solo con el **borde** (contorno negro, `'k'` = black) y sin relleno (`facecolor='none'`) — esto es útil cuando se quiere ver el contorno de los países como referencia, sin que el color de relleno tape las otras capas (ríos, ciudades) que se dibujan encima.
- `rivers.plot(ax=ax)` dibuja los ríos con su color por defecto (azul).
- `cities.plot(ax=ax, color='red')` dibuja las ciudades como puntos rojos.
- `ax.set(xlim=..., ylim=...)` recorta la vista del mapa a una región específica (aquí, aproximadamente el continente americano), usando límites de longitud (xlim) y latitud (ylim) para "hacer zoom" a la zona de interés.

### Ejemplo enfocado: mapa de un solo país (Argentina)

```python
country = countries[countries['SOVEREIGNT'] == 'Argentina']

rivers = rivers.to_crs(country.crs)
cities = cities.to_crs(country.crs)

fig, ax = plt.subplots(figsize=(15, 10))
country.plot(ax=ax, edgecolor='k', facecolor='none')
rivers.plot(ax=ax, color='blue', linewidth=1)
cities.plot(ax=ax, color='red', markersize=10)

ax.set_xlim(country.total_bounds[0] - 2, country.total_bounds[2] + 2)
ax.set_ylim(country.total_bounds[1] - 2, country.total_bounds[3] + 2)
ax.set_title('Mapa con ríos y ciudades', fontsize=15, fontweight='bold')
plt.show()
```

Puntos clave nuevos aquí:

- **`rivers.to_crs(country.crs)` y `cities.to_crs(country.crs)`**: esto es **crucial**. Para que varias capas se superpongan correctamente en un mapa, **todas deben estar en el mismo CRS**. Si `rivers` estuviera en un CRS distinto al de `country`, sus coordenadas no se alinearían visualmente con el país (aunque representen ubicaciones geográficamente correctas, los números de las coordenadas estarían en una escala/sistema distinto). `to_crs(country.crs)` toma el CRS actual de `country` y reproyecta `rivers`/`cities` para que coincidan.
- **`country.total_bounds`**: devuelve el rectángulo delimitador (bounding box) de la geometría, como un arreglo `[minx, miny, maxx, maxy]`. Es la forma estándar de saber "hasta dónde llega" un conjunto de geometrías en el espacio.
- **`total_bounds[0] - 2` / `total_bounds[2] + 2`**: se le resta/suma un margen (2 grados en este caso, ya que el CRS aquí sigue siendo en grados) a los límites del país, para que el mapa no quede "pegado" exactamente al borde del país, sino que tenga un pequeño margen visual alrededor — una práctica común de diseño cartográfico para que el mapa se vea más natural y no corte las etiquetas o capas cercanas al borde.
- **`markersize=10`**: controla el tamaño de los puntos (ciudades) en el gráfico.
- **`linewidth=1`**: controla el grosor de las líneas (ríos).

---

## 11. Ejercicios prácticos: datos de París

La segunda mitad del notebook cambia de escala geográfica: en vez de trabajar con el mundo completo, se trabaja con los **distritos administrativos de París**, usando un archivo GeoJSON (`quartier_paris.geojson`) obtenido del portal de datos abiertos de la ciudad de París (opendata.paris.fr).

### Carga y exploración inicial

```python
districts = gpd.read_file(r"...\quartier_paris.geojson")
districts.head(1)
districts.shape
districts.crs
districts.plot(figsize=(12, 6))
districts.explore()
```

Aquí se repite el flujo típico de exploración inicial de cualquier dataset geoespacial nuevo:

1. **Cargar** el archivo con `read_file()`.
2. **Inspeccionar** con `.head()` para ver la estructura de columnas y una muestra de los datos.
3. **`.shape`**: da el número de filas (features/distritos) y columnas — responde a la pregunta "¿cuántos distritos hay?" de forma inmediata (una tupla `(n_filas, n_columnas)`).
4. **`.crs`**: verificar en qué sistema de coordenadas vienen los datos (importante antes de hacer cualquier cálculo).
5. **`.plot()`**: una visualización rápida y estática para tener una primera impresión visual de la forma general del conjunto de datos.
6. **`.explore()`**: una visualización interactiva para poder hacer zoom y explorar distrito por distrito.

Este orden de exploración (`head → shape → crs → plot → explore`) es una buena práctica general al enfrentarse a cualquier dataset geoespacial nuevo, y el notebook lo usa como plantilla repetible.

### Selección de columnas relevantes

```python
districts = districts[['l_qu', 'perimetre', 'st_area_shape', 'geometry']]
```

Igual que con `countries`, se descartan columnas irrelevantes del GeoJSON original y se conservan solo:
- `l_qu`: probablemente el nombre/etiqueta del distrito ("libellé quartier").
- `perimetre`: el perímetro del distrito (posiblemente ya calculado en el dataset original).
- `st_area_shape`: el área del distrito (también posiblemente precalculada).
- `geometry`: la forma del distrito.

### Ejercicio: distritos más grandes por área

El ejercicio pide, paso a paso:

1. **Calcular el área de cada distrito** — usando `.geometry.area`, tal como se hizo con los países.
2. **Añadir esta área como nueva columna**.
3. **Convertir de m² a km²** dividiendo por `1e6` (mismo razonamiento explicado antes).
4. **Ordenar de mayor a menor** — usando `.sort_values(by='area', ascending=False)` (aparece comentado en el notebook, `# districts.sort_values(...)`, es decir, quedó como una línea de referencia/plantilla sin ejecutar en la versión final).
5. **Reproyectar a EPSG:3035** antes de calcular el área:

```python
districts = districts.to_crs(epsg=3035)
districts.geometry.area
```

**¿Por qué EPSG:3035 específicamente, y no EPSG:3857 como con los países?** Esta es una decisión metodológica importante que el notebook explica: **EPSG:3035 (ETRS89 / LAEA Europe)** es una proyección de **área equivalente (equal-area)** diseñada específicamente para Europa. A diferencia de Web Mercator (EPSG:3857), que distorsiona fuertemente las áreas (sobre todo lejos del ecuador), una proyección de área equivalente **preserva las proporciones reales de área** entre las distintas geometrías. Como el objetivo aquí es *comparar* el tamaño real de los distritos entre sí (cuál es más grande, cuál es más chico), es fundamental usar una proyección que no distorsione esas comparaciones — de lo contrario, un distrito podría "verse" más grande que otro en el cálculo simplemente por su posición geográfica, no por su tamaño real.

Esto contrasta con el ejemplo anterior de países del mundo, donde se usó EPSG:3857: para ese caso ilustrativo (calcular área a escala mundial de forma aproximada) era aceptable, pero para un análisis más riguroso a escala continental/regional como este, se elige una proyección más apropiada — EPSG:3035 aplica **solo** en el contexto europeo (fue diseñada para esa región), lo que es coherente porque París está en Europa.

```python
districts['area'] = districts.geometry.area / 1e6
```

Finalmente se agrega la columna de área en km², lista para poder ordenar y comparar distritos.

### Visualización final: mapa coroplético de París

```python
districts.plot(column='area', figsize=(12, 6), cmap='jet', legend=True)
```

Se cierra el notebook con un mapa coroplético de los distritos de París, coloreados según su área (`column='area'`), usando el colormap **`'jet'`** (un colormap muy conocido que va de azul → verde → amarillo → rojo, aunque hoy en día se considera menos ideal perceptualmente que alternativas como `'viridis'`, porque `'jet'` no tiene una progresión de luminosidad uniforme, lo que puede generar percepciones visuales engañosas sobre la magnitud de los datos — sin embargo, sigue siendo muy usado por su alto contraste visual y familiaridad).

---

## Resumen conceptual: ¿qué aprende este notebook, en esencia?

1. **GeoPandas extiende pandas**: todo el flujo de trabajo tabular (filtrar, agregar columnas, calcular estadísticas) se mantiene igual, con una columna especial `geometry` que agrega capacidades espaciales.

2. **El CRS no es un detalle técnico menor**: es la base para que las coordenadas tengan sentido, para que los cálculos de área/distancia sean correctos, y para que múltiples capas de datos se superpongan correctamente en un mismo mapa. Reproyectar (`to_crs`) es una operación central en cualquier flujo de trabajo geoespacial serio.

3. **Existen tres tipos básicos de geometría** (punto, línea, polígono) y cada uno se usa para representar distintos fenómenos del mundo real (ciudades como puntos, ríos como líneas, países/distritos como polígonos).

4. **Hay dos formas complementarias de visualizar**: estática (matplotlib, vía `.plot()`) para reportes/figuras fijas, e interactiva (folium/Leaflet, vía `.explore()`) para exploración y presentaciones dinámicas.

5. **Los mapas multicapa se construyen apilando `.plot(ax=ax)`**, siempre asegurándose de que todas las capas compartan el mismo CRS antes de superponerlas.

6. **La elección de proyección depende del propósito**: Web Mercator para visualización web general, proyecciones de área equivalente (como EPSG:3035) cuando el objetivo es comparar áreas de forma precisa dentro de una región específica.

---

## Nota práctica sobre las rutas de archivo

Vale la pena mencionar que el notebook usa rutas de archivo **absolutas y locales** (por ejemplo `C:\Users\jorge\Downloads\...`), lo que significa que este notebook **no es directamente ejecutable** en otro computador sin antes descargar los archivos de datos (Natural Earth, opendata.paris.fr) y actualizar las rutas para que apunten a la ubicación correcta en el sistema de quien lo ejecute. Esto es algo común en notebooks educativos/de clase, pero es importante tenerlo en cuenta si se quiere reproducir el análisis: hay que descargar los shapefiles/GeoJSON de las fuentes mencionadas (Natural Earth y Paris Open Data) y ajustar las rutas (`r"C:\Users\..."`) a donde efectivamente estén guardados los archivos.
