# Material de Ingeniería Informática — USM

Este repositorio contiene apuntes, laboratorios, proyectos y resúmenes de asignaturas de la carrera de **Ingeniería Informática** en la **Universidad Técnica Federico Santa María (USM)**.

Está estructurado bajo el patrón **LLM-Wiki**, diseñado para ser gestionado y evolucionado por agentes de IA en colaboración con humanos, optimizado para ser explorado en **Obsidian** y **GitHub**.

> [!NOTE]
> Todos los materiales docentes, enunciados y diapositivas incluidos en este repositorio pertenecen y han sido provistos por la **Universidad Técnica Federico Santa María (USM)**.

---

## Arquitectura del Repositorio (3 Capas)

El repositorio sigue una arquitectura estricta de 3 capas, definida en detalle en [`AGENTS.md`](./AGENTS.md):

```text
/
├── AGENTS.md          ← Schema, reglas y flujos de trabajo del LLM-Wiki
├── index.md           ← Índice global navegable
├── log.md             ← Registro cronológico de cambios de agentes
├── llm-wiki.md        ← Referencia teórica del patrón
│
├── wiki/              ← Notas procesadas y enriquecidas (Markdown)
│   ├── <Asignatura>/  ← Carpeta por asignatura (contiene su _MOC.md)
│   └── _conceptos/    ← Páginas-hub de conceptos transversales
│
├── raw/               ← Fuentes inmutables de solo lectura (PDFs, scripts, etc.)
│   ├── <Asignatura>/  
│   └── assets/        
│
└── .obsidian/         ← Configuración del vault de Obsidian
```

---

## Asignaturas Disponibles

El catálogo principal y la navegación se encuentran en [`index.md`](./index.md).

Las asignaturas documentadas actualmente incluyen:

| Asignatura | Carpeta Wiki | Contenido Principal |
| :--- | :--- | :--- |
| **Ciencia de Datos** | [`wiki/Ciencia de Datos/`](./wiki/Ciencia%20de%20Datos) | Fundamentos de DS, ML, regresión, SVM, ensembles, grafos y deployment. |
| **Gestión de Proyectos** | [`wiki/Gestion de Proyectos/`](./wiki/Gestion%20de%20Proyectos) | Fundamentos de gestión, planificación, metodologías ágiles y Scrum. |
| **Inteligencia de Negocio** | [`wiki/Inteligencia de Negocio/`](./wiki/Inteligencia%20de%20Negocio) | BI, Data Warehouse, modelado dimensional (OLTP a OLAP) y Proyecto SaludVital. |
| **Redes de Computadores** | [`wiki/Redes de Computadores/`](./wiki/Redes%20de%20Computadores) | Capas TCP/IP, seguridad en redes y certámenes. |
| **Responsabilidad Social y Ética Laboral** | [`wiki/Responsabilidad Social y Etica/`](./wiki/Responsabilidad%20Social%20y%20Etica) | Análisis ético en ingeniería y RSE. |
| **Taller de Administración de Sistemas** | [`wiki/Taller de Administracion de Sistemas/`](./wiki/Taller%20de%20Administracion%20de%20Sistemas) | Linux, contenedores (Docker), servicios de red (DNS, firewall). |
| **Visualización** | [`wiki/Visualizacion/`](./wiki/Visualizacion) | Power BI, mapas, alta dimensionalidad (PCA/t-SNE) y NLP. |

---

## Navegación y Uso

Se recomienda abrir este repositorio completo como un "Vault" en **Obsidian** para aprovechar la navegación mediante grafos, las consultas dinámicas (Dataview) y los *wikilinks* entre conceptos transversales de distintas asignaturas.

Para ver el estado actual de los apuntes y todas las conexiones, visita el **[Índice Global](./index.md)**.
