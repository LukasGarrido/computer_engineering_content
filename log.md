---
tags:
  - meta
  - log
tipo: log
---

# 📝 Log del Wiki

> Registro cronológico de todas las acciones realizadas sobre el wiki. Formato: `## [YYYY-MM-DD] <acción> | <detalle>`

---

## [2026-10-03] create | Reestructuración inicial del repositorio

**Acción:** Migración completa del repositorio al patrón LLM-Wiki.

**Cambios realizados:**
- Creada la estructura de 3 capas: `wiki/`, `raw/`, schema (`AGENTS.md`).
- Movidas todas las notas `.md` de teoría, laboratorios y certámenes a `wiki/<Asignatura>/`.
- Movidos todos los archivos inmutables (PDFs, notebooks, CSV, SQL, imágenes) a `raw/`.
- Eliminadas las subcarpetas numéricas (`01_Teoria/`, `02_Laboratorios/`, etc.).
- Creados 7 MOCs (Map of Content), uno por asignatura.
- Creadas 19 páginas de conceptos transversales en `wiki/_conceptos/`.
- Creados `index.md` (índice global) y `log.md` (este archivo).
- Creado `AGENTS.md` (schema del wiki).
- Añadido frontmatter YAML a las notas existentes.
- Actualizado `.obsidian/app.json` para attachments en `raw/assets/`.

**Archivos creados:** ~30 nuevos archivos (MOCs, conceptos, meta).
**Archivos movidos:** ~60 archivos redistribuidos.
**Archivos eliminados:** 7 READMEs de asignatura (reemplazados por MOCs).

---
