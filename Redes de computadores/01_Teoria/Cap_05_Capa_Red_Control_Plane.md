# Capítulo 5: Capa de Red — Control Plane (Plano de Control)
### Resumen detallado para certamen
> Computer Networking: A Top-Down Approach — Kurose & Ross, 8ª ed.

---

## Índice
1. [Plano de Datos vs. Plano de Control](#1-plano-de-datos-vs-plano-de-control)
2. [Algoritmos de Enrutamiento](#2-algoritmos-de-enrutamiento)
3. [Dijkstra — Link State (LS)](#3-dijkstra--link-state-ls)
4. [Bellman-Ford — Distance Vector (DV)](#4-bellman-ford--distance-vector-dv)
5. [Escalabilidad: Sistemas Autónomos (AS)](#5-escalabilidad-sistemas-autónomos-as)
6. [Enrutamiento Intra-AS: OSPF](#6-enrutamiento-intra-as-ospf)
7. [Enrutamiento Inter-AS: BGP](#7-enrutamiento-inter-as-bgp)
8. [SDN — Plano de Control Centralizado](#8-sdn--plano-de-control-centralizado)
9. [ICMP — Mensajes de Control](#9-icmp--mensajes-de-control)
10. [Gestión de Red: SNMP y NETCONF/YANG](#10-gestión-de-red-snmp-y-netconfyang)
11. [Temas frecuentes de certamen](#11-temas-frecuentes-de-certamen)

---

## 1. Plano de Datos vs. Plano de Control

Repaso clave antes de entrar al capítulo:

| | Plano de Datos | Plano de Control |
|--|----------------|------------------|
| **¿Qué hace?** | Mueve paquetes del puerto de entrada al puerto de salida correcto (forwarding) | Determina la ruta que siguen los paquetes de extremo a extremo (routing) |
| **Alcance** | Local (dentro de un router) | Global (toda la red) |
| **Velocidad** | Nanosegundos (hardware) | Milisegundos (software) |
| **Capítulo** | Capítulo 4 | **Capítulo 5** |

### Dos enfoques para el plano de control

**Enfoque tradicional — Per-Router Control:**
Cada router corre su propio algoritmo de enrutamiento (OSPF, BGP, RIP). Los routers se comunican entre sí para construir sus propias tablas de reenvío. Sistema distribuido, descentralizado.

```
Router A ←──── protocolo ────► Router B
   │                               │
[tabla de reenvío propia]    [tabla de reenvío propia]
```

**Enfoque SDN — Control Centralizado:**
Un controlador remoto centralizado (software) calcula las rutas y las instala en todos los routers. Los routers son "tontos" — solo hacen forwarding según lo que el controlador les diga.

```
         [Controlador SDN]
        /        |        \
   Router A  Router B  Router C
   (solo forwarding, sin routing propio)
```

---

## 2. Algoritmos de Enrutamiento

### ¿Qué objetivo tienen?

Determinar las **rutas de menor costo** (o equivalentes) desde los hosts emisores hasta los receptores, a través de la red de routers.

**¿Qué es una "buena" ruta?**
- Menor costo total.
- Mayor velocidad.
- Menor congestión.

El costo de un enlace lo define el operador de red: puede ser siempre 1, inversamente proporcional al ancho de banda, o proporcional a la congestión actual.

### Abstracción de grafo

La red se modela como un **grafo**:
- **Nodos** = routers.
- **Aristas** = enlaces físicos.
- **Peso de cada arista** = costo del enlace.

```
        5
  u ─────────── v
  │             │
1 │             │ 2
  │      3      │
  w ─────────── x
```

### Clasificación de algoritmos de enrutamiento

| Criterio | Tipo 1 | Tipo 2 |
|---------|--------|--------|
| **Información disponible** | **Link State (LS):** conocimiento global — todos conocen la topología completa | **Distance Vector (DV):** conocimiento local — cada nodo solo conoce a sus vecinos directos |
| **Dinamismo** | **Estático:** rutas cambian raramente | **Dinámico:** rutas se actualizan automáticamente ante cambios |

---

## 3. Dijkstra — Link State (LS)

### Idea central

**Centralizado:** toda la topología y los costos de los enlaces son conocidos por **todos los nodos** antes de calcular. Esto se logra mediante **link state broadcast** — cada router difunde su información de enlaces a todos los demás.

**Resultado:** calcula la ruta de menor costo desde un nodo origen hacia **todos los demás nodos**. Genera la tabla de reenvío completa para ese nodo.

**Iterativo:** después de k iteraciones, se conoce definitivamente la ruta de menor costo hacia k destinos.

---

### Notación

| Símbolo | Significado |
|---------|-------------|
| `c(x,y)` | Costo del enlace directo entre nodos x e y. Si no son vecinos = ∞ |
| `D(v)` | Estimación actual del costo de la ruta de menor costo desde el origen hasta v |
| `p(v)` | Nodo predecesor en la ruta desde el origen hasta v |
| `N'` | Conjunto de nodos cuya ruta de menor costo ya se conoce definitivamente |

---

### Algoritmo paso a paso

```
Inicialización:
  N' = {u}   (u = nodo origen)
  Para cada nodo v:
    Si v es vecino de u: D(v) = c(u,v)
    Si no:               D(v) = ∞

Bucle (repetir hasta que todos los nodos estén en N'):
  1. Encontrar el nodo w ∉ N' con el menor D(w)
  2. Agregar w a N'
  3. Para cada vecino v de w que no esté en N':
     D(v) = min(D(v),  D(w) + c(w,v))
     Si D(v) se actualizó: p(v) = w
```

---

### Ejemplo completo

Red con nodos u, v, w, x, y, z:

```
        2       1
  u ───────v ───────x
  │  \     │         \
1 │   5\   1│         2\ 
  │     \   │           \
  w──────x  y ───────────z
      3         2
```

Supón costos: u-v=2, u-w=5, u-x=1, v-x=2, x-w=3, x-y=1, y-z=2, v-y=1

**Tabla de iteraciones:**

| Paso | N' | D(v) p(v) | D(w) p(w) | D(x) p(x) | D(y) p(y) | D(z) p(z) |
|------|-----|-----------|-----------|-----------|-----------|-----------|
| Inicio | {u} | 2, u | 5, u | 1, u | ∞ | ∞ |
| 1 | {u,x} | 2, u | 4, x | — | 2, x | ∞ |
| 2 | {u,x,v} | — | 4, x | — | 2, x | ∞ |
| 3 | {u,x,v,y} | — | 4, x | — | — | 4, y |
| 4 | {u,x,v,y,w} | — | — | — | — | 4, y |
| 5 | {u,x,v,y,w,z} | — | — | — | — | — |

---

### Complejidad

**Complejidad del algoritmo:**
- Cada iteración revisa todos los nodos fuera de N' → n(n+1)/2 comparaciones.
- Complejidad: **O(n²)**
- Con implementaciones eficientes (heap): **O(n log n)**

**Complejidad de mensajes:**
- Cada router difunde su estado de enlace a todos los demás (n routers).
- Cada mensaje cruza O(n) enlaces → complejidad total: **O(n²)**

---

### Problema: Oscilaciones de Dijkstra

Cuando los costos de los enlaces **dependen del volumen de tráfico** (congestión), el algoritmo puede oscilar:

1. Todos calculan rutas con costos actuales → el tráfico se redistribuye.
2. Los costos cambian → todos recalculan → el tráfico se redistribuye de nuevo.
3. Los costos vuelven a cambiar → bucle infinito de oscilaciones.

**Ejemplo:** si todos los routers eligen la misma ruta por ser la más barata ahora, esa ruta se congestiona, su costo sube, y en el siguiente ciclo todos se van por otra ruta, congestionándola, y así infinitamente.

**Solución práctica:** aleatorizar el tiempo de ejecución del algoritmo en cada router para que no todos recalculen al mismo tiempo.

---

## 4. Bellman-Ford — Distance Vector (DV)

### Idea central

**Distribuido:** cada nodo solo conoce los costos hacia sus **vecinos directos**, no la topología completa.

**Iterativo y asíncrono:** cada nodo actualiza su vector de distancia cuando recibe nueva información de un vecino.

**Autodetenido:** el proceso se detiene solo cuando ya no hay cambios — ningún nodo necesita notificar si nada cambió.

---

### Ecuación de Bellman-Ford

Sea `dx(y)` el costo del camino de menor costo de x a y. Entonces:

```
dx(y) = min sobre todos los vecinos v { c(x,v) + dv(y) }
```

**Interpretación:** el costo mínimo de x a y es el mínimo entre todos los vecinos v de x de: el costo directo a v más el costo de v a y.

---

### Funcionamiento del algoritmo DV

**Cada nodo:**
1. Espera: un cambio en el costo de enlace local, o un mensaje de vector de distancia de algún vecino.
2. Recalcula su propio vector de distancia usando la ecuación de Bellman-Ford:
   ```
   Dx(y) ← min_v { c(x,v) + Dv(y) }  para cada nodo y
   ```
3. Si alguna estimación cambió → notifica a sus vecinos.
4. Si nada cambió → no hace nada.

**Propiedades:**
- **Iterativo:** cada actualización local puede disparar actualizaciones en vecinos.
- **Asíncrono:** los nodos no se sincronizan — actúan cuando tienen nueva información.
- **Distribuido:** no hay nodo central.
- **Autodetenido:** converge sin intervención externa.

---

### Comparación LS vs DV

| Característica | Link State (Dijkstra) | Distance Vector (Bellman-Ford) |
|----------------|----------------------|-------------------------------|
| **Información** | Topología completa conocida por todos | Solo vecinos directos |
| **Mensajes** | Broadcast de estado de enlace a todos | Solo intercambio con vecinos |
| **Velocidad de convergencia** | Más rápido (O(n²)) | Más lento, puede oscilar |
| **Robustez** | Si un nodo falla, solo afecta su info local | Un nodo mal puede propagar info incorrecta |
| **Complejidad** | Mayor (broadcast global) | Menor (solo vecinos) |
| **Problema** | Oscilaciones con costos variables | Problema del count-to-infinity |
| **Protocolo real** | OSPF, IS-IS | RIP, BGP (variante) |

### Problema count-to-infinity (DV)

Cuando el costo de un enlace **aumenta** (o un enlace se cae), los nodos pueden tardar mucho en converger porque propagan información obsoleta en bucle:

```
x ─── y ─── z

Si el enlace x-y se cae:
- y cree que puede llegar a x a través de z (con costo 2+1=3)
- z actualiza: puede llegar a x a través de y (con costo 3+1=4)
- y actualiza: puede llegar a x a través de z (con costo 4+1=5)
... sigue aumentando hasta ∞
```

**Solución: Poisoned Reverse** — si z llega a x a través de y, z le dice a y que su distancia a x es ∞ (envenena esa ruta). Así y no intenta usar z para llegar a x.

---

## 5. Escalabilidad: Sistemas Autónomos (AS)

### ¿Por qué no funciona el enrutamiento simple a escala?

Internet tiene **miles de millones de destinos**. Si intentáramos guardar todos en una tabla de enrutamiento única:
- Las tablas serían enormes → sin memoria suficiente.
- El intercambio de tablas inundaría los enlaces.
- No hay autonomía administrativa: cada ISP quiere controlar su propia red.

### Solución: Sistemas Autónomos (AS)

Se agrupan los routers en regiones llamadas **Sistemas Autónomos (AS)** (también llamados dominios).

```
┌──────────────────┐     ┌──────────────────┐
│       AS1        │     │       AS2        │
│  R1 ─── R2 ─── R3│─────│R4 ─── R5 ─── R6  │
│         │        │     │                  │
└─────────┼────────┘     └──────────────────┘
          │
    ┌─────┴──────┐
    │    AS3     │
    │ R7 ─── R8  │
    └────────────┘
```

**Enrutamiento intra-AS (intradominio):** entre routers dentro del mismo AS. Todos los routers del AS corren el mismo protocolo intradominio. Enfocado en **rendimiento**.

**Enrutamiento inter-AS (interdominio):** entre distintos AS. Los routers de borde (gateway routers) conectan AS entre sí. Dominado por **políticas**.

**Router de puerta de enlace (gateway router):** router en el borde de un AS. Tiene enlaces a routers de otros AS y participa en enrutamiento inter-AS además del intra-AS.

---

## 6. Enrutamiento Intra-AS: OSPF

### ¿Qué es OSPF?

**OSPF (Open Shortest Path First)** es el protocolo de enrutamiento intra-AS más usado en Internet. Usa el **algoritmo de Link State (Dijkstra)**.

- Cada router difunde su información de estado de enlace a **todos los routers del AS** (no solo a vecinos).
- Cada router construye el mapa completo de la topología del AS.
- Cada router corre Dijkstra localmente para calcular sus rutas.

### OSPF Jerárquico

Para AS muy grandes, OSPF organiza los routers en una **jerarquía de dos niveles**:

```
         ┌─────────────────────────────────┐
         │          BACKBONE (Área 0)       │
         │   ─── R_backbone ─── R_backbone  │
         └───────┬──────────────────┬───────┘
                 │                  │
        ┌────────┴───┐      ┌───────┴───────┐
        │   Área 1   │      │    Área 2     │
        │  R1 ─── R2 │      │  R3 ─── R4   │
        └────────────┘      └───────────────┘
```

- **Área local:** los anuncios de estado de enlace se difunden solo dentro del área. Cada nodo conoce la topología detallada de su área.
- **Backbone (área 0):** conecta todas las áreas entre sí. Los routers de borde de área resumen la información de su área al backbone.

**Ventaja:** los routers de una área solo necesitan conocer la topología de su área, no de todo el AS. Reduce el tamaño de las tablas y el tráfico de actualización.

### Otros protocolos intra-AS

| Protocolo | Algoritmo | Estado |
|-----------|-----------|--------|
| **RIP** | Distance Vector (DV). DVs intercambiados cada 30 segundos | Obsoleto, ya no se usa ampliamente |
| **EIGRP** | Basado en DV. Desarrollado por Cisco, abierto en 2013 | Usado en redes Cisco |
| **OSPF** | Link State (Dijkstra) | El más usado actualmente |
| **IS-IS** | Equivalente a OSPF, estándar ISO | Usado en ISPs grandes |

---

## 7. Enrutamiento Inter-AS: BGP

### ¿Qué es BGP?

**BGP (Border Gateway Protocol)** es el protocolo de enrutamiento inter-AS. Es el "pegamento que mantiene unida a Internet".

A diferencia de OSPF (que busca la ruta más corta), **BGP está orientado a políticas**: los AS deciden qué rutas aceptar y anunciar basándose en acuerdos económicos y políticas de negocio.

### eBGP e iBGP

**eBGP (external BGP):** sesión BGP entre routers de borde de **distintos AS**. Obtiene información de accesibilidad de AS vecinos.

**iBGP (internal BGP):** sesión BGP entre routers **dentro del mismo AS**. Propaga la información de accesibilidad aprendida via eBGP a todos los routers internos del AS.

```
  AS1                   AS2                  AS3
┌────────┐           ┌────────┐           ┌────────┐
│  1a    │◄─ eBGP ──►│  2c    │◄─ eBGP ──►│  3a    │
│  1b    │           │  2a    │           │  3b    │
│  1c    │           │  2b ───┤           └────────┘
└────────┘           │  2d    │
        ↑─── iBGP ───┘
```

**iBGP propaga** a todos los routers del AS la información que el router de borde aprendió via eBGP. Así todos los routers del AS saben cómo llegar a destinos externos.

---

### Atributos de ruta BGP

Cuando BGP anuncia una ruta, incluye el **prefijo** más sus **atributos**:

**AS-PATH:** lista de AS por los que pasó el anuncio.
- Ejemplo: para llegar a la red X, el path es `AS3 → AS2 → AS1`.
- Se usa para detectar loops (si aparece mi propio AS en el path, rechazo la ruta).
- Se prefiere el AS-PATH más corto.

**NEXT-HOP:** IP del router que es el siguiente salto hacia el destino anunciado.

---

### Selección de ruta BGP

Cuando un router conoce múltiples rutas hacia el mismo destino, selecciona en este orden de preferencia:

1. **Valor de preferencia local** (local preference): decisión de política, configurada por el administrador. Tiene la mayor prioridad.
2. **AS-PATH más corto:** menos saltos de AS.
3. **Router NEXT-HOP más cercano:** enrutamiento de "papa caliente" (hot potato routing).
4. **Criterios adicionales** (ID de router, etc.).

---

### Hot Potato Routing (Enrutamiento de papa caliente)

**Idea:** cuando hay múltiples rutas posibles hacia el mismo destino externo, el AS elige la que tiene el **menor costo intradominio** hasta el punto de salida, sin importar el costo entre dominios.

```
AS2:
  2d quiere enviar tráfico a X
  Puede salir por 2a (costo interno = 1) → ruta AS2, AS3, X  
  Puede salir por 2c (costo interno = 5) → ruta AS3, X (más corta en AS-hops)
  
  Hot potato elige 2a (costo interno menor), aunque AS-PATH sea más largo.
```

**Lógica:** "deshacerse del paquete lo más rápido posible dentro de mi AS" — como una papa caliente que quemas y pasas.

---

### Anuncio de rutas BGP — ejemplo

1. Gateway 3a de AS3 anuncia `AS3, X` a gateway 2c de AS2 via eBGP.
   - AS3 promete a AS2: "puedo reenviar tráfico hacia X".
2. AS2 acepta la ruta y la propaga internamente via iBGP a todos sus routers.
3. Gateway 2a de AS2 anuncia `AS2, AS3, X` a gateway 1c de AS1 via eBGP.
4. AS1 ahora también puede conocer la ruta directa `AS3, X` via eBGP desde 3a.
5. AS1 compara `AS2, AS3, X` vs `AS3, X` → elige `AS3, X` (AS-PATH más corto).

---

### Políticas BGP

**BGP es un protocolo de vector de ruta (path vector)**, no de vector de distancia. La gran diferencia es que BGP propaga el **camino completo** (lista de AS), no solo el costo. Esto permite políticas:

- Un ISP puede **no anunciar** ciertas rutas a ciertos vecinos por razones económicas.
- Un ISP puede **preferir** rutas por AS con los que tiene acuerdos de peering.
- Un ISP solo anuncia destinos accesibles **para sus clientes**, no tráfico de tránsito entre otros ISPs.

**Ejemplo de política:**
```
A ──── B ──── C
       │
       w

A anuncia ruta Aw a B y C.
B NO anuncia ruta BAw a C (B no gana dinero por enrutar tráfico entre C y A).
C no aprende sobre BAw → C usa CAw directamente.
```

---

### Mensajes BGP

Los pares BGP intercambian mensajes sobre una **conexión TCP semi-permanente**.

| Mensaje | Función |
|---------|---------|
| **OPEN** | Abre la conexión TCP y autentica al par |
| **UPDATE** | Anuncia una nueva ruta o retira una antigua |
| **KEEPALIVE** | Mantiene viva la conexión; confirma el OPEN |
| **NOTIFICATION** | Informa errores en el mensaje anterior; cierra la conexión |

---

### ¿Por qué protocolos distintos intra e inter AS?

| Criterio | Intra-AS (OSPF) | Inter-AS (BGP) |
|----------|-----------------|----------------|
| **Prioridad** | Rendimiento (velocidad, costo) | Política (acuerdos económicos, control de tráfico) |
| **Administración** | Un solo administrador → política simple | Múltiples organizaciones → políticas complejas |
| **Escala** | Solo el AS propio | Toda la Internet |
| **Algoritmo** | Link State (Dijkstra) | Path Vector (variante de DV) |

---

## 8. SDN — Plano de Control Centralizado

### El problema con el enfoque tradicional

El enfoque tradicional tiene limitaciones para la **ingeniería de tráfico** (traffic engineering):

- ¿El operador quiere que el tráfico u→z vaya por uvwz en vez de uxyz? → Tiene que redefinir pesos de todos los enlaces.
- ¿Quiere dividir el tráfico u→z entre dos rutas (load balancing)? → Imposible con routing tradicional.
- ¿Quiere tratar distintos tipos de tráfico (azul/rojo) diferente? → Imposible con forwarding basado en destino.

### La solución SDN

**SDN (Software-Defined Networking)** separa completamente el plano de datos del plano de control:

```
┌─────────────────────────────────────┐
│     Aplicaciones de control         │  ← "cerebros": routing, load balancing, firewall
│  (routing, load balancing, etc.)    │
├─────────────────────────────────────┤
│       Controlador SDN               │  ← sistema operativo de red
│  (mantiene estado global de la red) │
├────────┬──────────┬─────────────────┤
│Switch 1│ Switch 2 │    Switch 3     │  ← plano de datos: solo forwarding
└────────┴──────────┴─────────────────┘
```

### Los tres componentes SDN

**1. Switches del plano de datos:**
- Hardware simple y rápido.
- Solo implementan forwarding generalizado (match+action).
- Su tabla de flujo es calculada e instalada por el controlador.
- API abierta (OpenFlow) → controlable por el controlador.

**2. Controlador SDN (Network OS):**
- Mantiene información del estado completo de la red.
- Interactúa hacia arriba (northbound API) con las aplicaciones de control.
- Interactúa hacia abajo (southbound API) con los switches via OpenFlow.
- Implementado como sistema **distribuido** para rendimiento, escalabilidad y tolerancia a fallos.

**3. Aplicaciones de control de red:**
- Implementan la lógica de control: routing, firewalls, load balancers, etc.
- Pueden ser de terceros — desacopladas del hardware.
- Usan los servicios del controlador para "programar" la red.

---

### Protocolo OpenFlow

Opera entre el controlador y los switches. Usa **TCP** para el intercambio de mensajes (cifrado opcional).

**Mensajes del controlador al switch:**

| Mensaje | Función |
|---------|---------|
| `features` | Controlador consulta capacidades del switch |
| `configure` | Controlador establece parámetros del switch |
| `modify-state` | Agrega, elimina o modifica entradas en la tabla de flujo |
| `packet-out` | Controlador envía un paquete por un puerto específico del switch |

**Mensajes del switch al controlador:**

| Mensaje | Función |
|---------|---------|
| `packet-in` | Transfiere el paquete al controlador (cuando no hay regla que aplique) |
| `flow-removed` | Notifica que una entrada de flujo fue eliminada |
| `port-status` | Informa cambio en el estado de un puerto |

---

### Ventajas del control SDN centralizado

- **Gestión más sencilla:** configuración central, sin configurar cada router individualmente.
- **Mayor flexibilidad:** se pueden instalar reglas de forwarding complejas fácilmente.
- **Apertura:** implementación no propietaria del plano de control.
- **Ingeniería de tráfico:** load balancing, políticas por flujo, todo posible.
- **Programabilidad:** la red se puede "programar" como si fuera software.

### Desafíos SDN

- **Robustez:** el controlador es un punto de falla → debe ser distribuido y tolerante a fallos.
- **Seguridad:** un controlador comprometido puede afectar toda la red.
- **Escalabilidad:** funciona bien dentro de un AS, más difícil a escala de Internet.
- **Latencia:** la comunicación controlador-switch añade retardo.

---

## 9. ICMP — Mensajes de Control

### ¿Qué es ICMP?

**ICMP (Internet Control Message Protocol)** es usado por hosts y routers para **comunicar información de control a nivel de red**.

Aunque opera "por encima" de IP (los mensajes ICMP viajan dentro de datagramas IP), conceptualmente pertenece a la capa de red.

### Funciones principales

- **Reporte de errores:** host inalcanzable, red inalcanzable, puerto inalcanzable, protocolo inalcanzable.
- **Solicitud/respuesta de eco:** usado por el comando **ping**.
- **TTL expirado:** cuando un datagrama llega a TTL=0 en un router, ese router envía un ICMP "Time Exceeded" al origen. Esto es la base de **traceroute**.

### Tipos de mensajes ICMP más importantes

| Tipo | Código | Descripción |
|------|--------|-------------|
| 0 | 0 | Echo reply (respuesta a ping) |
| 3 | 0 | Destination network unreachable |
| 3 | 1 | Destination host unreachable |
| 3 | 3 | Destination port unreachable |
| 4 | 0 | Source quench (control de congestión obsoleto) |
| 8 | 0 | Echo request (ping) |
| 11 | 0 | TTL expired (usado por traceroute) |

### Traceroute y ICMP

`traceroute` usa ICMP tipo 11 (TTL expired):
1. Envía datagramas UDP con TTL=1 → el primer router lo decrementa a 0 → envía ICMP "TTL expired" al origen.
2. Envía con TTL=2 → el segundo router responde.
3. Continúa hasta llegar al destino.
4. El destino devuelve ICMP tipo 3 "port unreachable" (usa un puerto UDP poco probable).

El emisor mide el RTT a cada salto usando los tiempos de respuesta.

---

## 10. Gestión de Red: SNMP y NETCONF/YANG

### ¿Qué es la gestión de red?

Las redes son sistemas complejos con miles de componentes. Se necesitan herramientas para **monitorear, configurar y controlar** los dispositivos.

### Componentes de la gestión de redes

| Componente | Función |
|------------|---------|
| **Servidor de gestión** | Aplicación central con el administrador humano en el circuito |
| **Protocolo de gestión** | Usado para consultar, configurar y gestionar dispositivos (SNMP, NETCONF) |
| **Dispositivo gestionado** | Router, switch, host — con componentes configurables |
| **Datos** | Estado del dispositivo, datos operativos, estadísticas |

### Enfoques de gestión

| Enfoque | Descripción |
|---------|-------------|
| **CLI** | El administrador escribe comandos directamente en cada dispositivo via SSH |
| **SNMP/MIB** | Protocolo para consultar y modificar variables de estado de dispositivos |
| **NETCONF/YANG** | Gestión abstracta y holística de toda la red, basada en modelos de datos |

---

### SNMP (Simple Network Management Protocol)

**Objetivo:** permitir al servidor de gestión consultar y modificar variables de estado en dispositivos remotos.

**MIB (Management Information Base):** base de datos de variables del dispositivo. Hay ~400 módulos MIB estándar definidos en RFC, más MIBs específicas de fabricantes.

**Dos modos de operación SNMP:**

**1. Request-Response (consulta):**
```
Servidor de gestión ──► GET/SET ──► Agente SNMP (en el dispositivo)
                    ◄── Respuesta ◄──
```

**2. Trap (notificación proactiva):**
```
Agente SNMP (detecta evento) ──► TRAP ──► Servidor de gestión
```
El dispositivo notifica al servidor cuando ocurre algo importante (ej: enlace caído) sin que el servidor lo haya preguntado.

**Tipos de mensajes SNMP:**

| Mensaje | Dirección | Función |
|---------|-----------|---------|
| `GetRequest` | Manager → Agente | Solicita el valor de una o más variables MIB |
| `GetNextRequest` | Manager → Agente | Solicita la siguiente variable en la MIB |
| `GetBulkRequest` | Manager → Agente | Solicita muchas variables en una sola petición |
| `InformRequest` | Manager → Manager | Transfiere información entre servidores de gestión |
| `SetRequest` | Manager → Agente | Modifica el valor de una variable MIB |
| `Response` | Agente → Manager | Responde a cualquier solicitud |
| `Trap` | Agente → Manager | Notificación asíncrona de un evento |

---

### NETCONF/YANG

**NETCONF (Network Configuration Protocol):**
- Objetivo: gestionar y **configurar activamente** dispositivos en toda la red.
- Opera entre el servidor de gestión y los dispositivos.
- Acciones: recuperar, configurar, modificar y activar configuraciones.
- Permite **acciones atómicas en múltiples dispositivos** (todo o nada).
- Mensajes codificados en **XML**.
- Transmitido sobre protocolo seguro (TLS).
- Paradigma **RPC (Remote Procedure Call)**.

**YANG:**
- Lenguaje de **modelado de datos** para especificar la estructura, sintaxis y semántica de los datos de gestión NETCONF.
- Define qué variables existen, qué tipos tienen y qué restricciones deben cumplir.
- Un documento XML que describe las capacidades del dispositivo puede generarse automáticamente desde la descripción YANG.
- Garantiza que las configuraciones NETCONF cumplan restricciones de **corrección y coherencia**.

**Comparación SNMP vs NETCONF:**

| | SNMP | NETCONF/YANG |
|--|------|--------------|
| **Enfoque** | Variables individuales | Configuración completa del dispositivo |
| **Alcance** | Un dispositivo a la vez | Múltiples dispositivos coordinados |
| **Lenguaje** | ASN.1/BER | XML/YANG |
| **Transacciones** | No atómicas | Atómicas (commit de múltiples cambios) |
| **Uso típico** | Monitoreo, estadísticas | Configuración, gestión activa |

---

## 11. Temas frecuentes de certamen

### ✅ Preguntas conceptuales frecuentes

**1. Forwarding vs. Routing (repaso)**
- Forwarding = local, nanosegundos, hardware, plano de datos.
- Routing = global, milisegundos, software, plano de control.

**2. LS vs. DV**
- LS (Dijkstra): conocimiento global, broadcast, más rápido de converger, oscilaciones posibles.
- DV (Bellman-Ford): conocimiento local, solo vecinos, más lento, count-to-infinity.

**3. Dijkstra — complejidad**
- O(n²) en la versión básica.
- O(n log n) con implementaciones eficientes (heap).

**4. Por qué AS y dos tipos de enrutamiento**
- Escala: no caben todos los destinos en una tabla.
- Autonomía: cada red quiere controlar su propia política.
- Intra-AS: optimizar rendimiento dentro de la red.
- Inter-AS: políticas entre organizaciones distintas.

**5. OSPF**
- Usa Link State (Dijkstra) dentro del AS.
- Cada router difunde su estado a todos los demás del AS.
- Jerárquico: área local + backbone (área 0).

**6. BGP**
- Protocolo inter-AS, orientado a políticas.
- eBGP: entre AS distintos. iBGP: dentro del mismo AS.
- Atributos: AS-PATH (lista de AS) y NEXT-HOP.
- Selección: preferencia local → AS-PATH más corto → hot potato.

**7. Hot Potato Routing**
- Elegir el punto de salida del AS con menor costo intradominio.
- "Deshacerse del paquete lo más rápido posible".
- No considera el costo inter-dominio.

**8. SDN**
- Separa plano de datos (switches) del plano de control (controlador).
- Switches son "tontos" — solo hacen forwarding.
- Controlador centralizado instala tablas de flujo via OpenFlow.
- Ventaja: flexibilidad, programabilidad, gestión centralizada.

**9. ICMP**
- Protocolo de mensajes de control de red.
- Viaja dentro de datagramas IP.
- Ping usa tipo 8 (request) y tipo 0 (reply).
- Traceroute usa TTL expirado (tipo 11).

**10. SNMP vs NETCONF**
- SNMP: monitoreo y consulta de variables individuales. Traps para notificaciones.
- NETCONF: configuración activa de múltiples dispositivos con transacciones atómicas.
- YANG: lenguaje de modelado para definir la estructura de los datos NETCONF.

---

### ✅ Fórmulas y complejidades clave

| Concepto | Valor |
|----------|-------|
| Complejidad Dijkstra (básico) | O(n²) |
| Complejidad Dijkstra (eficiente) | O(n log n) |
| Complejidad mensajes Dijkstra | O(n²) |
| Bellman-Ford: ecuación | `dx(y) = min_v { c(x,v) + dv(y) }` |
| Convergencia DV | Asíncrona, puede ser lenta (count-to-infinity) |

---

### ✅ Trampas frecuentes de certamen

- ❌ "OSPF usa Distance Vector" → **Falso.** OSPF usa Link State (Dijkstra).
- ❌ "RIP sigue siendo el protocolo intra-AS más usado" → **Falso.** RIP está obsoleto. OSPF es el dominante.
- ❌ "BGP elige siempre la ruta con menor número de saltos" → **Falso.** BGP prioriza preferencia local (política), luego AS-PATH más corto, luego hot potato.
- ❌ "iBGP y eBGP son lo mismo" → **Falso.** eBGP = entre AS distintos. iBGP = dentro del mismo AS para propagar rutas aprendidas.
- ❌ "En SDN, los switches calculan sus propias tablas de reenvío" → **Falso.** El controlador centralizado las calcula e instala.
- ❌ "ICMP es un protocolo de capa de aplicación" → **Falso.** Es de capa de red, aunque viaja dentro de datagramas IP.
- ❌ "SNMP y NETCONF hacen lo mismo" → **Falso.** SNMP es para monitoreo/consulta de variables. NETCONF es para configuración activa y coordinada de múltiples dispositivos.
- ❌ "En DV, cada nodo conoce la topología completa" → **Falso.** En DV solo se conocen los vecinos directos. La topología completa es propia de LS.
- ❌ "Hot potato routing minimiza el costo total del camino" → **Falso.** Solo minimiza el costo intradominio hasta el punto de salida, ignorando el costo entre AS.
- ❌ "BGP garantiza entrega confiable usando TCP" → **Parcialmente cierto pero incompleto.** BGP usa TCP para la sesión entre pares, pero BGP en sí es un protocolo de control, no de datos. La confiabilidad de TCP aplica al intercambio de mensajes BGP, no a los datagramas de datos de los usuarios.

---

*Basado en: Computer Networking: A Top-Down Approach, 8ª edición — Jim Kurose, Keith Ross, Pearson 2020.*
