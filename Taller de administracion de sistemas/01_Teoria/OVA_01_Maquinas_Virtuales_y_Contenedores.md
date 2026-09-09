
---
# Misión - Estación 1

Una empresa necesita un CMS, servicios de red, automatización y entornos reproducibles. ¿Conviene usar máquinas virtuales, contenedores o una combinación?
## 1. El Error Conceptual: El contenedor NO es una "VM pequeña"

Tratar un contenedor como una VM ligera es el origen de fallas graves en seguridad y operaciones.

- **Virtualización por VM (Aislamiento de Hardware):** Un hipervisor (como KVM, ESXi o Hyper-V) virtualiza hardware. Cada VM corre su propio Kernel de Sistema Operativo independiente. Si una VM cae o es vulnerada, el límite de aislamiento está en el hardware virtualizado.
    
- **Contenedorización (Aislamiento de Procesos):** Un contenedor es simplemente un proceso en el espacio de usuario restringido por funcionalidades del kernel del host (como _namespaces_ y _cgroups_ en Linux).

### La Cadena del Contenedor: Imagen $\rightarrow$ Runtime $\rightarrow$ Kernel

1. **Imagen:** Es una plantilla de solo lectura que contiene las dependencias, bibliotecas y código de la aplicación.
    
2. **Runtime (ej. `containerd`, `CRI-O`):** El motor que toma la imagen, configura el aislamiento y le dice al kernel que ejecute el proceso.
    
3. **Kernel Compartido:** Todos los contenedores en un mismo host **comparten el mismo kernel del sistema operativo base**. Si un contenedor explota una vulnerabilidad a nivel de kernel, puede comprometer a todos los demás contenedores del mismo host.

## 2. Comparativa de Límites de Aislamiento

|**Criterio**|**Máquina Virtual (VM)**|**Contenedor**|
|---|---|---|
|**Límite de aislamiento**|Hardware / Kernel propio|Namespaces y cgroups / Kernel compartido|
|**Punto de falla de seguridad**|Hipervisor|Kernel del Host|
|**Tiempo de arranque**|Minutos / Segundos|Milisegundos|
|**Entornos reproducibles**|Difícil (alto peso, acoplado a la VM)|Ideal (imágenes inmutables e idénticas)|
|**Sobrecarga de recursos**|Alta (memoria/CPU reservada para cada SO)|Mínima (solo consume lo que usa el proceso)|

## 3. Asignación de Componentes al Enfoque Híbrido

```
                  ┌──────────────────────────────────────────┐
                  │            MÁQUINA VIRTUAL (VM)          │
                  │   - Kernel propio / Aislamiento total    │
                  │   - Servicios de Red (Firewall, VPN)     │
                  │                                          │
                  │   ┌──────────────────────────────────┐   │
                  │   │        MOTOR DE CONTENEDORES     │   │
                  │   │  ┌──────────────┐ ┌────────────┐ │   │
                  │   │  │ CMS (PHP/Node│ │Automatiz.  │ │   │
                  │   │  │ + Nginx)     │ │(CI/CD Runner│   │
                  │   │  └──────────────┘ └────────────┘ │   │
                  │   └──────────────────────────────────┘   │
                  └──────────────────────────────────────────┘
```

- **Contenedores (Para CMS, Entornos Reproducibles y Automatización):**
    
    - _Por qué:_ El CMS y los agentes de automatización requieren despliegues rápidos, consistentes entre desarrollo/producción y escalado horizontal. Los contenedores garantizan que "si funciona en mi máquina, funciona en producción".
        
- **Máquina Virtual (Para Hosting del Engine y Servicios de Red Críticos):**
    
    - _Por qué:_ Los servicios de red (como un firewall perimetral, VPN o enrutamiento central) y la base de datos principal (si requiere estado persistente estricto y tuning de I/O de disco) suelen alojarse directamente en VMs o sobre infraestructura donde el límite de kernel esté aislado.
        

## 4. Fundamentación Técnica, Riesgos y Evidencia Faltante

### Fundamentación

La combinación optimiza la densidad de recursos y la reproducibilidad (vía contenedores) sin sacrificar la seguridad perimetral ni la estabilidad del sistema (vía VMs como hipervisores base).

### Riesgo de la decisión

- **Si se usa solo Contenedores:** Colocar servicios de red sensibles y aplicaciones multitenant en el mismo kernel compartido expone la empresa a ataques de _container escape_ (fuga de contenedor al host).
    
- **Si se usa solo VMs:** La automatización y la creación de entornos reproducibles para los desarrolladores del CMS será lenta, pesada en consumo de RAM/Disco y propensa a desviaciones de configuración (_configuration drift_).

### Evidencia Faltante para el Diseño Final

Para cerrar la arquitectura final en las siguientes sesiones, se debe validar:

1. **Modelo de persistencia del CMS:** ¿El contenido/medios requiere almacenamiento compartido distribuido (ej. NFS, S3)?
    
2. **Tráfico estimado y escalabilidad:** ¿El CMS es estático o transaccional de alto tráfico?
    
3. **Cumplimiento y normativas:** ¿Existen requerimientos regulatorios (PCI-DSS, ISO 27001) que exijan aislamiento físico o de kernel para la base de datos o datos sensibles?

---

# Historia - Estación 2

La Contenerizacion integra décadas de aislamiento, control de recursos y estandarización.

**Microtutorial: Del aislamiento local a un artefacto portable**

**Objetivo y Contexto**

- El propósito de este ejercicio es ordenar la evolución del aislamiento según el problema técnico que resolvió cada tecnología.
    
- La contenerización no es una invención única de Docker, sino la acumulación de tres décadas de desarrollo en el kernel y en la estandarización de software.
    
- El error común es asimilar un contenedor a una VM pequeña o atribuir a Docker el invento de los aisladores de procesos.
    

**Orden Cronológico Correcto (1979 a 2015)**

`chroot` (1979) $\rightarrow$ `FreeBSD Jails` (2000) $\rightarrow$ `Linux Namespaces` (2002) $\rightarrow$ `cgroups` (2007) $\rightarrow$ `Docker` (2013) $\rightarrow$ `OCI` (2015)

**Detalle de cada Hito Técnico**

- **`chroot` (1979)**
    
    - **Qué es:** Una llamada al sistema para cambiar el directorio raíz asignado a un proceso y sus hijos.
        
    - **Problema que resolvió:** Creó el aislamiento básico del sistema de archivos (_jaula de directorio_) para evitar que un proceso acceda a rutas superiores.
        
    - **Límite técnico:** No aisla procesos, usuarios ni red. Un usuario con privilegios de administrador puede escapar de la jaula con facilidad.
        
- **`FreeBSD Jails` (2000)**
    
    - **Qué es:** Un mecanismo del kernel de FreeBSD que expandió la idea de `chroot` hacia un aislamiento multidimensional.
        
    - **Problema que resolvió:** Aisló la red (asignando IP propia), el árbol de procesos y la tabla de usuarios dentro del entorno.
        
    - **Límite técnico:** Tecnología ligada únicamente a FreeBSD. No permitía imponer límites estricto de uso de hardware ni empaquetar aplicaciones de forma portable.
        
- **`Linux Namespaces` (2002)**
    
    - **Qué es:** Primitivas del kernel de Linux que dividen los recursos globales del sistema operativo en vistas privadas.
        
    - **Problema que resolvió:** Resolvió el aislamiento de la **visión** del sistema (qué puede ver un proceso: PID, red, puntos de montaje, usuarios).
        
    - **Límite técnico:** Controlan la visibilidad pero **no la cantidad de recursos** que un proceso puede consumir.
        
- **`cgroups` — Control Groups (2007)**
    
    - **Qué es:** Funcionalidad del kernel Linux (creada originalmente por Google) para agrupar procesos y restringir métricas de hardware.
        
    - **Problema que resolvió:** Evitó el problema del _vecino ruidoso_, limitando y midiendo el consumo de CPU, RAM, disco y red.
        
    - **Límite técnico:** No aíslan la visión del sistema ni ocultan procesos; solo controlan cuotas de recursos.
        
- **`Docker` (2013)**
    
    - **Qué es:** Plataforma que combinó `namespaces` + `cgroups` con un sistema de archivos en capas (`OverlayFS`) y una herramienta de línea de comandos.
        
    - **Problema que resolvió:** Solucionó la portabilidad del código y el empaquetado inmutable (_"en mi máquina funciona"_), introduciendo la gestión completa del ciclo de vida de la aplicación.
        
    - **Límite técnico:** Inicialmente dependía de un demonio monolítico centralizado con permisos de administrador en el host.
        
- **`OCI` — Open Container Initiative (2015)**
    
    - **Qué es:** Un estándar industrial e independiente para definir las especificaciones de las imágenes y la ejecución de los contenedores.
        
    - **Problema que resolvió:** Evitó el acoplamiento a un solo proveedor (Docker), permitiendo que herramientas como Kubernetes, Podman o CRI-O ejecuten los mismos contenedores usando runtimes universales como `runc`.
        
    - **Límite técnico:** Es un conjunto de especificaciones y estándares, no un software ejecutable por sí solo para el usuario.
        

**Síntesis:**

Un contenedor moderno funciona mediante la regla: **Namespaces** (aislamiento de visión) + **cgroups** (límite de recursos) + **Formato OCI** (portabilidad e imágenes por capas).

Pregunta: ¿Qué estandariza OCI y qué no estandariza?

Fuentes de partida: visión general de OCI y visión general de Docker. Contrasta “imagen”, “runtime” y “distribución”; una fuente externa es complemento, no reemplazo del contenido de la OVA.

Respuesta: La Open Container Initiative (OCI) estandariza los formatos y protocolos esenciales para la portabilidad del software en tres pilares: **imagen** (`image-spec`, estructura inmutable por capas), **runtime** (`runtime-spec`, ejecución y ciclo de vida de un _bundle_ desempacado) y **distribución** (`distribution-spec`, API de _push_/_pull_ en registros).

Por el contrario, la OCI **no estandariza** las herramientas de compilación y experiencia de usuario (como la CLI de Docker o la sintaxis del Dockerfile), la orquestación de clústeres (como Kubernetes), ni las interfaces de red o almacenamiento. Mientras la **imagen** define el empaquetado, la **distribución** regula su transferencia y el **runtime** gestiona su ejecución aislada.

---

# Comparador - Estación 3 

## VM y contenedor: límites distintos

| Criterio          | Máquina virtual                                   | Contenedor                                        | Pregunta de decisión                      |
| ----------------- | ------------------------------------------------- | ------------------------------------------------- | ----------------------------------------- |
| Kernel            | Kernel propio del SO invitado                     | Comparte el kernel del host                       | ¿Necesito otro SO o kernel?               |
| Aislamiento       | Límite fuerte mediante virtualización de hardware | Aislamiento de procesos y recursos                | ¿Cuál es el límite de confianza?          |
| Inicio y densidad | Mayor sobrecarga; inicia un SO                    | Menor sobrecarga; inicia procesos                 | ¿Cuántas instancias y con qué rapidez?    |
| Persistencia      | Discos virtuales y snapshots                      | Volúmenes o almacenamiento externo                | ¿Qué datos deben sobrevivir al reemplazo? |
| Operación         | Administración completa del SO                    | Artefactos reemplazables y observabilidad externa | ¿Qué debe administrar el equipo?          |

**Conceptos**: 

- Hipervisor tipo 1: Se ejecuta directamente sobre hardware y crea maquinas virtuales con recursos virtualizados.
- Hipervisor tipo 2:Se ejecuta como una aplicación sobre un sistema Operativo anfitrión, como virtualBOX o VMware.
- Docker Engine no es un hipervisor: Coordina imágenes, redes, volúmenes y contenedores. Los contenedores son procesos aislados que comparten el kernel, no son maquinas con hardware virtualizado y kernel aislado.

El error conceptual se encuentra en las afirmaciones **1** y **3**:

- **"Un contenedor es una VM pequeña" (ERROR CONCEPTUAL):** Un contenedor no virtualiza hardware ni ejecuta un sistema operativo completo con un kernel propio como una máquina virtual. Es simplemente un proceso del sistema operativo host aislado a nivel de kernel mediante _namespaces_ (aislamiento de visión) y _cgroups_ (limitación de recursos), compartiendo el kernel con el resto de los contenedores.
    
- **"Una imagen es un artefacto inmutable; un contenedor es una instancia ejecutable" (CORRECTO):** Esta afirmación es técnicamente exacta. La imagen actúa como la plantilla de solo lectura en capas, mientras que el contenedor es la ejecución en espacio de usuario con una capa de escritura efímera encima.
    
- **"Usar Docker vuelve automáticamente segura y altamente disponible una aplicación" (ERROR CONCEPTUAL):** Docker es únicamente el motor de empaquetado y ejecución local. No otorga seguridad por sí solo (si el código o las dependencias dentro del contenedor son vulnerables, el contenedor será vulnerable, y la ejecución por defecto con permisos de administrador o el kernel compartido añaden vectores de riesgo). Tampoco garantiza alta disponibilidad; para tolerancia a fallos, auto-escalado y autorreparación se requiere un orquestador (como Kubernetes) y una arquitectura diseñada para ello.

---

# Docker - Estación 4

## ¿Qué ocurre al ejecutar un contenedor?

*Un contenedor es una instancia ejecutable de una imagen; no es una máquina virtual detenida ni una garantía automática de seguridad o alta disponibilidad.*

**Tutorial Conceptual: ¿Qué ocurre al ejecutar un contenedor?**

**Del comando al proceso aislado**

- **Objetivo:** Interpretar la arquitectura interna y la secuencia de llamadas que ocurren al lanzar un contenedor sin necesidad de instalar Docker.
    
- **Resultado Esperado:** Distinguir claramente entre el plano de control, el runtime, el proceso y el kernel del sistema host.
    
- **Error Frecuente:** Confundir una imagen con un proceso, o suponer que el runtime reemplaza al kernel de Linux.
    
- **Aclaración Inicial:** Un contenedor es una instancia ejecutable de una imagen; no es una máquina virtual pequeña ni garantiza por sí solo seguridad o alta disponibilidad.
    

**1. Flujo Arquitectónico: Del Comando al Proceso Aislado**

Cuando un usuario ejecuta un comando de inicio (como `docker run`), la solicitud atraviesa cinco capas hasta convertirse en un proceso en ejecución:

`Docker CLI` $\rightarrow$ `Docker Engine` $\rightarrow$ `containerd` $\rightarrow$ `Runtime OCI (runc)` $\rightarrow$ `Proceso (Kernel)`

- **Docker CLI (Interfaz de Cliente):**
    
    - **Función:** Es la herramienta de línea de comandos con la que interactúa el usuario.
        
    - **Responsabilidad:** No ejecuta contenedores directamente. Traduce las instrucciones del usuario en peticiones HTTP/REST y las envía a través de un socket al plano de control.
        
- **Docker Engine / Daemon (`dockerd`):**
    
    - **Función:** Plano de control de alto nivel.
        
    - **Responsabilidad:** Recibe la solicitud del cliente, gestiona la autenticación, coordinar volúmenes, redes e imágenes (haciendo _pull_ si la imagen no existe localmente). Delega la gestión de contenedores a capas inferiores.
        
- **`containerd` (Manager de Runtimes):**
    
    - **Función:** Daemon de gestión de ciclo de vida completo de contenedores de nivel medio.
        
    - **Responsabilidad:** Supervisa el estado de las imágenes, gestiona el almacenamiento de capas y coordina la ejecución, parada o pausa de los contenedores mediante llamadas al runtime de bajo nivel.
        
- **Runtime OCI (`runc`):**
    
    - **Función:** Runtime ligero de bajo nivel conforme a la especificación OCI (_Open Container Initiative_).
        
    - **Responsabilidad:** Toma el _bundle_ del contenedor (configuración + sistema de archivos) y realiza las llamadas al sistema (_syscalls_) al kernel de Linux para configurar el entorno e iniciar el proceso. Una vez que el proceso arranca, `runc` finaliza su ejecución.
        
- **Proceso (Kernel de Linux):**
    
    - **Función:** Ejecución final del código de la aplicación.
        
    - **Responsabilidad:** Es el proceso estándar que corre sobre el **kernel compartido** del host, restringido en su visión y consumo de recursos.
        

**2. Aislamiento y Recursos: Los Pilares del Kernel**

Una vez lanzado el proceso, el kernel de Linux aplica dos mecanismos fundamentales para convertirlo en un "contenedor":

- **Namespaces (Aislamiento de Visión):**
    
    - **Pregunta guía:** ¿Qué puede ver el proceso?
        
    - **Definición:** Entregan vistas separadas de recursos globales del sistema como PID (árbol de procesos), red, puntos de montaje (`mnt`), usuarios (`user`), IPC y hostname (`uts`).
        
    - **Ejemplo:** Dentro del contenedor, un servidor web puede aparecer como **PID 1** y ver solo su red virtual privada, aunque en la máquina host sea el PID 4521 compartiendo la CPU con otros miles de procesos.
        
- **cgroups / Control Groups (Medición y Límites):**
    
    - **Pregunta guía:** ¿Cuánto puede usar el proceso?
        
    - **Definición:** Organizan, contabilizan y restringen el consumo de recursos físicos de hardware (CPU, memoria, E/S de disco, ancho de banda).
        
    - **Ejemplo:** Limitar un contenedor a 512 MB de RAM evita que un consumo desmedido interfiera con otros contenedores en el mismo servidor (solución al problema del _noisy neighbor_).
        

**3. Solucionario del Desafío: Clasificación de Responsabilidades (4/4)**

A continuación se muestra la resolución técnica para completar el desafío y activar los cuatro módulos:

- **Petición 1:** _"Entrega una vista aislada de PID, red o montajes."_
    
    - **Mecanismo:** **Namespaces**
        
    - **Explicación:** Regula la visibilidad y límites de contexto que tiene el proceso dentro del sistema.
        
- **Petición 2:** _"Organiza y controla el uso de CPU y memoria."_
    
    - **Mecanismo:** **cgroups**
        
    - **Explicación:** Define las cuotas y presupuestos de hardware asignados al grupo de procesos.
        
- **Petición 3:** _"Conserva datos fuera de la capa escribible del contenedor."_
    
    - **Mecanismo:** **Volumen**
        
    - **Explicación:** Permite la persistencia de datos montando un directorio del host o almacenamiento externo fuera de la capa efímera.
        
- **Petición 4:** _"Define cómo crear y ejecutar el proceso de un contenedor."_
    
    - **Mecanismo:** **Runtime OCI**
        
    - **Explicación:** Es la especificación e implementación (`runc`) encargada de invocar las primitivas del kernel para materializar la instancia.
        

**4. Consideración de Seguridad**

Compartir el kernel del host elimina la sobrecarga de memoria y CPU asociada a la virtualización tradicional, pero modifica sustancialmente el límite de aislamiento. Si un proceso logra explotar una vulnerabilidad en el kernel compartido, puede comprometer la máquina host. La seguridad efectiva de un contenedor debe reforzarse configurando:

- Permisos sin privilegios de `root` (`non-root user`).
    
- Limitación de capacidades del kernel (_Linux Capabilities_).
    
- Perfiles de acceso mediante `seccomp`, `AppArmor` o `SELinux`.
    
- Imágenes firmadas y escaneadas desde registros confiables.

---

# Casos - Estación 5

## Mesa de arquitectura 

*Primero aprende a leer un caso; después decide entre VM, contenedor, híbrido o falta información.*

**Los 6 Criterios de Evaluación**

- **1. SO y Kernel:** Determina si la carga de trabajo requiere módulos del kernel específicos, controladores de hardware propietarios o un sistema operativo completamente diferente al host.
    
- **2. Aislamiento y Confianza:** Evalúa el límite de seguridad necesario (_hard isolation_ mediante hipervisor vs. _soft isolation_ mediante namespaces del kernel).
    
- **3. Estado y Persistencia:** Analiza si la aplicación es _stateless_ (sin estado) o si requiere volúmenes de almacenamiento persistente desacoplados del ciclo de vida de la instancia.
    
- **4. Despliegue y Escala:** Mide la frecuencia de actualización, la necesidad de auto-escalado horizontal y los tiempos de arranque requeridos (segundos vs. minutos).
    
- **5. Operación:** Sopesa el coste operativo: administrar el ciclo de vida de un sistema operativo completo (parches, agentes, auditoría) frente a gestionar un artefacto empaquetado (imagen inmutable).
    
- **6. Compatibilidad y Soporte:** Verifica restricciones externas, como contratos de licencias, certificación de proveedores de software independientes (ISV) o normativas institucionales.
    

**II. Análisis Razonado del Caso 1: Empresa Logística (Sistema Heredado)**

**Contexto del Problema** El área de operaciones necesita alojar una aplicación de inventario legada, sin modificar su código fuente. Los antecedentes destacan tres restricciones severas: requiere Windows Server 2019, instala dos servicios del sistema junto a un controlador propietario y el soporte del proveedor exige una instalación completa del SO.

**1. Decisión de Arquitectura**

**Decisión:** **Máquina Virtual (VM)**

**2. Criterios de Sustentación**

- **Criterio Dominante: SO y Kernel**
    
    - **Análisis:** Los contenedores en Linux o Windows comparten el kernel del host. Un contenedor no permite la instalación ni carga de controladores propietarios (_drivers_) independientes que modifiquen el espacio de kernel de forma arbitraria. Al requerir controladores específicos y servicios de bajo nivel sobre Windows Server 2019, la arquitectura necesita la virtualización de hardware completa que ofrece una VM.
        
- **Criterio Secundario: Compatibilidad y Soporte**
    
    - **Análisis:** El contrato del proveedor estipula explícitamente que la garantía y el soporte técnico solo son válidos sobre una instalación completa del sistema operativo. Intentar empaquetar este software en un contenedor rompería el acuerdo de nivel de servicio (SLA) y dejaría a la empresa sin cobertura ante fallos críticos.
        

**3. Riesgo Principal y Evidencia Faltante**

- **Riesgo Principal:** **Ineficiencia de recursos y acoplamiento técnico.**
    
    - Alojar la aplicación en una VM implica acarrear toda la sobrecarga (_overhead_) de memoria RAM y CPU requerida por el SO Windows Server 2019. Esto genera un despliegue lento, aprovisionamiento pesado y una dificultad acumulada para automatizar o migrar la carga en el futuro.
        
- **Evidencia Faltante / Información a solicitar:**
    
    1. ¿Existe una hoja de ruta (_roadmap_) del proveedor para modernizar la aplicación hacia un modelo sin controladores propietarios?
        
    2. ¿Cuál es la estrategia de respaldos (backups) y tiempo de recuperación objetivo (RTO/RPO) para la máquina virtual completa?

---
# Test - Estación 6

**1. ¿Qué diferencia estructural condiciona principalmente el aislamiento?**

- **Respuesta correcta:** **La VM posee un kernel invitado; el contenedor comparte el kernel del host**
    
- **Explicación:** Las máquinas virtuales utilizan un hipervisor para simular hardware y ejecutar un sistema operativo completo con su propio kernel independientemente. Los contenedores son procesos administrados por el kernel del sistema operativo host mediante primitivas de aislamiento.
    

**2. ¿Cuál definición es correcta?**

- **Respuesta correcta:** **Un contenedor es una instancia ejecutable de una imagen**
    
- **Explicación:** Una imagen de contenedor es una plantilla inmutable de solo lectura compuesta por capas de archivos. El contenedor es la materialización ejecutable en tiempo de correo (_runtime_) que añade una capa de escritura efímera sobre dicha imagen.
    

**3. ¿Qué componente limita y contabiliza recursos?**

- **Respuesta correcta:** **cgroups**
    
- **Explicación:** Los _Control Groups_ (`cgroups`) son una funcionalidad del kernel de Linux diseñada específicamente para agrupar procesos, asignar cuotas y restringir el uso de recursos físicos como CPU, memoria RAM, I/O de disco y ancho de banda de red.
    

**4. ¿Dónde debería persistir el contenido cargado por usuarios?**

- **Respuesta correcta:** **En un volumen o almacenamiento externo con respaldo**
    
- **Explicación:** La capa de escritura de un contenedor es efímera y se destruye al eliminar la instancia. Para garantizar que los datos sobrevivan al ciclo de vida del contenedor, se deben utilizar volúmenes administrados o servicios de almacenamiento externo (S3, NFS, etc.).
    

**5. Una aplicación requiere un kernel distinto al host. ¿Qué opción es coherente?**

- **Respuesta correcta:** **VM**
    
- **Explicación:** Dado que los contenedores comparten el kernel de la máquina donde se ejecutan, no es posible correr una aplicación que requiera llamadas al sistema o módulos de un kernel diferente. Una Máquina Virtual es la única opción que permite virtualizar un kernel invitado distinto.
    

**6. ¿Qué función cumplen los namespaces de Linux en un contenedor?**

- **Respuesta correcta:** **Aislar vistas de procesos, red, montajes u otros recursos**
    
- **Explicación:** Los _namespaces_ de Linux aíslan la **visión** del sistema (qué puede ver un proceso). Permiten que un contenedor tenga su propia tabla de procesos (`pid`), su propia interfaz de red (`net`), sus propios puntos de montaje (`mnt`) y sus propios usuarios (`user`).
    

**7. ¿Por qué Docker Engine no es un hipervisor tipo 1?**

- **Respuesta correcta:** **Porque coordina procesos aislados que comparten el kernel, no VMs con hardware virtualizado y kernel invitado**
    
- **Explicación:** Un hipervisor tipo 1 (bare-metal) se ejecuta directamente sobre el hardware para virtualizar recursos de cómputo y alojar kernels independientes. Docker Engine es un motor de alto nivel que gestiona procesos en espacio de usuario dentro de un sistema operativo existente.
    

**8. ¿Qué evidencia demuestra mejor un criterio arquitectónico?**

- **Respuesta correcta:** **Decisión, dos criterios, riesgo y condición de cambio**
    
- **Explicación:** Elegir infraestructura no consiste en seleccionar tecnologías por moda o velocidad. Un verdadero criterio arquitectónico requiere tomar una decisión clara, sustentarla con al menos dos criterios técnicos, identificar los riesgos operativos explícitos y definir bajo qué condiciones se cambiaría de alternativa.

---

# Cierre - Estación 7

**Ticket de Salida: Evidencia de Razonamiento Arquitectónico**

**1. Servicio seleccionado y Decisión**

- **Servicio:** Base de Datos Relacional Principal del CMS (ej. PostgreSQL / MySQL) con datos transaccionales críticos.
    
- **Decisión:** **Máquina Virtual (VM)**
    

**2. Criterios que sostienen la decisión**

- **Criterio 1: Estado y Persistencia (Aislamiento de I/O y Ciclo de Vida)**
    
    - **Fundamento:** Una base de datos relacional de alto tráfico requiere gestión directa de I/O de disco, tuneo fino de subsistema de archivos y persistencia estricta. Alojarla en una VM dedicada con almacenamiento adjunto bloque a bloque evita la sobrecarga de capas de abstracción complejas y garantiza que los datos sobrevivan sin depender del ciclo de vida efímero de las imágenes.
        
- **Criterio 2: Aislamiento y Confianza (Seguridad del Kernel)**
    
    - **Fundamento:** Al ser el componente que almacena la información más sensible de la empresa, requiere un límite de aislamiento de hardware (_hard isolation_). Ejecutar el motor de base de datos en una VM evita que una vulnerabilidad o fallo en otra aplicación (como el CMS web) que comprometa el kernel compartido del host pueda acceder a la memoria de la base de datos.
        

**3. Condición que haría cambiar la decisión**

- **Condición de cambio:** Cambiaría a un enfoque de **Contenedores (o Híbrido)** si el entorno fuera exclusivo para desarrollo/QA, si la base de datos se rediseñara como una arquitectura distribuida nativa de la nube (_cloud-native_) con réplicas stateless automatizadas mediante un _Operator_ en un orquestador (como Kubernetes), o si la empresa adoptara un servicio administrado de base de datos (DBaaS) que gestione el aislamiento por debajo.