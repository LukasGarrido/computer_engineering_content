---
tags:
  - gestion-de-proyectos
  - teoria
  - pmbok
  - stakeholders
  - comunicaciones
  - recursos
  - raci-ram
aliases:
  - "Clase 10 Gestión de Proyectos"
  - "Interesados, Comunicaciones y Recursos"
  - "Matriz RACI y RAM"
asignatura: "Gestión de Proyectos"
tipo: teoria
created: 2026-09-24
---

# Clase 10 — PMBOK® 8: Planificación de Interesados, Comunicaciones y Recursos

> Planificación de la participación de los interesados, diseño de la estrategia y matriz de comunicaciones, gestión de recursos humanos y técnicos, organigramas y Matriz de Asignación de Responsabilidades (RAM / RACI). Clase dictada por la Dra. Gerlys Villalobos Fontalvo (USM).

---

## 1. Planificación del Involucramiento de los Interesados (Proceso 5.2)

El proceso **5.2 Planificar el Involucramiento de los Interesados** define las estrategias y acciones para promover una participación activa y constructiva a lo largo de todo el ciclo de vida del proyecto.

### 1.1 Niveles de Participación
Para cada interesado identificado en el Registro Inicial (Proceso 5.1), se establece el nivel de participación más adecuado:

| Nivel | Enfoque | Acciones típicas |
|---|---|---|
| **Informar** | Unidireccional | Mantener al interesado al tanto de avances, decisiones y fechas clave mediante reportes o boletines. |
| **Consultar** | Bidireccional | Solicitar su opinión, requerimientos o retroalimentación previa a la toma de decisiones. |
| **Involucrar** | Trabajo conjunto | Incorporarlo en discusiones, talleres de requerimientos y mesas de trabajo. |
| **Colaborar** | Co-decisión | Trabajar conjuntamente como socios para definir soluciones e innovaciones. |
| **Empoderar** | Delegación | Otorgar autoridad y autonomía para decidir aspectos específicos del proyecto. |

---

## 2. Planificación de las Comunicaciones (Proceso 5.3)

El proceso **5.3 Planificar la Gestión de las Comunicaciones** establece qué información necesita cada interesado, cuándo, a través de qué medio y quién es el responsable de transmitirla.

### 2.1 Medios y Tipos de Comunicación

| Tipo \ Medio | Verbal | Escrita |
|---|---|---|
| **Formal** | Presentaciones ejecutivas, defensas de hitos, reuniones de comité. | Firma de contratos, actas de acuerdos, aprobación formal de entregables. |
| **Informal** | Llamadas telefónicas, conversaciones de pasillo, syncs rápidos. | Correos electrónicos, mensajes por chat de equipo (Teams/Slack), notas. |

### 2.2 Barreras para la Comunicación y Medidas Preventivas

| Barrera detectada | Causa u origen | Medida preventiva recomendada |
|---|---|---|
| **Falta de claridad** | Mensajes ambiguos o metas no explícitas | Usar plantillas estandarizadas, lenguaje directo y confirmación de entendimiento. |
| **Distancia física** | Equipos distribuidos o remotos | Fijar herramientas oficiales (Teams, Discord), cámaras activas y canales documentados. |
| **Lenguaje técnico excesivo** | Brecha entre desarrolladores y clientes de negocio | Adaptar el vocabulario al perfil del interesado (evitar jerga de código con directivos). |
| **Exceso de información (*Infoxicación*)** | Envío indiscriminado de reportes extensos | Segmentar los reportes: resúmenes ejecutivos para directivos y detalle técnico para soporte. |

### 2.3 Matriz de Gestión de las Comunicaciones

| Interesado / Destinatario | Información que recibirá | Medio o Canal | Frecuencia | Responsable |
|---|---|---|---|---|
| **Sponsor / Dirección** | Avance general, presupuesto, riesgos críticos | Informe mensual + Reunión ejecutiva | Mensual | Líder del Proyecto |
| **Usuarios clave** | Requisitos, demos funcionales, pruebas | Taller presencial / Teams | Quincenal | Analista de Requisitos |
| **Equipo de Desarrollo** | Tareas, dependencias técnicas, bloqueos | Daily Scrum / Tablero Kanban | Diario / Semanal | Líder / Scrum Master |
| **Soporte de TI / Infraestructura** | Requerimientos de servidores y seguridad | Correo institucional + Reunión técnica | Semanal | Ingeniero de Despliegue |

---

## 3. Planificación de la Gestión de Recursos (Proceso 6.1)

El área clave de Recursos comprende la identificación, obtención y coordinación de todos los medios requeridos para ejecutar las actividades.

### 3.1 Tipos de Recursos en Proyectos de TI
1. **Recursos Físicos:** Instalaciones, laboratorios, mobiliario, insumos.
2. **Recursos Técnicos:** Hardware, estaciones de trabajo, servidores cloud, licencias de software, herramientas IDE, repositorios.
3. **Recursos Financieros:** Presupuesto asignado, caja operativa y reservas.
4. **Recursos Humanos:** Equipo multidisciplinario con sus habilidades, roles, experiencia y disponibilidad horaria.

### 3.2 Organigrama del Proyecto y Estructura Organizacional
- **Organización Departamental (por Fase):** Estructura el equipo según etapas del ciclo de vida (Análisis y Diseño $\rightarrow$ Desarrollo $\rightarrow$ Pruebas y Despliegue).
- **Organización por Tipo de Recurso:** Agrupa por especialidades funcionales (Recursos Humanos, Recursos Financieros, Recursos Tecnológicos).

### 3.3 Descripción de Puestos de Trabajo
Cada rol del equipo debe tener formalmente definidos cuatro pilares:
- **Rol:** Nombre y función asignada (ej. *Líder de Proyecto*, *Desarrollador Fullstack*, *Analista QA*).
- **Responsabilidades:** Deberes específicos y entregables a cargo.
- **Autoridad:** Grado de decisión sobre presupuesto, cambios técnicos y asignación de tareas.
- **Competencia:** Conocimientos técnicos, experiencia requerida y habilidades blandas necesarias.

---

## 4. Matriz de Asignación de Responsabilidades (RAM / RACI)

La **RAM** (*Responsibility Assignment Matrix*) cruza el listado de actividades o paquetes de trabajo de la EDT con los miembros del equipo, aclarando el nivel de participación exacto:

| Nivel de Responsabilidad | Código Estándar | Definición |
|---|:---:|---|
| **Principal / Responsible** | **P** (o **R**) | Responsable directo de ejecutar el trabajo de la actividad. |
| **Secundaria / Accountable/Support** | **S** (o **A**) | Apoya o participa en la ejecución; asegura que se cumpla el entregable. |
| **Consulta / Consulted** | **C** | Especialista al que se le consulta información técnica o requisitos. |
| **Informado / Informed** | **I** | Persona a la que se le notifica el avance o resultado final. |

### Ejemplo aplicado a un Proyecto de Software:

| Actividad / Paquete EDT | Líder de Proyecto | Analista Requisitos | Dev Backend | Dev Frontend | QA / Tester |
|---|:---:|:---:|:---:|:---:|:---:|
| **1.1 Definir requisitos** | **P** | **P** | S | S | C |
| **1.2 Diseño de arquitectura** | **P** | S | **P** | S | C |
| **1.3 Desarrollo de API y BD** | I | C | **P** | S | S |
| **1.4 Desarrollo de interfaz UI** | I | C | S | **P** | S |
| **1.5 Pruebas de integración** | I | S | S | S | **P** |
| **1.6 Despliegue en producción** | **P** | S | S | S | C |

---

## 5. Proceso 6.2: Estimar los Recursos de las Actividades

Consiste en cuantificar de forma rigurosa los insumos necesarios para cada paquete de trabajo, especificando:
- Perfil requerido y cantidad de personas/horas.
- Infraestructura o servidores (ej. *1 Servidor de pruebas AWS EC2 durante 4 meses*).
- Licencias o herramientas especializadas.

Esta estimación de recursos constituye el insumo directo e indispensable para la **planificación del cronograma** y la **estimación presupuestaria**.

---

## Véase también
- [[_MOC|MOC Gestión de Proyectos]]
- [[Clase_08_PMBOK_Procesos_de_Inicio|Clase 08 — Procesos de Inicio PMBOK 8]]
- [[Clase_09_PMBOK_Planificacion_Alcance_EDT|Clase 09 — Planificación del Alcance y EDT]]
- [[Clase_11_PMBOK_Gestion_de_Riesgos_Identificacion_y_Analisis|Clase 11 — Gestión de Riesgos: Identificación y Análisis]]
- [[LiciFlow_Documentacion|Proyecto Semestral LiciFlow]]
