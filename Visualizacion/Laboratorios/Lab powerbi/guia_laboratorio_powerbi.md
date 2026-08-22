# Guía de Trabajo — Laboratorio Power BI (EIN092B)

**Fecha de entrega:** 21 de agosto (envío de archivos hasta las 23:59 del 26 de agosto, solo si la actividad quedó marcada como revisada en sesión)
**Entrega:** AulaUSM
**Penalización por atraso:** -15% si no se entrega en la sesión correspondiente

---

## 0. Resumen ejecutivo: qué hay que entregar

1. **Archivo `.pbix` final** con el proyecto completo.
2. **Documento PDF breve** que explique:
   - Decisiones de modelado.
   - Principales transformaciones en Power Query.
   - Medidas DAX desarrolladas.
   - Implementación de RLS.

Y durante la **sesión de laboratorio**, cada actividad debe mostrarse al staff (profesor/ayudante), quien hará preguntas conceptuales antes de marcarla como revisada. **Sin esa marca, no hay puntaje aunque el archivo esté entregado.**

---

## 1. Antes de empezar: conceptos que hay que manejar

Estos conceptos son la base teórica que sustenta cada actividad. Se resumen aquí porque el staff puede preguntarlos en la revisión — no basta con "hacer clic en los botones correctos", hay que poder explicar el porqué.

### 1.1 Business Intelligence (BI) y flujo de trabajo en Power BI

BI es el proceso de transformar datos crudos en información útil para decisiones. Power BI es una herramienta de **self-service BI** (no depende de un equipo de TI especializado) y sigue 4 etapas:

1. **Obtención de datos** (Excel, SQL Server, CSV, web).
2. **Transformación (ETL)** vía Power Query.
3. **Modelado semántico**: tablas, relaciones y medidas.
4. **Visualización y consumo**: reportes y dashboards.

El **modelo semántico** (antes llamado *dataset*) es la pieza central: conecta los datos transformados con las visualizaciones. Un modelo mal diseñado da resultados incorrectos aunque el dashboard se vea bien.

### 1.2 Modelado dimensional (esquema estrella)

- **Tablas de hechos (fact tables):** transacciones/eventos medibles (ventas, montos). Muchas filas.
- **Tablas de dimensiones:** atributos descriptivos para filtrar/agrupar (productos, clientes, fechas, regiones).
- **Esquema estrella:** las dimensiones se conectan directo a la tabla de hechos (recomendado). El **esquema copo de nieve** normaliza las dimensiones en subtablas — menos recomendado en Power BI por rendimiento.
- **Cardinalidad:** cuántas coincidencias hay entre dos tablas relacionadas. La relación **uno a muchos** desde dimensión → hechos es la más común.
- **Dirección del filtro:** si el filtro se propaga en un solo sentido (*single*) o en ambos (*bidirectional*). El filtrado bidireccional puede generar ambigüedades si se usa sin criterio.

### 1.3 Power Query y lenguaje M

Cada transformación que se hace en la interfaz gráfica de Power Query genera código en lenguaje **M** (funcional) automáticamente. Cada transformación queda registrada como un **paso (applied step)**, formando un historial reproducible y editable.

Transformaciones típicas: tipado de columnas, eliminación de duplicados/filas vacías, normalización de nombres, columnas calculadas simples, filtrado. Hacerlo en Power Query (y no en el modelo) mantiene el modelo liviano.

### 1.4 DAX (Data Analysis Expressions)

- **Columnas calculadas:** se calculan fila por fila, quedan almacenadas físicamente (ocupan memoria).
- **Medidas:** se calculan dinámicamente según el contexto de filtro activo (slicers, filtros de página). Son la forma preferida de construir KPIs porque no aumentan el tamaño del modelo.
- **Contexto de fila** vs **contexto de filtro**: el primero aplica al evaluar fila por fila (columnas calculadas); el segundo es el conjunto de filtros activos al evaluar una medida.
- **`CALCULATE()`** es la función más importante: modifica el contexto de filtro. Es la base de `ALL()`, `ALLSELECTED()`, `FILTER()`.

### 1.5 Parámetros What-if y análisis de sensibilidad

Un parámetro What-if genera una **tabla desconectada** del modelo (sin relaciones), cuyo único propósito es alimentar una medida vía `SELECTEDVALUE()`. Es un caso particular del **análisis de sensibilidad**:

- **Análisis de una variable:** lo que construye un parámetro What-if estándar.
- **Análisis de escenarios discretos:** comparar escenarios predefinidos (pesimista/base/optimista).
- **Análisis multivariable:** efecto combinado de 2+ variables (requiere combinar varios What-if o visuales tipo *tornado chart*).

Importante: un What-if **no reemplaza** una medida existente, crea una variable nueva que se combina con medidas ya definidas.

### 1.6 KPIs

Un KPI es una medida cuantificable ligada a un objetivo de negocio. Se evalúa con el marco **SMART** (específico, medible, alcanzable, relevante, acotado en el tiempo). Un buen KPI casi siempre tiene 3 componentes:

- **Valor actual.**
- **Objetivo (target).**
- **Estado/tendencia** (color, ícono, flecha).

Distinción útil: **indicadores adelantados** (leading, anticipan resultados) vs **rezagados** (lagging, miden resultados pasados). Evitar **vanity metrics** (se ven bien pero no informan decisiones).

### 1.7 Principios de diseño de dashboard

- **Jerarquía visual:** lo más importante en el lugar de mayor atención; el resto vía drill-down/tooltips.
- **Consistencia:** mismos colores/tipografías/escalas entre páginas.
- **Interactividad con propósito:** slicers que ayudan, no que saturan.
- **Elección del gráfico adecuado** según el tipo de relación a comunicar (tendencia, comparación, correlación, distribución geográfica).

### 1.8 Seguridad: RLS (Row Level Security)

RLS define **roles**, cada uno con una expresión DAX que filtra las filas visibles según el usuario.

- **RLS estático:** filtro fijo (`[Region] = "Norte"`). Simple pero escala mal.
- **RLS dinámico:** se calcula según quién consulta, típicamente con `USERPRINCIPALNAME()` + `LOOKUPVALUE()` sobre una tabla de mapeo usuario–categoría. Recomendado cuando hay muchos perfiles.

Dos comportamientos clave:

- **Los roles son aditivos, no restrictivos entre sí:** si un usuario pertenece a 2 roles, ve la **unión** de ambos, no la intersección.
- **RLS depende de la dirección del filtro del modelo:** el filtro se propaga siguiendo la dirección configurada en las relaciones; si es de un solo sentido y RLS necesita el sentido contrario, puede requerirse filtrado bidireccional (evaluando impacto en rendimiento).

Concepto relacionado (no se implementa en este lab): **OLS (Object Level Security)** — oculta tablas/columnas completas en vez de filas.

**Power BI Desktop vs Power BI Service:** el laboratorio se hace mayormente en Desktop (autoría). En un flujo real se publica en el **Service** (nube), donde se configuran actualizaciones automáticas (*scheduled refresh*) y *gateways*. No confundir los **roles de RLS** (qué filas ve cada usuario) con los **roles del workspace** (Visor/Colaborador/Miembro/Administrador — qué puede hacer cada usuario con el reporte).

---

## 2. Elección del dataset

Antes de dividir el trabajo, deben **elegir juntos** el dataset, porque todo lo demás depende de esta decisión.

Opciones sugeridas (de mavenanalytics.io/data-playground):

- **Coffee Shop Sales**
- **Pizza Place Sales**
- **Video Game Sales**

También pueden generar datos propios en mockaroo.com. El dataset elegido debe permitir cubrir **todas** las actividades: relaciones entre tablas, medidas con fechas (crecimiento interanual), una dimensión tipo región/categoría para RLS, y datos geográficos si quieren usar mapas.

**Recomendación práctica:** revisen el dataset ANTES de dividir tareas, y verifiquen que tenga al menos:
- Una tabla de transacciones (ventas) con fecha, monto, cantidad.
- Una dimensión de producto/categoría.
- Una dimensión de cliente o región (para RLS).

---

## 3. Cómo dividir el trabajo en pareja

**Restricción importante a tener en cuenta:** el `.pbix` es **un solo archivo binario**. Power BI Desktop no tiene "control de versiones" tipo Git ni fusión automática de cambios como Word/Google Docs. Esto significa que **no se puede editar el mismo archivo `.pbix` al mismo tiempo desde dos computadores** sin perder el trabajo de uno de los dos.

Por eso, la división de módulos abajo está pensada para que cada persona pueda **avanzar en paralelo sin tocar el mismo archivo `.pbix` a la vez**, y luego integrar. Hay dos estrategias posibles, elijan la que les acomode:

### Estrategia A — "Un archivo, trabajo por turnos + preparación en paralelo"
Una persona tiene el `.pbix` "maestro" en su máquina. Mientras esa persona construye el modelo y las relaciones (Fase 1, que es intrínsecamente secuencial), la otra persona **prepara en paralelo, en documentos separados**, todo lo que no requiere tener el modelo abierto: fórmulas DAX escritas y probadas conceptualmente en un archivo de texto, el diseño/mockup de las 3 páginas del dashboard (qué visual va dónde), y la lista de roles de RLS a crear. Luego se juntan, la persona con el archivo pega/aplica lo preparado, y se turnan el archivo para las fases siguientes.

### Estrategia B — "Sesión compartida en vivo"
Trabajan con pantalla compartida (Zoom/Discord/Meet) o control remoto, una persona "maneja" el mouse mientras ambos deciden juntos. Es más lento pero evita cualquier problema de fusión de archivos. Recomendado para la Fase 1 (modelado), donde los errores de relaciones son difíciles de corregir después.

**Recomendación combinada (la más eficiente):** usar Estrategia B para la Fase 1 (modelado — 30-45 min juntos), y Estrategia A para las Fases 2 a 4, repartiendo el archivo por turnos mientras el que no tiene el archivo prepara el siguiente bloque en paralelo.

A continuación, los módulos de trabajo con esta lógica.

---

## MÓDULO 1 — Construcción del modelo semántico (secuencial, idealmente juntos)

**Por qué debe ir primero:** todas las medidas DAX, el RLS y el dashboard dependen de que existan las tablas y relaciones correctamente definidas. Empezar el DAX antes de tener el modelo estable genera trabajo repetido.

**Documentación de referencia:** *Modos de modelo semántico*.

### Pasos

1. **Seleccionar la base de datos** (ver sección 2 de esta guía).
2. **Importar datos desde al menos dos orígenes distintos.** Ejemplos: Excel con ventas históricas, CSV con catálogo de productos, fuente Web con tipos de cambio, base SQL Server con clientes. Usar **Inicio → Obtener datos**.
3. **Comprobar estructura de las tablas importadas** en la *Vista de datos*:
   - Todas las columnas cargadas correctamente.
   - Sin columnas innecesarias (eliminar en Power Query si sobran).
   - Nombres de columna claros, sin caracteres especiales.
4. **Definir relaciones entre tablas** en la *Vista de modelo* (arrastrando los campos clave). Ejemplo esperado:

   ```
   Tabla Ventas (muchos) --- (uno) Tabla Productos
   Tabla Ventas (muchos) --- (uno) Tabla Clientes
   ```

5. **Configurar cardinalidades y dirección de filtro.** Tip del enunciado: en la mayoría de los casos, las relaciones deben filtrar en un solo sentido, desde las dimensiones hacia los hechos.
6. **Validar el modelo con una tabla visual temporal** en una página de prueba, para confirmar que los datos de distintas tablas se combinan bien. (Ver *Modos de modelo semántico* / *Temp Table* en Fabric Community).

**Checklist de salida de este módulo (antes de dividirse):**
- [ ] Al menos 2 fuentes de datos distintas importadas.
- [ ] Columnas revisadas y sin basura evidente.
- [ ] Relaciones creadas con cardinalidad correcta (revisar que no queden como "muchos a muchos" por error).
- [ ] Tabla de prueba confirma que el cruce de datos funciona.

---

## MÓDULO 2 — Transformaciones en Power Query

**Documentación de referencia:** *Transformación, definición y modelado de datos*.

Este módulo puede repartirse **por tabla**: por ejemplo, una persona limpia la tabla de Ventas, la otra limpia Productos/Clientes. Como cada quien puede trabajar sobre su propia copia del archivo/datos de origen antes de consolidar, es un buen punto para paralelizar (Estrategia A).

### Pasos

1. **Acceder al editor:** Inicio → Transformar datos.
2. **Explorar la vista previa** de cada tabla: columnas innecesarias, valores nulos/vacíos/inconsistentes, nombres de columna poco claros.
3. **Eliminar duplicados y filas en blanco:** seleccionar la columna clave → Quitar duplicados; filtrar filas en blanco/nulas.
4. **Corregir tipos de datos.** Ejemplo en código M:

   ```
   = Table.TransformColumnTypes(Fuente,
       {{"FechaVenta", type date}, {"Cantidad", Int64.Type}})
   ```

5. **Normalizar nombres de columnas** (sin espacios ni caracteres especiales), usando "Usar primera fila como encabezados" si aplica.
6. **Crear columnas calculadas básicas.** Ejemplos:

   ```
   NombreCompleto = [Nombre] & " " & [Apellido]
   AñoVenta = Date.Year([FechaVenta])
   ```

7. **Filtrar datos irrelevantes** (fuera de rango de fechas/categorías de interés).
8. **Revisar los pasos aplicados** en el panel derecho: orden correcto, sin pasos redundantes.
9. **Cerrar y aplicar** para volver a Power BI Desktop.

**Nota de coordinación:** si se dividen las tablas entre los dos, definan **antes** una convención común de nombres de columnas (ej. todo en `PascalCase`, sin tildes ni espacios) para que al consolidar el modelo no haya inconsistencias entre las tablas que limpió cada uno.

---

## MÓDULO 3 — Desarrollo de medidas DAX

**Documentación de referencia:** *Escribe consultas DAX*.

Este es el módulo más fácil de preparar **en paralelo sin tocar el `.pbix`**: las fórmulas DAX se pueden escribir y revisar en un documento de texto compartido (Google Docs, Notion, un `.txt`) y luego pegarse todas de una vez cuando se tenga el archivo. Se puede dividir por "familia de medidas": una persona hace las medidas base y derivadas, la otra las medidas de contexto/ranking.

### Pasos

1. **Identificar las métricas clave.** Ejemplos: ventas totales, margen (valor y %), clientes únicos, ticket promedio, crecimiento interanual.
2. **Crear una tabla de medidas dedicada:** Inicio → Nueva tabla, llamarla `Medidas`, para mantener todo ordenado (buena práctica recomendada).
3. **Medidas básicas:**

   ```dax
   Ventas Totales = SUM(Ventas[Monto])
   Margen Valor = SUM(Ventas[Margen])
   Margen % = DIVIDE(SUM(Ventas[Margen]), SUM(Ventas[Monto]), 0)
   Clientes Únicos = DISTINCTCOUNT(Ventas[ClienteID])
   ```

4. **Medidas derivadas:**

   ```dax
   Ticket Promedio = DIVIDE([Ventas Totales], [Clientes Únicos], 0)

   Crecimiento % =
   DIVIDE(
       [Ventas Totales] -
       CALCULATE([Ventas Totales],
                 DATEADD('Calendario'[Fecha], -1, YEAR)),
       CALCULATE([Ventas Totales],
                 DATEADD('Calendario'[Fecha], -1, YEAR)),
       0
   )
   ```

5. **Medidas con funciones de contexto** (`FILTER`, `ALL`, `CALCULATE`):

   ```dax
   Ventas Año Actual =
       CALCULATE([Ventas Totales], YEAR('Calendario'[Fecha]) = YEAR(TODAY()))
   ```

6. **Validar cada medida** con tablas visuales temporales, probando distintos contextos de filtrado.
7. **Nombrar y formatear correctamente:** nombres claros y consistentes, formatos apropiados (moneda, %, entero).

**Importante para el modelo:** varias de estas fórmulas asumen que existe una tabla `Calendario` (tabla de fechas). Si su dataset no trae una, es buen momento para crearla (`CALENDAR()` o `CALENDARAUTO()` en DAX) — coordínenlo dentro del Módulo 1/3, ya que `DATEADD` y comparaciones año a año dependen de tener una tabla de fechas marcada como tal en el modelo.

---

## MÓDULO 4 — Parámetro What-if

**Documentación de referencia:** *Creación y uso de parámetros What-if*.

Módulo relativamente corto e independiente — se puede asignar a una sola persona mientras la otra avanza en el Módulo 5 (diseño de páginas), siempre que ambos coordinen quién tiene el archivo en ese momento.

### Pasos

1. **Definir el escenario a simular.** Ejemplos: % de descuento en ventas, incremento de precios, variación de costos.
2. **Crear el parámetro:** Modelado → Parámetro → Parámetro What-if. Definir valor mínimo, máximo, incremento (paso) y valor predeterminado. Ejemplo para descuento de 0% a 30% en pasos de 1%:

   ```dax
   Descuento WhatIf = GENERATESERIES(0, 0.3, 0.01)
   ```

   Esto genera automáticamente: una tabla con los valores del parámetro, una medida asociada al valor seleccionado, y un slicer para controlarlo.

3. **Crear una medida que use el parámetro:**

   ```dax
   Ventas con Descuento =
       [Ventas Totales] *
       (1 - 'Descuento WhatIf'[Descuento WhatIf Value])
   ```

4. **Probar la funcionalidad:** insertar el slicer del parámetro, crear una tarjeta con `[Ventas con Descuento]`, mover el slicer y confirmar que la medida cambia.

Recuerden: el parámetro genera una **tabla desconectada** (sin relaciones con el resto del modelo) — no debe intentar relacionarse con las tablas de hechos/dimensiones, su función es solo alimentar medidas puntuales.

---

## MÓDULO 5 — Diseño del dashboard (3 páginas)

**Documentación de referencia:** *Creación de un panel de Power BI*.

**Este es el módulo ideal para dividir el trabajo de diseño en paralelo**, incluso antes de tener el archivo `.pbix` con todas las medidas: mientras uno tiene el archivo y arma la página, el otro puede estar bocetando en papel/Figma/PowerPoint el layout de la siguiente página, para no perder tiempo esperando el turno del archivo.

### Estructura de 3 páginas

| Página | Contenido |
|---|---|
| **Visión general** | KPIs principales, tendencias globales, filtros generales |
| **Análisis por producto** | Ventas, rentabilidad y evolución por categoría/producto |
| **Análisis por cliente o región** | Distribución geográfica, clientes clave, comportamiento de compra |

**Sugerencia de división:** Persona 1 arma "Visión general" + coordina consistencia visual global (paleta de colores, tipografía). Persona 2 arma "Análisis por producto" y "Análisis por cliente/región".

### Página 1 — Visión general

- Tarjetas con KPIs: Ventas Totales, Margen %, Clientes Únicos, Crecimiento %.
- Medida de ejemplo para KPI binario:

  ```dax
  KPI Ventas vs Meta =
      IF([Ventas Totales] >= [Meta Ventas],
          "Meta alcanzada",
          "Meta no alcanzada")
  ```

- Gráfico de líneas para tendencia mensual.
- Slicers globales: año, región, categoría.

### Página 2 — Análisis por producto

- Gráfico de barras/columnas: ventas por categoría/producto.
- Gráfico de dispersión: precio promedio vs. ventas.
- Filtros específicos por producto/familia.
- Medida de ranking:

  ```dax
  Ranking Producto =
      RANKX(ALL(Productos[NombreProducto]), [Ventas Totales], , DESC)
  ```

### Página 3 — Análisis por cliente o región

- Mapa geográfico de ventas por ubicación.
- Tabla de clientes ordenados por compras.
- (Opcional) Gráfico de embudo para proceso de conversión.
- Medida de ventas acumuladas:

  ```dax
  Ventas Acumuladas Cliente =
      CALCULATE(
          [Ventas Totales],
          FILTER(
              ALLSELECTED(Clientes[ClienteID]),
              Clientes[ClienteID] <= MAX(Clientes[ClienteID])
          )
      )
  ```

### Transversal a las 3 páginas

- **Segmentaciones y formato condicional.** Ejemplo:

  ```dax
  Color KPI Ventas =
      IF([Ventas Totales] >= [Meta Ventas], "Green", "Red")
  ```

- **Consistencia visual:** mismos colores/tipografías/tamaños entre páginas.
- **Títulos y nombres descriptivos** en cada visual.
- **Probar interactividad:** combinaciones de filtros, verificar que todos los KPIs respondan de forma coherente en las 3 páginas.

---

## MÓDULO 6 — Row Level Security (RLS)

**Documentación de referencia:** *Definir roles y reglas*.

Módulo final, corto, mejor hacerlo juntos porque requiere probar (Modelado → Ver como) con ambos verificando que el filtro se comporte como se espera — un error de RLS es difícil de detectar solo con inspección visual del código DAX, hay que probarlo activamente.

### Pasos

1. **Analizar la necesidad de RLS:** determinar qué dimensión sirve para restringir (región, departamento, segmento de cliente) y verificar que la tabla tenga la columna adecuada.
2. **Definir los roles:** Modelado → Administrar roles. Ejemplos: `Rol_Ventas_Norte`, `Rol_Ventas_Sur`, `Rol_Marketing`.
3. **Configurar el filtro DAX de cada rol.**

   RLS estático:
   ```dax
   [Region] = "Norte"
   ```

   RLS dinámico (recomendado si hay muchos usuarios/roles):
   ```dax
   [Region] = LOOKUPVALUE(
       Usuarios[Region],
       Usuarios[Email], USERPRINCIPALNAME()
   )
   ```
   (requiere una tabla `Usuarios` con el mapeo Email → Region)

4. **Probar en Power BI Desktop:** Modelado → Ver como → seleccionar un rol → verificar que los datos visibles sean los esperados.
5. **Publicar y asignar roles en el servicio Power BI** (si el laboratorio lo requiere): publicar el reporte, ir al conjunto de datos → Seguridad, asignar usuarios/grupos de Azure AD a cada rol.

**Recordatorios conceptuales para la interrogación del staff:**
- Los roles son **aditivos**: un usuario en 2 roles ve la unión de ambos, no la intersección.
- El filtro de RLS se propaga siguiendo la **dirección de filtro configurada en las relaciones** — si la relación es de un solo sentido y el filtro necesita ir al revés, puede requerirse bidireccionalidad (evaluar impacto en rendimiento).
- No confundir roles de RLS (filas visibles) con roles del workspace en el Service (permisos sobre el reporte).

---

## MÓDULO 7 (Bonus, opcional)

Actividades opcionales que dan puntaje adicional — buen módulo para repartir si a cada uno le interesa un tema distinto:

1. **Integración con Python o R en Power Query:** un script para una transformación/cálculo avanzado no trivial en Power Query estándar (ej. clustering K-means y visualizar los grupos).
2. **Automatización con Power Automate:** un flujo que, ante una condición del dashboard (ej. ventas bajo el objetivo), envíe un correo automático o actualice una base de datos externa.
3. **Parámetros dinámicos con vinculación a datos:** un parámetro alimentado dinámicamente desde una tabla, que cambie la lógica de medidas/filtros del dashboard.

---

## 4. Plan de trabajo sugerido (orden y quién hace qué)

| Fase | Módulo | Modo de trabajo | Responsable sugerido |
|---|---|---|---|
| 1 | Elección de dataset | Juntos | Ambos |
| 2 | Modelo semántico (relaciones) | Juntos (Estrategia B) | Ambos |
| 3 | Power Query | Paralelo por tabla | Persona 1: Ventas / Persona 2: Productos-Clientes |
| 4 | Medidas DAX | Preparación en paralelo (doc de texto) + pegado conjunto | Persona 1: básicas/derivadas / Persona 2: contexto/ranking |
| 5 | Parámetro What-if | Uno solo, mientras el otro avanza en diseño | A definir |
| 6 | Diseño dashboard (3 páginas) | Paralelo (bocetos) + turnos con el archivo | Persona 1: Visión general / Persona 2: Producto + Cliente-Región |
| 7 | RLS | Juntos (requiere prueba activa) | Ambos |
| 8 | Documento PDF de entrega | Paralelo, cada uno redacta lo que hizo | Ambos |
| 9 (bonus) | Actividad opcional | A elección | A definir |

---

## 5. Checklist final antes de entregar

- [ ] Al menos 2 orígenes de datos distintos importados.
- [ ] Relaciones entre tablas con cardinalidad y dirección de filtro correctas.
- [ ] Transformaciones de Power Query aplicadas y sin pasos redundantes.
- [ ] Al menos las medidas: Ventas Totales, Margen %, Clientes Únicos, Ticket Promedio, Crecimiento %.
- [ ] Parámetro What-if funcional con su medida asociada y slicer.
- [ ] 3 páginas de dashboard (Visión general / Producto / Cliente-Región) con KPIs, gráficos e interactividad probada.
- [ ] Consistencia visual entre páginas (colores, tipografía).
- [ ] Al menos un rol de RLS definido, probado con "Ver como", y coherente con la dirección de filtro del modelo.
- [ ] Documento PDF con las 4 secciones pedidas (modelado, Power Query, DAX, RLS).
- [ ] Actividad mostrada y marcada como revisada por el staff **durante la sesión**.
- [ ] (Opcional) Al menos una actividad bonus si buscan puntaje extra.
