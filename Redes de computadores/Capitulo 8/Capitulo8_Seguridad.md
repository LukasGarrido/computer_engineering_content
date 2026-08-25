# Capítulo 8: Seguridad en Redes
### Explicación Detallada — *Computer Networking: A Top-Down Approach* (Kurose & Ross, 8ª ed.)

---

## Tabla de Contenidos

1. [¿Qué es la seguridad en redes?](#1-qué-es-la-seguridad-en-redes)
2. [Principios de Criptografía](#2-principios-de-criptografía)
3. [Autenticación e Integridad de Mensajes](#3-autenticación-e-integridad-de-mensajes)
4. [Seguridad en el Correo Electrónico](#4-seguridad-en-el-correo-electrónico)
5. [TLS — Seguridad en la Capa de Transporte](#5-tls--seguridad-en-la-capa-de-transporte)
6. [IPsec — Seguridad en la Capa de Red](#6-ipsec--seguridad-en-la-capa-de-red)
7. [Seguridad en Redes Inalámbricas y Móviles](#7-seguridad-en-redes-inalámbricas-y-móviles)
8. [Firewalls e IDS](#8-firewalls-e-ids)

---

## 1. ¿Qué es la seguridad en redes?

### Los cuatro pilares de la seguridad

Antes de hablar de técnicas, hay que entender **qué propiedades queremos garantizar**:

| Propiedad | Definición | Ejemplo |
|---|---|---|
| **Confidencialidad** | Solo el emisor y el receptor legítimo pueden entender el contenido del mensaje | Nadie más puede leer tus mensajes aunque los intercepte |
| **Autenticación** | Emisor y receptor pueden confirmar mutuamente su identidad | Saber que realmente estás hablando con tu banco, no con un impostor |
| **Integridad del mensaje** | El mensaje no fue alterado en tránsito (ni después) sin que se detecte | El documento que recibes es exactamente el que enviaron |
| **Acceso y disponibilidad** | Los servicios deben estar disponibles para los usuarios legítimos | Tu banco online no puede estar caído por un ataque |

### Los personajes del capítulo

El capítulo usa tres personajes para ilustrar los escenarios:
- **Alice y Bob**: quieren comunicarse de forma segura
- **Trudy** (intruder): el atacante que intenta interferir

### ¿Qué puede hacer un atacante?

- **Eavesdrop (escucha pasiva)**: interceptar mensajes sin modificarlos
- **Inserción activa**: inyectar mensajes falsos en la conexión
- **Impersonación (spoofing)**: falsificar la dirección origen de un paquete
- **Hijacking**: "secuestrar" una conexión en curso, removiendo al emisor o receptor real e insertándose en su lugar
- **Denial of Service (DoS)**: impedir que el servicio sea usado por otros (ej. saturando los recursos del servidor)

---

## 2. Principios de Criptografía

### El lenguaje de la criptografía

```
EMISOR                                          RECEPTOR
Alice                                           Bob

Texto plano  →  [Algoritmo de cifrado]  →  Texto cifrado  →  [Algoritmo de descifrado]  →  Texto plano
    m              usando clave KA               KA(m)              usando clave KB              m
```

- **m**: el mensaje original (plaintext)
- **KA(m)**: el mensaje cifrado con la clave KA
- **m = KB(KA(m))**: el receptor recupera m aplicando KB

### Tipos de ataques a un sistema de cifrado

- **Cipher-text only attack**: Trudy solo tiene el texto cifrado y trata de deducir el original (análisis estadístico, fuerza bruta)
- **Known-plaintext attack**: Trudy tiene pares (texto plano, texto cifrado) y usa esa información para atacar
- **Chosen-plaintext attack**: Trudy puede elegir qué texto plano cifrar y observar el resultado — el ataque más poderoso

---

### 2.1 Criptografía de Clave Simétrica

**Idea central**: emisor y receptor comparten la **misma clave secreta** para cifrar y descifrar.

```
Alice cifra:   KS(m)   →  viaja por la red  →  Bob descifra: KS(KS(m)) = m
              usando KS                                       usando la misma KS
```

El problema fundamental: **¿cómo acuerdan la clave sin que nadie la intercepte?**

#### Cifrado de sustitución simple (monoalfabético)

La forma más básica: sustituir cada letra por otra según un patrón fijo:

```
Texto plano:  a b c d e f g h i j k l m n o p q r s t u v w x y z
Texto cifrado: m n b v c x z a s d f g h j k l p o i u y t r e w q

Ejemplo:
  Plano:   "bob. i love you. alice"
  Cifrado: "nkn. s gktc wky. mgsbc"
```

La clave es el **mapeo completo** de 26 letras. Tiene 26! combinaciones posibles (~4×10²⁶) — imposible por fuerza bruta, pero vulnerable al **análisis estadístico** (la letra "e" es la más frecuente en inglés — si en el cifrado la letra "x" es la más frecuente, probablemente representa "e").

#### Cifrados de sustitución más sofisticados

En lugar de una sola sustitución, usar **n cifrados distintos** y ciclar entre ellos:

```
Ejemplo con n=4 cifrados M1,M3,M4,M3,M2, ciclando:
"dog": d cifrado con M1, o cifrado con M3, g cifrado con M4
```

Esto hace el análisis estadístico mucho más difícil porque la misma letra no siempre se cifra igual.

#### DES — Data Encryption Standard

- Estándar del gobierno de EEUU desde 1993 (NIST)
- Clave simétrica de **56 bits**, bloques de 64 bits
- **Problema**: clave de 56 bits es demasiado corta. En un "DES Challenge" se rompió por fuerza bruta en **menos de un día**
- **Solución**: **3DES** — cifrar tres veces con tres claves distintas → efectivamente 168 bits de seguridad
- Hoy en día está obsoleto

#### AES — Advanced Encryption Standard

- Reemplazó a DES en noviembre 2001 (NIST)
- Procesa bloques de **128 bits**
- Claves de **128, 192 o 256 bits**
- Si un ataque de fuerza bruta a DES tarda 1 segundo, el mismo ataque a AES tardaría **149 billones de años**
- Es el estándar actual para cifrado simétrico

---

### 2.2 Criptografía de Clave Pública

Cambio radical de paradigma: en lugar de una sola clave compartida, cada persona tiene **dos claves distintas**:

```
Clave PÚBLICA  (K+B): conocida por todos — se puede publicar libremente
Clave PRIVADA  (K-B): conocida SOLO por su dueño — nunca se comparte
```

**Cómo funciona el cifrado:**

```
Alice quiere enviar un mensaje secreto a Bob:
1. Alice usa la clave PÚBLICA de Bob (K+B) para cifrar:   c = K+B(m)
2. Solo Bob puede descifrar, usando su clave PRIVADA:      m = K-B(K+B(m))
```

La magia: **solo Bob puede descifrar**, porque solo él tiene su clave privada — aunque todo el mundo sabe la clave pública.

#### Propiedades matemáticas requeridas

Para que un algoritmo de clave pública funcione, necesita:

1. `K-B(K+B(m)) = m` — descifrar lo que se cifró con la pública da el mensaje original
2. Dada la clave pública K+B, debe ser **computacionalmente imposible** calcular K-B

---

### 2.3 RSA — El Algoritmo de Clave Pública más usado

RSA (Rivest, Shamir, Adleman, 1978) es el algoritmo de clave pública dominante.

#### Fundamento matemático: aritmética modular

```
x mod n = resto de dividir x entre n

Propiedades clave:
[(a mod n) + (b mod n)] mod n = (a+b) mod n
[(a mod n) × (b mod n)] mod n = (a×b) mod n
→ en consecuencia: (a mod n)^d mod n = a^d mod n
```

#### Generación del par de claves

1. Elegir dos números primos grandes **p** y **q** (típicamente 1024 bits cada uno)
2. Calcular `n = p×q` y `z = (p-1)(q-1)`
3. Elegir **e** tal que e < n y e no tenga factores comunes con z (e y z son "coprimos")
4. Elegir **d** tal que `ed mod z = 1`
5. **Clave pública**: `(n, e)` — se puede publicar
6. **Clave privada**: `(n, d)` — se guarda en secreto

#### Cifrado y descifrado

```
Cifrar mensaje m:    c = m^e mod n
Descifrar c:         m = c^d mod n

O equivalentemente: m = (m^e mod n)^d mod n = m^(ed mod z) mod n = m^1 mod n = m
```

#### Ejemplo concreto (con números pequeños)

```
Bob elige p=5, q=7 → n=35, z=24, e=5, d=29

Cifrar m=12:
  c = 12^5 mod 35 = 24832 mod 35 = 17

Descifrar c=17:
  m = 17^29 mod 35 = 12 ✓
```

#### Por qué RSA es seguro

Para romper RSA necesitarías calcular d a partir de (n,e). Para eso necesitarías factorizar n = p×q. **Factorizar números muy grandes es computacionalmente inviable** con la tecnología actual — un número de 2048 bits tomaría más tiempo que la edad del universo.

#### Propiedad importante de RSA

```
K-B(K+B(m)) = m = K+B(K-B(m))
```

Da igual en qué orden apliques las claves — el resultado es el mismo. Esto será clave para las **firmas digitales**.

#### RSA en la práctica: session keys

RSA es computacionalmente caro — al menos 100 veces más lento que DES. En la práctica se usa así:

```
1. RSA establece la conexión segura y acuerda una clave simétrica KS (session key)
2. A partir de ahí, toda la comunicación se cifra con KS (mucho más rápido)
```

Este es exactamente el modelo que usa TLS (HTTPS).

---

## 3. Autenticación e Integridad de Mensajes

### El problema de la autenticación

Bob quiere verificar que realmente está hablando con Alice, no con un impostor. El capítulo muestra una evolución de protocolos, cada uno rompiendo el anterior:

#### ap1.0: "Soy Alice" (trivial)

```
Alice → Bob: "Soy Alice"
```
**Problema**: Trudy puede enviar exactamente el mismo mensaje. Cualquiera puede decir que es Alice.

#### ap2.0: Con dirección IP

```
Alice → Bob: "Soy Alice" + IP de Alice en el paquete
```
**Problema**: Trudy puede hacer **IP spoofing** — falsificar la IP origen del paquete. No hay forma de verificar que la IP sea real.

#### ap3.0: Con contraseña

```
Alice → Bob: "Soy Alice" + contraseña secreta
```
**Problema**: **Playback attack** — Trudy graba este intercambio y lo "reproduce" más tarde. No importa que la contraseña sea secreta si Trudy puede reenviar el mensaje exacto.

#### ap3.0 modificado: Con contraseña cifrada

```
Alice → Bob: "Soy Alice" + contraseña cifrada
```
**Problema**: El playback attack **sigue funcionando**. Trudy no necesita descifrar la contraseña — solo reenvía el paquete cifrado tal como lo grabó.

#### ap4.0: Con nonce (número de un solo uso)

Un **nonce** es un número R usado **una sola vez en la vida** (number used once).

```
1. Alice → Bob: "Soy Alice"
2. Bob → Alice: R (el nonce, un número aleatorio)
3. Alice → Bob: KA-B(R)  — cifra el nonce con la clave compartida
```

**Por qué funciona**: Bob sabe que solo Alice conoce la clave KA-B. Si Alice puede cifrar el nonce R correctamente, debe ser Alice "en vivo" (no una grabación, porque R es distinto cada vez).

**Problema**: requiere una clave simétrica compartida KA-B. ¿Cómo la establecieron?

#### ap5.0: Con clave pública y nonce

```
1. Alice → Bob: "Soy Alice"
2. Bob → Alice: R (nonce)
3. Alice → Bob: K-A(R)  — cifra el nonce con su CLAVE PRIVADA
4. Bob verifica:  K+A(K-A(R)) = R  → solo Alice pudo haber generado esto
5. Alice → Bob: "Envíame tu clave pública"
6. Bob → Alice: K+B
```

**Problema grave: Ataque Man-in-the-Middle (MITM)**

Trudy se pone en el medio entre Alice y Bob, suplantando a ambos:

```
Alice ←→ [Trudy haciéndose pasar por Bob] ←→ Bob
           [Trudy haciéndose pasar por Alice]
```

Trudy puede:
- Dar a Alice **su propia clave pública** K+T haciéndola pasar por la de Bob
- Dar a Bob **su propia clave pública** K+T haciéndola pasar por la de Alice
- Descifrar todos los mensajes, leerlos, y reenviarlos cifrados con la clave correcta

Alice y Bob no pueden detectar esto — creen que se están comunicando directamente, pero Trudy lo ve todo.

**Solución: Autoridades de Certificación (CA)**

---

### 3.1 Firmas Digitales

Una firma digital es el equivalente criptográfico de la firma manuscrita: prueba que el mensaje fue enviado por una persona específica.

**Funcionamiento básico:**

```
Bob quiere "firmar" el mensaje m:
1. Bob cifra m con su CLAVE PRIVADA K-B
2. Envía m y K-B(m) juntos

Alice verifica:
1. Aplica la clave PÚBLICA de Bob: K+B(K-B(m)) = m
2. Si coincide con el m recibido → Bob y nadie más pudo haberlo firmado
```

**Propiedades que garantiza:**
- Bob firmó m (autenticación)
- Nadie más firmó m (no repudiación)
- Bob no puede negar haberlo firmado — Alice puede llevar m y K-B(m) a un tribunal

### 3.2 Funciones Hash y Resumen de Mensaje (Message Digest)

**Problema**: cifrar con clave pública mensajes largos es muy caro computacionalmente.

**Solución**: en lugar de firmar el mensaje completo, firmar solo su "huella digital" (hash).

Una función hash H toma un mensaje de cualquier tamaño y produce una salida de **tamaño fijo** (el message digest):

```
H(m) = huella digital de m  (tamaño fijo, ej. 256 bits)
```

**Propiedades requeridas:**
- **Muchos-a-uno**: muchos mensajes posibles, pocos digests posibles
- **Tamaño fijo de salida**: independientemente del tamaño de m
- **Irreversible**: dado H(m), es computacionalmente imposible encontrar m
- **Resistente a colisiones**: imposible encontrar dos mensajes distintos con el mismo hash

**Por qué el checksum de Internet NO sirve como hash criptográfico:**

```
Mensaje 1:  IOU1 / 00.9 / 9BOB  → checksum = B2C1D2AC
Mensaje 2:  IOU9 / 00.1 / 9BOB  → checksum = B2C1D2AC  ← ¡mismo hash, distinto mensaje!
```

Un atacante puede modificar el mensaje y mantener el mismo checksum — no es seguro.

**Algoritmos de hash usados en la práctica:**
- **MD5**: digest de 128 bits (RFC 1321) — hoy en día considerado débil
- **SHA-1**: digest de 160 bits (estándar NIST) — también considerado débil
- **SHA-256/SHA-384**: los estándares actuales

### 3.3 Firma Digital = Hash firmado

La combinación práctica es:

```
Bob envía un documento firmado:
1. Calcula H(m) — el hash del mensaje
2. Cifra H(m) con su clave privada K-B → K-B(H(m))
3. Envía: m  +  K-B(H(m))

Alice verifica:
1. Descifra K-B(H(m)) usando K+B → obtiene H(m)
2. Calcula independientemente H(m') del mensaje recibido m'
3. Compara H(m) == H(m')
   ✓ Iguales → mensaje íntegro, firmado por Bob
   ✗ Distintos → el mensaje fue alterado
```

### 3.4 Autoridades de Certificación (CA)

**El problema que resuelven**: ¿cómo sabes que la clave pública que tienes realmente pertenece a Bob y no a Trudy?

Una **CA (Certification Authority)** es una entidad de confianza que:
1. Verifica la identidad de Bob (Alice, empresa, servidor web, etc.)
2. Emite un **certificado digital** que vincula "la identidad de Bob" con "la clave pública de Bob"
3. Firma ese certificado con su propia clave privada K-CA

```
Certificado de Bob = [Identidad de Bob + K+B] firmado con K-CA
```

**Cómo Alice obtiene la clave pública real de Bob:**
1. Obtiene el certificado de Bob
2. Verifica la firma del certificado con la clave pública de la CA (K+CA) — que es públicamente conocida
3. Si la firma es válida → la clave K+B dentro del certificado es genuinamente la de Bob

Ahora el ataque MITM falla: Trudy no puede falsificar un certificado firmado por la CA (no tiene la clave privada de la CA).

---

## 4. Seguridad en el Correo Electrónico

El correo electrónico puede necesitar tres propiedades: **confidencialidad, autenticación e integridad**. Veamos cada caso:

### 4.1 Solo confidencialidad

```
Alice quiere enviar m secreto a Bob:

1. Alice genera una clave simétrica aleatoria KS (session key)
2. Cifra m con KS:                    KS(m)      [eficiente]
3. Cifra KS con la clave pública de Bob: K+B(KS) [seguro]
4. Envía ambas cosas: KS(m) + K+B(KS)

Bob recibe:
1. Descifra K+B(KS) con su clave privada K-B → obtiene KS
2. Descifra KS(m) con KS → obtiene m
```

**¿Por qué usar KS en lugar de cifrar directamente con K+B(m)?**
RSA es muy lento para mensajes largos. Usar una clave simétrica temporal es mucho más eficiente — RSA solo cifra la clave KS (que es pequeña).

### 4.2 Solo autenticación e integridad

```
Alice quiere que Bob sepa que fue ella quien envió m:

1. Calcula H(m)
2. Firma el hash con su clave privada: K-A(H(m))
3. Envía: m  +  K-A(H(m))

Bob verifica:
1. Aplica K+A al hash firmado → obtiene H(m)
2. Calcula H(m') del mensaje recibido
3. Compara → si iguales, Alice firmó m y no fue alterado
```

### 4.3 Confidencialidad + Autenticación + Integridad

Combina ambos esquemas. Alice usa **tres claves**:

```
1. Firma: K-A(H(m))     — su clave privada para firmar
2. Cifrado del mensaje: KS(m + firma)  — clave simétrica temporal
3. Cifrado de KS: K+B(KS)             — clave pública de Bob

Envía todo junto → Bob deshace el proceso en orden inverso
```

---

## 5. TLS — Seguridad en la Capa de Transporte

### ¿Qué es TLS?

**TLS (Transport Layer Security)** es el protocolo de seguridad más ampliamente desplegado en Internet. Es lo que hace el candadito verde en tu navegador:

- Usado por casi todos los navegadores y servidores web: **HTTPS (puerto 443)**
- Versión anterior: **SSL** (obsoleto desde 2015)
- Versión actual: **TLS 1.3** (RFC 8446, 2018)

Provee los tres pilares de la seguridad usando exactamente las técnicas del capítulo:
- **Confidencialidad**: cifrado simétrico (AES)
- **Integridad**: hashing criptográfico (SHA-256)
- **Autenticación**: criptografía de clave pública y certificados

### Las cuatro piezas de TLS

**1. Handshake (apretón de manos)**
Alice y Bob usan sus certificados y claves privadas para autenticarse mutuamente y acordar o generar un secreto compartido (Master Secret, MS).

**2. Derivación de claves**
A partir del MS se generan **4 claves distintas** (no se reutiliza la misma clave para todo):

| Clave | Uso |
|---|---|
| **Kc** | Cifrado de datos del cliente al servidor |
| **Mc** | MAC del cliente al servidor (integridad) |
| **Ks** | Cifrado de datos del servidor al cliente |
| **Ms** | MAC del servidor al cliente (integridad) |

Por qué 4 claves distintas: usar la misma clave para cifrado y MAC es una mala práctica criptográfica.

**3. Transferencia de datos**
TCP provee un flujo continuo de bytes — TLS los divide en **registros (records)**:

```
Cada registro: [longitud | datos | MAC]
              cifrado con Kc o Ks
```

Esto permite al receptor verificar la integridad de cada registro a medida que llega, sin esperar a que termine toda la transferencia.

**Ataques posibles y sus soluciones:**
- **Re-ordering** (reordenamiento): un MITM reordena los segmentos TCP → solución: incluir **número de secuencia TLS** en el MAC
- **Replay**: reproducir segmentos anteriores → solución: usar **nonces**
- **Truncation attack**: el atacante forja un cierre de conexión TCP → solución: tipo de registro especial para cierre (type=1), incluido en el MAC

**4. Cierre de conexión**
Tipo de registro especial para indicar cierre seguro:
```
Registro de datos:  type=0
Registro de cierre: type=1
MAC calculado sobre: datos + tipo + número de secuencia
```

### TLS 1.3: Cipher Suite y Handshake

**Cipher suite**: el conjunto de algoritmos negociados para la sesión.

TLS 1.3 (más restrictivo que TLS 1.2):
- Solo 5 opciones (antes eran 37)
- Obliga a usar **Diffie-Hellman (DH)** para intercambio de claves
- Cifrado autenticado con AES
- HMAC con SHA-256 o SHA-384

#### Handshake TLS 1.3 — 1 RTT

```
Cliente → Servidor: "hello" (cipher suites soportados, parámetros DH)
Servidor → Cliente: "hello" (cipher suite elegido, parámetros DH, certificado firmado)
Cliente:            verifica certificado, genera claves, ya puede enviar datos HTTPS
```

Solo **1 RTT** (round-trip time) para establecer la conexión — mejora significativa sobre TLS 1.2 (2 RTT).

#### Handshake TLS 1.3 — 0 RTT (conexiones previas)

Si ya existe una conexión previa, el cliente puede enviar **datos cifrados desde el primer mensaje** (usando un "resumption master secret" de la sesión anterior):

```
Cliente → Servidor: "hello" + datos de aplicación cifrados (ej. HTTPS GET)
Servidor → Cliente: "hello" + respuesta
```

**Vulnerabilidad**: susceptible a **replay attacks** — un atacante puede reenviar ese primer mensaje. Solo es seguro para operaciones idempotentes (como HTTP GET, que no modifica estado).

---

## 6. IPsec — Seguridad en la Capa de Red

### ¿Qué es IPsec?

Mientras TLS protege una conexión específica (entre una app y un servidor), **IPsec** protege el tráfico **a nivel de datagrama IP** — todo el tráfico entre dos puntos, independientemente de la aplicación.

```
TLS:    [App específica] ←→ [Servidor específico]    (capa transporte)
IPsec:  [Red A completa] ←→ [Red B completa]          (capa de red)
```

Provee: cifrado, autenticación e integridad para datagramas IP (incluyendo tráfico de control como BGP y DNS).

### Dos modos de operación

**Modo transporte:**
- Solo el **payload (datos)** del datagrama se cifra/autentica
- El encabezado IP original se mantiene visible
- Usado entre dos hosts

**Modo túnel:**
- El **datagrama IP completo** (encabezado + datos) se cifra y se encapsula en un **nuevo datagrama IP** con un nuevo encabezado
- El datagrama original queda completamente oculto
- Usado para VPNs entre dos routers/firewalls

```
Modo túnel:
[ Nuevo encabezado IP | ESP header | Encabezado IP original | Datos originales | ESP trailer | ESP auth ]
  visible (ruta del túnel)             ←─── todo esto está cifrado ──────────────────────────────────────→
```

### Los dos protocolos IPsec

**AH — Authentication Header (RFC 4302)**
- Provee: autenticación del origen + integridad
- No provee: confidencialidad (no cifra)
- Uso: cuando solo necesitas verificar que el paquete no fue alterado, sin ocultarlo

**ESP — Encapsulating Security Payload (RFC 4303)**
- Provee: autenticación del origen + integridad + **confidencialidad** (cifra)
- Es el más usado en la práctica (hace todo lo que hace AH y además cifra)

### Security Associations (SA)

Antes de enviar datos, se establece una **SA (Security Association)** entre los dos extremos. Una SA es como un "canal seguro unidireccional":

```
SA de R1 a R2 contiene:
  - SPI (32 bits): identificador único de esta SA
  - IP origen: 200.168.1.100
  - IP destino: 193.68.2.23
  - Tipo de cifrado y clave de cifrado
  - Tipo de autenticación y clave de autenticación
```

**Importante**: IP es sin conexión, pero IPsec **es orientado a conexión** (mantiene estado en la SA). Para comunicación bidireccional se necesitan dos SAs (una en cada dirección).

### Estructura del datagrama IPsec (modo túnel ESP)

```
[ Nuevo encabezado IP | ESP header | Encabezado IP original | Datos | ESP trailer | ESP auth ]
                         ↑            ←──────── cifrado ─────────────────────────→
                      SPI + Seq#                                                    ↑
                                                                                  MAC
```

**ESP trailer**: relleno para que el mensaje sea múltiplo del tamaño de bloque del cifrador.
**ESP header**: SPI (para que el receptor sepa qué SA usar) + número de secuencia (contra replay attacks).
**ESP auth**: MAC para verificar integridad y autenticidad.

### Bases de datos IPsec

**SAD (Security Association Database)**: "¿cómo debo tratar este paquete?"
- Almacena el estado de cada SA activa
- Al enviar: R1 consulta SAD para saber qué claves y algoritmos usar
- Al recibir: R2 usa el SPI del paquete para encontrar la SA correcta en el SAD

**SPD (Security Policy Database)**: "¿debo usar IPsec para este paquete?"
- Define las políticas: para qué tráfico (por IP origen/destino, protocolo) aplicar IPsec
- Decide: ¿usar IPsec? ¿cuál SA usar? ¿descartar el paquete?

```
SPD dice "QUÉ hacer"   →   SAD dice "CÓMO hacerlo"
```

### IKE — Internet Key Exchange

**Problema**: establecer SAs manualmente para una VPN de 100 endpoints es inmanejable.

**IKE** automatiza el establecimiento de SAs:

**Autenticación con dos métodos posibles:**
- **PSK (Pre-Shared Key)**: ambos extremos parten de un secreto compartido → IKE deriva las claves de sesión
- **PKI**: ambos extremos tienen par de claves pública/privada y certificados → similar al handshake TLS

**Dos fases de IKE:**
1. **Fase 1**: establece un canal seguro bidireccional (IKE SA / ISAKMP) para que las fases siguientes sean seguras
   - Dos modos: "aggressive mode" (menos mensajes) y "main mode" (más seguro, más flexible)
2. **Fase 2**: usa ese canal seguro para negociar el par de SAs de IPsec (una en cada dirección)

---

## 7. Seguridad en Redes Inalámbricas y Móviles

### 7.1 WiFi — 802.11 (WPA3)

La autenticación en WiFi involucra tres partes:
- **Mobile**: el dispositivo que quiere conectarse
- **AP (Access Point)**: el punto de acceso
- **AS (Authentication Server)**: el servidor que toma la decisión final de autenticación

El proceso tiene 4 fases:

**Fase 1: Descubrimiento de capacidades de seguridad**
- El AP anuncia qué métodos de autenticación y cifrado soporta
- El dispositivo solicita los métodos que prefiere
- OJO: en este punto el dispositivo **no está autenticado ni tiene claves**

**Fase 2: Autenticación mutua y derivación de clave**
- El AS y el dispositivo comparten un secreto previo (la contraseña WiFi)
- Usan ese secreto + nonces + hashing para autenticarse mutuamente
- Derivan una clave simétrica de sesión

**Handshake WPA3 en detalle:**
```
AS → Mobile: NonceAS  (número aleatorio del AS)

Mobile:
  - Genera NonceM
  - Deriva KM-AP usando secreto inicial + NonceAS + NonceM
  - Envía: NonceM + HMAC(f(KAS-M, NonceAS))  ← prueba que conoce el secreto

AS:
  - Deriva KM-AP usando los mismos valores
  - Verifica el HMAC → autentica al dispositivo
```

**¿Por qué los nonces?** Evitan replay attacks — si alguien graba el handshake y lo reproduce, los nonces serán distintos y la autenticación fallará.

**Fase 3: Distribución de la clave simétrica**
- El AS informa al AP de la clave de sesión KM-AP derivada
- El AP la usa para cifrar la comunicación con el dispositivo

**Fase 4: Comunicación cifrada**
- Todo el tráfico entre el dispositivo y el AP se cifra con la clave de sesión (AES)

**Protocolo subyacente: EAP (Extensible Authentication Protocol)**
```
Mobile ←─ EAP over LAN (EAPoL, 802.11) ─→ AP ←─ RADIUS (UDP/IP) ─→ AS
```
EAP define el protocolo de request/response entre el dispositivo y el AS.

### 7.2 Redes Móviles 4G LTE

En 4G, los actores son:
- **Mobile**: el teléfono
- **BS (Base Station)**: la estación base (la antena)
- **MME**: Mobility Management Entity (en la red visitada)
- **HSS**: Home Subscriber Service (en la red de origen del usuario)

**Diferencias clave respecto a WiFi:**
- El SIM card del teléfono provee identidad global y contiene claves compartidas de antemano con el HSS
- La autenticación depende de la **red de origen** (home network), no de la red visitada
- La autenticación es **mutua**: el teléfono autentica la red Y la red autentica al teléfono

**Proceso de autenticación 4G:**

```
a. Mobile → BS → MME → HSS: mensaje "attach" con IMSI (identidad del SIM)
   (IMSI identifica la red de origen del usuario)

b. HSS usa la clave compartida KHSS-M para:
   - Generar auth_token (permite al móvil autenticar la red)
   - Generar xresHSS (respuesta esperada del móvil)
   HSS envía ambos al MME

c. Mobile recibe auth_token, lo verifica (autentica la red)
   Mobile calcula resM usando su clave KHSS-M
   Mobile envía resM al MME

d. MME compara resM == xresHSS
   Si coinciden → móvil autenticado ✓
   MME informa al BS y genera claves para él

e. Mobile y BS derivan la clave de sesión KBS-M para cifrar la comunicación
```

**¿Por qué funciona?** Solo alguien que conoce KHSS-M puede calcular resM correctamente. KHSS-M está en el SIM del móvil y en el HSS — nunca viaja por la red.

### 7.3 De 4G a 5G: mejoras de seguridad

| Aspecto | 4G | 5G |
|---|---|---|
| **Decisión de autenticación** | En la red visitada (MME) | En la red de origen (más seguro) |
| **Claves** | Compartidas de antemano | No compartidas de antemano para IoT |
| **IMSI** | Transmitido en texto claro al BS | Cifrado con criptografía de clave pública |

---

## 8. Firewalls e IDS

### ¿Qué es un Firewall?

Un firewall **aísla la red interna de una organización** de Internet, permitiendo pasar algunos paquetes y bloqueando otros:

```
Red interna                                    Internet
(red de confianza) ←──── FIREWALL ────────→ (no confiable)
```

**¿Por qué se necesita?**
- Prevenir ataques DoS: ej. SYN flooding (el atacante abre miles de conexiones TCP falsas, agotando los recursos del servidor)
- Prevenir acceso/modificación ilegal de datos internos
- Permitir solo acceso autorizado a la red interna

Hay **tres tipos** de firewalls:

---

### 8.1 Stateless Packet Filtering (Filtrado de paquetes sin estado)

Filtra paquete por paquete de forma **independiente**, basándose solo en los campos del encabezado:

- IP origen / IP destino
- Puerto TCP/UDP origen / destino
- Tipo de mensaje ICMP
- Bits SYN/ACK de TCP

**Ejemplos de reglas:**
```
Bloquear todos los paquetes con protocolo UDP y puerto origen/destino = 23
  → Bloquea todo Telnet y todos los flujos UDP

Bloquear segmentos TCP entrantes con ACK=0
  → Previene que clientes externos inicien conexiones TCP hacia dentro
  → (un SYN con ACK=0 es el inicio de una nueva conexión)
  → Las conexiones iniciadas desde dentro (que tienen ACK=1) sí pueden recibir respuestas
```

**ACL (Access Control List)**: tabla de reglas aplicadas de arriba hacia abajo, similar a las tablas de OpenFlow:

```
Acción | IP Origen      | IP Destino     | Protocolo | Puerto orig | Puerto dest | Flag
allow  | 222.22/16      | fuera 222.22   | TCP       | >1023       | 80          | any
allow  | fuera 222.22   | 222.22/16      | TCP       | 80          | >1023       | ACK
allow  | 222.22/16      | fuera 222.22   | UDP       | >1023       | 53          | ---
deny   | all            | all            | all       | all         | all         | all
```

**Problema del filtrado sin estado:**

Puede admitir paquetes que "no tienen sentido". Por ejemplo, esta regla:
```
allow | fuera/222.22 | 222.22/16 | TCP | 80 | >1023 | ACK
```
Permite cualquier paquete TCP con puerto 80 y ACK=1 — incluyendo paquetes que llegan **sin que haya ninguna conexión TCP establecida**. Un atacante puede explotar esto.

---

### 8.2 Stateful Packet Filtering (Filtrado con estado)

**Mantiene un registro de todas las conexiones TCP activas** y solo admite paquetes que "tienen sentido" en el contexto de una conexión establecida.

```
Tabla de estado de conexiones:
IP_origen | IP_destino | Puerto_orig | Puerto_dest | Estado
```

- Rastrea SYN (establecimiento) y FIN (cierre) de cada conexión
- Paquetes que llegan sin una conexión correspondiente en la tabla → **bloqueados**
- Conexiones inactivas por demasiado tiempo → **eliminadas de la tabla**

En la ACL del filtrado con estado, se añade una columna "check connection":

```
allow | fuera/222.22 | 222.22/16 | TCP | 80 | >1023 | ACK | ✓ (verificar tabla)
```

El ✓ significa: "solo permitir si existe una conexión correspondiente en la tabla de estado".

---

### 8.3 Application Gateways (Proxies de aplicación)

Van un paso más allá: filtran también **a nivel de datos de aplicación** (no solo encabezados IP/TCP).

**Ejemplo: gateway para Telnet**

```
1. Todos los usuarios que quieran usar Telnet DEBEN hacerlo a través del gateway
2. El gateway autentica al usuario (¿está autorizado?)
3. Si está autorizado, el gateway establece una conexión Telnet separada hacia el destino externo
4. El gateway retransmite datos entre las dos conexiones
5. El router bloquea todas las conexiones Telnet que no pasen por el gateway
```

```
[Usuario interno] ←─ Telnet ─→ [Gateway] ←─ Telnet ─→ [Host externo]
                    (conn 1)               (conn 2)
```

**Ventaja**: puede verificar quién usa el servicio y qué comandos ejecuta.

---

### 8.4 Limitaciones de los Firewalls

- **IP spoofing**: el router no puede saber si la IP origen es real
- **Si múltiples apps necesitan tratamiento especial**: cada una necesita su propio gateway
- **El software cliente debe saber cómo usar el gateway** (ej. configurar proxy en el navegador)
- **Políticas "todo o nada" para UDP**: difícil filtrar UDP de forma granular
- **Tradeoff**: más seguridad = menos comunicación con el exterior
- **Sitios muy protegidos siguen siendo atacados**: el firewall no es solución completa

---

### 8.5 IDS — Intrusion Detection System

Los firewalls operan solo sobre **encabezados TCP/IP** y no correlacionan paquetes entre sí. Un **IDS** complementa al firewall con:

**Deep packet inspection**: analiza el **contenido** de los paquetes (no solo los encabezados):
- Busca strings conocidos de virus o patrones de ataque en el contenido
- Examina correlación entre múltiples paquetes de distintas sesiones

**Ejemplos de lo que detecta un IDS:**
- **Port scanning**: alguien explorando qué puertos están abiertos
- **Network mapping**: alguien trazando la topología de la red interna
- **DoS attacks**: patrones de tráfico anómalos que sugieren un ataque distribuido

**Arquitectura típica**:

```
                    Firewall
                       │
              Red interna
                       │
        ┌──────────────┼────────────────┐
        │              │                │
    Sensores IDS    Servidor Web      DNS
                        FTP Server
                              ← zona desmilitarizada (DMZ)
                         (accesible desde Internet, con protección extra)
```

Se colocan **múltiples sensores IDS** en distintos puntos de la red para diferentes tipos de inspección.

---

## Resumen del Capítulo

El capítulo construye una jerarquía de técnicas de seguridad que se usan en combinación:

```
TÉCNICAS BASE:
  ├── Criptografía simétrica (AES, DES)     → confidencialidad eficiente
  ├── Criptografía de clave pública (RSA)   → intercambio de claves, firmas
  ├── Funciones hash (SHA-256)              → integridad (message digest)
  └── Certificados digitales (CA)           → autenticación confiable

APLICADAS EN CADA CAPA:
  ├── Aplicación:  E-mail seguro (hash + firma + cifrado híbrido)
  ├── Transporte:  TLS/HTTPS (handshake → session keys → AES + HMAC)
  ├── Red:         IPsec (SA + ESP/AH + IKE → VPNs)
  └── Enlace:      802.11 WPA3 (EAP + nonces + AES), 4G/5G

DEFENSA OPERACIONAL:
  ├── Firewalls: stateless, stateful, application gateway
  └── IDS: deep packet inspection, correlación de sesiones
```

**La idea clave que conecta todo**: ninguna técnica por sí sola es suficiente. La seguridad real combina **criptografía** (para proteger los datos), **autenticación** (para verificar las identidades), **integridad** (para detectar modificaciones), y **controles operacionales** (para gestionar el acceso y detectar intrusiones).

---

*Basado en: Kurose, J.F. & Ross, K.W. — Computer Networking: A Top-Down Approach, 8ª Edición, Pearson 2020. Capítulo 8: Security in Computer Networks.*
