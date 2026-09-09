# BI en acción: áreas, componentes y ciclo de vida — Explicación del laboratorio

Este documento explica el contenido de la sesión práctica (laboratorio) de 3 horas de la Clase 2 de Inteligencia de Negocios, de la carrera de Ciencia de Datos. A diferencia de las dos clases teóricas anteriores, este material está diseñado como un **taller**: combina explicación conceptual con ejercicios grupales, y usa un mismo caso transversal (una agencia de viajes) para que los conceptos se vean aplicados de principio a fin. A continuación se explica el sentido de cada bloque, no solo su contenido.

---

## Objetivos de aprendizaje

La sesión se organiza en torno a cuatro objetivos explícitos, que en la práctica son también la estructura de los tres bloques del taller:

1. **Explicar el rol de BI:** describir cómo se aplica en marketing, finanzas, recursos humanos y operaciones (esto se cubre en el Bloque 1).
2. **Identificar componentes:** distinguir datos, procesos y herramientas, y cómo se relacionan entre sí (Bloque 2).
3. **Aplicar el ciclo de vida:** situar un requerimiento real dentro de las fases de un proyecto de BI (Bloque 3).
4. **Diseñar una solución:** proponer indicadores, fuentes y visualizaciones para un caso de negocio concreto (esto se practica de forma transversal en los tres ejercicios).

Es útil notar que estos cuatro objetivos son, en esencia, una aplicación práctica de lo que ya se explicó en las Clases 1 y 2 (arquitectura BI, componentes DSS, ciclo de vida del dato). Este laboratorio no introduce teoría nueva de fondo: su función es **ejercitar** esa teoría sobre un caso realista, hasta que el estudiante pueda aplicarla sin depender de la diapositiva.

---

## Repaso rápido: ¿qué es BI?

Antes de entrar al taller, se hace un repaso deliberado, conectando explícitamente con la Clase 1. Se organiza en tres columnas:

- **Definición operativa:** BI es un conjunto de datos, procesos y tecnologías que convierte datos crudos en decisiones, con foco en el pasado y el presente del negocio. Este último punto es importante y algo nuevo respecto a las clases anteriores: aclara que BI, por definición, mira hacia atrás y hacia el presente — no hacia el futuro, que es tarea de la analítica predictiva.
- **Qué NO es BI:** se aclaran tres malentendidos comunes — BI no es solo un dashboard bonito, no reemplaza el criterio de negocio (la persona sigue siendo quien decide), y no predice por sí solo (eso corresponde a la analítica avanzada, vista en el Módulo 4 de la Clase 2 teórica). Esta sección es valiosa porque corrige una confusión típica de quien recién aprende BI: pensar que "hacer BI" es lo mismo que "hacer un bonito gráfico".
- **Escalera del valor:** se resume en dos progresiones ya vistas — Dato → Información → Conocimiento (la jerarquía DIKW), y Descriptivo → Diagnóstico → Predictivo → Prescriptivo (los tipos de analítica). Esto reafirma que BI clásico vive en los primeros escalones (descriptivo/diagnóstico), mientras que las etapas más avanzadas (predictivo/prescriptivo) ya pertenecen al terreno de machine learning y analítica avanzada.

### Pregunta de activación

Se pide a los estudiantes pensar en su última compra en línea y anotar tres decisiones que la empresa tomó gracias a sus datos, antes, durante y después de la compra, compartiéndolas con un compañero. Esta dinámica cumple el mismo propósito que los casos de Amazon o Mercado Libre de la Clase 1: hacer que el concepto abstracto de BI se sienta concreto, pero esta vez usando la propia experiencia del estudiante como fuente del ejemplo, en vez de un caso ya armado por el profesor.

---

## Bloque 1 — BI en las áreas funcionales

Este bloque responde al primer objetivo de aprendizaje: cómo BI se aplica de forma distinta según el área de la organización que lo use. Es, en cierto modo, una versión mucho más aplicada de los "niveles de decisión en la organización" vistos en la Clase 1 (estratégico/táctico/operacional) — aquí el eje no es el nivel jerárquico, sino el **área funcional**.

### Una misma plataforma, cuatro conversaciones

Se presenta la idea central del bloque: la misma infraestructura de BI puede alimentar conversaciones completamente distintas según el área que la use. Se resume cada área en una sola pregunta de negocio:

- **Marketing:** "¿A quién le hablo y con qué retorno?"
- **Finanzas:** "¿Cómo se comporta el dinero del negocio?"
- **Recursos Humanos:** "¿Quién sostiene la operación y cómo está?"
- **Operaciones:** "¿Cómo entrego mejor, más rápido y más barato?"

La frase de cierre del slide es la idea clave de todo el bloque: **"la diferencia no está en la tecnología, sino en las preguntas de negocio y en los indicadores que cada área necesita responder"**. Esto es coherente con algo ya visto en la Clase 1 (la capa semántica y los KPI con dueño y meta): la tecnología subyacente puede ser la misma (el mismo Data Warehouse, el mismo Power BI), pero lo que cambia entre áreas es **qué preguntas se le hacen** a esos datos.

### BI en Marketing, Finanzas, Recursos Humanos y Operaciones

Cada una de las cuatro áreas se explica con la misma estructura de tres partes, usando siempre el mismo caso transversal — una **agencia de viajes** —, lo cual permite ver cómo un mismo negocio genera necesidades de información completamente distintas según el área que pregunte:

- **Preguntas típicas:** las dudas de negocio reales que el área necesita resolver.
- **Indicadores clave:** los KPI concretos que responderían esas preguntas.
- **Un ejemplo narrativo:** un caso corto que muestra cómo, en la práctica, cruzar ciertos datos llevó a una decisión y un resultado concreto.

**Marketing** se pregunta qué campañas rentan más, qué perfiles de viajero tienen mayor valor de vida (CLV) y en qué paso del embudo de reserva se pierden clientes, usando indicadores como CAC (costo de adquisición de cliente), ROAS (retorno sobre la inversión publicitaria) y la tasa de conversión de búsqueda a reserva. El ejemplo muestra cómo cruzar búsquedas del sitio, historial de reservas y campañas de correo permitió a una agencia dejar de premiar el clic (una métrica superficial) y empezar a premiar el margen por pasajero (una métrica que realmente refleja rentabilidad) — una lección importante sobre elegir bien qué indicador optimizar.

**Finanzas** se pregunta qué destinos o sucursales pierden dinero, cómo se desvía la ejecución respecto del presupuesto y cómo el tipo de cambio afecta el margen, usando indicadores como margen por reserva, ingreso por pasajero y desviación presupuestaria. El ejemplo es particularmente ilustrativo del valor real de BI: el equipo de finanzas pasaba **cinco días** consolidando planillas manualmente cada mes; al centralizar los datos en un modelo único, el análisis quedó disponible el día 2, y la conversación del equipo cambió de "¿este número está bien?" (dudar de los datos) a "¿por qué el Caribe cayó tres puntos?" (analizar el negocio). La frase final del ejemplo resume perfectamente la idea: **"el valor no fue el gráfico: fue recuperar tres días de análisis"** — es decir, el verdadero valor de BI muchas veces no es visual, sino de tiempo recuperado para pensar en el negocio en vez de en reconciliar números.

**Recursos Humanos** se pregunta qué sucursales concentran mayor rotación de personal, cuánto cuesta y demora contratar, y si la dotación acompaña la estacionalidad de la demanda, usando indicadores como rotación voluntaria, tiempo y costo de contratación, y ausentismo. El ejemplo muestra cómo cruzar turnos, antigüedad, metas y evaluaciones permitió detectar que la rotación se disparaba entre el mes 3 y el mes 5 en sucursales de alta temporada — y que la solución no fue subir sueldos (una respuesta intuitiva y costosa), sino rediseñar el acompañamiento durante el primer trimestre. Se agrega una advertencia importante: estos datos son sensibles y exigen anonimización y control de acceso, reforzando el tema de gobierno de datos visto en clases anteriores.

**Operaciones** se pregunta dónde están los cuellos de botella en la emisión de reservas, qué cupos quedan sin vender y si se cumplen los itinerarios comprometidos, usando indicadores como ocupación de cupos, puntualidad de traslados y tiempo de emisión. El ejemplo muestra cómo combinar GPS de vehículos, itinerarios de vuelos y reclamos de pasajeros permitió detectar que el 70% de los atrasos ocurría con vuelos que aterrizaban entre las 17 y las 20 horas en temporada alta, lo que llevó a reprogramar turnos sin necesidad de comprar más vehículos. Se cierra con una observación técnica relevante: **la frecuencia de actualización es crítica — un dato diario llega tarde** para este tipo de decisión operacional, lo que conecta con el concepto de "oportunidad" (una de las seis dimensiones de calidad de datos) y con la idea de que la latencia debe ajustarse a la urgencia de la decisión, ya vista en la Clase 1.

### El mismo dato, cuatro lecturas

Este slide cierra el Bloque 1 con una tabla-síntesis que resume las cuatro áreas en una sola vista: pregunta de negocio, indicador y fuente de datos habitual para cada una. La regla práctica que se entrega al final es memorable y muy aplicable: **"si no puedes escribir la pregunta de negocio en una frase, todavía no estás listo para construir el tablero"**. Esta idea funciona como un criterio de diseño concreto: antes de abrir cualquier herramienta de visualización, primero hay que poder formular la pregunta de negocio de forma clara y específica — si eso no es posible, construir el dashboard sería prematuro (probablemente terminaría siendo un dashboard bonito pero sin propósito claro, justo lo que se advertía que BI "no es" al inicio de la sesión).

### Ejercicio 1 · Del área a la pregunta

Primer ejercicio práctico, en grupos de 3, con 25 minutos de duración. Los estudiantes eligen una empresa que conozcan (retail, banco, delivery, universidad), formulan dos preguntas de negocio por cada una de las cuatro áreas funcionales (ocho preguntas en total), y para cada una definen el indicador que la respondería y la fuente de datos correspondiente. Un paso interesante del ejercicio es marcar con una estrella la pregunta que **la empresa hoy NO puede responder** — esto obliga a los estudiantes a distinguir entre lo que BI debería poder hacer en teoría y lo que realmente se puede hacer con los datos disponibles hoy, una distinción muy realista en proyectos de BI reales. Se evalúa la claridad de la pregunta, la coherencia entre pregunta e indicador, y el realismo de la fuente de datos propuesta.

---

## Bloque 2 — Componentes de un sistema de BI

Este bloque responde al segundo objetivo de aprendizaje, retomando y profundizando de forma práctica los "elementos clave de BI" vistos en la Clase 2 teórica (fuentes, integración, calidad, acceso), pero organizándolos ahora en tres grandes componentes.

### Los tres componentes

Se presenta el marco central del bloque: todo sistema de BI está compuesto por **Datos** (la materia prima), **Procesos** (la transformación) y **Herramientas** (la entrega). La idea clave, remarcada explícitamente, es que **ninguno de los tres funciona sin los otros dos**, y se cierra con una frase muy directa que resume el espíritu de todo el bloque: **"un sistema de BI falla por su eslabón más débil: datos sucios con la mejor herramienta siguen siendo datos sucios"**. Esta es, en esencia, la misma idea de la Clase 1 sobre el ETL ("un dashboard elegante construido sobre datos sucios entrega decisiones equivocadas con apariencia de rigor"), pero generalizada a los tres componentes: no basta con tener buena tecnología si los datos o los procesos fallan.

### Componente 1 · Datos

Se profundiza en la naturaleza de los datos desde tres ángulos:

- **Origen:** datos internos (ERP, CRM, POS, RR.HH.), externos (INE, precios, clima, redes sociales) y generados específicamente para el análisis (encuestas, sensores). Esta distinción entre interno/externo/generado es un poco más detallada que la clasificación de "fuentes" vista en clases anteriores.
- **Naturaleza:** estructurados (tablas y transacciones), semiestructurados (JSON, logs, XML) y no estructurados (texto, imagen, audio) — la misma clasificación vista en la Clase 1.
- **Temporalidad:** un ángulo nuevo respecto a clases anteriores — los datos pueden ser históricos (útiles para ver tendencias), casi en tiempo real (necesarios para decisiones operativas urgentes, como el caso de Operaciones visto en el Bloque 1) o instantáneas/snapshots (una "foto" del estado de algo en un momento específico).

Se repite el listado de las **seis dimensiones de calidad** ya vistas en la Clase 1 (exactitud, completitud, consistencia, oportunidad, unicidad, validez), presentadas aquí como "las que debes exigir" — un lenguaje más directo y orientado a la acción, propio del formato de taller.

### Componente 2 · Procesos

Se presenta un flujo de cinco pasos que explica **cómo el dato se vuelve confiable**: Extraer (conectar y leer las fuentes) → Transformar (limpiar, unificar, calcular) → Cargar (depositar en el modelo) → Modelar (organizar en hechos y dimensiones) → Publicar (entregar y monitorear). Este flujo de cinco pasos es una versión ampliada del ETL clásico (Extract-Transform-Load) visto en la Clase 1: agrega explícitamente dos pasos que antes quedaban implícitos — **Modelar** (que corresponde al modelado dimensional visto en la Clase 2 teórica) y **Publicar** (que corresponde a la capa de explotación/dashboards).

Se retoma la comparación **ETL frente a ELT** ya vista en clases anteriores, ahora resumida en una regla práctica muy clara: **"la elección depende del volumen, la latencia y el costo, no de la moda"** — una advertencia útil, porque en la práctica profesional a veces se elige una tecnología "de moda" (por ejemplo, ELT en la nube) sin evaluar si realmente es la opción correcta para el caso concreto.

También se repasa el **gobierno de datos**, con cuatro elementos: un diccionario con definiciones únicas de cada métrica (esto es exactamente la "capa semántica" vista en la Clase 1), roles y permisos sobre quién puede ver qué información, trazabilidad o linaje del dato de punta a punta, y políticas de ciclo de vida, retención y anonimización de los datos.

### Componente 3 · Herramientas

Se presenta el "stack tecnológico por capas", organizando las herramientas según la etapa del flujo de datos en la que participan: Fuentes (ERP, CRM, POS, APIs, archivos planos, sensores) → Integración (herramientas de ETL/ELT y orquestación) → Almacenamiento (bodega de datos, lago de datos o arquitectura mixta) → Análisis y modelo (motor semántico, cubos, SQL, capas de métricas) → Visualización (tableros, reportes, alertas, autoservicio). Esta es, en esencia, la misma arquitectura de referencia vista en la Clase 1 (fuentes → integración → almacenamiento → análisis → explotación), pero explicada ahora desde la perspectiva de "qué herramienta usar en cada capa" en vez de "qué función cumple cada capa".

Se agregan seis criterios prácticos para **elegir** entre las distintas herramientas disponibles en cada capa: el volumen y variedad de los datos, la latencia que exige la decisión, las competencias del equipo que operará la herramienta, el costo total de propiedad (no solo el precio de las licencias), la integración con los sistemas existentes en la organización, y el nivel de gobierno, seguridad y trazabilidad que ofrece. Esta lista es valiosa porque traslada la discusión de "qué herramienta es mejor en abstracto" a "qué herramienta es mejor **para este contexto específico**" — un criterio mucho más realista para quien deba tomar esta decisión en un proyecto real.

### Dónde se va el esfuerzo real

Este slide entrega un dato cuantitativo que refuerza, con números concretos, algo que la Clase 1 ya había afirmado de forma cualitativa (que la integración concentra entre el 60% y el 80% del esfuerzo de un proyecto BI). Aquí se muestra una distribución típica del esfuerzo en un proyecto de BI:

- Levantamiento de requerimientos: 15%
- **Integración y limpieza de datos: 40%** (la etapa más grande, por lejos)
- Modelado de datos: 20%
- Visualización y tableros: 15%
- Adopción y capacitación: 10%

La lectura que se entrega es clara: **"el dashboard es la punta del iceberg"** y **"la integración concentra el mayor riesgo del proyecto"**. La implicancia práctica para quien planifique un proyecto de BI es doble: hay que **planificar el doble de tiempo del que se cree** para la parte de datos (porque siempre se subestima), y la **adopción se diseña, no se espera** — es decir, no basta con construir un buen tablero y asumir que la gente lo va a usar; hay que planificar activamente cómo lograr que se adopte, algo que se retomará en el Bloque 3.

### Ejercicio 2 · Mapa de componentes

Segundo ejercicio práctico, en grupos de 3, con 20 minutos de duración. Se plantea un caso concreto: una agencia de viajes con 40 sucursales y venta web, donde la gerencia quiere un tablero diario de reservas, margen por destino y cumplimiento de metas por sucursal, pero hoy cada sucursal envía una planilla por correo los lunes, el motor de reservas web es independiente del sistema de las sucursales, y no existe un catálogo único de destinos ni de proveedores (es decir, el clásico problema de "múltiples verdades" y sistemas desconectados visto en la Clase 1).

El ejercicio se divide exactamente según los tres componentes recién explicados:

- **Parte A · Datos:** qué fuentes se necesitan, qué granularidad mínima requiere el análisis, y qué problemas de calidad se anticipan (dado el escenario descrito, con planillas manuales y sistemas desconectados, seguramente habrá varios).
- **Parte B · Procesos:** si conviene usar ETL o ELT y por qué, con qué frecuencia debe actualizarse la información (recordando el ejemplo de Operaciones, donde un dato diario llegaba tarde), y quién debe definir formalmente qué significa una "reserva confirmada" (un ejemplo directo de por qué se necesita un diccionario de métricas con dueño y definición única).
- **Parte C · Herramientas:** qué capas del stack tecnológico se necesitan, qué debería ver el gerente y qué debería ver el jefe de sucursal (retomando la idea de los distintos niveles de decisión — estratégico versus operacional — vista en la Clase 1), y qué **no** comprarían todavía (una pregunta inteligente que obliga a priorizar y evitar sobre-invertir en tecnología antes de resolver los problemas de datos y procesos).

El entregable es un diagrama en una hoja con las tres capas y las decisiones justificadas en una línea cada una — un ejercicio de síntesis que obliga a decidir, no solo a listar opciones.

---

## Bloque 3 — Ciclo de vida de la inteligencia de negocios

Este bloque responde al tercer objetivo de aprendizaje: situar un requerimiento real dentro de las fases de un proyecto de BI. El subtítulo del bloque lo resume bien: **"de la pregunta de negocio al valor sostenido en el tiempo"** — es decir, este bloque no se detiene en la entrega del producto (el tablero), sino que sigue hasta que ese producto genere valor de forma sostenida.

### Las seis fases del ciclo de vida

Se presenta un ciclo de proyecto de seis fases, distinto (y más orientado a gestión de proyectos) que el "ciclo de vida de los datos" visto en la Clase 2 teórica (captura, almacenamiento, procesamiento, análisis, reportes, mantenimiento). Aquí el foco está en cómo se gestiona un **proyecto** de BI de principio a fin:

1. **Planificación:** definir el problema, el alcance, los actores involucrados y el caso de negocio (por qué vale la pena hacer este proyecto).
2. **Requerimientos:** levantar las preguntas de negocio, los indicadores, los roles de quienes usarán la solución, y los criterios de éxito.
3. **Diseño:** definir la arquitectura, el modelo de datos, las métricas concretas y construir prototipos.
4. **Desarrollo:** construir efectivamente las integraciones, el modelo de datos, los tableros, y hacer pruebas de calidad.
5. **Despliegue:** poner la solución en producción, capacitar a los usuarios y gestionar activamente su adopción.
6. **Evolución:** monitorear el uso real y el valor generado, y ajustar, ampliar o depurar la solución según sea necesario.

El título del slide aclara algo importante: **"es un ciclo, no una línea recta"** — es decir, después de la fase de Evolución no se termina el proyecto, sino que puede volver a generar nuevos requerimientos, reiniciando el ciclo. Se cierra con una recomendación de gestión de proyectos muy concreta: **"cada iteración debería durar semanas, no años: entregar valor temprano es la mejor estrategia de adopción"** — esto conecta directamente con la fase de "Adopción y capacitación" mencionada en el slide anterior (Bloque 2), reforzando que la adopción no es automática, sino que se logra entregando resultados útiles rápido, en vez de esperar a tener un proyecto "perfecto" y completo antes de mostrar algo.

### Qué se entrega en cada fase

Se detalla, para cada una de las seis fases, cuál es su **entregable principal** y cuál es el **criterio de salida** (la señal concreta que indica que se puede avanzar a la siguiente fase, evitando que un proyecto se quede estancado indefinidamente en una etapa):

- **Planificación** → Caso de negocio y alcance; se avanza cuando el patrocinador firma el objetivo y el presupuesto.
- **Requerimientos** → Catálogo de preguntas e indicadores; se avanza cuando cada indicador tiene dueño, fórmula y fuente definidos (esto retoma directamente el concepto de KPI bien definido visto en la Clase 1: "sin meta no hay indicador, sólo una cifra").
- **Diseño** → Modelo dimensional y prototipo; se avanza cuando el usuario final reconoce sus propios números en el prototipo (una validación práctica muy útil: si el usuario no reconoce sus datos, algo está mal modelado).
- **Desarrollo** → Flujos, modelo y tableros ya probados; se avanza cuando las pruebas de calidad y la conciliación de cifras cuadran correctamente.
- **Despliegue** → El sistema en producción, con manual y capacitación; se avanza cuando los usuarios entran a usar la herramienta sin que nadie tenga que recordárselo (una señal de adopción genuina, no forzada).
- **Evolución** → Un backlog priorizado y métricas de uso; el criterio de éxito final es que **el tablero cambia decisiones, no solo se mira** — la prueba definitiva de que el proyecto de BI realmente cumplió su propósito.

Este último criterio es especialmente importante porque conecta con la definición de BI vista desde la primera clase: el objetivo nunca fue construir un dashboard bonito, sino apoyar mejores decisiones. Un tablero que se mira pero no cambia ninguna decisión, técnicamente, no ha cumplido su función.

### Errores frecuentes y cómo evitarlos

Se presentan cuatro errores comunes en proyectos reales de BI, cada uno con su síntoma y su contramedida:

- **Empezar por la herramienta:** comprar una licencia antes de saber qué pregunta se va a responder. La contramedida es siempre partir por la decisión que se quiere mejorar, no por la tecnología (esto es coherente con la "regla práctica" del Bloque 1: si no puedes escribir la pregunta de negocio, no estás listo para construir nada).
- **Métricas sin dueño:** tres áreas calculan "venta" de forma distinta y nadie cede — el clásico problema de "las múltiples verdades" visto en la Clase 1 (Ventas informa $1.250 millones, Finanzas informa $1.180 millones, Gerencia informa $1.310 millones). La contramedida es tener un diccionario único, con dueño y fórmula publicada para cada métrica.
- **El proyecto de un año:** se entrega tan tarde que el negocio ya cambió de prioridad. La contramedida son las iteraciones cortas con valor visible cada pocas semanas, la misma idea de "entregar valor temprano" mencionada en el slide de las seis fases.
- **Ignorar la adopción:** el tablero existe, pero todos siguen usando su planilla de siempre. La contramedida es la capacitación, generar rituales de uso (por ejemplo, revisar el tablero en cada reunión semanal) y medir el uso real de la herramienta, no asumir que se usa solo porque existe.

Este slide funciona como una síntesis muy práctica de todos los riesgos mencionados a lo largo del taller, presentados de forma directa para que sean fáciles de recordar y evitar en un proyecto real.

### Ejercicio 3 · Del requerimiento al plan

Tercer y último ejercicio, presentado como un "taller integrador" (25 minutos, grupos de 3), lo cual indica que su objetivo es combinar todo lo aprendido en los dos bloques anteriores. Se entrega un encargo deliberadamente vago y realista de un gerente: **"Necesito saber por qué estamos perdiendo clientes y lo necesito para el directorio del próximo mes"** — sin más detalle. Este tipo de encargo ambiguo es muy típico en el mundo real, y el ejercicio consiste justamente en convertirlo en un plan de proyecto concreto:

1. **Paso 1:** traducir el encargo vago en tres preguntas de negocio medibles (aplicando lo aprendido en el Bloque 1 sobre cómo formular preguntas de negocio claras).
2. **Paso 2:** definir indicadores, fuentes y granularidad para cada pregunta (aplicando el Componente 1 — Datos, del Bloque 2).
3. **Paso 3:** ubicar las tareas necesarias dentro de las seis fases del ciclo de vida (aplicando lo recién visto en este mismo Bloque 3).
4. **Paso 4:** declarar dos riesgos del proyecto y qué se haría para mitigarlos (aplicando la lección de "errores frecuentes" recién vista).

El entregable final es una lámina con el plan por fases, tres preguntas con su indicador, dos riesgos con su mitigación, y una presentación de 3 minutos — es decir, este ejercicio pide producir, en miniatura, exactamente lo que se necesitaría para justificar y planificar un proyecto de BI real.

### Cómo se evalúan los ejercicios

Se entrega una rúbrica formativa que aplica a los tres ejercicios de la sesión, con cuatro criterios evaluados en tres niveles (Logrado / En desarrollo / Inicial):

- **Pregunta de negocio:** desde "específica, medible y accionable" (logrado) hasta "confunde pregunta con reporte" (inicial) — este último error es justamente lo que se advertía al principio de la sesión sobre qué NO es BI.
- **Indicador y fuente:** desde "coherentes y con granularidad definida" hasta "indicador sin fuente asociada".
- **Uso del ciclo de vida:** desde "ubica tareas y criterios de salida" hasta "omite fases clave".
- **Riesgos y supuestos:** desde "identifica riesgos con mitigación" hasta "no los declara".

Esta rúbrica hace explícito, de forma evaluable, todo lo que el taller buscó enseñar: no basta con generar cualquier pregunta, indicador o plan — deben cumplir criterios de calidad específicos, que son los mismos que se exigirían en un proyecto de BI real.

---

## Síntesis y trabajo para la próxima clase

La sesión cierra con tres ideas para llevarse, que resumen exactamente los tres bloques del taller:

1. **"BI cambia de preguntas según el área, no de naturaleza"** — síntesis del Bloque 1: la misma plataforma sirve a Marketing, Finanzas, RR.HH. y Operaciones, pero cada una le hace preguntas distintas.
2. **"Datos, procesos y herramientas son un solo sistema: el eslabón débil manda"** — síntesis del Bloque 2: ningún componente funciona de forma aislada, y el sistema completo es tan bueno como su parte más débil.
3. **"El ciclo de vida es iterativo y termina en el uso, no en la entrega"** — síntesis del Bloque 3: un proyecto de BI no termina cuando se entrega el tablero, sino cuando ese tablero efectivamente se usa y cambia decisiones.

Como tarea para la próxima sesión, se pide elegir una organización real y documentar 5 indicadores con su fuente, identificar en qué fase del ciclo de vida está su capacidad analítica actual, y entregar todo esto en una lámina de formato libre al inicio de la Clase 3.

Finalmente, se anticipa el contenido de la próxima clase práctica: **arquitectura de datos para BI** (bodegas de datos, lagos de datos y modelado dimensional), donde se retomará el mismo caso de la agencia de viajes usado en este laboratorio, pero llevándolo esta vez a un **modelo de hechos y dimensiones concreto** — es decir, la siguiente sesión tomará todo lo diseñado conceptualmente aquí (qué preguntas, qué indicadores, qué fuentes) y lo convertirá en un modelo técnico real, cerrando el ciclo entre la teoría de las Clases 1 y 2 y su aplicación práctica completa.
