*Octavio Valencia - Lukas Garrido*
*Visualización*
**Data set utilizado:** https://mavenanalytics.io/data-playground/pizza-place-sales

---

## 4.1 Construcción del modelo semántico

### Análisis y decisiones sobre el modelo

| Tabla            | Rol                     | Columnas clave                                          |
| ---------------- | ----------------------- | -------------------------------------------------------- |
| `orders`         | Dimensión (fecha/hora)  | `order_id`, `date`, `time`                                |
| `order_details`  | **Tabla de hechos**     | `order_details_id`, `order_id`, `pizza_id`, `quantity`    |
| `pizzas`         | Dimensión               | `pizza_id`, `pizza_type_id`, `size`, `price`              |
| `pizza_types`    | Dimensión               | `pizza_type_id`, `name`, `category`, `ingredients`        |
| `Usuarios`       | Tabla auxiliar (RLS)    | `Email`, `Category`                                       |

- `order_details` es la tabla de hechos (muchas filas, valores medibles = `quantity`). 
- El precio (`price`) vive en `pizzas`, no en `order_details`, así que para calcular ventas vas a necesitar relacionar tablas.
- **Se uso esquema copo de nieve**: `pizza_types` se fusionó dentro de `pizzas`, quedando una sola dimensión `Pizzas` con tamaño, precio, nombre, categoría e ingredientes. Así se evita el esquema copo de nieve y se simplifica el filtrado.
- **Se uso `category` en vez de región**: el dataset no tiene datos de clientes ni geografía, por esa razón  `Pizzas[category]` (Classic, Chicken, Supreme, Veggie) se usó como dimensión de segmentación para el dashboard y para RLS.
- **Esquema final** (estrella): `order_details` (hechos) ← `Pizzas` (1:N por `pizza_id`) y ← `orders` (1:N por `order_id`) → `Calendario` (1:N por fecha). Todas las relaciones son 1 a muchos, filtro de un solo sentido (dimensión → hechos).
---

## 4.2 Transformaciones en Power Query

- **Tipado**: `orders[date]` a Fecha y `orders[time]` a Hora (venían mal tipadas del CSV).
- **Columnas nuevas**: `Hora_día = Time.Hour([time])` y `Dia_semana = Date.DayOfWeekName([date])`, para realizar el análisis temporal.
- **Merge**: `pizzas` + `pizza_types` por `pizza_type_id`, expandiendo `name`, `category`, `ingredients`.

### Problemas detectados y corregidos durante el desarrollo

Durante la construcción del modelo se detectaron y corrigieron los siguientes problemas de datos, que en un inicio hacían parecer que el dashboard "solo filtraba por enero" o mostraba ventas irreales:

- **`order_details` truncada a 91 filas**: un paso de filtrado en el origen dejaba cargar solo los pedidos de enero (91 filas) contra las más de 21,000 órdenes reales de `orders`. Se identificó y eliminó ese paso para cargar el año completo.
- **`Pizzas[price]` con el punto decimal perdido**: una conversión de tipo con configuración regional incorrecta interpretaba el punto decimal como separador de miles en algunos valores (ej. `10.5` → `105`), inflando las ventas totales. Se corrigió reconvirtiendo la columna con configuración regional en inglés (Estados Unidos).
- **Dependencia circular en la columna de orden de días**: se necesitaba una columna auxiliar para ordenar `Dia_semana` cronológicamente (lunes a domingo en vez de alfabético). La primera versión (`Orden_Dia` calculada a partir de `Dia_semana` con `SWITCH`) generaba una dependencia circular al usarse a su vez para ordenar `Dia_semana`. Se resolvió calculando `Orden_Dia` directamente desde la fecha: `Orden_Dia = WEEKDAY(orders[date], 2)`.
- **Visual de prueba interfiriendo como filtro**: un visual dejado de pruebas anteriores (jerarquía de meses) estaba actuando como filtro cruzado sobre toda la página de Visión General, haciendo parecer que las tarjetas solo mostraban un mes a la vez. Se eliminó ese visual del dashboard final.

---

## 4.3 Desarrollo de medidas DAX

| Medida                | Fórmula                                                                                         | Qué calcula                                                                   |
| --------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Ventas_Totales        | `SUMX(order_details, order_details[quantity] * RELATED(Pizzas[price]))`                         | Ventas totales (precio vive en `Pizzas`, no en los hechos)                    |
| Ticket_Promedio       | `DIVIDE([Ventas_Totales],[Numero_Ordenes],0)`                                                   | Gasto promedio por orden                                                      |
| Crecimiento_Mensual_% | `DIVIDE([Ventas_Totales]-CALCULATE([Ventas_Totales],DATEADD('Calendario'[Date],-1,MONTH)),...)` | Variación vs. mes anterior (no interanual, porque solo hay datos de 2015)     |
| Ranking_Pizza         | `RANKX(ALL(Pizzas[name]),[Ventas_Totales],,DESC)`                                               | Ranking de pizzas por ventas, comparando cada una contra el catálogo completo |
| Ventas_con_Aumento    | `SUMX(order_details, ... * (1+'Aumento Precio'[Value]))`                                        | Medida del parámetro What-if, simula alza de precio                           |
| Meta Ventas           | `AVERAGEX(VALUES('Calendario'[mes]), [Ventas_Totales]) * 12`                                    | Meta de referencia proyectada a partir del promedio mensual histórico         |
| KPI Ventas vs Meta    | `IF([Ventas_Totales] >= [Meta Ventas], "Meta alcanzada", "Meta no alcanzada")`                  | Indicador binario de cumplimiento de meta                                     |

> Nota sobre `Ranking_Pizza`: la primera versión usaba `ALL(Pizzas[pizza_id])`, lo que generaba un desfase de granularidad frente a las tablas/gráficos agrupados por `Pizzas[name]` (todas las pizzas terminaban en la posición 1). Se corrigió usando `ALL(Pizzas[name])`, que coincide con el nivel de detalle usado en los visuales.

---

## 4.4 Parámetros What-if

Se creó un parámetro numérico (**Aumento Precio**) mediante Modelado → Nuevo parámetro → Parámetro numérico, que genera automáticamente una tabla de valores y una medida `'Aumento Precio'[Value]` asociada a un slicer.

Este parámetro se usa dentro de la medida `Ventas_con_Aumento`, que recalcula el ingreso total aplicando el porcentaje de aumento seleccionado sobre el precio de cada pizza:

```dax
Ventas_con_Aumento =
SUMX(
    order_details,
    order_details[quantity] * RELATED(Pizzas[price]) * (1 + 'Aumento Precio'[Value])
)
```

Al mover el slicer del parámetro, el usuario puede simular en vivo cuánto subirían los ingresos totales si se aplicara un alza de precio (por ejemplo, +5%, +10%), sin modificar los datos originales. Esto mismo se reutilizó como base conceptual para la medida `Meta Ventas` en la Página 1 del dashboard (ver 4.5), donde también se ofrece la alternativa de convertir la meta en un parámetro What-if ajustable en vivo.

---

## 4.5 Diseño del dashboard

Como el dataset no tiene clientes ni región geográfica, la tercera página se adaptó para analizar comportamiento de consumo en el tiempo en vez de cliente/región.

### Página 1 — Visión general

- Tarjetas: `Ventas_Totales`, `Pizzas_Vendidas`, `Numero_Ordenes`, `Ticket_Promedio`.
- Gráfico de líneas: `Ventas_Totales` por mes, usando `Calendario[Nombre_Mes]` (ordenado cronológicamente mediante "Ordenar por columna" → `mes`).
- Slicers globales: mes, `Pizzas[category]`, `Pizzas[size]`.
- KPI binario `KPI Ventas vs Meta`, comparando `Ventas_Totales` contra `Meta Ventas`.

### Página 2 — Análisis por producto

- Gráfico de barras: `Ventas_Totales` por `Pizzas[name]`, filtrado a Top 10.
- Gráfico de dispersión: precio promedio vs. `Pizzas_Vendidas`, coloreado por `category`.
- Tabla con `Ranking_Pizza`.
- Filtros por `category` y `size`.

### Página 3 — Análisis por tiempo y comportamiento de consumo

*(reemplaza "cliente/región", ya que el dataset no tiene esos datos)*

- Matriz con formato condicional (mapa de calor) de `Pizzas_Vendidas` por `Dia_semana` × `Hora_día`, para identificar horas pico.
- Gráfico de columnas: número de órdenes por día de la semana, ordenado cronológicamente mediante la columna auxiliar `Orden_Dia`.
- Gráfico de embudo: categorías más pedidas en orden descendente.
- Formato condicional en la tabla de horas, resaltando en verde las horas de mayor venta.

---

## 4.6 Configuración de Row Level Security (RLS)

Como el dataset no tiene región, se usó `Pizzas[category]` (Classic, Chicken, Supreme, Veggie) como atributo de control — funciona igual de bien conceptualmente y es un campo real del dataset.

### RLS estático

Se crearon cuatro roles (Modelado → Administrar roles), uno por categoría, cada uno con un filtro DAX fijo sobre la tabla `Pizzas`:

```dax
[category] = "Classic"      // Rol_Classic
[category] = "Chicken"      // Rol_Chicken
[category] = "Supreme"      // Rol_Supreme
[category] = "Veggie"       // Rol_Veggie
```

### RLS dinámico (versión recomendada)

Se creó una tabla auxiliar `Usuarios` (Email, Category), cargada manualmente con filas de prueba:

| Email               | Category |
| ------------------- | -------- |
| ana@empresa.com     | Classic  |
| bruno@empresa.com   | Supreme  |

Y un único rol `Rol_Dinamico`, con este filtro sobre `Pizzas`:

```dax
[category] = LOOKUPVALUE(
    Usuarios[Category],
    Usuarios[Email], USERPRINCIPALNAME()
)
```

Este filtro busca el correo del usuario actual (`USERPRINCIPALNAME()`) en la tabla `Usuarios` y devuelve la categoría que le corresponde. La tabla `Usuarios` no está relacionada con el resto del modelo; se consulta directamente dentro de la fórmula del rol.

### Prueba

Se probó cada rol desde Modelado → Ver como (los estáticos directamente, y el dinámico simulando un usuario específico como "Otro usuario" con el correo de prueba), confirmando que en todas las páginas del dashboard solo se ven las pizzas de la categoría correspondiente.

### Por qué la versión dinámica es más escalable

La versión estática requiere crear y mantener un rol nuevo por cada categoría existente; si el negocio agrega una categoría nueva o decide dar acceso a más usuarios, cada uno necesitaría su propio rol estático, lo cual es inmanejable a mediano plazo. La versión dinámica no depende del número de categorías ni de usuarios: basta con agregar una fila nueva a la tabla `Usuarios` (correo + categoría) para dar de alta a alguien, sin tocar el modelo, los roles ni el reporte.

### Nota sobre dirección de filtro

Como `Pizzas` está relacionada con `order_details` en un solo sentido (filtro desde la dimensión hacia los hechos), el filtro de RLS definido en `Pizzas` se propaga correctamente hacia `order_details`, sin necesitar relaciones bidireccionales ni ajustes adicionales — un buen ejemplo de que RLS bien ubicado en la dimensión correcta no requiere trucos adicionales.

---

## Resumen del mapeo de tablas

| Requisito del laboratorio    | Cómo se cumple con este dataset                                                 |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Modelo con múltiples fuentes | CSV (4 tablas) + datos manuales (`Usuarios`)                                    |
| Esquema estrella             | `order_details` (hechos) + `Pizzas` (aplanada) + `orders`/`Calendario` (tiempo) |
| Transformaciones Power Query | Tipado, columnas de hora/día, fusión de tablas, limpieza de nombres             |
| Medidas DAX                  | Ventas, ticket promedio, crecimiento mensual, ranking, % del total              |
| Parámetro What-if            | Simulación de aumento de precio                                                 |
| Dashboard 3 páginas          | Visión general / Producto / Tiempo (sustituye a cliente-región)                 |
| RLS                          | Por `category` de pizza, estático y dinámico con tabla `Usuarios`               |
