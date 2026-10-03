---
tags:
  - indice
  - meta
tipo: indice
---

# Índice Global del Wiki

> Catálogo completo de todas las páginas del wiki de Ingeniería Informática — USM.
> Última actualización: 2026-10-03

---

## Maps of Content (por asignatura)

| Asignatura | MOC | Notas | Descripción |
|:---|:---|:---:|:---|
| **Ciencia de Datos** | [[_MOC\|MOC Ciencia de Datos]] | 14 | DS, ML, regresión, SVM, ensembles, grafos, deployment |
| **Gestión de Proyectos** | [[_MOC\|MOC Gestión de Proyectos]] | 4 | Fundamentos, planificación, metodologías, Scrum |
| **Inteligencia de Negocio** | [[_MOC\|MOC Inteligencia de Negocio]] | 8 | BI, Data Warehouse, OLTP→OLAP, proyecto SaludVital |
| **Redes de Computadores** | [[_MOC\|MOC Redes de Computadores]] | 10 | Capas TCP/IP, seguridad, certámenes |
| **Responsabilidad Social** | [[_MOC\|MOC Responsabilidad Social]] | 1 | Ética profesional y RSE |
| **Taller de Admin. Sistemas** | [[_MOC\|MOC TAS]] | 6 | Linux, Docker, DNS, firewall, Nginx |
| **Visualización** | [[_MOC\|MOC Visualización]] | 13 | Power BI, PCA, t-SNE, clustering, NLP |

---

## Conceptos Transversales (`wiki/_conceptos/`)

Páginas-hub que conectan conocimiento entre asignaturas:

### Ciencia de Datos & ML
- [[Machine Learning]] — IA, aprendizaje supervisado/no supervisado
- [[Regresion Lineal]] — modelos lineales y logísticos
- [[Clustering]] — K-Means, DBSCAN, jerárquico
- [[PCA]] — reducción de dimensionalidad
- [[Metricas de Evaluacion]] — accuracy, precision, recall, F1, MSE
- [[Series de Tiempo]] — análisis temporal y forecasting
- [[Redes Neuronales]] — deep learning, CNN

### Gestión & Metodologías
- [[Metodologias Agiles]] — Scrum, Kanban
- [[CRISP-DM]] — metodología para proyectos de datos

### Business Intelligence
- [[Data Warehouse]] — bodegas de datos y modelado dimensional
- [[OLTP vs OLAP]] — sistemas transaccionales vs analíticos
- [[ETL]] — Extract, Transform, Load
- [[Power BI]] — herramienta de visualización y BI

### Redes & Sistemas
- [[Modelo OSI y TCP-IP]] — modelos de capas de red
- [[DNS]] — Sistema de Nombres de Dominio
- [[TCP y UDP]] — protocolos de transporte
- [[Seguridad en Redes]] — criptografía, firewalls, autenticación
- [[Linux]] — administración de sistemas
- [[Docker]] — contenedores y despliegue

### Visualización & Procesamiento
- [[Procesamiento de Imagenes]] — visión por computador
- [[NLP]] — procesamiento de lenguaje natural

### Transversales
- [[Etica Profesional]] — ética y responsabilidad social en ingeniería

---

## Estructura del Repositorio

```text
wiki/              ← Notas procesadas (Markdown + frontmatter)
raw/               ← Fuentes inmutables (PDFs, notebooks, SQL, etc.)
AGENTS.md          ← Schema y reglas del wiki
index.md           ← Este archivo
log.md             ← Registro cronológico
llm-wiki.md        ← Referencia del patrón
```

---

> Para entender cómo funciona este wiki, consulta [[AGENTS]] y [[llm-wiki]].
