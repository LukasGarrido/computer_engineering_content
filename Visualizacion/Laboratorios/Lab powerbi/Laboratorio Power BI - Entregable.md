*Octavio Valencia - Lukas Garrido*
*Visualización*
**Data set utilizado:** https://mavenanalytics.io/data-playground/pizza-place-sales

---

## 4.1 Construcción del modelo semántico

### Análisis y decisiones sobre el modelo 

| Tabla           | Rol                    | Columnas clave                                         |
| --------------- | ---------------------- | ------------------------------------------------------ |
| `orders`        | Dimensión (fecha/hora) | `order_id`, `date`, `time`                             |
| `order_details` | **Tabla de hechos**    | `order_details_id`, `order_id`, `pizza_id`, `quantity` |
| `pizzas`        | Dimensión              | `pizza_id`, `pizza_type_id`, `size`, `price`           |
| `pizza_types`   | Dimensión              | `pizza_type_id`, `name`, `category`, `ingredients`     |
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

---

## 4.3 Desarrollo de medidas DAX

| Medida                | Fórmula                                                                                         | Qué calcula                                                               |
| --------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Ventas_Totales        | `SUMX(order_details, order_details[quantity] * RELATED(Pizzas[price]))`                         | Ventas totales (precio vive en `Pizzas`, no en los hechos)                |
| Ticket_Promedio       | `DIVIDE([Ventas_Totales],[Numero_Ordenes],0)`                                                   | Gasto promedio por orden                                                  |
| Crecimiento_Mensual_% | `DIVIDE([Ventas_Totales]-CALCULATE([Ventas_Totales],DATEADD('Calendario'[Date],-1,MONTH)),...)` | Variación vs. mes anterior (no interanual, porque solo hay datos de 2015) |
| Ranking_Pizza         | `RANKX(ALL(Pizzas[name]),[Ventas_Totales],,DESC)`                                               | Ranking de pizzas por ventas                                              |
| Ventas_con_Aumento    | `SUMX(order_details, ... * (1+'Aumento Precio'[Value]))`                                        | Medida del parámetro What-if, simula alza de precio                       |

---

