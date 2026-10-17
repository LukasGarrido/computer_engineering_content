---
tags:
  - gestion-de-proyectos
  - teoria
  - pmbok
  - alcance
  - wbs-edt
aliases:
  - "Clase 09 Gestión de Proyectos"
  - "Planificación del Alcance y EDT"
  - "WBS y Diccionario de la EDT"
asignatura: "Gestión de Proyectos"
tipo: teoria
created: 2026-09-22
---

# Clase 09 — PMBOK® 8: Planificación del Alcance, Declaración de Alcance y EDT/WBS

> La fase de planificación en el estándar PMBOK 8. Gobernanza del plan general y los 4 procesos del área de Alcance: recopilación de requisitos, Declaración de Alcance (*Scope Statement*), descomposición jerárquica mediante la EDT/WBS y diseño del Diccionario de la EDT. Clase dictada por la Dra. Gerlys Villalobos Fontalvo (USM).

---

## 1. La Fase de Planificación en PMBOK® 8

La fase de planificación es el corazón del estándar y agrupa **19 procesos** distribuidos en las 7 áreas clave:

> *¿Cómo lo vamos a realizar, con qué recursos, en qué plazos y con qué controles?*

En esta clase se abordan el plan de gobernanza general y la línea base del alcance:
- **Gobernanza (Proceso 1.2):** Desarrollar el Plan de Gestión del Proyecto (plan integrado que consolida los planes subsidiarios de alcance, tiempo, costo, calidad, recursos, comunicaciones y riesgos).
- **Alcance (Procesos 2.1 a 2.4):** Definir qué trabajo forma parte del proyecto y cuál queda explícitamente excluido.

---

## 2. Los 4 Procesos de Planificación del Alcance

```text
  [Proceso 2.1]                      [Proceso 2.2]
Planificar gestión  ──────────────►  Recopilar y analizar
  del alcance                         los requisitos
       │                                    │
       ▼                                    ▼
Documento de enfoque                Matriz de Requisitos
       │                                    │
       └─────────────────┬──────────────────┘
                         ▼
                   [Proceso 2.3]
                 Definir el alcance
                         │
                         ▼
              Declaración de Alcance
                 (Scope Statement)
                         │
                         ▼
                   [Proceso 2.4]
                  Crear la EDT/WBS
                         │
                         ▼
                Línea Base del Alcance:
             EDT + Diccionario de la EDT
```

### 2.1 Proceso 2.1: Planificar la Gestión del Alcance
Define cómo se identificará, validará y controlará el alcance a lo largo del ciclo de vida del proyecto, estableciendo herramientas, criterios de aceptación y responsabilidades.

### 2.2 Proceso 2.2: Recopilar y Analizar los Requisitos
Identifica las necesidades de los clientes y demás interesados mediante:
- **Entrevistas estructuradas y semiestructuradas.**
- **Talleres de facilitación y lluvia de ideas.**
- **Encuestas y cuestionarios.**
- **Análisis de documentos y benchmarking.**
Los requisitos se categorizan en funcionales (RF) y no funcionales (RNF: rendimiento, seguridad, disponibilidad, usabilidad).

### 2.3 Proceso 2.3: Definir el Alcance (Scope Statement)
Desarrolla la **Declaración de Alcance del Proyecto**, delimitando formalmente:
1. **Objetivos del proyecto:** Alineados con las metas del negocio.
2. **Entregables principales:** Productos o resultados verificables.
3. **Lista de tareas:** Trabajo necesario para generar cada entregable.
4. **Fuera del alcance (*Exclusiones explícitas*):** Todo aquello que **no** será desarrollado. *Definir lo que no se hace es tan crítico como definir lo que sí se hace para evitar el deslizamiento del alcance (Scope Creep).*
5. **Supuestos y Restricciones actualizados.**

---

## 3. Proceso 2.4: Crear la EDT / WBS (Estructura de Desglose del Trabajo)

### 3.1 ¿Qué es la EDT?
La **Estructura de Desglose del Trabajo** (*Work Breakdown Structure - WBS*) es una descomposición jerárquica orientada a entregables de todo el trabajo que el equipo debe ejecutar.

> [!IMPORTANT]
> **La Regla del 100%:** La EDT debe incluir el 100% del trabajo definido en el alcance, ni más ni menos. El conjunto de actividades y entregables de cada nivel inferior debe sumar exactamente el 100% del componente padre.

### 3.2 Jerarquía y Niveles de la EDT

```text
Nivel 1: Proyecto Completo (ej. 1.0 Sistema de Reservas de Laboratorios)
  │
  ├── Nivel 2: Entregable Mayor o Fase (ej. 1.1 Requisitos del Sistema)
  │     ├── Nivel 3: Paquete de Trabajo (ej. 1.1.1 Levantamiento de Requisitos)
  │     └── Nivel 3: Paquete de Trabajo (ej. 1.1.2 Especificación de Requisitos)
  │
  ├── Nivel 2: Entregable Mayor (ej. 1.2 Diseño del Sistema)
  │     ├── Nivel 3: Paquete de Trabajo (ej. 1.2.1 Diseño de Interfaces UI/UX)
  │     └── Nivel 3: Paquete de Trabajo (ej. 1.2.2 Diseño de Base de Datos)
  │
  └── Nivel 2: Entregable Mayor (ej. 1.3 Desarrollo del Prototipo)
        ├── Nivel 3: Paquete de Trabajo (ej. 1.3.1 Módulo de Reservas)
        └── Nivel 3: Paquete de Trabajo (ej. 1.3.2 Módulo de Autenticación)
```

- **Paquete de trabajo (*Work Package*):** Es el nivel más bajo de la EDT. Debe tener un tamaño suficientemente manejable para que se le pueda asignar un responsable único, estimar duración y costo, y verificar su cumplimiento.
- **Importante:** La EDT muestra **QUÉ** se va a hacer, **NO CUÁNDO** ni en qué secuencia (eso corresponde al cronograma).

---

## 4. El Diccionario de la EDT

El **Diccionario de la EDT** es el documento que complementa a la EDT gráfica describiendo en detalle cada paquete de trabajo:

| Campo del Diccionario | Descripción / Contenido |
|---|---|
| **Código del paquete** | Numeración jerárquica (ej. `1.3.2`). |
| **Nombre de la tarea** | Denominación clara del paquete. |
| **Descripción detallada** | Explicación del trabajo a ejecutar. |
| **Entregable asociado** | Artefacto resultante verificable. |
| **Responsable** | Rol o persona encargada de liderar la actividad. |
| **Tiempo estimado** | Duración esperada en días/semanas. |
| **Costo estimado** | Presupuesto preliminar asignado al paquete. |
| **Criterios de aceptación** | Condiciones cuantitativas o cualitativas para validar la entrega (ej. *"$\ge 95\%$ pruebas exitosas"*). |
| **Recursos requeridos** | Perfiles, servidores, licencias o equipos necesarios. |
| **Dependencias** | Paquetes previos indispensables para iniciar este trabajo. |

---

## 5. Entregables Académicos y Aplicación

Esta clase habilita la formulación de tres entregables clave:
- **Entregable 3:** Plan de Gestión del Proyecto (documento Word integrador).
- **Entregable 4:** Línea Base del Alcance y Scope Statement (plantilla Excel).
- **Entregable 4B y 5:** Diagrama de la EDT y Diccionario de la EDT.

Véase en el proyecto [[LiciFlow_Documentacion]] las Secciones 2 (*Definición del Proyecto y Alcance MVP*), 4 (*Requerimientos Funcionales y No Funcionales*) y 5 (*Arquitectura del Sistema*), formuladas conforme a este estándar.

---

## Véase también
- [[_MOC|MOC Gestión de Proyectos]]
- [[Clase_08_PMBOK_Procesos_de_Inicio|Clase 08 — Procesos de Inicio PMBOK 8]]
- [[Clase_10_PMBOK_Interesados_Comunicaciones_Recursos|Clase 10 — Interesados, Comunicaciones y Recursos]]
- [[Clase_13_PMBOK_Gestion_del_Cronograma|Clase 13 — Gestión del Cronograma y PERT]]
- [[LiciFlow_Documentacion|Proyecto Semestral LiciFlow]]
