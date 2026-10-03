---
description: Schema del LLM-Wiki para el repositorio de Ingeniería Informática USM
version: 1.0.0
updated: 2026-10-03
---

# AGENTS.md — Schema del Wiki

Este documento define las reglas, convenciones y flujos de trabajo para que un agente LLM mantenga y evolucione este wiki personal de apuntes de **Ingeniería Informática (USM)**.

---

## 1. Arquitectura del Repositorio (3 capas)

```text
/
├── AGENTS.md          ← Este archivo (schema y reglas)
├── index.md           ← Índice global del wiki
├── log.md             ← Registro cronológico de cambios
├── llm-wiki.md        ← Referencia del patrón LLM-Wiki
│
├── wiki/              ← Notas procesadas (Markdown)
│   ├── <Asignatura>/  ← Una carpeta por asignatura
│   │   ├── _MOC.md    ← Map of Content de la asignatura
│   │   └── *.md       ← Notas de teoría, labs, certámenes
│   └── _conceptos/    ← Páginas-hub de conceptos transversales
│
├── raw/               ← Fuentes inmutables (NUNCA modificar)
│   ├── <Asignatura>/  ← PDFs, notebooks, CSVs, SQL, etc.
│   └── assets/        ← Imágenes y recursos multimedia
│
└── .obsidian/         ← Configuración de Obsidian
```

### Reglas por capa

| Capa | Quién escribe | Quién lee | Modificable |
|------|--------------|-----------|-------------|
| `wiki/` | LLM + Humano | Ambos | ✅ Sí |
| `raw/` | Humano (carga archivos) | LLM (para ingestar) | ❌ No |
| `AGENTS.md` | Co-evoluciona (LLM + Humano) | LLM | ✅ Con cuidado |

---

## 2. Convenciones de las Notas

### 2.1 Frontmatter YAML obligatorio

Toda nota en `wiki/` **debe** tener un bloque YAML al inicio con los siguientes campos:

```yaml
---
tags:
  - <asignatura-slug>          # ej: ciencia-de-datos, redes-de-computadores
  - <tipo>                      # teoria | laboratorio | certamen | proyecto | concepto
aliases:
  - "Nombre alternativo"       # Nombres cortos o en inglés para encontrar la nota
asignatura: "<Nombre Completo>" # ej: "Ciencia de Datos"
tipo: <tipo>                    # teoria | laboratorio | certamen | proyecto | concepto
created: YYYY-MM-DD
---
```

### 2.2 Wikilinks para el grafo

- **Usar `[[wikilinks]]`** para referenciar otras notas del wiki.
- Formato: `[[Nombre del archivo sin extensión]]` o `[[Nombre del archivo sin extensión|texto visible]]`.
- **Toda nota debe tener al menos un wikilink** de entrada (desde su MOC o desde otra nota).
- Los conceptos transversales en `wiki/_conceptos/` son hubs: deben ser enlazados desde cualquier nota que toque ese tema.

### 2.3 Secciones especiales

Al final de cada nota de teoría o laboratorio, incluir una sección:

```markdown
---
## Véase también
- [[Nota relacionada 1]]
- [[Nota relacionada 2]]
- [[Concepto transversal]]
```

### 2.4 Nombres de archivo

- **Sin prefijos numéricos de orden** (el orden lo da el MOC).
- **Usar guiones bajos** `_` para separar palabras: `Regresion_Lineal_y_Logistica.md`.
- **Evitar caracteres especiales** en nombres de archivo (tildes, ñ, paréntesis).

---

## 3. Map of Content (_MOC.md)

Cada asignatura tiene un archivo `_MOC.md` que actúa como índice y hub de navegación.

### Estructura del MOC

```markdown
---
tags:
  - <asignatura-slug>
  - moc
tipo: moc
asignatura: "<Nombre>"
---

# <Nombre de la Asignatura> — MOC

> Descripción breve de la asignatura.

## Teoría
- [[Nota 1]]
- [[Nota 2]]

## Laboratorios
- [[Lab 1]]

## Certámenes
- [[Certamen 1]]

## Conceptos Clave
- [[Concepto transversal 1]]
- [[Concepto transversal 2]]
```

---

## 4. Conceptos Transversales (`wiki/_conceptos/`)

Los conceptos que aparecen en **más de una asignatura** tienen su propia página-hub en `wiki/_conceptos/`. Estas páginas:

- Son **stubs con contexto**: no duplican contenido, sino que reúnen enlaces a las notas donde el concepto se desarrolla.
- Tienen frontmatter con `tipo: concepto` y `tags: [concepto]`.
- Incluyen una definición breve y una lista de wikilinks a las notas relevantes.

### Template de concepto

```markdown
---
tags:
  - concepto
aliases:
  - "Nombre alternativo"
tipo: concepto
created: YYYY-MM-DD
---

# <Nombre del Concepto>

> Definición breve (1-3 líneas).

## Aparece en

- [[Nota de asignatura A]] — contexto breve
- [[Nota de asignatura B]] — contexto breve

## Notas
- Observaciones, contradicciones o puntos de conexión entre asignaturas.
```

---

## 5. Flujos de Trabajo (Operaciones)

### 5.1 Ingestar una nueva fuente

1. El humano coloca el archivo fuente en `raw/<Asignatura>/`.
2. El LLM lee el archivo fuente.
3. El LLM crea o actualiza la(s) nota(s) correspondiente(s) en `wiki/<Asignatura>/`.
4. El LLM actualiza el `_MOC.md` de la asignatura.
5. El LLM actualiza las páginas de conceptos transversales en `wiki/_conceptos/` si aplica.
6. El LLM actualiza `index.md`.
7. El LLM registra la acción en `log.md`.

### 5.2 Responder una pregunta (Query)

1. El LLM consulta `index.md` para encontrar páginas relevantes.
2. Lee las páginas necesarias.
3. Sintetiza la respuesta con `[[wikilinks]]` a las fuentes.
4. Si la respuesta es valiosa, se puede archivar como nueva nota en el wiki.

### 5.3 Mantenimiento (Lint)

Periódicamente, verificar:
- [ ] Páginas huérfanas (sin enlaces entrantes).
- [ ] Conceptos mencionados sin página propia en `_conceptos/`.
- [ ] Contradicciones entre notas de distintas asignaturas.
- [ ] Frontmatter incompleto o faltante.
- [ ] MOCs desactualizados.
- [ ] `index.md` desactualizado.

---

## 6. Archivos Especiales

### `index.md`
- Catálogo global de todas las páginas del wiki.
- Organizado por asignatura y tipo.
- Cada entrada tiene: wikilink + resumen de una línea.
- Se actualiza en cada ingest.

### `log.md`
- Registro cronológico append-only.
- Formato de entrada: `## [YYYY-MM-DD] <acción> | <detalle>`
- Acciones: `ingest`, `query`, `lint`, `update`, `create`.

---

## 7. Asignaturas Registradas

| Slug | Nombre | Carpeta Wiki | Carpeta Raw |
|------|--------|-------------|-------------|
| `ciencia-de-datos` | Ciencia de Datos | `wiki/Ciencia de Datos/` | `raw/Ciencia de Datos/` |
| `gestion-de-proyectos` | Gestión de Proyectos | `wiki/Gestion de Proyectos/` | `raw/Gestion de Proyectos/` |
| `inteligencia-de-negocio` | Inteligencia de Negocio | `wiki/Inteligencia de Negocio/` | `raw/Inteligencia de Negocio/` |
| `redes-de-computadores` | Redes de Computadores | `wiki/Redes de Computadores/` | `raw/Redes de Computadores/` |
| `responsabilidad-social` | Responsabilidad Social y Ética | `wiki/Responsabilidad Social y Etica/` | — |
| `taller-admin-sistemas` | Taller de Admin. de Sistemas | `wiki/Taller de Administracion de Sistemas/` | — |
| `visualizacion` | Visualización | `wiki/Visualizacion/` | `raw/Visualizacion/` |

---

## 8. Herramientas y Plugins Recomendados

- **Obsidian Graph View**: Visualizar la red de conexiones entre notas.
- **Dataview**: Consultas dinámicas sobre el frontmatter YAML.
- **Obsidian Web Clipper**: Capturar artículos web como fuentes raw.
- **Wikilinks**: Activado en Obsidian para máxima interconexión.

---

> [!NOTE]
> Este schema co-evoluciona con el uso del wiki. Si un flujo de trabajo no funciona, se debe actualizar este documento para reflejar la nueva convención.
