# Laboratorio: DNS Autoritativo Local con BIND 9

**Operación 4 de 4 · 105 minutos**
**Módulo:** RDA1 / RDA2 / RDA3
**Autor:** lukas3

---

## 1. Problema técnico

El futuro CMS requiere nombres verificables. Editar `/etc/hosts` ocultaría el problema y no demuestra autoridad, zona inversa, TTL ni operación real del servicio DNS.

## 2. Misión

Publicar una zona directa e inversa local, restringir consultas a la red de laboratorio y validar el servicio usando `dig` y logs, tanto desde el servidor como desde el cliente.

---

## 3. Fundamentos conceptuales

| Concepto | Definición |
|---|---|
| **Nombre** | Etiqueta que identifica un nodo o servicio dentro de un contexto DNS. |
| **Dominio** | Espacio jerárquico de nombres, en este caso `pruebatas.test`. |
| **Zona** | Porción administrada por una autoridad DNS, descrita en un archivo (o base de datos). |
| **FQDN** | Nombre completo hasta la raíz. En archivos de zona, el punto final evita que BIND concatene el `$ORIGIN` automáticamente. |
| **TTL** | Tiempo durante el cual una respuesta puede permanecer en caché. Afecta propagación y velocidad de recuperación ante cambios. |
| **Serial** | Versión de la zona, declarada en el registro SOA. Debe incrementarse cada vez que se modifican datos que otros servidores deban reconocer. |

---

## 4. Entorno de trabajo

| Rol | Host | IP |
|---|---|---|
| Servidor DNS (`srv-infra`) | `lukas3` | `192.168.1.185/24` |
| Cliente de laboratorio (`cli-linux`) | `lukas2` | `192.168.1.184/24` |

- Red: `192.168.1.0/24` (confirmada como `/24` real en labs anteriores mediante `ip route`)
- Firewall (UFW) ya activo desde el laboratorio de red/firewall, con reglas previas de SSH y HTTP

---

## 5. Paso 1 — Definir autoridad y datos de zona

**Objetivo:** separar nombre, dominio, zona y registro antes de configurar nada.

### Datos definidos

| Variable | Valor |
|---|---|
| Dominio | `pruebatas.test` |
| Servidor NS | `ns1.pruebatas.test.` |
| Web (futuro WordPress + nginx) | `www.pruebatas.test.` (registro A) |
| Alias del CMS | `cms.pruebatas.test.` (registro CNAME → `www`) |
| Correo | `mail.pruebatas.test.` (genérico) |
| IP del servidor | `192.168.1.185` |
| Zona inversa | `1.168.192.in-addr.arpa` |
| PTR del servidor | owner `185` → `ns1.pruebatas.test.` |

### Cálculo de la zona inversa

Para una red `/24`, la zona inversa se arma invirtiendo los primeros 3 octetos y agregando `.in-addr.arpa`:

```
192.168.1.0/24  →  1.168.192.in-addr.arpa
```

El registro PTR dentro de esa zona solo necesita el **último octeto** como owner (`185`), ya que los primeros 3 octetos ya están representados en el nombre de la zona.

### Decisión sobre `www` (A) vs `cms` (CNAME)

- **A** → apunta directo a una IP.
- **CNAME** → alias que apunta a *otro nombre*, no a una IP.

Se definió `www` como A y `cms` como CNAME hacia `www`, de forma que si en el futuro cambia la IP del servidor web, solo se actualiza el registro `www` y `cms` lo sigue automáticamente.

### Error frecuente
Calcular la zona inversa asumiendo siempre `/24` sin confirmar el prefijo real de la red — en este caso se verificó explícitamente contra la salida de `ip route` de un laboratorio anterior antes de asumirlo.

### Seguridad y reversión
Los segmentos de red pueden cambiar; el prefijo y la delegación deben confirmarse siempre contra evidencia real, no por convención. No hay cambios en el sistema en este paso.

**Punto de control 1 completado**

---

## 6. Paso 2 — Instalar BIND y respaldar

**Objetivo:** reconocer unidades, archivos y herramientas de validación antes de configurar.

```bash
sudo apt update
sudo apt install bind9 bind9-utils dnsutils
systemctl status bind9 --no-pager
sudo cp -a /etc/bind /etc/bind.b2.bak
command -v named-checkconf named-checkzone dig
```

### Explicación de cada comando

- `apt install bind9 bind9-utils dnsutils` → instala el servidor (`bind9`/`named`), las utilidades de validación (`named-checkconf`, `named-checkzone`, `rndc`) y las herramientas de consulta (`dig`, parte de `dnsutils`).
- `systemctl status bind9` → confirma que el servicio quedó instalado y corriendo con configuración por defecto.
- `cp -a /etc/bind /etc/bind.b2.bak` → respaldo completo del directorio de configuración, antes de editar nada.
- `command -v ...` → confirma que los tres binarios clave están disponibles en el `PATH`.

### Resultado obtenido

```
● named.service - BIND Domain Name Server
   Active: active (running)
   Main PID: 2257 (named)
```

Se observaron mensajes repetidos de `network unreachable resolving './DNSKEY/IN'` y `'./NS/IN'` sobre direcciones IPv6. **No son errores de configuración** — es BIND intentando resolver la zona raíz vía IPv6, protocolo no enrutado en esta máquina. Se resuelven en el paso 3 al desactivar explícitamente `listen-on-v6`.

```
/usr/bin/named-checkconf
/usr/bin/named-checkzone
/usr/bin/dig
```

Los tres binarios disponibles, confirmando instalación completa.

### Error frecuente
Confundir Kea/BIND con software DNS obsoleto, o habilitar la API de control remoto sin necesitarla — no aplicado en este laboratorio.

### Seguridad y reversión
No se registran claves TSIG ni secretos en la evidencia. Reversión: restaurar `/etc/bind` desde el respaldo y detener la unidad.

**Punto de control 2 completado**

---

## 7. Paso 3 — Restringir escucha, consultas y recursión

**Objetivo:** operar como autoridad local con superficie de exposición controlada, evitando actuar como resolvedor abierto.

Archivo editado: `/etc/bind/named.conf.options`

```
options {
  directory "/var/cache/bind";
  listen-on { 127.0.0.1; 192.168.1.185; };
  listen-on-v6 { none; };
  allow-query { localhost; 192.168.1.0/24; };
  recursion no;
};
```

### Explicación de cada directiva

- `directory "/var/cache/bind"` → ruta de trabajo de BIND (preexistente por defecto).
- `listen-on { 127.0.0.1; 192.168.1.185; }` → BIND escucha únicamente en localhost y en la IP real del servidor, en vez de todas las interfaces por defecto.
- `listen-on-v6 { none; }` → desactiva IPv6 explícitamente, eliminando los mensajes de "network unreachable" vistos en el paso anterior.
- `allow-query { localhost; 192.168.1.0/24; }` → define **quién puede consultar** a este servidor: solo el propio servidor y la red local. Nadie desde internet puede preguntarle nada.
- `recursion no` → el ajuste conceptualmente más importante: este servidor **no resuelve dominios ajenos** (como `google.com`) reenviando la consulta a otros DNS. Solo responde con autoridad sobre `pruebatas.test`; para cualquier otra cosa, responde negativamente en vez de intentar resolverlo. Esto es lo que evita que el servidor se convierta en un "resolvedor abierto" — un riesgo de seguridad real si se deja mal configurado en producción.

### Validación y recarga

```bash
sudo named-checkconf
sudo systemctl restart bind9
sudo ss -lntup | grep :53
```

### Resultado obtenido

```
udp  192.168.1.185:53   named
udp  127.0.0.1:53       named
udp  127.0.0.54:53      systemd-resolve
udp  127.0.0.53%lo:53   systemd-resolve
tcp  127.0.0.1:53       named
tcp  192.168.1.185:53   named
tcp  127.0.0.54:53      systemd-resolve
```

`named-checkconf` no devolvió ningún error (silencio = sintaxis válida).

### Interpretación

`named` escucha correctamente en `127.0.0.1` y `192.168.1.185`, ambos protocolos (UDP/TCP). `systemd-resolved` sigue operando en paralelo en direcciones internas distintas (`127.0.0.53`/`127.0.0.54`) sin conflicto: son dos resolvedores DNS conviviendo en la misma máquina con propósitos distintos — uno para que `lukas3` resuelva internet, otro para servir autoridad sobre `pruebatas.test` a la red.

### Error frecuente
Permitir `any` en `allow-query`, o publicar recursión abierta — ambos casos convertirían al servidor en un resolvedor abierto explotable.

### Seguridad y reversión
Si se habilitara IPv6 en el futuro, debe existir diseño y pruebas reales — no se publican registros AAAA sin servicio IPv6 real. Reversión: restaurar `named.conf.options` desde el respaldo y ejecutar `named-checkconf`.

**Punto de control 3 completado**

---

## 8. Paso 4 — Declarar zonas directa e inversa

**Objetivo:** vincular cada zona con su archivo autoritativo correspondiente.

Archivo editado: `/etc/bind/named.conf.local`

```
zone "pruebatas.test" {
  type primary;
  file "/etc/bind/zones/db.pruebatas.test";
};

zone "1.168.192.in-addr.arpa" {
  type primary;
  file "/etc/bind/zones/db.reverse";
};
```

```bash
sudo mkdir -p /etc/bind/zones
sudo named-checkconf
```

### Explicación

- Cada bloque `zone { type primary; file "..."; }` declara que este servidor es la **autoridad primaria** de esa zona y en qué archivo están los datos.
- `db.reverse` es un nombre convencional elegido libremente — no hay una regla que lo exija, pero conviene que sea descriptivo.

### Hallazgo — alcance real de `named-checkconf`

En este punto los archivos `db.pruebatas.test` y `db.reverse` **todavía no existían**, y se esperaba que `named-checkconf` señalara el problema. Sin embargo, devolvió éxito sin errores. Se verificó con:

```bash
ls -la /etc/bind/zones/
# total 8 — directorio vacío, sin archivos
```

**Conclusión documentada:** `named-checkconf` valida únicamente la **sintaxis** de `named.conf` y sus includes (`named.conf.local`, `named.conf.options`) — no verifica que los archivos de zona referenciados existan o sean cargables. Esa verificación ocurre recién cuando BIND intenta **cargar** las zonas de verdad, con `rndc reload` o al reiniciar el servicio, o específicamente con `named-checkzone` sobre cada archivo.

### Error frecuente
Confundir el nombre de dominio de la zona directa con el nombre (formato `in-addr.arpa`) de la zona inversa al declarar los bloques.

### Seguridad y reversión
Se usan nombres y rutas coherentes, con permisos mínimos de lectura sobre los archivos de zona. Reversión: retirar las declaraciones agregadas, validar y recargar.

**Punto de control 4 completado**

---

## 9. Paso 5 — Crear zona directa con serial

**Objetivo:** publicar los registros reales del dominio `pruebatas.test`.

Archivo: `/etc/bind/zones/db.pruebatas.test`

```
$TTL 300
@ IN SOA ns1.pruebatas.test. admin.pruebatas.test. (
  2026092701 3600 900 604800 300 )
  IN NS ns1.pruebatas.test.
ns1 IN A 192.168.1.185
www IN A 192.168.1.185
cms IN CNAME www.pruebatas.test.
mail IN A 192.168.1.185
@ IN MX 10 mail.pruebatas.test.
@ IN TXT "bloque2-validado"
```

### Explicación línea por línea

- **`$TTL 300`** → tiempo de vida por defecto (segundos) para todo registro que no especifique uno propio. 300s (5 min), apropiado para un entorno de laboratorio con iteración rápida.
- **`@ IN SOA ns1.pruebatas.test. admin.pruebatas.test. ( ... )`** → registro SOA (Start of Authority), obligatorio y único por zona:
  - `@` → representa la zona misma (`pruebatas.test`), expandida automáticamente desde `$ORIGIN`
  - `ns1.pruebatas.test.` → servidor de nombres autoritativo primario (FQDN completo, con punto final)
  - `admin.pruebatas.test.` → contacto del administrador en formato de email con `@` reemplazado por `.` (equivale a `admin@pruebatas.test`)
  - Paréntesis: `serial refresh retry expire minimum-ttl`
- **Serial `2026092701`** → convención `AAAAMMDDNN` (año-mes-día-número de cambio ese día). Debe incrementarse en cada modificación futura de la zona, o los demás servidores no detectarán el cambio.
- **`IN NS ns1.pruebatas.test.`** → declara el servidor de nombres de la zona (hereda el `@` implícito de la línea anterior).
- **`ns1 IN A 192.168.1.185`** → registro A del propio servidor de nombres.
- **`www IN A 192.168.1.185`** → futuro WordPress + nginx.
- **`cms IN CNAME www.pruebatas.test.`** → alias hacia `www`. El punto final es obligatorio — sin él, BIND concatenaría el `$ORIGIN` de nuevo, produciendo `www.pruebatas.test.pruebatas.test` (error frecuente explícitamente señalado por el documento).
- **`mail IN A 192.168.1.185`** → servidor de correo genérico.
- **`@ IN MX 10 mail.pruebatas.test.`** → registro MX: indica dónde se entrega el correo de `pruebatas.test`. El `10` es la prioridad (menor número = mayor prioridad).
- **`@ IN TXT "bloque2-validado"`** → registro de texto libre, usado como marca de verificación del laboratorio. Nunca debe contener tokens, contraseñas o datos personales reales.

### Validación

```bash
sudo named-checkzone pruebatas.test /etc/bind/zones/db.pruebatas.test
```

### Resultado obtenido

```
zone pruebatas.test/IN: loaded serial 2026092701
OK
```

Sintaxis correcta, SOA bien formado, todos los registros parseables. A diferencia de `named-checkconf`, este comando sí valida el **contenido real** del archivo de zona.

### Error frecuente
Omitir el punto final en destinos completos (FQDN) dentro del archivo de zona, duplicando el dominio por concatenación automática.

### Seguridad y reversión
El TXT no contiene tokens, contraseñas ni datos personales. Reversión: restaurar archivo respaldado, incrementando el serial si se revierte una versión ya publicada.

**Punto de control 5 completado**

---

## 10. Paso 6 — Crear zona inversa y validar

**Objetivo:** permitir resolver una IP de vuelta a un nombre mediante PTR.

Archivo: `/etc/bind/zones/db.reverse`

```
$TTL 300
@ IN SOA ns1.pruebatas.test. admin.pruebatas.test. (
  2026092701 3600 900 604800 300 )
  IN NS ns1.pruebatas.test.
185 IN PTR ns1.pruebatas.test.
```

### Explicación

- SOA y NS con la misma estructura que la zona directa, mismo servidor autoritativo.
- **`185 IN PTR ns1.pruebatas.test.`** → registro clave del archivo:
  - `185` es el owner. Como la zona ya se llama `1.168.192.in-addr.arpa`, BIND concatena automáticamente: `185.1.168.192.in-addr.arpa` = `192.168.1.185` escrita al revés.
  - `PTR` apunta de vuelta a un nombre, no a una IP.
  - `ns1.pruebatas.test.` con punto final, FQDN completo.

El owner solo necesita el último octeto porque la zona ya representa los primeros 3 octetos invertidos — mismo principio que en la zona directa, donde solo se escribe `www` en vez del FQDN completo.

### Validación

```bash
sudo named-checkzone 1.168.192.in-addr.arpa /etc/bind/zones/db.reverse
```

### Resultado obtenido

```
zone 1.168.192.in-addr.arpa/IN: loaded serial 2026092701
OK
```

### Error frecuente
Copiar una zona inversa de ejemplo (ej. `20.10.in-addr.arpa`) sin recalcularla para el segmento real de la red.

### Seguridad y reversión
La zona inversa depende del prefijo/delegación real, no de una convención genérica. Reversión: restaurar el archivo de zona anterior y su serial.

**Punto de control 6 completado**

---

## 11. Paso 7 — Recargar, abrir puerto 53 y probar autoridad

**Objetivo:** validar desde servidor y cliente, por UDP y TCP, que el servicio responde con autoridad real.

### 1. Validar y recargar en caliente

```bash
sudo named-checkconf
sudo rndc reload
```

`rndc reload` (Remote Name Daemon Control) le indica a BIND, sin reiniciar el proceso completo, que vuelva a leer su configuración y sus zonas. A diferencia de `named-checkconf`, aquí sí se detectaría un fallo real de carga si los archivos de zona tuvieran problemas.

### 2. Abrir firewall para DNS

```bash
sudo ufw allow in on enp0s3 from 192.168.1.0/24 to any port 53 proto udp comment "DNS lab UDP"
sudo ufw allow in on enp0s3 from 192.168.1.0/24 to any port 53 proto tcp comment "DNS lab TCP"
sudo ufw status numbered
```

**Decisión de diseño:** se usó `192.168.1.0/24` (toda la red) en vez de restringir a una IP puntual como `192.168.1.184/32`, siguiendo la advertencia explícita del documento: *"limitar el origen a la red del pool puede bloquear Discover"* — en un servicio DNS, distintos clientes de la red pueden necesitar consultar, no solo un cliente de prueba fijo.

**Ambos protocolos habilitados** — UDP para consultas normales, TCP para respuestas grandes o transferencias de zona, siguiendo la advertencia del documento: *"DNS usa UDP y TCP 53; no habilites solo UDP"*.

### Resultado — estado final de UFW

```
[ 1] 22/tcp                     ALLOW IN    192.168.1.184   # SSH administracion
[ 2] 8080/tcp on enp0s3         ALLOW IN    192.168.1.184   # TAS laboratorio
[ 3] 22/tcp                     ALLOW IN    192.168.1.144   # SSH admin windows
[ 4] 53/udp on enp0s3           ALLOW IN    192.168.1.0/24  # DNS lab UDP
[ 5] 53/tcp on enp0s3           ALLOW IN    192.168.1.0/24  # DNS lab TCP
```

Las reglas 1-3 corresponden al laboratorio anterior (red/firewall) y se mantienen intactas — evidencia de que las políticas de distintos laboratorios pueden convivir sin conflicto cuando están bien delimitadas por puerto/protocolo/origen.

### 3. Validar autoridad — pruebas desde `lukas3`

```bash
dig @192.168.1.185 www.pruebatas.test A +norecurse
dig @192.168.1.185 -x 192.168.1.185 +norecurse
dig @192.168.1.185 pruebatas.test MX +norecurse
dig @192.168.1.185 pruebatas.test TXT +norecurse
dig @192.168.1.185 www.pruebatas.test A +tcp +norecurse
```

### Qué significa cada elemento de la consulta

- **`@192.168.1.185`** → especifica explícitamente qué servidor preguntar, en vez del DNS por defecto del sistema. El documento marca como error frecuente olvidar esto y terminar consultando sin darse cuenta a otro resolvedor.
- **`+norecurse`** → simula una consulta autoritativa directa, coherente con `recursion no` configurado en el paso 3.
- **flag `aa`** (Authoritative Answer, visible en `;; flags: qr aa;`) → confirma que la respuesta es autoritativa, no cacheada ni reenviada.

### Resultados obtenidos

| Consulta                    | Resultado                                                                        |
| --------------------------- | -------------------------------------------------------------------------------- |
| `www.pruebatas.test A`      | `192.168.1.185` — zona directa funcionando                                       |
| `-x 192.168.1.185` (PTR)    | `ns1.pruebatas.test.` — zona inversa funcionando                                 |
| `pruebatas.test MX`         | `10 mail.pruebatas.test.`, con glue record (A de `mail`) en `ADDITIONAL SECTION` |
| `pruebatas.test TXT`        | `"bloque2-validado"`                                                             |
| `www.pruebatas.test A +tcp` | Igual que la primera, pero confirmando `(TCP)` en el pie de respuesta            |

Ejemplo de respuesta completa (consulta A):
```
;; ->>HEADER<<- opcode: QUERY, status: NOERROR
;; flags: qr aa; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 2

;; ANSWER SECTION:
www.pruebatas.test.     300     IN      A       192.168.1.185

;; AUTHORITY SECTION:
pruebatas.test.         300     IN      NS      ns1.pruebatas.test.

;; SERVER: 192.168.1.185#53(192.168.1.185) (UDP)
```

**Detalle adicional observado:** cada respuesta incluyó `COOKIE: ... (good)` en la sección OPT PSEUDOSECTION — una extensión de seguridad DNS (RFC 7873, DNS Cookies) que valida la correspondencia entre consulta y respuesta, mitigando spoofing. No requirió configuración explícita; viene habilitada por defecto en `dig`/BIND modernos.

### 4. Validación cruzada desde el cliente (`lukas2`)

```bash
dig @192.168.1.185 www.pruebatas.test A +norecurse
dig @192.168.1.185 -x 192.168.1.185 +norecurse
```

**Resultado:** ambas consultas respondieron correctamente desde `lukas2`, confirmando que la regla de firewall (`192.168.1.0/24` en puerto 53) efectivamente permite consultas desde otra máquina de la red, no solo desde el propio servidor.

### Error frecuente
Consultar sin especificar `@servidor` y terminar usando el DNS por defecto del sistema en vez del servidor de laboratorio.

### Seguridad y reversión
DNS requiere ambos protocolos, UDP y TCP, en el puerto 53 — habilitar solo uno deja el servicio parcialmente inoperante (falla en respuestas grandes o transferencias de zona). Reversión: eliminar las dos reglas UFW por número (`ufw delete <n>`), restaurar zonas desde respaldo, validar y `rndc reload`.

**Punto de control 7 completado — Laboratorio finalizado**

---

## 12. Resumen de la solución

| Elemento | Decisión tomada | Por qué |
|---|---|---|
| Dominio | `pruebatas.test` | dominio de laboratorio, no resoluble en internet real |
| Zona inversa | `1.168.192.in-addr.arpa` | calculada explícitamente a partir del `/24` real, no asumida por convención |
| Alcance de escucha | `127.0.0.1` + IP del servidor, sin IPv6 | evita exposición innecesaria y elimina errores de resolución IPv6 fallida |
| Recursión | Desactivada (`recursion no`) | evita que el servidor se convierta en resolvedor abierto explotable |
| Alcance de consultas | Red completa `192.168.1.0/24` | un servicio DNS de laboratorio puede necesitar servir a más de un cliente, a diferencia de un servicio puntual como el HTTP del laboratorio anterior |
| Firewall | Reglas UDP y TCP separadas, puerto 53 | DNS requiere ambos protocolos para operar correctamente |
| Validación | `named-checkconf` (sintaxis) + `named-checkzone` (contenido) + `rndc reload` (carga real) + `dig` (funcionamiento end-to-end) | cada herramienta valida una capa distinta; ninguna por sí sola es suficiente |

## 13. Hallazgo documentado — alcance real de `named-checkconf`

**Observación:** al declarar las zonas en `named.conf.local` antes de que los archivos de zona existieran, `named-checkconf` no reportó ningún error, a pesar de que los archivos referenciados no existían en el sistema.

**Causa:** `named-checkconf` valida exclusivamente la sintaxis de `named.conf` y sus archivos incluidos (`named.conf.options`, `named.conf.local`) — no verifica la existencia ni la validez del contenido de los archivos de zona referenciados.

**Lección:** la validación de una zona real (existencia del archivo, sintaxis del SOA, registros bien formados) requiere `named-checkzone <zona> <archivo>` específicamente, o el intento de carga real vía `rndc reload`. Confiar solo en `named-checkconf` para verificar que "todo está listo" habría permitido avanzar con una configuración incompleta sin detectarlo hasta el intento de recarga.
