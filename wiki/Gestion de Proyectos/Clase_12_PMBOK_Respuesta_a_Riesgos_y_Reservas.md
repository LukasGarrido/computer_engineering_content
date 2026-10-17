---
tags:
  - gestion-de-proyectos
  - teoria
  - pmbok
  - riesgos
  - reservas-contingencia
aliases:
  - "Clase 12 Gestión de Proyectos"
  - "Respuesta a Riesgos y Reservas"
  - "Estrategias ante Amenazas y Oportunidades"
asignatura: "Gestión de Proyectos"
tipo: teoria
created: 2026-10-01
---

# Clase 12 — PMBOK® 8: Planificación de Respuestas a Riesgos y Reservas de Contingencia

> Estrategias formales de tratamiento ante amenazas y oportunidades en proyectos según el PMBOK 8. Riesgos secundarios y residuales, cálculo del Valor Monetario Esperado (VME) y diferenciación clave entre Reservas de Contingencia y Reservas de Gerencia. Clase dictada por la Dra. Gerlys Villalobos Fontalvo (USM).

---

## 1. El Proceso 7.4: Planificar la Respuesta a los Riesgos

Una vez priorizados los eventos en la Matriz de Evaluación (RAM), el proceso **7.4 Planificar las Respuestas a los Riesgos** define las acciones concretas para abordar los riesgos críticos:

> *Consiste en desarrollar opciones y acciones para mejorar las oportunidades y reducir las amenazas sobre los objetivos del proyecto.*

### Componentes de una Respuesta Efectiva:
1. **Estrategia seleccionada:** Acorde a la severidad y costo-efectividad.
2. **Acciones específicas:** Tareas técnicas o administrativas concretas.
3. **Responsable de la respuesta (*Risk Owner*):** Persona designada para monitorear y ejecutar la acción.
4. **Recursos necesarios:** Horas-hombre, presupuesto o software de apoyo.
5. **Plan de contingencia:** Procedimiento a ejecutar si el riesgo finalmente se materializa.
6. **Reserva asignada:** Tiempo o dinero reservado específicamente.

---

## 2. Estrategias de Respuesta ante Amenazas (Riesgos Negativos)

```text
                               ESTRATEGIAS ANTE AMENAZAS
                                           │
         ┌──────────────────┬──────────────┴──────────────┬──────────────────┐
         ▼                  ▼                             ▼                  ▼
      EVITAR            TRANSFERIR                     MITIGAR            ACEPTAR
(Elimina la causa) (Traslada a un 3ro)       (Reduce Prob o Imp)   (Activa o Pasiva)
```

| Estrategia | ¿En qué consiste? | Acciones y Ejemplos | Cuándo aplicarla |
|---|---|---|---|
| **Evitar (*Avoid*)** | El equipo actúa para **eliminar por completo la amenaza** o proteger al proyecto de su impacto. | Cambiar la arquitectura técnica, prescindir de una librería inestable, extender el cronograma oficial o reducir el alcance conflictivo. | Riesgos críticos o catastróficos que amenazan la viabilidad del proyecto. |
| **Transferir (*Transfer*)** | Implica trasladar la titularidad, responsabilidad e impacto de la amenaza a un **tercero**. | Contratación de pólizas de seguro, garantías bancarias, subcontratación de módulos a precio fijo, acuerdos de nivel de servicio (SLA). *(Suele requerir el pago de una prima).* | Riesgos financieros o de infraestructura fuera del control directo del equipo. |
| **Mitigar (*Mitigate*)** | Se toman medidas preventivas para **reducir la probabilidad de ocurrencia y/o la gravedad del impacto**. | Implementar pruebas unitarias y de estrés automatizadas, adoptar arquitecturas modulares desacopladas, redundancia de servidores, capacitación previa. | Amenazas de alta probabilidad o severidad media-alta donde no es posible evitar el riesgo. |
| **Aceptar (*Accept*)** | Se reconoce formalmente la existencia de la amenaza pero **no se toman medidas preventivas proactivas**. | - **Aceptación activa:** Establecer una **reserva para contingencias** (tiempo o presupuesto) para reaccionar si ocurre.<br>- **Aceptación pasiva:** Monitoreo periódico sin asignar fondos específicos. | Amenazas de baja prioridad o cuando el costo de mitigar supera el impacto del riesgo. |

---

## 3. Estrategias de Respuesta ante Oportunidades (Riesgos Positivos)

| Estrategia | Propósito | Acciones y Ejemplos |
|---|---|---|
| **Explotar (*Exploit*)** | Eliminar la incertidumbre para **asegurar al 100% que la oportunidad se haga realidad**. | Asignar al proyecto a los desarrolladores más experimentados de la empresa; adoptar de inmediato una nueva API más económica y eficiente. |
| **Mejorar (*Enhance*)** | **Aumentar la probabilidad y/o el impacto positivo** de la oportunidad. | Añadir recursos tempranamente a una tarea para liberar antes una funcionalidad comercializable; optimizar código para exceder los requerimientos. |
| **Compartir (*Share*)** | Asignar parte o la totalidad de la oportunidad a un **tercero mejor capacitado** para capturar el valor. | Formación de consorcios, asociaciones estratégicas (*joint ventures*) o convenios con centros de I+D. |
| **Aceptar (*Accept*)** | Disposición a aprovechar la oportunidad si se presenta, pero **sin destinar recursos proactivos** a buscarla. | Utilizar una rebaja arancelaria o descuento de proveedor si llega a estar disponible. |

---

## 4. Riesgos Residuales y Riesgos Secundarios

- **Riesgo Residual:** Aquel nivel de riesgo que permanece tras haber implementado con éxito la estrategia de respuesta planificada.
- **Riesgo Secundario:** Un nuevo riesgo que **surge como consecuencia directa** de haber implementado una respuesta a un riesgo previo.
  - *Ejemplo:* Para mitigar el retraso en el backend, se subcontrata a un equipo externo (respuesta). Esto genera el riesgo secundario de filtración de código fuente o incompatibilidad en la integración.

---

## 5. Reservas de Contingencia vs. Reservas de Gerencia

La adecuada gestión financiera de los riesgos exige diferenciar con claridad los fondos asignados:

```text
Presupuesto Total del Proyecto
  ├── Reserva de Gerencia (Unknown-Unknowns) [No forma parte de la Línea Base]
  └── Línea Base de Costos (Cost Baseline)
        ├── Estimación de Costos del Proyecto (Suma de paquetes de trabajo)
        └── Reserva de Contingencia (Known-Unknowns) [Calculada vía VME]
```

### 5.1 Reserva de Contingencia
- **Propósito:** Destinada a cubrir los riesgos identificados en el PGR (*known-unknowns* o incertidumbres conocidas).
- **Cálculo:** Se calcula mediante la suma del Valor Monetario Esperado ($\text{VME} = P \times I$) de los riesgos conocidos o como un porcentaje técnico sobre el costo base.
- **Gobernanza:** **Forma parte de la Línea Base de Costos**. Su utilización es potestad directa del Director del Proyecto.

### 5.2 Reserva de Gerencia
- **Propósito:** Destinada a cubrir imprevistos no planificables (*unknown-unknowns* o riesgos no identificados).
- **Cálculo:** Fijada a nivel corporativo por políticas organizacionales (ej. 5% a 10% del total).
- **Gobernanza:** **No forma parte de la Línea Base de Costos**. Para utilizarla se requiere una solicitud formal de control de cambios aprobada por la alta gerencia o el patrocinador.

---

## Véase también
- [[_MOC|MOC Gestión de Proyectos]]
- [[Clase_11_PMBOK_Gestion_de_Riesgos_Identificacion_y_Analisis|Clase 11 — Identificación y Análisis de Riesgos]]
- [[Clase_14_PMBOK_Gestion_Financiera_y_Calidad|Clase 14 — Gestión Financiera, Costos y Calidad]]
- [[LiciFlow_Documentacion|Proyecto Semestral LiciFlow]]
