---
tags:
  - gestion-de-proyectos
  - teoria
  - pmbok
  - riesgos
  - dafo
  - ram-riesgos
aliases:
  - "Clase 11 Gestión de Proyectos"
  - "Gestión de Riesgos: Identificación y Análisis"
  - "Matriz de Riesgos y DAFO"
asignatura: "Gestión de Proyectos"
tipo: teoria
created: 2026-09-29
---

# Clase 11 — PMBOK® 8: Gestión de Riesgos — Planificación, Identificación y Análisis Cualitativo

> Fundamentos de la gestión de la incertidumbre en proyectos según el PMBOK 8. Definición de riesgos y oportunidades, Estructura de Desglose de Riesgos (RBS), técnicas de identificación (Brainstorming, Delphi, Causa Raíz, DAFO) y matriz cualitativa de probabilidad e impacto (RAM). Clase dictada por la Dra. Gerlys Villalobos Fontalvo (USM).

---

## 1. Concepto y Dimensiones del Riesgo

En la dirección de proyectos, el **riesgo** se define formalmente como:

> *Un evento o condición incierta que, si ocurre, tiene un efecto positivo o negativo en uno o más objetivos del proyecto (alcance, tiempo, costo o calidad).*

- **Amenazas:** Eventos con impacto negativo que se deben mitigar o evitar.
- **Oportunidades:** Eventos con impacto positivo que se deben explotar o potenciar.

### 1.1 Las Dos Dimensiones Clave
1. **Probabilidad ($P$):** La frecuencia o certeza con que un evento podría manifestarse.
2. **Impacto o Criticidad ($I$):** La severidad del efecto que causaría sobre los objetivos si llegara a materializarse, medido preferentemente en unidades monetarias o días de atraso.

### 1.2 Valor Monetario Esperado (VME)
El VME cuantifica el valor promedio ponderado del riesgo:

$$\text{VME} = \text{Probabilidad} \times \text{Impacto monetario}$$

*Ejemplo:* Si existe un 20% de probabilidad ($P=0.20$) de que un proveedor externo se atrase 2 días con un sobrecosto diario de \$1.000.000 CLP (Impacto = \$2.000.000 CLP), el $\text{VME} = 0.20 \times \$2.000.000 = \$400.000\text{ CLP}$.

---

## 2. Tipos y Categorías de Riesgos (RBS)

La **Estructura de Desglose de Riesgos** (*Risk Breakdown Structure - RBS*) organiza jerárquicamente las posibles fuentes de riesgo del proyecto:

```text
                                  Riesgos del Proyecto
                                           │
         ┌──────────────────┬──────────────┴───────────────┬──────────────────┐
         ▼                  ▼                             ▼                  ▼
  Riesgos Técnicos   Riesgos de Gestión           Riesgos Externos    Riesgos Organizacionales
  - Arquitectura     - Estimaciones irreales       - Proveedores API  - Conflictos de prioridad
  - Nuevas libs      - Comunicación deficiente     - Cambios legales  - Pérdida de personal
  - Rendimiento/BD   - Control de cambios tardío   - Competencia      - Falta de financiamiento
```

---

## 3. Proceso 7.1: Planificar la Gestión de Riesgos

Define cómo se realizarán las actividades de identificación, análisis y respuesta en el **Plan de Gestión de Riesgos (PGR)**:
- **Metodología y herramientas:** Escalas de medición, matrices y software a emplear.
- **Roles y responsabilidades:** Quién lidera y quién actúa ante cada categoría de evento.
- **Presupuesto y calendario:** Asignación de recursos y revisiones periódicas del registro.
- **Tolerancia y actitud frente al riesgo:** Sensibilidad del cliente o sponsor (adverso, neutral o tolerante al riesgo).

---

## 4. Proceso 7.2: Identificar los Riesgos

Proceso continuo y sistemático para determinar qué eventos inciertos pueden afectar al proyecto:

### 4.1 Técnicas de Identificación
1. **Tormenta de Ideas (*Brainstorming*):** Sesión grupal con el equipo y especialistas para generar un inventario exhaustivo guiado por la RBS.
2. **Técnica Delphi:** Consulta a paneles de expertos mediante cuestionarios anónimos en sucesivas rondas para alcanzar consenso sin sesgos ni presiones jerárquicas.
3. **Entrevistas Estructuradas:** Diálogo con clientes, usuarios clave y desarrolladores experimentados.
4. **Análisis de Causa Raíz:** Descompone el evento en la cadena lógica fundamental:

$$\text{Causa (Origen técnico o humano)} \longrightarrow \text{Riesgo (Evento incierto)} \longrightarrow \text{Consecuencia (Efecto en el proyecto)}$$

5. **Análisis DAFO / FODA Estratégico:**
   - **Factores Internos:** Fortalezas (F) y Debilidades (D) del equipo.
   - **Factores Externos:** Oportunidades (O) y Amenazas (A) del mercado o la tecnología.
   - Cruces estratégicos ($F+O$ ofensiva, $F+A$ defensiva, $D+O$ mejora, $D+A$ supervivencia).

### 4.2 Registro Inicial de Riesgos
Contiene como mínimo: identificador único (ID), descripción del riesgo, causa identificada, consecuencia estimada y categoría de la RBS.

---

## 5. Proceso 7.3: Realizar el Análisis Cualitativo de Riesgos (RAM)

Prioriza los riesgos del registro evaluando su probabilidad y su criticidad sobre una escala uniforme del 1 al 5:

### 5.1 Escalas de Medición

| Nivel | Probabilidad ($P$) | Criterio de Frecuencia | Impacto / Criticidad ($I$) | Criterio de Daño |
|:---:|---|---|---|---|
| **1** | **Improbable** | Muy raro; solo circunstancias excepcionales. | **Insignificante** | Efecto mínimo; no altera alcance ni plazo. |
| **2** | **Posible** | Podría ocurrir en algún momento puntual. | **Leve** | Efecto menor; requiere pequeños ajustes. |
| **3** | **Ocasional** | Probabilidad moderada durante el proyecto. | **Moderado** | Efecto significativo; consume contingencias. |
| **4** | **Frecuente** | Se espera que ocurra varias veces. | **Crítico** | Pone en riesgo el cumplimiento del hito. |
| **5** | **Muy frecuente** | Alta certeza de ocurrencia durante la ejecución. | **Catastrófico** | Provoca el fracaso o cancelación del proyecto. |

### 5.2 Matriz de Evaluación de Riesgos (RAM de Riesgos)

El **Nivel de Riesgo** numérico se obtiene multiplicando $\text{Nivel} = P \times I$ (rango de 1 a 25):

```text
Impacto (I)
  5 (Catastrófico) │  5 (Bajo)   10 (Medio)   15 (Alto)    20 (Extremo)  25 (Extremo)
  4 (Crítico)      │  4 (Bajo)    8 (Medio)   12 (Alto)    16 (Alto)     20 (Extremo)
  3 (Moderado)     │  3 (Bajo)    6 (Medio)    9 (Medio)   12 (Alto)     15 (Alto)
  2 (Leve)         │  2 (Bajo)    4 (Bajo)     6 (Medio)    8 (Medio)    10 (Medio)
  1 (Insignificante)│ 1 (Bajo)    2 (Bajo)     3 (Bajo)     4 (Bajo)      5 (Bajo)
                   └──────────────────────────────────────────────────────────────
                        1            2            3            4            5
                    Improbable    Posible     Ocasional    Frecuente   Muy frecuente
                                         Probabilidad (P)
```

### 5.3 Clasificación por Severidad y Prioridad

| Rango ($P \times I$) | Nivel de Riesgo | Color | Acción Requerida |
|:---:|:---:|:---:|---|
| **1 – 5** | **Bajo** | Verde | Monitoreo pasivo / Lista de observación. |
| **6 – 10** | **Medio** | Amarillo | Atención y seguimiento en revisiones periódicas. |
| **11 – 16** | **Alto** | Naranja | Plan de respuesta activo mandatorio. |
| **17 – 25** | **Extremo / Muy alto** | Rojo | Acción inmediata y escalamiento a la alta dirección. |

---

## 6. Aplicación Práctica: Entregable 6

El resultado práctico de esta clase es la **Matriz de Riesgos Priorizada** del proyecto semestral. Véase la Sección 7 (*Gestión de Riesgos*) en la documentación consolidada de [[LiciFlow_Documentacion]], donde se aplica esta metodología paso a paso sobre la integración con Mercado Público.

---

## Véase también
- [[_MOC|MOC Gestión de Proyectos]]
- [[Clase_10_PMBOK_Interesados_Comunicaciones_Recursos|Clase 10 — Interesados, Comunicaciones y Recursos]]
- [[Clase_12_PMBOK_Respuesta_a_Riesgos_y_Reservas|Clase 12 — Planificación de Respuestas a Riesgos y Reservas]]
- [[LiciFlow_Documentacion|Proyecto Semestral LiciFlow]]
