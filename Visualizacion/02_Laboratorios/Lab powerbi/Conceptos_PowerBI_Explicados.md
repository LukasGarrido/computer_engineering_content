# Conceptos Teóricos de Power BI

Este documento desarrolla en profundidad cada uno de los conceptos presentados en la sección "Fundamentos teóricos" del laboratorio EIN092B. La idea es que entiendas el **por qué** detrás de cada práctica, no solo la definición superficial.

---

## 1. Business Intelligence (BI) y Power BI

### ¿Qué es Business Intelligence?

BI es un campo que existe porque las organizaciones generan enormes cantidades de datos operativos (ventas, transacciones, registros de clientes, logs de sistemas) que **por sí solos no dicen nada útil**. Una fila en una base de datos que dice `2024-03-15, Cliente_882, $45.000` no es información, es un dato crudo. BI es el conjunto de procesos y herramientas que transforma ese dato crudo en algo que un gerente puede usar para tomar una decisión: "las ventas de marzo cayeron 12% respecto a febrero en la región sur".

### ¿Por qué Power BI es "self-service"?

Antes de herramientas como Power BI, el flujo típico era: un analista de negocio pedía un reporte, un equipo de TI escribía consultas SQL, generaba el reporte y se lo entregaba días o semanas después. Power BI colapsa ese proceso: la misma persona que necesita el análisis puede conectar los datos, transformarlos, modelarlos y visualizarlos sin depender de un especialista técnico intermedio. Esto es lo que se llama **self-service BI**.

### Las cuatro etapas del flujo de trabajo

1. **Obtención de datos**: conectar Power BI a las fuentes (Excel, SQL Server, APIs web, CSV, etc.). Esta etapa define de dónde viene la "materia prima".
2. **Transformación (ETL)**: limpiar y preparar esos datos con Power Query. Aquí se corrigen errores, se eliminan duplicados, se cambian tipos de datos.
3. **Modelado semántico**: definir cómo se relacionan las tablas entre sí y qué cálculos (medidas) se pueden hacer sobre ellas. Esta es la capa "invisible" pero más importante: es el cerebro que le da sentido a los datos.
4. **Visualización y consumo**: construir los reportes y dashboards que finalmente ve el usuario de negocio.

### ¿Qué es exactamente un "modelo semántico"?

Es fácil pensar que un modelo semántico es "solo las tablas cargadas", pero es más que eso: es la definición de **qué tablas existen, cómo se conectan entre sí, y qué fórmulas (medidas) están disponibles**. Piensa en el modelo semántico como el plano eléctrico de una casa: no es la casa en sí (eso sería el dashboard visual), pero si el plano está mal hecho, aunque la casa se vea bonita por fuera, algo no va a funcionar bien por dentro. Por eso el documento enfatiza que **un modelo mal diseñado puede generar resultados incorrectos incluso si las visualizaciones se ven correctas**: un gráfico de barras perfectamente formateado puede estar mostrando un número mal calculado si las relaciones del modelo están mal definidas.

---

## 2. Modelado dimensional

### El esquema estrella (star schema)

El esquema estrella es la forma estándar de organizar datos para análisis. Se basa en distinguir dos roles distintos que puede jugar una tabla:

- **Tablas de hechos (fact tables)**: contienen los eventos medibles que quieres analizar. Por ejemplo, cada fila es una venta individual: fecha, producto vendido, cliente, monto, cantidad. Estas tablas son las que más filas tienen (pueden ser millones) porque cada transacción genera una fila nueva.

- **Tablas de dimensiones (dimension tables)**: contienen los atributos descriptivos que usas para **filtrar y agrupar** los hechos. Por ejemplo, la tabla `Productos` tiene una fila por cada producto con su nombre, categoría, precio de lista; la tabla `Clientes` tiene una fila por cliente con su nombre, región, segmento.

La razón por la que se llama "esquema estrella" es visual: si dibujas la tabla de hechos en el centro y cada dimensión conectada directamente a ella, el diagrama se parece a una estrella con la tabla de hechos en el núcleo y las dimensiones como puntas irradiando hacia afuera.

**¿Por qué separar hechos de dimensiones en lugar de tener todo en una sola tabla gigante?** Porque si mezclas todo, terminas repitiendo información constantemente (el nombre completo del producto se repetiría en cada una de las miles de filas de venta de ese producto), lo cual infla el tamaño del modelo, hace más lento el procesamiento, y complica el mantenimiento (si cambias el nombre de un producto, tendrías que actualizarlo en miles de filas en lugar de una sola).

### El esquema copo de nieve (snowflake schema)

Es una variante donde las dimensiones, en lugar de ser tablas "planas" y autocontenidas, se normalizan en subtablas adicionales. Por ejemplo, en lugar de que la tabla `Productos` tenga una columna de texto `Categoría`, podrías tener una tabla separada `Categorías` conectada a `Productos`. Esto reduce la redundancia de datos (el nombre de la categoría no se repite en cada producto), pero en Power BI **generalmente no se recomienda** porque cada relación adicional que el motor tiene que atravesar para responder una consulta añade complejidad y puede afectar el rendimiento. La recomendación general es "aplanar" las dimensiones cuando sea razonable.

### Cardinalidad

La cardinalidad describe la naturaleza numérica de la relación entre dos tablas:

- **Uno a muchos (1:N)**: un valor en la tabla "uno" puede corresponder a muchas filas en la tabla "muchos". Es el caso más común: un producto (1) puede aparecer en muchas ventas (N). Esta es la relación recomendada y la que debes buscar establecer entre dimensión → hechos.
- **Uno a uno (1:1)**: cada valor de una tabla corresponde exactamente a un valor de la otra. Es poco común y suele indicar que en realidad esas dos tablas podrían fusionarse en una sola.
- **Muchos a muchos (N:N)**: ambos lados pueden tener múltiples coincidencias. Esto es más complejo de manejar y generalmente requiere una tabla intermedia (tabla puente) para evitar ambigüedades en los cálculos.

### Dirección del filtro

Cuando seleccionas un valor en un slicer o filtras una tabla, ese filtro tiene que "propagarse" a las tablas relacionadas para que las medidas se recalculen correctamente. La dirección del filtro determina hacia dónde viaja esa propagación:

- **Single direction (un solo sentido)**: el filtro va desde la dimensión hacia la tabla de hechos. Por ejemplo, si filtras la tabla `Clientes` por región, ese filtro afecta a `Ventas`, pero un filtro en `Ventas` no afectaría a `Clientes`. Este es el comportamiento por defecto y el recomendado en la gran mayoría de los casos.
- **Both/bidirectional (ambos sentidos)**: el filtro se propaga en las dos direcciones. Esto puede ser necesario en casos específicos, pero introduce el riesgo de **ambigüedad**: si tienes múltiples caminos bidireccionales entre tablas, el motor puede no saber cómo debe combinarse el filtrado, o puede generar resultados que no esperabas. Además, el filtrado bidireccional es computacionalmente más costoso.

**Analogía**: piensa en el filtro como el agua que fluye por tuberías. En un esquema estrella normal, el agua fluye "cuesta abajo" desde las dimensiones (más altas) hacia los hechos (más bajos). El modo bidireccional sería como si el agua también pudiera subir, lo cual puede ser útil en situaciones puntuales pero generalmente complica el sistema de tuberías.

---

## 3. Transformación de datos (Power Query)

### ¿Qué es Power Query y el lenguaje M?

Power Query es el motor de Power BI dedicado exclusivamente a la etapa de limpieza y preparación de datos (la "T" de ETL: Transform). Cuando usas la interfaz gráfica —por ejemplo, haces clic derecho en una columna y seleccionas "eliminar columna"— Power Query no solo ejecuta la acción, sino que **traduce esa acción a código** en un lenguaje llamado **M**. M es un lenguaje funcional, lo que significa que cada transformación se expresa como una función que toma una tabla de entrada y devuelve una tabla de salida modificada.

### El concepto de "paso" (applied step)

Cada transformación que aplicas —cambiar un tipo de dato, eliminar una columna, filtrar filas— queda registrada como un **paso** individual y visible en el panel de "Pasos aplicados". Esto es fundamental porque:

- Puedes ver exactamente qué se hizo y en qué orden.
- Puedes hacer clic en cualquier paso anterior y ver cómo se veían los datos en ese momento del proceso.
- Puedes reordenar, editar o eliminar pasos sin tener que rehacer todo desde cero.

Es literalmente como un historial de control de versiones aplicado a la limpieza de datos: cada paso es como un "commit" que puedes inspeccionar y modificar.

### ¿Por qué transformar en Power Query y no directamente en el modelo?

Esta es una decisión de arquitectura importante. Si limpias y calculas cosas en Power Query, esas operaciones se ejecutan **una sola vez**, cuando se actualizan los datos (refresh). Si en cambio intentas hacer esos mismos cálculos con columnas calculadas dentro del modelo (usando DAX), en algunos casos esos cálculos se recalculan con más frecuencia o consumen más memoria innecesariamente. La regla práctica es: **limpieza y preparación estructural → Power Query; cálculos analíticos dinámicos → DAX (medidas)**.

### Transformaciones típicas

- **Tipado de columnas**: asegurarte de que una columna de fechas sea reconocida como tipo `date` y no como texto, que una columna numérica sea `Int64` o `Decimal` y no texto. Esto es crítico porque si Power BI no reconoce una columna como fecha, no podrás hacer cálculos de tiempo (año, trimestre, etc.) sobre ella.
- **Eliminación de duplicados y filas vacías**: evita que una misma transacción se cuente dos veces o que filas completamente vacías distorsionen conteos.
- **Normalización de nombres de columnas**: cambiar `Fecha de Venta (dd/mm/yyyy)` por `FechaVenta` — nombres claros, sin espacios ni caracteres especiales, facilitan referenciarlos después en DAX.
- **Columnas calculadas simples en M**: por ejemplo `Date.Year([FechaVenta])` extrae el año de una fecha directamente en la etapa de preparación.
- **Filtrado de registros irrelevantes**: si tu análisis solo necesita los últimos 3 años, filtrar el resto reduce el volumen de datos que el modelo tiene que cargar y procesar, mejorando el rendimiento.

---

## 4. DAX (Data Analysis Expressions)

DAX es el lenguaje de fórmulas que usa Power BI (y también Excel con Power Pivot, y Analysis Services) para hacer cálculos **dentro del modelo semántico**. Es distinto de M: mientras M transforma tablas completas antes de que los datos entren al modelo, DAX calcula valores **usando** el modelo ya cargado.

### Columnas calculadas vs. Medidas — la distinción más importante de DAX

Esta es probablemente la confusión más común entre quienes empiezan con Power BI, así que vale la pena detenerse.

**Columnas calculadas:**
- Se calculan **una vez**, fila por fila, en el momento en que el modelo se procesa (cuando haces refresh).
- El resultado se **almacena físicamente** en la tabla, igual que cualquier otra columna. Esto significa que ocupa espacio en memoria (RAM) y en el archivo `.pbix`.
- Son útiles cuando necesitas ese valor como un atributo fijo por fila, por ejemplo, para usarlo como criterio de filtro o para agrupar (poner en el eje de un gráfico).
- Ejemplo: `NombreCompleto = [Nombre] & " " & [Apellido]` — cada fila de la tabla tendrá ese valor fijo calculado.

**Medidas:**
- Se calculan **dinámicamente, en el momento de la consulta**, es decir, cada vez que un visual necesita mostrar un número.
- No se almacenan como una columna; el resultado depende completamente del **contexto de filtro** activo en ese momento (qué año está seleccionado, qué región, qué fila de una tabla).
- No aumentan el tamaño del modelo (no ocupan espacio de almacenamiento adicional significativo).
- Son la forma preferida de construir KPIs porque **se recalculan automáticamente** según cómo interactúa el usuario con el reporte (al cambiar un slicer, todas las medidas visibles se vuelven a evaluar).
- Ejemplo: `Ventas Totales = SUM(Ventas[Monto])` — este número cambia según qué filtros estén activos: si filtras por "Región = Norte", la medida solo suma las ventas del norte.

**Analogía**: una columna calculada es como escribir un número en una hoja de papel: queda fijo ahí. Una medida es como una calculadora que recalcula el resultado cada vez que le cambias los números de entrada.

### Contexto de fila vs. Contexto de filtro

Estos dos conceptos son el corazón de cómo "piensa" DAX, y suelen ser lo más difícil de internalizar:

- **Contexto de fila**: es el contexto que existe cuando una expresión se está evaluando "fila por fila". Es relevante, por ejemplo, al crear una columna calculada: cuando escribes `[Precio] * [Cantidad]` en una columna calculada, DAX sabe a qué fila te refieres porque se está posicionando fila por fila mientras calcula.

- **Contexto de filtro**: es el conjunto de todos los filtros que están activos en el momento en que se evalúa una medida. Estos filtros pueden venir de: un slicer que el usuario seleccionó, un filtro de página o de reporte, o las filas/columnas de una tabla o matriz visual (cada celda de una matriz tiene su propio contexto de filtro implícito, determinado por el cruce de esa fila y esa columna).

Entender esta distinción es clave porque una misma fórmula puede comportarse de forma completamente distinta según en qué contexto se evalúe.

### CALCULATE(): la función más importante de DAX

`CALCULATE()` permite **modificar el contexto de filtro** de una expresión. Es decir, te permite decir "calcula esta medida, pero cambia (o agrega) estas condiciones de filtro específicas, sin importar qué esté seleccionado en el reporte".

Por ejemplo:
```
Ventas Año Actual =
    CALCULATE([Ventas Totales], YEAR('Calendario'[Fecha]) = YEAR(TODAY()))
```
Esta medida toma la medida base `[Ventas Totales]` pero le impone un filtro adicional: que el año de la fecha sea igual al año actual, sin importar qué año haya seleccionado el usuario en un slicer.

`CALCULATE()` es la base de funciones más avanzadas:
- **ALL()**: elimina los filtros de una tabla o columna, útil para calcular totales "sin importar el filtro actual" (por ejemplo, para calcular un porcentaje del total general).
- **ALLSELECTED()**: similar a `ALL()`, pero respeta los filtros externos al visual (como los de un slicer de página), y solo elimina el contexto de filtro interno del visual mismo. Útil para cálculos como "acumulado dentro de lo que el usuario ya filtró".
- **FILTER()**: permite aplicar una condición más compleja, fila por fila, dentro de una tabla, para construir el nuevo contexto de filtro.

Estas funciones combinadas permiten construir cálculos analíticos avanzados: comparaciones interanuales (como se ve en el ejemplo del laboratorio con `DATEADD`), rankings (`RANKX`), porcentajes del total, y acumulados.

---

## 5. Parámetros What-if y análisis de sensibilidad

### ¿Qué problema resuelven?

Imagina que quieres responder la pregunta: "si le doy un 15% de descuento a todos los productos, ¿cuánto bajarían mis ventas totales?" Sin un parámetro What-if, tendrías que crear una medida fija con ese 15% escrito directamente en la fórmula, y si quisieras probar con 20%, tendrías que editar la fórmula manualmente. Un parámetro What-if convierte ese número en algo que el **usuario final puede ajustar interactivamente** con un slicer, viendo el resultado cambiar en tiempo real.

### La tabla desconectada (disconnected table)

Técnicamente, cuando creas un parámetro What-if, Power BI genera una tabla auxiliar que **no tiene ninguna relación** con las demás tablas del modelo (ni con hechos ni con dimensiones). Por eso se llama "desconectada". Esto es intencional: esta tabla no debe filtrar ni agregar datos como lo haría una dimensión normal; su único propósito es proveer una lista de valores posibles (por ejemplo, de 0% a 30% en incrementos de 1%) que el usuario selecciona mediante un slicer.

El valor que el usuario selecciona se captura con la función `SELECTEDVALUE()`, y luego se usa dentro de una medida para modificar un cálculo existente. Por ejemplo:
```
Ventas con Descuento =
    [Ventas Totales] * (1 - 'Descuento WhatIf'[Descuento WhatIf Value])
```

Es importante notar: **el parámetro What-if no reemplaza una medida existente**, sino que introduce una variable nueva e independiente que se combina con medidas ya definidas. Por eso el documento recalca que primero debes tener claras tus medidas base antes de construir un escenario sobre ellas.

### Análisis de sensibilidad: el concepto general detrás

Los parámetros What-if son un caso particular de algo más amplio en BI: el **análisis de sensibilidad**, que estudia cómo cambia un resultado cuando varían una o más variables de entrada. Existen tres variantes:

1. **Análisis de una variable**: ajustas un solo parámetro (por ejemplo, el descuento) y observas su efecto. Es lo que construye un parámetro What-if estándar.
2. **Análisis de escenarios discretos (scenario analysis)**: en vez de un rango continuo de valores, comparas un puñado de escenarios predefinidos con nombre —por ejemplo, "pesimista", "base", "optimista"— cada uno con su propia combinación fija de supuestos (no solo una variable, sino varias combinadas en cada escenario).
3. **Análisis multivariable**: evalúas el efecto combinado de dos o más variables simultáneamente (por ejemplo, descuento y volumen de ventas a la vez). En Power BI esto normalmente requiere combinar varios parámetros What-if, o usar visuales especializados como el *tornado chart* (que muestra qué variables tienen mayor impacto en el resultado).

---

## 6. Indicadores clave de desempeño (KPIs)

### La diferencia entre una métrica y un KPI

Este es un punto conceptual que suele pasarse por alto: **no todo número relevante es un KPI**. Una métrica es simplemente cualquier dato medible (por ejemplo, "cantidad de visitas a una página"). Esa métrica solo se convierte en un **KPI** (Key Performance Indicator) cuando cumple dos condiciones adicionales: está **directamente ligada a un objetivo estratégico del negocio**, y tiene una **meta de referencia definida** contra la cual comparar el valor actual.

### El marco SMART

Para evaluar si una medida es un buen KPI, se suele usar el marco SMART:
- **Specific (específica)**: mide algo concreto, no algo vago.
- **Measurable (medible)**: puede cuantificarse con datos reales.
- **Achievable (alcanzable)**: la meta asociada es realista.
- **Relevant (relevante)**: está conectada a un objetivo real del negocio.
- **Time-bound (acotada en el tiempo)**: tiene un periodo de referencia definido (mensual, trimestral, etc.).

### Los tres componentes de un KPI

En la práctica, casi todo KPI requiere estos tres elementos:
1. **Valor actual**: el resultado obtenido hasta el momento (ej. Ventas Totales de este mes).
2. **Objetivo (target)**: el valor esperado o comprometido contra el cual se compara ese resultado.
3. **Estado o tendencia (status/trend)**: una señal visual —color, ícono, flecha— que indica de un vistazo si el indicador va bien, mal, o cómo ha evolucionado. Esta es la parte que le da al KPI su poder comunicativo: no basta con mostrar un número, hay que mostrar si ese número es "bueno" o "malo" respecto a lo esperado.

Esta estructura de tres componentes es literalmente la que sigue el visual nativo "KPI" de Power BI, aunque también puedes replicarla combinando tarjetas simples con formato condicional.

### Indicadores adelantados vs. rezagados (leading vs. lagging)

- **Rezagados (lagging)**: miden resultados que **ya ocurrieron**. Ejemplo: ventas del mes pasado. Son útiles para evaluar desempeño histórico, pero no te ayudan a anticipar el futuro.
- **Adelantados (leading)**: intentan **anticipar** resultados futuros. Ejemplo: cantidad de cotizaciones abiertas (que probablemente se conviertan en ventas próximamente).

Un buen dashboard suele combinar ambos tipos: los rezagados te dicen "cómo nos fue", los adelantados te dan una pista de "cómo nos podría ir".

### Evitar las "vanity metrics" (métricas vanidosas)

Son indicadores que **se ven impresionantes visualmente** pero que en realidad no informan ninguna decisión concreta. El ejemplo típico es "número total de registros históricos" sin relación con ningún objetivo específico: suena grande e importante, pero no le dice a nadie qué acción tomar. La regla práctica es que un buen KPI debe responder a una necesidad concreta y facilitar la identificación de acciones posibles, no solo "verse bien" en la pantalla.

---

## 7. Principios de diseño de dashboards

Un dashboard no es simplemente "poner varios gráficos juntos"; debe comunicar información de forma clara y jerarquizada. Cuatro principios guían este diseño:

- **Jerarquía visual**: los KPIs más importantes deben ubicarse en las zonas de mayor atención visual (típicamente la parte superior o superior-izquierda de la pantalla, según cómo se lee normalmente). El número de indicadores destacados debe mantenerse acotado —mostrar demasiados a la vez diluye la atención—; el resto de la información puede quedar disponible mediante interacción: drill-down (profundizar en el detalle), tooltips (información al pasar el mouse), o páginas secundarias.

- **Consistencia**: usar los mismos colores, tipografías y escalas a través de todas las páginas del reporte. Un error común es que un mismo color signifique cosas distintas en distintos gráficos (por ejemplo, verde = "bueno" en un gráfico pero verde = una categoría específica de producto en otro), lo cual confunde al usuario.

- **Interactividad con propósito**: los slicers y filtros deben facilitar la exploración de los datos, no sobrecargar al usuario con demasiadas opciones simultáneas que terminen paralizando la toma de decisiones (parálisis por análisis).

- **Elección del gráfico adecuado**: cada tipo de visualización comunica mejor cierto tipo de relación entre datos, y elegir el tipo incorrecto puede oscurecer el mensaje en lugar de aclararlo:
  - Líneas → tendencias a lo largo del tiempo.
  - Barras/columnas → comparaciones entre categorías.
  - Dispersión (scatter) → correlación entre dos variables numéricas.
  - Mapas → distribución geográfica.

---

## 8. Seguridad y gobierno de datos

### El problema que resuelve la seguridad a nivel de fila (RLS)

Cuando un reporte se comparte con múltiples usuarios, no siempre todos deben ver la misma información. Por ejemplo, un vendedor de la región Norte probablemente no debería poder ver los datos de ventas de la región Sur. La **Row Level Security (RLS)** permite definir **roles**, cada uno asociado a una expresión DAX que filtra qué filas puede ver cada usuario que consulta el reporte.

### RLS estático vs. RLS dinámico

- **RLS estático**: el filtro queda escrito de forma fija dentro de la definición del rol, por ejemplo `[Region] = "Norte"`. Es conceptualmente simple de implementar, pero **escala mal**: si tienes 10 regiones, necesitas crear y mantener 10 roles distintos, uno por cada una. Si agregas una región nueva, tienes que crear un rol adicional manualmente.

- **RLS dinámico**: el filtro se calcula automáticamente **en función de quién está consultando el reporte**, típicamente combinando la función `USERPRINCIPALNAME()` (que devuelve el correo del usuario que inició sesión) con `LOOKUPVALUE()` sobre una tabla de mapeo usuario–categoría. Ejemplo:
```
[Region] = LOOKUPVALUE(
    Usuarios[Region],
    Usuarios[Email], USERPRINCIPALNAME()
)
```
Aquí, un único rol sirve para **todos** los usuarios: en lugar de crear un rol por región, mantienes actualizada una tabla `Usuarios` que mapea cada correo a su región correspondiente. Si un usuario nuevo se une, solo agregas una fila a esa tabla, sin tener que tocar la configuración de roles. Este es el enfoque recomendado cuando el número de perfiles de acceso es grande o cambia con frecuencia.

### Dos comportamientos de RLS que es fácil malinterpretar

1. **Los roles son aditivos, no restrictivos entre sí.** Si un usuario pertenece a más de un rol (por ejemplo, `Rol_Ventas_Norte` y `Rol_Ventas_Sur`), Power BI le mostrará la **unión** de las filas permitidas por ambos roles —no la intersección—. Esto significa que asignar a alguien a más roles de los necesarios **amplía** su acceso a los datos, no lo restringe. Es un error común asumir lo contrario (que combinar roles reduce el acceso).

2. **RLS depende de la dirección del filtro en el modelo.** El filtro definido en un rol se propaga desde la tabla donde se define hacia las tablas relacionadas, siguiendo la dirección de filtrado configurada en las relaciones (ver sección de "Dirección del filtro" más arriba). Si una relación está configurada en un solo sentido y el filtro de RLS necesita propagarse en el sentido contrario, puede ser necesario habilitar el filtrado bidireccional en esa relación específica —evaluando cuidadosamente el impacto en el rendimiento y en la lógica del resto de las medidas del modelo, porque el bidireccional puede tener efectos secundarios en otros cálculos—.

### Seguridad a nivel de objeto (OLS) — un concepto relacionado

Mientras que RLS oculta **filas** de datos, la **Object Level Security (OLS)** oculta **tablas o columnas completas** según el rol del usuario. Por ejemplo, podrías ocultar por completo una columna de sueldos a ciertos perfiles, sin que ni siquiera sepan que esa columna existe en el modelo. Ambos mecanismos —RLS y OLS— forman parte de lo que en BI se llama **gobierno de datos**: el conjunto de políticas que garantizan que la información correcta llegue únicamente a quien debe tener acceso a ella.

### Power BI Desktop vs. Power BI Service

Es importante no confundir estos dos entornos:

- **Power BI Desktop**: la aplicación de escritorio donde se hace la mayor parte del trabajo de autoría (conectar datos, transformar, modelar, diseñar visuales).
- **Power BI Service**: la plataforma en la nube donde se **publican** los reportes terminados. Ahí se pueden configurar actualizaciones automáticas de datos (**scheduled refresh**) y **gateways** (puentes que permiten conectar el servicio en la nube con fuentes de datos que están alojadas localmente, como una base de datos SQL Server interna de la empresa).

Al publicar, existen **dos capas de seguridad distintas y complementarias** que no deben confundirse:
- Los **roles de RLS** definidos en el modelo controlan **qué filas de datos** ve cada usuario.
- Los **roles del workspace** en el Service (Visor, Colaborador, Miembro, Administrador) controlan **qué puede hacer** cada usuario con el reporte en sí mismo (por ejemplo, si puede editarlo, compartirlo, o solo verlo).

---

## Resumen de cómo se conectan todos estos conceptos

Estos conceptos no son piezas aisladas: forman una cadena donde cada etapa depende de que la anterior esté bien hecha:

1. **Power Query** limpia y prepara los datos crudos → sin datos limpios, cualquier cálculo posterior es poco confiable.
2. El **modelo semántico** (esquema estrella, cardinalidad, dirección de filtro) organiza esos datos limpios en una estructura coherente → sin relaciones correctas, las medidas DAX pueden dar resultados incorrectos aunque la fórmula esté bien escrita.
3. **DAX** (medidas, contexto de filtro, CALCULATE) construye los cálculos dinámicos sobre ese modelo → esto es lo que finalmente alimenta cada visual con números.
4. Los **KPIs** seleccionan cuáles de esos cálculos son realmente relevantes para el negocio, con una meta y un estado asociado.
5. Los **principios de diseño** organizan esos KPIs y visuales de forma clara en el dashboard.
6. La **RLS** asegura que cada usuario, al abrir ese mismo dashboard, solo vea la porción de datos que le corresponde.

Entender esta cadena es lo que separa "saber apretar botones en Power BI" de realmente entender BI como disciplina.
