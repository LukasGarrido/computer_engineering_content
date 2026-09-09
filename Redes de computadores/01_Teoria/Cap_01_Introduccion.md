# Capítulo 1: Introducción a las Redes de Computadores
### Computer Networking: A Top-Down Approach — Kurose & Ross, 8ª ed.
> Guía completa de estudio para certamen

---

## Índice
1. [¿Qué es Internet?](#1-qué-es-internet)
2. [¿Qué es un Protocolo?](#2-qué-es-un-protocolo)
3. [Perímetro de la Red: Hosts y Redes de Acceso](#3-perímetro-de-la-red-hosts-y-redes-de-acceso)
4. [Medios Físicos](#4-medios-físicos)
5. [El Núcleo de la Red](#5-el-núcleo-de-la-red)
6. [Conmutación de Paquetes vs. Conmutación de Circuitos](#6-conmutación-de-paquetes-vs-conmutación-de-circuitos)
7. [Estructura de Internet: Red de Redes](#7-estructura-de-internet-red-de-redes)
8. [Rendimiento: Pérdida, Retardo y Throughput](#8-rendimiento-pérdida-retardo-y-throughput)
9. [Seguridad en Redes](#9-seguridad-en-redes)
10. [Capas de Protocolo y Encapsulación](#10-capas-de-protocolo-y-encapsulación)
11. [Historia de Internet](#11-historia-de-internet)
12. [Resumen Rápido y Tablas de Referencia](#12-resumen-rápido-y-tablas-de-referencia)

---

## 1. ¿Qué es Internet?

### Vista práctica ("nuts and bolts")

Internet puede describirse desde dos perspectivas complementarias.

**Perspectiva de hardware y software:**

Internet es una **red de redes** formada por tres componentes esenciales:

- **Hosts (sistemas finales):** Miles de millones de dispositivos de cómputo conectados — computadores, teléfonos, tablets, sensores, televisores, automóviles, etc. Corren aplicaciones en el "borde" de Internet (network edge). El término *host* = *end system*.
- **Packet switches (conmutadores de paquetes):** Dispositivos que reciben y reenvían paquetes hacia su destino. Los principales son los **routers** (en el núcleo de la red) y los **switches** (en redes de acceso).
- **Communication links (enlaces de comunicación):** Fibra óptica, cable coaxial, cobre, radio, satélite. Cada enlace tiene una **tasa de transmisión** (bandwidth), medida en bits por segundo (bps).

**Perspectiva de servicios:**

Internet es una **infraestructura que provee servicios a aplicaciones distribuidas** — web, streaming, email, juegos, comercio electrónico, redes sociales, IoT. Internet proporciona una **interfaz de programación (API)** para que las aplicaciones puedan enviar y recibir datos, similar a cómo el servicio postal ofrece opciones de envío.

### Estándares de Internet

Los protocolos de Internet se definen en documentos públicos llamados **RFC (Request For Comments)**, administrados por el **IETF (Internet Engineering Task Force)**. Los protocolos abiertos (HTTP, SMTP, TCP, IP) permiten la interoperabilidad entre dispositivos de distintos fabricantes.

> **Para el certamen:** Internet = "red de redes" de ISPs interconectados. Los protocolos están en todas partes. RFC = estándar público. IETF = organismo que los gestiona.

---

## 2. ¿Qué es un Protocolo?

Un **protocolo** define el **formato**, el **orden** de los mensajes enviados y recibidos entre entidades de la red, y las **acciones** que se toman al transmitir y recibir esos mensajes.

**Analogía humana:** Cuando preguntas "¿Tienes la hora?" esperas un saludo o la hora — no que la persona empiece a hablar de otro tema. Hay un formato implícito, un orden y una respuesta esperada. Los protocolos de red hacen lo mismo entre máquinas.

**Ejemplo HTTP:**
```
Cliente                              Servidor
   │                                    │
   │──── TCP connection request ───────►│
   │◄─── TCP connection response ───────│
   │──── GET http://gaia.cs.umass.edu ─►│
   │◄─── <file> ────────────────────────│
```

Toda actividad de comunicación en Internet está gobernada por protocolos: HTTP, TCP, IP, WiFi, Ethernet, 4G, etc.

---

## 3. Perímetro de la Red: Hosts y Redes de Acceso

### Estructura general de Internet

Se divide en tres partes que conviene distinguir:

- **Network edge (perímetro):** Hosts — clientes y servidores. Los servidores suelen estar en centros de datos.
- **Access networks / physical media (redes de acceso):** Cómo los hosts se conectan al primer router del ISP (el "edge router"). Pueden ser cableadas o inalámbricas.
- **Network core (núcleo):** Routers interconectados — la "red de redes".

---

### Redes de Acceso: ¿Cómo conectar el host al edge router?

#### Cable (HFC — Hybrid Fiber Coax)

El acceso por cable residencial usa una infraestructura de **fibra óptica + cable coaxial**. La señal se divide en múltiples canales de frecuencia mediante **FDM (Frequency Division Multiplexing)**: canales de video, canales de datos, canal de control.

- **HFC es asimétrico:** descarga mucho más rápida que subida.
  - Descarga: hasta 40 Mbps – 1.2 Gbps
  - Subida: 30 – 100 Mbps
- Los hogares **comparten** el mismo cable coaxial de acceso a la cabecera (cable headend). Esto significa que el ancho de banda se divide entre los vecinos.
- El **CMTS (Cable Modem Termination System)** en la cabecera conecta la red de cable al ISP.

#### DSL (Digital Subscriber Line)

Usa la **línea telefónica existente** (par de cobre) para llevar datos.

- Un **DSL modem** en el hogar convierte los datos digitales en señales que viajan por el cable telefónico.
- El **DSLAM (DSL Access Multiplexer)** en la central telefónica separa la señal de voz y de datos:
  - Datos → Internet
  - Voz → red telefónica pública
- **DSL es dedicado:** la línea telefónica solo conecta tu hogar con la central. No se comparte con vecinos (a diferencia del cable).
- Velocidades típicas: descarga 24–52 Mbps, subida 3.5–16 Mbps.

#### Redes domésticas (Home Networks)

Un hogar típico combina: modem DSL o cable → router/NAT/firewall → switch Ethernet (1 Gbps) → AP WiFi (54/450 Mbps) → dispositivos. En la práctica, todos estos componentes suelen integrarse en **una sola caja**.

#### Redes Inalámbricas de Acceso

Conexión a través de una **estación base** (punto de acceso, access point).

**WLAN (Wireless LAN / WiFi):**
- Dentro o alrededor de un edificio (~30 metros).
- Estándar 802.11: versión b=11 Mbps, g=54 Mbps, n=450 Mbps.

**Redes celulares de área amplia (4G/5G):**
- Provistas por operadores móviles, cobertura de ~10 km.
- 4G: decenas de Mbps. 5G: cientos de Mbps o más.

#### Redes Empresariales

Mezcla de tecnologías cableadas (Ethernet a 100 Mbps / 1 Gbps / 10 Gbps) e inalámbricas (WiFi), conectando switches y routers internos hacia un router institucional que enlaza con el ISP.

#### Redes de Centros de Datos

Los servidores de Google, Amazon, Netflix, etc. se conectan entre sí y hacia Internet mediante **enlaces de altísimo ancho de banda** (decenas a cientos de Gbps), dentro de instalaciones que alojan decenas de miles de servidores.

### El host como emisor de paquetes

Un host toma un mensaje de la aplicación, lo divide en **paquetes** de L bits, y los transmite al enlace de acceso a tasa R bps.

```
Packet transmission delay (tiempo de transmisión) = L (bits) / R (bits/sec)
```

Este es uno de los cuatro tipos de retardo que se acumulan en la red.

---

## 4. Medios Físicos

Un bit viaja por el **medio físico** entre pares transmisor-receptor.

- **Medios guiados:** señal se propaga dentro de un material sólido.
- **Medios no guiados:** señal se propaga libremente (radio, microondas, satélite).

### Comparación de medios físicos

| Medio | Tipo | Velocidad | Características |
|-------|------|-----------|-----------------|
| **Par trenzado (TP)** | Guiado | Cat5: 100 Mbps/1 Gbps. Cat6: 10 Gbps | Dos cables de cobre aislados y trenzados. El más económico y común. |
| **Cable coaxial** | Guiado | 100s Mbps/canal | Dos conductores concéntricos. Bidireccional. Permite múltiples canales (FDM). |
| **Fibra óptica** | Guiado | 10–100 Gbps | Pulsos de luz en fibra de vidrio. Alta velocidad, baja tasa de error, inmune a interferencias electromagnéticas, repetidores muy distantes. |
| **Radio WiFi (WLAN)** | No guiado | 11–450 Mbps | Cobertura ~30 m. Sujeto a interferencias, reflexión, obstrucción. |
| **Radio celular (4G)** | No guiado | 10s Mbps | Cobertura ~10 km. |
| **Microondas terrestres** | No guiado | 45 Mbps | Punto a punto. |
| **Satélite** | No guiado | Hasta 45 Mbps/canal | Retardo extremo a extremo de ~270 ms (por la distancia orbital). |

**Características de la radio inalámbrica:** broadcast (todos reciben), half-duplex (emisor no puede recibir simultáneamente), efectos de propagación: reflexión, obstrucción por objetos, interferencia/ruido.

---

## 5. El Núcleo de la Red

El **núcleo de Internet** es una malla de routers interconectados. Su función es recibir paquetes y reenviarlos hacia su destino final.

### Dos funciones clave del núcleo

**Forwarding (Reenvío):** Acción local. El router examina el campo de dirección destino en la cabecera del paquete entrante y lo mueve al puerto de salida adecuado según su **tabla de reenvío local**. Ocurre en nanosegundos (hardware).

**Routing (Enrutamiento):** Acción global. Algoritmos de enrutamiento calculan las rutas de extremo a extremo que siguen los paquetes y construyen las tablas de reenvío. Ocurre en milisegundos (software).

**Analogía:** Routing = planificar el recorrido completo en el mapa antes de viajar. Forwarding = tomar la decisión en cada intersección/peaje durante el viaje.

### Conmutación de Paquetes: Store-and-Forward

En **packet switching**, el host divide el mensaje en **paquetes**. Cada router recibe el paquete completo, lo procesa y lo reenvía al siguiente enlace.

**Store-and-Forward:** El paquete entero debe llegar al router antes de que pueda transmitirse por el siguiente enlace.

**Ejemplo numérico:** L = 10 Kbits, R = 100 Mbps → tiempo de transmisión = L/R = 0.1 ms.

**Retardo de transmisión de un paquete por N enlaces:**
```
d_extremo_a_extremo = N × L/R
```
(suponiendo que no hay retardo de cola ni propagación.)

### Colas y Pérdida de Paquetes

Si la **tasa de llegada** de paquetes a un router supera temporalmente la **capacidad de transmisión** del enlace de salida:

- Los paquetes se almacenan en la **cola (buffer)** del router → esperan ser transmitidos → **retardo de cola**.
- Si la cola se llena (buffer overflow) → los paquetes se **descartan (pierden)**.
- El paquete perdido puede ser retransmitido por el host origen, por el nodo anterior, o no retransmitirse.

---

## 6. Conmutación de Paquetes vs. Conmutación de Circuitos

### Circuit Switching (Conmutación de Circuitos)

Antes de transmitir datos, se establece un **circuito dedicado de extremo a extremo** para la llamada. Los recursos (ancho de banda en cada enlace) se **reservan** y no se comparten.

- **Garantiza** rendimiento constante (como una llamada telefónica clásica).
- Si el circuito no se usa activamente, los recursos se **desperdician** (permanecen ociosos).
- Requiere tiempo de establecimiento de llamada.
- Usado en redes telefónicas tradicionales (PSTN).

**Multiplexación en circuit switching:**

- **FDM (Frequency Division Multiplexing):** Cada llamada ocupa una banda de frecuencia distinta y exclusiva. Puede transmitir continuamente pero solo a la velocidad de esa banda estrecha.
- **TDM (Time Division Multiplexing):** El tiempo se divide en slots. A cada llamada se le asignan slots periódicos. Puede transmitir a la velocidad completa del enlace, pero solo durante sus slots.

### Packet Switching (Conmutación de Paquetes)

Los recursos de la red **no se reservan**. Los paquetes de distintos flujos se intercalan en el mismo enlace según disponibilidad — esto se llama **statistical multiplexing** (multiplexación estadística).

- Excelente para tráfico **bursty** (en ráfagas): muchas aplicaciones no usan la red constantemente.
- Permite que más usuarios compartan la red.
- No garantiza rendimiento constante.
- Puede generar congestión, retardo y pérdidas.

**Ejemplo numérico comparativo:**

Enlace de 1 Gbps. Cada usuario necesita 100 Mbps cuando está activo, pero solo está activo el 10% del tiempo.

- **Circuit switching:** solo puede haber 10 usuarios simultáneos (1 Gbps / 100 Mbps = 10). Si hay 11 usuarios, el undécimo no puede conectarse.
- **Packet switching:** con 35 usuarios, la probabilidad de que más de 10 estén activos al mismo tiempo es menor que 0.0004. En la práctica, 35 usuarios coexisten cómodamente.

**Conclusión:** Packet switching permite más usuarios con la misma infraestructura, siempre que el tráfico sea bursty. Internet usa packet switching.

> **Para el certamen:** Circuit switching = recursos reservados + garantía + desperdicio. Packet switching = compartido + eficiente + sin garantía + posible congestión.

---

## 7. Estructura de Internet: Red de Redes

### El problema de escala

Hay millones de ISPs de acceso en el mundo. Conectarlos directamente entre sí requeriría O(N²) conexiones — imposible de escalar. La solución es una **jerarquía de ISPs**.

### Evolución hacia la estructura actual

La estructura de Internet evolucionó por motivaciones **económicas y de política**, no por un diseño central. Los pasos fueron:

1. Cada ISP de acceso se conecta a un **ISP de tránsito global** (acuerdo económico cliente-proveedor).
2. Como un ISP global viable genera competidores, surgen múltiples **ISP Tier-1** que deben interconectarse.
3. Los Tier-1 se interconectan en puntos llamados **IXP (Internet eXchange Points)**, donde se hace "peering" (intercambio de tráfico gratuito entre iguales).
4. Surgen **ISP regionales** que conectan ISPs de acceso locales a los Tier-1.
5. Las grandes empresas de contenido (Google, Netflix, Meta) crean sus propias redes privadas globales (**content provider networks**) que se conectan directamente a ISPs regionales y de acceso, evitando los Tier-1.

### Estructura actual

```
         ISP Tier-1 (AT&T, NTT, Sprint)
              /      IXP      \
       ISP Regional        ISP Regional
          /    \               /    \
  ISP Acceso  ISP Acceso   ISP Acceso ISP Acceso
      |             |
    Host          Host
```

En el "centro": pocos Tier-1 y redes de proveedores de contenido muy bien conectados. En la periferia: millones de ISPs de acceso.

> **Para el certamen:** Los ISP de acceso conectan usuarios a Internet. Los Tier-1 son la columna vertebral global. Los IXP permiten peering entre ISPs. Las CDN y redes de content providers (Google, etc.) evitan los Tier-1.

---

## 8. Rendimiento: Pérdida, Retardo y Throughput

### Los cuatro tipos de retardo de paquetes

En cada router del camino, un paquete experimenta:

```
d_nodal = d_proc + d_queue + d_trans + d_prop
```

| Componente | Símbolo | Descripción | Magnitud típica |
|------------|---------|-------------|-----------------|
| **Retardo de procesamiento** | d_proc | Tiempo para verificar errores de bits y determinar el enlace de salida | < microsegundos |
| **Retardo de cola** | d_queue | Tiempo esperando en la cola de salida del router | Microsegundos a milisegundos (variable, depende de la congestión) |
| **Retardo de transmisión** | d_trans | Tiempo para empujar todos los bits del paquete al enlace: **L/R** | Microsegundos a milisegundos |
| **Retardo de propagación** | d_prop | Tiempo para que el bit viaje por el medio físico: **d/s** | Milisegundos a cientos de ms |

**d_trans vs d_prop — son muy diferentes:**
- d_trans depende de L (tamaño del paquete) y R (velocidad del enlace). No depende de la distancia.
- d_prop depende de d (distancia) y s (velocidad de propagación, ≈ 2×10⁸ m/s). No depende del tamaño del paquete.

### Analogía de la Caravana de Autos

Esta analogía del libro es clásica y muy útil para distinguir transmisión de propagación:

- Auto ↔ bit
- Caravana (10 autos) ↔ paquete (10 bits)
- Cabina de peaje ↔ router (enlace)
- Tiempo que tarda el peaje en atender un auto ↔ tiempo de transmisión de 1 bit

**Datos:**
- Peaje: 12 segundos por auto
- Velocidad de viaje: 100 km/h
- Distancia entre peajes: 100 km

**Tiempo de transmisión** (meter toda la caravana en la carretera):
```
10 autos × 12 seg/auto = 120 segundos = 2 minutos
```

**Tiempo de propagación** (el último auto viaja 100 km a 100 km/h):
```
100 km / 100 km/h = 1 hora = 60 minutos
```

**Tiempo total** hasta que toda la caravana está frente al segundo peaje:
```
2 min (transmisión) + 60 min (propagación) = 62 minutos
```

**Lección:** Aunque la transmisión termina rápido (2 min), la propagación domina en este caso. En redes de alta velocidad puede ocurrir lo inverso.

### Retardo de Cola y Traffic Intensity

El retardo de cola es la componente más variable e impredecible.

```
Traffic Intensity = La/R
```

Donde:
- `L` = longitud del paquete en bits
- `a` = tasa promedio de llegada de paquetes (paquetes/segundo)
- `R` = capacidad del enlace (bits/segundo)
- `La` = tasa de llegada de bits

| Traffic Intensity (La/R) | Comportamiento |
|--------------------------|----------------|
| La/R ≈ 0 | Cola casi vacía, retardo de cola ≈ 0 |
| La/R → 1 | Cola crece, retardo de cola crece rápidamente |
| La/R > 1 | Llegan más bits de los que se pueden transmitir → cola crece indefinidamente → retardo infinito y pérdidas |

**Regla práctica:** Diseñar redes para que La/R sea bajo (< 0.7–0.8).

### Traceroute

Herramienta para medir el retardo real en Internet:

1. Envía 3 paquetes a cada router en el camino al destino, con TTL = i (router i los devuelve).
2. Mide el tiempo de ida y vuelta para cada router.
3. Muestra la ruta completa y los retardos de cada salto.

Los retardos no siempre crecen monótonamente porque diferentes paquetes pueden tomar rutas distintas y hay variabilidad de carga.

### Pérdida de Paquetes

El buffer de un router tiene **capacidad finita**. Si llega un paquete y el buffer está lleno → el paquete se **descarta (drop)**. El paquete perdido puede ser retransmitido por el nodo anterior, por el host origen (TCP lo hace), o no ser retransmitido (UDP no lo hace).

### Throughput (Rendimiento)

El **throughput** es la tasa a la que bits se transfieren efectivamente entre emisor y receptor.

- **Throughput instantáneo:** tasa en un momento dado.
- **Throughput promedio:** tasa promedio durante un período.

**Enlace cuello de botella (bottleneck link):** el enlace en el camino extremo a extremo que tiene la menor capacidad. Es quien limita el throughput total.

```
Throughput = min(R_s, R_c)
```

Donde R_s es la capacidad del servidor y R_c es la capacidad del cliente.

**Escenario con múltiples flujos:**
Con 10 conexiones TCP compartiendo un enlace de backbone de capacidad R y links de servidor/cliente R_s y R_c:

```
Throughput por conexión = min(R_s, R_c, R/10)
```

En la práctica, el cuello de botella suele ser el enlace de acceso del cliente (R_c) o el del servidor (R_s), no el backbone.

---

## 9. Seguridad en Redes

Internet no fue diseñado originalmente con seguridad en mente. La visión original era "usuarios que se confían mutuamente". Hoy la seguridad es una preocupación en **todas las capas**.

### Ataques principales

#### Packet Sniffing (Escucha de paquetes)

En medios broadcast (Ethernet compartida, WiFi), una interfaz de red en modo **promiscuo** puede leer y registrar **todos** los paquetes que pasan, incluyendo contraseñas en texto claro. Herramienta: **Wireshark**.

**Defensa:** Cifrado de extremo a extremo (TLS, HTTPS).

#### IP Spoofing (Suplantación de IP)

Inyección de paquetes con una **dirección IP de origen falsa**. El receptor cree que el paquete viene de quien no es.

**Defensa:** Filtros de ingress en los routers (verificar que el origen sea coherente con la interfaz de llegada).

#### DoS (Denial of Service) y DDoS (Distributed DoS)

El atacante satura un recurso (servidor, enlace) con **tráfico basura** hasta que queda inaccesible para el tráfico legítimo.

- **DoS:** desde un solo host.
- **DDoS:** desde múltiples hosts comprometidos (**botnet**).

**Pasos de un DDoS:**
1. Seleccionar el objetivo.
2. Comprometer hosts en la red (infectarlos, formar botnet).
3. Dirigir la botnet para inundar el objetivo.

**Defensa:** Filtros en routers/firewalls que detectan y bloquean tráfico anormal.

### Líneas de Defensa

| Mecanismo | Descripción |
|-----------|-------------|
| **Autenticación** | Verificar la identidad (¿eres quien dices ser?). Ejemplo: SIM en redes celulares; contraseñas + 2FA en Internet. |
| **Confidencialidad** | Cifrado para que solo el destinatario pueda leer los datos. Protocolos: TLS, HTTPS, VPN. |
| **Integridad** | Verificar que los datos no fueron modificados. Mecanismos: firmas digitales, funciones hash. |
| **Restricciones de acceso** | Limitar quién puede conectarse. Ejemplo: VPNs con contraseña. |
| **Firewalls** | Middleboxes especializados que filtran tráfico según reglas (off-by-default: bloquear todo excepto lo explícitamente permitido). Detectan y reaccionan ante ataques DoS. |

---

## 10. Capas de Protocolo y Encapsulación

### ¿Por qué usar capas?

Las redes son sistemas complejos con muchas piezas (hosts, routers, medios, aplicaciones, protocolos). Las capas permiten:

- **Estructura clara:** cada capa tiene una función bien definida.
- **Modularidad:** cambiar la implementación de una capa (ej: reemplazar Ethernet por WiFi) es transparente para las capas superiores.
- **Identificación de relaciones:** cada capa usa los servicios de la capa inferior y provee servicios a la capa superior.

**Analogía del viaje aéreo:** Hay servicios de boleto, equipaje, puerta, pista, ruta aérea. Cada uno es independiente y se puede cambiar sin afectar a los demás (cambiar el proceso de boletos no afecta cómo se maneja el equipaje).

### El Stack de Protocolos de Internet (5 capas)

```
┌─────────────────────┐
│    Aplicación       │  HTTP, SMTP, DNS, FTP
├─────────────────────┤
│    Transporte       │  TCP, UDP
├─────────────────────┤
│    Red (Network)    │  IP, protocolos de enrutamiento
├─────────────────────┤
│    Enlace (Link)    │  Ethernet, WiFi (802.11), PPP
├─────────────────────┤
│    Física           │  bits "en el cable"
└─────────────────────┘
```

| Capa | Función | Unidad de datos | Protocolos |
|------|---------|-----------------|------------|
| **Aplicación** | Soporte a aplicaciones de red (qué y cómo se comunican los procesos) | Mensaje | HTTP, SMTP, DNS, FTP, IMAP |
| **Transporte** | Transferencia de datos proceso a proceso | Segmento | TCP, UDP |
| **Red** | Enrutamiento de datagramas desde origen al destino | Datagrama | IP, OSPF, BGP |
| **Enlace** | Transferencia de datos entre nodos vecinos directamente conectados | Frame (trama) | Ethernet, WiFi, PPP |
| **Física** | Bits en el medio físico | Bits | Varía por medio |

### Encapsulación

La **encapsulación** es el proceso de agregar una cabecera (header) a los datos de cada capa al bajar por el stack en el emisor. La **desencapsulación** es el proceso inverso en el receptor.

```
Aplicación:    [ Mensaje M                          ]
               Transporte agrega H_t
Transporte:    [ H_t | M                            ]  ← Segmento
               Red agrega H_n
Red:           [ H_n | H_t | M                      ]  ← Datagrama
               Enlace agrega H_l
Enlace:        [ H_l | H_n | H_t | M                ]  ← Frame
               Física: señales
```

**Rol de los dispositivos intermedios:**
- **Switches (capa de enlace):** procesan y reenvían frames — ven hasta la capa de enlace.
- **Routers (capa de red):** desencapsulan hasta la capa de red, leen la IP destino, y reencapsulan para el siguiente salto — ven hasta la capa de red. No ven TCP/UDP ni HTTP.
- **Hosts (origen y destino):** implementan todas las capas.

### Modelo OSI vs. Internet

El modelo de referencia **OSI/ISO** tiene **7 capas**, agregando:
- **Presentación:** interpretación del significado de los datos (cifrado, compresión, conversión de formato).
- **Sesión:** sincronización, checkpointing y recuperación del intercambio de datos.

El stack de Internet de 5 capas **no incluye estas dos**. Si se necesitan esas funciones (como cifrado), deben implementarse en la **capa de aplicación** (como hace TLS).

---

## 11. Historia de Internet

### Cronología

| Período | Hitos |
|---------|-------|
| **1961–1972:** Primeros principios de packet switching | 1961: Kleinrock demuestra la eficiencia del packet switching con teoría de colas. 1964: Baran propone packet switching para redes militares. 1967: ARPAnet concebido. 1969: primer nodo ARPAnet operativo. 1972: demo pública de ARPAnet, primer protocolo host-host (NCP), primer programa de email, 15 nodos. |
| **1972–1980:** Internetworking | 1974: Cerf y Kahn definen la arquitectura para interconectar redes (TCP/IP). Principios: minimalismo, best-effort, stateless routing, control descentralizado. 1976: Ethernet en Xerox PARC. 1979: ARPAnet tiene 200 nodos. |
| **1980–1990:** Nuevos protocolos, proliferación de redes | 1983: despliegue de TCP/IP. 1982: SMTP. 1983: DNS. 1985: FTP. 1988: control de congestión TCP. 100,000 hosts conectados. |
| **1990–2000:** Comercialización, la Web | 1991: NSF levanta restricciones de uso comercial. Berners-Lee inventa HTML y HTTP (1989-1991). 1994: Mosaic, luego Netscape. Boom comercial de la Web. Finales de los 90: IM, P2P. |
| **2005–presente:** Escala, SDN, movilidad, nube | Broadband masivo, smartphones dominan (más móviles que fijos en 2017), ~18B dispositivos. 2008: SDN. Google, Facebook crean sus propias redes. Servicios en la nube (AWS, Azure). |

**Principios de Cerf y Kahn (1974)** — definen la arquitectura de Internet moderna:
- Minimalismo y autonomía: no se requieren cambios internos a las redes para interconectarlas.
- Modelo de servicio best-effort.
- Routing stateless.
- Control descentralizado.

---

## 12. Resumen Rápido y Tablas de Referencia

### Componentes de Internet

| Componente | Descripción | Ejemplos |
|------------|-------------|---------|
| Hosts (end systems) | Ejecutan aplicaciones en el borde | PC, smartphones, servidores |
| Packet switches | Reenvían paquetes | Routers, switches |
| Communication links | Conectan switches y hosts | Fibra, cobre, radio, satélite |
| Networks | Colección de dispositivos gestionada por una organización | Red empresarial, red hogareña |
| ISPs | Proveen acceso a Internet | AT&T, Movistar, Claro |

### Los Cuatro Retardos

| Retardo | Fórmula | Depende de |
|---------|---------|------------|
| Procesamiento | d_proc | Velocidad del hardware del router |
| Cola | d_queue = variable | Tráfico (La/R) |
| Transmisión | **d_trans = L/R** | Tamaño del paquete L y velocidad del enlace R |
| Propagación | **d_prop = d/s** | Distancia d y velocidad del medio s |

### Circuit Switching vs. Packet Switching

| | Circuit Switching | Packet Switching |
|--|-------------------|-----------------|
| Recursos | Dedicados y reservados | Compartidos (bajo demanda) |
| Garantías | Sí (ancho de banda garantizado) | No |
| Desperdicio | Sí (circuito ocioso) | No |
| Congestion | No posible (si hay circuito) | Posible |
| Overhead | Setup de llamada | Cabeceras por paquete |
| Uso principal | Telefonía tradicional | Internet |

### Fórmulas Clave

| Concepto | Fórmula |
|----------|---------|
| Tiempo de transmisión | `d_trans = L (bits) / R (bps)` |
| Retardo de propagación | `d_prop = d (metros) / s (m/s)` |
| Retardo extremo a extremo (N enlaces, sin cola) | `d = N × L/R` |
| Traffic intensity | `I = La / R` |
| Throughput extremo a extremo | `min(R_s, R_c)` o `min(R_s, R_c, R/N)` con N flujos |

### Redes de Acceso Comparadas

| Tipo | Velocidad bajada | Velocidad subida | Compartida |
|------|-----------------|-----------------|------------|
| Cable (HFC) | 40 Mbps – 1.2 Gbps | 30–100 Mbps | Sí (vecinos) |
| DSL | 24–52 Mbps | 3.5–16 Mbps | No (línea dedicada) |
| WiFi (802.11n) | hasta 450 Mbps | hasta 450 Mbps | Sí (usuarios del AP) |
| 4G | decenas de Mbps | decenas de Mbps | Sí (celda) |
| Ethernet empresarial | 100 Mbps – 10 Gbps | 100 Mbps – 10 Gbps | No (conmutado) |

### Stack de Protocolos

| Capa | Unidad | Protocolos | Dispositivos |
|------|--------|------------|-------------|
| Aplicación | Mensaje | HTTP, DNS, SMTP | Hosts |
| Transporte | Segmento | TCP, UDP | Hosts |
| Red | Datagrama | IP, OSPF, BGP | Hosts, Routers |
| Enlace | Frame | Ethernet, WiFi | Hosts, Routers, Switches |
| Física | Bits | — | Todo |

### Ataques y Defensas

| Ataque | Descripción | Defensa |
|--------|-------------|---------|
| Sniffing | Captura de paquetes en medio broadcast | Cifrado (TLS/HTTPS) |
| IP Spoofing | Paquetes con IP de origen falsa | Ingress filtering en routers |
| DoS / DDoS | Saturación de recursos con tráfico basura | Firewalls, rate limiting, filtros |

### Temas Frecuentes de Certamen

1. **¿Qué es un protocolo?** Definición formal: formato + orden de mensajes + acciones. Ejemplo de protocolo humano vs. protocolo de red.
2. **Packet switching vs. circuit switching:** Ventajas y desventajas de cada uno. Ejemplo numérico de cuántos usuarios soporta cada enfoque.
3. **Los cuatro tipos de retardo:** Fórmulas de d_trans y d_prop, cuándo domina cada uno. Analogía de la caravana.
4. **Traffic intensity:** Interpretar La/R en tres rangos (≈0, →1, >1) y su efecto en el retardo de cola.
5. **Throughput y bottleneck link:** Calcular el throughput dado un camino con múltiples enlaces de distintas capacidades.
6. **Tipos de redes de acceso:** Diferencia entre HFC y DSL (compartida vs. dedicada). Velocidades aproximadas.
7. **Estructura de Internet:** Tier-1 ISPs, ISPs regionales, ISPs de acceso, IXPs, redes de content providers. ¿Por qué no conectar todos directamente?
8. **Encapsulación:** Cómo se llama la unidad de datos en cada capa (mensaje, segmento, datagrama, frame). Qué agrega cada capa.
9. **Papel de los routers y switches:** Hasta qué capa procesan cada tipo de dispositivo.
10. **Seguridad:** Describir sniffing, IP spoofing y DoS. Las cinco líneas de defensa.
11. **FDM vs. TDM:** Diferencia entre los dos enfoques de multiplexación en circuit switching.
12. **Modelo OSI vs. Internet:** Por qué Internet tiene 5 capas y no 7 como OSI.

---

*Basado en: Computer Networking: A Top-Down Approach, 8ª edición — Jim Kurose, Keith Ross, Pearson 2020.*
