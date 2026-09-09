# Capítulo 2: Capa de Aplicación

### Computer Networking: A Top-Down Approach — Kurose & Ross, 8ª ed.

> Guía completa de estudio para certamen

---

## Índice

1. [Principios de las Aplicaciones de Red](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#1-principios-de-las-aplicaciones-de-red)
2. [Web y HTTP](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#2-web-y-http)
3. [Correo Electrónico: SMTP e IMAP](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#3-correo-electr%C3%B3nico-smtp-e-imap)
4. [DNS: Sistema de Nombres de Dominio](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#4-dns-sistema-de-nombres-de-dominio)
5. [Aplicaciones P2P y BitTorrent](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#5-aplicaciones-p2p-y-bittorrent)
6. [Video Streaming y CDNs](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#6-video-streaming-y-cdns)
7. [Programación de Sockets](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#7-programaci%C3%B3n-de-sockets)
8. [Resumen Rápido y Tablas de Referencia](https://claude.ai/chat/b4322633-96b6-4baf-95a1-6d41bbbc2185#8-resumen-r%C3%A1pido-y-tablas-de-referencia)

---

## 1. Principios de las Aplicaciones de Red

### ¿Qué es una aplicación de red?

Una aplicación de red consiste en programas que:

- Se ejecutan en **sistemas finales** (hosts) distintos — no en dispositivos del núcleo de la red (routers, switches).
- Se comunican entre sí a través de la red.

> **Clave:** Los dispositivos centrales de la red (routers) **no** ejecutan aplicaciones de usuario. Toda la lógica vive en los extremos. Esto permite desarrollar y desplegar aplicaciones sin tocar la infraestructura de red.

---

### Arquitecturas de Aplicación

#### Paradigma Cliente-Servidor

|Componente|Características|
|---|---|
|**Servidor**|Siempre activo, IP permanente, normalmente en centros de datos para escalar|
|**Clientes**|Contactan al servidor, pueden conectarse intermitentemente, pueden tener IP dinámica, **no se comunican entre sí directamente**|

**Ejemplos:** HTTP, IMAP, FTP.

#### Arquitectura Peer-to-Peer (P2P)

- **Sin servidor** siempre activo.
- Los sistemas finales arbitrarios (pares) se comunican **directamente** entre sí.
- Los nodos **solicitan y también proveen** servicio a otros pares.
- **Autoescalabilidad:** Cada nuevo nodo aporta tanto demanda como capacidad de servicio.
- Pares se conectan intermitentemente y cambian de IP → gestión compleja.
- **Ejemplos:** BitTorrent, VoIP (Skype), streaming P2P.

---

### Procesos y Sockets

**Proceso:** Programa en ejecución dentro de un host.

- En el mismo host: dos procesos se comunican mediante IPC (Inter-Process Communication, definido por el SO).
- En hosts distintos: los procesos se comunican intercambiando **mensajes** a través de la red.

**Socket:** La "puerta" entre el proceso de aplicación y el protocolo de transporte subyacente.

- El proceso emisor empuja el mensaje fuera por su socket.
- Depende de la infraestructura de transporte para entregar el mensaje al socket receptor.
- El desarrollador controla lo que hay **encima** del socket (la aplicación). El SO controla lo que hay **debajo** (TCP/UDP, IP).

**Identificación de procesos:**

- Una IP sola no basta (muchos procesos pueden correr en el mismo host).
- Se necesita **IP + número de puerto** para identificar un proceso específico.
- Ejemplos de puertos estándar: HTTP=80, HTTPS=443, SMTP=25, DNS=53.

---

### Requisitos de los Servicios de Transporte

Las aplicaciones difieren en qué necesitan de la capa de transporte:

|Dimensión|Descripción|Ejemplos|
|---|---|---|
|**Integridad de datos**|¿Toleran pérdidas?|FTP/email: sin pérdida. Audio/video: tolerante|
|**Throughput**|¿Necesitan ancho de banda mínimo?|Multimedia: sí. Apps elásticas: usan lo disponible|
|**Temporización**|¿Requieren baja latencia?|VoIP, juegos: decenas de ms. Descarga: no importa|
|**Seguridad**|¿Cifrado, integridad, autenticación?|Transacciones financieras: sí|

**Tabla de requisitos de aplicaciones comunes:**

|Aplicación|Pérdida de datos|Throughput|Sensible al tiempo|
|---|---|---|---|
|Transferencia/descarga de archivos|Sin pérdida|Elástico|No|
|E-mail|Sin pérdida|Elástico|No|
|Documentos web|Sin pérdida|Elástico|No|
|Audio/video tiempo real|Tolera pérdidas|5 Kbps–5 Mbps|Sí, decenas de ms|
|Streaming audio/video|Tolera pérdidas|5 Kbps–5 Mbps|Sí, pocos segundos|
|Juegos interactivos|Tolera pérdidas|Kbps+|Sí, decenas de ms|
|Mensajería de texto|Sin pérdida|Elástico|Sí y no|

---

### TCP vs. UDP

|Característica|TCP|UDP|
|---|---|---|
|Confiabilidad|Sí (retransmisiones)|No|
|Control de flujo|Sí (no satura al receptor)|No|
|Control de congestión|Sí (no satura la red)|No|
|Orientado a la conexión|Sí (requiere handshake)|No|
|Timing / retardo mínimo|No garantiza|No garantiza|
|Throughput mínimo|No garantiza|No garantiza|
|Seguridad nativa|No (usar TLS)|No|
|Overhead|Mayor (20 bytes cabecera)|Menor (8 bytes cabecera)|

**¿Por qué existe UDP si es "inferior"?**

- Sin handshake → sin latencia inicial (ideal para DNS, juegos, VoIP).
- Sin control de congestión → puede enviar a tasa constante aunque la red esté congestionada (útil para streaming en tiempo real donde pausar es peor que perder un frame).
- Sin estado de conexión → puede soportar más clientes simultáneos.

---

### TLS (Transport Layer Security)

TCP y UDP estándar no ofrecen cifrado: las contraseñas viajan en texto claro.

**TLS:** Implementado en la **capa de aplicación** (no en transporte):

- Las apps usan bibliotecas TLS, que a su vez usan TCP.
- Proporciona: conexiones TCP cifradas, integridad de datos, autenticación de punto final.
- Texto sin cifrar enviado al socket → viaja por Internet cifrado.

**Un protocolo de capa de aplicación define:**

- **Tipos de mensajes:** request, response.
- **Sintaxis:** qué campos tiene el mensaje y cómo se delimitan.
- **Semántica:** significado de los campos.
- **Reglas:** cuándo y cómo enviar/responder mensajes.

---

## 2. Web y HTTP

### Conceptos Básicos

- Una **página web** consiste en objetos (HTML base + imágenes, videos, scripts, etc.), cada uno almacenable en distintos servidores.
- Cada objeto es accesible por una **URL**: `www.someschool.edu/someDept/pic.gif` (host + path).
- **HTTP (HyperText Transfer Protocol):** protocolo de capa de aplicación de la web, cliente-servidor.
    - **Cliente:** navegador que solicita y muestra objetos.
    - **Servidor:** envía objetos en respuesta a solicitudes.

---

### HTTP y TCP

1. El cliente inicia una **conexión TCP** al servidor en el **puerto 80**.
2. El servidor acepta la conexión.
3. Se intercambian mensajes HTTP.
4. Se cierra la conexión TCP.

**HTTP es "sin estado" (stateless):**

- El servidor **no recuerda** solicitudes anteriores.
- Cada solicitud HTTP es completamente independiente.
- Ventaja: simplicidad, escalabilidad.
- Desventaja: para mantener estado (sesión, carrito de compras) se necesitan mecanismos extra (cookies).

---

### Conexiones HTTP: No Persistente vs. Persistente

#### HTTP No Persistente (HTTP/1.0)

1. Abrir conexión TCP.
2. Enviar **un solo objeto** por la conexión.
3. Cerrar la conexión TCP.
4. Repetir para cada objeto.

**Tiempo de respuesta por objeto:**

```
Tiempo total = 2 RTT + tiempo de transmisión del archivo
```

- 1 RTT para establecer la conexión TCP (SYN + SYN-ACK).
- 1 RTT para la solicitud HTTP y los primeros bytes de respuesta.
- Tiempo de transmisión del objeto.

**Problemas:**

- 2 RTTs por objeto → lento para páginas con muchos objetos.
- Overhead del SO por cada conexión TCP.
- Los navegadores compensan abriendo múltiples conexiones TCP en paralelo.

#### HTTP Persistente (HTTP/1.1)

- El servidor **deja la conexión abierta** después de enviar la respuesta.
- Múltiples objetos se envían por la **misma** conexión TCP.
- El cliente envía solicitudes tan pronto como encuentra un objeto referenciado (pipelining).
- Resultado: **tan solo 1 RTT para todos los objetos referenciados** (en vez de 2 RTTs × N objetos).

---

### Mensajes HTTP

#### Solicitud (Request)

Formato en ASCII (legible por humanos):

```
GET /index.html HTTP/1.1\r\n
Host: www-net.cs.umass.edu\r\n
User-Agent: Mozilla/5.0 ...\r\n
Accept: text/html,...\r\n
Connection: keep-alive\r\n
\r\n
```

- **Línea de solicitud:** método + URL + versión HTTP.
- **Líneas de cabecera:** pares clave-valor.
- **Línea en blanco** (`\r\n`): indica fin de cabeceras.
- **Cuerpo** (opcional, en POST).

**Métodos HTTP:**

|Método|Descripción|
|---|---|
|**GET**|Solicitar un recurso. Para enviar datos al servidor: incluir en la URL (`?clave=valor`).|
|**POST**|Enviar datos al servidor en el **cuerpo** del mensaje (formularios, login).|
|**HEAD**|Como GET pero el servidor responde solo con las cabeceras (sin cuerpo). Útil para verificar existencia o metadatos.|
|**PUT**|Subir un nuevo archivo (reemplaza el existente en la URL especificada).|

#### Respuesta (Response)

```
HTTP/1.1 200 OK\r\n
Date: Tue, 08 Sep 2020 00:53:20 GMT\r\n
Server: Apache/2.4.6\r\n
Content-Length: 2651\r\n
Content-Type: text/html; charset=UTF-8\r\n
\r\n
<datos del objeto>
```

**Códigos de estado HTTP más importantes:**

|Código|Significado|
|---|---|
|**200 OK**|Solicitud exitosa, objeto en el mensaje de respuesta.|
|**301 Moved Permanently**|El objeto fue movido, nueva URL en el campo `Location:`.|
|**304 Not Modified**|Usado en GET condicional: la copia en caché es válida.|
|**400 Bad Request**|El servidor no pudo entender la solicitud.|
|**404 Not Found**|El objeto no existe en este servidor.|
|**505 HTTP Version Not Supported**|El servidor no soporta la versión HTTP del cliente.|

---

### Cookies: Manteniendo Estado

HTTP es stateless, pero los sitios web necesitan recordar usuarios. Solución: **cookies**.

**Cuatro componentes del sistema de cookies:**

1. Línea `Set-Cookie:` en el mensaje de respuesta HTTP del servidor.
2. Línea `Cookie:` en el siguiente mensaje de solicitud del cliente.
3. Archivo de cookies almacenado en el host del usuario (gestionado por el navegador).
4. Base de datos en el servidor del sitio web.

**Funcionamiento (ejemplo: primera visita a amazon.com):**

```
1. Cliente envía solicitud HTTP normal (sin cookie).
2. Servidor crea ID único (ej: 1678), guarda en BD.
3. Servidor responde con: Set-Cookie: 1678
4. El navegador guarda la cookie.
5. En próximas solicitudes: Cookie: 1678  →  servidor identifica al usuario.
```

**Usos de las cookies:** Autenticación, carrito de compras, recomendaciones, estado de sesión.

**Privacidad:** Las cookies de terceros (_tracking cookies_) permiten rastrear al usuario a través de múltiples sitios web mediante el mismo valor de cookie.

---

### Web Caché (Proxy)

**Objetivo:** Satisfacer solicitudes del cliente sin involucrar al servidor de origen.

**Funcionamiento:**

1. El usuario configura su navegador para usar una caché web local.
2. El navegador envía **todas** las solicitudes HTTP a la caché.
3. Si el objeto está en caché → la caché lo devuelve directamente (baja latencia).
4. Si no está → la caché lo solicita al servidor de origen, lo almacena, y lo devuelve.

La caché actúa como **cliente** (frente al servidor de origen) y como **servidor** (frente al cliente que solicita).

**¿Por qué usar caché?**

- Reduce tiempo de respuesta al cliente (caché más cercana).
- Reduce tráfico en el enlace de acceso de la institución.
- Permite a proveedores con pocos recursos entregar contenido eficazmente.

**Ejemplo numérico de caché:**

Escenario: enlace de acceso = 1.54 Mbps, RTT al servidor = 2 s, tasa promedio = 1.50 Mbps.

- **Sin caché:** Utilización enlace = 1.50/1.54 = **0.97** → colas enormes, retardo de **minutos**.
- **Con caché** (hit rate = 0.4):
    - Solo el 60% del tráfico va al servidor de origen.
    - Tasa en enlace = 0.6 × 1.50 = 0.9 Mbps → Utilización = 0.9/1.54 = **0.58** → baja latencia.
    - Retardo promedio = 0.6 × 2.01 s + 0.4 × milisegundos ≈ **1.2 segundos**.
    - Mucho mejor que un enlace de 154 Mbps... ¡y más barato!

---

### GET Condicional

**Objetivo:** No enviar el objeto si la caché ya tiene una copia actualizada.

**Funcionamiento:**

1. Cliente incluye en la solicitud: `If-Modified-Since: <fecha de la copia en caché>`
2. Servidor verifica si el objeto fue modificado:
    - **No modificado:** Responde `HTTP/1.0 304 Not Modified` (sin cuerpo → ahorra ancho de banda).
    - **Modificado:** Responde `HTTP/1.0 200 OK` con el nuevo objeto.

---

### HTTP/2 y HTTP/3

#### HTTP/2 (RFC 7540, 2015)

**Problema de HTTP/1.1 con pipelining:** Responde en orden FCFS (first-come-first-served). Un objeto grande bloquea a los pequeños → **bloqueo HOL (Head-of-Line blocking)**.

**Soluciones de HTTP/2:**

- **Priorización de objetos:** El cliente especifica la prioridad de cada objeto (no necesariamente FCFS).
- **División en tramas (frames):** Los objetos se dividen en tramas más pequeñas. Las tramas de diferentes objetos se **intercalan** en la transmisión, mitigando el bloqueo HOL.
- **Server push:** El servidor puede enviar objetos no solicitados explícitamente que anticipa que el cliente necesitará.
- Métodos, códigos de estado y cabeceras sin cambios respecto a HTTP/1.1.

**Ejemplo HOL con HTTP/2:**

```
HTTP/1.1:  [O1 grande ─────────────] [O2] [O3] [O4]  ← O2,O3,O4 esperan
HTTP/2:    [O1-trama] [O2] [O3] [O4] [O1-trama] [O2]  ← objetos pequeños llegan rápido
```

#### HTTP/3

**Problema de HTTP/2:** Si se pierde un paquete TCP, **todos** los streams de objetos quedan bloqueados (HTTP/2 comparte una sola conexión TCP).

**HTTP/3:** Añade seguridad, control de errores y congestión **por objeto** sobre **UDP** (protocolo QUIC). Mayor pipelining, sin bloqueo HOL entre objetos.

---

## 3. Correo Electrónico: SMTP e IMAP

### Arquitectura del Sistema de E-mail

Tres componentes principales:

1. **Agente de Usuario (UA):** "Lector de correo" — compone, edita y lee mensajes. Ej: Outlook, iPhone Mail. Los mensajes entrantes/salientes se almacenan en el servidor.
2. **Servidores de correo:** Contienen el buzón del usuario (mensajes entrantes) y la cola de mensajes salientes.
3. **SMTP:** Protocolo para transferir mensajes entre servidores.

**Flujo de un e-mail de Alice a Bob:**

```
1. Alice usa su UA para componer el email a bob@someschool.edu.
2. El UA de Alice envía el mensaje a su servidor de correo via SMTP.
3. El servidor de Alice (cliente SMTP) abre conexión TCP al servidor de Bob.
4. El servidor de Alice transfiere el mensaje al servidor de Bob via SMTP.
5. El servidor de Bob deposita el mensaje en el buzón de Bob.
6. Bob usa su UA para leer el mensaje (via IMAP o HTTP).
```

---

### SMTP (RFC 5321)

- Usa **TCP** para transferencia confiable, **puerto 25**.
- Transferencia **directa**: del servidor emisor (actuando como cliente SMTP) al servidor receptor.

**Tres fases:**

1. **Handshaking (saludo):** Presentación entre cliente y servidor.
2. **Transferencia de mensajes.**
3. **Cierre.**

**Interacción SMTP (ejemplo real):**

```
S: 220 hamburger.edu
C: HELO crepes.fr
S: 250 Hello crepes.fr, pleased to meet you
C: MAIL FROM: <alice@crepes.fr>
S: 250 alice@crepes.fr... Sender ok
C: RCPT TO: <bob@hamburger.edu>
S: 250 bob@hamburger.edu... Recipient ok
C: DATA
S: 354 Enter mail, end with "." on a line by itself
C: Do you like ketchup?
C: How about pickles?
C: .
S: 250 Message accepted for delivery
C: QUIT
S: 221 hamburger.edu closing connection
```

---

### SMTP vs. HTTP

|Aspecto|HTTP|SMTP|
|---|---|---|
|Dirección del flujo|**Pull** (cliente solicita)|**Push** (cliente envía)|
|Interacción|Comando/respuesta ASCII|Comando/respuesta ASCII|
|Encapsulación de objetos|Cada objeto en su propia respuesta|Varios objetos en un mensaje multiparte|
|Conexión|Persistente (HTTP/1.1)|Persistente|
|Codificación del mensaje|Sin restricción|Requiere ASCII de 7 bits|
|Fin de mensaje|Content-Length o chunked|`CRLF.CRLF`|

---

### Formato del Mensaje de Email (RFC 2822)

```
To: bob@someschool.edu
From: alice@crepes.fr
Subject: ¿Te gusta el ketchup?

[línea en blanco]

Cuerpo del mensaje en ASCII
```

**Distinción importante:**

- `From:` / `To:` en el **cuerpo** del email: lo que el usuario ve.
- `MAIL FROM:` / `RCPT TO:` en el protocolo SMTP: lo que el servidor usa para enrutar.

---

### Recuperación de Email: IMAP

- **SMTP** solo sirve para **enviar** y almacenar en el servidor del destinatario.
- Para **recuperar** el email del servidor se necesita otro protocolo.

**IMAP (RFC 3501):**

- Mensajes almacenados en el servidor.
- Permite recuperar, eliminar y organizar mensajes en carpetas remotas.
- El estado de lectura/organización se sincroniza entre dispositivos.

**HTTP:** Gmail, Hotmail, Yahoo! Mail usan una interfaz web sobre SMTP (envío) + IMAP (recuperación).

---

## 4. DNS: Sistema de Nombres de Dominio

### ¿Qué es el DNS?

Las personas prefieren nombres (`www.google.com`) pero los routers usan **direcciones IP** (32 bits).

**DNS** es el sistema que traduce entre nombres y direcciones IP:

- **Base de datos distribuida** implementada en una jerarquía de servidores de nombres.
- **Protocolo de capa de aplicación:** los hosts y servidores DNS se comunican para resolver nombres.

**Servicios DNS:**

- Traducción hostname → dirección IP (y viceversa: reverse DNS).
- **Host aliasing:** `www.ibm.com` es alias de `servereast.backup2.ibm.com`.
- **Mail server aliasing:** el campo MX mapea un dominio a su servidor SMTP.
- **Distribución de carga:** múltiples IPs para un solo nombre (servidores web replicados). DNS rota entre ellas.

**¿Por qué NO centralizar el DNS?**

- Punto único de fallo.
- Volumen de tráfico enorme (Comcast: 600 mil millones de consultas/día; Akamai: 2.2 billones/día).
- Base de datos centralizada remota → alta latencia.
- Mantenimiento imposible a escala global.
- **No escala.** → Por eso es distribuido y jerárquico.

---

### Jerarquía DNS

```
                     [Servidores Raíz]         ← 13 grupos lógicos, ~200 instancias físicas
                    /       |        \
           [.com]       [.org]       [.edu]    ← TLD (Top Level Domain)
          /    \                       |
   [amazon.com] [yahoo.com]        [umass.edu] ← Autoritativos
```

**Tipos de servidores:**

|Tipo|Función|
|---|---|
|**Servidores raíz**|Contacto de último recurso. Conocen los servidores TLD. 13 grupos lógicos, cientos de réplicas físicas. Gestionados por ICANN.|
|**Servidores TLD**|Responsables de `.com`, `.org`, `.edu`, `.cn`, etc. Conocen los servidores autoritativos.|
|**Servidores autoritativos**|Propios de cada organización. Proveen mapeos definitivos hostname → IP para los hosts de esa organización.|
|**Servidor DNS local**|No es estrictamente parte de la jerarquía. Es el servidor al que va primero un host cuando hace una consulta DNS. Cada ISP tiene uno. Actúa como caché y proxy.|

---

### Resolución de Nombres DNS

#### Consulta Iterada

El servidor contactado responde con el nombre del siguiente servidor a consultar. La carga de la resolución es del **cliente DNS local**.

```
Host (engineering.nyu.edu) quiere IP de gaia.cs.umass.edu:

1. Host → DNS local (dns.nyu.edu): "¿Cuál es gaia.cs.umass.edu?"
2. DNS local → Raíz: "¿Cuál es gaia.cs.umass.edu?"
3. Raíz → DNS local: "No sé, pregunta al TLD .edu"
4. DNS local → TLD .edu: "¿Cuál es gaia.cs.umass.edu?"
5. TLD .edu → DNS local: "No sé, pregunta a dns.cs.umass.edu"
6. DNS local → dns.cs.umass.edu: "¿Cuál es gaia.cs.umass.edu?"
7. dns.cs.umass.edu → DNS local: "128.119.245.12"
8. DNS local → Host: "128.119.245.12"
```

#### Consulta Recursiva

El servidor DNS local **delega completamente** la resolución al siguiente servidor en la cadena. Más carga en los servidores superiores de la jerarquía.

---

### Caché DNS

- Cuando cualquier servidor DNS aprende un mapeo, lo **almacena en caché**.
- Responde desde caché inmediatamente a consultas futuras → mejora el tiempo de respuesta.
- Las entradas **expiran** después de un tiempo (TTL — Time To Live).
- Los servidores TLD típicamente están en caché en los servidores DNS locales → las consultas al servidor raíz pueden omitirse.
- **Problema:** Si un host cambia su IP, el cambio puede no propagarse hasta que expiren todos los TTLs.

---

### Registros DNS (Resource Records — RR)

Formato: `(nombre, valor, tipo, ttl)`

|Tipo|Nombre|Valor|Uso|
|---|---|---|---|
|**A**|Hostname|Dirección IPv4|Mapeo principal hostname → IP|
|**AAAA**|Hostname|Dirección IPv6|Mapeo hostname → IPv6|
|**NS**|Dominio (ej: `foo.com`)|Hostname del servidor autoritativo|Delegar resolución a otro servidor|
|**CNAME**|Alias (ej: `www.ibm.com`)|Nombre canónico real|Apuntar alias al nombre real|
|**MX**|Dominio|Nombre del servidor SMTP|Identificar servidor de correo|

**Ejemplo para registrar `networkutopia.com`:**

```
(networkutopia.com, dns1.networkutopia.com, NS)       ← en el servidor TLD .com
(dns1.networkutopia.com, 212.212.212.1, A)             ← en el servidor TLD .com
(www.networkutopia.com, 212.212.212.5, A)              ← en servidor autoritativo
(networkutopia.com, mail.networkutopia.com, MX)        ← en servidor autoritativo
```

---

### Mensajes DNS

Las consultas y respuestas tienen el **mismo formato**:

```
┌─────────────────────┬─────────────────┐
│    Identificación   │      Flags      │
├─────────────────────┼─────────────────┤
│   # Preguntas       │  # Answer RRs   │
├─────────────────────┼─────────────────┤
│  # Authority RRs    │ # Additional RRs│
├─────────────────────────────────────────┤
│       Preguntas (variable)              │
├─────────────────────────────────────────┤
│       Respuestas (RRs) (variable)       │
├─────────────────────────────────────────┤
│       Autoridad (RRs) (variable)        │
├─────────────────────────────────────────┤
│       Adicional (RRs) (variable)        │
└─────────────────────────────────────────┘
```

**Flags importantes:**

- Query/Reply: ¿es consulta o respuesta?
- Recursión deseada / disponible.
- La respuesta es autoritativa.
- El ID de 16 bits empareja consulta con respuesta.

---

### Seguridad DNS

|Tipo de Ataque|Descripción|Mitigación|
|---|---|---|
|**DDoS a servidores raíz**|Bombardear los raíces con tráfico. No exitoso hasta la fecha.|Filtrado de tráfico. Los servidores TLD están en caché local, permitiendo omitir la raíz.|
|**DDoS a servidores TLD**|Más peligroso que atacar la raíz.|Replicación, anycast.|
|**Envenenamiento de caché (Spoofing)**|Interceptar consultas DNS y responder con IPs falsas. Redirige usuarios a sitios maliciosos.|**DNSSEC** (RFC 4033): autenticación e integridad de mensajes mediante firmas criptográficas.|

---

## 5. Aplicaciones P2P y BitTorrent

### Distribución de Archivos: Cliente-Servidor vs. P2P

**P (pregunta):** ¿Cuánto tiempo se tarda en distribuir un archivo de tamaño F desde un servidor a N pares?

#### Tiempo mínimo para cliente-servidor:

```
D_cs ≥ max { NF / u_s ,  F / d_min }
```

- `NF / u_s`: El servidor debe subir N copias. Si tiene upload u_s, tarda NF/u_s segundos.
- `F / d_min`: El cliente más lento tarda al menos F/d_min.
- **El tiempo crece linealmente con N** (el servidor es el cuello de botella).

#### Tiempo mínimo para P2P:

```
D_P2P ≥ max { F / u_s ,  F / d_min ,  NF / (u_s + Σu_i) }
```

- `F / u_s`: El servidor debe subir al menos una copia.
- `F / d_min`: El peer más lento.
- `NF / (u_s + Σu_i)`: El sistema debe distribuir NF bits en total; la capacidad total de upload es la suma de todos.
- **Clave:** Aunque el tiempo también crece con N (el tercer término), el denominador también crece con N (cada nuevo peer aporta su upload). Por eso P2P **escala mucho mejor** que cliente-servidor.

**Comparación visual:**

```
     Tiempo
       │                        Cliente-Servidor (crece rápido)
       │                    ╱─────────────────────────────────
       │                ╱──
       │   P2P    ╱───
       │      ╱──
       └──────────────────────────────────────── N (usuarios)
```

---

### BitTorrent

**Mecanismo de distribución P2P** para archivos grandes.

**Conceptos clave:**

- El archivo se divide en **chunks de 256 KB**.
- Los pares en el **torrent** intercambian chunks.
- El **tracker** registra qué pares participan y facilita que nuevos pares se conecten.

**Al unirse al torrent:**

1. El nuevo par (Alice) no tiene chunks.
2. Se registra en el tracker, obtiene lista de pares.
3. Se conecta a un subconjunto de pares ("vecinos").
4. Mientras descarga, sube chunks a otros pares.
5. Puede cambiar de pares con quienes intercambia.
6. Una vez completo, puede quedarse (altruista) o irse (egoísta).

**Solicitud de chunks — "Rarest First":**

- Periódicamente, Alice pide a cada par la lista de sus chunks.
- Solicita los chunks que le **faltan**, empezando por los más raros en la red.
- Esto asegura que los chunks escasos se repliquen rápido.

**Envío de chunks — "Tit-for-Tat" (ojo por ojo):**

- Alice envía chunks a los **4 pares** que actualmente le envían a la tasa **más alta**.
- Los demás quedan bloqueados (no reciben de Alice).
- Reevalúa el top-4 cada **10 segundos**.
- Cada **30 segundos**: desbloquea **optimistamente** a un par aleatorio (puede unirse al top-4).
- **Incentivo:** Si ofreces buen upload, recibirás buen download.

---

## 6. Video Streaming y CDNs

### Contexto

- El streaming de video es el **principal consumidor de ancho de banda** en Internet.
- Netflix, YouTube, Amazon Prime: **80% del tráfico ISP residencial** (2020).
- Desafíos:
    - **Escala:** ~1,000 millones de usuarios.
    - **Heterogeneidad:** distintos usuarios tienen distintas capacidades (cable, móvil, ancho de banda variable).

---

### Codificación de Video

- Video: secuencia de imágenes a tasa constante (ej: 24 frames/seg).
- Codificación: aprovechar redundancia **espacial** (píxeles similares) y **temporal** (frames similares) para reducir bits.
- **CBR (Constant Bit Rate):** tasa de codificación fija. Predecible, fácil de planificar.
- **VBR (Variable Bit Rate):** tasa varía según el contenido. Más eficiente.

|Estándar|Uso|Velocidad|
|---|---|---|
|MPEG-1|CD-ROM|1.5 Mbps|
|MPEG-2|DVD|3-6 Mbps|
|MPEG-4|Internet|64 Kbps – 12 Mbps|

---

### Streaming Almacenado: Desafíos

El ancho de banda servidor-cliente varía en el tiempo (congestión, cambios de red). Soluciones necesarias:

- **Buffer del lado del cliente:** Absorbe variaciones de retardo (jitter). El cliente reproduce desde el buffer, no directamente de la red.
- **Retardo de reproducción:** Esperar a que el buffer se llene antes de comenzar a reproducir. Compensación entre tiempo de inicio y robustez.

---

### DASH: Dynamic Adaptive Streaming over HTTP

**Idea central:** El servidor ofrece el mismo video a **múltiples calidades**. El cliente elige dinámicamente la calidad según su ancho de banda disponible.

**Rol del servidor:**

- Divide el archivo de video en **chunks**.
- Cada chunk se codifica a **múltiples tasas de bits** (calidades).
- Los archivos se replican en nodos de CDN.
- Proporciona un **archivo de manifiesto** con las URLs de los chunks en cada calidad.

**Rol del cliente:**

- Estima periódicamente el ancho de banda disponible.
- Consulta el manifiesto y solicita un chunk a la vez.
- Elige la **mayor tasa de codificación sostenible** dado el ancho de banda actual.
- Puede cambiar de calidad y de servidor en cada chunk.

**Decisiones del cliente (toda la "inteligencia"):**

- **¿Cuándo pedir un chunk?** Para evitar que el buffer se vacíe (starvation) o se desborde.
- **¿Qué calidad pedir?** Mayor calidad cuando hay más ancho de banda.
- **¿A qué servidor pedirlo?** Al más cercano o con mayor ancho de banda disponible.

```
Streaming de video = Codificación + DASH + Buffer de reproducción
```

---

### CDN: Redes de Distribución de Contenido

**Problema:** ¿Cómo distribuir contenido a cientos de miles de usuarios simultáneos?

**Opción 1 — Megaservidor único:** Punto único de fallo, punto de congestión, ruta larga a clientes remotos. **No escala.**

**Opción 2 — CDN:** Almacenar múltiples copias del contenido en sitios distribuidos geográficamente.

**Dos filosofías de despliegue CDN:**

|Estrategia|Descripción|Ejemplo|
|---|---|---|
|**Enter Deep**|Servidores CDN integrados profundamente en múltiples redes de acceso. Cerca de los usuarios.|Akamai: 240,000 servidores en >120 países (2015)|
|**Bring Home**|Pocos clusters grandes en POPs (Points of Presence) cerca de las redes de acceso.|Limelight|

**Cómo funciona el acceso a contenido CDN (ej: Netflix via CDN):**

1. Bob solicita `http://netcinema.com/6Y7B23V`.
2. DNS de netcinema.com devuelve un CNAME apuntando a un servidor CDN: `http://KingCDN.com/NetC6y&B23V`.
3. El DNS local de Bob resuelve el dominio CDN → devuelve IP del nodo CDN más cercano/adecuado.
4. Bob descarga el video directamente desde ese nodo CDN via HTTP/DASH.

**Ventajas de CDN:**

- Contenido más cerca del usuario → menor latencia.
- Distribuye la carga entre muchos servidores.
- Resiliencia: si un nodo falla, se usa otro.

---

## 7. Programación de Sockets

### Conceptos Básicos

**Socket:** Interfaz entre la aplicación y el protocolo de transporte (TCP o UDP). Es la "puerta" a través de la cual el proceso envía y recibe mensajes.

**Dos tipos de sockets:**

- **UDP:** Datagrama no confiable.
- **TCP:** Confiable, orientado a flujo de bytes.

---

### Sockets UDP

**Características:**

- Sin conexión: no hay handshake antes de enviar datos.
- El emisor adjunta explícitamente **IP destino + puerto** a cada paquete.
- El receptor extrae **IP origen + puerto** del paquete recibido.
- Los datos pueden perderse o llegar fuera de orden.

**Interacción cliente-servidor UDP:**

```
Servidor                                 Cliente
───────────────────────────────────────────────────
create socket (serverSocket)
bind(serverSocket, port=12000)
                                         create socket (clientSocket)
wait for datagram...
                                         sendto(serverIP, port 12000, mensaje)
recvfrom(serverSocket)                   ←── datagrama llega
                                         
sendto(clientAddress, port, respuesta)
                                         recvfrom(clientSocket)
                                         close(clientSocket)
```

**Código Python UDP (cliente):**

```python
from socket import *
serverName = 'hostname'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Ingresa texto: ')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
```

**Código Python UDP (servidor):**

```python
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("Servidor listo")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
```

---

### Sockets TCP

**Características:**

- El cliente debe contactar al servidor **que ya está corriendo** con un socket de bienvenida.
- Al conectarse el cliente, TCP crea un **nuevo socket dedicado** a esa conexión específica.
- Permite que el servidor se comunique con múltiples clientes simultáneamente.
- Proporciona transferencia **confiable y en orden** ("pipe").

**Interacción cliente-servidor TCP:**

```
Servidor                                 Cliente
───────────────────────────────────────────────────
serverSocket = socket()
serverSocket.bind(port=x)
serverSocket.listen()                    
                                         clientSocket = socket()
connectionSocket =                 TCP   clientSocket.connect(hostid, port=x)
serverSocket.accept()        ←─ setup ──
                                         clientSocket.send(solicitud)
read(connectionSocket)        ←─────────
write(connectionSocket, resp)
                                         read(clientSocket)
connectionSocket.close()                 clientSocket.close()
```

**Diferencia clave con UDP:** El servidor TCP tiene **dos tipos de sockets**:

1. **Socket de bienvenida** (`serverSocket`): escucha nuevas conexiones entrantes.
2. **Socket de conexión** (`connectionSocket`): creado automáticamente por `accept()` para cada cliente nuevo.

**Código Python TCP (cliente):**

```python
from socket import *
serverName = 'servername'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))  # TCP handshake aquí
sentence = input('Ingresa texto: ')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('Del servidor:', modifiedSentence.decode())
clientSocket.close()
```

**Código Python TCP (servidor):**

```python
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("Servidor listo")
while True:
    connectionSocket, addr = serverSocket.accept()  # bloquea hasta nueva conexión
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()  # cierra solo la conexión con este cliente
```

---

## 8. Resumen Rápido y Tablas de Referencia

### Protocolos de Aplicación: Tabla Resumen

|Protocolo|Capa de transporte|Puerto|Función|
|---|---|---|---|
|**HTTP**|TCP|80|Transferencia de páginas web|
|**HTTPS**|TCP (+ TLS)|443|HTTP cifrado|
|**FTP**|TCP|20/21|Transferencia de archivos|
|**SMTP**|TCP|25|Envío de e-mail|
|**IMAP**|TCP|143|Recuperación de e-mail del servidor|
|**DNS**|UDP (y TCP para grandes)|53|Resolución de nombres|
|**HTTP/3 (QUIC)**|UDP|443|HTTP con congestión por objeto|

### Comparación de Arquitecturas

|Característica|Cliente-Servidor|P2P|
|---|---|---|
|Servidor siempre activo|Sí|No|
|Escalabilidad|Lineal con N (cuello de botella)|Buena (cada par aporta capacidad)|
|Gestión|Simple|Compleja|
|Ejemplos|HTTP, SMTP, DNS|BitTorrent, VoIP antiguo|

### Tipos de Registros DNS

|Tipo|Mapeo|Ejemplo|
|---|---|---|
|A|hostname → IPv4|`gaia.cs.umass.edu → 128.119.245.12`|
|AAAA|hostname → IPv6|similar a A para IPv6|
|NS|dominio → servidor autoritativo|`foo.com → dns.foo.com`|
|CNAME|alias → nombre canónico|`www.ibm.com → servereast.backup2.ibm.com`|
|MX|dominio → servidor SMTP|`foo.com → mail.foo.com`|

### Comparación HTTP 1.1 / 2 / 3

|Versión|Conexión|Problemas|Solución|
|---|---|---|---|
|HTTP/1.0|No persistente|2 RTTs por objeto|—|
|HTTP/1.1|Persistente|HOL blocking con objetos grandes|Múltiples conexiones TCP paralelas|
|HTTP/2|TCP única con frames|Pérdida de paquete bloquea todo|División en frames intercalados, priorización|
|HTTP/3|UDP (QUIC)|Sin bloqueo HOL, seguridad|Error/congestión por objeto sobre UDP|

### Temas Frecuentes de Certamen

1. **TCP vs. UDP:** ¿Cuándo usar cada uno? ¿Por qué existe UDP si TCP es "mejor"?
2. **HTTP no persistente vs. persistente:** Calcular el tiempo total dado N objetos, RTT y tiempo de transmisión.
3. **Métodos HTTP:** Diferencia entre GET, POST, HEAD, PUT. ¿Cuándo usar cada uno?
4. **Códigos de estado HTTP:** 200, 301, 304, 400, 404, 505 — qué significan.
5. **Cookies:** ¿Cómo funcionan? Los 4 componentes. ¿Por qué HTTP es stateless y cómo las cookies añaden estado?
6. **Web caché:** Calcular utilización del enlace y retardo promedio con/sin caché dado un hit rate.
7. **GET condicional:** ¿Qué es? ¿Para qué sirve? ¿Qué responde el servidor si el objeto no cambió?
8. **DNS jerárquico:** ¿Qué son los servidores raíz, TLD y autoritativos? Trazar la resolución iterativa.
9. **Registros DNS:** Dado un escenario, identificar qué tipo de RR se necesita (A, NS, CNAME, MX).
10. **BitTorrent:** ¿Qué es tit-for-tat? ¿Qué es rarest-first? ¿Por qué P2P escala mejor que cliente-servidor?
11. **DASH:** ¿Qué hace el servidor? ¿Qué hace el cliente? ¿Dónde está la "inteligencia"?
12. **CDN:** Enter deep vs. bring home. ¿Cómo funciona el acceso a contenido CDN via DNS?
13. **Sockets TCP vs UDP:** Diferencia en la interacción (handshake, socket de bienvenida vs. socket de conexión).
14. **SMTP vs. HTTP:** Pull vs. push. ¿Por qué SMTP requiere ASCII de 7 bits? ¿Cómo termina un mensaje SMTP?

---

_Basado en: Computer Networking: A Top-Down Approach, 8ª edición — Jim Kurose, Keith Ross, Pearson 2020._


