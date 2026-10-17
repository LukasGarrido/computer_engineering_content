---
tags:
  - indice
  - meta
tipo: indice
---

# Índice Global del Wiki

> Catálogo completo de todas las páginas del wiki de Ingeniería Informática — USM.
> Última actualización: 2026-10-17

---

## Maps of Content (por asignatura)

| Asignatura | MOC | Notas | Descripción |
|:---|:---|:---:|:---|
| **Ciencia de Datos** | [[_MOC\|MOC Ciencia de Datos]] | 14 | DS, ML, regresión, SVM, ensembles, grafos, deployment |
| **Gestión de Proyectos** | [[_MOC\|MOC Gestión de Proyectos]] | 13 | Fundamentos, metodologías, Scrum, PMBOK 8 (Inicio, Alcance, EDT, Interesados, Riesgos, Cronograma, Finanzas, Calidad), proyecto LiciFlow |
| **Inteligencia de Negocio** | [[_MOC\|MOC Inteligencia de Negocio]] | 8 | BI, Data Warehouse, OLTP→OLAP, proyecto SaludVital (análisis y arquitectura ETL) |
| **Redes de Computadores** | [[_MOC\|MOC Redes de Computadores]] | 10 | Capas TCP/IP, plano de datos/control, seguridad, certámenes |
| **Responsabilidad Social** | [[_MOC\|MOC Responsabilidad Social]] | 2 | Ética profesional, RSE, norma ISO 26000, programa de RSE y mapeo de stakeholders |
| **Taller de Admin. Sistemas** | [[_MOC\|MOC TAS]] | 6 | Linux, Docker, DNS, firewall, Nginx, almacenamiento |
| **Visualización** | [[_MOC\|MOC Visualización]] | 17 | Power BI, PCA, t-SNE, UMAP, clustering, NLP, evaluación C9, curvas ROC, SHAP (Lab S9) |

---

## Conceptos Transversales (`wiki/_conceptos/`)

Páginas-hub que conectan conocimiento entre asignaturas:

### Ciencia de Datos & ML
- [[Machine Learning]] — IA, aprendizaje supervisado/no supervisado
- [[Regresion Lineal]] — modelos lineales y logísticos
- [[Clustering]] — K-Means, DBSCAN, jerárquico
- [[PCA]] — reducción de dimensionalidad
- [[Metricas de Evaluacion]] — accuracy, precision, recall, F1, MSE, curvas ROC/AUC, validación cruzada y SHAP
- [[Series de Tiempo]] — análisis temporal y forecasting
- [[Redes Neuronales]] — deep learning, CNN

### Gestión & Metodologías
- [[Metodologias Agiles]] — Scrum, Kanban
- [[CRISP-DM]] — metodología para proyectos de datos

### Business Intelligence
- [[Data Warehouse]] — bodegas de datos y modelado dimensional
- [[OLTP vs OLAP]] — sistemas transaccionales vs analíticos
- [[ETL]] — Extract, Transform, Load (arquitectura y auditoría en SaludVital)
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
- [[Etica Profesional]] — ética y responsabilidad social en ingeniería e ISO 26000
- [[Gestion de Interesados]] — identificación, matriz poder/interés y participación de stakeholders en GP, RSE y BI

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
