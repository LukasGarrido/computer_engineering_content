# Preguntas de Práctica — Capítulos 1 al 4

### Computer Networking: A Top-Down Approach — Kurose & Ross, 8ª ed.

> Mix de preguntas fáciles, intermedias y revuscadas con respuestas detalladas

---

## Capítulo 1 — Introducción

---

**P1.1 (Fácil)** ¿Cuál es la diferencia entre _forwarding_ y _routing_? ¿En qué capa ocurre cada uno?

<details> <summary>▶ Ver respuesta</summary>

**Forwarding** es una acción _local_ dentro de un router: tomar el paquete que llegó por un puerto de entrada y enviarlo al puerto de salida correcto, consultando la tabla de reenvío del propio router. Ocurre en el **plano de datos** (hardware, nanosegundos).

**Routing** es una función _global de la red_: calcular las rutas que deben seguir los paquetes de extremo a extremo, y con eso construir las tablas de reenvío. Ocurre en el **plano de control** (software, milisegundos), mediante algoritmos como OSPF o BGP.

**Analogía:** Routing = planificar el mapa completo del viaje antes de salir. Forwarding = tomar la decisión en cada intersección durante el viaje.

</details>

---

**P1.2 (Fácil)** Un paquete de 1,000,000 bits debe transmitirse por un enlace de 1 Mbps. ¿Cuánto tiempo tarda en transmitirse? Si el enlace tiene una longitud de 3,000 km y la velocidad de propagación es 2×10⁸ m/s, ¿cuánto tarda en propagarse el primer bit?

<details> <summary>▶ Ver respuesta</summary>

**Retardo de transmisión:**

```
d_trans = L / R = 1,000,000 bits / 1,000,000 bps = 1 segundo
```

**Retardo de propagación:**

```
d_prop = d / s = 3,000,000 m / 2×10⁸ m/s = 0.015 segundos = 15 ms
```

Son conceptos completamente distintos: d_trans depende del tamaño del paquete y la velocidad del enlace; d_prop depende de la distancia y el medio físico. El último bit del paquete no llega al destino hasta que hayan pasado **1 s + 15 ms = 1.015 s** desde que empezó la transmisión.

</details>

---

**P1.3 (Intermedia)** Una red de circuit switching tiene un enlace de 1.5 Mbps. Cada usuario necesita 150 Kbps cuando está activo y está activo el 10% del tiempo. ¿Cuántos usuarios soporta con circuit switching? ¿Y con packet switching si se acepta que la probabilidad de que haya más de 10 usuarios activos simultáneamente sea menor al 0.001?

<details> <summary>▶ Ver respuesta</summary>

**Circuit switching:**

```
Usuarios = 1,500,000 bps / 150,000 bps = 10 usuarios
```

Con circuit switching los recursos se reservan siempre, sin importar si el usuario los usa o no. Solo caben exactamente 10.

**Packet switching:** Con 35 usuarios y una probabilidad de actividad del 10%, la probabilidad de que más de 10 estén activos al mismo tiempo es muy pequeña (< 0.004 según el libro). Si el umbral permitido es 0.001, podrían soportarse algo más de 30 usuarios. El punto clave es que packet switching permite **más usuarios** aprovechando que el tráfico es bursty — los recursos no se desperdician cuando los usuarios están inactivos.

</details>

---

**P1.4 (Revuscada)** Considera un camino de extremo a extremo con 3 routers (es decir, 4 enlaces). Cada enlace tiene capacidad R = 10 Mbps y retardo de propagación de 5 ms. El paquete tiene un tamaño de L = 5000 bits. Asume que no hay retardo de cola ni de procesamiento. ¿Cuál es el retardo total de extremo a extremo? Ahora, ¿qué ocurriría con el retardo total si duplicas el tamaño del paquete? ¿Y si duplicas R?

<details> <summary>▶ Ver respuesta</summary>

**Retardo de transmisión por enlace:**

```
d_trans = L/R = 5000 bits / 10,000,000 bps = 0.5 ms
```

**Retardo total (4 enlaces):**

```
d_total = 4 × (d_trans + d_prop) = 4 × (0.5 ms + 5 ms) = 4 × 5.5 ms = 22 ms
```

**Si se duplica L (L = 10,000 bits):**

```
d_trans = 10,000 / 10,000,000 = 1 ms
d_total = 4 × (1 ms + 5 ms) = 24 ms
```

El retardo de propagación no cambia; solo aumenta el de transmisión.

**Si se duplica R (R = 20 Mbps):**

```
d_trans = 5000 / 20,000,000 = 0.25 ms
d_total = 4 × (0.25 ms + 5 ms) = 21 ms
```

Duplicar R reduce a la mitad el retardo de transmisión, pero el retardo de propagación domina en este caso, por lo que la mejora total es modesta.

**Lección:** Cuando el retardo de propagación domina (enlaces largos), mejorar la capacidad del enlace (R) tiene poco efecto. Cuando domina el retardo de transmisión (paquetes grandes, enlaces lentos), aumentar R sí ayuda mucho.

</details>

---

**P1.5 (Revuscada)** Un router tiene un tráfico de entrada con intensidad La/R = 0.9. Luego se añade tráfico adicional que eleva La/R a 1.1. ¿Qué le ocurre al retardo de cola? Explica por qué esta situación es cualitativamente diferente a pasar de La/R = 0.5 a La/R = 0.9. ¿Qué implica esto para el diseño de redes?

<details> <summary>▶ Ver respuesta</summary>

Cuando La/R = 0.9 el retardo de cola ya es **grande pero finito**: la cola crece en los picos pero se vacía en los valles, el sistema es estable.

Cuando La/R > 1 (en este caso 1.1), **llegan más bits por segundo de los que el enlace puede enviar**. La cola crece _indefinidamente_ y el retardo medio se vuelve teóricamente infinito. El router empieza a descartar paquetes (pérdidas).

La diferencia entre 0.5 → 0.9 es cuantitativa (el retardo aumenta mucho, pero el sistema sigue siendo estable). La diferencia entre 0.9 → 1.1 es **cualitativa**: el sistema pasa de estable a inestable. La curva de retardo vs. traffic intensity tiene una asíntota vertical en La/R = 1.

**Implicación de diseño:** Las redes se diseñan para operar con traffic intensity **bien por debajo de 1** (típicamente < 0.7–0.8) para garantizar que los picos de tráfico no superen la capacidad del enlace. Operar cerca de la capacidad máxima genera retardos y pérdidas desproporcionados.

</details>

---

## Capítulo 2 — Capa de Aplicación

---

**P2.1 (Fácil)** ¿Por qué HTTP es un protocolo "sin estado" (stateless)? ¿Qué mecanismo usan los sitios web para mantener el estado de sesión a pesar de eso?

<details> <summary>▶ Ver respuesta</summary>

HTTP es **stateless** porque el servidor no recuerda nada de solicitudes anteriores del mismo cliente. Cada solicitud HTTP es completamente independiente. Esto simplifica el diseño del servidor y facilita la escalabilidad (no hay que mantener tablas de estado por cliente).

Para mantener estado de sesión (usuario logueado, carrito de compras, etc.) se usan **cookies**:

1. El servidor envía `Set-Cookie: id=1678` en la respuesta HTTP.
2. El navegador guarda la cookie.
3. En cada solicitud siguiente, el navegador incluye `Cookie: 1678`.
4. El servidor consulta su base de datos con ese ID y recupera el estado asociado.

Las cookies son el "parche" que añade estado a un protocolo diseñado para ser stateless.

</details>

---

**P2.2 (Fácil)** Explica la diferencia entre HTTP no persistente y HTTP persistente. ¿Cuántos RTTs se necesitan para descargar una página con un objeto HTML base y 10 imágenes referenciadas, usando cada versión?

<details> <summary>▶ Ver respuesta</summary>

**HTTP no persistente (HTTP/1.0):** Cada objeto requiere una conexión TCP separada. Para cada objeto: 1 RTT para el handshake TCP + 1 RTT para la solicitud y respuesta HTTP = **2 RTTs + tiempo de transmisión por objeto**.

Para 1 HTML + 10 imágenes = 11 objetos:

```
Total = 11 × 2 RTT + tiempos de transmisión = 22 RTT (mínimo, sin paralelismo)
```

Con múltiples conexiones TCP paralelas (como hacen los navegadores) el tiempo se reduce pero el overhead sigue siendo alto.

**HTTP persistente (HTTP/1.1):** El servidor mantiene la conexión TCP abierta. Una sola conexión sirve todos los objetos. Con pipelining:

- 1 RTT para el TCP handshake inicial.
- 1 RTT para el HTML base.
- 1 RTT para las 10 imágenes (todas en pipeline).

```
Total ≈ 3 RTT (aprox) + tiempos de transmisión
```

La mejora es drástica para páginas con muchos objetos.

</details>

---

**P2.3 (Intermedia)** ¿Qué es el GET condicional en HTTP? Explica el mecanismo con las cabeceras involucradas y por qué es beneficioso para la web caché.

<details> <summary>▶ Ver respuesta</summary>

El **GET condicional** permite que una caché verifique si su copia de un objeto sigue siendo válida sin tener que descargarlo de nuevo.

**Mecanismo:**

1. La caché guarda el objeto junto con la fecha de última modificación (del campo `Last-Modified:` de la respuesta original).
2. En la siguiente solicitud del mismo objeto, la caché envía al servidor de origen:
    
    ```
    GET /index.html HTTP/1.1If-Modified-Since: Wed, 09 Sep 2020 10:30:00
    ```
    
3. El servidor verifica si el objeto fue modificado después de esa fecha:
    - **No fue modificado:** responde `304 Not Modified` sin cuerpo (sin el objeto). La caché usa su copia local.
    - **Fue modificado:** responde `200 OK` con el nuevo objeto.

**Beneficio:** Cuando el objeto no cambió, se evita transmitir el objeto completo — solo se intercambian cabeceras. Esto ahorra ancho de banda y reduce el tiempo de respuesta al usuario. Combina las ventajas del caché local (velocidad) con la garantía de contenido actualizado.

</details>

---

**P2.4 (Revuscada)** Considera la jerarquía DNS. Cuando un host `alumno.usach.cl` hace una consulta DNS para resolver `www.amazon.com` por primera vez, describe paso a paso el proceso de consulta **iterativa**. ¿Qué ocurre en la segunda consulta al mismo nombre? ¿Por qué los servidores raíz rara vez son consultados en la práctica?

<details> <summary>▶ Ver respuesta</summary>

**Primera consulta — proceso iterativo:**

1. El host envía la consulta `www.amazon.com` al **servidor DNS local** de su red (configurado por DHCP, ej: `dns.usach.cl`).
2. El servidor DNS local no tiene la respuesta en caché → consulta a un **servidor raíz**.
3. El servidor raíz responde: "No sé la IP, pero el servidor TLD para `.com` es `a.gtld-servers.net` con IP X.X.X.X".
4. El servidor DNS local consulta al **servidor TLD `.com`**.
5. El TLD responde: "No sé la IP de `www.amazon.com`, pero el servidor autoritativo de `amazon.com` es `ns1.amazon.com` con IP Y.Y.Y.Y".
6. El servidor DNS local consulta al **servidor autoritativo de amazon.com**.
7. El servidor autoritativo responde con la IP de `www.amazon.com`: `205.251.242.103`.
8. El servidor DNS local devuelve la IP al host, y la **almacena en caché** con su TTL.

**Segunda consulta:** El servidor DNS local ya tiene la respuesta en caché. Responde **directamente** sin contactar a ningún servidor externo. Esto reduce el tiempo de respuesta y el tráfico DNS.

**¿Por qué los servidores raíz rara vez son contactados?** Los servidores TLD y autoritativos también quedan en caché en los servidores DNS locales. Una vez que un servidor DNS local conoce la dirección del TLD `.com` (que es estable), no necesita consultar al raíz para resolver cualquier nombre `.com`. Con TTLs de días o semanas para los TLDs, la mayoría de las consultas se resuelven directamente a nivel de TLD o autoritativo.

</details>

---

**P2.5 (Revuscada)** En BitTorrent, un peer recién unido al torrent no tiene ningún chunk. Explica los mecanismos de **rarest-first** y **tit-for-tat** y argumenta por qué ambos son necesarios para el funcionamiento correcto del sistema. ¿Qué pasaría si un peer solo implementara uno de los dos?

<details> <summary>▶ Ver respuesta</summary>

**Rarest-first (el más escaso primero):** Al solicitar chunks, cada peer prioriza los chunks que son **más raros en la red** (los que menos peers tienen). Esto asegura que los chunks escasos se repliquen rápidamente, evitando que el sistema quede atascado cuando pocos peers tienen un chunk crítico. Sin rarest-first, los peers descargarían chunks populares repetidamente, dejando los raros sin replicar y haciendo la distribución más lenta.

**Tit-for-tat (ojo por ojo):** Cada peer sube datos a los **4 peers que actualmente le están subiendo a mayor velocidad**, bloqueando a los demás. Cada 30 segundos desbloquea aleatoriamente a un peer ("optimistic unchoke") para descubrir nuevos peers capaces. Esto crea un **incentivo económico**: si quieres descargar rápido, debes subir rápido.

**Si solo hubiera rarest-first sin tit-for-tat:** Los "free riders" (peers que descargan pero no suben) se aprovecharían del sistema sin contribuir. Con el tiempo, los peers contribuyentes dejarían de compartir y el sistema colapsaría.

**Si solo hubiera tit-for-tat sin rarest-first:** Los peers intercambiarían eficientemente, pero los chunks raros podrían nunca replicarse suficientemente. Un peer con el único chunk raro podría convertirse en cuello de botella o abandonar el torrent antes de compartirlo, dejando el archivo incompleto para todos.

**Juntos:** rarest-first garantiza disponibilidad de todos los chunks; tit-for-tat garantiza que todos contribuyan. Son complementarios.

</details>

---

## Capítulo 3 — Capa de Transporte

---

**P3.1 (Fácil)** ¿Por qué existe UDP si TCP es más confiable? Da tres casos de uso donde UDP es preferible a TCP y explica por qué en cada uno.

<details> <summary>▶ Ver respuesta</summary>

UDP existe porque en algunos escenarios sus "debilidades" son en realidad ventajas:

**1. DNS:** Una consulta DNS es un solo paquete de ida y otro de vuelta. Establecer una conexión TCP (3-way handshake) añadiría un RTT completo antes de recibir la respuesta. Con UDP, la consulta va directa. Si no llega respuesta, la aplicación simplemente reintenta — no necesita que TCP lo haga.

**2. Streaming de video/audio en tiempo real (VoIP, videoconferencias):** Un frame de video retrasado es peor que uno perdido — en una videollamada, si TCP retransmite un paquete viejo, lo recibes tarde y fuera de sincronía. Es mejor saltar ese frame y seguir. Además, el control de congestión de TCP podría reducir la tasa de envío en momentos críticos, causando pausas perceptibles.

**3. Aplicaciones que implementan su propia confiabilidad (QUIC, HTTP/3):** Algunas aplicaciones necesitan control fino sobre qué se retransmite y cuándo. UDP como base permite que la capa de aplicación implemente solo los mecanismos que necesita, sin todo el overhead de TCP.

En general: UDP es preferible cuando la latencia importa más que la confiabilidad, o cuando la aplicación puede manejar pérdidas por sí misma.

</details>

---

**P3.2 (Intermedia)** El protocolo rdt 2.0 introduce ACK/NAK para manejar errores de bits. Sin embargo, tiene un fallo fatal. Describe el fallo y explica exactamente cómo rdt 2.1 lo soluciona. ¿Por qué es suficiente usar números de secuencia de 1 bit (0 y 1) en stop-and-wait?

<details> <summary>▶ Ver respuesta</summary>

**Fallo de rdt 2.0:** Si el ACK o el NAK se corrompe en el canal, el emisor no sabe qué ocurrió en el receptor. Si retransmite el paquete (asumiendo que el receptor pidió reenvío), puede enviar un **duplicado** cuando en realidad el receptor ya recibió el paquete correctamente. El receptor no puede distinguir si es un paquete nuevo o una retransmisión.

**Solución de rdt 2.1:** El emisor agrega un **número de secuencia** (0 o 1) a cada paquete. Ahora el receptor puede detectar duplicados:

- Si recibe un paquete con el mismo número de secuencia que el último aceptado → es un duplicado → lo descarta y reenvía ACK.
- Si recibe un paquete con el número de secuencia esperado → es nuevo → lo acepta y cambia lo que espera.

**¿Por qué 1 bit es suficiente?** En stop-and-wait, el emisor envía un paquete y espera su ACK antes de enviar el siguiente. Esto significa que solo hay **un paquete "en vuelo" a la vez**. El receptor solo necesita saber si el paquete que llegó es el actual (nuevo) o el anterior (duplicado retransmitido). Para distinguir dos estados, basta con 1 bit (0 o 1). Si hubiera pipelining, se necesitarían más bits.

</details>

---

**P3.3 (Intermedia)** En un escenario de Repetición Selectiva (SR) con k = 3 bits para los números de secuencia, ¿cuál es el tamaño máximo permitido de la ventana del emisor? Explica con un ejemplo concreto por qué una ventana mayor causaría ambigüedad en el receptor.

<details> <summary>▶ Ver respuesta</summary>

**Espacio de números de secuencia:** 2^3 = 8 valores (0 a 7).

**Tamaño máximo de ventana SR:** 2^(k-1) = 2^2 = **4**.

**¿Por qué no 5 o más?**

Supón que la ventana es 5 y los números de secuencia son {0,1,2,3,4,5,6,7}.

- El emisor envía los paquetes 0, 1, 2, 3, 4.
- El receptor recibe correctamente 0, 1, 2, 3, 4, los entrega a la aplicación y su ventana avanza. Ahora espera 5, 6, 7, 0, 1.
- Los ACKs de 0, 1, 2, 3, 4 se pierden todos.
- El emisor retransmite 0.
- El receptor recibe un paquete con número de secuencia 0. ¿Es el **nuevo** paquete 0 (que va después del 7) o una **retransmisión** del paquete 0 original?

Con ventana = 5, el receptor no puede saberlo porque el número de secuencia 0 puede corresponder a ambos casos. Con ventana ≤ 4, esto no ocurre porque el emisor no puede haber avanzado lo suficiente como para reutilizar un número de secuencia que aún podría confundirse con una retransmisión.

**Regla:** Ventana SR ≤ (espacio de secuencias) / 2. Con k=3: ventana ≤ 4.

</details>

---

**P3.4 (Revuscada)** TCP usa EWMA para estimar el RTT. Dado el siguiente historial de mediciones SampleRTT: 100 ms, 200 ms, 80 ms, 150 ms (en orden), calcula EstimatedRTT y DevRTT tras cada muestra, empezando con EstimatedRTT₀ = 100 ms y DevRTT₀ = 0. Usa α = 0.125 y β = 0.25. Finalmente, calcula el TimeoutInterval después de la última muestra. ¿Qué propiedad del EWMA explica que las muestras más antiguas tengan menos influencia?

<details> <summary>▶ Ver respuesta</summary>

Fórmulas:

```
EstimatedRTT = (1 - 0.125) × EstimatedRTT + 0.125 × SampleRTT
DevRTT = (1 - 0.25) × DevRTT + 0.25 × |SampleRTT - EstimatedRTT|
TimeoutInterval = EstimatedRTT + 4 × DevRTT
```

**Muestra 1: SampleRTT = 100 ms**

```
EstRTT = 0.875 × 100 + 0.125 × 100 = 100 ms
DevRTT = 0.75 × 0 + 0.25 × |100 - 100| = 0 ms
```

**Muestra 2: SampleRTT = 200 ms**

```
EstRTT = 0.875 × 100 + 0.125 × 200 = 87.5 + 25 = 112.5 ms
DevRTT = 0.75 × 0 + 0.25 × |200 - 112.5| = 0.25 × 87.5 = 21.875 ms
```

**Muestra 3: SampleRTT = 80 ms**

```
EstRTT = 0.875 × 112.5 + 0.125 × 80 = 98.44 + 10 = 108.44 ms
DevRTT = 0.75 × 21.875 + 0.25 × |80 - 108.44| = 16.41 + 7.11 = 23.52 ms
```

**Muestra 4: SampleRTT = 150 ms**

```
EstRTT = 0.875 × 108.44 + 0.125 × 150 = 94.88 + 18.75 = 113.63 ms
DevRTT = 0.75 × 23.52 + 0.25 × |150 - 113.63| = 17.64 + 9.09 = 26.73 ms
```

**TimeoutInterval:**

```
TimeoutInterval = 113.63 + 4 × 26.73 = 113.63 + 106.92 = 220.55 ms
```

**¿Por qué las muestras antiguas pesan menos?** En EWMA, el peso de una muestra decrece _exponencialmente_ con el tiempo. La muestra actual tiene peso α = 0.125; la anterior tiene peso α(1-α) = 0.109; la de dos pasos atrás α(1-α)² ≈ 0.096, y así sucesivamente. Como (1-α) < 1, los pesos convergen a 0 geométricamente. Esto hace que el estimado reaccione a cambios recientes sin ser demasiado sensible al ruido de una sola medición.

</details>

---

**P3.5 (Revuscada)** En TCP Reno, la ventana de congestión (cwnd) es inicialmente 1 MSS y ssthresh = 8 MSS. Describe la evolución de cwnd durante los primeros 12 RTTs asumiendo que ocurren los siguientes eventos: pérdida por triple ACK duplicado en RTT 6, timeout en RTT 9. ¿En qué RTT vuelve el cwnd a ser mayor que 8 MSS?

<details> <summary>▶ Ver respuesta</summary>

**Slow Start** (crecimiento exponencial mientras cwnd < ssthresh):

|RTT|cwnd (MSS)|Fase|Evento|
|---|---|---|---|
|1|1|Slow Start|—|
|2|2|Slow Start|—|
|3|4|Slow Start|—|
|4|8|Slow Start → CA|cwnd alcanza ssthresh=8|
|5|9|Congestion Avoidance|+1 MSS/RTT|
|6|10|CA → Fast Recovery|Triple ACK dup: ssthresh = 10/2 = 5, cwnd = 5+3 = 8|
|7|6|Congestion Avoidance|cwnd = ssthresh = 5 → +1/RTT → 6|
|8|7|Congestion Avoidance|—|
|9|8|CA → Slow Start|Timeout: ssthresh = 8/2 = 4, cwnd = 1|
|10|2|Slow Start|—|
|11|4|Slow Start → CA|cwnd alcanza ssthresh=4|
|12|5|Congestion Avoidance|—|

**Nota RTT 6:** Al detectar triple ACK dup, TCP Reno aplica fast retransmit + fast recovery: ssthresh = cwnd/2 = 5, cwnd = ssthresh + 3 = 8. Luego entra directamente a Congestion Avoidance (no vuelve a Slow Start).

**¿Cuándo cwnd > 8 MSS de nuevo?** Tras el timeout en RTT 9, cwnd vuelve a 1 y ssthresh = 4. El crecimiento es: 1→2→4 (Slow Start), luego CA: 5, 6, 7, 8, **9** en RTT 17 aproximadamente.

**Diferencia clave Reno vs. Tahoe:** Tahoe ante triple ACK dup también volvería cwnd = 1 (como si fuera timeout). Reno es más suave: hace fast recovery y mantiene cwnd en ssthresh+3.

</details>

---

## Capítulo 4 — Capa de Red: Data Plane

---

**P4.1 (Fácil)** ¿Qué es el _longest prefix matching_ y por qué es necesario en las tablas de reenvío IP? Da un ejemplo con tres entradas en la tabla y muestra qué entrada se usa para dos direcciones destino distintas.

<details> <summary>▶ Ver respuesta</summary>

**Longest prefix matching** es la regla que dice: al buscar en la tabla de reenvío, se usa la entrada cuyo prefijo de red sea el más largo (más específico) que coincida con la dirección destino.

**¿Por qué es necesario?** CIDR permite que una misma dirección encaje en múltiples prefijos de distintos tamaños (un bloque grande `/16` puede contener subredes `/24`). Sin una regla de desempate, no se sabría cuál usar. El prefijo más largo es el más específico y tiene precedencia.

**Ejemplo:**

|Prefijo destino|Interfaz|
|---|---|
|`200.23.16.0/20`|0|
|`200.23.18.0/23`|1|
|Cualquier otro|2|

- Dirección `200.23.19.5`: coincide con `/20` (primeros 20 bits) y con `/23` (primeros 23 bits) → se usa **interfaz 1** (prefijo /23, más largo).
- Dirección `200.23.30.1`: coincide solo con `/20` → se usa **interfaz 0**.

</details>

---

**P4.2 (Fácil)** Explica qué es DHCP, los 4 mensajes del proceso, y por qué usa broadcast UDP en lugar de TCP.

<details> <summary>▶ Ver respuesta</summary>

**DHCP (Dynamic Host Configuration Protocol)** permite que un host obtenga automáticamente su configuración de red al conectarse: dirección IP, máscara de subred, dirección del router por defecto (gateway) y dirección del servidor DNS.

**Los 4 mensajes:**

1. **DHCP DISCOVER:** El cliente (sin IP) envía broadcast a `255.255.255.255` con IP origen `0.0.0.0`. "¿Hay algún servidor DHCP en la red?"
2. **DHCP OFFER:** El servidor responde (broadcast o unicast) ofreciendo una IP disponible, con el tiempo de lease.
3. **DHCP REQUEST:** El cliente acepta la oferta enviando broadcast "Quiero usar esa IP". Se hace broadcast para que otros servidores DHCP sepan que su oferta fue rechazada.
4. **DHCP ACK:** El servidor confirma la asignación con todos los parámetros de configuración.

**¿Por qué UDP y no TCP?**

- El cliente aún **no tiene dirección IP** al hacer el DISCOVER. Sin IP no puede establecer una conexión TCP (que requiere IPs para el handshake).
- El broadcast (`255.255.255.255`) no es enrutable por TCP.
- La transacción es corta (4 mensajes) y si falla, el cliente simplemente reintenta — no necesita la confiabilidad de TCP.

</details>

---

**P4.3 (Intermedia)** Un datagrama IPv4 de 4400 bytes (cabecera de 20 bytes + 4380 bytes de datos) debe transmitirse por un enlace con MTU = 1500 bytes. ¿En cuántos fragmentos se divide? Para cada fragmento, indica: longitud total, identificador, flag MF, y desplazamiento (offset). Recuerda que el offset se expresa en unidades de 8 bytes.

<details> <summary>▶ Ver respuesta</summary>

**Datos del paquete original:**

- Longitud total: 4400 bytes
- Cabecera: 20 bytes
- Datos: 4380 bytes
- MTU: 1500 bytes → máximo de datos por fragmento: 1500 - 20 = **1480 bytes**

**Número de fragmentos:**

```
⌈4380 / 1480⌉ = ⌈2.96⌉ = 3 fragmentos
```

|Fragmento|Datos|Longitud total|ID|MF|Offset|
|---|---|---|---|---|---|
|1|1480 bytes (bytes 0-1479)|1500|x|1|0|
|2|1480 bytes (bytes 1480-2959)|1500|x|1|185|
|3|1420 bytes (bytes 2960-4379)|1440|x|0|370|

**Cálculo de offsets:**

- Frag 1: empieza en byte 0 → offset = 0/8 = **0**
- Frag 2: empieza en byte 1480 → offset = 1480/8 = **185**
- Frag 3: empieza en byte 2960 → offset = 2960/8 = **370**

**Verificación del tercer fragmento:**

- Datos restantes: 4380 - 1480 - 1480 = 1420 bytes
- Longitud total: 1420 + 20 = 1440 bytes ✓
- MF = 0 porque es el último fragmento ✓

El reensamblaje ocurre solo en el **host destino**, no en los routers intermedios.

</details>

---

**P4.4 (Revuscada)** Considera una red con el prefijo `192.168.1.0/24`. Se requiere dividirla en 4 subredes de igual tamaño. ¿Cuál sería el prefijo de cada subred? ¿Cuántos hosts válidos tiene cada una? ¿Qué dirección es el broadcast de la segunda subred? ¿Qué concepto de CIDR explica por qué esto funciona?

<details> <summary>▶ Ver respuesta</summary>

**Dividir /24 en 4 subredes iguales:** Para 4 subredes se necesitan 2 bits adicionales (2² = 4), por lo que el prefijo pasa de `/24` a `/26`.

**Las 4 subredes:**

|Subred|Prefijo|Rango de hosts|Broadcast|
|---|---|---|---|
|1|`192.168.1.0/26`|192.168.1.1 – 192.168.1.62|192.168.1.63|
|2|`192.168.1.64/26`|192.168.1.65 – 192.168.1.126|**192.168.1.127**|
|3|`192.168.1.128/26`|192.168.1.129 – 192.168.1.190|192.168.1.191|
|4|`192.168.1.192/26`|192.168.1.193 – 192.168.1.254|192.168.1.255|

**Hosts válidos por subred:**

```
2^(32-26) - 2 = 2^6 - 2 = 64 - 2 = 62 hosts
```

Se restan 2: la dirección de red (todos los bits de host = 0) y el broadcast (todos los bits de host = 1).

**Broadcast de la segunda subred:** `192.168.1.127`

**Concepto CIDR:** CIDR (Classless InterDomain Routing) permite usar prefijos de longitud arbitraria en lugar de las clases fijas A/B/C. Esto hace posible subdividir un bloque de direcciones de forma flexible — "pedir prestados" bits del campo de host para crear más subredes. La notación `a.b.c.d/x` indica que los primeros x bits son parte de red. Este mismo mecanismo permite la **agregación de rutas**: un ISP puede anunciar un único bloque `/20` que abarca múltiples organizaciones con `/24`.

</details>

---

**P4.5 (Revuscada)** NAT viola el principio end-to-end de Internet. Explica en qué consiste ese principio, por qué NAT lo viola específicamente, y cuáles son las consecuencias prácticas de esta violación. ¿Qué problema concreto genera NAT para un servidor detrás de NAT que quiere recibir conexiones entrantes?

<details> <summary>▶ Ver respuesta</summary>

**El principio end-to-end** (Saltzer, Reed y Clark, 1981) establece que la inteligencia y el estado deben estar en los **extremos** de la red (los hosts), no en los dispositivos intermedios. La red en el medio solo debe transportar paquetes. Las funciones que requieren conocimiento del contexto de la aplicación solo pueden implementarse correctamente en los extremos.

**¿Por qué NAT lo viola?** NAT opera en la capa 3 (IP) pero **modifica campos de capa 4** (puertos TCP/UDP) y mantiene estado por conexión (la tabla de traducción). Específicamente:

1. Reescribe las IPs y puertos de origen en los datagramas salientes.
2. Reescribe las IPs y puertos de destino en los datagramas entrantes.
3. Mantiene una tabla con el mapeo `(IP_privada:puerto_orig) ↔ (IP_pública:puerto_nuevo)`.

Esto rompe la abstracción de capas: un router debería solo mirar la cabecera IP, no el contenido de capa de transporte.

**Consecuencias de la violación:**

- Protocolos que llevan IPs o puertos en el **payload** (como FTP modo activo, SIP, H.323) se rompen porque NAT no sabe que debe traducir también esas IPs embebidas en los datos.
- Aplicaciones P2P, juegos y VoIP necesitan técnicas especiales (STUN, TURN, UPnP, hole punching) para funcionar.
- Dificulta diagnósticos de red y auditorías de seguridad.

**El problema del servidor detrás de NAT:** Un servidor en `192.168.1.5:8080` detrás de un NAT no tiene una IP pública propia. Cuando un cliente externo quiere conectarse, envía a la IP pública del NAT (`138.76.29.7`). Pero, ¿a qué puerto del NAT? Y si llega en el puerto correcto, ¿cómo sabe el NAT a qué dispositivo interno enviarlo? La tabla NAT solo tiene entradas de conexiones _salientes_ iniciadas desde adentro. Para conexiones _entrantes_ no hay entrada automática. Soluciones: **port forwarding** manual (el administrador configura que el puerto X del NAT siempre vaya a la IP:puerto internos), o protocolos de traversal como STUN/TURN/UPnP.

</details>

---

_Basado en: Computer Networking: A Top-Down Approach, 8ª edición — Jim Kurose, Keith Ross, Pearson 2020._