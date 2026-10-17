---
tags:
  - gestion-de-proyectos
  - teoria
  - pmbok
  - finanzas
  - presupuesto
  - calidad
aliases:
  - "Clase 14 Gestión de Proyectos"
  - "Gestión Financiera y Calidad PMBOK 8"
  - "Costos, Presupuesto y Calidad"
asignatura: "Gestión de Proyectos"
tipo: teoria
created: 2026-10-13
---

# Clase 14 — PMBOK® 8: Gestión Financiera, Desarrollo del Presupuesto y Planificación de la Calidad

> Planificación financiera integral en proyectos según el PMBOK 8. Clasificación de costos (fijos, variables, directos, indirectos, hundidos), técnicas de estimación (análoga, paramétrica, ascendente), construcción jerárquica del presupuesto y planificación de la calidad con criterios de aceptación verificables. Clase dictada por la Dra. Gerlys Villalobos Fontalvo (USM).

---

## 1. La Dimensión Financiera en PMBOK® 8

El área clave de **Finanzas** comprende los procesos orientados a estimar, estructurar, presupuestar y controlar los fondos económicos para asegurar que el proyecto se complete dentro de los límites aprobados.

Se articula a través de tres procesos secuenciales en la planificación:
1. **4.1 Planificar la gestión financiera:** Establece políticas, métricas de control y formatos de reporte.
2. **4.2 Estimar los costos:** Cuantifica los recursos monetarios necesarios para ejecutar cada actividad.
3. **4.3 Desarrollar el presupuesto:** Consolida las estimaciones y añade las reservas para establecer la línea base de costo autorizada.

---

## 2. Clasificación de los Costos en Proyectos de Software

| Tipo de Costo | Definición | Comportamiento | Ejemplo en Proyecto TI |
|---|---|---|---|
| **Costo Fijo** | No varía en función del volumen de trabajo o usuarios. | Constante | Cuota mensual fija de servidor cloud, licencia anual de base de datos. |
| **Costo Variable** | Varía en forma proporcional al volumen de producción o uso. | Dinámico | Costo por horas extras de desarrollo, consumo por gigabyte transferido en la nube. |
| **Costo Directo** | Se puede atribuir e imputar de forma exclusiva al proyecto. | Específico | Salarios de los programadores, diseño UI del sistema, pruebas funcionales. |
| **Costo Indirecto** | Compartido entre varios proyectos o la operación general. | Prorrateado | Electricidad de la oficina, conectividad a Internet, sueldo del área administrativa. |
| **Costo Hundido (*Sunk Cost*)** | Gasto ya incurrido en el pasado que no se puede recuperar. | Irreversible | Costos de un estudio preliminar descartado; **no debe sesgar** decisiones presentes. |

---

## 3. Proceso 4.2: Estimar los Costos del Proyecto

La estimación de costos parte de la EDT, el cronograma y la asignación de recursos:

```text
  [Alcance / EDT]       [Cronograma]        [Recursos]         [Riesgos]
   ¿Qué se hace?      ¿Cuándo se hace?   ¿Quién lo hace?   ¿Posibles sobrecostos?
         │                   │                  │                  │
         └───────────────────┼──────────────────┴──────────────────┘
                             ▼
                 [Estimación de Costos]
           Costo unitario × Cantidad requerida
```

### 3.1 Técnicas de Estimación de Costos
1. **Estimación Análoga:** Basada en el costo histórico real de proyectos anteriores similares.
   - *Ejemplo:* Si un módulo de reservas costó anteriormente \$1.500.000 CLP y el actual tiene mayor complejidad, se estima un 20% adicional: $\$1.500.000 \times 1.20 = \$1.800.000\text{ CLP}$.
2. **Estimación Paramétrica:** Aplica un ratio cuantitativo o estadístico por unidad de trabajo.
   - *Ejemplo:* Si desarrollar una pantalla cuesta \$200.000 CLP, 8 pantallas costarán: $8 \times \$200.000 = \$1.600.000\text{ CLP}$.
3. **Estimación Ascendente (*Bottom-Up*):** Estima el costo de cada tarea individual en el nivel más bajo y suma sucesivamente hacia los paquetes de trabajo y cuentas de control. Es la más precisa y confiable.

---

## 4. Proceso 4.3: Desarrollar el Presupuesto del Proyecto

El presupuesto se construye mediante una estructura jerárquica piramidal ascendente que culmina con la incorporación de las reservas:

```text
┌────────────────────────────────────────────────────────────────────────┐
│             PRESUPUESTO TOTAL DEL PROYECTO ($10.000.000 CLP)           │
├───────────────────────────────────┬────────────────────────────────────┤
│     Línea Base de Costos          │        Reserva de Gerencia         │
│       ($8.700.000 CLP)            │          ($1.300.000 CLP)          │
├─────────────────┬─────────────────┴────────────────────────────────────┤
│  Estimación del │   Reserva de Contingencia (Known-Unknowns)           │
│    Proyecto     │               ($1.000.000 CLP)                       │
│($7.700.000 CLP) │                                                      │
├─────────────────┴──────────────────────────────────────────────────────┤
│  Cuentas de Control (Diseño, Programación, Infraestructura, Pruebas)   │
├────────────────────────────────────────────────────────────────────────┤
│  Paquetes de Trabajo de la EDT                                         │
├────────────────────────────────────────────────────────────────────────┤
│  Estimación de Costos por Actividad individual                         │
└────────────────────────────────────────────────────────────────────────┘
```

- **Estimación de Costos del Proyecto:** Suma de todas las actividades y paquetes de trabajo (\$7.700.000 CLP en el ejemplo docente).
- **Línea Base de Costos (*Cost Baseline*):** Estimación base + Reserva de Contingencia (\$7.700.000 + \$1.000.000 = \$8.700.000 CLP). Es la curva $S$ aprobada contra la cual se mide el desempeño financiero.
- **Presupuesto Total:** Línea Base + Reserva de Gerencia (\$8.700.000 + \$1.300.000 = \$10.000.000 CLP).

---

## 5. Gobernanza: Planificar la Calidad del Proyecto (Proceso 1.3)

La calidad no se inspecciona al final; se planifica e incorpora desde el inicio (*Embed Quality*):

> *Define los criterios, estándares y métodos de verificación para asegurar que los entregables satisfagan los requisitos del cliente y de la organización.*

### 5.1 Matriz de Planificación de la Calidad

| Entregable / Aspecto | Indicador o Criterio de Aceptación | Método de Verificación | Rol Responsable |
|---|---|---|---|
| **Disponibilidad del Sistema** | $\ge 99\%$ tiempo de disponibilidad operativa | Prueba de carga, monitoreo de uptime continuo | Equipo de Infraestructura / DevOps |
| **Integridad Transaccional** | 0 reservas duplicadas o solapadas | Pruebas funcionales de concurrencia | Desarrollador Backend |
| **Seguridad de Acceso** | Solo usuarios autenticados con roles válidos | Pruebas de penetración y control de tokens JWT | Desarrollador Backend |
| **Tiempo de Respuesta (Usabilidad)** | Finalizar una reserva en $\le 3\text{ minutos}$ | Pruebas de usabilidad con usuarios representativos | Diseñador UI/UX y QA |
| **Satisfacción del Usuario** | $\ge 80\%$ de evaluaciones positivas en encuesta | Encuesta estandarizada post-uso | Product Owner / Líder de Proyecto |

---

## 6. Aplicación Práctica y Fechas Clave

Esta clase articula dos entregables decisivos del taller:
- **Plantilla de Presupuesto (Excel):** Costos unitarios por actividad, cálculo de línea base y reservas.
- **Plantilla de Planificación de la Calidad (Word):** Matriz de aseguramiento de calidad con responsables y frecuencias.

Véase la Sección 1.1 y 1.8 del proyecto [[LiciFlow_Documentacion|LiciFlow]], donde se analizan las restricciones y coherencias presupuestarias del proyecto semestral.

---

## Véase también
- [[_MOC|MOC Gestión de Proyectos]]
- [[Clase_12_PMBOK_Respuesta_a_Riesgos_y_Reservas|Clase 12 — Respuesta a Riesgos y Reservas de Contingencia]]
- [[Clase_13_PMBOK_Gestion_del_Cronograma|Clase 13 — Cronograma y Diagrama de Gantt]]
- [[LiciFlow_Documentacion|Proyecto Semestral LiciFlow]]
