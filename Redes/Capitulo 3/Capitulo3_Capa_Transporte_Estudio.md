# Capítulo 3: Capa de Transporte
### Computer Networking: A Top-Down Approach — Kurose & Ross, 8ª ed.
> Guía completa de estudio para certamen

---

## Índice
1. [Servicios de la Capa de Transporte](#1-servicios-de-la-capa-de-transporte)
2. [Multiplexación y Demultiplexación](#2-multiplexación-y-demultiplexación)
3. [UDP: Transporte Sin Conexión](#3-udp-transporte-sin-conexión)
4. [Principios de Transferencia Confiable (rdt)](#4-principios-de-transferencia-confiable-rdt)
5. [Go-Back-N y Repetición Selectiva](#5-go-back-n-y-repetición-selectiva)
6. [TCP: Transporte Orientado a la Conexión](#6-tcp-transporte-orientado-a-la-conexión)
7. [Control de Flujo TCP](#7-control-de-flujo-tcp)
8. [Gestión de Conexiones TCP](#8-gestión-de-conexiones-tcp)
9. [Principios del Control de Congestión](#9-principios-del-control-de-congestión)
10. [Control de Congestión TCP](#10-control-de-congestión-tcp)
11. [Evolución: QUIC](#11-evolución-quic)
12. [Resumen Rápido y Tabla Comparativa](#12-resumen-rápido-y-tabla-comparativa)

---

## 1. Servicios de la Capa de Transporte

### ¿Qué hace la capa de transporte?

Proporciona **comunicación lógica entre procesos** que se ejecutan en hosts diferentes. Es importante distinguirla de la capa de red:

| Capa | Comunica entre... | Ejemplo |
|------|-------------------|---------|
| Red (IP) | Hosts (máquinas) | De PC A a Servidor B |
| Transporte | Procesos (aplicaciones) | Del proceso navegador al proceso servidor web |

**Analogía del libro:** Imagina 12 niños en la casa de Ann que escriben cartas a 12 niños en la casa de Bill. El servicio postal (capa de red) lleva las cartas de casa a casa. Ann y Bill (capa de transporte) se encargan de repartir cada carta al niño correcto dentro de su casa.

### Acciones del emisor y receptor

**Emisor:**
1. Recibe un mensaje de la capa de aplicación.
2. Determina los valores de los campos del encabezado del segmento.
3. Crea el segmento (agrega cabecera al mensaje).
4. Pasa el segmento a la capa de red (IP).

**Receptor:**
1. Recibe el segmento de IP.
2. Verifica los valores de la cabecera.
3. Extrae el mensaje de aplicación.
4. Desmultiplexa el mensaje al socket correcto.

### TCP vs UDP — Diferencias clave

**TCP (Transmission Control Protocol):**
- Entrega confiable y **ordenada**.
- Control de congestión.
- Control de flujo.
- Establecimiento de conexión (handshake).
- Más lento, más seguro.

**UDP (User Datagram Protocol):**
- Entrega **no confiable** y posiblemente desordenada.
- Extensión mínima del servicio "mejor esfuerzo" de IP.
- Sin garantías de entrega, orden, ni ancho de banda.
- Más rápido, sin overhead de conexión.

> **Para el certamen:** La capa de transporte no puede garantizar retardo mínimo ni ancho de banda mínimo, porque eso dependería de la capa de red. Solo puede entregar confiabilidad y orden (TCP) o bien velocidad sin garantías (UDP).

---

## 2. Multiplexación y Demultiplexación

### Concepto central

Múltiples procesos en un host comparten **un único enlace de red**. La capa de transporte necesita saber a qué proceso entregar cada segmento que llega. Los **puertos** son el mecanismo que lo hace posible.

- **Multiplexación (en el emisor):** Recoger datos de múltiples sockets, agregar cabeceras de transporte y enviarlos por el canal.
- **Demultiplexación (en el receptor):** Leer la información del encabezado del segmento recibido y entregarlo al socket correcto.

### ¿Cómo funciona la demultiplexación?

Cada datagrama IP que llega al host trae:
- Dirección IP de origen y destino.
- Un segmento de capa de transporte.
- Dentro del segmento: **número de puerto de origen** y **número de puerto de destino**.

El host usa IPs + puertos para dirigir el segmento al socket correcto.

### Demultiplexación sin conexión (UDP)

UDP identifica el socket destino usando **solo el puerto de destino**.

Esto significa que dos datagramas UDP de hosts completamente distintos pero con el mismo puerto de destino llegan al **mismo socket**. El socket UDP no distingue de quién vino el paquete.

```
Cliente A (puerto 9157)  ──┐
                            ├──► Puerto destino 6428 → mismo socket UDP
Cliente B (puerto 5775)  ──┘
```

### Demultiplexación orientada a la conexión (TCP)

TCP identifica el socket destino usando la **cuádrupla completa**:
1. IP de origen
2. Puerto de origen
3. IP de destino
4. Puerto de destino

Esto significa que dos clientes que se conectan al **mismo puerto 80** del servidor generan **dos sockets distintos**, uno por cada cliente, porque sus IPs o puertos de origen son diferentes.

```
Cliente A (IP=A, puerto=9157) → puerto 80 del servidor → socket 1
Cliente C (IP=C, puerto=9157) → puerto 80 del servidor → socket 2
```

|                            | UDP                                   | TCP                     |
| -------------------------- | ------------------------------------- | ----------------------- |
| ¿Sé si el otro está listo? | No                                    | Sí (handshake)          |
| ¿Sé si llegó?              | No                                    | Sí (ACKs)               |
| ¿Llega en orden?           | No garantizado                        | Sí                      |
| ¿Frena en congestión?      | No                                    | Sí                      |
| ¿Es rápido?                | Sí                                    | Más lento               |
| ¿Cuándo usarlo?            | Latencia crítica, pérdidas aceptables | Confiabilidad necesaria |


> **Para el certamen:** Esta es la diferencia fundamental. UDP: demultiplexa solo con puerto destino. TCP: necesita la cuádrupla completa. Por eso un servidor web puede atender miles de conexiones simultáneas en el puerto 80 — cada una tiene su propio socket.

---

## 3. UDP: Transporte Sin Conexión

### ¿Por qué existe UDP si es "peor" que TCP?

UDP tiene ventajas reales para ciertos casos:

- **Sin establecimiento de conexión:** No hay RTT de handshake antes de enviar datos. DNS necesita una respuesta rápida; no puede perder tiempo en un handshake.
- **Sin estado de conexión:** El emisor y el receptor no mantienen variables de estado. Puede soportar más clientes simultáneos.
- **Cabecera pequeña:** Solo 8 bytes (vs. 20 bytes de TCP).
- **Sin control de congestión:** UDP puede enviar tan rápido como desee, incluso en condiciones de congestión de red. Útil para streaming donde es peor pausar que perder un frame.

### ¿Cuándo usar UDP?

- Aplicaciones multimedia de streaming (tolerantes a pérdidas, sensibles a la velocidad): video llamadas, streaming de audio/video.
- DNS (resolución de nombres: necesita rapidez).
- SNMP (monitoreo de red).
- HTTP/3 (implementa confiabilidad propia sobre UDP).

### Estructura del segmento UDP

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Puerto Origen        |        Puerto Destino          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|            Longitud           |           Checksum             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                    Datos (payload)                            |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- **Longitud:** Longitud total del segmento UDP en bytes (cabecera + datos). Mínimo 8 bytes.
- **Checksum:** Suma de verificación para detectar errores.

### UDP Checksum (Suma de Verificación)

**Objetivo:** Detectar bits invertidos (errores) en el segmento transmitido.

**Emisor:**
1. Trata el contenido del segmento UDP (incluyendo cabecera y direcciones IP) como una secuencia de enteros de 16 bits.
2. Calcula la suma en **complemento a uno** de todos esos enteros.
3. Coloca el resultado en el campo checksum.

**Receptor:**
1. Calcula el checksum del segmento recibido.
2. Compara con el campo checksum:
   - **Distinto:** Se detectó un error. El segmento se descarta (o se entrega con advertencia).
   - **Igual:** No se detectó ningún error... *pero podrían existir*. El checksum no es infalible (protección débil).

**¿Por qué es débil?** Dos errores compensatorios pueden pasar desapercibidos: si un bit sube y otro baja en el lugar correcto, la suma puede ser la misma.

**Ejemplo de cálculo:**
```
Número 1: 1110 0110 1100 1100
Número 2: 1101 0101 0101 0101
Suma:   1 1011 1011 1011 1011  (el carry del MSB se envuelve: wraparound)
Final:     1011 1011 1100 0000  (después del wraparound)
Checksum:  0100 0100 0011 1111  (complemento a uno: invertir bits)
```

> **Para el certamen:** El checksum UDP detecta errores pero no los corrige. Si necesitas confiabilidad real, debes agregarla en la capa de aplicación (como hace HTTP/3 sobre QUIC).

---

## 4. Principios de Transferencia Confiable (rdt)

### El problema fundamental

La capa de transporte quiere ofrecer un canal **confiable** aunque el canal de red subyacente sea **no confiable** (puede perder paquetes, invertir bits, reordenar). La complejidad del protocolo depende de qué tan malo sea el canal.

El emisor y el receptor desconocen el estado del otro a menos que se lo comuniquen explícitamente.

### Evolución de los protocolos rdt

#### rdt 1.0 — Canal perfectamente confiable

**Supuesto:** No hay errores de bits, no hay pérdida de paquetes.

**Comportamiento:** El emisor envía, el receptor recibe. Sin mecanismo de control.

Esto es trivial y no ocurre en la práctica.

---

#### rdt 2.0 — Canal con errores de bits (sin pérdida)

**Supuesto:** El canal puede invertir bits. No pierde paquetes.

**Mecanismo:** ACK/NAK
- **ACK (Acknowledgement):** El receptor le dice al emisor "paquete recibido correctamente".
- **NAK (Negative Acknowledgement):** El receptor le dice al emisor "paquete con errores, retransmite".

**Modelo:** Stop-and-Wait — el emisor envía un paquete y espera la respuesta antes de enviar el siguiente.

**Fallo fatal de rdt 2.0:** ¿Qué pasa si el ACK o el NAK se corrompe?
- El emisor no sabe qué ocurrió en el receptor.
- Si retransmite, el receptor puede recibir un **duplicado** y no sabe si es nuevo o repetido.

---

#### rdt 2.1 — Manejo de ACK/NAK corruptos

**Solución:** Agregar **números de secuencia** (0 y 1 son suficientes en stop-and-wait).

- El emisor agrega el número de secuencia (0 o 1) a cada paquete.
- El receptor verifica si el paquete es nuevo o duplicado según el número de secuencia esperado.
- Si llega un ACK/NAK corrupto, el emisor retransmite. El receptor descarta duplicados.

**¿Por qué 1 bit (0 y 1) es suficiente?** En stop-and-wait solo hay un paquete "en vuelo" a la vez. Solo necesitas saber si el paquete es el actual (1) o el anterior retransmitido (0).

---

#### rdt 2.2 — Sin NAK (solo ACKs)

**Idea:** En lugar de enviar NAK, el receptor envía ACK del **último paquete correcto recibido** (con su número de secuencia explícito).

- Si el emisor recibe un **ACK duplicado**, actúa igual que con un NAK: retransmite el paquete actual.
- TCP usa exactamente este enfoque (no usa NAK).

---

#### rdt 3.0 — Canal con errores Y pérdidas

**Nuevo problema:** El canal puede perder paquetes (datos o ACKs), no solo corromperlos.

**Solución:** **Temporizador (timer)** en el emisor.

- El emisor espera un tiempo razonable por el ACK.
- Si el timer expira sin recibir ACK → **retransmite**.
- Si el paquete no se perdió sino que se retrasó: el receptor detectará el duplicado con el número de secuencia y lo descartará.

**Funcionamiento completo de rdt 3.0:**

| Escenario | ¿Qué ocurre? |
|-----------|-------------|
| Sin pérdida | Normal: pkt → ACK → siguiente pkt |
| Pérdida del paquete | Timer expira → retransmisión |
| Pérdida del ACK | Timer expira → retransmisión → receptor descarta duplicado, reenvía ACK |
| ACK retrasado | Timer expira → retransmisión → llega ACK tardío y es ignorado (número de secuencia equivocado) |

### Rendimiento de rdt 3.0 (Stop-and-Wait)

El problema de stop-and-wait es que es muy ineficiente cuando el RTT es grande.

**Ejemplo:** Enlace de 1 Gbps, retardo de propagación 15 ms, paquete de 8000 bits.

- Tiempo para transmitir el paquete: `Dtrans = 8000 bits / 10^9 bps = 0.008 ms`
- RTT ≈ 30 ms

```
Utilización del emisor = (L/R) / (RTT + L/R) = 0.008 ms / 30.008 ms ≈ 0.00027
```

Solo el 0.027% del tiempo el enlace está siendo usado. Esto es terrible.

### Pipelining — La solución al rendimiento

**Pipelining:** El emisor envía múltiples paquetes sin esperar el ACK de cada uno.

- Aumenta la utilización del enlace.
- Requiere mayor rango de números de secuencia.
- Requiere buffering en el emisor y/o receptor.

Con un pipeline de 3 paquetes, la utilización se multiplica por 3 (≈ 0.00081). Con ventanas más grandes, se acerca al 100%.

Hay dos enfoques de pipelining: **Go-Back-N** y **Repetición Selectiva**.

---

## 5. Go-Back-N y Repetición Selectiva

### Go-Back-N (GBN)

**Concepto de ventana:** El emisor puede tener hasta **N paquetes** en tránsito (enviados pero sin ACK).

```
|  ACKed  | en tránsito sin ACK | disponible para enviar | fuera de ventana |
    ↑             ↑
  base        base+N-1
```

**Comportamiento del emisor:**
- Mantiene timer para el paquete más antiguo en tránsito.
- Si el timer expira para el paquete `n`: **retransmite n y TODOS los paquetes con número de secuencia mayor** dentro de la ventana.
- ACK(n) es **acumulativo**: confirma todos los paquetes hasta `n` inclusive. Al recibir ACK(n), la ventana avanza a `n+1`.

**Comportamiento del receptor:**
- Solo envía ACK para paquetes **en orden**. Si llega un paquete fuera de orden, lo **descarta** (no lo bufferiza) y reenvía el ACK del último paquete en orden recibido correctamente.
- Solo necesita recordar `rcv_base` (el número de secuencia del siguiente paquete esperado).

**Ventaja:** Simple, el receptor no necesita buffer.

**Desventaja:** Si se pierde un paquete, se retransmiten muchos paquetes innecesarios.

---

### Repetición Selectiva (SR)

**Concepto:** El receptor confirma **individualmente** cada paquete recibido correctamente. El emisor solo retransmite los paquetes **específicamente no confirmados**.

**Comportamiento del emisor:**
- Mantiene un timer **por cada paquete** no confirmado.
- Si el timer de `n` expira → retransmite solo el paquete `n`.
- Al recibir ACK(n): marca `n` como recibido. Si `n` es el paquete sin confirmar más pequeño, avanza la ventana.

**Comportamiento del receptor:**
- Almacena en buffer los paquetes fuera de orden (no los descarta).
- Al recibir el paquete faltante, entrega todos los paquetes en orden al nivel superior de una vez.
- Envía ACK individual por cada paquete recibido correctamente, incluso fuera de orden.

**Ventaja:** Solo retransmite lo necesario, más eficiente ante pérdidas.

**Desventaja:** Más complejo, el receptor necesita buffer.

---

### El Dilema de la Repetición Selectiva

**Problema:** Si el espacio de números de secuencia es demasiado pequeño relativo al tamaño de ventana, el receptor puede confundir un paquete **nuevo** con una **retransmisión**.

**Ejemplo:** Seq #s = {0,1,2,3}, ventana = 3.

- Escenario (a): Todo funciona bien. Los ACKs 0,1,2 llegan y la ventana avanza. Si llega pkt0 de nuevo, el receptor sabe que es un paquete nuevo.
- Escenario (b): Los 3 ACKs se pierden. El emisor retransmite pkt0. El receptor (cuya ventana avanzó) acepta pkt0 creyendo que es el **próximo paquete nuevo**. ¡Error!

**Regla:** El tamaño de la ventana SR debe ser ≤ la mitad del espacio de números de secuencia.

```
Tamaño ventana SR ≤ (espacio de secuencias) / 2
```

Para GBN la restricción es menos severa: ventana ≤ espacio de secuencias - 1.

> **Para el certamen:** Este dilema es pregunta clásica. Memorizar la regla: **ventana SR ≤ 2^(k-1)** donde k es el número de bits del número de secuencia.

### Comparación GBN vs SR

| Característica | Go-Back-N | Repetición Selectiva |
|----------------|-----------|----------------------|
| ACKs | Acumulativos | Individuales |
| Paquetes fuera de orden | Descarta | Bufferiza |
| Retransmisión en pérdida | Paquete + todos los siguientes | Solo el paquete perdido |
| Buffer en receptor | No necesita | Sí necesita |
| Timers en emisor | Uno (para el más antiguo) | Uno por paquete |
| Eficiencia ante pérdidas | Menor | Mayor |

---

## 6. TCP: Transporte Orientado a la Conexión

### Características principales de TCP

- **Punto a punto:** Un emisor, un receptor.
- **Flujo de bytes confiable y ordenado:** TCP ve los datos como un flujo continuo de bytes, sin límites de mensaje.
- **Full-duplex:** Comunicación bidireccional simultánea en la misma conexión.
- **Confirmaciones acumulativas:** Un ACK confirma todos los bytes hasta ese número.
- **Pipelining:** Múltiples segmentos en vuelo simultáneamente.
- **Orientado a la conexión:** Requiere handshake antes de datos.
- **Control de flujo:** El emisor no saturará el buffer del receptor.
- **MSS (Maximum Segment Size):** Tamaño máximo de datos en un segmento TCP.

### Estructura del Segmento TCP

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Puerto Origen        |        Puerto Destino          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Número de Secuencia                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  Número de Confirmación (ACK)                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  HLen |  Res  |C|E|U|A|P|R|S|F|    Ventana de Recepción       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|            Checksum           |        Puntero Urgente         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Opciones (variable)                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Datos                                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Campos clave:**
- **Número de Secuencia:** Número del **primer byte** de datos de este segmento (cuenta bytes, no segmentos).
- **Número de ACK:** El número del **próximo byte que espera recibir** del otro lado. Confirmación acumulativa.
- **rwnd (Ventana de Recepción):** Espacio libre en el buffer del receptor. Usado para control de flujo.
- **Flags:** SYN (establecer conexión), FIN (cerrar conexión), ACK (confirmación válida), RST (reset), PSH (enviar datos a la app inmediatamente), URG (datos urgentes).
- **C, E:** Bits de notificación de congestión (ECN).

### Números de Secuencia y ACKs

**Ejemplo clásico con telnet:**

```
Host A                                    Host B
  │                                          │
  │ ← Usuario teclea 'C'                     │
  │                                          │
  │ Seq=42, ACK=79, data='C' ──────────────► │
  │                                          │ ← Host B recibe 'C', hace eco
  │ ◄────────────────────── Seq=79, ACK=43, data='C'
  │                                          │
  │ Seq=43, ACK=80 ────────────────────────► │
  │                                          │
```

- Host A envía 'C' (1 byte) con Seq=42. El próximo byte de A será el 43.
- Host A tiene ACK=79, lo que significa que A ha recibido todo hasta el byte 78 y espera el byte 79 de B.
- Host B confirma con ACK=43, diciendo "recibí hasta el byte 42, espero el 43".

> **Para el certamen:** El número de ACK siempre es el número de secuencia del **próximo byte esperado**, no el del último recibido. Si recibí el byte 100 y era de largo 57, mi ACK será 157.

### RTT y Timeout TCP

**Problema:** ¿Cuánto tiempo esperar antes de retransmitir?

- Si el timeout es muy corto → retransmisiones innecesarias.
- Si el timeout es muy largo → reacción lenta ante pérdidas.

**Solución:** Estimar el RTT dinámicamente.

**SampleRTT:** Tiempo medido desde la transmisión de un segmento hasta recibir su ACK (ignorando retransmisiones).

**EstimatedRTT** (media móvil ponderada exponencialmente — EWMA):

```
EstimatedRTT = (1 - α) × EstimatedRTT + α × SampleRTT
```

Valor típico: **α = 0.125**

La influencia de muestras pasadas decrece exponencialmente. Las mediciones recientes pesan más.

**DevRTT** (desviación, también EWMA):

```
DevRTT = (1 - β) × DevRTT + β × |SampleRTT - EstimatedRTT|
```

Valor típico: **β = 0.25**

**TimeoutInterval** (el timeout real):

```
TimeoutInterval = EstimatedRTT + 4 × DevRTT
```

El factor 4 actúa como margen de seguridad. Si el RTT varía mucho (DevRTT grande), el timeout será mayor.

### Retransmisión en TCP

**Evento 1: Timeout**
- El timer del segmento más antiguo sin confirmar expira.
- Se retransmite ese segmento.
- Se reinicia el timer.

**Evento 2: Triple ACK Duplicado (Fast Retransmit)**
- El emisor recibe **3 ACKs duplicados** del mismo número de secuencia.
- Esto indica que probablemente ese segmento se perdió (los siguientes llegaron, pero el receptor sigue pidiendo el faltante).
- El emisor retransmite el segmento faltante **sin esperar el timeout**.
- Esto es mucho más rápido que esperar el timer.

```
          Host A                        Host B
            │ pkt 0 ──────────────────► │
            │ pkt 1 ──────────────────► │
            │ pkt 2 ──────────────────► │ (se pierde)
            │ pkt 3 ──────────────────► │
            │                          │
            │ ◄──────────────── ACK=2  │ (espera pkt 2)
            │ ◄──────────────── ACK=2  │ (llegó pkt 3, sigue esperando 2)
            │ ◄──────────────── ACK=2  │ (llegó pkt 4, sigue esperando 2)
            │                          │
            │ ← 3 ACK dup. → retransmite pkt 2 inmediatamente
```

### Generación de ACKs en el Receptor (RFC 5681)

| Evento | Acción del receptor |
|--------|---------------------|
| Llega segmento en orden, todos anteriores ya ACKeados | Espera hasta 500ms antes de enviar ACK (ACK retrasado) |
| Llega segmento en orden, hay un ACK pendiente | Envía ACK acumulativo inmediatamente |
| Llega segmento fuera de orden (gap detectado) | Envía ACK duplicado indicando el próximo byte esperado |
| Llega segmento que llena un gap | Envía ACK inmediatamente si llena el límite inferior del gap |

---

## 7. Control de Flujo TCP

### El problema

La capa de red puede entregar datos más rápido de lo que la capa de aplicación los consume del buffer de socket. Si el buffer se llena y el emisor sigue enviando, los datos se pierden.

### Solución: Ventana de Recepción (rwnd)

El receptor anuncia al emisor cuánto espacio libre tiene en su buffer usando el campo **rwnd** del encabezado TCP.

```
RcvBuffer
│◄────────────────────────── RcvBuffer ──────────────────────────►│
│  datos que ya llegaron  │          espacio libre                 │
│   (buffered data)       │◄──────── rwnd ────────────────────────►│
```

**Regla del emisor:**

```
LastByteSent - LastByteAcked ≤ rwnd
```

El emisor limita los datos "en vuelo" (enviados pero no confirmados) al valor de rwnd recibido.

**Tamaño típico del RcvBuffer:** 4096 bytes por defecto, aunque muchos SO ajustan automáticamente.

**Window Scaling (WS):** Negociado en el handshake, permite multiplicar rwnd por un factor (hasta 2^14). Esto es necesario en enlaces de alta velocidad o alto RTT donde rwnd de 16 bits no es suficiente.

> **Para el certamen:** rwnd ≠ cwnd. `rwnd` es la ventana de recepción (control de flujo, limitado por el buffer del receptor). `cwnd` es la ventana de congestión (control de congestión, calculado por el emisor). El emisor usa `min(cwnd, rwnd)` para determinar cuántos datos enviar.

---

## 8. Gestión de Conexiones TCP

### Three-Way Handshake (Apertura de Conexión)

Antes de enviar datos, emisor y receptor realizan un "apretón de manos" de tres vías para:
1. Confirmar que ambos están listos para comunicarse.
2. Acordar los números de secuencia iniciales (ISN — Initial Sequence Number).

```
     Cliente                              Servidor
        │                                    │
        │  SYN (SYNbit=1, Seq=x)             │
        │ ──────────────────────────────────►│
        │                                    │ Estado: SYN_RCVD
        │  SYN-ACK (SYNbit=1, Seq=y,         │
        │           ACKbit=1, ACKnum=x+1)    │
        │ ◄──────────────────────────────────│
Estado: │                                    │
ESTAB   │  ACK (ACKbit=1, ACKnum=y+1)        │
        │ ──────────────────────────────────►│ Estado: ESTAB
        │                                    │
        │         ← Datos fluyen →           │
```

**Paso 1 — SYN:** El cliente elige su ISN `x` y envía SYN. El cliente pasa a `SYN_SENT`.

**Paso 2 — SYN-ACK:** El servidor elige su ISN `y` y responde confirmando el SYN del cliente (ACKnum=x+1). El servidor pasa a `SYN_RCVD`.

**Paso 3 — ACK:** El cliente confirma el SYN del servidor (ACKnum=y+1). Ambos pasan a `ESTABLISHED`.

**¿Por qué 3 pasos y no 2?** Con solo 2 mensajes (handshake de 2 vías), el servidor nunca sabría si el cliente recibió el SYN-ACK. Sin confirmación mutua, podrían quedar conexiones "medio abiertas" con datos de estado sin usar.

### Cierre de Conexión TCP (4-Way Handshake)

```
     Cliente                              Servidor
        │  FIN (FINbit=1, seq=x)          │
        │ ──────────────────────────────►│
        │                                 │ Estado: CLOSE_WAIT
        │  ACK (ACKnum=x+1)               │ (puede seguir enviando)
        │ ◄──────────────────────────────│
Estado: │                                 │
FIN_WAIT_2│                               │
        │                                 │
        │  FIN (FINbit=1, seq=y)          │
        │ ◄──────────────────────────────│ Estado: LAST_ACK
        │  ACK (ACKnum=y+1)               │
        │ ──────────────────────────────►│ Estado: CLOSED
Estado: │                                 │
TIMED_WAIT│ (espera 2*MSL para seguridad) │
        │                                 │
CLOSED  │                                 │
```

Cada lado cierra su **mitad** de la conexión con un FIN. El otro lado responde con ACK y luego envía su propio FIN. El cliente espera en TIMED_WAIT (2× el tiempo máximo de vida de un segmento) antes de cerrar definitivamente, para asegurarse de que el ACK llegó.

---

## 9. Principios del Control de Congestión

### ¿Qué es la congestión?

**Informalmente:** "Demasiadas fuentes enviando demasiados datos demasiado rápido para que la red pueda gestionarlos."

**Manifestaciones:**
- Grandes retardos (paquetes en colas de routers).
- Pérdida de paquetes (overflow de buffers en routers).

**Diferencia con control de flujo:**
- **Control de flujo:** Un emisor demasiado rápido para **un** receptor específico.
- **Control de congestión:** Demasiados emisores para la capacidad de la **red**.

### Escenarios de Congestión (Causas y Costos)

**Escenario 1 — Router con buffer infinito, sin retransmisión:**
- Al acercarse a la capacidad R/2, el throughput se estabiliza en R/2.
- Pero los retardos crecen hacia infinito. Nadie pierde paquetes, pero la red se vuelve inutilizable por latencia.

**Escenario 2 — Router con buffer finito, con retransmisión:**
- Los paquetes se pierden cuando el buffer se llena.
- El emisor retransmite → mayor carga en la red.
- Costos:
  - Trabajo extra (retransmisiones) para el mismo throughput efectivo.
  - Retransmisiones innecesarias (si el timeout fue prematuro): el enlace lleva múltiples copias del mismo paquete, reduciendo el throughput máximo alcanzable.

**Escenario 3 — Múltiples saltos, múltiples emisores:**
- Cuando un paquete se pierde en un router downstream, toda la capacidad de transmisión y buffering usada para ese paquete en los routers anteriores fue **desperdiciada**.

### Enfoques para el Control de Congestión

1. **Control de congestión de extremo a extremo:**
   - Sin retroalimentación explícita de la red.
   - Los extremos infieren congestión de pérdidas y retardos observados.
   - **Enfoque de TCP clásico.**

2. **Control de congestión asistido por red:**
   - Los routers informan directamente a los hosts sobre congestión.
   - Pueden indicar el nivel de congestión o establecer la tasa de envío.
   - Ejemplos: TCP ECN, ATM, DECbit.

---

## 10. Control de Congestión TCP

### AIMD — Additive Increase, Multiplicative Decrease

TCP sondea continuamente el ancho de banda disponible usando AIMD:

- **Incremento Aditivo (AI):** Aumenta la tasa de envío en **1 MSS por RTT** hasta que se detecta pérdida.
- **Disminución Multiplicativa (MD):** Reduce la tasa de envío a la **mitad** cuando se detecta pérdida.

Esto produce el **comportamiento en diente de sierra** característico de TCP: sube linealmente, baja a la mitad, sube de nuevo.

**¿Por qué AIMD?** Es un algoritmo distribuido y asíncrono que ha demostrado optimizar las tasas de flujo en toda la red y tener propiedades de estabilidad deseables (convergencia a equidad).

### La Variable cwnd (Congestion Window)

El emisor TCP limita los datos en tránsito:

```
LastByteSent - LastByteAcked ≤ min(cwnd, rwnd)
```

La tasa de envío aproximada es:

```
tasa ≈ cwnd / RTT  bytes/seg
```

`cwnd` se ajusta dinámicamente según la congestión observada.

### Slow Start (Inicio Lento)

Al inicio de la conexión (o después de un timeout), `cwnd` comienza pequeño y crece **exponencialmente**:

- Inicio: `cwnd = 1 MSS`
- Por cada ACK recibido: `cwnd += 1 MSS`
- Resultado: `cwnd` se **duplica cada RTT**.

Esto parece contradictorio con "inicio lento", pero el nombre refiere a que comienza despacio (1 MSS) en lugar de enviar todo de golpe. El crecimiento exponencial permite detectar rápidamente el ancho de banda disponible.

**¿Cuándo deja de ser exponencial?** Cuando `cwnd` alcanza `ssthresh` (slow start threshold). A partir de ese punto, el crecimiento se vuelve **lineal** (Congestion Avoidance).

### Congestion Avoidance (Evitación de Congestión)

Cuando `cwnd ≥ ssthresh`:
- Por cada ACK recibido: `cwnd += MSS × (MSS/cwnd)` (aproximadamente +1 MSS por RTT).
- Crecimiento **lineal**, más cauteloso.

### Reacción a la Pérdida

**Pérdida por triple ACK duplicado (TCP Reno):**
- `ssthresh = cwnd / 2`
- `cwnd = ssthresh + 3 MSS` (fast recovery)
- Continúa en Congestion Avoidance.
- Más suave: infiere congestión pero no catástrofe.

**Pérdida por timeout (TCP Tahoe / Reno):**
- `ssthresh = cwnd / 2`
- `cwnd = 1 MSS`
- Vuelve a Slow Start.
- Más agresivo: timeout indica congestión severa.

### Diagrama de Estados del Control de Congestión

```
Estado inicial:
  cwnd = 1 MSS
  ssthresh = 64 KB
  dupACKcount = 0

                    ┌──────────────┐
              ┌────►│  SLOW START  │◄────────────────────┐
              │     └──────┬───────┘                     │
              │            │ cwnd > ssthresh              │
              │            ▼                              │ timeout:
        timeout│     ┌──────────────────────┐            │ ssthresh=cwnd/2
        ssthresh=cwnd/2│ CONGESTION AVOIDANCE│            │ cwnd=1
        cwnd=1 │     └──────────┬───────────┘            │
              │                │                          │
              │                │ triple dupACK:           │
              │                │ ssthresh=cwnd/2          │
              │                │ cwnd=ssthresh+3          │
              │                ▼                          │
              │         ┌──────────────┐                  │
              └─────────┤ FAST RECOVERY│──────────────────┘
                        └──────────────┘
                              │
                              │ nuevo ACK:
                              │ cwnd=ssthresh
                              ▼
                        CONGESTION AVOIDANCE
```

### TCP CUBIC

Alternativa a AIMD clásico, **predeterminado en Linux**:

- **Idea:** Después de una pérdida, la tasa de envío fue reducida a la mitad. La congestión en el cuello de botella probablemente no cambió mucho.
- TCP CUBIC aumenta W en función del **cubo del tiempo** transcurrido desde el último evento de congestión.
- Crece rápido cuando está lejos de `Wmax` (el ancho de banda donde ocurrió la última pérdida).
- Se vuelve cauteloso al acercarse a `Wmax`.
- Logra mayor throughput que TCP Reno en enlaces de alta velocidad.

```
            Wmax ─────────────────────────────────────────────────────
                                              ╭──────────────────
         Wmax/2 ─────────────────────────╭───╯
                              TCP CUBIC ╭╯
                         ──────────────╯
                        ╱  TCP Reno (lineal)
                       ╱
```

### Control de Congestión Basado en Retardo

En lugar de esperar pérdidas (que implican daño ya hecho), algunos TCPs miden el **retardo**:

- `RTTmin`: RTT mínimo observado (camino sin congestión).
- Si el throughput medido se acerca al throughput sin congestión → el canal está bien, seguir aumentando.
- Si el throughput medido cae muy por debajo del teórico → hay congestión, reducir.

**BBR (Bottleneck Bandwidth and RTT):** Implementado en la red troncal de Google. No induce pérdidas deliberadamente; mantiene el canal "justo lleno, pero no más".

### ECN — Notificación Explícita de Congestión

Mecanismo asistido por la red:

1. Dos bits en la cabecera IP (campo ToS) marcados por routers congestionados.
2. El destino activa el bit **ECE** en el ACK TCP para notificar al emisor.
3. El emisor reacciona como si hubiera pérdida (reduce cwnd), pero sin que se haya perdido ningún paquete.

Beneficio: detecta congestión antes de que se pierdan paquetes.

### Equidad TCP

**Objetivo:** Si K sesiones TCP comparten un enlace de capacidad R, cada una debería recibir R/K en promedio.

TCP AIMD **converge a la equidad** bajo condiciones ideales (mismo RTT, número fijo de sesiones):
- El incremento aditivo lleva ambas conexiones hacia la línea de equidad (R1 = R2).
- La reducción multiplicativa las mantiene cerca de ella.

**Excepciones:**
- **UDP:** Las aplicaciones multimedia usan UDP y no reducen su tasa. Pueden "robar" ancho de banda de TCP.
- **Conexiones TCP paralelas:** Un browser puede abrir múltiples conexiones TCP al mismo servidor. Con 10 conexiones paralelas, obtiene 10× la cuota de una sola conexión TCP. Esto rompe la equidad.

---

## 11. Evolución: QUIC

### ¿Por qué QUIC?

TCP tiene limitaciones en escenarios modernos:
- Redes inalámbricas: TCP interpreta pérdida como congestión (pero puede ser ruido).
- Latencia del handshake: TCP necesita 1 RTT + TLS necesita 1-2 RTTs más = 2-3 RTTs antes de enviar datos.
- Bloqueo HOL (Head-of-Line): En HTTP/2, múltiples streams sobre un TCP. Si un segmento se pierde, **todos** los streams quedan bloqueados esperando.

### ¿Qué es QUIC?

**QUIC (Quick UDP Internet Connections)** es un protocolo de capa de **aplicación** que corre sobre UDP e implementa por sí mismo:
- Establecimiento de conexión.
- Control de errores y confiabilidad.
- Control de congestión.
- Seguridad (TLS 1.3 integrado).

**Usado por:** Google (Chrome, YouTube móvil), y es la base de HTTP/3.

### Ventajas de QUIC

**1. Establecimiento de conexión en 1 RTT:**
```
TCP + TLS:
  RTT 1: TCP SYN → SYN-ACK → ACK
  RTT 2: TLS hello → ...
  RTT 3: Datos

QUIC:
  RTT 1: QUIC handshake (incluye crypto) → Datos listos
```

**2. Múltiples streams sin bloqueo HOL:**
- Cada stream es independiente dentro de la misma conexión QUIC.
- Si un paquete de stream 1 se pierde, los streams 2 y 3 **no se bloquean**.
- En TCP+HTTP/2, todos los streams comparten el mismo flujo TCP, por lo que una pérdida bloquea todo.

**3. Migración de conexión:**
- QUIC usa un ID de conexión propio, no depende de la IP+puerto como TCP.
- Si cambias de WiFi a 4G, la conexión QUIC puede continuar sin interrupción.

### Stack de Protocolos

```
Antes (HTTP/2 sobre TCP):          Ahora (HTTP/3 sobre QUIC):
┌─────────────────────┐            ┌─────────────────────┐
│      HTTP/2         │            │      HTTP/3         │
├─────────────────────┤            ├─────────────────────┤
│        TLS          │            │   QUIC (confiab.,   │
├─────────────────────┤            │   cong., crypto)    │
│        TCP          │            ├─────────────────────┤
├─────────────────────┤            │        UDP          │
│         IP          │            ├─────────────────────┤
└─────────────────────┘            │         IP          │
                                   └─────────────────────┘
```

---

## 12. Resumen Rápido y Tabla Comparativa

### UDP vs TCP — Tabla Resumen

| Característica | UDP | TCP |
|----------------|-----|-----|
| Conexión | Sin conexión | Orientado a la conexión |
| Confiabilidad | No | Sí (retransmisiones) |
| Orden de entrega | No garantizado | Garantizado |
| Control de flujo | No | Sí (rwnd) |
| Control de congestión | No | Sí (cwnd, AIMD) |
| Overhead de cabecera | 8 bytes | 20 bytes mínimo |
| Velocidad | Alta | Menor |
| Establecimiento | Ninguno | 3-way handshake |
| Demultiplexación | Puerto destino solo | Cuádrupla completa |
| Usos típicos | DNS, streaming, juegos | HTTP, SSH, email |

### Protocolos rdt — Tabla Resumen

| Versión | Canal | Mecanismos nuevos | Limitación |
|---------|-------|-------------------|------------|
| rdt 1.0 | Perfecto | Ninguno | Canal real no es perfecto |
| rdt 2.0 | Errores de bits | ACK/NAK, checksum | ACK/NAK pueden corromperse |
| rdt 2.1 | Errores de bits | + Números de secuencia (0/1) | Solo stop-and-wait |
| rdt 2.2 | Errores de bits | + Sin NAK (ACK con seq#) | Solo stop-and-wait |
| rdt 3.0 | Errores + Pérdidas | + Timer/Timeout | Stop-and-wait ineficiente |
| Pipeline | Errores + Pérdidas | + Pipelining (GBN o SR) | — |

### GBN vs SR — Resumen

| | Go-Back-N | Repetición Selectiva |
|--|-----------|----------------------|
| ACKs | Acumulativos | Individuales |
| En pérdida | Retransmite pkt perdido + todos los siguientes | Solo retransmite pkt perdido |
| Buffer receptor | No necesita | Sí necesita |
| Restricción de ventana | N ≤ 2^k - 1 | N ≤ 2^(k-1) |

### Fórmulas Clave

| Concepto | Fórmula |
|----------|---------|
| Tiempo de transmisión | `Dtrans = L (bits) / R (bps)` |
| Utilización Stop-and-Wait | `U = (L/R) / (RTT + L/R)` |
| Utilización con Pipeline N pkts | `U ≈ N × (L/R) / (RTT + L/R)` |
| EstimatedRTT | `EstRTT = (1-α) × EstRTT + α × SampleRTT`, α=0.125 |
| DevRTT | `DevRTT = (1-β) × DevRTT + β × |SampleRTT - EstRTT|`, β=0.25 |
| TimeoutInterval | `TimeoutInterval = EstRTT + 4 × DevRTT` |
| Throughput TCP promedio | `Throughput ≈ (3/4) × W / RTT` |
| Datos en vuelo (emisor TCP) | `LastByteSent - LastByteAcked < min(cwnd, rwnd)` |

### Temas Frecuentes de Certamen

1. **Demultiplexación:** ¿UDP usa 2 datos (IP+puerto destino), TCP usa 4 (cuádrupla)? ¿Por qué importa?
2. **rdt 2.1 vs 2.2:** ¿Por qué se necesitan números de secuencia? ¿Por qué 1 bit basta en stop-and-wait?
3. **Dilema de SR:** Calcular el tamaño máximo de ventana dado el espacio de números de secuencia.
4. **Números de secuencia TCP:** Dado Seq y Len de varios segmentos, calcular los ACKs esperados.
5. **RTT y timeout:** Dado SampleRTT, calcular EstimatedRTT, DevRTT y TimeoutInterval.
6. **Three-way handshake:** Describir los 3 pasos, qué se acuerda en cada uno, por qué no basta con 2.
7. **Slow Start vs Congestion Avoidance:** Dibujar la evolución de cwnd dado un escenario de pérdidas.
8. **AIMD:** ¿Por qué el incremento es aditivo y la reducción es multiplicativa? ¿Qué implica para la equidad?
9. **rwnd vs cwnd:** Diferencia entre control de flujo y control de congestión.
10. **QUIC:** ¿Por qué sobre UDP? ¿Qué ventajas tiene respecto a TCP+TLS?

---

*Basado en: Computer Networking: A Top-Down Approach, 8ª edición — Jim Kurose, Keith Ross, Pearson 2020.*
