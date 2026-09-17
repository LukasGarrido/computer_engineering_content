# Guía práctica: Laboratorio Power BI con dataset "Pizza Place Sales"

Esta guía adapta cada actividad del laboratorio EIN092B al dataset [Pizza Place Sales](https://mavenanalytics.io/data-playground/pizza-place-sales) de Maven Analytics (ventas de un año de "Plato's Pizza", un local ficticio). Sigue el mismo orden que el documento original (secciones 4.1 a 4.6).

## 0. Conoce el dataset antes de empezar

El dataset viene en **4 archivos CSV** que ya forman, casi de fábrica, un esquema estrella:

| Tabla | Rol | Columnas clave | Filas aprox. |
|---|---|---|---|
| `orders` | Dimensión (fecha/hora) | `order_id`, `date`, `time` | ~21.350 |
| `order_details` | **Tabla de hechos** | `order_details_id`, `order_id`, `pizza_id`, `quantity` | ~48.620 |
| `pizzas` | Dimensión | `pizza_id`, `pizza_type_id`, `size`, `price` | 97 |
| `pizza_types` | Dimensión | `pizza_type_id`, `name`, `category`, `ingredients` | 32 |

**Importante:** `order_details` es la tabla de hechos (muchas filas, valores medibles = `quantity`). El precio (`price`) vive en `pizzas`, no en `order_details`, así que para calcular ventas vas a necesitar relacionar tablas (esto es intencional, para que practiques `RELATED()` y `SUMX()`).

**Limitación a tener en cuenta:** este dataset **no tiene datos de clientes ni de región/ubicación**. Más abajo te explico dos formas de resolver esto para la parte de RLS y de la página "por cliente o región" del dashboard.

---

## 1. Construcción del modelo semántico (sección 4.1)

### Paso 1 — Descargar los datos
Entra a https://mavenanalytics.io/data-playground/pizza-place-sales y descarga el ZIP con los 4 CSV.

### Paso 2 — Importar desde múltiples fuentes (mínimo 2 orígenes distintos)
El requisito del laboratorio es conectar **al menos dos orígenes de datos distintos**. Como los 4 CSV cuentan como un solo tipo de origen ("archivo de texto/CSV"), agrega una **segunda fuente de tipo diferente**. Te recomiendo estas dos, que además te sirven más adelante:

- **Fuente Web (tipo de cambio):** `Inicio → Obtener datos → Web`. Usa una API pública de tipo de cambio, por ejemplo `https://api.exchangerate-api.com/v4/latest/USD`, para traer el valor USD→CLP y así poder mostrar tus ventas (que están en USD) también en pesos chilenos. Esto cumple exactamente el ejemplo que da el laboratorio ("Fuente Web para tipos de cambio").
- **Tabla ingresada manualmente (para RLS más adelante):** `Inicio → Obtener datos → Escribir datos`. Crea una tabla `Usuarios` con columnas `Email` y `Category` (la usarás en la sección de RLS).

Con esto tienes 3 tipos de origen distintos: CSV, Web y datos manuales — más que suficiente.

Importa los 4 CSV: **Inicio → Obtener datos → Texto/CSV**, uno por uno (`orders.csv`, `order_details.csv`, `pizzas.csv`, `pizza_types.csv`).

### Paso 3 — Comprobar estructura de las tablas
En la **Vista de datos**, revisa:
- `orders`: que `date` se haya cargado como fecha y `time` como hora (Power BI a veces las detecta como texto).
- `pizza_types`: la columna `ingredients` viene como un solo texto largo separado por comas — está bien así por ahora, la limpiamos en Power Query.
- Verifica que no haya columnas índice sobrantes (a veces el CSV trae una columna extra sin nombre).

### Paso 4 — Definir relaciones entre tablas
Ve a la **Vista de modelo** y crea estas relaciones (arrastrando el campo clave de una tabla a otra):

```
orders (1) -------- (muchos) order_details      [por order_id]
pizzas (1) -------- (muchos) order_details      [por pizza_id]
pizza_types (1) --- (muchos) pizzas             [por pizza_type_id]
```

Este es un **esquema copo de nieve** (`pizza_types → pizzas → order_details`) porque `pizza_types` no se conecta directamente a los hechos. Como el documento recomienda evitar copos de nieve en Power BI, en el Paso 6 de Power Query vamos a **aplanarlo**: fusionar `pizza_types` dentro de `pizzas` para que el modelo final quede como una estrella real:

```
Pizzas (dimensión aplanada, incluye category, name, ingredients, size, price)
   |
   +--- (muchos) order_details  <-- tabla de hechos
   |
Orders (dimensión de fecha/hora) --- (muchos) order_details
```

### Paso 5 — Cardinalidad y dirección de filtro
Todas las relaciones de arriba deben quedar como **1 a muchos**, con dirección de filtro **de un solo sentido** (desde la dimensión hacia `order_details`). No actives bidireccional a menos que lo necesites explícitamente para RLS (ver sección 6).

### Paso 6 — Validar con tabla temporal
Crea una página de prueba, arrastra `pizzas[name]`, `orders[date]` y `order_details[quantity]` a una tabla visual y confirma que los números se ven razonables (sin filas en blanco raras, sin duplicación de cantidades).

---

## 2. Transformaciones en Power Query (sección 4.2)

Abre **Inicio → Transformar datos** y aplica esto por tabla:

### `orders`
- Verifica tipo `date` = Fecha, `time` = Hora.
- Crea columna calculada `Hora del día` = `Time.Hour([time])` (para análisis de horas pico).
- Crea columna `Día semana` = `Date.DayOfWeekName([date])`.
- Quita duplicados por `order_id`.

### `order_details`
- Verifica que `quantity` sea `Int64`.
- Elimina filas con `order_id` o `pizza_id` nulos (si existieran).

### `pizzas`
- Verifica que `price` sea tipo `Decimal` (moneda), no texto.
- `size` como texto categórico (S, M, L, XL, XXL).

### `pizza_types`
- Columna `ingredients`: sepárala en una lista si quieres analizar ingredientes individuales (`Dividir columna → por delimitador → coma`), aunque para este laboratorio puedes dejarla como texto único.
- Normaliza `category` (Classic, Chicken, Supreme, Veggie) — revisa que no haya espacios extra.

### Fusión para aplanar el copo de nieve (paso clave)
En la consulta `pizzas`, usa **Combinar consultas → Combinar** con `pizza_types` por `pizza_type_id`, y expande las columnas `name`, `category` e `ingredients`. Resultado: una sola tabla `Pizzas` con todo el detalle del producto, sin necesidad de mantener `pizza_types` como tabla aparte en el modelo final. Elimina la relación con `pizza_types` y, opcionalmente, deshabilita la carga de esa consulta (clic derecho → **Habilitar carga** desmarcado) ya que su información ya vive dentro de `Pizzas`.

### Fuente Web (tipo de cambio)
En la consulta del tipo de cambio, filtra o expande el JSON hasta quedarte con una tabla simple: `Moneda = "CLP"`, `Valor = <número>`. Esta tabla queda **desconectada** del modelo (no necesita relación), la usarás con `SELECTEDVALUE()` o directamente como constante en una medida.

### Cerrar y aplicar
Termina con **Cerrar y aplicar**.

---

## 3. Desarrollo de medidas DAX (sección 4.3)

Crea una tabla de medidas: **Inicio → Nueva tabla** → `Medidas = ROW("_", 0)` (o el método que prefieras para crear una tabla vacía) y agrega ahí todas las medidas.

También crea una **tabla de calendario** para poder usar funciones de inteligencia de tiempo correctamente:

```dax
Calendario =
CALENDAR(MIN(orders[date]), MAX(orders[date]))
```
Luego agrégale columnas `Año`, `Mes`, `NombreMes`, `Trimestre` con DAX o Power Query, y relaciónala 1 a muchos con `orders[date]`.

### Medidas básicas

```dax
Pizzas Vendidas = SUM(order_details[quantity])

Número de Órdenes = DISTINCTCOUNT(order_details[order_id])

Ventas Totales =
SUMX(order_details, order_details[quantity] * RELATED(Pizzas[price]))
```

> Nota: como `price` vive en `Pizzas` y no en `order_details`, no puedes usar `SUM()` directo — necesitas `SUMX()` recorriendo `order_details` fila por fila y trayendo el precio relacionado con `RELATED()`.

```dax
Ticket Promedio = DIVIDE([Ventas Totales], [Número de Órdenes], 0)

Pizzas por Orden = DIVIDE([Pizzas Vendidas], [Número de Órdenes], 0)
```

### Medida derivada: crecimiento

El dataset cubre **un solo año (2015)**, así que el crecimiento interanual (año contra año) no aplica — no hay un año anterior con el cual comparar. En su lugar, calcula **crecimiento mes a mes**:

```dax
Ventas Mes Anterior =
CALCULATE([Ventas Totales], DATEADD('Calendario'[Date], -1, MONTH))

Crecimiento Mensual % =
DIVIDE([Ventas Totales] - [Ventas Mes Anterior], [Ventas Mes Anterior], 0)
```

### Funciones de contexto

```dax
Ventas Categoría Actual =
CALCULATE([Ventas Totales], ALLSELECTED(Pizzas[category]))

Ranking Pizza =
RANKX(ALL(Pizzas[name]), [Ventas Totales], , DESC)

% del Total =
DIVIDE([Ventas Totales], CALCULATE([Ventas Totales], ALL(Pizzas)), 0)
```

### Medida usando la fuente Web (tipo de cambio)

```dax
Ventas Totales CLP =
[Ventas Totales] * SELECTEDVALUE('TipoCambio'[Valor])
```

### Formatea las medidas
Asigna formato moneda (USD y CLP), porcentaje a las medidas de `%`, y número entero a los conteos.

---

## 4. Parámetros What-if (sección 4.4)

Un escenario natural para una pizzería: **simular un aumento de precios**.

### Crear el parámetro
`Modelado → Parámetro → Parámetro What-if`:
- Nombre: `Aumento Precio`
- Mínimo: 0, Máximo: 0.30, Incremento: 0.01, Valor predeterminado: 0

Esto genera automáticamente una tabla desconectada `Aumento Precio` con una columna de valores y una medida `Aumento Precio Value`.

### Medida que usa el parámetro

```dax
Ventas con Aumento =
SUMX(
    order_details,
    order_details[quantity] * RELATED(Pizzas[price]) * (1 + 'Aumento Precio'[Aumento Precio Value])
)

Impacto del Aumento = [Ventas con Aumento] - [Ventas Totales]
```

### Probar
Agrega un slicer con `Aumento Precio`, y dos tarjetas: `[Ventas Totales]` vs `[Ventas con Aumento]`. Al mover el slicer de 0% a 30%, ambas tarjetas deben reaccionar (la segunda cambia, la primera no).

---

## 5. Diseño del dashboard (sección 4.5)

Como el dataset no tiene clientes ni región geográfica, adapta la tercera página así:

**Página 1 — Visión general**
- Tarjetas: `Ventas Totales`, `Pizzas Vendidas`, `Número de Órdenes`, `Ticket Promedio`.
- Gráfico de líneas: `Ventas Totales` por mes (usando `Calendario[NombreMes]`).
- Slicers globales: mes, categoría (`Pizzas[category]`), tamaño (`Pizzas[size]`).
- KPI binario:
```dax
KPI Ventas vs Meta =
IF([Ventas Totales] >= [Meta Ventas], "Meta alcanzada", "Meta no alcanzada")
```
(Define `Meta Ventas` como una medida fija, por ejemplo un promedio mensual histórico multiplicado por 12, o usa el parámetro What-if como "meta simulada".)

**Página 2 — Análisis por producto**
- Gráfico de barras: `Ventas Totales` por `Pizzas[name]` (top 10).
- Gráfico de dispersión: `price` promedio vs `Pizzas Vendidas`, por categoría.
- Tabla con `Ranking Pizza`.
- Filtro por `category` y `size`.

**Página 3 — Análisis por tiempo y comportamiento de consumo** *(reemplaza "cliente/región", ya que el dataset no tiene esos datos)*
- Mapa de calor (matriz con formato condicional) de `Pizzas Vendidas` por `Día semana` × `Hora del día`, para identificar horas pico.
- Gráfico de columnas: órdenes por día de la semana.
- Gráfico de embudo (opcional): categorías más pedidas en orden descendente, simulando un "proceso de preferencia".
- Formato condicional en tabla de horas: resaltar en verde las horas de mayor venta.

> Si tu profesor exige explícitamente una dimensión geográfica, puedes crear una columna ficticia `Zona de Reparto` en Power Query (por ejemplo, asignando "Norte"/"Sur"/"Centro" según el resto de `order_id % 3`), dejando claro en tu documento PDF que es una variable sintética creada para efectos del ejercicio, ya que el dataset original no incluye esa información.

---

## 6. Configuración de Row Level Security (sección 4.6)

Como no hay región, usa **`Pizzas[category]`** (Classic, Chicken, Supreme, Veggie) como el atributo de control — funciona igual de bien conceptualmente y es un campo real del dataset.

### RLS estático (versión simple)
`Modelado → Administrar roles → Crear rol` para cada categoría, por ejemplo `Rol_Classic`, y en el filtro DAX de la tabla `Pizzas`:

```dax
[category] = "Classic"
```
Repite para `Rol_Chicken`, `Rol_Supreme`, `Rol_Veggie`.

### RLS dinámico (versión recomendada)
Usa la tabla `Usuarios` que creaste como segunda fuente (Email, Category). Crea un único rol `Rol_Dinamico` con este filtro sobre `Pizzas`:

```dax
[category] = LOOKUPVALUE(
    Usuarios[Category],
    Usuarios[Email], USERPRINCIPALNAME()
)
```

Llena la tabla `Usuarios` con un par de filas de prueba, por ejemplo:

| Email | Category |
|---|---|
| ana@empresa.com | Classic |
| bruno@empresa.com | Supreme |

### Probar
`Modelado → Ver como → Rol_Dinamico` (o los estáticos) y confirma que solo ves las pizzas de la categoría correspondiente en todas las páginas.

### Nota sobre dirección de filtro
Si `Pizzas` está relacionada a `order_details` en un solo sentido, el filtro de RLS definido en `Pizzas` se propagará correctamente hacia `order_details` (porque el filtro va desde la dimensión hacia los hechos, que es la dirección normal). No deberías necesitar bidireccional aquí — es un buen ejemplo de que RLS bien ubicado en la dimensión correcta no requiere trucos adicionales.

---

## 7. Qué poner en el PDF de entrega

Recuerda que el laboratorio pide un PDF breve explicando:
1. **Decisiones de modelado**: por qué aplanaste `pizza_types` dentro de `Pizzas` (evitar copo de nieve), por qué usaste `category` en vez de región para RLS (limitación del dataset), y el esquema final de relaciones.
2. **Transformaciones en Power Query**: tipado de `date`/`time`, columnas `Hora del día` y `Día semana`, la fusión (merge) de `pizza_types` en `pizzas`, y la fuente Web del tipo de cambio.
3. **Medidas DAX**: lista las medidas clave (`Ventas Totales`, `Ticket Promedio`, `Crecimiento Mensual %`, `Ranking Pizza`, la medida del parámetro What-if) con una frase de qué calcula cada una.
4. **Implementación de RLS**: explica la diferencia entre tu versión estática y dinámica, y por qué la dinámica es más escalable si en el futuro hay más categorías o usuarios.

---

## Resumen del mapeo de tablas

| Requisito del laboratorio | Cómo se cumple con este dataset |
|---|---|
| Modelo con múltiples fuentes | CSV (4 tablas) + Web (tipo de cambio) + datos manuales (`Usuarios`) |
| Esquema estrella | `order_details` (hechos) + `Pizzas` (aplanada) + `Orders`/`Calendario` (tiempo) |
| Transformaciones Power Query | Tipado, columnas de hora/día, fusión de tablas, limpieza de nombres |
| Medidas DAX | Ventas, ticket promedio, crecimiento mensual, ranking, % del total |
| Parámetro What-if | Simulación de aumento de precio |
| Dashboard 3 páginas | Visión general / Producto / Tiempo (sustituye a cliente-región) |
| RLS | Por `category` de pizza, estático y dinámico con tabla `Usuarios` |
