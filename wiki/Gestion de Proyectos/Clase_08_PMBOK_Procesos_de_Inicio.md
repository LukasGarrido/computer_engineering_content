---
tags:
  - gestion-de-proyectos
  - teoria
  - pmbok
  - project-charter
  - stakeholders
aliases:
  - "Clase 08 Gestión de Proyectos"
  - "Procesos de Inicio PMBOK 8"
  - "Acta de Constitución y Registro de Interesados"
asignatura: "Gestión de Proyectos"
tipo: teoria
created: 2026-09-10
---

# Clase 08 — PMBOK® 8: Procesos de Inicio, Acta de Constitución y Registro de Interesados

> Los dos procesos que formalizan el nacimiento de un proyecto: Iniciar el proyecto o fase (Gobernanza 1.1) e Identificar a los interesados (Interesados 5.1). Elaboración del Project Charter y diseño de la Matriz Poder vs. Interés. Clase dictada por la Dra. Gerlys Villalobos Fontalvo (USM).

---

## 1. El Propósito de la Fase de Inicio

La fase de Inicio transforma una idea o necesidad difusa en un **proyecto formalmente autorizado y delimitado**, respondiendo a tres interrogantes fundamentales:

> *¿Qué proyecto vamos a realizar, por qué es necesario y quiénes están involucrados?*

En el estándar PMBOK® 8, la fase de inicio concentra exactamente **2 procesos**:

```text
       ┌────────────────────────────────────────────────────────┐
       │                FASE DE INICIO (PMBOK 8)                │
       └───────────────────────────┬────────────────────────────┘
                                   │
         ┌─────────────────────────┴────────────────────────┐
         ▼                                                  ▼
   [Proceso 1.1]                                      [Proceso 5.1]
Iniciar el proyecto o fase                         Identificar interesados
 (Área 1: Gobernanza)                               (Área 5: Interesados)
         │                                                  │
         ▼                                                  ▼
Acta de Constitución                               Registro Inicial de
 (Project Charter)                                     Interesados
```

---

## 2. Proceso 1.1: Iniciar el Proyecto o Fase (Acta de Constitución)

### 2.1 Definición y Alcance del Project Charter
El **Acta de Constitución del Proyecto** (*Project Charter*) es el documento formal emitido por el patrocinador (*sponsor*) que autoriza formalmente la existencia del proyecto y otorga al director del proyecto la autoridad para asignar recursos de la organización.

> [!IMPORTANT]
> El Acta de Constitución **no es el Plan de Gestión del Proyecto**. Contiene información estratégica y de alto nivel que posteriormente será detallada durante la fase de planificación.

### 2.2 Estructura del Acta de Constitución

| N° | Elemento | Pregunta guía | Descripción |
|---|---|---|---|
| **1** | **Nombre del proyecto** | *¿Cómo lo identificamos?* | Nombre formal, código y versión. |
| **2** | **Problema / Necesidad** | *¿Qué situación resolvemos?* | Origen, dolor operativo o brecha del negocio. |
| **3** | **Justificación** | *¿Por qué es necesario?* | Razón estratégica o económica que respalda la inversión. |
| **4** | **Objetivo general** | *¿Qué queremos lograr?* | Resultado final esperado (redactado con criterio SMART). |
| **5** | **Solución inicial** | *¿Qué proponemos desarrollar?* | Descripción preliminar del producto, servicio o sistema. |
| **6** | **Beneficios esperados** | *¿Qué valor generará?* | Mejoras cuantificables o cualitativas proyectadas. |
| **7** | **Alcance inicial** | *¿Qué incluye y qué no incluye?* | Fronteras preliminares para evitar expectativas desalineadas. |
| **8** | **Restricciones iniciales** | *¿Qué limitaciones existen?* | Topes presupuestarios, plazos fatales, normativas o tecnologías mandatorias. |
| **9** | **Supuestos iniciales** | *¿Bajo qué condiciones operamos?* | Factores considerados verdaderos para planificar, pendientes de verificación. |
| **10** | **Sponsor y Director** | *¿Quién respalda y quién gestiona?* | Autoridad patrocinadora y asignación del líder de proyecto. |

### 2.3 Restricciones vs. Supuestos

- **Restricciones:** Condiciones que **limitan** de forma obligatoria las decisiones del equipo (ej. *"El presupuesto no puede exceder $10.000.000 CLP"*, *"El sistema debe desplegarse en servidores institucionales"*).
- **Supuestos:** Factores que el equipo asume como **verdaderos o garantizados** para poder avanzar con la planificación (ej. *"La universidad facilitará las APIs de autenticación"*). Si un supuesto resulta ser falso, se convierte de inmediato en un **riesgo** que afecta alcance, tiempo o costos.

---

## 3. Proceso 5.1: Identificar a los Interesados (Stakeholders)

### 3.1 ¿Qué es un Interesado?
Un **interesado** (*stakeholder*) es cualquier persona, grupo u organización que puede afectar, verse afectada o percibirse afectada por una decisión, actividad o resultado del proyecto.

> [!WARNING]
> **Interesado $\neq$ Usuario:** Todos los usuarios finales son interesados, pero muchos interesados clave **nunca utilizarán directamente el software** (patrocinadores, auditores, comités de ética, administradores de infraestructura, directivos).

### 3.2 Matriz Poder vs. Interés

Permite priorizar a los interesados y definir la estrategia de involucramiento y comunicación:

| Nivel de Poder \ Interés | Interés Bajo | Interés Alto |
|---|---|---|
| **Poder / Influencia Alto** | **Mantener satisfecho**<br>*(Estrategia: Reportes ejecutivos, consultas puntuales)* | **Gestionar de cerca**<br>*(Estrategia: Reuniones periódicas, co-decisión, patrocinador clave)* |
| **Poder / Influencia Bajo** | **Monitorear**<br>*(Estrategia: Comunicación masiva pasiva, mínimo esfuerzo)* | **Mantener informado**<br>*(Estrategia: Boletines, demos, consultas de feedback)* |

### 3.3 Registro Inicial de Interesados

Estructura de la tabla del registro:
1. **Identificación:** Nombre del interesado o grupo, rol y contacto.
2. **Clasificación:** Interno (dentro de la organización ejecutora) o Externo (clientes, proveedores, entes reguladores).
3. **Evaluación:** Nivel de poder (Alto/Medio/Bajo), nivel de interés (Alto/Medio/Bajo).
4. **Expectativas y Necesidades:** Qué espera conseguir o qué teme que ocurra.
5. **Estrategia Inicial:** Cómo y con qué periodicidad se interactuará con él.

---

## 4. Aplicación Práctica y Entregables

En la metodología de taller del curso, esta clase sienta las bases para los primeros entregables del proyecto semestral:
- **Entregable 1:** Acta de Constitución del Proyecto formalizada.
- **Entregable 2:** Registro de Interesados y Matriz Poder/Interés.

Para la implementación documentada en este wiki, véase el proyecto [[LiciFlow_Documentacion|LiciFlow (CRM de Licitaciones de Mercado Público)]], donde las Secciones 1 y 3 corresponden directamente a estos dos procesos.

---

## Véase también
- [[_MOC|MOC Gestión de Proyectos]]
- [[Clase_07_Estandar_PMBOK_8|Clase 07 — Estándar PMBOK 8]]
- [[Clase_09_PMBOK_Planificacion_Alcance_EDT|Clase 09 — Planificación del Alcance y EDT]]
- [[LiciFlow_Documentacion|Proyecto Semestral LiciFlow]]
- [[Etica Profesional]]
