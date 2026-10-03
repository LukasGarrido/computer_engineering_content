---
tags:
  - concepto
aliases:
  - "OLTP"
  - "OLAP"
  - "Online Transaction Processing"
  - "Online Analytical Processing"
tipo: concepto
created: 2026-10-03
---

# OLTP vs OLAP

> Dos paradigmas de procesamiento de datos: OLTP (transaccional, normalizado, operaciones CRUD rápidas) vs OLAP (analítico, desnormalizado, consultas complejas sobre grandes volúmenes históricos).

## Aparece en

### Inteligencia de Negocio
- [[03_Explicacion_OLTP_a_OLAP|De OLTP a OLAP]] — transición completa con metodología Kimball
- [[01_Explicacion_Business_Intelligence|Fundamentos de BI]] — contexto de OLTP/OLAP en la arquitectura de BI

## Notas
- La transición de OLTP a OLAP implica crear un [[Data Warehouse]] con procesos [[ETL]].
- OLTP usa modelo relacional normalizado; OLAP usa modelo dimensional (estrella/copo de nieve).
