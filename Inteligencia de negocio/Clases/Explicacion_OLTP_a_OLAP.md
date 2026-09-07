# De OLTP a OLAP: Modelado Dimensional para Inteligencia de Negocios

Este documento explica en detalle el contenido de las dos presentaciones subidas:

1. **De OLTP a OLAP 2** — Caso Retail «Casa Norte» (2 tablas de hecho)
2. **De un MER a un Modelo Dimensional** — Caso Empresa de Energía «Energía Sur»

---

# PARTE 1 · Caso Retail «Casa Norte»

## Agenda de la presentación

La presentación se organiza en 6 bloques:

1. El caso de negocio
2. Modelo relacional (OLTP)
3. Procesos de negocio a analizar
4. Paso a paso: los 4 pasos de Kimball
5. Qué entidad es hecho, dimensión o se descarta
6. Modelo dimensional final y matriz bus

## 1. El caso de negocio: Retail «Casa Norte»

### Contexto
Casa Norte es una cadena de **42 tiendas** de mejoramiento del hogar más un **canal online**, con **3 centros de distribución** y aproximadamente **35.000 SKU** (referencias de producto).

Hoy la operación corre sobre un **ERP relacional normalizado (OLTP)**: excelente para registrar transacciones, pero muy lento para analizar.

### Dolores del negocio (problemas actuales)
- **Dolor 1:** Los informes de venta se arman en Excel y tardan **3 días**.
- **Dolor 2:** No hay visión única del **margen por categoría y tienda**.
- **Dolor 3:** Los **quiebres de stock** se detectan tarde, sin medir su costo.

### Objetivo
Construir un **data warehouse dimensional** que responda en **segundos**.

## 2. OLTP vs. OLAP: por qué convertir

| OLTP · Modelo relacional | OLAP · Modelo dimensional |
|---|---|
| Objetivo: registrar la operación | Objetivo: analizar el negocio |
| Altamente normalizado (3FN) | Desnormalizado (esquema estrella) |
| Muchas tablas, muchos JOIN | Pocas tablas, JOIN directos |
| Datos actuales, se sobrescriben | Guarda historia (SCD) |
| Optimizado para INSERT/UPDATE | Optimizado para lectura y agregación |
| Consulta analítica = lenta y costosa | Consulta analítica = segundos |

## 3. Paso 0 · El modelo relacional de origen

El ERP entregado por TI tiene **14 tablas principales**:

- **CLIENTE**: id, rut, nombre, comuna
- **PRODUCTO**: sku, desc, marca, costo
- **CATEGORIA**: id, nombre, línea
- **TIENDA**: id, nombre, región
- **EMPLEADO**: id, nombre, cargo
- **BOLETA**: folio, fecha, tienda, cliente
- **DETALLE_BOLETA**: folio, sku, cantidad, precio
- **MEDIO_PAGO**: id, tipo
- **PROVEEDOR**: rut, nombre
- **ORDEN_COMPRA**: id, prov, fecha
- **DET_ORDEN_COMPRA**: id, sku, cantidad
- **STOCK_DIARIO**: fecha, sku, tienda, unid
- **USUARIO_SISTEMA**: login, hash, rol (tabla técnica, sin valor analítico)
- **LOG_AUDITORIA**: id, tabla, timestamp (tabla técnica, sin valor analítico)

## 4. ¿Quién es Ralph Kimball?

**Ralph Kimball (1944–2025)**: Doctor en Ingeniería Eléctrica por Stanford. Trabajó en **Xerox PARC** (fue parte del equipo del **Xerox Star**) y luego fundó **Red Brick Systems** y **Kimball Group**.

Es el autor de **«The Data Warehouse Toolkit»**, la obra de referencia del modelado dimensional, y el creador de la metodología que hoy lleva su nombre.

### Sus aportes clave
- **Enfoque bottom-up:** el DW se construye por incrementos: se parte por el proceso de negocio de mayor valor y se van sumando data marts.
- **Modelo dimensional:** hechos + dimensiones en esquema estrella, pensado para que un usuario de negocio entienda el modelo sin ayuda de TI.
- **Arquitectura bus:** dimensiones conformadas que integran todos los data marts en un mismo DW; es la alternativa práctica al modelo normalizado de **Bill Inmon**.
- **Legado:** sus 4 pasos y sus reglas de diseño siguen siendo el estándar de facto en proyectos de BI en todo el mundo.

## 5. Los 4 pasos de Kimball, en detalle

> El orden importa: cada paso condiciona al siguiente, y saltárselo es la causa más común de un DW que nadie usa.

### Paso 1 — Elegir el proceso de negocio
Identificar un evento operativo medible y relevante (una venta, un despacho, una atención).
- Se elige por valor para el negocio y por disponibilidad de datos.
- **Un proceso = una tabla de hecho.** NO se modela por departamento ni por informe.
- En el caso: **Venta** y **Reposición/Inventario**.

### Paso 2 — Declarar la granularidad
Definir exactamente qué representa **UNA fila** del hecho, antes de seguir.
- Siempre al grano más atómico disponible: da máxima flexibilidad de análisis.
- **Un grano por tabla:** mezclar granos rompe las agregaciones.
- En el caso: **línea de boleta**; y **producto-tienda-día**.

### Paso 3 — Identificar las dimensiones
Preguntar «¿cómo describe el negocio este evento?»: quién, qué, dónde, cuándo, cómo.
- Las dimensiones caen naturalmente del grano declarado.
- Se desnormalizan con sus jerarquías y se conforman entre procesos.
- En el caso: **tiempo, producto, tienda, cliente, medio de pago…**

### Paso 4 — Identificar los hechos (medidas)
Definir las medidas numéricas que son consistentes con el grano.
- Preferir medidas aditivas; marcar las semi-aditivas (stock) y evitar razones precalculadas.
- Incluir dimensiones degeneradas útiles (nro. de boleta).
- En el caso: **unidades, monto, margen; stock y días de quiebre.**

> **Regla de oro:** nunca elegir dimensiones o medidas antes de haber declarado el grano.

## 6. Paso 1 · Elegir los procesos de negocio

Un proceso de negocio es un evento medible que la empresa ejecuta repetidamente. Cada proceso genera **UNA tabla de hecho**.

### Proceso A · VENTA → `fact_ventas`
- Evento: se emite una boleta y se vende un producto.
- Mide ingresos, unidades, descuento y margen.
- Responde: ¿qué vendemos, dónde, a quién y cuánto ganamos?

### Proceso B · REPOSICIÓN E INVENTARIO → `fact_inventario_diario`
- Evento: fotografía diaria del stock por producto y tienda.
- Mide unidades disponibles, en tránsito y días de quiebre.
- Responde: ¿dónde falta stock y cuánto nos cuesta?

## 7. Paso 2 · Declarar la granularidad

El grano es la respuesta a «¿qué representa una fila de la tabla de hecho?». Se declara **ANTES** de elegir dimensiones y medidas.

### `fact_ventas`
Una fila = **una línea de detalle de boleta** (un SKU dentro de una boleta).

Grano atómico: el máximo detalle disponible. Nunca partir de datos ya agregados: si guardamos «venta diaria por tienda» perdemos la capacidad de analizar por producto o cliente.

### `fact_inventario_diario`
Una fila = **un producto, en una tienda, en un día**.

Hecho de snapshot periódico: no registra transacciones sino un estado. Sus medidas (unidades en stock) son **semi-aditivas**: se suman por producto y tienda, pero **NO por tiempo**.

## 8. Cómo definir la granularidad · tips y ejemplos

**Método en una frase:** completa «una fila de esta tabla de hecho representa ______» hasta que la respuesta no admita dudas.

1. **Ve al evento, no al informe:** pregunta qué ocurre en el mundo real que el sistema registra: una línea de boleta, un escaneo, una consulta médica.
2. **Siempre al nivel más atómico:** si guardas el detalle, después puedes agregar. Si guardas agregado, el detalle se perdió para siempre.
3. **Un solo grano por tabla:** mezclar «venta por línea» con «venta por boleta» en la misma tabla duplica los montos al sumar.
4. **Descríbelo en lenguaje de negocio:** si un gerente no entiende la frase del grano, el modelo tampoco lo entenderá nadie más.
5. **Verifica con las dimensiones:** cada dimensión debe aplicar a TODA fila. Si una no aplica siempre, el grano está mal declarado.
6. **Verifica con las medidas:** toda medida debe ser válida a ese nivel. Un total mensual no cabe en una fila de detalle.

### ✘ Granos mal declarados
- «Una fila = una venta» → ¿la boleta completa o el producto?
- «Una fila = un cliente» → eso es una dimensión, no un evento.
- «Una fila = venta mensual por tienda» → ya viene agregado.

### ✓ Granos bien declarados
- «Una fila = un SKU dentro de una boleta» (transaccional)
- «Una fila = un producto, en una tienda, en un día» (snapshot)
- «Una fila = un despacho entregado a un cliente» (evento)

## 9. Las preguntas que debe responder el grano

Un grano bien declarado contesta estas preguntas sin ambigüedad. Cada respuesta anticipa una dimensión del modelo.

| Pregunta | Descripción | Ejemplo | Dimensión resultante |
|---|---|---|---|
| **¿QUÉ ocurrió?** | El evento que se registra | Se vendió un producto · Se registró el stock · Se despachó un pedido | `dim_producto` |
| **¿CUÁNDO ocurrió?** | El momento exacto y su nivel de detalle: ¿día, hora, minuto? | El 12-08 a las 19:42 · El día 12-08 (cierre diario) | `dim_tiempo` · `dim_hora` |
| **¿DÓNDE ocurrió?** | El lugar físico o el canal | Tienda La Serena · Bodega CD Norte · Canal online | `dim_tienda` · `dim_canal` |
| **¿QUIÉN participó?** | Los actores del evento | El socio Juan Pérez · El vendedor · El proveedor | `dim_cliente` · `dim_vendedor` |
| **¿CÓMO ocurrió?** | La forma o modalidad en que se ejecutó | Pagó con débito en 3 cuotas · Compra con retiro en tienda | `dim_medio_pago` · `dim_modalidad` |
| **¿CUÁNTO se midió?** | Las magnitudes numéricas asociadas a ese evento | 3 unidades · $24.990 · 15% de descuento | medidas del hecho |

> Si alguna respuesta es «depende» o «a veces», el grano todavía no está declarado: aún hay dos eventos distintos mezclados.

## 10. Paso 3 y 4 · Criterio: ¿hecho, dimensión o descarte?

### HECHO
La entidad registra un **EVENTO** con fecha y con valores numéricos que se suman.
- Señales: tabla transaccional, crece sin parar, tiene cantidades e importes, muchas claves foráneas.

### DIMENSIÓN
La entidad describe el **CONTEXTO** del evento: quién, qué, dónde, cuándo, cómo.
- Señales: tabla maestra, pocos registros, atributos de texto usados para filtrar y agrupar.

### SE DESCARTA
La entidad no aporta al análisis del negocio.
- Señales: tablas técnicas o de seguridad, catálogos que se absorben en otra dimensión, datos redundantes o sin usuario analítico.

## 11. Decisión entidad por entidad

| Entidad OLTP | Decisión | Justificación |
|---|---|---|
| DETALLE_BOLETA + BOLETA | → `fact_ventas` | Evento transaccional con cantidad y precio: es el hecho. La cabecera aporta fecha, tienda y cliente. |
| STOCK_DIARIO | → `fact_inventario_diario` | Estado medible en el tiempo: snapshot periódico, segundo hecho. |
| PRODUCTO + CATEGORIA | → `dim_producto` | Descriptivo. CATEGORIA se desnormaliza dentro del producto: jerarquía línea→categoría→marca→SKU. |
| TIENDA | → `dim_tienda` | Contexto del «dónde», con jerarquía región→comuna→tienda. |
| CLIENTE | → `dim_cliente` | Contexto del «quién». Se anonimiza el RUT y se aplica SCD tipo 2 en comuna. |
| MEDIO_PAGO | → `dim_medio_pago` | Dimensión pequeña, útil para segmentar la venta. |
| EMPLEADO | → `dim_vendedor` | Solo atributos analíticos (cargo, tienda); se excluyen sueldo y datos sensibles. |
| PROVEEDOR | → `dim_proveedor` | Compartida por el hecho de inventario/reposición. |
| ORDEN_COMPRA / DET_ORDEN_COMPRA | ✕ Fuera del alcance | Sería un tercer hecho (compras). No es uno de los 2 procesos priorizados en esta fase. |
| USUARIO_SISTEMA | ✕ Se descarta | Tabla técnica de seguridad, sin valor de negocio. |
| LOG_AUDITORIA | ✕ Se descarta | Registro operativo de auditoría; volumen enorme y sin métrica analítica. |

## 12. Modelo estrella · `fact_ventas`

**Tabla de hechos:**
`fact_ventas`
- Grano: línea de boleta
- Medidas: unidades · monto_neto · descuento · costo · margen
- Degenerada: nro_boleta

**Dimensiones conectadas:**
- `dim_tiempo`: fecha, mes, trimestre, año, feriado
- `dim_producto`: SKU, marca, categoría, línea
- `dim_cliente`: segmento, comuna (SCD2)
- `dim_tienda`: tienda, comuna, región, formato
- `dim_medio_pago`: efectivo, débito, crédito, cuotas
- `dim_vendedor`: vendedor, cargo, turno

## 13. Modelo estrella · `fact_inventario_diario`

**Tabla de hechos:**
`fact_inventario_diario`
- Grano: producto/tienda/día
- Medidas: unidades_stock (semi-aditiva) · unidades_en_transito · costo_inventario · dias_quiebre

**Dimensiones conectadas:**
- `dim_tiempo`: conformada con ventas
- `dim_producto`: conformada con ventas
- `dim_proveedor`: proveedor, lead time
- `dim_tienda`: conformada con ventas
- `dim_bodega`: CD, tienda, tipo de bodega
- `dim_estado_stock`: normal, crítico, quiebre

## 14. Matriz bus: dimensiones conformadas

Compartir las mismas dimensiones entre ambos hechos permite cruzar venta e inventario (ej. venta perdida por quiebre).

| Proceso / Dimensión | Tiempo | Producto | Tienda | Cliente | Medio pago | Vendedor | Proveedor | Bodega |
|---|---|---|---|---|---|---|---|---|
| Ventas | X | X | X | X | X | X | | |
| Inventario diario | X | X | X | | | | X | X |

- **Conformadas:** Tiempo, Producto y Tienda tienen la misma clave y los mismos atributos en ambos hechos.
- **Beneficio:** un solo filtro «Región = Norte» aplica simultáneamente a venta e inventario.
- **Regla:** nunca duplicar una dimensión por proceso: se diseña una vez y se reutiliza.

## 15. ¿Un solo DW o dos? · Arquitectura bus

> Respuesta corta: **UN SOLO data warehouse.** Dos procesos de negocio ⇒ dos tablas de hecho dentro del mismo DW, nunca dos DW separados.

### ✓ UN DW con arquitectura bus
Ambos hechos viven en el mismo DW y comparten dim_tiempo, dim_producto y dim_tienda.
- Una sola verdad: mismo SKU, misma tienda y misma fecha en todo el negocio.
- Permite drill-across: cruzar venta e inventario en un mismo informe.
- Un solo ETL, un solo modelo de seguridad, menor costo.
- Escalable: mañana se agrega fact_compras sin rediseñar nada.

### ✘ DOS DW separados
Cada proceso con su propio almacén y sus propias dimensiones.
- Dimensiones duplicadas y desalineadas (silos o «stovepipes»).
- Imposible cruzar venta con stock de forma confiable.
- Doble ETL, doble mantención, doble costo.
- Solo se justifica por razones legales o geográficas extremas.

## 16. Cómo quedan relacionadas: constelación de hechos

Los hechos **NO se relacionan entre sí directamente**: se conectan a través de las dimensiones conformadas que comparten.

- `fact_ventas` — Grano: línea de boleta — Medidas: unidades · monto_neto · costo · margen
- `fact_inventario_diario` — Grano: producto/tienda/día — Medidas: unidades_stock · dias_quiebre

**Dimensiones conformadas (compartidas):**
- `dim_tiempo`: fecha, mes, trimestre, año
- `dim_producto`: SKU, marca, categoría, línea
- `dim_tienda`: tienda, comuna, región

**Dimensiones exclusivas de ventas:** `dim_cliente` · `dim_medio_pago` · `dim_vendedor`

**Dimensiones exclusivas de inventario:** `dim_proveedor` · `dim_bodega` · `dim_estado_stock`

> **Drill-across:** se consulta cada hecho por separado al mismo nivel de dimensión conformada y luego se combinan los resultados; nunca con un JOIN directo entre hechos, que duplicaría las medidas.

## 17. ¿Entonces son data marts por área?

Sí: cada tabla de hecho con sus dimensiones forma un data mart orientado a un área. Pero son data marts **DENTRO** del mismo DW, no almacenes independientes.

### Data mart COMERCIAL — `fact_ventas`
- Área: Comercial y Marketing.
- Preguntas: ¿qué se vende, dónde, a quién y con qué margen?
- KPI: venta neta, ticket promedio, margen %, mix por categoría.

### Data mart OPERACIONES — `fact_inventario_diario`
- Área: Supply Chain y Tiendas.
- Preguntas: ¿dónde falta stock y cuánto cuesta?
- KPI: quiebre %, días de inventario, rotación, stock valorizado.

### La clave
Los data marts NO se construyen aislados: se implementan sobre el mismo DW y comparten las dimensiones conformadas. Así Comercial y Operaciones hablan del mismo producto, la misma tienda y la misma fecha.

- **Vista de área:** cada gerencia consume «su» data mart y ve solo lo que necesita.
- **Vista corporativa:** BI cruza ambos marts: venta perdida por quiebre, margen vs. rotación.
- **Riesgo a evitar:** data marts independientes = silos: mismas preguntas con cifras distintas.

## 18. Ejercicio en clase · Caso «Gimnasio Vitalis»

### El caso
Vitalis opera **15 sucursales** de gimnasio en Chile. Vende planes mensuales y anuales a sus socios, y cada socio registra su entrada en el torniquete cada vez que asiste.

La gerencia quiere saber qué planes dejan más ingreso y, sobre todo, qué relación hay entre **asistencia** y **renovación de plan** (los socios que dejan de ir se dan de baja).

### Tablas del sistema operacional (OLTP)
- **SOCIO** (rut, nombre, comuna, fecha_ingreso)
- **PLAN** (id, nombre, duración, precio)
- **SUCURSAL** (id, nombre, ciudad)
- **CONTRATO** (id, socio, plan, sucursal, fecha, monto)
- **ACCESO_TORNIQUETE** (socio, sucursal, fecha_hora)
- **INSTRUCTOR** (id, nombre, especialidad)
- **CLASE** (id, tipo, instructor, horario)
- **EQUIPO_MAQUINA** (id, marca, fecha_compra)
- **USUARIO_APP** (login, password_hash)

### Preguntas guía para el ejercicio (pasos 1 y 2)
- **Paso 1:** ¿Cuáles son los 2 procesos de negocio de Vitalis? (pista: busca eventos que se repiten y se pueden medir).
- **Paso 2:** ¿Cuál es la granularidad de cada tabla de hecho? Completa: «una fila = ______». Trampa frecuente: confundir un informe («ventas por sucursal») con un proceso de negocio.

### Preguntas guía para el ejercicio (pasos 3 y 4)
- **Paso 3:** ¿Qué dimensiones describen cada evento? ¿Cuáles serían conformadas entre ambos hechos?
- **Paso 4:** ¿Qué medidas numéricas guardarías? ¿Alguna es semi-aditiva o degenerada?
- **Pregunta bonus:** ¿qué tablas del OLTP dejarías fuera y por qué?

## 19. Resultados del ejercicio · Los 4 pasos aplicados a Vitalis

### 1. Procesos de negocio
- Contratación / renovación de plan → `fact_contratos`
- Asistencia al gimnasio → `fact_accesos`

Ambos en un mismo DW, unidos por dimensiones conformadas.

### 2. Granularidad
- `fact_contratos`: una fila = un contrato de un socio a un plan, en una sucursal y fecha.
- `fact_accesos`: una fila = un ingreso de un socio por el torniquete (evento atómico).

### 3. Dimensiones
- **Conformadas:** `dim_tiempo`, `dim_socio`, `dim_sucursal`.
- **Solo contratos:** `dim_plan`, `dim_canal_venta`.
- **Solo accesos:** `dim_hora_del_dia`, `dim_tipo_actividad`.
- **Se descartan:** EQUIPO_MAQUINA, USUARIO_APP (mantención y seguridad, sin valor analítico). INSTRUCTOR y CLASE quedan para un tercer proceso futuro.

### 4. Hechos (medidas)
- `fact_contratos`: monto_contrato, descuento, meses_plan, flag_renovacion. Degenerada: nro_contrato.
- `fact_accesos`: contador_visita (=1), minutos_estadía. El «socios activos» es semi-aditivo: no se suma en el tiempo.

> **Cruce de valor:** asistencia (fact_accesos) vs. renovación (fact_contratos) por socio y mes, usando las dimensiones conformadas.

## 20. En síntesis (cierre de la Parte 1)

1. Se priorizaron 2 procesos: **Venta** y **Reposición/Inventario** → 2 tablas de hecho.
2. El grano se declaró primero: **línea de boleta** y **snapshot diario producto-tienda**.
3. Las tablas maestras se convirtieron en dimensiones desnormalizadas con jerarquías.
4. Se descartaron tablas técnicas (usuarios, auditoría) y se dejó Compras para una fase 2.
5. Las dimensiones conformadas permiten analizar ambos procesos con un mismo lenguaje.

---

# PARTE 2 · Caso Empresa de Energía «Energía Sur»

## Título de la clase
**De un MER a un Modelo Dimensional**
Caso aplicado: Empresa de Energía «Energía Sur» — Clase práctica de Inteligencia de Negocios.

## 1. El objetivo: convertir datos en preguntas respondibles

- **Competencia:** transformar un modelo operacional normalizado en un modelo dimensional orientado al análisis.
- El modelo dimensional organiza los datos en **hechos medibles** y **dimensiones descriptivas**.
- La ruta de trabajo será: **preguntas de negocio → proceso → grano → hechos → dimensiones → métricas → validación**.

> **Idea clave:** no se comienza dibujando tablas; se comienza entendiendo qué decisión debe apoyar el modelo.

## 2. MER y modelo dimensional responden a necesidades distintas

| Modelo entidad–relación (MER) | Modelo dimensional |
|---|---|
| Registra operaciones y mantiene integridad transaccional. | Facilita análisis, filtros, agrupaciones y tendencias. |
| Normaliza entidades para reducir redundancia. | Prioriza una estructura clara para consultar y resumir. |
| Sigue relaciones del proceso operativo. | Centra el análisis en hechos y sus dimensiones. |

En **Energía Sur**, el MER distribuye la información entre clientes, medidores, lecturas, consumo, facturas, pagos e interrupciones. El modelo dimensional debe reorganizarla alrededor de eventos que la gerencia quiera medir.

## 3. Paso 1: traducir la necesidad gerencial a preguntas

| Necesidad | Pregunta analítica |
|---|---|
| Consumo por zona | ¿Cuántos kWh se consumen por zona, mes y tipo de cliente? |
| Tipos de clientes | ¿Cómo cambia el consumo entre clientes residenciales, comerciales e industriales? |
| Evolución mensual | ¿Cuál es la tendencia del consumo y su variación mes a mes? |
| Facturación y pagos | ¿Cuánto se factura, cuánto se recauda y cuál es la morosidad? |
| Interrupciones | ¿Cuántos cortes ocurren y cuánto duran por zona? |

> **Decisión de alcance para el ejercicio:** comenzar con el proceso de **consumo energético** y después extender el modelo a facturación, pagos e interrupciones.

## 4. Paso 2: elegir el proceso principal: consumo energético

El proceso principal seleccionado es **registrar y analizar el consumo de energía por medidor**.

**Cadena del proceso:** Medidor → LecturaMedidor → Consumo

El evento analítico es la lectura que permite calcular o registrar los kWh consumidos durante un periodo. Cliente, instalación, dirección, zona, tarifa y tiempo aportan el contexto para analizar ese evento.

> **Por qué no elegir "toda la empresa" como un único hecho:** consumo, facturación, pagos e interrupciones son eventos distintos. Mezclarlos produciría duplicaciones y una granularidad ambigua.

## 5. Paso 3: declarar el grano antes de diseñar

**Grano propuesto:** una fila de `FactConsumo` representa el consumo registrado para un medidor, una instalación y una fecha o periodo de lectura.

El grano debe ser atómico y único. Si se agregan filas mensuales junto con filas diarias en la misma tabla, se mezclan niveles de detalle y las sumas pueden duplicarse.

| Elemento | Decisión para Energía Sur |
|---|---|
| Evento | Lectura/registro de consumo |
| Nivel temporal | Día de lectura y periodo de consumo |
| Entidad medida | Medidor asociado a una instalación |
| Unidad principal | kWh consumidos |
| Clave candidata | Medidor + fecha_lectura + periodo |

## 6. Paso 4: diseñar la tabla de hechos `FactConsumo`

| Columna | Tipo | Propósito |
|---|---|---|
| sk_fecha | Clave foránea | Conecta con DimTiempo |
| sk_cliente | Clave foránea | Permite analizar por cliente y segmento |
| sk_instalacion | Clave foránea | Permite analizar el punto de suministro |
| sk_medidor | Clave foránea | Identifica el equipo que registró la lectura |
| sk_zona | Clave foránea | Permite comparar zonas de distribución |
| sk_tarifa | Clave foránea | Permite analizar el plan tarifario |
| lectura_actual | Medida base | Lectura acumulada al momento del registro |
| lectura_anterior | Medida base | Lectura de referencia |
| kwh_consumidos | Medida aditiva | Energía consumida en el grano definido |
| cantidad_lecturas | Medida técnica | Valor 1 para contar registros válidos |

> **Clave primaria técnica sugerida:** sk_fecha + sk_medidor + periodo, o una clave sustituta de hecho más una restricción de unicidad.

## 7. Paso 5: transformar entidades en dimensiones

| Entidades del MER | Dimensión propuesta | Atributos analíticos |
|---|---|---|
| Cliente + TipoCliente | `DimCliente` | nombre, tipo_cliente, segmento |
| Dirección + ZonaDistribución | `DimUbicacion` | calle, comuna, ciudad, región, zona |
| Instalación | `DimInstalacion` | fecha_instalacion, estado, cliente, ubicación |
| Medidor | `DimMedidor` | numero_medidor, modelo, instalación |
| Tarifa | `DimTarifa` | nombre_tarifa, valor_kwh, tipo_cliente |
| Fecha de lectura / periodo | `DimTiempo` | día, mes, trimestre, semestre, año, semana |

> **Regla práctica:** las dimensiones describen y permiten filtrar o agrupar; no deben contener las métricas principales del evento.

> **Observación de integración:** el MER no muestra id_zona en Instalación/Dirección ni id_tarifa en Consumo/Lectura. Para que esas dimensiones sean analizables, el proceso ETL debe derivar la relación desde una fuente confiable o solicitarla al sistema operacional.

## 8. Paso 6: crear una DimTiempo reutilizable

| Atributo | Ejemplo |
|---|---|
| sk_fecha | 20260825 |
| fecha | 25-08-2026 |
| día | 25 |
| mes | 8 |
| nombre_mes | Agosto |
| trimestre | T3 |
| semestre | S2 |
| año | 2026 |
| semana | 35 |

La clave sustituta **sk_fecha** facilita relaciones estables y permite que una misma dimensión de fecha sea reutilizada por consumo, facturación, pagos e interrupciones.

Se recomienda ordenar *nombre_mes* por *mes* y definir jerarquías como: **Año → Trimestre → Mes → Día**

## 9. Paso 7: ensamblar el esquema estrella

**Tabla central:** `FactConsumo`

**Dimensiones conectadas:** `DimTiempo`, `DimCliente`, `DimInstalacion`, `DimMedidor`, `DimUbicacion` y `DimTarifa`.

Esquema (diagrama descrito):
```
DimTiempo (fecha, mes, trimestre, año, semana)
DimCliente (tipo, segmento)
DimInstalacion (estado, fecha instalación)      →  FactConsumo
DimMedidor (número, modelo)                       Grano: medidor + fecha/periodo
DimUbicacion (comuna, ciudad, región, zona)        kWh, lecturas
DimTarifa (nombre, valor kWh)
```

La tabla de hechos conserva claves y medidas; las dimensiones aportan el contexto. Las relaciones esperadas son **uno a muchos** desde cada dimensión hacia FactConsumo.

## 10. Paso 8: convertir preguntas en métricas

| Pregunta de negocio | Medida o cálculo |
|---|---|
| ¿Cuánto consumo hubo? | SUM(FactConsumo[kwh_consumidos]) |
| ¿Cuál es el consumo promedio por lectura? | AVERAGE(FactConsumo[kwh_consumidos]) |
| ¿Cuántas lecturas válidas se registraron? | SUM(FactConsumo[cantidad_lecturas]) |
| ¿Cuál es el consumo por cliente? | Consumo total / DISTINCTCOUNT(DimCliente[id_cliente]) |
| ¿Cómo varía el consumo mes a mes? | (Consumo actual − Consumo anterior) / Consumo anterior |
| ¿Cuál es el costo energético estimado? | SUM(kwh_consumidos × valor_kwh) |

### Ejemplos de lectura del modelo
- Filtrar `DimUbicacion[zona]` permite analizar el consumo por zona.
- Agrupar por `DimTiempo[nombre_mes]` muestra la evolución mensual.
- Segmentar por `DimCliente[tipo_cliente]` compara residenciales, comerciales e industriales.

## 11. Una empresa, varios procesos: no mezclar granos

Para responder todo el caso, se recomienda una **constelación de hechos** con tablas separadas:

| Proceso | Tabla de hechos | Grano sugerido | Medidas ejemplo |
|---|---|---|---|
| Consumo | `FactConsumo` | Un medidor por fecha/periodo | kWh, lecturas |
| Facturación | `FactFactura` | Una factura por cliente | monto_total, saldo |
| Pagos | `FactPago` | Un pago por factura y fecha | monto_pagado, cantidad_pagos |
| Interrupciones | `FactInterrupcion` | Un corte por instalación | duración_horas, cantidad_cortes |

Cada hecho puede compartir dimensiones conformadas como `DimTiempo`, `DimCliente` y `DimUbicacion`. El desafío es justificar el grano de cada proceso y evitar sumar hechos de distinta naturaleza como si fueran equivalentes.

> **Limitación del MER:** Técnico no está relacionado con una entidad de actividad técnica. Para analizar desempeño de técnicos se requiere una entidad adicional, por ejemplo `ActividadTecnica`.

## 12. Cierre: del evento operativo a la decisión

### Secuencia que debe recordar
1. Formular preguntas de negocio.
2. Elegir un proceso medible.
3. Declarar el grano en una frase.
4. Diseñar la tabla de hechos con claves y medidas.
5. Convertir entidades descriptivas en dimensiones.
6. Crear métricas y validar que respondan las preguntas.
7. Separar procesos cuando sus granos sean diferentes.

### Producto esperado del ejercicio
Un esquema estrella, el diccionario de columnas, la dimensión tiempo, al menos cinco medidas y una justificación escrita de las decisiones.

### Referencias citadas
1. Microsoft Learn, «Comprender el esquema de estrella y su importancia para Power BI»
2. Ralph Kimball, «Keep to the Grain in Dimensional Modeling»
3. Databricks, «¿Qué es el esquema en estrella?»

> **Frase de cierre:** Un buen modelo dimensional no solo organiza tablas; hace explícita la forma en que la empresa mide su negocio.

---

# Comparación entre ambos casos

Ambas presentaciones enseñan la **misma metodología de Kimball** (4 pasos: proceso → grano → dimensiones → hechos), pero aplicada a dos industrias distintas:

| Aspecto | Casa Norte (Retail) | Energía Sur (Energía) |
|---|---|---|
| Punto de partida | Modelo relacional OLTP (14 tablas de un ERP) | MER (clientes, medidores, lecturas, consumo, facturas, pagos, interrupciones) |
| Procesos priorizados | Venta y Reposición/Inventario | Consumo energético (con extensión futura a facturación, pagos e interrupciones) |
| Tabla(s) de hecho | `fact_ventas`, `fact_inventario_diario` | `FactConsumo` (y futuras: `FactFactura`, `FactPago`, `FactInterrupcion`) |
| Grano principal | Línea de boleta / producto-tienda-día | Medidor + fecha/periodo de lectura |
| Dimensiones conformadas | Tiempo, Producto, Tienda | Tiempo, Cliente, Ubicación |
| Arquitectura resultante | Constelación de hechos dentro de un único DW (arquitectura bus) | Esquema estrella que se extenderá a constelación de hechos |
