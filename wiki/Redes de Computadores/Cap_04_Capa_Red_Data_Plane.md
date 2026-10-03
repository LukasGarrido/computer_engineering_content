# Capítulo 4: Capa de Red — Data Plane (Plano de Datos)

### Computer Networking: A Top-Down Approach — Kurose & Ross, 8ª ed.

> Guía completa de estudio para certamen

---

## Índice

1. [Visión General de la Capa de Red](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#1-visi%C3%B3n-general-de-la-capa-de-red)
2. [Interior de un Router](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#2-interior-de-un-router)
3. [Gestión de Buffers y Planificación](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#3-gesti%C3%B3n-de-buffers-y-planificaci%C3%B3n)
4. [Protocolo IP: Formato del Datagrama](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#4-protocolo-ip-formato-del-datagrama)
5. [Direccionamiento IP](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#5-direccionamiento-ip)
6. [DHCP: Configuración Dinámica de Host](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#6-dhcp-configuraci%C3%B3n-din%C3%A1mica-de-host)
7. [NAT: Traducción de Direcciones de Red](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#7-nat-traducci%C3%B3n-de-direcciones-de-red)
8. [IPv6](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#8-ipv6)
9. [Reenvío Generalizado y SDN](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#9-reenv%C3%ADo-generalizado-y-sdn)
10. [OpenFlow: Match + Action en Acción](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#10-openflow-match--action-en-acci%C3%B3n)
11. [Middleboxes y Principios Arquitectónicos](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#11-middleboxes-y-principios-arquitect%C3%B3nicos)
12. [Resumen Rápido y Tablas de Referencia](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#12-resumen-r%C3%A1pido-y-tablas-de-referencia)

---

## 1. Visión General de la Capa de Red

### ¿Qué hace la capa de red?

La capa de red transporta **segmentos** de la capa de transporte desde el host emisor hasta el host receptor. A diferencia de la capa de transporte (proceso a proceso), la capa de red trabaja **host a host**.

- **Emisor:** Encapsula segmentos de transporte en **datagramas** y los pasa a la capa de enlace.
- **Receptor:** Entrega los segmentos al protocolo de capa de transporte correspondiente.
- **Routers:** Examinan los campos de cabecera de **todos** los datagramas IP que pasan y los mueven de puertos de entrada a puertos de salida.

### Las Dos Funciones Clave

|Función|Descripción|Analogía del viaje|
|---|---|---|
|**Forwarding (Reenvío)**|Mover un paquete del puerto de entrada de un router al puerto de salida correcto. Acción **local**, ocurre en **nanosegundos** (hardware).|Pasar por una sola intersección o peaje|
|**Routing (Enrutamiento)**|Determinar la ruta completa que siguen los paquetes desde el origen hasta el destino. Lógica de **toda la red**, ocurre en **milisegundos** (software).|Planificar todo el viaje en el mapa|

### Plano de Datos vs. Plano de Control

||Plano de Datos|Plano de Control|
|---|---|---|
|**Alcance**|Local, per-router|Toda la red (network-wide)|
|**Función**|¿A qué puerto de salida reenvío este datagrama?|¿Qué ruta sigue el datagrama de extremo a extremo?|
|**Velocidad**|Nanosegundos (hardware)|Milisegundos (software)|
|**Implementación**|Tablas de reenvío en el router|Algoritmos de enrutamiento (OSPF, BGP) o SDN|

**Dos enfoques para el plano de control:**

1. **Algoritmos de enrutamiento tradicionales:** Implementados en cada router. Los routers se comunican entre sí para construir las tablas de reenvío.
2. **SDN (Software-Defined Networking):** Un controlador remoto centralizado calcula e instala las tablas de reenvío en todos los routers.

### Modelo de Servicio de Internet: Best-Effort

Internet usa un modelo de servicio de **"mejor esfuerzo"** (best-effort). No ofrece garantías sobre:

- Entrega exitosa de datagramas al destino.
- Momento u orden de la entrega.
- Ancho de banda disponible para el flujo.

**¿Por qué este modelo tan simple tiene éxito?**

- La simplicidad permitió la adopción masiva de Internet.
- El aprovisionamiento suficiente de ancho de banda hace que el rendimiento sea "suficientemente bueno".
- Los servicios distribuidos (CDNs, datacenters) compensan la falta de garantías de red.
- El control de congestión de TCP actúa como mecanismo de compensación.

> **Para el certamen:** Comparar con ATM CBR (Constant Bit Rate, garantiza ancho de banda, orden y timing), ATM ABR (ancho de banda mínimo garantizado) e IntServ/DiffServ (QoS en IP). Internet elige simplicidad sobre garantías.

---

## 2. Interior de un Router

### Arquitectura General

Un router tiene cuatro componentes principales:

```
┌─────────────────────────────────────────────────────────┐
│           Procesador de Enrutamiento                    │
│      (plano de control — software, ms)                  │
├──────────────┬───────────────────────┬──────────────────┤
│              │   Switching Fabric    │                  │
│  Puertos de  │   (plano de datos —   │  Puertos de      │
│  Entrada     │   hardware, ns)       │  Salida          │
│              │                       │                  │
└──────────────┴───────────────────────┴──────────────────┘
```

El **procesador de enrutamiento** maneja el plano de control (ms). El **switching fabric** y los puertos operan en el plano de datos (ns).

---

### Puertos de Entrada

Cada puerto de entrada realiza tres funciones en cadena:

```
Terminación → Protocolo de → Lookup/Forwarding → Switching
de línea       capa de        (coincidencia       Fabric
(física)       enlace         + acción)
```

1. **Terminación de línea (física):** Recepción a nivel de bits.
2. **Protocolo de capa de enlace:** Por ejemplo, Ethernet.
3. **Lookup y forwarding (la parte importante):**
    - Usando el valor del campo de cabecera (IP destino), busca el puerto de salida en la **tabla de reenvío** almacenada en la memoria del puerto de entrada.
    - **Objetivo:** Completar el procesamiento del puerto de entrada a "line speed" (a la misma velocidad que llegan los datos).
    - Si los datagramas llegan más rápido de lo que el switching fabric puede procesarlos → se forman colas.

**Dos tipos de reenvío:**

- **Reenvío basado en destino (tradicional):** Solo usa la dirección IP de destino para decidir.
- **Reenvío generalizado:** Usa cualquier combinación de campos de cabecera (SDN/OpenFlow).

---

### Longest Prefix Matching (Coincidencia del Prefijo Más Largo)

Este es el algoritmo fundamental de forwarding basado en destino.

**Regla:** Al buscar en la tabla de reenvío la entrada para una dirección destino dada, usar el **prefijo de dirección más largo** que coincida.

**Ejemplo de tabla de reenvío:**

|Prefijo destino|Interfaz|
|---|---|
|`11001000 00010111 00010*** ********`|0|
|`11001000 00010111 00011000 ********`|1|
|`11001000 00010111 00011*** ********`|2|
|(cualquier otro)|3|

**Ejemplos:**

- `11001000 00010111 00010110 10100001` → coincide con prefijo de interfaz **0** (prefijo más específico: 21 bits).
- `11001000 00010111 00011000 10101010` → coincide tanto con interfaz 1 (32 bits exactos) como con interfaz 2 (21 bits). Se usa interfaz **1** porque tiene el prefijo más largo (más específico).

**¿Por qué el prefijo más largo?** Permite la agregación de rutas (CIDR): un ISP puede anunciar un bloque grande (`/20`), y sus clientes pueden tener rutas más específicas (`/23`) que sobreescriben la ruta general para esas direcciones.

**Implementación con TCAMs:**

- Las tablas de reenvío se implementan en **TCAM (Ternary Content Addressable Memory)**.
- Permiten presentar una dirección y recuperar el resultado en **un solo ciclo de reloj**, independientemente del tamaño de la tabla.
- Cisco Catalyst: ~1 millón de entradas en TCAM.

---

### Switching Fabric (Tejido de Conmutación)

Transfiere el paquete desde el buffer del puerto de entrada al buffer del puerto de salida correcto.

**Tasa de conmutación:** A qué velocidad se pueden transferir paquetes de entradas a salidas. Con N puertos, se desea una tasa N veces la velocidad de línea para evitar cuellos de botella.

**Tres tipos principales:**

#### 1. Conmutación via Memoria

- Los primeros routers (computadoras tradicionales).
- El paquete se copia a la memoria del sistema (RAM).
- La CPU decide el puerto de salida y copia el paquete.
- **Limitación:** Velocidad limitada por el ancho de banda de memoria. Cada datagrama cruza el bus del sistema **dos veces** (una al leer, una al escribir).

```
Puerto    →    Memoria    →    Puerto
entrada        del sistema     salida
         bus           bus
```

#### 2. Conmutación via Bus

- El datagrama se transfiere directamente de la memoria del puerto de entrada a la memoria del puerto de salida a través de un **bus compartido**.
- **Limitación:** Solo un paquete puede usar el bus a la vez. Velocidad limitada por el ancho de banda del bus (~32 Gbps en Cisco 5600).
- Suficiente para routers de acceso (home, SOHO).

#### 3. Conmutación via Red de Interconexión (Crossbar/Clos)

- Usa una red de interconexión (crossbar, Clos) que permite **transferencias paralelas** simultáneas entre múltiples pares de puertos de entrada/salida.
- Elimina la contención del bus: múltiples paquetes pueden transferirse en paralelo.
- **Escalado:** Usa múltiples "planos" de conmutación en paralelo.
- Cisco CRS: hasta cientos de **Tbps** de capacidad con 8 planos de conmutación, cada uno con una red de interconexión de 3 etapas.

|Tipo|Limitación principal|Velocidad típica|
|---|---|---|
|Memoria|Ancho de banda RAM, 2 cruces de bus|~1 Gbps|
|Bus|Ancho de banda del bus compartido|~32 Gbps|
|Interconexión (crossbar)|Escalable, paralelo|Cientos de Tbps|

---

### Bloqueo HOL (Head-of-Line Blocking)

**Problema:** Si la switching fabric es más lenta que la suma de los puertos de entrada, se forman colas en los puertos de entrada. El **bloqueo HOL** ocurre cuando:

- Un datagrama en la **cabeza** de la cola de entrada necesita ir a un puerto de salida **ocupado**.
- Bloquea a todos los datagramas **detrás** de él en la misma cola de entrada, aunque esos datagramas podrían ir a puertos de salida libres.

```
Puerto entrada 1: [paquete rojo (→salida 1)] [paquete verde (→salida 2)]
Puerto entrada 2: [paquete rojo (→salida 1)]   ← contención en salida 1

Solo un paquete rojo puede transferirse. El verde queda bloqueado
aunque la salida 2 esté libre. ← Esto es HOL blocking
```

---

## 3. Gestión de Buffers y Planificación

### Colas en Puertos de Salida

Los buffers de salida son necesarios cuando los datagramas llegan del switching fabric **más rápido** de lo que el enlace puede transmitirlos.

- Si el buffer se llena → los datagramas se **pierden** (congestión).
- La disciplina de planificación decide **qué paquete enviar a continuación**.

### ¿Cuánta Capacidad de Buffer?

**Regla empírica RFC 3439:**

```
Buffer = RTT × C
```

Ejemplo: enlace de 10 Gbps con RTT típico de 250 ms → buffer de 2.5 Gbit.

**Recomendación más reciente** (con N flujos TCP):

```
Buffer = (RTT × C) / √N
```

**Problema del exceso de buffer (bufferbloat):**

- Demasiado buffer → grandes retardos.
- Perjudica aplicaciones en tiempo real (VoIP, videoconferencia).
- Respuesta TCP lenta ante congestión (el control de congestión tarda en detectarla).
- Principio: "mantener el enlace de cuello de botella justo lleno, pero no más lleno".

---

### Políticas de Descarte (Drop Policies)

Cuando el buffer está lleno, se debe decidir qué paquete descartar:

- **Tail drop (descarte al final):** Se descarta el paquete recién llegado. Política más simple.
- **Priority drop:** Se descarta el paquete de menor prioridad.
- **RED (Random Early Detection) / ECN:** Marca o descarta paquetes aleatoriamente cuando el buffer empieza a llenarse, señalando congestión a TCP antes de que se desborde.

---

### Políticas de Planificación (Packet Scheduling)

#### FCFS / FIFO (First Come, First Served)

- Los paquetes se transmiten en el **orden de llegada**.
- Simple, sin diferenciación de tráfico.
- Ningún flujo recibe tratamiento especial.

```
Llegada: [1] [2] [3] [4]
Salida:  [1] [2] [3] [4]
```

#### Priority Scheduling (Prioridad)

- El tráfico se clasifica en **clases de prioridad** (alta, baja).
- Siempre se sirve primero la cola de **mayor prioridad** que tenga paquetes.
- Dentro de cada clase: FCFS.
- **Problema:** La cola de baja prioridad puede quedarse sin servicio si la de alta prioridad nunca se vacía (starvation).

```
Cola alta prioridad: [1H] [3H]
Cola baja prioridad: [2L] [4L]
Salida: [1H] [3H] [2L] [4L]
```

#### Round Robin (RR)

- El tráfico se clasifica en clases.
- El planificador escanea cíclicamente las colas y envía **un paquete completo** de cada clase disponible por turno.
- Equitativo: cada clase recibe la misma fracción del ancho de banda (si tienen la misma cantidad de paquetes).

```
Cola clase 1: [1] [3]     Salida: [1] [2] [3] [4]
Cola clase 2: [2] [4]
```

#### WFQ (Weighted Fair Queueing)

- **Round Robin generalizado**: cada clase `i` tiene un peso `wᵢ`.
- En cada ciclo, la clase `i` recibe una fracción `wᵢ / Σwⱼ` del ancho de banda.
- **Garantía de ancho de banda mínimo por clase de tráfico.**
- Más flexible que RR: permite priorizar sin starvar a las clases bajas.

```
Clase 1 (w=3): [A] [B]     → recibe 3/5 del ancho de banda
Clase 2 (w=2): [C] [D]     → recibe 2/5 del ancho de banda
```

> **Para el certamen:** WFQ garantiza un mínimo de ancho de banda por clase. Priority puede generar starvation. Round Robin es equitativo pero no diferencia. FIFO es el más simple. Neutralidad de red: los ISPs deberían (idealmente) tratar todo el tráfico igual → FIFO/WFQ favorecidos.

---

## 4. Protocolo IP: Formato del Datagrama

### Estructura del Datagrama IPv4

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Versión| HLen  | Tipo Servicio |       Longitud Total          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identificador 16 bits |Flags|   Desplazamiento Frag.  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     TTL       |   Protocolo   |     Checksum de Cabecera      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Dirección IP Origen                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Dirección IP Destino                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Opciones (variable)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Datos (payload)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Descripción de Campos Clave

|Campo|Tamaño|Descripción|
|---|---|---|
|**Versión**|4 bits|IPv4 = 4|
|**HLen**|4 bits|Longitud de la cabecera en palabras de 32 bits. Mín. = 5 (20 bytes sin opciones)|
|**Tipo de Servicio (ToS)**|8 bits|Bits DiffServ (0:5) + bits ECN (6:7) para control de congestión|
|**Longitud Total**|16 bits|Longitud total del datagrama (cabecera + datos) en bytes. Máx: 65,535 bytes. Típico: ≤1500 bytes|
|**Identificador**|16 bits|Identifica fragmentos del mismo datagrama original|
|**Flags**|3 bits|Bit "More Fragments" (MF) y bit "Don't Fragment" (DF)|
|**Desplazamiento de Fragmento**|13 bits|Posición de este fragmento en el datagrama original (en unidades de 8 bytes)|
|**TTL (Time To Live)**|8 bits|Decrementado en 1 por cada router. Si llega a 0, el datagrama se descarta (evita loops infinitos)|
|**Protocolo**|8 bits|Protocolo de capa superior: 6=TCP, 17=UDP, 1=ICMP|
|**Checksum de Cabecera**|16 bits|Verificación de integridad de la cabecera (solo cabecera, no datos)|
|**IP Origen**|32 bits|Dirección IP del host emisor|
|**IP Destino**|32 bits|Dirección IP del host receptor|
|**Opciones**|Variable|Timestamp, record route, etc. Raramente usados|
|**Datos**|Variable|Segmento TCP o UDP (u otro protocolo)|

**Overhead mínimo TCP+IP:**

- Cabecera IP: 20 bytes
- Cabecera TCP: 20 bytes
- Total: **40 bytes** + overhead de capa de aplicación

### Fragmentación y Reensamblaje

Los enlaces de red tienen un **MTU (Maximum Transfer Unit)**: el tamaño máximo de trama a nivel de enlace. Tipos de enlace diferentes tienen MTUs diferentes (Ethernet: 1500 bytes típicamente).

Si un datagrama IP es más grande que el MTU del enlace:

- El router **fragmenta** el datagrama en varios datagramas más pequeños.
- El reensamblaje ocurre **solo en el destino final** (no en los routers intermedios).
- Los bits del identificador, flags y desplazamiento de fragmento permiten reensamblar.

**Ejemplo de fragmentación:**

- Datagrama original: 4000 bytes, MTU = 1500 bytes.
- Cabecera IP: 20 bytes → máximo 1480 bytes de datos por fragmento.

|Fragmento|Length|ID|MF|Offset|
|---|---|---|---|---|
|1|1500|x|1|0|
|2|1500|x|1|185 (=1480/8)|
|3|1040|x|0|370 (=2960/8)|

El último fragmento tiene MF=0 (no hay más fragmentos) y el offset indica su posición.

> **Para el certamen:** IPv6 elimina la fragmentación en routers (solo en los extremos). Esto acelera el procesamiento en routers. Si un paquete IPv6 es muy grande, el router envía un mensaje ICMP "Packet Too Big" al origen.

---

## 5. Direccionamiento IP

### ¿Qué es una Dirección IP?

- Identificador de **32 bits** asociado a cada **interfaz** de host o router (no al dispositivo en sí).
- Notación decimal punteada: cada byte en decimal, separado por puntos.
    - Ejemplo: `223.1.1.1 = 11011111 00000001 00000001 00000001`
- Los routers típicamente tienen **múltiples interfaces** (una por enlace conectado) y por tanto múltiples IPs.
- Los hosts típicamente tienen una o dos interfaces.

### Subredes (Subnets)

Una **subred** es un conjunto de interfaces de dispositivos que pueden comunicarse físicamente entre sí **sin pasar por un router**.

Las direcciones IP tienen estructura:

- **Parte de subred (red):** Los bits de orden alto, comunes a todos los dispositivos de la misma subred.
- **Parte de host:** Los bits de orden bajo, identifica el dispositivo específico dentro de la subred.

**Cómo identificar subredes:** "Desconectar" cada interfaz de su host/router. Las "islas" de red aisladas resultantes son cada una una subred.

### CIDR: Classless InterDomain Routing

**CIDR** (se pronuncia "cider") permite prefijos de subred de **longitud arbitraria**.

**Formato:** `a.b.c.d/x`

Donde `/x` indica que los primeros `x` bits son la parte de red (subred) y los restantes `32-x` bits son la parte de host.

**Ejemplo:** `200.23.16.0/23`

- 23 bits de subred, 9 bits de host.
- Hosts válidos: `200.23.16.1` a `200.23.17.254` (2⁹ - 2 = 510 hosts).

**Ventaja clave: Agregación de rutas.** Un ISP con bloque `/20` puede anunciar una sola ruta que cubre 8 organizaciones con bloques `/23`. Los routers de Internet solo necesitan una entrada en su tabla para todo el bloque.

```
ISP: 200.23.16.0/20  →  anunciar una sola ruta en Internet
     ├── Org0: 200.23.16.0/23
     ├── Org1: 200.23.18.0/23
     ├── ...
     └── Org7: 200.23.30.0/23
```

Si Org1 cambia de ISP, el nuevo ISP anuncia una ruta **más específica** (`200.23.18.0/23`). Por el principio de longest prefix matching, esa ruta más específica tiene prioridad sobre la ruta agregada.

### Espacios de Direcciones Privadas

Rangos reservados para redes privadas (no enrutables en Internet público):

- `10.0.0.0/8` — Clase A privada (16,777,216 hosts)
- `172.16.0.0/12` — Clase B privada (1,048,576 hosts)
- `192.168.0.0/16` — Clase C privada (65,536 hosts)

Estos rangos se usan en redes domésticas, empresariales y redes celulares junto con NAT.

### Jerarquía de Asignación

```
ICANN (raíz)
    ↓
RR (Registros Regionales: ARIN, RIPE, LACNIC, APNIC, AFRINIC)
    ↓
ISPs
    ↓
Organizaciones / Usuarios
```

ICANN asignó el último bloque de IPv4 a los RR en **2011**. El espacio de IPv4 está agotado.

---

## 6. DHCP: Configuración Dinámica de Host

### ¿Qué es DHCP?

**DHCP (Dynamic Host Configuration Protocol)** permite que un host obtenga automáticamente su dirección IP (y otros parámetros de red) de un servidor cuando se conecta a la red. Es "plug-and-play".

**Ventajas:**

- No requiere configuración manual.
- Permite reutilización de direcciones (solo ocupa IP mientras está conectado).
- Soporte natural para usuarios móviles (laptop, smartphone).

### Proceso DHCP: 4 Mensajes

Todo ocurre via **UDP broadcast** (excepto el ACK final que puede ser unicast):

```
Cliente                                        Servidor DHCP
   │                                                │
   │  DHCP DISCOVER (src: 0.0.0.0:68,             │
   │  dst: 255.255.255.255:67)                     │
   │  "¿Hay algún servidor DHCP?"                 │
   │ ─────────────────────────────────────────── ►│
   │                                                │
   │  DHCP OFFER (src: IP_servidor:67,             │
   │  dst: 255.255.255.255:68)                     │
   │  "Yo soy servidor, ofrezco IP: 223.1.2.4"    │
   │ ◄─────────────────────────────────────────── │
   │                                                │
   │  DHCP REQUEST (broadcast)                     │
   │  "Quiero usar la IP 223.1.2.4"               │
   │ ─────────────────────────────────────────── ►│
   │                                                │
   │  DHCP ACK (broadcast o unicast)               │
   │  "Confirmado, IP: 223.1.2.4, lease: 3600s"   │
   │ ◄─────────────────────────────────────────── │
   │                                                │
```

**¿Por qué broadcast en DISCOVER?** El cliente no sabe la IP del servidor DHCP. Usa `0.0.0.0` como IP origen (aún no tiene IP) y `255.255.255.255` como broadcast.

### ¿Qué devuelve DHCP?

DHCP puede devolver más que la dirección IP:

- **IP asignada** al cliente (con tiempo de lease).
- **IP del router de primer salto** (default gateway).
- **Nombre e IP del servidor DNS**.
- **Máscara de red** (para saber la parte de subred vs. host).

**Ubicación típica del servidor DHCP:** Integrado en el router, sirviendo a todas las subredes conectadas a él.

**Proceso completo de encapsulación:** `DHCP message → UDP → IP → Ethernet → (broadcast en LAN) → router DHCP`

> **Para el certamen:** DHCP usa UDP (no TCP) porque en el DISCOVER el cliente no tiene IP y no puede establecer una conexión TCP. El broadcast evita conocer la IP del servidor de antemano.

---

## 7. NAT: Traducción de Direcciones de Red

### El Problema que Resuelve

Con el agotamiento de IPs IPv4, las redes domésticas e institucionales no pueden tener una IP pública por cada dispositivo. NAT permite que **todos los dispositivos de una red local compartan una única IP pública**.

### Cómo Funciona NAT

Todos los datagramas que salen de la red local tienen la **misma IP pública** como origen, pero **diferentes números de puerto** de origen. El router NAT mantiene una tabla de traducción.

```
Red local (privada 10.0.0/24)            Internet
10.0.0.1 (puerto 3345) ────────────────► (138.76.29.7, puerto 5001) ──► Servidor
10.0.0.2 (puerto 7654) ────────────────► (138.76.29.7, puerto 5002) ──► Servidor
10.0.0.3 (puerto 1234) ────────────────► (138.76.29.7, puerto 5003) ──► Servidor
```

**Tabla NAT del router:**

|WAN side (IP pública : puerto)|LAN side (IP privada : puerto)|
|---|---|
|138.76.29.7 : 5001|10.0.0.1 : 3345|
|138.76.29.7 : 5002|10.0.0.2 : 7654|
|...|...|

### Proceso Detallado

**Datagrama saliente:**

1. Host `10.0.0.1:3345` envía paquete a `128.119.40.186:80`.
2. El router NAT reemplaza origen `10.0.0.1:3345` por `138.76.29.7:5001`.
3. Guarda la traducción en la tabla NAT.
4. Envía el paquete a Internet.

**Datagrama entrante:**

1. Llega paquete con destino `138.76.29.7:5001`.
2. El router NAT busca en la tabla: `5001 → 10.0.0.1:3345`.
3. Reemplaza destino `138.76.29.7:5001` por `10.0.0.1:3345`.
4. Entrega a la red local.

### Ventajas de NAT

- Solo se necesita **una IP pública** del ISP para toda la red local.
- Se pueden cambiar IPs internas sin notificar al exterior.
- Se puede cambiar de ISP sin cambiar las IPs internas.
- **Seguridad implícita:** Los dispositivos internos no son directamente accesibles desde Internet.

### Controversias de NAT

NAT es controversial por varias razones técnicas:

1. **Viola el modelo de capas:** Los routers "deberían" procesar solo hasta capa 3 (IP). NAT manipula números de puerto (capa 4). Viola la abstracción de capas.
    
2. **Viola el argumento end-to-end:** La inteligencia debería estar en los extremos. NAT introduce estado e inteligencia en la red.
    
3. **El problema de la "escasez" debería resolverse con IPv6**, no con hacks como NAT.
    
4. **NAT traversal:** Si un servidor está **detrás de NAT**, los clientes externos no pueden inicicar conexiones directamente (porque el servidor no tiene IP pública directamente accesible). Se necesitan técnicas especiales (STUN, TURN, UPnP, hole punching).
    

**Pero NAT llegó para quedarse:** Se usa extensivamente en redes domésticas, institucionales y redes celulares 4G/5G.

---

## 8. IPv6

### Motivación para IPv6

1. **Agotamiento de IPv4:** El espacio de 32 bits (4,294,967,296 direcciones) es insuficiente. ICANN agotó el último bloque en 2011.
2. **Procesamiento más rápido:** Cabecera de **longitud fija de 40 bytes** (vs. variable en IPv4). Los routers no tienen que calcular la longitud de la cabecera.
3. **Nuevas funcionalidades:** Etiquetas de flujo (flow labels), mejor soporte para QoS.

### Formato del Datagrama IPv6

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Versión| Prioridad |               Flow Label                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Payload Length        | Next Header   |  Hop Limit   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                    Dirección IPv6 Origen                      |
|                         (128 bits)                            |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                   Dirección IPv6 Destino                      |
|                         (128 bits)                            |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Datos (payload)                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Campos clave:**

- **Versión:** 6
- **Prioridad (Priority):** Identifica la prioridad entre datagramas del mismo flujo.
- **Flow Label:** Identifica datagramas del mismo "flujo" para tratamiento especial.
- **Payload Length:** Longitud del payload (sin la cabecera de 40 bytes).
- **Next Header:** Protocolo de capa superior (TCP=6, UDP=17) o cabecera de extensión.
- **Hop Limit:** Equivalente al TTL de IPv4.
- **Direcciones:** 128 bits (vs. 32 de IPv4) — espacio prácticamente ilimitado.

### ¿Qué Desaparece en IPv6 vs. IPv4?

|Campo eliminado|Razón|
|---|---|
|**Checksum de cabecera**|Acelera el procesamiento en routers. Las capas de enlace y transporte ya tienen checksums.|
|**Fragmentación/reensamblaje**|Los routers no fragmentan. Si el paquete es muy grande, el router envía ICMP "Packet Too Big". Solo los extremos fragmentan.|
|**Opciones**|Disponibles como protocolos de "next header", pero no en la cabecera base.|

### Transición de IPv4 a IPv6: Tunneling

No es posible actualizar todos los routers de Internet simultáneamente. La solución es el **tunneling**: transportar datagramas IPv6 como payload dentro de datagramas IPv4.

```
Nodos IPv6 ── [Router IPv6/v4] ── IPv4 tunnel ── [Router IPv6/v4] ── Nodos IPv6
     A             B                  C/D                E                F
```

- Entre B y E hay una "nube" IPv4 que no soporta IPv6.
- B encapsula el datagrama IPv6 de A dentro de un datagrama IPv4 (src=B, dst=E).
- C y D lo reenvían como cualquier datagrama IPv4 normal (no saben que adentro hay IPv6).
- E desencapsula y extrae el datagrama IPv6, lo entrega a F.

**Analogía:** El datagrama IPv6 va dentro del IPv4 como una "carga útil" ("paquete dentro de un paquete").

### Adopción de IPv6

- Google: ~30% de los clientes acceden via IPv6.
- NIST: 1/3 de los dominios del gobierno de EE.UU. son compatibles con IPv6.
- 25+ años de despliegue y aún no es universal.

¿Por qué tan lento? La transición requiere actualizar miles de millones de dispositivos, y NAT ha paliado el agotamiento de IPv4, reduciendo la urgencia.

---

## 9. Reenvío Generalizado y SDN

### Limitación del Reenvío Tradicional

El reenvío basado en destino (IP destino → puerto de salida) es poderoso pero limitado. Solo puede tomar decisiones basadas en la dirección IP de destino.

### Reenvío Generalizado: Match + Action

**Idea central:** Extender el concepto de reenvío para que pueda hacer **coincidencias** (match) sobre **cualquier campo** de la cabecera (capa 2, 3, y 4) y tomar **cualquier acción**.

**Tabla de flujo (flow table):** Cada entrada tiene:

- **Match (coincidencia):** Valores de patrón en campos de cabecera. Soporta wildcards (`*`).
- **Action (acción):** Para el paquete que coincide: descartar, reenviar, modificar campos, enviar al controlador.
- **Priority (prioridad):** Desambigua patrones superpuestos.
- **Counters (contadores):** Número de bytes y paquetes que coincidieron.

**Ejemplo de tabla de flujo:**

```
src = *.*.*.*, dst = 3.4.*.*    → forward(puerto 2)
src = 1.2.*.*, dst = *.*.*.*    → drop
src = 10.1.2.3, dst = *.*.*.*   → send to controller
```

---

## 10. OpenFlow: Match + Action en Acción

### ¿Qué es OpenFlow?

OpenFlow es el protocolo estándar que implementa el reenvío generalizado. Define cómo un controlador SDN puede instalar reglas de match+action en los switches/routers.

### Campos de Coincidencia en OpenFlow

Una entrada de tabla de flujo OpenFlow puede hacer match sobre:

|Capa|Campos|
|---|---|
|**Enlace (L2)**|Puerto de ingreso, MAC origen, MAC destino, Tipo Ethernet, VLAN ID, VLAN Priority|
|**Red (L3)**|IP origen, IP destino, Protocolo IP, IP ToS|
|**Transporte (L4)**|Puerto TCP/UDP origen, Puerto TCP/UDP destino|

Esto unifica en una sola abstracción lo que antes requería dispositivos distintos.

### OpenFlow Unifica Diferentes Dispositivos

La misma abstracción match+action puede emular:

|Dispositivo|Match|Action|
|---|---|---|
|**Router**|Prefijo IP destino más largo|Reenviar por un enlace|
|**Switch L2**|Dirección MAC destino|Reenviar o broadcast|
|**Firewall**|IPs + puertos TCP/UDP|Permitir o denegar|
|**NAT**|IP + puerto|Reescribir IP y puerto|

### Ejemplo OpenFlow: Comportamiento en Toda la Red

Escenario: En una red con switches s1, s2, s3 y hosts h1-h6, se quiere que el tráfico de h5 y h6 (red 10.3.0.0) hacia h3 y h4 (red 10.2.0.0) pase primero por s1 y luego por s2.

El controlador SDN instala estas reglas en cada switch:

**En s3:**

```
match: IP src = 10.3.*.*, IP dst = 10.2.*.*  →  forward(puerto 3)
```

**En s1:**

```
match: puerto entrada=1, IP src=10.3.*.*, IP dst=10.2.*.*  →  forward(puerto 4)
```

**En s2:**

```
match: puerto entrada=2, IP dst=10.2.0.3  →  forward(puerto 3)
match: puerto entrada=2, IP dst=10.2.0.4  →  forward(puerto 4)
```

Con reglas coordinadas por el controlador, se puede "programar" el comportamiento de toda la red.

---

## 11. Middleboxes y Principios Arquitectónicos

### ¿Qué son los Middleboxes?

**Definición (RFC 3234):** "Cualquier dispositivo intermediario que realiza funciones distintas a las funciones normales y estándar de un router IP en el camino de datos entre un host origen y un host destino."

**Ejemplos:**

- **NAT:** Traducción de direcciones.
- **Firewalls:** Filtrado de paquetes según reglas de seguridad.
- **IDS (Intrusion Detection System):** Detección de intrusiones.
- **Load Balancers:** Distribución de carga entre servidores.
- **Caches:** Almacenamiento en caché de contenido (CDN).
- **Application-specific devices:** Procesamiento específico de aplicación.

### Evolución de los Middleboxes

**Antes:** Soluciones de hardware propietario (cerrado). Cada función requería un dispositivo especial.

**Tendencia actual:**

- **Whitebox hardware:** Hardware genérico (commodity) con APIs abiertas.
- **NFV (Network Functions Virtualization):** Los middleboxes se implementan como software sobre hardware genérico. Más flexible, más barato.
- **SDN:** Control centralizado (lógicamente) de los middleboxes.
- **Cloud deployment:** Funciones de red implementadas en la nube pública/privada.

### El "Hourglass" IP (La Cintura de Reloj de Arena)

```
        HTTP  SMTP  RTP  QUIC  DASH  ...
              TCP      UDP
                  IP          ← la "cintura" estrecha
         Ethernet   PPP   WiFi  ...
           copper  radio  fiber  ...
```

**IP es la "cintura estrecha" de Internet:**

- Hay muchos protocolos encima (TCP, UDP, HTTP, etc.) y debajo (Ethernet, WiFi, fibra, etc.).
- Todos deben pasar por IP.
- IP es el único protocolo que **debe** implementar cada dispositivo conectado a Internet.

**Con los middleboxes modernos:** La cintura se ha ensanchado con firewalls, NAT, caches que operan dentro de la red. Algunos lo llaman los "love handles" (michelines) del hourglass.

### El Argumento End-to-End (Extremo a Extremo)

**Formulado por Saltzer, Reed y Clark (1981):**

> "La función en cuestión solo puede implementarse de forma completa y correcta con el conocimiento y la ayuda de la aplicación ubicada en los extremos del sistema de comunicación. Por tanto, no es posible proporcionar dicha función como característica del propio sistema de comunicación."

**Ejemplo:** Transferencia de datos confiable.

- ¿Puede la red garantizar entrega confiable? Podría hacerlo hop-by-hop.
- Pero incluso si cada enlace es confiable, el host receptor podría fallar antes de procesar los datos. La fiabilidad end-to-end **requiere** intervención del extremo.
- La red puede ayudar como **optimización de rendimiento**, pero no puede reemplazar la implementación en los extremos.

**Implicación para el diseño de Internet:**

- La complejidad y la inteligencia van en los **extremos** (hosts).
- La red en el medio (routers) es simple: solo reenvía paquetes.
- Los protocolos de transporte (TCP) y aplicación implementan fiabilidad, control de congestión, etc.

**Tres principios fundamentales de Internet (RFC 1958):**

1. **Simple conectividad:** La red se encarga solo de mover paquetes.
2. **Protocolo IP como cintura estrecha:** Un único protocolo de red.
3. **Inteligencia en el borde:** Los extremos (hosts, aplicaciones) manejan la complejidad.

**Evolución histórica:**

- **Teléfonos siglo XX:** Inteligencia en los switches de la red, terminales tontos.
- **Internet pre-2005:** Inteligencia en los extremos, red simple.
- **Internet post-2005:** Dispositivos de red programables + masiva infraestructura en los extremos.

---

## 12. Resumen Rápido y Tablas de Referencia

### Comparación IPv4 vs. IPv6

|Característica|IPv4|IPv6|
|---|---|---|
|Tamaño de dirección|32 bits|128 bits|
|Tamaño de cabecera|Variable (mín. 20 bytes)|Fija (40 bytes)|
|Checksum en cabecera|Sí|No|
|Fragmentación en routers|Sí|No (solo en extremos)|
|Opciones en cabecera|Sí|No (next-header extensions)|
|TTL|Sí|Hop Limit (equivalente)|
|Broadcast|Sí|No (usa multicast)|
|NAT|Necesario (por escasez)|No necesario|
|Transición|—|Tunneling sobre IPv4|

### Tipos de Switching Fabric

|Tipo|Mecanismo|Limitación|Velocidad|
|---|---|---|---|
|**Memoria**|CPU copia a RAM|Bandwidth de RAM|~1 Gbps|
|**Bus**|Bus compartido|Contención de bus|~32 Gbps|
|**Interconexión**|Crossbar paralelo|Escalable|>100 Tbps|

### Políticas de Planificación

|Política|Mecanismo|Garantía|Problema|
|---|---|---|---|
|**FIFO/FCFS**|Orden de llegada|Ninguna|Sin diferenciación|
|**Priority**|Clases con prioridades|Baja latencia para alta prioridad|Starvation de baja prioridad|
|**Round Robin**|Turnos por clase|Equidad (pesos iguales)|No diferencia peso|
|**WFQ**|Turnos ponderados|Ancho de banda mínimo por clase|Más complejo|

### Campos del Datagrama IP: Los Más Preguntados

|Campo|Función|Certamen|
|---|---|---|
|TTL|Evita loops infinitos, decrementado en cada router|¿Qué pasa si TTL=0? → descarta y envía ICMP|
|Protocolo|Identifica capa superior (TCP=6, UDP=17)|Usado en demultiplexación|
|Identificador + Flags + Offset|Fragmentación y reensamblaje|Calcular fragmentos dado MTU|
|ToS/DiffServ + ECN|Control de congestión y QoS|Bits ECN señalizan congestión|
|Checksum|Integridad de cabecera|IPv6 lo elimina para acelerar|

### Proceso DHCP Simplificado

```
Cliente                     Servidor
   │                             │
   │──── DISCOVER (broadcast) ──►│
   │◄─── OFFER ─────────────────│
   │──── REQUEST (broadcast) ───►│
   │◄─── ACK ───────────────────│
   │                             │
   └── Ya tiene: IP, gateway, DNS, máscara
```

### NAT: Operación Resumida

```
Saliente: (IP_privada:puerto_orig) → (IP_NAT:puerto_nuevo) + guardar en tabla
Entrante: (IP_NAT:puerto_nuevo) → (IP_privada:puerto_orig)  [consultar tabla]
```

### Temas Frecuentes de Certamen

1. **Forwarding vs. Routing:** Diferencia conceptual y temporal (ns vs. ms), local vs. red completa.
2. **Longest Prefix Matching:** Dado un destino y una tabla, identificar la interfaz correcta. ¿Por qué se necesita el prefijo más largo?
3. **Tipos de switching fabric:** Descripción, limitación y velocidad comparativa.
4. **HOL Blocking:** ¿Qué es? ¿Cuándo ocurre? ¿Cuál es el impacto?
5. **Fragmentación IP:** Dado un datagrama y MTU, calcular los fragmentos (length, ID, MF, offset).
6. **CIDR y subredes:** Dado `200.23.16.0/23`, calcular hosts disponibles, rango, máscara.
7. **DHCP:** Los 4 mensajes, por qué broadcast, qué información devuelve.
8. **NAT:** Ventajas, proceso de traducción, controversias (end-to-end, violación de capas).
9. **IPv6 vs. IPv4:** Qué se eliminó y por qué. Tunneling para transición.
10. **OpenFlow/Match+Action:** Cómo unifica router, switch, firewall y NAT en una sola abstracción.
11. **Argumento end-to-end:** ¿Qué significa? ¿Por qué la inteligencia va en los extremos?
12. **Best-effort vs. QoS:** ¿Por qué Internet eligió best-effort? ¿Cuáles son sus ventajas?

---

_Basado en: Computer Networking: A Top-Down Approach, 8ª edición — Jim Kurose, Keith Ross, Pearson 2020._