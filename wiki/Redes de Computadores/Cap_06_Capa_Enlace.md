# Capítulo 6: La Capa de Enlace y las Redes LAN
### *Computer Networking: A Top-Down Approach* (Kurose & Ross, 8ª ed.)

---
G7#pL2@vQ9x
## Tabla de Contenidos

1. [Introducción a la Capa de Enlace](#1-introducción-a-la-capa-de-enlace)
2. [Detección y Corrección de Errores](#2-detección-y-corrección-de-errores)
3. [Protocolos de Acceso Múltiple](#3-protocolos-de-acceso-múltiple)
4. [LANs: Direccionamiento y ARP](#4-lans-direccionamiento-y-arp)
5. [Ethernet](#5-ethernet)
6. [Switches (Conmutadores)](#6-switches-conmutadores)
7. [VLANs](#7-vlans-redes-de-área-local-virtuales)
8. [Virtualización de Enlace: MPLS](#8-virtualización-de-enlace-mpls)
9. [Redes de Centros de Datos (Datacenter Networks)](#9-redes-de-centros-de-datos)
10. [Un Día en la Vida de una Solicitud Web](#10-un-día-en-la-vida-de-una-solicitud-web)

---

## 1. Introducción a la Capa de Enlace

### ¿Qué es la capa de enlace?

La capa de enlace es la **Capa 2** del modelo OSI y se encarga de transferir datos entre dos nodos **físicamente adyacentes** (conectados directamente) a través de un enlace de comunicación.

### Terminología fundamental

| Término | Definición |
|--------|-----------|
| **Nodo** | Cualquier dispositivo conectado a la red: hosts, routers, switches |
| **Enlace (Link)** | El canal de comunicación que conecta nodos adyacentes. Puede ser cableado, inalámbrico o LAN |
| **Frame (Trama)** | El paquete de la capa 2. Encapsula el datagrama de capa 3 (IP) añadiéndole un encabezado y un pie de página |

> **Punto clave:** La capa de enlace es responsable de mover el datagrama de *un nodo* al *siguiente nodo físicamente adyacente* — no de extremo a extremo. Es un trabajo segmentado, enlace por enlace.

### Analogía del transporte

Imagina un viaje de Princeton a Lausana:

```
Princeton ──(Limo)──→ JFK ──(Avión)──→ Ginebra ──(Tren)──→ Lausana
```

- El **turista** = datagrama (lo que se transporta)
- Cada **medio de transporte** (limo, avión, tren) = protocolo de capa de enlace distinto
- Cada **segmento del viaje** = un enlace diferente
- El **agente de viajes** = algoritmo de enrutamiento (decide la ruta general)

Esto ilustra que un datagrama puede atravesar **múltiples tipos de enlace** en su camino (ej: WiFi → Ethernet → fibra óptica), y cada uno usa su propio protocolo de capa 2.

### Servicios que ofrece la capa de enlace

**1. Entramado (Framing) y acceso al enlace**
- Encapsula el datagrama en un *frame* añadiéndole cabecera y cola
- Gestiona el acceso al canal si el medio es compartido
- Las direcciones **MAC** en los encabezados del frame identifican origen y destino (¡distintas a las IP!)

**2. Entrega confiable entre nodos adyacentes**
- Garantiza que el frame llegue sin errores al siguiente nodo
- Se usa poco en enlaces cableados (baja tasa de error)
- Es crítico en enlaces inalámbricos (alta tasa de error)
- Pregunta importante: *¿por qué tener fiabilidad tanto a nivel de enlace como a nivel de extremo a extremo (TCP)?* Porque la fiabilidad de enlace es local y más eficiente para reenvíos rápidos; TCP cubre la ruta completa

**3. Control de flujo**
- Regula la velocidad de envío entre el nodo emisor y el receptor adyacente para evitar desbordamiento de buffers

**4. Detección de errores**
- Los errores ocurren por atenuación de señal o ruido
- El receptor detecta el error y solicita retransmisión o descarta el frame

**5. Corrección de errores**
- El receptor no solo detecta el error, sino que lo **corrige** sin necesidad de retransmitir
- Requiere más bits redundantes que la mera detección

**6. Half-duplex y full-duplex**
- **Half-duplex**: los nodos en ambos extremos pueden transmitir, pero no al mismo tiempo (como una radio walkie-talkie)
- **Full-duplex**: transmisión simultánea en ambas direcciones

### ¿Dónde se implementa?

La capa de enlace se implementa en la **NIC** (Network Interface Card / Tarjeta de Interfaz de Red):
- Es un chip o tarjeta física (ej: tarjeta Ethernet, chip WiFi)
- Implementa tanto la capa de enlace como la capa física
- Se conecta al bus del sistema del host (ej: bus PCI)
- Es una combinación de hardware, software y firmware

**Funcionamiento:**
- **Lado emisor:** encapsula el datagrama en un frame, añade bits de detección de error, control de flujo, etc.
- **Lado receptor:** busca errores, extrae el datagrama y lo pasa a la capa superior (red/IP)

---

## 2. Detección y Corrección de Errores

### El problema

Cuando los bits viajan por un enlace (cable, aire, fibra), pueden sufrir alteraciones por ruido, interferencia o atenuación. El objetivo es detectar (y si es posible, corregir) estos errores.

### Esquema general EDC

```
[  D  |  EDC  ]  ──enlace con errores──→  [  D'  |  EDC'  ]
```

- **D** = datos originales protegidos (puede incluir campos del encabezado)
- **EDC** = bits redundantes de detección/corrección de errores
- En el destino se compara D' con EDC' para detectar si hubo errores
- **Importante:** La detección de errores NO es 100% confiable. Un campo EDC más grande mejora la detección, pero nunca la hace perfecta

### Técnica 1: Paridad

**Paridad simple (1 dimensión)**
- Se añade un bit extra tal que el número total de `1s` en el mensaje sea **par** (paridad par) o **impar** (paridad impar)
- Detecta **un solo bit** de error
- Si el error afecta a 2 bits, se cancela y no se detecta

Ejemplo con paridad par:
```
Datos:    0 1 1 1 0 0 0 1 1 0 1 0 1 0 1 1   → 9 unos (impar)
Con paridad: ...añadir un 1 al final → total 10 unos (par) ✓
```

**Paridad bidimensional (2D)**
- Organiza los bits en una matriz 2D
- Calcula paridad por filas Y por columnas
- Permite **detectar y corregir un único error de bit**
- El error queda ubicado en la intersección de la fila y columna con paridad incorrecta

### Técnica 2: Checksum de Internet (revisión)

Ya visto en capas superiores (UDP, TCP). Funciona así:

**Emisor:**
1. Trata el contenido del segmento como una secuencia de enteros de 16 bits
2. Suma todos los enteros usando **complemento a uno**
3. Coloca el resultado en el campo de checksum

**Receptor:**
1. Recalcula el checksum del segmento recibido
2. Compara con el campo de checksum
3. Si son distintos → error detectado; si son iguales → probablemente sin error (pero no garantizado)

> **Nota:** El checksum de Internet es una técnica de detección, no de corrección. Y tiene limitaciones: puede pasar por alto errores que se cancelen mutuamente.

### Técnica 3: CRC (Cyclic Redundancy Check)

Es la técnica más potente y es la usada en **Ethernet** y **WiFi 802.11**.

**Conceptos clave:**
- **D**: los datos a transmitir (tratados como un número binario)
- **G**: el generador, un patrón de bits de `r+1` bits (conocido tanto por emisor como receptor)
- **R**: los `r` bits CRC que se añaden a D

**¿Cómo funciona?**

El objetivo es elegir R tal que la cadena `<D, R>` sea **exactamente divisible por G** (aritmética módulo 2, sin acarreo):

```
R = resto de [ D · 2^r ÷ G ]
```

**Proceso de verificación:**
- El receptor divide `<D', R'>` entre G
- Si el resto es 0 → no hay error
- Si el resto es distinto de 0 → error detectado

**Ventajas del CRC:**
- Detecta **todos los errores en ráfaga** de menos de `r+1` bits
- Ampliamente usado en la práctica por su eficiencia en hardware

**Ejemplo simplificado:**
```
D = 101110  (datos)
G = 1001    (generador de 4 bits, r=3)
D·2³ = 101110000

División módulo 2 de 101110000 ÷ 1001 = ... resto R = 011

Transmitir: <D,R> = 101110 011
```

---

## 3. Protocolos de Acceso Múltiple

### El problema del medio compartido

Existen dos tipos fundamentales de enlace:

1. **Punto a punto:** un enlace dedicado entre dos dispositivos (ej: switch y host, PPP dial-up). No hay conflicto.
2. **Broadcast (difusión):** múltiples dispositivos comparten el mismo canal (ej: Ethernet antigua con cable coaxial, WiFi, 4G, satélite)

En los canales broadcast, si dos nodos transmiten simultáneamente, sus señales se mezclan → **colisión** → ninguno de los mensajes llega correctamente.

El **protocolo de acceso múltiple (MAC)** define las reglas para determinar *cuándo* puede transmitir cada nodo.

### Requisitos del protocolo MAC ideal

Para un canal de R bps con M nodos activos:
1. Un solo nodo activo puede usar todo el canal: **tasa R**
2. M nodos activos se reparten equitativamente: **tasa R/M cada uno**
3. Totalmente **descentralizado**: sin nodo coordinador especial, sin sincronización de relojes
4. **Simple** de implementar

### Categorías de protocolos MAC

Existen tres grandes familias:

---

#### 3.1 Partición de Canal

Dividen el canal en partes y asignan cada parte exclusivamente a un nodo.

**TDMA – Time Division Multiple Access (Acceso Múltiple por División de Tiempo)**
- El tiempo se divide en **rondas**; cada ronda se divide en **ranuras** de duración fija
- Cada estación tiene una ranura asignada en cada ronda
- Las ranuras no usadas quedan **inactivas** (desperdicio)

```
Ronda 1:  [Estación 1][Estación 2][Estación 3][Estación 4][Estación 5][Estación 6]
           ── usada ──── vacía ───── usada ──── usada ──── vacía ──── vacía ───
```

- **Ventaja:** Sin colisiones, acceso garantizado
- **Desventaja:** Ineficiente a baja carga; una estación no puede usar las ranuras de otra

**FDMA – Frequency Division Multiple Access (Acceso Múltiple por División de Frecuencia)**
- El espectro de frecuencia del canal se divide en **bandas**
- Cada estación tiene una banda asignada permanentemente
- Las bandas no usadas quedan **inactivas**
- Mismo principio que TDMA pero en frecuencia en lugar de tiempo

---

#### 3.2 Acceso Aleatorio

No se divide el canal. Los nodos transmiten cuando quieren, a tasa plena. Si hay colisión, se recupera de ella.

**Slotted ALOHA (ALOHA con ranuras)**

*Supuestos:*
- Todos los frames tienen el mismo tamaño
- El tiempo se divide en ranuras (1 ranura = tiempo de transmitir 1 frame)
- Los nodos solo comienzan a transmitir al inicio de una ranura
- Los nodos están sincronizados

*Operación:*
- Cuando un nodo tiene un frame nuevo, lo transmite en la próxima ranura
- Si **no hay colisión**: éxito → puede enviar otro frame en la siguiente ranura
- Si hay **colisión**: retransmite el frame en cada ranura subsiguiente con probabilidad `p` (aleatoriamente) hasta que tenga éxito

*Ejemplo visual:*
```
Nodo 1:  [1][1][  ][  ][1][  ][  ][1]
Nodo 2:  [2][  ][2][2][  ][  ]
Nodo 3:  [3][  ][  ][  ][3][  ][  ][  ][3]
          C  E   C  S   E   C   E   S   S
          ↑                ↑           ↑
       colisión         colisión    éxito
```
(C=colisión, E=vacía, S=éxito)

*Eficiencia máxima:*
```
P(éxito de un nodo) = p · (1-p)^(N-1)
P(éxito de cualquier nodo) = N · p · (1-p)^(N-1)
Eficiencia máxima cuando N→∞ = 1/e ≈ 0.37
```
**Solo el 37% del tiempo el canal se usa para transmisiones útiles.**

*Pros:* Simple, descentralizado, un nodo activo usa el canal completo
*Contras:* Colisiones, ranuras vacías, requiere sincronización de relojes

**Pure ALOHA (ALOHA puro / sin ranuras)**
- Más simple: sin sincronización. Cuando llega un frame, se transmite **inmediatamente**
- Mayor probabilidad de colisión porque un frame en t₀ puede colisionar con frames enviados en el rango [t₀-1, t₀+1]
- **Eficiencia máxima: 18%** — peor que el ALOHA con ranuras

**CSMA – Carrier Sense Multiple Access**
- "Escucha antes de transmitir" (listen before talk)
- Si el canal está **libre** → transmite el frame completo
- Si el canal está **ocupado** → espera (difiere la transmisión)
- Analogía humana: no interrumpas una conversación en curso

*Problema:* Las colisiones aún pueden ocurrir. El **retardo de propagación** significa que un nodo puede no "escuchar" que otro ya está transmitiendo (empezó justo antes). Toda la duración del frame se desperdicia.

**CSMA/CD – CSMA con Detección de Colisiones**
- Mientras transmite, el nodo también **escucha el canal**
- Si detecta una colisión → **aborta inmediatamente** + envía señal de interferencia (jam signal)
- Reducción del desperdicio: no se pierde toda la duración del frame
- Fácil en redes cableadas; difícil en inalámbricas (el nodo no puede escuchar mientras transmite)

*Algoritmo completo Ethernet CSMA/CD:*

```
1. NIC recibe datagrama de la capa red → crea frame
2. ¿Canal libre?
   - Libre → inicia transmisión
   - Ocupado → espera hasta que esté libre, luego transmite
3. ¿Transmitió el frame completo sin colisión? → ¡Listo! ✓
4. ¿Detectó otra transmisión durante el envío?
   - Aborta → envía señal jam
5. Backoff exponencial binario:
   - Tras la m-ésima colisión, elige K aleatoriamente de {0,1,...,2^m - 1}
   - Espera K·512 tiempos de bit → vuelve al paso 2
   - A más colisiones, mayor tiempo de espera (backoff más largo)
```

*Eficiencia de CSMA/CD:*
```
Eficiencia = 1 / (1 + 5·t_prop / t_trans)
```
- `t_prop` = retardo máximo de propagación entre 2 nodos
- `t_trans` = tiempo de transmitir el frame más grande
- Cuando `t_prop → 0` o `t_trans → ∞`, eficiencia → 1 (casi perfecto)
- Mejor rendimiento que ALOHA; simple, barato, descentralizado

---

#### 3.3 Protocolos "Tomándose Turnos"

Buscan lo mejor de ambos mundos: eficiencia a alta carga (como partición) + eficiencia a baja carga (como acceso aleatorio).

**Polling (Sondeo)**
- Un nodo **maestro** invita a cada esclavo a transmitir por turnos
- Usado con dispositivos "tontos" (ej: terminales legacy)
- Inconvenientes: overhead de polling, latencia, **punto único de falla** (si el maestro falla, todo colapsa)

**Token Passing (Paso de Token)**
- Se pasa un **token** (mensaje especial) de nodo en nodo secuencialmente
- Solo el nodo que tiene el token puede transmitir
- Usado en: Bluetooth, FDDI, Token Ring
- Inconvenientes: overhead del token, latencia, **punto único de falla** (si el token se pierde, la red se detiene)

### Red de Acceso por Cable: Combinación de FDM, TDM y acceso aleatorio

Las redes de cable (DOCSIS) usan una mezcla sofisticada:
- **Downstream (bajada):** múltiples canales FDM, un único CMTS (Cable Modem Termination System) transmite → hasta 1.6 Gbps por canal
- **Upstream (subida):** TDM + acceso aleatorio
  - Algunas ranuras se asignan fijas (TDM)
  - Otras son disputadas por contención (random access con backoff binario)
  - El CMTS envía tramas MAP que asignan las ranuras upstream

---

## 4. LANs: Direccionamiento y ARP

### Direcciones MAC

Existen dos tipos de direcciones en las redes:

| Característica | Dirección IP | Dirección MAC |
|---------------|-------------|--------------|
| Capa | 3 (Red) | 2 (Enlace) |
| Tamaño | 32 bits (IPv4) | 48 bits |
| Formato ejemplo | `128.119.40.136` | `1A-2F-BB-76-09-AD` |
| Portabilidad | No portátil (depende de la subred) | Portátil (grabada en hardware) |
| Analogía | Dirección postal (cambia con la ubicación) | Número de Seguridad Social (no cambia) |
| Alcance | Reenvío global de paquetes | Uso local (mismo enlace/subred) |

**Características de las direcciones MAC:**
- 48 bits, expresados en **hexadecimal** (cada número hexadecimal = 4 bits)
  - Ejemplo: `1A-2F-BB-76-09-AD` = 6 pares de 2 dígitos hex
- Grabadas ("burned in") en la ROM de la NIC por el fabricante
- Algunas NIC permiten cambiarlas por software
- La asignación es administrada por el **IEEE** (el fabricante compra bloques de direcciones para garantizar unicidad global)
- **Dirección de broadcast:** `FF-FF-FF-FF-FF-FF` (todos los nodos en el enlace reciben el frame)

### ARP: Address Resolution Protocol

**El problema:** La capa de red usa direcciones IP; la capa de enlace usa direcciones MAC. Cuando el nodo A quiere enviar un frame al nodo B (en la misma subred), necesita conocer la **MAC de B** conociendo solo su **IP**.

**La solución: ARP**

Cada nodo IP mantiene una **tabla ARP** con:
```
< IP address | MAC address | TTL >
```
- **TTL** (Time To Live): tiempo tras el cual se borra la entrada (típicamente 20 minutos)
- La tabla se construye dinámicamente y es "auto-mantenida"

**Proceso ARP paso a paso (A quiere enviar a B):**

```
Paso 1: A no encuentra la MAC de B en su tabla ARP
         → A envía un ARP Query en broadcast:
           Frame: destino = FF-FF-FF-FF-FF-FF (todos escuchan)
           Pregunta: "¿Quién tiene la IP 137.196.7.14?"

Paso 2: B reconoce su IP y responde directamente a A (unicast):
         Frame: destino = MAC de A
         Respuesta: "Yo tengo 137.196.7.14, mi MAC es 58-23-D7-FA-20-B0"

Paso 3: A recibe la respuesta y actualiza su tabla ARP:
         137.196.7.14 → 58-23-D7-FA-20-B0 (TTL=500s)
         Ahora puede enviar el frame a B directamente
```

### Enrutamiento entre subredes distintas

Cuando A quiere enviar a B en una **subred diferente**, necesita pasar por un router R. El proceso es más complejo:

**Situación:** A (111.111.111.111) quiere enviar a B (222.222.222.222), a través del router R.

**Flujo de frames y datagramas:**

```
TRAMO 1: A → R
  - Frame: [MAC_A → MAC_R | IP_A → IP_B | datos]
  - A usa la MAC de la interfaz de R en su subred (obtenida via ARP)
  - La IP destino del datagrama ya es la de B (no cambia)

En R:
  - R recibe el frame, extrae el datagrama, sube a capa IP
  - R consulta su tabla de ruteo → salida por interfaz hacia subred de B
  - R crea un NUEVO frame para el siguiente tramo

TRAMO 2: R → B
  - Frame: [MAC_R2 → MAC_B | IP_A → IP_B | datos]
  - El datagrama IP es el mismo (mismas IPs fuente y destino)
  - Solo el encabezado del frame cambia en cada salto

En B:
  - Recibe el frame, extrae el datagrama
  - Lo sube por la pila de protocolos hasta la aplicación
```

**Puntos clave:**
- Las **IPs** no cambian a lo largo de la ruta
- Las **MACs** cambian en cada salto (son locales a cada enlace)
- ARP se usa en cada subred para resolver las MACs necesarias

---

## 5. Ethernet

### ¿Qué es Ethernet?

Ethernet es la tecnología LAN cableada dominante. Sus características:
- Primera tecnología LAN ampliamente adoptada (inventada por Bob Metcalfe en Xerox PARC, 1973)
- Simple y económica
- Ha evolucionado en velocidad: **10 Mbps → 10 Mbps → 100 Mbps → 1 Gbps → 10 Gbps → 40 Gbps → 400 Gbps**
- Un solo chip puede operar a múltiples velocidades

### Topología física de Ethernet

**Bus (hasta mediados de los 90s):**
- Todos los nodos comparten un único cable coaxial
- Todos están en el mismo **dominio de colisión** (cualquier transmisión puede colisionar con cualquier otra)
- Si un cable se rompe, toda la red cae

**Switched / Conmutado (estándar actual):**
- Un **switch** (conmutador) activo en el centro
- Cada nodo tiene su propio cable directo al switch
- Cada enlace es su propio dominio de colisión → **no hay colisiones**

### Estructura del Frame Ethernet

```
┌──────────┬───────────┬───────────┬──────┬─────────────────────┬─────┐
│ Preámbulo│   Dest.   │  Origen   │ Tipo │    Datos (payload)  │ CRC │
│  7+1 B   │  MAC 6B   │  MAC 6B   │  2B  │    46 a 1500 B      │ 4B  │
└──────────┴───────────┴───────────┴──────┴─────────────────────┴─────┘
```

**Preámbulo (8 bytes):**
- 7 bytes de `10101010` seguidos de 1 byte de `10101011`
- Permite sincronizar los relojes del receptor y del emisor antes de los datos reales
- El último byte (`10101011`) señala: "empiezan los datos reales"

**Dirección destino y origen (6 bytes cada una):**
- Direcciones MAC del origen y el destino
- Si la dirección destino coincide con la MAC de la NIC (o es broadcast `FF:FF:FF:FF:FF:FF`), el frame se procesa
- Si no coincide, la NIC **descarta el frame** silenciosamente

**Tipo (2 bytes):**
- Indica qué protocolo de capa superior se usará
- Ejemplo: `0x0800` = IPv4, `0x0806` = ARP, `0x86DD` = IPv6
- Permite **demultiplexar** el frame correctamente en el receptor

**Datos / Payload (46 a 1500 bytes):**
- El datagrama IP (u otro protocolo) encapsulado
- Tamaño mínimo 46 bytes (si el datagrama es menor, se añade relleno)
- Tamaño máximo 1500 bytes = **MTU** (Maximum Transmission Unit) de Ethernet

**CRC (4 bytes):**
- Cyclic Redundancy Check para detección de errores
- Si se detecta error → el frame se **descarta** (sin notificación al emisor)
- Ethernet es "best effort": no reintenta

### Características de Ethernet

**Sin conexión (connectionless):**
- No hay handshaking previo entre las NICs emisora y receptora
- Se envía el frame directamente, sin establecer una "sesión"

**No confiable (unreliable):**
- La NIC receptora **no envía ACK ni NAK** a la emisora
- Si un frame se pierde o tiene errores → se descarta sin aviso
- La recuperación depende de capas superiores (ej: TCP retransmitirá; UDP no)

**Protocolo MAC:**
- Ethernet usa **CSMA/CD sin ranuras con backoff binario exponencial**

### Estándares Ethernet 802.3

Todos los estándares comparten el mismo protocolo MAC y formato de frame, pero difieren en velocidad y medio físico:

| Estándar | Velocidad | Medio |
|---------|-----------|-------|
| 10BASE-T | 10 Mbps | Par trenzado |
| 100BASE-TX | 100 Mbps | Par trenzado (2 pares Cat5) |
| 100BASE-FX | 100 Mbps | Fibra óptica |
| 1000BASE-T | 1 Gbps | Par trenzado (4 pares Cat5e) |
| 10GBASE-SR | 10 Gbps | Fibra óptica multimodo |
| 40GBASE-CR4 | 40 Gbps | Cable de cobre apantallado |

La notación: `[velocidad]BASE-[medio]`
- BASE = banda base (usa todo el ancho del canal)
- TX = twisted pair (par trenzado), FX = fiber (fibra), etc.

---

## 6. Switches (Conmutadores)

### ¿Qué es un switch Ethernet?

Un switch es un dispositivo de **capa de enlace** (Layer 2) que:
- Almacena y reenvía frames Ethernet (**store-and-forward**)
- Examina la dirección MAC destino y decide a qué puerto enviarlo
- Es **transparente**: los hosts no saben que existe (no necesitan configurarlo)
- Es **plug-and-play**: no requiere configuración manual
- Es **auto-aprendiz**: aprende solo las rutas

### Ventajas del switch frente al hub/bus

Con un switch:
- Cada host tiene su propio enlace dedicado (full-duplex)
- **No hay colisiones** entre hosts diferentes (cada enlace es su dominio de colisión)
- Múltiples transmisiones simultáneas son posibles

Ejemplo con 6 interfaces:
- A puede enviar a A' mientras B envía a B' → **sin colisión**
- Pero A y C **no pueden** enviar a A' simultáneamente (mismo destino → contienden en el puerto de salida)

### Tabla de Reenvío del Switch

El switch mantiene una tabla similar a la de enrutamiento:
```
MAC Address    | Interfaz | Timestamp
58-23-D7-FA-20-B0 |    4    |   60s
71-65-F7-2B-08-53 |    1    |   60s
```

### Auto-aprendizaje (Self-learning)

El switch aprende las MACs automáticamente observando el tráfico:

1. Cuando llega un frame por el puerto X con MAC origen M:
   - El switch registra: "M está accesible por el puerto X"
   - Actualiza la tabla con un timestamp

2. Para enviar: el switch busca la MAC destino en la tabla:
   - **Encontrada:** reenvía solo por el puerto indicado
   - **No encontrada:** hace **flooding** → reenvía por todos los puertos excepto por donde llegó

3. Las entradas expiran (TTL) y se eliminan si no se refrescan

**Algoritmo de filtrado/reenvío:**
```
Al recibir frame:
  1. Registrar: (MAC_origen, puerto_entrada, timestamp) en la tabla
  2. Buscar MAC_destino en la tabla
  3. Si encontrada:
       Si destino está en el mismo segmento de donde llegó → DROP (descarta)
       Sino → Reenvía solo por el puerto indicado
  4. Si no encontrada → FLOOD (todos los puertos excepto el de entrada)
```

### Switches Interconectados

Los switches de auto-aprendizaje pueden conectarse entre sí formando redes complejas:

```
         S4
   S1          S3
A     S2     F      I
  B  C    D     G H
        E
```

Si A quiere enviar a G, S1 aprende automáticamente (sin configuración) qué camino tomar a través de S4 y S3. El auto-aprendizaje funciona exactamente igual que con un solo switch.

### Switches vs Routers

| Característica | Switch | Router |
|---------------|--------|--------|
| Capa | 2 (Enlace) | 3 (Red) |
| Examina | Encabezado de frame (MAC) | Encabezado IP |
| Tabla de reenvío | Aprende por flooding/learning | Calculada por algoritmos de routing |
| Direcciones usadas | MAC | IP |
| Ámbito | Dentro de una LAN/subred | Entre subredes/Internet |
| Configuración | Plug-and-play | Requiere configuración |

Ambos son dispositivos **store-and-forward**: reciben, almacenan brevemente y luego reenvían.

---

## 7. VLANs (Redes de Área Local Virtuales)

### El problema que resuelven

En una LAN grande sin VLANs, todos los hosts comparten el mismo dominio de broadcast. Esto genera:

1. **Escalabilidad:** Todo el tráfico broadcast de capa 2 (ARP, DHCP, MACs desconocidas) debe atravesar **toda** la LAN. Con miles de hosts, esto satura la red.

2. **Seguridad y privacidad:** Cualquier host puede capturar broadcasts de cualquier otro. Departamentos que no deberían "verse" entre sí quedan expuestos.

3. **Administración:** Si un empleado del departamento de CS se muda físicamente a la oficina de EE, queda conectado al switch de EE pero quiere pertenecer lógicamente a la red de CS.

### ¿Qué es una VLAN?

Una VLAN permite que un **único switch físico** se comporte como **múltiples switches lógicos independientes**, cada uno con su propio dominio de broadcast.

### VLANs basadas en puertos (Port-based VLANs)

Los puertos del switch se agrupan mediante software de administración:

```
Switch físico único:
┌─────────────────────────────────────────────┐
│  Puerto 1  │  Puerto 2  │ ... │  Puerto 8   │  ← VLAN EE
│  Puerto 9  │  Puerto 10 │ ... │  Puerto 15  │  ← VLAN CS
└─────────────────────────────────────────────┘
```

Esto opera como si fueran dos switches separados:
- Los frames de los puertos 1-8 **solo pueden llegar** a otros puertos 1-8 (VLAN EE)
- Los frames de los puertos 9-15 **solo pueden llegar** a otros puertos 9-15 (VLAN CS)

**Características:**
- **Aislamiento de tráfico:** Un frame de VLAN EE nunca llegará a un puerto de VLAN CS
- **También posible por MAC:** Alternativamente, se puede asignar por MAC de los endpoints (más flexible pero más complejo)
- **Membresía dinámica:** Los puertos se pueden reasignar entre VLANs en cualquier momento
- **Enrutamiento entre VLANs:** Para que EE y CS se comuniquen, se necesita un **router** (o un switch de Capa 3)

### VLANs que abarcan múltiples switches

Si la VLAN EE existe en dos switches físicos distintos, se necesita un mecanismo para transportar frames entre switches manteniendo la información de VLAN:

**Puerto troncal (Trunk port):**
- Un puerto especial que transporta frames de **múltiples VLANs**
- Los frames en el trunk deben identificar a qué VLAN pertenecen (no pueden ser frames 802.1 estándar)
- Se usa el protocolo **802.1Q**

### Protocolo 802.1Q

Añade un campo de 4 bytes al frame Ethernet estándar:

```
Frame 802.1 estándar:
┌──────────┬───────┬───────┬──────┬──────────────┬─────┐
│ Preámbulo│ Dest  │ Orig  │ Tipo │     Datos    │ CRC │
└──────────┴───────┴───────┴──────┴──────────────┴─────┘

Frame 802.1Q (con tag VLAN):
┌──────────┬───────┬───────┬──────┬──────┬────────────┬─────┐
│ Preámbulo│ Dest  │ Orig  │ TPID │ TCI  │    Datos   │ CRC │
│          │       │       │ 2B   │ 2B   │            │     │
└──────────┴───────┴───────┴──────┴──────┴────────────┴─────┘
```

- **TPID** (Tag Protocol Identifier, 2 bytes): valor fijo `0x8100` que identifica el frame como 802.1Q
- **TCI** (Tag Control Information, 2 bytes): contiene:
  - 12 bits de **VLAN ID** (hasta 4096 VLANs diferentes)
  - 3 bits de **prioridad** (similar al campo TOS de IP, para QoS)
- El CRC se **recalcula** al añadir el tag

Los switches que reciben el frame en el trunk leen el VLAN ID y saben a qué VLAN pertenece el frame.

---

## 8. Virtualización de Enlace: MPLS

### El problema que MPLS resuelve

El enrutamiento IP estándar busca la coincidencia del **prefijo más largo** en las tablas de enrutamiento para cada paquete. Esto es lento y no permite control fino de las rutas. MPLS (Multiprotocol Label Switching) ofrece:
- **Mayor velocidad**: usa etiquetas de longitud fija en lugar de búsqueda de prefijos
- **Mayor control**: la ruta puede depender de origen + destino (no solo destino)
- **Recuperación rápida**: rutas de respaldo precalculadas

### ¿Cómo funciona MPLS?

**Estructura del frame MPLS:**
```
┌────────────────────────────────────────────────────────┐
│  Encabezado Ethernet  │  Encabezado MPLS  │  Datagrama IP  │
└────────────────────────────────────────────────────────┘
                            ↓ detalle del encabezado MPLS:
                    ┌────────┬─────┬───┬─────┐
                    │ Label  │ Exp │ S │ TTL │
                    │ 20 bits│ 3b  │ 1b│ 8b  │
                    └────────┴─────┴───┴─────┘
```

- **Label (20 bits):** la etiqueta usada para el reenvío
- **Exp (3 bits):** bits experimentales (usados para QoS/prioridad)
- **S (1 bit):** bit de pila (stack) - indica si es la última etiqueta
- **TTL (8 bits):** Time To Live (como en IP)

**El datagrama IP original se mantiene intacto dentro del frame MPLS.**

### Enrutadores MPLS (Label-Switched Routers)

Un router MPLS (también llamado LSR, Label-Switched Router):
- Reenvía paquetes basándose **solo en la etiqueta** (no inspecciona la IP)
- Tiene su propia tabla de reenvío MPLS (separada de la tabla IP)
- Al recibir un paquete: busca la etiqueta entrada → determina etiqueta salida + interfaz de salida

**Tabla de reenvío MPLS ejemplo:**
```
Label entrada | Label salida | Destino | Interfaz salida
     10       |      6       |    A    |       1
     12       |      9       |    D    |       0
```

### MPLS vs IP: comparación de rutas

```
Red con routers R1...R6 y destinos A y D

IP: La ruta siempre va al destino más corto (solo el destino determina la ruta)
     R4 → R3 → R1 → A  (mismo camino para todos los paquetes hacia A)

MPLS: El router de entrada (R4) puede usar DIFERENTES rutas MPLS
     según el origen del paquete:
     - Tráfico de S1: R4 → R3 → R1 → A
     - Tráfico de S2: R4 → R2 → R1 → A  (ruta alternativa)
```

Esto se llama **traffic engineering** (ingeniería de tráfico): la capacidad de distribuir el tráfico de forma diferente a como lo haría IP puro.

### Señalización MPLS

Para establecer las rutas MPLS, se modifican los protocolos de estado de enlace existentes:
- **OSPF e IS-IS** se extienden para transportar información MPLS (ancho de banda disponible, ancho de banda reservado)
- El router de entrada usa **RSVP-TE** (Resource Reservation Protocol - Traffic Engineering) para configurar el reenvío MPLS en todos los routers del camino

---

## 9. Redes de Centros de Datos

### Características generales

Los centros de datos modernos albergan desde decenas de miles hasta **cientos de miles de servidores** muy cercanos entre sí. Ejemplos:
- E-commerce: Amazon
- Servidores de contenido: YouTube, Akamai, Apple, Microsoft
- Motores de búsqueda y minería de datos: Google

### Desafíos

- Múltiples aplicaciones sirviendo a **millones de clientes** simultáneamente
- Alta **fiabilidad** requerida (no puede caerse)
- **Balanceo de carga**: distribuir el trabajo uniformemente entre servidores
- Evitar cuellos de botella en procesamiento, red y almacenamiento

### Arquitectura de red del datacenter

```
Internet
   │
Border Routers (Enrutadores de borde)
   │           ← conexiones al exterior
Tier-1 Switches (Conmutadores de nivel 1)
   │           ← cada uno conectado a ~16 Tier-2
Tier-2 Switches (Conmutadores de nivel 2)
   │           ← cada uno conectado a ~16 TOR
Top-of-Rack (TOR) Switches
   │           ← uno por rack, Ethernet 40-100 Gbps
Server Racks (Racks de servidores)
               ← 20-40 server blades por rack
```

Esta jerarquía de 3 niveles permite escalar a cientos de miles de servidores.

**Ejemplo real:** Topología F16 de Facebook (publicada en 2019): usa una arquitectura de red plana con múltiples rutas y alto ancho de banda entre todos los racks.

### Multipaths (Múltiples caminos)

La interconexión rica entre switches y racks proporciona:
- **Mayor rendimiento:** múltiples rutas posibles entre racks (mayor throughput agregado)
- **Mayor fiabilidad:** redundancia; si un enlace falla, hay rutas alternativas

Los switches están interconectados de forma que existen múltiples caminos **disjuntos** entre cualquier par de racks (lo que evita un único punto de fallo).

### Balanceador de Carga (Load Balancer)

El load balancer es un componente crítico con enrutamiento de **capa de aplicación**:

```
Cliente externo → Internet → Load Balancer → Servidor interno adecuado
                  ←────────────────────────────────────────────────── respuesta
```

**Funciones:**
1. Recibe solicitudes de clientes externos
2. Selecciona el servidor interno más apropiado (el menos cargado, el más cercano, etc.)
3. Dirige la solicitud al servidor seleccionado
4. Devuelve la respuesta al cliente
5. **Oculta la infraestructura interna** al cliente (el cliente solo ve una IP/dominio público)

### Innovaciones de Protocolos en Datacenters

**Capa de enlace:**
- **RoCE** (RDMA over Converged Ethernet): permite DMA remoto (acceso directo a memoria de otro servidor) sobre Ethernet, eliminando la latencia de la pila TCP/IP para comunicaciones servidor-servidor de baja latencia

**Capa de transporte:**
- **ECN** (Explicit Congestion Notification): notificación explícita de congestión, usada en DCTCP (Datacenter TCP) y DCQCN para control de congestión más eficiente
- Experimentación con control de congestión **hop-by-hop** (contrapresión entre switches)

**Enrutamiento y gestión:**
- **SDN** (Software-Defined Networking): ampliamente utilizado para gestionar las redes internas de los datacenters
- Estrategia de colocación: ubicar servicios y datos relacionados **en el mismo rack o racks cercanos** para minimizar la comunicación que sube a los niveles Tier-1 y Tier-2 (que son los cuellos de botella)

---

## 10. Un Día en la Vida de una Solicitud Web

Esta sección sintetiza todos los protocolos estudiados en el libro mostrando qué ocurre, capa por capa, cuando un estudiante conecta su laptop a la red del campus y visita `www.google.com`.

### Escenario

- **Cliente:** laptop del estudiante (conectada por Ethernet o WiFi al switch del campus)
- **Red del campus:** `68.80.2.0/24`
- **DNS server:** Comcast (proveedor ISP)
- **Web server:** `www.google.com` → IP: `64.233.169.105` (red `64.233.160.0/19`)

### Fase 1: Obtener dirección IP (DHCP)

El laptop recién conectado no tiene IP asignada. Usa **DHCP** (Dynamic Host Configuration Protocol):

```
1. Laptop genera un mensaje DHCP Request (¡necesito una IP!)
2. Encapsula: DHCP → UDP → IP (src: 0.0.0.0, dst: 255.255.255.255) → Ethernet (dst: FF:FF:FF:FF:FF:FF)
3. Envía el frame en broadcast a toda la red local
4. El router del campus (que tiene un servidor DHCP) recibe el frame
   - Ethernet demux → IP demux → UDP demux → DHCP
5. El servidor DHCP responde con un DHCP ACK que incluye:
   - IP asignada al laptop
   - IP del router de primer salto (default gateway)
   - Nombre e IP del servidor DNS
6. El laptop recibe el DHCP ACK, ya conoce:
   ✓ Su propia IP
   ✓ La IP del router (primer salto)
   ✓ La IP del servidor DNS
```

### Fase 2: Resolver la MAC del router (ARP)

Antes de enviar al DNS, el laptop necesita conocer la **MAC del router** para poder construir el frame:

```
1. Laptop genera un ARP Query:
   "¿Quién tiene la IP [router]? Soy [IP_laptop], [MAC_laptop]"
2. Broadcast a FF:FF:FF:FF:FF:FF
3. El router responde con su MAC
4. Laptop actualiza su tabla ARP con la MAC del router
```

### Fase 3: Resolver el nombre DNS

Con la MAC del router disponible, el laptop puede enviar el paquete DNS:

```
1. Laptop construye DNS Query: "¿Cuál es la IP de www.google.com?"
2. Encapsula: DNS → UDP → IP (dst: IP_DNS_server) → Ethernet (dst: MAC_router)
3. El router recibe el frame, extrae el datagrama IP
4. El datagrama IP se enruta a través de la red Comcast (usando RIP, OSPF, BGP)
   hasta el servidor DNS
5. El servidor DNS responde con la IP de www.google.com: 64.233.169.105
6. La respuesta DNS viaja de regreso al laptop (enrutada por BGP/OSPF/RIP)
```

### Fase 4: Establecer conexión TCP (3-way handshake)

Para enviar el HTTP request, primero se necesita una conexión TCP:

```
1. Laptop envía SYN → enrutado hasta el servidor web de Google
2. Servidor web responde con SYN-ACK → enrutado de vuelta al laptop
3. Laptop envía ACK → conexión TCP establecida ✓
```

Todo esto requiere múltiples encapsulaciones a través de diferentes redes y enrutadores.

### Fase 5: Petición y respuesta HTTP

```
1. Laptop envía HTTP GET / (encapsulado en TCP, IP, Ethernet)
2. El paquete viaja por múltiples routers hasta el servidor de Google
3. Google recibe el GET, genera la página web
4. Responde con HTTP 200 OK + contenido HTML (encapsulado en TCP, IP, Ethernet)
5. La respuesta viaja de vuelta al laptop, siendo enrutada por la red
6. El navegador recibe el HTML y renderiza la página ¡¡¡por fin!!!
```

### Mapa completo de protocolos involucrados

| Capa | Protocolo | Función en este escenario |
|------|-----------|--------------------------|
| Aplicación | HTTP | Solicitar/recibir la página web |
| Aplicación | DNS | Resolver www.google.com → IP |
| Aplicación | DHCP | Obtener IP, gateway, DNS |
| Transporte | TCP | Conexión confiable para HTTP |
| Transporte | UDP | Transporte de DNS y DHCP |
| Red | IP | Enrutamiento de paquetes |
| Red | BGP, OSPF, RIP | Construir las tablas de enrutamiento |
| Enlace | Ethernet | Transferencia local (frame a frame) |
| Enlace | ARP | Resolver IPs a MACs |
| Enlace | 802.1Q | Si hay VLANs en el campus |

---

## Resumen del Capítulo

El Capítulo 6 cubre la **capa de enlace**, la última capa antes del hardware puro. Los conceptos clave son:

1. **Servicios de la capa de enlace:** framing, detección/corrección de errores, entrega confiable, control de flujo, acceso al medio compartido.

2. **Detección de errores:** paridad simple/bidimensional, checksum de Internet, y CRC (el más poderoso, usado en Ethernet y WiFi).

3. **Protocolos MAC:** tres familias — partición de canal (TDMA, FDMA), acceso aleatorio (ALOHA, CSMA, CSMA/CD), y "tomándose turnos" (polling, token passing).

4. **Ethernet:** tecnología dominante, usa CSMA/CD, frame con MAC de 48 bits, sin conexión, no confiable.

5. **Switches:** dispositivos de capa 2, auto-aprendices, plug-and-play. Eliminan colisiones al crear dominios de colisión separados por puerto.

6. **VLANs:** permiten segmentar lógicamente una LAN física; el protocolo 802.1Q añade tags VLAN a los frames para transportarlos entre switches (trunk ports).

7. **MPLS:** virtualiza la red de enlace usando etiquetas fijas para reenvío rápido y control de rutas (traffic engineering).

8. **Datacenters:** arquitecturas jerárquicas de switches, múltiples caminos, balanceadores de carga, e innovaciones de protocolo (RoCE, DCTCP, SDN).

9. **Día en la vida:** la síntesis final muestra cómo DHCP, ARP, DNS, TCP, HTTP, y Ethernet colaboran en una simple visita a una página web.

---

*Basado en: Kurose, J.F. & Ross, K.W. — Computer Networking: A Top-Down Approach, 8ª Edición, Pearson 2020. Capítulo 6: The Link Layer and LANs.*
