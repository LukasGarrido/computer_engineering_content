![Encabezado](raw/assets/logo_encabezado.png)

PLAN DE GESTIÓN DEL PROYECTO

Plantilla para integrar los entregables de planificación · Entregable n.º 3

| **Identificación** | **Completar por el equipo** |
| --- | --- |
| Nombre del proyecto | LiciFlow |
| Código | G8 |
| Versión | 2.0 |
| Equipo de proyecto | Lukas Garrido y Octavio Valencia |
| Líder / responsable | Lukas Garrido |
| Sponsor / Patrocinador | Empresas / Mercado publico |
| Duración estimada | 8 meses (10-09-2026 a 10-05-2027) |
| Presupuesto | 10.674.000 CLP (tope del Acta: 12.000.000 CLP) |
| Estado (pendiente / aprobado / rechazado) | Pendiente |
| Paralelo y fecha | 702 - 22/10/2026 |

**Orientaciones generales**

- Para los documentos elaborados en **Excel y GanttProject**, correspondientes al alcance, la EDT, los diccionarios, el cronograma y el presupuesto, incorporen en el informe de Word las tablas resumidas, los diagramas o las capturas legibles que permitan comprender los resultados de la planificación.

- **Conserven como anexos los archivos originales editables:** Entregable n.º 4 (Alcance, EDT y Diccionarios), Entregable n.º 8 (Cronograma) y Entregable n.º 9 (Presupuesto), incluyendo el archivo de GanttProject cuando corresponda.

- **Verifiquen la coherencia entre los documentos.** Los nombres de los entregables, códigos de la EDT, actividades, responsables, recursos, duraciones, fechas, costos, riesgos y criterios de calidad deben ser consistentes en todo el Plan de Gestión del Proyecto.

- Los textos entre corchetes **[ ]** corresponden a campos que cada equipo deberá completar con información de su propio proyecto. Eliminen las indicaciones y los textos de ejemplo antes de realizar la entrega.

- El proyecto **Sistema de Reserva de Laboratorios USM** se utiliza únicamente como referencia didáctica. Cada equipo deberá desarrollar la plantilla utilizando la información de su propio proyecto.

- Los elementos identificados como *propuestos*, *pendientes* o *por confirmar* deberán revisarse y actualizarse según corresponda. No deben presentarse como decisiones aprobadas si aún no cuentan con la validación correspondiente.

**ÍNDICE DE CONTENIDO**

- [1. Descripción](#1-descripción)
  - [1.1 Descripción y justificación](#11-descripción-y-justificación)
  - [1.2 Objetivo del proyecto](#12-objetivo-del-proyecto)
  - [1.4 Entregables y criterios de éxito](#14-entregables-y-criterios-de-éxito)
- [2. Planes por dominio](#2-planes-por-dominio)
- [3. Planes de gestión](#3-planes-de-gestión)
  - [3.1 Plan de Gobernanza](#31-plan-de-gobernanza)
  - [3.2 Plan de Gestión del Alcance](#32-plan-de-gestión-del-alcance)
  - [3.3 Plan de Gestión del Cronograma](#33-plan-de-gestión-del-cronograma)
  - [3.4 Plan de Gestión de Recursos](#34-plan-de-gestión-de-recursos)
  - [3.5 Plan de Gestión Financiera](#35-plan-de-gestión-financiera)
  - [3.6 Plan de Gestión de Riesgos](#36-plan-de-gestión-de-riesgos)
  - [3.7 Plan de Gestión de Interesados](#37-plan-de-gestión-de-interesados)
  - [3.8 Plan de Gestión de Comunicaciones](#38-plan-de-gestión-de-comunicaciones)
  - [3.9 Planificación de la Calidad](#39-planificación-de-la-calidad)
- [4. Integración, seguimiento y aprobación](#4-integración-seguimiento-y-aprobación)
  - [4.1 Verificación de coherencia entre planes](#41-verificación-de-coherencia-entre-planes)
  - [4.2 Seguimiento y control](#42-seguimiento-y-control)
  - [4.3 Aprobación del plan](#43-aprobación-del-plan)
- [5. Anexos y archivos de respaldo](#5-anexos-y-archivos-de-respaldo)
- [Lista de comprobación antes de entregar](#lista-de-comprobación-antes-de-entregar)
- [Ejemplo de verificación cruzada](#ejemplo-de-verificación-cruzada)

# 1. Descripción

## 1.1 Descripción y justificación

*Fuente: 1. Acta de constitución. Criterio de integración: Resuman qué problema aborda el proyecto, quiénes se beneficiarán y cuál es su solución propuesta.*

| **Elemento a registrar** | **Información del proyecto** |
| --- | --- |
| Problema / necesidad | Pérdida de tiempo productivo por búsqueda y seguimiento de licitaciones. |
| Solución propuesta | Plataforma web tipo SaaS que funciona como un CRM especializado en licitaciones. El sistema se conectará a la API de Mercado Público para buscar y filtrar licitaciones según el perfil comercial de cada empresa usuaria. |
| Justificación y beneficios | Ayuda a centralizar y automatizar el proceso de descubrimiento, evaluación y seguimiento de licitaciones públicas y privadas entre empresas. |

## 1.2 Objetivo del proyecto

*Fuente: Acta de constitución (entregable 1). Describan el objetivo general y los beneficios esperados.*

| **Elemento a registrar** | **Información del proyecto** |
| --- | --- |
| Objetivo general | Centralizar y automatizar el proceso de descubrimiento, evaluación y seguimiento de licitaciones públicas y privadas. |
| Resultados esperados | Disminuir la carga operativa del equipo comercial, Mitigar los errores administrativos que causan descalificación, Aumentar la probabilidades de adjudicación de las empresas usuarias. |

## 1.3 Límites y restricciones

*Fuente: 1. Acta de constitución y 4. Alcance–EDT–Diccionarios (Excel). Criterio de integración: Incluyan limitaciones de plazo, presupuesto, tecnología y exclusiones, indiquen los supuestos relevantes.*

| **Tipo** | **Descripción** |
| --- | --- |
| Alcance general | Sincronización  automática con la API de Mercado Público, filtros de búsqueda por palabras clave, rubro, región y monto, tablero Kanban para gestionar el estado de cada postulación, etc. |
| Restricción | Tiempo: 8 meses. Presupuesto: tope de 12.000.000 CLP. Recursos: 2 desarrolladores. Tecnología: los datos dependen de la disponibilidad y las condiciones de uso de la API pública de Mercado Público (ChileCompra). |
| Supuesto | La API de Mercado Público se mantiene pública, gratuita y con una estructura de datos razonablemente estable. Las empresas usuarias tienen internet estable en su jornada laboral. Los usuarios finales saben navegar en la web (no requieren capacitación técnica avanzada). |
| Exclusión | Licitaciones privadas o de portales distintos a Mercado Público, gestión de contratos posteriores a la adjudicación, facturación o cobros dentro de la plataforma, integración con otros portales de compras públicas regionales o internacionales. |

## 1.4 Entregables y criterios de éxito

* *Fuente: Acta de constitución (1) y alcance (4). Enumeren productos verificables y criterios de éxito, distingan los entregables del proyecto de los documentos académicos.*

| **Entregable** | **Criterio de aceptación / éxito** |
| --- | --- |
| Documentación técnica (objetivos, requerimientos, tecnologías y funcionalidades) | Requerimientos y alcance definidos y aprobados antes del hito H1 (29-09-2026). |
| Prototipo inicial del sistema | Prototipo de las vistas principales validado con el cliente (hito H2, 05-11-2026). |
| Arquitectura del sistema y modelo ER | Modelo de datos y arquitectura aprobados, con la conexión a la API de Mercado Público probada (hito H3, 09-11-2026). |
| Plataforma LiciFlow (MVP) en producción | Sincroniza licitaciones cada día y permite filtrarlas, el usuario gestiona una postulación de principio a fin en el Kanban, envía correctamente las alertas de plazos críticos. Lanzamiento el 10-05-2027 (H6). |

**Nota:** Los entregables del proyecto son los productos que se comprometen a desarrollar para solucionar el problema identificado. No deben confundirse con los entregables académicos solicitados en la asignatura, como el acta de constitución, las plantillas Excel, la matriz RAM o el informe de planificación.

# 2. Planes por dominio

*Indicaciones: Completen la siguiente síntesis de los siete dominios. No repitan aquí todas las tablas, el detalle va en la sección 3.*

| **Dominio** | **Decisión o resultado principal** | **Fuente principal** | **Sección del informe** |
| --- | --- | --- | --- |
| Gobernanza | El sponsor (Empresas) autoriza el proyecto y Lukas Garrido lo lidera y aprueba los entregables. Los cambios se manejan con solicitud escrita y las decisiones de calidad se definen en 3.9. | 1, 3 y 5 | 3.1 y 3.9 |
| Alcance | MVP definido por los requerimientos RF01–RF16 y RNF, 6 paquetes de trabajo (1 a 6), exclusiones del Acta (privadas, contratos, facturación y otros portales). | 4 (Excel) | 3.2 |
| Cronograma | Inicio 10-09-2026 y lanzamiento 10-05-2027 (H6), 6 fases, 45 actividades y 6 hitos, reserva de cronograma de 2 días hábiles. | 8 (Excel) | 3.3 |
| Finanzas | Estimación de costos 8.434.000 CLP, línea base 9.530.000 CLP, presupuesto total 10.674.000 CLP (bajo el tope de 12.000.000 CLP). | 9 (Excel) | 3.5 |
| Interesados | 6 interesados prioritarios, el más crítico es el proveedor de datos (ChileCompra / Mercado Público). Comunicaciones: matriz y protocolos propuestos en 3.8. | 2 y 7 | 3.7 y 3.8 |
| Recursos | 2 integrantes (Lukas Garrido y Octavio Valencia, 3 h/día cada uno), infraestructura en la nube y asesoría legal externa. Matriz RAM y organigrama propuestos en 3.4. | 5 | 3.4 |
| Riesgos | 9 riesgos identificados, mayor exposición: atraso por carga académica, cambios en la API y fuga de documentos, contingencia de 1.096.000 CLP. | 6 | 3.6 |
| Calidad | Se incorpora como componente transversal de la planificación. | 10 | 3.9 |

# 3. Planes de gestión

Desarrollen los siguientes apartados usando las plantillas ya trabajadas. Cada plan debe indicar sus decisiones principales, responsables y relación con los demás planes.

## 3.1 Plan de Gobernanza

*Indicaciones: Fuente: Acta (1), RR. HH. (5) y calidad (10). Explicar cómo se organiza la gobernanza del proyecto, quién toma y aprueba las decisiones y cómo se gestionan los cambios y problemas.*

| **Decisión / instancia** | **Responsable** | **Procedimiento / evidencia** |
| --- | --- | --- |
| Estructura de gobernanza | Sponsor (Empresas) y Lukas Garrido | El sponsor autorizó el proyecto en el Acta (10-09-2026). Lukas lidera y coordina al equipo, Octavio ejecuta. Reunión semanal del equipo (propuesto). |
| Roles y autoridad de aprobación | Lukas Garrido (líder) y sponsor | Lukas aprueba los entregables técnicos y los criterios de calidad (3.9). El sponsor aprueba el plan y los cambios que afecten la fecha de lanzamiento o el presupuesto total (propuesto). |
| Procedimiento de cambios y decisiones | Lukas Garrido | Solicitud de cambio escrita con su efecto en alcance, cronograma y costo, la decisión se registra con fecha. La reserva de gestión solo se usa con autorización del sponsor (propuesto). |

## 3.2 Plan de Gestión del Alcance

*Fuente: Excel Alcance–EDT–Diccionarios (4). Presentar los requisitos, el alcance, las exclusiones y los principales paquetes de trabajo del proyecto, incluyendo sus criterios de aceptación. Incorporar la EDT como imagen y mantener el diccionario detallado en el anexo Excel.*

- **Resumen del alcance**

| **Elemento a registrar** | **Información del proyecto** |
| --- | --- |
| Alcance aprobado | Plataforma web que sincroniza cada día las licitaciones de Mercado Público, las filtra (palabra clave, rubro, región y monto), las gestiona en un tablero Kanban con checklists y archivos adjuntos, avisa los plazos críticos (alertas 48 h antes) y ofrece calendario y panel de métricas, con registro de usuarios y organizaciones (RF01–RF16). |
| Exclusiones | Licitaciones privadas o de otros portales, gestión de contratos posteriores a la adjudicación, facturación o cobros, e integración con otros portales de compras públicas. |
| EDT / paquetes de trabajo | 6 paquetes de trabajo (1 Documentación técnica, 2 Prototipo inicial, 3 Arquitectura, 4 Desarrollo del MVP, 5 Pruebas y calidad, 6 Despliegue y cierre), el presupuesto agrega infraestructura y gestión. Detalle en el anexo A. |

*Figura 1. EDT del proyecto (niveles 1 a 3), según los paquetes de trabajo del cronograma.*

![Figura 1. EDT del proyecto](raw/assets/figura1_edt.png)

- **Entregables y criterios de aceptación**

| **Código EDT** | **Entregable / paquete de trabajo** | **Criterio de aceptación** |
| --- | --- | --- |
| 1 | Documentación técnica | Requerimientos y alcance aprobados (H1). |
| 2 | Prototipo inicial | Prototipo validado con el cliente (H2). |
| 3 | Arquitectura del sistema | Modelo ER y arquitectura aprobados, API probada (H3). |
| 4 | Desarrollo del MVP | Funcionalidades RF01–RF16 operativas (H4). |
| 5 | Pruebas y calidad | Los 5 criterios de calidad se cumplen y el piloto se realizó (H5). |
| 6 | Despliegue y cierre | Sistema en producción con HTTPS y respaldos, lanzamiento (H6). |

- **Referencia financiera de los paquetes de trabajo**

| **Paquete de trabajo** | **Costo estimado** |
| --- | --- |
| 1 / PT1 Documentación técnica | 528.000 CLP |
| 2 / PT2 Prototipo inicial | 624.000 CLP |
| 3 / PT3 Arquitectura del sistema | 672.000 CLP |
| 4 / PT4 Desarrollo del MVP | 3.600.000 CLP |
| 5 / PT5 Pruebas y calidad | 1.128.000 CLP |
| 6 / PT6 Despliegue y cierre | 600.000 CLP |
| PT7 Infraestructura y servicios | 562.000 CLP |
| PT8 Gestión del proyecto | 720.000 CLP |
| **Total estimado** | 8.434.000 CLP |

Esta tabla sirve para verificar la correspondencia entre alcance y presupuesto. El detalle de los costos debe mantenerse en el Plan de Gestión Financiera, evitando duplicarlo innecesariamente en este apartado.

## 3.3 Plan de Gestión del Cronograma

*Fuentes: 8. Cronograma (Excel), 4. Alcance–EDT–Diccionarios (Excel)*

*Criterio de integración: Presenten la duración total del proyecto, las fechas previstas de inicio y término, los hitos principales y las dependencias entre actividades. Identifiquen los responsables y los códigos de la EDT correspondientes. Incluyan el diagrama de Gantt actualizado y legible, indicando las actividades críticas cuando estén identificadas. Adjunten el cronograma completo en su formato editable.*

**A. Información general del cronograma**

| **Elemento a registrar** | **Información del proyecto** |
| --- | --- |
| Duración y fechas | 8 meses: inicio 10-09-2026 y lanzamiento 10-05-2027 (173 días hábiles), el cierre termina el 12-05-2027. Días hábiles de lunes a viernes, sin feriados. |
| Estructura | 6 fases (códigos EDT 1 a 6), 45 actividades y 6 hitos. Duraciones por estimación de tres puntos (PERT) y secuencia con dependencias Fin–Inicio y algunas Inicio–Inicio. |
| Ruta crítica | Requerimientos (1.1) → arquitectura (3.1 a 3.3) → desarrollo backend del MVP (4.1 a 4.8) → pruebas (5.2, 5.4, 5.5) → documentación final (6.3) → reserva y despliegue (6.4, 6.5) → H6. Dura 171 días de actividades (σ ≈ 4,8 días) y la reserva de cronograma es de solo 2 días hábiles. |
| Archivos | LiciFlow_Cronograma.xlsx (plantilla con PERT, recursos y Gantt) y LiciFlow.gan (GanttProject), en el anexo B. |

**B.Hitos y actividades principales**

| **Hito / actividad** | **Fecha** | **Responsable** | **Código EDT relacionado** |
| --- | --- | --- | --- |
| H1 Documentación aprobada | 29-09-2026 | Lukas Garrido | 1 |
| H2 Prototipo aprobado | 05-11-2026 | Octavio Valencia | 2 |
| H3 Arquitectura aprobada | 09-11-2026 | Lukas Garrido | 3 |
| H4 MVP funcional completo | 17-03-2027 | Lukas Garrido y Octavio Valencia | 4 |
| H5 Pruebas finalizadas | 23-04-2027 | Octavio Valencia y Lukas Garrido | 5 |
| H6 Lanzamiento / puesta en marcha | 10-05-2027 | Lukas Garrido y Octavio Valencia | 6 |

**C. Diagrama de Gantt / Recursos**

![Figura 2. Diagrama de Gantt](raw/assets/figura2_gantt.png)

*Figura 2. Diagrama de Gantt resumido por fase y grupo de actividades, con los 6 hitos (◆). El detalle de las 45 actividades está en los anexos B (Excel y .gan).*

![Figura 3. Carga mensual por integrante](raw/assets/figura3_carga_mensual.png)

*Figura 3. Carga mensual por integrante, en días hábiles con tarea asignada (dedicación de 3 h por día).*

El diagrama debe permitir visualizar la secuencia de actividades, sus duraciones, dependencias, responsables e hitos principales. Cuando el software lo permita, deberán señalarse las actividades de la ruta crítica.

El cronograma completo se conservará como anexo editable.

## 3.4 Plan de Gestión de Recursos

*Fuente: RR. HH.: rol–RAM–EDT (5), estimación de recursos y cronograma (8). Criterios de integración: Describan la estructura organizacional del proyecto, los roles, responsabilidades, niveles de autoridad y competencias requeridas. Presenten una síntesis de la matriz RAM y la estimación de los recursos humanos, tecnológicos y materiales necesarios. Verifiquen que las asignaciones sean coherentes con la EDT, el cronograma y el presupuesto.*

**A. Organización y asignación de responsabilidades**

| **Elemento a registrar** | **Información del proyecto:** |
| --- | --- |
| Estructura del equipo | Equipo de 2 integrantes: Lukas Garrido (líder y backend) y Octavio Valencia (frontend y pruebas). Sponsor: Empresas. |
| Responsabilidades | Lukas: gestión, arquitectura, conector, módulos de servidor y pruebas no funcionales. Octavio: prototipo, interfaces, pruebas funcionales, piloto y documentación final. |
| Autoridad | Lukas decide prioridades y aprueba entregables técnicos, los cambios de fecha de lanzamiento o de presupuesto total se consultan al sponsor (propuesto). |
| Disponibilidad y competencias | 3 h por día hábil por persona (≈ 15 h a la semana). Competencias requeridas: desarrollo backend y de APIs, frontend y diseño de interfaces, bases de datos y pruebas. |

**B. Estimación y asignación de recursos**

| **Rol / recurso** | **Responsabilidad** | **Cantidad / disponibilidad** | **Actividad o paquete** |
| --- | --- | --- | --- |
| Lukas Garrido | Líder y desarrollo backend: gestión, arquitectura, conector, módulos de servidor y pruebas no funcionales | 1 persona, 3 h/día (157 días-persona) | PT1 (1.2), PT3, PT4 (backend), 5.3, 6.1–6.2, 6.5–6.6 y PT8 |
| Octavio Valencia | Prototipo, frontend, pruebas funcionales, piloto y documentación final | 1 persona, 3 h/día (141 días-persona) | PT2, PT4 (interfaces), 5.1, 5.2, 5.5 y 6.3 |
| Infraestructura en la nube | Servidor de staging y producción, base de datos y almacenamiento, correo para alertas y dominio .cl | Servidor, base de datos y correo: 6 meses, dominio: 1 año | PT7, tareas 4.1 y 6.1 |
| Asesoría legal externa | Revisión de la política de privacidad (Ley 19.628) | 1 servicio antes del lanzamiento | PT7, tarea 6.2 |

**C. Matriz RAM — Asignación de responsabilidades**

Matriz elaborada a partir de las asignaciones del cronograma (LiciFlow.gan) y de la sección 3.4 B, por contrastar con el Entregable n.º 5.

| **Código EDT** | **Paquete / actividad** | **Lukas Garrido** | **Octavio Valencia** | **Sponsor (Empresas)** | **Clientes / usuarios** |
| --- | --- | --- | --- | --- | --- |
| 1.1 | Definición de requerimientos | P | P | I | C |
| 1.2 | Definición de tecnologías | P | C | I | — |
| 2.1–2.2 | Prototipo: vistas de registro y vistas principales | S | P | I | — |
| 2.3 | Validación del prototipo con el cliente (H2) | S | P | I | C |
| 3.1–3.2 | Modelo de datos y arquitectura de componentes | P | C | I | — |
| 3.3 | Integración con la API de Mercado Público | P | I | I | — |
| 4.1 | Configuración del entorno (Git y ambientes) | P | P | I | — |
| 4.2–4.7 | Módulos del MVP: identidad, conector, licitaciones, Kanban, documentos, alertas y métricas (backend: Lukas, frontend: Octavio) | P | P | I | — |
| 4.8 | Continuidad y respaldos | P | I | I | — |
| 5.1–5.2 | Plan de pruebas y pruebas funcionales | S | P | I | — |
| 5.3 | Pruebas no funcionales | P | C | I | — |
| 5.4 | Corrección de defectos | P | P | I | — |
| 5.5 | Piloto con usuarios (H5) | S | P | I | C |
| 6.1–6.2 | Infraestructura de producción y revisión de privacidad | P | I | I | — |
| 6.3 | Documentación final y manual de usuario | S | P | I | — |
| 6.4–6.6 | Reserva, despliegue, lanzamiento (H6) y cierre | P | P | I | I |

Para mantener coherencia con la matriz de asignación de recursos generada anteriormente, puede utilizarse la siguiente leyenda:

| **Código** | **Significado** | **Significado** |
| --- | --- | --- |
| P | Principal | Responsable de ejecutar la actividad. |
| S | Secundaria | Autoridad que aprueba o responde por el resultado. |
| C | Consulta | Consultado durante el desarrollo. |
| I | Informado | Informado sobre el avance o resultado. |

**D. Organigrama del proyecto**

![Figura 4. Organigrama del proyecto LiciFlow](raw/assets/figura4_organigrama.png)

*Figura 4. Organigrama del proyecto LiciFlow: relaciones de autoridad y coordinación (propuesto a partir del cronograma, por contrastar con el Entregable n.º 5).*

El organigrama debe representar las relaciones de autoridad, coordinación y responsabilidad entre los integrantes del proyecto.

## 3.5 Plan de Gestión Financiera

*Indicaciones: Fuente: Excel Presupuesto (9), alcance (4) y cronograma (8). Incluyan costo estimado por paquete, reserva de contingencia, línea base, reserva de gestión y presupuesto total, expliquen criterios de estimación y control.*

| **Componente** | **Monto (moneda del proyecto)** |
| --- | --- |
| Estimación de costos | 8.434.000 CLP |
| Reserva de contingencia | 1.096.000 CLP |
| Línea base de costos (estimación + contingencia) | 9.530.000 CLP |
| Reserva de gestión | 1.144.000 CLP |
| Presupuesto total (línea base + gestión) | 10.674.000 CLP |

Criterios de estimación: ascendente, desde las actividades del cronograma (894 horas a 8.000 CLP por hora, más infraestructura, asesoría legal y gestión). La contingencia es la suma de probabilidad × impacto de 9 riesgos, la reserva de gestión es el 12 % de la línea base. El presupuesto total queda 1.326.000 CLP bajo el tope de 12.000.000 CLP del Acta. La tarifa y los precios de infraestructura son valores referenciales por confirmar. Control: cada mes se compara el gasto y las horas reales con la línea base (ver 4.2).

## 3.6 Plan de Gestión de Riesgos

*Indicaciones: Fuente: Gestión de riesgos (6). Presenten una síntesis de la estructura de desglose de riesgos (RBS), identifiquen los riesgos prioritarios y registren su probabilidad, impacto y nivel de exposición. Definan la estrategia de respuesta, las acciones preventivas, los responsables y las medidas de contingencia. Expliquen cómo las respuestas afectan el cronograma, los recursos y el presupuesto.*

**A. Identificación y evaluación de riesgos**

| **Riesgo / código** | **P × I / prioridad** | **Respuesta y responsable** | **Efecto en otros planes** |
| --- | --- | --- | --- |
| R7 Atraso por carga académica | P 40 % × I 480.000 = 192.000 CLP (1.º) | Mitigar: seguimiento semanal del avance y priorizar las funciones del MVP. Responsable: Lukas Garrido | Cronograma: reserva de 2 días (6.4). Costos: contingencia. |
| R1 Cambios en la API de ChileCompra | P 30 % × I 500.000 = 150.000 CLP (2.º) | Mitigar: conector aislado y validación del esquema de datos. Responsable: Lukas Garrido | Cronograma: tareas 4.3 y 5.2. Costos: ≈ 60 h de retrabajo. |
| R5 Fuga o pérdida de documentos sensibles | P 10 % × I 1.500.000 = 150.000 CLP (2.º) | Mitigar: acceso por organización, HTTPS, contraseñas encriptadas y respaldos. Responsable: Lukas Garrido | Calidad: criterio de seguridad. Costos: respaldos y asesoría legal (PT7). |
| R9 Indisponibilidad de un integrante | P 10 % × I 1.200.000 = 120.000 CLP (4.º, empata con R2, R4 y R6) | Mitigar: código y documentos en Git y tareas compartidas. Responsables: Lukas Garrido y Octavio Valencia | Recursos: tareas críticas en una sola persona. Cronograma: posible atraso. |

**B. Plan de respuesta y contingencia**

| **Riesgo** | **Acción de respuesta** | **Plan de contingencia** | **Recursos / reserva** |
| --- | --- | --- | --- |
| R7 | Revisión semanal del avance en GanttProject, recortar funciones de menor prioridad si hay atraso. | Usar la reserva de cronograma (2 días) y, si no alcanza, pedir al sponsor ajustar fecha o alcance. | Contingencia: 192.000 CLP |
| R1 | Aislar el conector (4.3) y validar el esquema de los datos recibidos. | Adaptar el conector (≈ 60 h) y trabajar con los datos ya sincronizados mientras tanto. | Contingencia: 150.000 CLP |
| R5 | Control de acceso por organización, HTTPS, contraseñas encriptadas y respaldos diarios. | Restaurar el respaldo, avisar a las empresas afectadas y corregir la falla. | Contingencia: 150.000 CLP |
| R9 | Código y documentación compartidos en el repositorio Git. | La otra persona asume las tareas críticas y se renegocian alcance y fechas. | Contingencia: 120.000 CLP |

**C. Estructura de desglose de riesgos (RBS)**

![Figura 5. Estructura de desglose de riesgos (RBS)](raw/assets/figura5_rbs.png)

*Figura 5. Estructura de desglose de riesgos (RBS) con los 9 riesgos del registro (R1 a R9).*

La RBS debe permitir visualizar las categorías y fuentes de riesgos identificadas. Su contenido debe corresponder con el registro de riesgos del proyecto.

**D. Relación con el presupuesto**

El presupuesto del proyecto contempla una reserva de contingencia total de $1.096.000 CLP (suma de probabilidad × impacto de los 9 riesgos identificados), incluida en la línea base de costos.

Esta reserva no debe distribuirse arbitrariamente entre los riesgos. Cada asignación deberá justificarse según el costo estimado de la respuesta o contingencia y el procedimiento de autorización establecido.

## 3.7 Plan de Gestión de Interesados

*Fuente: 2. Registro de interesados, 7. Comunicación e interesados (2)*

*Criterio de integración: Identifiquen los interesados relevantes del proyecto, su nivel de poder e interés, sus necesidades y expectativas y las estrategias para gestionar su participación. La información debe ser coherente con el registro de interesados y el plan de comunicaciones.*

**A. Identificación y estrategias de participación**

| **Interesado** | **Poder / interés** | **Necesidad** | **Estrategia de participación** |
| --- | --- | --- | --- |
| Patrocinadores / inversionistas | Poder alto / interés alto | Cumplimiento de los objetivos y viabilidad del proyecto | Gestionar de cerca: informarles en cada hito y consultarles los cambios mayores. |
| Jefe de proyecto / Product Owner | Poder alto / interés alto | Cumplimiento de alcance, plazos y calidad | Gestionar de cerca: prioriza tareas y aprueba entregables. |
| Clientes / gerentes comerciales | Poder alto / interés alto | Reducir el tiempo operativo y los errores de postulación | Gestionar de cerca: validan el prototipo (tarea 2.3) y participan en el piloto. |
| Proveedor de datos (ChileCompra / Mercado Público) | Poder alto / interés bajo | Acceso estable a su API pública (interesado crítico) | Mantener satisfecho: respetar sus condiciones de uso y vigilar cambios en la API (R1). |
| Bid Managers (encargados de licitaciones) | Poder bajo / interés alto | Facilidad de uso y ahorro real de tiempo | Mantener informados: participan en las pruebas de usabilidad del piloto (5.5). |
| Ejecutivos comerciales | Poder bajo / interés alto | Alertas confiables y visibilidad del estado de cada licitación | Mantener informados: prueban las alertas y el tablero en el piloto (5.5). |

**B. Resumen de la gestión de interesados**

| **Elemento a registrar** | **Información del Proyecto** |
| --- | --- |
| Interesados clave | Patrocinadores, jefe de proyecto / Product Owner, clientes / gerentes comerciales, proveedor de datos (ChileCompra), Bid Managers y ejecutivos comerciales. |
| Interesados de mayor prioridad | El proveedor de datos (interesado más crítico) y los de poder e interés altos: patrocinadores, jefe de proyecto y clientes. |
| Participación en decisiones | El sponsor autoriza el proyecto (Acta) y el jefe de proyecto / Product Owner prioriza las tareas. |
| Participación en validación | El cliente valida el prototipo (tarea 2.3, hito H2), Bid Managers y ejecutivos comerciales validan el sistema en el piloto (tarea 5.5, antes de H5). |
| Seguimiento del involucramiento | Cada semana el líder revisa en la reunión del equipo la participación de los interesados y registra en actas la validación del prototipo (tarea 2.3, H2) y del piloto (tarea 5.5, antes de H5). El proveedor de datos se vigila cada mes junto con el riesgo R1, si un interesado de poder alto no responde, se escala al sponsor (propuesto). |

## 3.8 Plan de Gestión de Comunicaciones

*Fuente: Entregable n.º 7 (Comunicación e Interesados) y Entregable n.º 2 (Registro de Interesados).*

*Indicaciones para la plantilla: Definan qué información se comunicará, a quién, mediante qué canal, con qué frecuencia y quién será responsable. Incluyan los mecanismos para registrar acuerdos, comunicar cambios y mantener la trazabilidad de las decisiones.*

**A. Matriz de comunicaciones resumida**

| **Destinatario** | **Información** | **Canal** | **Frecuencia** | **Responsable** |
| --- | --- | --- | --- | --- |
| Patrocinador (Empresas) | Avance por hito, cambios de alcance, plazo o presupuesto y solicitudes de aprobación | Correo electrónico e informe de hito | En cada hito (H1 a H6) y ante cambios mayores | Lukas Garrido |
| Equipo de proyecto | Avance de tareas, riesgos y defectos | Reunión semanal por videollamada y repositorio Git | Semanal | Lukas Garrido |
| Clientes / gerentes comerciales | Prototipo para validación y resultados del piloto | Reunión de validación y correo electrónico | Tarea 2.3 (antes de H2) y piloto 5.5 | Octavio Valencia |
| Proveedor de datos (ChileCompra / Mercado Público) | Solicitud del ticket de acceso a la API y consultas sobre condiciones de uso | Portal oficial y correo de soporte | Al solicitar el ticket (3.3.1) y ante cambios en la API (R1) | Lukas Garrido |
| Bid Managers y ejecutivos comerciales | Instrucciones y comentarios del piloto, manual de usuario | Correo electrónico y sesión de piloto | Durante el piloto (5.5) y en el lanzamiento (H6) | Octavio Valencia |

**B. Protocolos de comunicación**

| **Elemento** | **Procedimiento propuesto** |
| --- | --- |
| Canal official | Correo electrónico para el sponsor, los clientes y el proveedor, reunión semanal por videollamada para el equipo (propuesto). |
| Registro de acuerdos | Acta breve tras cada reunión (fecha, participantes, acuerdos, responsables y plazos), guardada en el repositorio Git. |
| Almacenamiento de información | Repositorio Git del proyecto: documentos, Excel, archivo .gan y actas, con número de versión y fecha. |
| Comunicación de cambios | Solicitud de cambio escrita con su efecto en alcance, cronograma y costo, la decisión se registra con fecha. El sponsor aprueba si afecta el lanzamiento o el presupuesto total. |
| Confidencialidad | Los documentos y datos de licitaciones son solo del equipo y de las organizaciones usuarias, las credenciales y el ticket de la API no se comparten fuera del equipo (Ley 19.628, revisión en 6.2). |

## 3.9 Planificación de la Calidad

*Fuente: 10. Calidad*

*Criterio de integración: Definan los requisitos de calidad asociados a los entregables del proyecto, estableciendo indicadores medibles, criterios de aceptación, métodos de verificación, responsables y momentos de revisión. Los criterios deben ser coherentes con el alcance, el cronograma y las pruebas.*

**A. Matriz de planificación de la calidad**

| **Requisito** | **Indicador / criterio** | **Verificación** | **Responsable** | **Momento** |
| --- | --- | --- | --- | --- |
| Sincronización confiable de licitaciones (RF03) | 0 licitaciones duplicadas tras sincronizar, cada sincronización queda registrada con sus errores | Prueba funcional con dos sincronizaciones seguidas | Octavio | Tras 4.3 y pruebas 5.2 (18-03 a 31-03-2027) |
| Alertas de plazos críticos (RF13, RF14) | 100 % de las alertas enviadas 48 h antes del cierre de preguntas o de postulación | Prueba funcional con licitaciones de prueba | Octavio | Pruebas 5.2 (18-03 a 31-03-2027) |
| Seguridad de acceso y datos (RNF03, RNF04) | Solo usuarios autorizados de su organización acceden a sus datos, contraseñas encriptadas, todo en HTTPS | Prueba de autenticación y roles, revisión de HTTPS | Lukas | Pruebas 5.3 (18-03 a 26-03-2027) |
| Rendimiento y continuidad (RNF02, RNF05, RNF09) | Búsqueda y tablero en ≤ 3 s, disponibilidad ≥ 99,5 %, respaldo con pérdida máxima de 24 h | Prueba de carga, monitoreo y restauración del respaldo | Lukas | Pruebas 5.3 y despliegue 6.1 (abr-2027) |
| Usabilidad (RNF01) | Un usuario nuevo guarda una licitación y la mueve en el Kanban en ≤ 5 min sin ayuda, vista correcta en escritorio y móvil | Pruebas de usabilidad con usuarios en el piloto | Octavio | Piloto 5.5 (13-04 a 22-04-2027) |

**B. Seguimiento y control de Calidad**

Se harán tres revisiones: de requisitos (hitos H1 y H2, a cargo de Lukas), pruebas del sistema (tareas 5.1 a 5.4, del 02-03 al 12-04-2027, Octavio las funcionales y Lukas las no funcionales) y piloto con usuarios (tarea 5.5). Los resultados se guardan en el plan y casos de prueba, y los defectos en la lista de incidencias del repositorio Git. Si un criterio no se cumple, se corrige en la tarea 5.4 y se repite la misma prueba, si no alcanza el tiempo, Lukas decide si se ajusta el alcance o se usa la reserva.

# 4. Integración, seguimiento y aprobación

## 4.1 Verificación de coherencia entre planes

*Indicaciones: Fuente: Todos los entregables. Comprueben la coherencia entre los planes desarrollados, verificando que las actividades, códigos EDT, responsables, recursos, fechas, costos, riesgos, criterios de calidad y comunicaciones sean consistentes. Identifiquen las diferencias o contradicciones encontradas, indiquen las correcciones necesarias o realizadas y registren al responsable y el estado de cada revisión.*

| **Cruce entre planes** | **Resultado de revisión / hallazgo** | **Corrección necesaria o realizada** | **Responsable / estado** |
| --- | --- | --- | --- |
| EDT ↔ Cronograma | Los códigos 1 a 3 del cronograma siguen el diccionario WBS. El Entregable 4 define solo 3 entregables, tiene fechas desde 01-09-2026 (antes del inicio oficial del 10-09-2026) y tareas sin completar, el cronograma agrega las fases 4, 5 y 6. | Actualizar el Excel del Entregable 4 (EDT y diccionario) con las fases 4 a 6 y las fechas del cronograma. | Equipo / pendiente |
| Cronograma ↔ Recursos/RAM | Cada actividad tiene responsable (Lukas u Octavio) y nadie tiene dos tareas a la vez. La matriz RAM del Entregable 5 no estaba disponible para compararla. | Contrastar el cronograma con la RAM cuando esté lista. | Equipo / pendiente |
| Recursos/EDT ↔ Presupuesto | Coherente: las 894 h del presupuesto equivalen a 298 días-persona del cronograma × 3 h/día, PT1 a PT6 corresponden a las fases 1 a 6. Diferencia: el Acta indica un presupuesto inicial de 1.000.000 CLP y una restricción de 12.000.000 CLP. | Corregir en el Acta la cifra de 1.000.000 CLP, el presupuesto total es 10.674.000 CLP. | Lukas / en revisión |
| Riesgos ↔ Cronograma/Costos | La reserva de cronograma (2 días) es corta frente al riesgo R7, la contingencia (1.096.000 CLP) equivale a la suma de P × I de R1 a R9. La matriz del Entregable 6 estaba sin completar. | Completar el Entregable 6 y contrastar sus niveles con estas exposiciones. | Equipo / pendiente |
| Calidad ↔ Alcance/Pruebas | Coherente, sin observaciones, los 5 criterios se vinculan con los RF y RNF y se verifican en las tareas 5.1 a 5.5 (PT5 del presupuesto). | No requiere corrección. | Octavio / revisado |
| Interesados ↔ Comunicaciones | No se pudo verificar: falta el Entregable n.º 7 (comunicación e interesados). | Completar el plan de comunicaciones y contrastarlo con el registro de interesados. | Equipo / pendiente |

**Importante**: Los estudiantes no deben inventar inconsistencias para completar la tabla. Cuando no encuentren diferencias, pueden registrar «Coherente, sin observaciones», indicando brevemente qué verificaron.

## 4.2 Seguimiento y control

*Fuente: Cronograma (8), riesgos (6), presupuesto (9), calidad (10). Describan cómo realizarán el seguimiento del avance del proyecto, verificando el cumplimiento de las actividades, los plazos, los costos, la disponibilidad de recursos, las respuestas a los riesgos y los criterios de calidad. Definan indicadores o evidencias, frecuencia de revisión y responsables. Expliquen cómo se identificarán las desviaciones y cómo se documentarán las acciones correctivas y los cambios aprobados.*

**A. Matriz de seguimiento y control**

Cada semana el equipo compara lo realizado con lo planificado, cada mes revisa además costos y riesgos. Los resultados de las revisiones actualizan el plan.

| **Qué se controlará** | **Indicador / evidencia** | **Frecuencia** | **Responsable** |
| --- | --- | --- | --- |
| Avance del cronograma | Porcentaje de avance por actividad en GanttProject, comparado con las fechas del cronograma | Semanal | Lukas Garrido |
| Cumplimiento de entregables | Entregables aprobados en los hitos H1 a H6 con su criterio de aceptación cumplido | En cada hito | Lukas Garrido |
| Costos y presupuesto | Horas reales frente a las 894 h presupuestadas y gasto frente a la línea base (9.530.000 CLP) | Mensual | Lukas Garrido |
| Disponibilidad de recursos | Horas trabajadas por persona (3 h/día) y uso del servidor y la base de datos | Semanal | Lukas y Octavio |
| Gestión de riesgos | Revisión de R1 a R9: probabilidad, impacto y exposición | Mensual | Lukas Garrido |
| Cumplimiento de Calidad | Resultados de las pruebas 5.1 a 5.5 frente a los criterios de la matriz de calidad | En las pruebas, antes de H5 | Octavio Valencia |
| Solicitudes de cambio | Registro de cada solicitud de cambio con su efecto en alcance, cronograma y costo | Cuando se solicite | Lukas Garrido (el sponsor, si afecta fecha o presupuesto) |

**B. Procedimiento de seguimiento y actualización**

El equipo controla el proyecto comparando el avance, las horas y el gasto reales con el cronograma y la línea base, y documenta las desviaciones y los cambios aprobados.

| **Elemento a registrar** | **Información del proyecto** |
| --- | --- |
| Frecuencia de revisión | Semanal para avance, recursos y calidad, mensual para costos y riesgos. |
| Identificación de desviaciones | Una actividad con más de 2 días hábiles de atraso (igual a la reserva de cronograma), horas o gasto sobre lo planificado, o un criterio de calidad incumplido (propuesto). |
| Acciones correctivas | Reasignar tareas entre Lukas y Octavio, recortar funciones de menor prioridad o usar la reserva, cada acción se registra con fecha y responsable. |
| Responsable de actualización | Lukas Garrido (líder), con apoyo de Octavio Valencia. |
| Registro de cambios / versiones | Solicitud de cambio escrita y número de versión del plan con su fecha (partiendo de la versión 2.0), los archivos se guardan con versión en el repositorio Git. |
| Actualización de documentos | Tras cada cambio aprobado se actualizan juntos el cronograma (Excel y .gan), el presupuesto y la matriz de calidad para mantener la coherencia. |

## 4.3 Aprobación del plan

*Indicaciones: Fuente: Acta (1) y gobernanza. Definan quién revisa y aprueba el plan, no indiquen aprobado si no existe aprobación real.*

| **Rol / autoridad** | **Nombre** | **Estado / fecha** |
| --- | --- | --- |
| Responsable del proyecto | Lukas Garrido | Pendiente de revisión |
| Patrocinador / autoridad | Empresas (sponsor) | Pendiente de aprobación |

# 5. Anexos y archivos de respaldo

*Indicaciones: Adjuntar los Excel originales editables. Otros Word o evidencias se incorporan como respaldo cuando se necesiten. Verifiquen que el informe cite correctamente cada anexo.*

| **Anexo** | **Documento de respaldo** | **Nombre del archivo / versión** |
| --- | --- | --- |
| A | Alcance–EDT–Diccionarios (Excel, entregable 4) | 4- IC-Project-Scope.xlsx (declaración de alcance y diccionario WBS, versión parcial) |
| B | Cronograma (Excel, entregable 8) | LiciFlow_Cronograma.xlsx y LiciFlow.gan (GanttProject) |
| C | Presupuesto (Excel, entregable 9) | 8_presupuesto_LiciFlow.xlsx |
| D | Otros documentos y evidencias, si corresponde | Acta de constitución (E1), registro de interesados (1_2__Stakeholders) y 9_Calidad_LiciFlow.docx |

## Lista de comprobación antes de entregar

**Antes de enviar el Plan de Gestión del Proyecto, verifiquen lo siguiente:**

- Se completaron todas las secciones del informe, utilizando la información del proyecto desarrollado por el equipo.

- Se integró la información de los nueve entregables anteriores en las secciones correspondientes.

- Los códigos, actividades y paquetes de trabajo son coherentes entre la EDT, el cronograma, la matriz RAM y el presupuesto.

- Los responsables asignados coinciden con los roles definidos en el organigrama y la matriz RAM.

- Los riesgos incluyen estrategias de respuesta, responsables y su relación con los planes afectados.

- Los requisitos de calidad cuentan con indicadores medibles, criterios de aceptación, métodos de verificación y responsables.

- El presupuesto total, la línea base de costos y las reservas coinciden con la información del archivo Excel.

- Se adjuntaron los tres archivos Excel originales y editables como anexos.

- Las tablas, diagramas e imágenes incorporadas son legibles y corresponden a la versión actualizada del proyecto.

- Se revisaron la redacción, ortografía, nombres de archivos, formato y versión final del informe.

# Ejemplo de verificación cruzada

Requisito: impedir dos reservas simultáneas del mismo laboratorio y horario. 

- Alcance: función de validación de conflictos. 

- EDT: diseño, programación y pruebas. 

- Cronograma: reservar tiempo para desarrollo y pruebas. 

- Recursos: analista, desarrollador y QA. 

- Presupuesto: sus actividades deben figurar en la estimación. 

- Riesgo: fallas de concurrencia. 

- Calidad: cero reservas duplicadas en escenarios de prueba. 

- Interesados: coordinación de laboratorios valida el comportamiento esperado.

---

Project Management Institute · PMBOK® 8 ·