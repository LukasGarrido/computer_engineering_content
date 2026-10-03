# Resumen Integrado — Capítulos 5, 6 y 8
### Redes de Computadores — Kurose & Ross, 8ª ed.

---

## Índice

1. [Capítulo 5 — Plano de Control](#capítulo-5--plano-de-control)
2. [Capítulo 6 — Capa de Enlace y LANs](#capítulo-6--capa-de-enlace-y-lans)
3. [Capítulo 8 — Seguridad en Redes](#capítulo-8--seguridad-en-redes)
4. [Preguntas Tipo Certamen — Cap. 5](#preguntas-tipo-certamen--cap-5)
5. [Preguntas Tipo Certamen — Cap. 6](#preguntas-tipo-certamen--cap-6)
6. [Preguntas Tipo Certamen — Cap. 8](#preguntas-tipo-certamen--cap-8)
7. [Tabla Comparativa Integradora](#tabla-comparativa-integradora)

---

# Capítulo 5 — Plano de Control

## 1. Plano de Datos vs. Plano de Control

| | Plano de Datos (Cap. 4) | Plano de Control (Cap. 5) |
|---|---|---|
| ¿Qué hace? | Mueve el paquete del puerto de entrada al de salida (forwarding) | Calcula las rutas extremo a extremo (routing) |
| Alcance | Local (dentro de un router) | Global (toda la red) |
| Velocidad | Nanosegundos (hardware) | Milisegundos (software) |

**Dos enfoques:** per-router control (tradicional, distribuido — cada router calcula su propia tabla) vs. SDN (centralizado — un controlador externo calcula todo e instala las tablas en los switches).

---

## 2. Algoritmos de Enrutamiento

La red se modela como **grafo**: nodos = routers, aristas = enlaces, peso = costo del enlace.

| Criterio | Link State (LS) | Distance Vector (DV) |
|---|---|---|
| Información | Topología completa conocida por todos | Solo vecinos directos |
| Comunicación | Broadcast a todos | Solo a vecinos |
| Convergencia | Más rápida | Más lenta |
| Problema | Oscilaciones con costos variables | Count-to-infinity |
| Protocolo real | OSPF, IS-IS | RIP (obsoleto), BGP (variante) |

---

## 3. Dijkstra — Link State

**Idea:** todos los nodos conocen la topología completa → cada uno corre Dijkstra localmente.

**Notación:**
- `c(x,y)` = costo del enlace x-y (∞ si no son vecinos)
- `D(v)` = estimación actual del costo mínimo desde origen hasta v
- `N'` = conjunto de nodos ya resueltos definitivamente

**Algoritmo:**
```
Inicializar: N' = {u}, D(v) = c(u,v) si vecino, sino ∞

Repetir hasta que N' = todos los nodos:
  1. Tomar w ∉ N' con menor D(w)
  2. Agregar w a N'
  3. Para cada vecino v de w, v ∉ N':
       D(v) = min(D(v), D(w) + c(w,v))
```

**Complejidad:** O(n²) básico, O(n log n) con heaps. Mensajes: O(n²).

**Problema — oscilaciones:** si el costo depende del tráfico (congestión), todos recalculan a la vez y se mueven en masa a otra ruta, congestionándola. **Solución:** aleatorizar el momento del cálculo.

---

## 4. Bellman-Ford — Distance Vector

**Ecuación fundamental:**
```
dx(y) = min sobre vecinos v { c(x,v) + dv(y) }
```

**Operación:** cada nodo espera un cambio (local o mensaje de vecino), recalcula su vector, y notifica a sus vecinos si algo cambió. **Asíncrono, iterativo, distribuido, autodetenido.**

**Problema — count-to-infinity:** cuando un enlace cae, dos nodos pueden "enganarse" mutuamente con info obsoleta, incrementando el costo indefinidamente. **Solución:** Poisoned Reverse — si z usa a y para llegar a x, z le dice a y que su distancia a x es ∞.

---

## 5. Sistemas Autónomos (AS)

Internet no puede tener una tabla de enrutamiento plana para todos los destinos — no escala. La solución es agrupar routers en **AS (Sistemas Autónomos)**.

```
Enrutamiento INTRA-AS: dentro del AS → protocolo único → prioridad: RENDIMIENTO
Enrutamiento INTER-AS: entre AS → BGP → prioridad: POLÍTICA y NEGOCIO
```

**Gateway routers:** routers en el borde del AS que conectan con otros AS y participan en inter-AS.

---

## 6. OSPF — Intra-AS

- Usa **Link State (Dijkstra)** dentro del AS
- Cada router difunde su estado de enlace a **todos** los routers del AS
- Jerárquico: **áreas locales** (inundación limitada al área) + **Backbone / Área 0** (conecta todas las áreas)
- Ventaja: routers solo necesitan mapa detallado de su área → tablas más pequeñas

---

## 7. BGP — Inter-AS

**BGP** es el "pegamento de Internet". Orientado a **políticas**, no solo a rendimiento.

**eBGP:** entre AS distintos (aprende rutas externas).
**iBGP:** dentro del mismo AS (propaga internamente lo que aprendió eBGP).

**Atributos clave:**
- **AS-PATH:** lista de AS atravesados → detecta loops, se prefiere el más corto
- **NEXT-HOP:** IP del próximo router hacia el destino

**Selección de ruta (orden de prioridad):**
1. Preferencia local (política del administrador) — máxima prioridad
2. AS-PATH más corto
3. Hot potato routing (menor costo intradominio hasta el punto de salida)
4. Criterios de desempate adicionales

**Hot Potato Routing:** salir del AS lo antes posible por el punto de salida con menor costo interno, sin importar el costo inter-AS.

**Mensajes BGP** (sobre conexión TCP semi-permanente):
- OPEN: abre sesión y autentica
- UPDATE: anuncia nueva ruta o retira una existente
- KEEPALIVE: mantiene la sesión viva
- NOTIFICATION: informa errores y cierra la conexión

---

## 8. SDN

**Problema del enfoque tradicional:**
- No se puede elegir una ruta específica para un flujo sin afectar todo el tráfico
- Load balancing entre dos rutas: imposible con routing tradicional
- Diferenciar tráfico por tipo (no solo por destino): imposible

**Solución SDN — tres componentes:**

```
┌─────────────────────────────────────┐
│     Aplicaciones de control         │  ← lógica: routing, firewall, LB
├─────────────────────────────────────┤
│       Controlador SDN               │  ← "SO de red", visión global
│  (northbound API + southbound API)   │
├──────────┬──────────┬───────────────┤
│ Switch 1 │ Switch 2 │   Switch 3    │  ← solo forwarding (hardware)
└──────────┴──────────┴───────────────┘
```

**OpenFlow** (southbound API):
- Controlador → Switch: `modify-state` (instala reglas), `packet-out`
- Switch → Controlador: `packet-in` (no tiene regla), `port-status`

---

## 9. ICMP

Protocolo de mensajes de control de la capa de red. Viaja **dentro de datagramas IP**.

| Tipo | Código | Función |
|---|---|---|
| 0 | 0 | Echo reply (respuesta ping) |
| 8 | 0 | Echo request (ping) |
| 3 | 0/1/3 | Destino inalcanzable (red/host/puerto) |
| 11 | 0 | TTL expirado → usado por traceroute |

**traceroute:** envía UDP con TTL=1, 2, 3... → cada router decrementa TTL a 0 → responde con ICMP tipo 11 → el origen descubre la ruta salto a salto.

---

## 10. Gestión de Red

| | SNMP | NETCONF/YANG |
|---|---|---|
| Objetivo | Monitoreo, consulta de variables | Configuración activa coordinada |
| Alcance | Un dispositivo a la vez | Múltiples dispositivos simultáneos |
| Transacciones | No atómicas | Atómicas (todo o nada) |
| Lenguaje | ASN.1 | XML / YANG |

**SNMP Traps:** el agente notifica proactivamente al servidor cuando ocurre un evento (ej: enlace caído) sin que se le haya preguntado.

---

# Capítulo 6 — Capa de Enlace y LANs

## 1. Introducción

La capa de enlace mueve datagramas entre **nodos físicamente adyacentes** (no extremo a extremo). Su unidad es el **frame**. Se implementa en la **NIC** (hardware + firmware + software).

**Servicios:** framing + acceso al canal (MAC), entrega confiable opcional, control de flujo, detección/corrección de errores, half/full-duplex.

**Por qué fiabilidad en enlace Y en TCP:** son escalas distintas. La fiabilidad de enlace corrige errores localmente (rápido, eficiente). TCP garantiza todo el recorrido extremo a extremo. No son redundantes — son complementarias.

---

## 2. Detección y Corrección de Errores

Esquema: `[D | EDC]` — D son los datos, EDC son bits redundantes calculados de D. Campos EDC más grandes → 2ⁿ huellas posibles → menor probabilidad de error no detectado.

| Técnica | Bits EDC | Detecta | Corrige | Uso |
|---|---|---|---|---|
| Paridad simple | 1 bit | Errores impares de bits | Nada | Simple, legacy |
| Paridad 2D | 1/fila + 1/col | Casi todos de 1 bit | 1 bit (intersección fila/col) | Educativo |
| Checksum | 16 bits | Mayoría | Nada | UDP, TCP, IP |
| CRC | 32 bits | Todas las ráfagas < r+1 bits | Nada | Ethernet, WiFi |

**CRC:** `R = resto de (D·2^r ÷ G)`. Receptor divide `<D',R'>` entre G → si resto=0 OK, sino error.

---

## 3. Protocolos de Acceso Múltiple (MAC)

Necesarios en canales broadcast. Tres categorías:

**Partición de canal** (sin colisiones, ineficiente a baja carga):
- TDMA: ranuras de tiempo fijas por estación
- FDMA: bandas de frecuencia fijas por estación

**Acceso aleatorio** (colisiones posibles, eficiente a baja carga):
- Slotted ALOHA: eficiencia máx. ≈ 1/e ≈ **37%**
- Pure ALOHA: eficiencia máx. ≈ **18%**
- CSMA: "escucha antes de transmitir"
- **CSMA/CD** (Ethernet): detecta colisión → aborta → backoff exponencial binario → reintenta. Eficiencia = 1/(1 + 5·t_prop/t_trans)

**Tomando turnos** (mejor de ambos mundos, pero punto único de falla):
- Polling: maestro/esclavos
- Token Passing: Bluetooth, Token Ring

---

## 4. Direccionamiento MAC y ARP

**MAC** (48 bits, hexadecimal, fija al hardware, asignada por IEEE):
- Analogía: número de Seguro Social (no cambia al moverse)
- Broadcast: `FF-FF-FF-FF-FF-FF`

**IP** (32 bits, depende de la subred):
- Analogía: dirección postal (cambia si te mudas)

**ARP** (traduce IP → MAC dentro de la misma LAN):
1. Query en **broadcast:** "¿quién tiene la IP X?"
2. Reply en **unicast:** "soy yo, mi MAC es Y"
3. Se guarda en tabla ARP con TTL (~20 min)

**Enrutamiento entre subredes:**
- **IP nunca cambia** en todo el viaje (extremo a extremo)
- **MAC cambia en cada salto** (local, salto a salto)
- Cada router desencapsula el frame, extrae el datagrama intacto, y crea un frame nuevo con nuevas MACs

---

## 5. Ethernet

Tecnología LAN dominante (10 Mbps → 400 Gbps). Topología bus (legacy) → switched (actual, sin colisiones).

**Estructura del frame:**
```
Preámbulo(8B) | MAC dest(6B) | MAC orig(6B) | Tipo(2B) | Datos(46-1500B) | CRC(4B)
```

**Sin conexión** (no hay handshaking) y **no confiable** (sin ACK/NAK; errores = descarte silencioso). Recuperación delegada a TCP. MAC protocol: CSMA/CD.

---

## 6. Switches

Dispositivo de **capa 2**: store-and-forward, examina MAC destino. **Transparente** y **plug-and-play** (auto-aprendizaje).

**Self-learning:** aprende (MAC, puerto, timestamp) observando la MAC origen de cada frame entrante.

**Forwarding:** conoce destino → envío selectivo al puerto correspondiente; no conoce → flooding (todos los puertos excepto el de entrada).

**Switch vs Router:**

| | Switch | Router |
|---|---|---|
| Capa | 2 | 3 |
| Examina | MAC destino | IP destino |
| Aprende | Por flooding/observación | Algoritmos de routing |

---

## 7. VLANs

**Problemas que resuelven:** escalabilidad (broadcast cruza toda la LAN), seguridad/privacidad, administración (mover usuarios sin mover cables).

**VLAN por puerto:** cada VLAN = su propio **dominio de broadcast**. Comunicación entre VLANs → obligatoriamente pasa por un **router** (o switch L3).

```
Dominio de COLISIÓN   → lo separa cualquier switch (con o sin VLANs)
Dominio de BROADCAST  → lo separan las VLANs y los routers
```

**Trunk ports + 802.1Q:** un solo cable físico transporta múltiples VLANs. El frame 802.1Q añade 4 bytes: TPID (`0x8100`) + 12 bits VLAN ID (hasta 4096 VLANs) + 3 bits de prioridad.

---

## 8. MPLS

Reenvío usando **etiquetas de 20 bits** (no longest-prefix-match IP). El datagrama IP permanece intacto. Los LSR (Label-Switched Routers) reenvían **solo por la etiqueta**.

**Ventajas:** traffic engineering (rutas distintas según origen+destino) y fast reroute (rutas de respaldo precalculadas).

---

## 9. Un Día en la Vida de una Solicitud Web

Orden real de protocolos al visitar una página:
1. **DHCP** → obtiene IP propia, gateway, DNS
2. **ARP** → obtiene MAC del router
3. **DNS** → resuelve nombre → IP del servidor
4. **TCP** → 3-way handshake (SYN, SYN-ACK, ACK)
5. **HTTP** → GET request → respuesta → página renderizada

---

# Capítulo 8 — Seguridad en Redes

## 1. Los 4 Pilares

| Pilar | Qué garantiza |
|---|---|
| **Confidencialidad** | Solo emisor y receptor legítimo leen el mensaje |
| **Autenticación** | Verificar la identidad del otro extremo |
| **Integridad** | El mensaje no fue alterado en tránsito |
| **Disponibilidad** | El servicio sigue funcionando bajo ataque |

**Tipos de ataque:** eavesdrop (pasivo), inserción activa, IP spoofing, hijacking, DoS.

---

## 2. Criptografía Simétrica

Misma clave para cifrar y descifrar. **Problema:** ¿cómo se comparte la clave de forma segura?

| Algoritmo | Clave | Estado |
|---|---|---|
| DES | 56 bits | Obsoleto (roto en <1 día) |
| 3DES | ~168 bits efectivos | Transitorio |
| AES | 128/192/256 bits | Estándar actual |

---

## 3. Criptografía de Clave Pública (RSA)

Cada persona tiene **K+ (pública, todos la conocen)** y **K- (privada, solo el dueño)**.

```
Cifrar para Bob:    c = K+B(m)   → solo Bob puede descifrar con K-B
Firmar (Bob firma): s = K-B(m)  → cualquiera verifica con K+B
Propiedad RSA:      K-B(K+B(m)) = m = K+B(K-B(m))
```

**RSA es ~100x más lento que DES** → en práctica solo cifra la session key KS; los datos viajan cifrados con AES.

**Seguridad:** basada en la imposibilidad práctica de factorizar números de 2048 bits.

---

## 4. Firmas Digitales y Hash

**Hash criptográfico:** H(m) = huella de tamaño fijo. Propiedades: irreversible, resistente a colisiones.
- MD5: 128 bits (débil), SHA-1: 160 bits (débil), **SHA-256: estándar actual**

**Firma digital:**
```
Bob envía: m + K-B(H(m))
Alice verifica: K+B(K-B(H(m))) = H(m) y compara con H(m recibido)
→ garantiza autenticación + integridad + no repudiación
```

**CA (Certification Authority):** vincula identidad↔clave pública mediante un certificado firmado con K-CA. Soluciona el ataque MITM en intercambio de claves públicas.

---

## 5. Autenticación con Nonce (ap1.0 → ap5.0)

| Protocolo | Mecanismo | Falla porque |
|---|---|---|
| ap1.0 | "Soy Alice" | Cualquiera puede decirlo |
| ap2.0 | + IP origen | IP spoofing |
| ap3.0 | + contraseña | Replay attack |
| ap3.0 cifrado | + contraseña cifrada | Replay attack (igual, no hace falta descifrar) |
| ap4.0 | + nonce cifrado con KS | Requiere clave simétrica previa |
| ap5.0 | + nonce cifrado con K- | MITM si no hay CA |

**Nonce:** número aleatorio de un solo uso → previene replay attacks.

---

## 6. Email Seguro

**Solo confidencialidad:** cifrar KS con K+B, datos con KS (RSA solo para la clave, AES para los datos).

**Solo autenticación + integridad:** enviar m + K-A(H(m)).

**Todo junto (3 claves):**
```
1. K-A(H(m))           → firma (autenticación + integridad)
2. KS(m + firma)       → cifrado del mensaje (confidencialidad)
3. K+B(KS)             → cifrado de la clave de sesión
```

---

## 7. TLS — Seguridad en la Capa de Transporte

TLS = HTTPS (puerto 443). Provee confidencialidad, integridad y autenticación.

**4 claves derivadas del Master Secret:**
- Kc / Mc: cifrado y MAC del cliente al servidor
- Ks / Ms: cifrado y MAC del servidor al cliente

**TLS 1.3:**
- Solo 5 cipher suites (antes 37)
- Diffie-Hellman obligatorio
- **1 RTT** para establecer conexión
- **0-RTT** para sesiones previas → vulnerable a replay attacks (solo seguro para operaciones idempotentes como HTTP GET)

**Ataques en TLS y sus soluciones:**

| Ataque | Solución |
|---|---|
| Re-ordering | Números de secuencia TLS en el MAC |
| Replay | Nonces |
| Truncation attack | Tipo de registro (0=datos, 1=cierre) incluido en el MAC |

---

## 8. IPsec — Seguridad en la Capa de Red

Protege el tráfico a nivel de datagrama IP (toda la red, no solo una app).

| Modo | Cifra | Uso |
|---|---|---|
| Transporte | Solo el payload | Entre dos hosts |
| **Túnel** | **El datagrama IP completo** | **VPNs entre redes** |

**AH:** autenticación + integridad, sin cifrado.
**ESP:** autenticación + integridad + cifrado (el más usado).

**SA (Security Association):** canal seguro **unidireccional**. Contiene SPI, algoritmos y claves. Para comunicación bidireccional se necesitan **2 SAs**.

**SAD** (Security Association Database): almacena el estado de cada SA activa → "¿CÓMO proceso el paquete?"
**SPD** (Security Policy Database): define políticas → "¿QUÉ hago con este paquete?" → se consulta primero.

**IKE:** automatiza el establecimiento de SAs en 2 fases:
1. Establece canal seguro (IKE SA) para que las negociaciones siguientes sean privadas
2. Negocia las SAs de IPsec usando ese canal

---

## 9. Firewalls e IDS

**Stateless packet filtering:** filtra por encabezados (IP, puerto, flags TCP), paquete a paquete, sin contexto. Vulnerable: no puede saber si un ACK corresponde a una sesión legítima.

**Stateful packet filtering:** mantiene tabla de conexiones TCP activas. Bloquea paquetes sin contexto válido. Agrega la columna "check connection" a las ACL.

**Application gateway:** proxy de aplicación, filtra a nivel de datos de aplicación. Ejemplo: gateway Telnet autentica al usuario y establece dos conexiones separadas.

**IDS (Intrusion Detection System):** complementa al firewall con:
- **Deep packet inspection:** busca contenido malicioso en el payload
- **Correlación entre sesiones:** detecta port scanning, mapping, DoS por patrones de múltiples paquetes

---

# Preguntas Tipo Certamen — Cap. 5

**P1.** Un router R está en el AS2. Aprende la ruta hacia el prefijo X via eBGP de dos fuentes distintas: una con AS-PATH = "AS3, AS1, X" (costo intradominio hasta el punto de salida = 2) y otra con AS-PATH = "AS5, X" (costo intradominio hasta el punto de salida = 7). ¿Cuál ruta elige R y por qué?

**Respuesta:** R elige la ruta con AS-PATH = "AS3, AS1, X", aunque su costo interno sea menor la segunda. El orden de preferencia de BGP es: (1) preferencia local → (2) AS-PATH más corto → (3) hot potato. Si la preferencia local es igual para ambas rutas, se aplica AS-PATH: "AS5, X" tiene 1 salto de AS y "AS3, AS1, X" tiene 2. Por lo tanto R elige **"AS5, X"** (AS-PATH más corto). Hot potato solo aplica como tercer criterio de desempate.

---

**P2.** ¿Por qué el algoritmo de Dijkstra puede generar oscilaciones en la red y el Bellman-Ford no tiene este problema específico? ¿Cuál es el problema equivalente de Bellman-Ford?

**Respuesta:** Dijkstra oscila cuando los costos de los enlaces dependen del tráfico: todos los routers calculan simultáneamente con los costos actuales, se concentran en la ruta más barata, la congestiona, y en el siguiente ciclo todos se mueven en masa a otra ruta. Esto ocurre porque LS hace broadcast global y todos recalculan al mismo tiempo. Bellman-Ford no tiene este problema porque es asíncrono y no requiere que todos actúen en el mismo instante. El problema equivalente de DV es el **count-to-infinity**: cuando un enlace cae, dos nodos se "engansan" en un bucle de información obsoleta, incrementando el costo indefinidamente hasta infinito.

---

**P3.** Verdadero o Falso: "Un router de borde (gateway router) de un AS solo necesita ejecutar BGP, no OSPF, porque BGP maneja todo el enrutamiento."

**Respuesta: Falso.** Un gateway router ejecuta **ambos protocolos simultáneamente**: OSPF (intra-AS) para conocer las rutas dentro de su propio AS y calcular el costo interno hasta los puntos de salida, y BGP (inter-AS) para aprender las rutas externas de otros AS. Necesita OSPF, entre otras cosas, para aplicar correctamente el hot potato routing (que requiere conocer el costo intradominio hasta cada punto de salida).

---

**P4.** Explica la diferencia entre iBGP y eBGP. ¿Qué problema resuelve iBGP dentro de un AS?

**Respuesta:** eBGP es una sesión BGP entre routers de borde de **AS distintos** — es como dos organizaciones distintas comunicándose sobre qué destinos pueden alcanzar. iBGP es una sesión BGP entre routers **del mismo AS**. El problema que resuelve iBGP es que cuando un router de borde aprende una ruta externa via eBGP, los demás routers internos del AS no la conocen automáticamente (OSPF solo maneja rutas internas, no externas). iBGP propaga internamente esa información a todos los routers del AS para que cualquier router sepa cómo salir hacia destinos externos.

---

**P5.** En SDN, ¿qué ocurre cuando un paquete llega a un switch y no existe ninguna regla en su tabla de flujo que aplique? ¿Cómo se diferencia esto del comportamiento de un router tradicional en la misma situación?

**Respuesta:** En SDN, el switch envía el paquete al controlador mediante el mensaje **`packet-in`** de OpenFlow, esperando instrucciones. El controlador decide qué hacer (puede instalar una nueva regla con `modify-state` o reenviar el paquete con `packet-out`). En un router tradicional, si no existe entrada en la tabla de enrutamiento para el prefijo destino, el router simplemente **descarta el paquete** y puede enviar un ICMP "destination unreachable" al origen. La diferencia fundamental: el switch SDN "consulta" a una autoridad externa; el router tradicional toma la decisión localmente.

---

# Preguntas Tipo Certamen — Cap. 6

**P1.** Un switch recibe un frame de A destinado a B. La MAC de B no está en su tabla. Simultáneamente, otro frame llega destinado a C, cuya MAC sí está en la tabla (puerto 3). Describe exactamente qué hace el switch con cada frame y por qué.

**Respuesta:**
- **Frame hacia B (MAC desconocida):** el switch hace **flooding** — reenvía el frame por todos los puertos excepto el de entrada. Esto permite que B reciba el frame y, cuando responda, el switch aprenderá su MAC (observará que la respuesta sale del puerto donde está B).
- **Frame hacia C (MAC conocida):** el switch hace **envío selectivo** — reenvía únicamente por el puerto 3. Los demás hosts no reciben el frame.

Ambas operaciones pueden ocurrir **simultáneamente** si sus puertos de salida son distintos (esto es la ventaja del switch sobre el hub — permite múltiples transmisiones paralelas).

---

**P2.** Explica por qué en el enrutamiento entre subredes la dirección IP no cambia pero la MAC sí cambia en cada salto. Usa un ejemplo con A → R → B.

**Respuesta:** La dirección IP representa el destino **global final** (B) — es la información que los routers necesitan para tomar decisiones de enrutamiento. No tiene sentido cambiarla porque el destino real no cambia.

La MAC representa el destino **local e inmediato** en el tramo actual. Cuando A envía a R, el frame lleva MAC_R como destino (porque R es el vecino físico de A). R extrae el datagrama, lo examina, decide enviarlo hacia B, y construye un **nuevo frame** con MAC_B como destino. Si usara la misma MAC (MAC_R), B no sabría que el frame es para él.

```
Tramo A→R: [MAC_A → MAC_R | IP_A → IP_B | datos]  ← MAC de R como destino local
En R: desencapsula, crea frame nuevo
Tramo R→B: [MAC_R → MAC_B | IP_A → IP_B | datos]  ← MAC de B como destino local
IP_A e IP_B nunca cambiaron
```

---

**P3.** Verdadero o Falso: "Las VLANs separan dominios de colisión, lo que mejora la seguridad y eficiencia de la red."

**Respuesta: Falso (técnicamente).** Las VLANs separan **dominios de broadcast**, no dominios de colisión. Los dominios de colisión ya los separa cualquier switch — cada puerto es su propio dominio de colisión con o sin VLANs. Lo que las VLANs agregan es la separación de dominios de broadcast: un broadcast enviado en VLAN EE nunca llegará a los puertos de VLAN CS. Esto sí mejora la seguridad y eficiencia (al limitar el alcance del tráfico de difusión), pero el término correcto es **dominio de broadcast**.

---

**P4.** CRC detecta todos los errores en ráfaga menores a r+1 bits, pero no puede corregirlos. La paridad 2D puede corregir 1 bit de error pero detecta menos que CRC. ¿Por qué se usa CRC en Ethernet en lugar de paridad 2D si CRC no puede corregir errores?

**Respuesta:** En Ethernet no se necesita corrección de errores a nivel de enlace porque:
1. Los errores en cables de cobre/fibra son poco frecuentes — la detección es suficiente
2. Cuando se detecta un error, el frame simplemente se descarta y TCP (capa superior) se encarga de la retransmisión
3. CRC es mucho más eficiente en hardware (implementado con registros de desplazamiento y compuertas XOR) y puede calcularse a velocidades de 1-400 Gbps
4. CRC detecta una clase de errores mucho más amplia que la paridad 2D (especialmente ráfagas, que son los errores más comunes en transmisión)

La corrección de errores (como paridad 2D o códigos Hamming) se reserva para enlaces donde la retransmisión es muy costosa (alta latencia), como enlaces satelitales o inalámbricos.

---

**P5.** ¿Por qué ARP solo funciona dentro de la misma subred y qué mecanismo permite a un host comunicarse con un host en otra subred?

**Respuesta:** ARP usa broadcast (`FF-FF-FF-FF-FF-FF`) para preguntar "¿quién tiene esta IP?". Los routers **no reenvían broadcasts de capa 2** — actúan como barrera que delimita el dominio de broadcast. Por lo tanto, un ARP broadcast nunca llega a otra subred.

Para comunicarse con un host en otra subred, el proceso es:
1. El host emisor detecta que la IP destino está fuera de su subred (comparando con su máscara)
2. En lugar de hacer ARP hacia el destino final, hace ARP hacia su **gateway (router)**
3. Envía el frame al router (MAC del router como destino en el frame)
4. El router recibe el datagrama, consulta su tabla de enrutamiento, y lo reenvía hacia la siguiente subred — haciendo ARP hacia el siguiente salto en esa subred
5. El proceso se repite salto a salto hasta llegar al destino

---

# Preguntas Tipo Certamen — Cap. 8

**P1.** Alice envía a Bob el mensaje m junto con K-A(H(m)). Bob verifica la firma. Luego Trudy intercepta la comunicación y reemplaza m por m' (conservando K-A(H(m)) sin tocar). ¿Qué ocurre en la verificación de Bob y qué concluye?

**Respuesta:**
```
Bob recibe: m'  +  K-A(H(m))   (m fue reemplazado por m' por Trudy)

Verificación:
1. Bob calcula: K+A(K-A(H(m))) = H(m)   → obtiene el hash original
2. Bob calcula: H(m')                    → hash del mensaje recibido
3. Compara: H(m) ≠ H(m')                → ¡son distintos!
→ Bob concluye: el mensaje fue alterado → RECHAZA
```

La firma digital garantiza la integridad — Bob detecta cualquier modificación porque cambiar m sin tener K-A hace imposible generar un K-A(H(m')) que pase la verificación. Bob sabe que alguien alteró el mensaje, pero no puede saber quién fue ni qué decía el mensaje original.

---

**P2.** Explica por qué el modo 0-RTT de TLS 1.3 es vulnerable a replay attacks pero el modo 1-RTT no lo es. ¿En qué condición es seguro usar 0-RTT?

**Respuesta:**
- **1-RTT:** el handshake genera nonces frescos específicos de esa sesión. Cualquier intento de replay fallará porque los nonces serán distintos — el servidor rechazará el paquete al verificar el MAC.
- **0-RTT:** el cliente envía datos en el primer mensaje usando material criptográfico de una **sesión anterior** (resumption master secret). No se negocian nonces frescos antes de ese primer mensaje. Un atacante puede capturar ese primer mensaje y reenviarlo — el servidor lo procesará de nuevo porque no puede distinguirlo de una solicitud legítima.

**Condición para usar 0-RTT con seguridad:** solo en operaciones **idempotentes** que producen el mismo resultado si se ejecutan múltiples veces (ej: HTTP GET). Nunca en HTTP POST, transacciones bancarias u operaciones que modifican estado.

---

**P3.** ¿Por qué una Security Association (SA) en IPsec es unidireccional? ¿Qué implicaciones tiene esto para una VPN entre dos oficinas?

**Respuesta:** Una SA es unidireccional porque define el estado de seguridad (claves, algoritmos, SPI) para el tráfico que fluye en **una sola dirección**. Tener claves distintas para cada dirección es una mejor práctica criptográfica — si un atacante compromete la clave de una dirección, la comunicación en la otra dirección sigue segura.

Para una VPN entre la oficina A y la oficina B se necesitan **2 SAs**:
- SA1: de A hacia B (con sus propias claves y SPI)
- SA2: de B hacia A (con claves distintas y distinto SPI)

Esto implica también que el SAD de cada router mantiene entradas para ambas SAs, y que IKE debe negociar ambas durante su Fase 2.

---

**P4.** Un firewall stateless tiene la regla: "allow TCP desde exterior hacia interior, puerto destino 80". Un atacante envía un paquete TCP con puerto origen=80, puerto destino=4500, ACK=1, desde una IP externa. ¿Pasa el firewall? ¿Por qué es esto problemático y cómo lo resuelve un firewall stateful?

**Respuesta:** La regla especificada permite TCP con puerto **destino** 80, no con puerto origen 80. Este paquete tiene puerto destino 4500 → **no pasa** con esa regla específica.

Sin embargo, si existe también la regla típica "allow TCP desde exterior, puerto origen 80, ACK=1" (para permitir respuestas de servidores web externos), entonces el paquete del atacante **sí pasaría**, aunque no corresponda a ninguna conexión establecida. El firewall stateless no puede distinguirlo de una respuesta legítima.

Un **firewall stateful** resuelve esto verificando que exista una entrada en su tabla de conexiones activas que corresponda a ese paquete (misma IP origen/destino, puertos y estado de la sesión TCP). Si no existe → bloquea el paquete aunque sus campos encajen con una regla.

---

**P5.** Bob quiere garantizar confidencialidad, autenticación e integridad al enviarle un documento a Alice. Describe el proceso completo indicando qué claves usa y en qué orden. ¿Cuántas claves distintas se necesitan y de quién es cada una?

**Respuesta — 3 claves necesarias:**

| Clave | De quién | Para qué |
|---|---|---|
| K-B (privada de Bob) | Bob | Firma: garantiza autenticación + integridad |
| KS (simétrica temporal, generada aleatoriamente) | Nadie (creada para esta sesión) | Cifra el mensaje: garantiza confidencialidad eficiente |
| K+A (pública de Alice) | Alice (conocida por todos) | Cifra KS: solo Alice puede descifrarla |

**Proceso Bob (emisor):**
```
1. Calcula H(m)
2. Firma: K-B(H(m))
3. Concatena: m + K-B(H(m))
4. Genera KS aleatorio
5. Cifra el mensaje: KS( m + K-B(H(m)) )
6. Cifra la clave de sesión: K+A(KS)
7. Envía: KS(m + K-B(H(m))) + K+A(KS)
```

**Proceso Alice (receptora, orden inverso):**
```
1. Descifra K+A(KS) con K-A → obtiene KS
2. Descifra con KS → obtiene m + K-B(H(m))
3. Aplica K+B al hash firmado: K+B(K-B(H(m))) = H(m)
4. Calcula H(m recibido) y compara → si iguales: OK
```

---

# Tabla Comparativa Integradora

## Los tres capítulos en perspectiva de capa

| Capa | Cap | Función principal | Protocolo clave | Unidad de datos |
|---|---|---|---|---|
| Aplicación/Transporte | 8 | Seguridad extremo a extremo | TLS, IPsec | Segmento/Datagrama cifrado |
| Red (Control) | 5 | Calcular rutas globales | OSPF, BGP, SDN | Tablas de reenvío |
| Red (Datos) | 4 | Reenviar paquetes hop a hop | IP | Datagrama |
| Enlace | 6 | Transferir entre nodos adyacentes | Ethernet, WiFi | Frame |

## Conceptos que se repiten en los tres capítulos

| Concepto | Cap 5 | Cap 6 | Cap 8 |
|---|---|---|---|
| **Broadcast** | BGP flood de anuncios | Dominio de broadcast, ALOHA | ARP broadcast para autenticación WiFi |
| **Tabla de estado** | Tabla de enrutamiento, SAD | Tabla ARP, tabla switch | Tabla de conexiones (firewall stateful) |
| **Autenticación** | BGP entre pares | WPA3, 4G (implícito) | Toda la sección 3 |
| **Descentralizado vs centralizado** | Per-router vs SDN | Switch auto-aprendiz vs admin VLAN | Firewalls distribuidos vs controlador SDN |
| **Detección de errores** | Checksum en datagramas IP | CRC en frames Ethernet | MAC (Message Authentication Code) en TLS/IPsec |

---

## Trampas frecuentes de certamen (los tres capítulos)

| Afirmación incorrecta | Corrección |
|---|---|
| "OSPF usa Distance Vector" | OSPF usa Link State (Dijkstra) |
| "BGP elige siempre la ruta más corta en saltos" | BGP prioriza preferencia local → AS-PATH → hot potato |
| "iBGP y eBGP son protocolos distintos" | Son el mismo protocolo en roles distintos (inter-AS vs intra-AS) |
| "Las VLANs separan dominios de colisión" | Separan dominios de broadcast; los dominios de colisión los separa cualquier switch |
| "La IP cambia en cada salto del router" | La IP nunca cambia; la MAC sí cambia en cada salto |
| "Cifrar con K+ es una firma digital" | Firmar = cifrar con K- (privada). Cifrar para alguien = usar su K+ (pública) |
| "Una SA en IPsec es bidireccional" | Una SA es unidireccional; se necesitan 2 para comunicación bidireccional |
| "TLS 1.3 0-RTT es siempre seguro" | Solo seguro para operaciones idempotentes (HTTP GET); vulnerable a replay en operaciones con estado |
| "ARP funciona entre subredes distintas" | ARP es solo local (misma LAN/subred); los routers no reenvían broadcasts de capa 2 |
| "El checksum de Internet sirve como hash criptográfico" | No — es vulnerable a cancelaciones; no es resistente a colisiones intencionales |

---

*Basado en: Kurose, J.F. & Ross, K.W. — Computer Networking: A Top-Down Approach, 8ª Edición, Pearson 2020.*
