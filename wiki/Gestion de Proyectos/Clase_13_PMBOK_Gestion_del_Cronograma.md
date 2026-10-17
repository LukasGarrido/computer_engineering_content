---
tags:
  - gestion-de-proyectos
  - teoria
  - pmbok
  - cronograma
  - pert
  - gantt
aliases:
  - "Clase 13 Gestión de Proyectos"
  - "Gestión del Cronograma PMBOK 8"
  - "Estimación PERT y Diagrama de Gantt"
asignatura: "Gestión de Proyectos"
tipo: teoria
created: 2026-10-06
---

# Clase 13 — PMBOK® 8: Gestión del Cronograma, Estimación PERT y Diagrama de Gantt

> Planificación temporal del proyecto según el PMBOK 8. Los 6 pasos para construir el cronograma: descomposición de actividades, tipos de precedencias (FS, SS, FF, SF), técnicas de estimación (análoga, paramétrica, PERT triangular y beta) y construcción del Diagrama de Gantt. Clase dictada por la Dra. Gerlys Villalobos Fontalvo (USM).

---

## 1. El Área Clave de Cronograma en PMBOK® 8

El cronograma organiza y gestiona **cuándo y en qué orden** se ejecutará el trabajo del proyecto para cumplir con los plazos comprometidos.

Comprende dos procesos fundamentales en la fase de planificación:
- **3.1 Planificar la gestión del cronograma:** Establece las políticas, herramientas (GanttProject, Project), unidades de tiempo y reglas para modelar el cronograma.
- **3.2 Desarrollar el cronograma:** Construye formalmente el modelo temporal integrando actividades, dependencias, duraciones, recursos y fechas límite.

---

## 2. Los 6 Pasos para Construir el Cronograma

```text
 ┌────────────────┐     ┌──────────────────┐     ┌────────────────┐
 │ Paso 1:        │     │ Paso 2:          │     │ Paso 3:        │
 │ Definir        ├────►│ Secuenciar       ├────►│ Estimar        │
 │ Actividades    │     │ Actividades      │     │ Duración (PERT)│
 └────────────────┘     └──────────────────┘     └───────┬────────┘
                                                         │
 ┌────────────────┐     ┌──────────────────┐             │
 │ Paso 6:        │     │ Paso 5:          │     ┌───────▼────────┐
 │ Construir el   │◄────┤ Establecer       │◄────┤ Paso 4:        │
 │ Cronograma     │     │ Fechas e Hitos   │     │ Asignar        │
 │ (Gantt)        │     │                  │     │ Recursos       │
 └────────────────┘     └──────────────────┘     └────────────────┘
```

---

## 3. Paso 1 y Paso 2: Actividades y Tipos de Dependencias

### 3.1 Descomposición en Actividades
A partir de los paquetes de trabajo de nivel más bajo de la EDT, se identifican las tareas concretas requeridas. Cada actividad debe:
- Ser medible y tener un resultado verificable.
- Tener un responsable claramente asignado.
- Estar redactada preferentemente con verbos en infinitivo (*"Diseñar base de datos"*, *"Desarrollar endpoint API"*).

### 3.2 Tipos de Dependencias Lógicas (Precedencias)

Las relaciones de precedencia determinan el orden de ejecución:

| Tipo | Sigla | Nombre | Relación y Comportamiento | Frecuencia de uso |
|:---:|:---:|---|---|:---:|
| **Fin a Inicio** | **FS** | *Finish to Start* | La actividad sucesora B solo puede comenzar cuando la predecesora A haya finalizado por completo. | **La más común (~95%)** |
| **Inicio a Inicio** | **SS** | *Start to Start* | La actividad B puede comenzar tan pronto comience la actividad A (trabajo paralelo o en solapamiento). | Habitual |
| **Fin a Fin** | **FF** | *Finish to Finish* | La actividad B no puede finalizar hasta que la actividad A haya terminado. | Moderada (pruebas vs documentación) |
| **Inicio a Fin** | **SF** | *Start to Finish* | La actividad B no puede finalizar hasta que la actividad A inicie. | Muy inusual / Excepcional |

- **Adelanto (*Lead*):** Tiempo en que una sucesora se adelanta respecto a la finalización de la predecesora ($FS - 2\text{ días}$).
- **Retraso (*Lag*):** Tiempo de espera obligado antes de que la sucesora pueda comenzar ($FS + 3\text{ días}$ por ejemplo para secado, compilación o validación externa).

---

## 4. Paso 3: Técnicas de Estimación de Duración

### 4.1 Estimación Análoga y Paramétrica
- **Análoga:** Utiliza la duración real de actividades similares ejecutadas en proyectos pasados como referencia. Es rápida y económica, pero de baja precisión.
- **Paramétrica:** Aplica algoritmos y relaciones estadísticas entre variables históricas (ej. tiempo unitario por elemento $\times$ cantidad: $0.5\text{ días/pantalla} \times 8\text{ pantallas} = 4\text{ días}$).

### 4.2 Estimación de Tres Puntos (PERT)

Considera la incertidumbre asignando tres estimaciones de duración a cada actividad:
- **$O$ (Optimista):** Duración mínima en el mejor de los escenarios posibles.
- **$M$ (Más probable):** Duración realista en condiciones habituales de trabajo.
- **$P$ (Pesimista):** Duración máxima asumiendo contratiempos significativos.

#### Distribución Triangular (Promedio Simple):
$$E_{\text{triangular}} = \frac{O + M + P}{3}$$

#### Distribución Beta (Fórmula PERT Tradicional):
Pondera con mayor fuerza el valor más probable:

$$E_{\text{PERT}} = \frac{O + 4M + P}{6}$$

#### Cálculo de la Incertidumbre (Desviación Estándar PERT):
$$\sigma = \frac{P - O}{6}$$

El rango esperado de duración con un 68.3% de probabilidad estadística es $[E - \sigma, E + \sigma]$.

*Ejemplo Docente:* Para una tarea con $O = 30\text{ min}$, $M = 35\text{ min}$, $P = 45\text{ min}$:
- $E_{\text{triangular}} = (30 + 35 + 45)/3 = 36.6\text{ min}$
- $E_{\text{PERT}} = (30 + 4(35) + 45)/6 = \frac{215}{6} = 35.8\text{ min}$
- $\sigma = (45 - 30)/6 = 2.5\text{ min}$
- Rango de confianza: $35.8 \pm 2.5\text{ min} \implies [33.3, 38.3]\text{ min}$.

---

## 5. Pasos 4, 5 y 6: Recursos, Hitos y Diagrama de Gantt

### 5.1 Asignación de Recursos y Nivelación
Se vinculan los perfiles de la matriz RAM a cada tarea asegurando que ningún desarrollador quede sobreasignado en los mismos días.

### 5.2 Hitos del Proyecto (*Milestones*)
Puntos de control clave o eventos relevantes que marcan la finalización de una fase o entrega crítica:
- Tienen **duración cero** ($\text{Duración} = 0$).
- Ejemplos: *Acta de Inicio firmada*, *Arquitectura y BD aprobadas*, *Prototipo funcional validado*, *Paso a producción*.

### 5.3 El Diagrama de Gantt
Representación gráfica en barras horizontales donde el eje horizontal es la línea de tiempo (días/semanas) y el vertical lista las actividades con sus dependencias e hitos:
- Identifica la **Ruta Crítica** (la secuencia de actividades sin holgura que determina la duración total mínima del proyecto).
- Permite detectar cuellos de botella y desvíos tempranos durante la ejecución.

---

## 6. Aplicación Práctica del Cronograma

En la asignatura, el cronograma se modela utilizando **GanttProject** (archivos `.gan`) exportados a plantillas de seguimiento. Conecta directamente con la estimación de plazos y sprints del proyecto [[LiciFlow_Documentacion]].

---

## Véase también
- [[_MOC|MOC Gestión de Proyectos]]
- [[Clase_09_PMBOK_Planificacion_Alcance_EDT|Clase 09 — Alcance y EDT]]
- [[Clase_10_PMBOK_Interesados_Comunicaciones_Recursos|Clase 10 — Interesados y Recursos (RAM)]]
- [[Clase_14_PMBOK_Gestion_Financiera_y_Calidad|Clase 14 — Gestión Financiera y Calidad]]
- [[LiciFlow_Documentacion|Proyecto Semestral LiciFlow]]
