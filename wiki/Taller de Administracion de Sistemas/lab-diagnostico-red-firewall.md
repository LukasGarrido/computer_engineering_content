# Laboratorio: Diagnóstico de Red y Firewall Inicial

**Operación 2 de 4 · 105 minutos**
**Módulo:** RDA1 / RDA3 — Diagnóstico por capas
**Autor:** lukas3

---

## 1. Problema técnico

Un servicio responde en el propio servidor, pero el cliente no logra conectarse. Abrir todos los puertos ocultaría la causa real del problema y ampliaría innecesariamente la superficie de ataque.

## 2. Misión

Distinguir con evidencia **proceso, socket, puerto, servicio y firewall** como capas independientes; habilitar el puerto 8080 solo desde la red de laboratorio, sin perder acceso SSH administrativo.

---

## 3. Fundamentos conceptuales

| Concepto | Definición |
|---|---|
| **Proceso** | Programa en ejecución con PID, usuario y recursos. Puede existir sin estar escuchando en ninguna red. |
| **Socket** | Extremo de comunicación que vincula protocolo, dirección y puerto con un proceso concreto. |
| **Puerto** | Número lógico de transporte. Un puerto "abierto" requiere un socket escuchando **y** una ruta permitida (firewall) — ninguna de las dos condiciones por sí sola basta. |
| **Servicio** | Capacidad administrada, a menudo por systemd. Su unidad, su proceso y su puerto son **evidencias distintas**: un servicio puede figurar "activo" para systemd mientras el proceso real falló o escucha en un lugar inaccesible. |
| **UFW** | Interfaz para declarar políticas de firewall. Traduce reglas simples al backend real del sistema (Netfilter). |
| **Política por defecto** | Comportamiento base para tráfico sin regla específica. Denegar entrada por defecto reduce la superficie de ataque, pero exige preservar una vía de administración antes de activarla. |

---

## 4. Entorno de trabajo

| Rol | Host | IP |
|---|---|---|
| Servidor (`srv-infra`) | `lukas3` | `192.168.1.185/24` |
| Cliente de laboratorio (`cli-linux`) | `lukas2` | `192.168.1.184/25` |
| Administración (PC anfitriona, PowerShell/SSH) | Windows host | `192.168.1.144` |

- Gateway de la red: `192.168.1.1`
- Interfaz única en `lukas3`: `enp0s3` (no hay interfaz de laboratorio separada; se filtra por IP/rango sobre la misma interfaz)
- DNS: `1.1.1.1` (Cloudflare), `8.8.8.8` (Google), vía `systemd-resolved`

---

## 5. Paso 1 — Construir una línea base de red

**Objetivo:** registrar el estado de la red **antes** de modificar nada, para poder comparar si algo falla más adelante.

```bash
ip -br link
ip -br address
ip route
resolvectl status 2>/dev/null || cat /etc/resolv.conf
ping -c 2 192.168.1.184
tracepath 192.168.1.184
ip route get 192.168.1.184
```

### Explicación de cada comando

- `ip -br link` → lista las interfaces de red en formato breve (nombre, estado UP/DOWN, MAC).
- `ip -br address` → igual, pero mostrando las IPs asignadas a cada interfaz.
- `ip route` → tabla de rutas: por dónde sale el tráfico según el destino. La ruta `default via ...` indica el gateway.
- `resolvectl status` (con fallback a `/etc/resolv.conf` si el comando no existe) → cómo resuelve DNS la máquina. **Se revisa al final a propósito**: un error frecuente del diagnóstico es sospechar de DNS antes de confirmar que el enlace, la IP y la ruta están correctos.
- `ping -c 2 <IP>` → conectividad básica ICMP, solo 2 paquetes para no saturar la red.
- `tracepath <IP>` → muestra la ruta salto a salto hacia el destino.
- `ip route get <IP>` → le pregunta al kernel qué interfaz y ruta usaría para llegar a esa IP específica, sin enviar tráfico real.

### Resultado obtenido

```
lo               UNKNOWN   127.0.0.1/8 ::1/128
enp0s3           UP        192.168.1.185/24
```
```
default via 192.168.1.1 dev enp0s3 proto static
192.168.1.0/24 dev enp0s3 proto kernel scope link src 192.168.1.185
```
```
Current DNS Server: 1.1.1.1
DNS Servers: 1.1.1.1 8.8.8.8
```
```
PING 192.168.1.184: 2 packets transmitted, 2 received, 0% packet loss
rtt min/avg/max/mdev = 1.885/2.405/2.925/0.520 ms
```
```
tracepath: 1 hop, reached directamente (192.168.1.184)
```
```
192.168.1.184 dev enp0s3 src 192.168.1.185 uid 1000
```

### Interpretación

- Una sola interfaz (`enp0s3`), IP estática correcta, gateway alcanzable.
- `lukas2` y `lukas3` están en el mismo segmento de red (`192.168.1.0/24`) → **1 solo salto**, sin pasar por el gateway.
- DNS operativo, aunque no se usó en este paso (no hay nombres de host involucrados, solo IPs).

### Validación

`ip route get 192.168.1.184` confirmó `dev enp0s3 src 192.168.1.185` — la ruta que el kernel realmente usará coincide con lo esperado.

### Error frecuente
Diagnosticar DNS antes de comprobar enlace, IP y ruta.

### Seguridad y reversión
No hay cambios en este paso; se conserva la línea base para comparación futura.

**Punto de control 1 completado** — en este punto queda descartada la capa de red (enlace/IP/ruta) como causa de cualquier falla posterior.

---

## 6. Paso 2 — Relacionar servicio, proceso y socket

**Objetivo:** evitar concluir "el puerto está abierto" sin evidencia real, antes de tocar el firewall.

```bash
systemctl --failed
sudo ss -lntup
systemctl status tas-http --no-pager
journalctl -u tas-http -n 30 --no-pager
```

### Explicación de cada comando

- `systemctl --failed` → lista unidades de systemd que fallaron al iniciar. Barrido rápido de salud general del sistema.
- `ss -lntup` → el comando central de este paso:
  - `-l` → solo sockets en estado *listening*
  - `-n` → puertos numéricos (no resuelve nombres, más rápido y preciso)
  - `-t` → TCP
  - `-u` → UDP
  - `-p` → proceso dueño del socket (requiere `sudo` para ver procesos de otros usuarios)
- `systemctl status tas-http` → estado de la unidad (en este punto, **aún no existe**, es la foto "antes").
- `journalctl -u tas-http -n 30` → últimas 30 líneas de log de esa unidad (vacío por ahora).

### Resultado obtenido

```
systemctl --failed → 0 loaded units listed.
```
```
ss -lntup:
  127.0.0.53%lo:53   systemd-resolve   (DNS stub local)
  127.0.0.54:53      systemd-resolve
  0.0.0.0:22         sshd              ← único servicio real expuesto
  [::]:22            sshd
```
```
tas-http.service could not be found.
-- No entries --
```

### Interpretación

Antes de crear el servicio del laboratorio, la única evidencia real en la máquina es que **SSH escucha globalmente** (`0.0.0.0:22` y `[::]:22`) y nada más. No hay nada en el puerto 8080. Esta es la línea base contra la que se compara cualquier fallo posterior.

### Error frecuente
Un servicio puede figurar activo en `systemctl` pero escuchar solo en `127.0.0.1` (inaccesible desde afuera), o fallar después de arrancar — por eso se revisan proceso, socket y logs como evidencias independientes, no una sola fuente.

### Seguridad y reversión
No se matan procesos sin revisar antes unidad, logs y dependencias. No aplica todavía ningún cambio.

**Punto de control 2 completado**

---

## 7. Paso 3 — Levantar un servicio HTTP controlado

**Objetivo:** crear un objetivo real de pruebas: un servidor HTTP simple en el puerto 8080, corriendo como usuario no privilegiado (`www-data`), sirviendo contenido desde `/srv/proyecto/web-prueba`.

```bash
sudo install -d -o root -g www-data -m 0750 /srv/proyecto/web-prueba
echo "Nodo TAS operativo" | sudo tee /srv/proyecto/web-prueba/index.html >/dev/null
sudo chown root:www-data /srv/proyecto/web-prueba/index.html
sudo chmod 0640 /srv/proyecto/web-prueba/index.html
sudo -u www-data test -r /srv/proyecto/web-prueba/index.html
sudo systemd-run --unit=tas-http --property=User=www-data /usr/bin/python3 -m http.server 8080 --bind 0.0.0.0 --directory /srv/proyecto/web-prueba
systemctl status tas-http --no-pager
sudo ss -lntp "sport = :8080"
curl -I http://127.0.0.1:8080
```

### Explicación de cada comando

- `install -d -o root -g www-data -m 0750 ...` → crea el directorio del sitio con dueño `root`, grupo `www-data`, modo `0750`.
- `echo ... | sudo tee ... >/dev/null` → escribe contenido a un archivo que requiere privilegios elevados. No se puede usar `sudo echo "x" > archivo` porque la redirección `>` la ejecuta el shell **sin** privilegios; `tee` sí corre con `sudo` y escribe el archivo correctamente.
- `chown root:www-data` + `chmod 0640` → archivo con dueño root, grupo www-data: dueño lee/escribe, grupo solo lee, otros nada.
- `sudo -u www-data test -r ...` → verificación crítica **antes** de levantar el servicio: simula ser `www-data` y comprueba si puede leer el archivo. `test` no imprime nada por sí solo (solo devuelve código de salida), así que conviene envolverlo en un `&& echo ... || echo ...` para ver el resultado explícitamente.
- `systemd-run --unit=tas-http --property=User=www-data /usr/bin/python3 -m http.server 8080 --bind 0.0.0.0 --directory /srv/proyecto/web-prueba`:
  - crea una unidad **systemd transitoria** (administrable con `systemctl`/`journalctl`, pero no persiste en disco como archivo `.service`)
  - corre como `www-data`, no como root (mínimo privilegio)
  - `--bind 0.0.0.0` → escucha en **todas** las interfaces (crítico: si fuera `127.0.0.1`, sería inaccesible desde `lukas2` aunque el proceso estuviera activo)
- `ss -lntp "sport = :8080"` → filtra directamente por el puerto de interés.
- `curl -I http://127.0.0.1:8080` → prueba local, solo headers de la respuesta.

### Incidente durante la ejecución — condición de carrera

**Primer intento:**
```
curl: (7) Failed to connect to 127.0.0.1 port 8080 after 0 ms: Couldn't connect to server
```

El servicio mostraba `systemctl status` como `active (running)`, pero el `curl` inmediatamente posterior falló. Se investigó con evidencia, sin asumir causa:

```bash
sudo ss -lntp
stat -c "%A %a %U %G %n" /srv/proyecto
namei -l /srv/proyecto/web-prueba/index.html
```

**Resultado del `ss` (segunda vez, momentos después):**
```
LISTEN  0  5  0.0.0.0:8080  0.0.0.0:*  users:(("python3",pid=1318,fd=3))
```
El socket sí existía. **Diagnóstico:** el primer `curl` se ejecutó a los ~100ms de haber arrancado `systemd-run`, antes de que el socket estuviera listo para aceptar conexiones — una condición de carrera, no un problema de permisos ni de configuración.

**Repetición del `curl`:**
```
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.12.3
Content-type: text/html
Content-Length: 19
```
Confirmado: el servicio funcionaba correctamente. El error inicial de curl (`(7) Couldn't connect to server`) es cualitativamente distinto a un bloqueo de firewall, que habría dado timeout en vez de rechazo inmediato — buena distinción de diagnóstico documentada.

### Hallazgo secundario — permisos de `/srv/proyecto` tras montar el disco

```bash
stat -c "%A %a %U %G %n" /srv/proyecto
# drwxr-xr-x 755 root root /srv/proyecto
```

En el laboratorio anterior, `/srv/proyecto` se creó con `install -d -m 0750` (dueño root, grupo root, sin grupo específico asignado) **antes** de montar el disco `/dev/sdb1` encima. Al montar un filesystem nuevo sobre un directorio existente, los permisos visibles pasan a ser los de la **raíz del filesystem montado** — y `mkfs.ext4` crea su raíz con `755 root:root` por defecto, independientemente de los permisos que tenía la carpeta vacía antes del montaje.

**Consecuencia:** el `chmod 0750` original quedó "oculto" bajo el punto de montaje. No bloqueó el acceso de `www-data` en este caso (755 permite `r-x` a "otros"), pero es un comportamiento importante de recordar al planificar permisos sobre puntos de montaje.

### `namei -l` — lectura correcta de "Permission denied"

```
drwxr-xr-x root root     /
drwxr-xr-x root root     srv
drwxr-xr-x root root     proyecto
drwxr-x--- root www-data web-prueba
                          index.html - Permission denied
```

Este "Permission denied" corresponde al usuario que ejecutó el comando (`lukas3`), **no** a `www-data`. `lukas3` no es dueño ni pertenece al grupo `www-data`, por lo que cae en la categoría "otros" del archivo (`rw-r-----`, sin acceso). No era el bug — la verificación real de acceso de `www-data` se hace con `sudo -u www-data test -r ...`.

### Resultado final

```
HTTP/1.0 200 OK
```

### Error frecuente
El usuario del servicio no puede atravesar el directorio o leer el archivo servido; también, probar conectividad inmediatamente después de iniciar un servicio, sin dar margen al arranque del socket.

### Seguridad y reversión
Se comprueba acceso explícitamente como `www-data` antes de considerar el servicio listo; no se abren permisos a todos ni se incorpora el servicio al grupo colaborativo completo sin justificarlo.
Reversión: `sudo systemctl stop tas-http; sudo rm -f /srv/proyecto/web-prueba/index.html; sudo rmdir /srv/proyecto/web-prueba`

**Punto de control 3 completado**

---

## 8. Paso 4 — Diseñar UFW antes de activarlo

**Objetivo:** preservar la vía de administración y planificar el acceso mínimo antes de tocar cualquier regla.

```bash
sudo ufw status verbose
sudo ufw show added
sudo cp -a /etc/ufw /etc/ufw.b2.bak
```

### Explicación de cada comando

- `ufw status verbose` → estado actual (activo/inactivo), política por defecto, reglas existentes.
- `ufw show added` → reglas en formato de comando, tal como fueron agregadas.
- `cp -a /etc/ufw /etc/ufw.b2.bak` → respaldo completo del directorio de configuración de UFW.

### Resultado obtenido

```
Status: inactive
Added user rules: (None)
```

Confirmado: sin reglas previas, sin riesgo de conflicto.

### Definición de redes reales del laboratorio

A diferencia del escenario genérico del documento (que asume una interfaz de laboratorio separada), en este entorno solo existe `enp0s3`. Se decidió, por simplicidad de aprendizaje, restringir el acceso a IPs puntuales en vez de rangos completos:

| Variable | Valor decidido | Justificación |
|---|---|---|
| Origen SSH autorizado (lab) | `192.168.1.184/32` (`lukas2`) | único cliente de laboratorio definido |
| Origen 8080 autorizado | `192.168.1.184/32` (`lukas2`) | mismo criterio, acceso mínimo |
| Interfaz de laboratorio | `enp0s3` | única interfaz disponible |

### Incidente detectado antes de activar — origen real de administración

Antes de proceder al paso 5, se verificó desde dónde estaba conectada la sesión de administración activa:

```bash
echo $SSH_CONNECTION
# 192.168.1.144 49400 192.168.1.185 22
```

**Hallazgo:** la sesión de PowerShell/SSH usada para administrar `lukas3` proviene de `192.168.1.144` (la PC anfitriona Windows), **no** de `192.168.1.184` (`lukas2`). La regla de SSH planeada inicialmente no cubría el origen real de administración — de activarse tal cual, la sesión administrativa se habría cortado sin posibilidad de reconexión por SSH.

**Decisión tomada:** agregar una segunda regla SSH específica para `192.168.1.144/32`, manteniendo el criterio de mínimo privilegio (IPs puntuales, no rangos completos), en vez de abrir SSH a toda la red o arriesgar la sesión activa.

### Error frecuente
Activar `deny incoming` antes de autorizar SSH — o, como en este caso, autorizar SSH solo desde el origen "esperado" sin verificar desde dónde se está administrando realmente en ese momento.

### Seguridad y reversión
Se confirmó explícitamente el origen de la sesión administrativa antes de aplicar cualquier política restrictiva. Reversión disponible: `sudo ufw disable`; restaurar `/etc/ufw` desde el respaldo si fuera necesario.

**Punto de control 4 completado**

---

## 9. Paso 5 — Aplicar políticas restringidas

**Objetivo:** permitir únicamente los orígenes y puertos necesarios.

```bash
sudo ufw allow from 192.168.1.184/32 to any port 22 proto tcp comment "SSH administracion"
sudo ufw allow in on enp0s3 from 192.168.1.184/32 to any port 8080 proto tcp comment "TAS laboratorio"
sudo ufw allow from 192.168.1.144/32 to any port 22 proto tcp comment "SSH admin windows"
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw logging medium
sudo ufw enable
sudo ufw status numbered
```

### Explicación de cada comando

- `ufw allow from <IP>/32 to any port <puerto> proto tcp comment "..."` → regla de permiso puntual: solo esa IP exacta (`/32` = máscara de host único), solo ese puerto, solo TCP, con comentario para trazabilidad futura.
- `ufw allow in on enp0s3 from ...` → además de filtrar por IP, especifica la interfaz de entrada — redundante en este caso (solo hay una interfaz), pero documenta la intención tal como pide la estructura original del laboratorio.
- `ufw default deny incoming` → política base: todo el tráfico entrante se rechaza salvo lo permitido explícitamente. Esto es lo que realmente reduce la superficie de ataque — sin esto, cualquier otro puerto seguiría accesible por defecto.
- `ufw default allow outgoing` → el tráfico que la máquina inicia hacia afuera queda permitido (necesario para actualizaciones, DNS, etc.).
- `ufw logging medium` → registra paquetes bloqueados y conexiones nuevas permitidas.
- `ufw enable` → activa el firewall con las reglas y políticas configuradas. UFW advierte explícitamente que puede interrumpir sesiones SSH existentes si no coinciden con las reglas.
- `ufw status numbered` → lista las reglas activas con número de índice (útil para borrarlas puntualmente después: `ufw delete <n>`).

### Resultado obtenido

```
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
Status: active

[ 1] 22/tcp                     ALLOW IN    192.168.1.184   # SSH administracion
[ 2] 8080/tcp on enp0s3         ALLOW IN    192.168.1.184   # TAS laboratorio
[ 3] 22/tcp                     ALLOW IN    192.168.1.144   # SSH admin windows
```

La sesión de PowerShell permaneció activa tras el `enable` — confirmación práctica de que la regla `[3]` cubrió correctamente el origen real de administración.

### Error frecuente
Usar `ufw allow 8080` sin especificar origen abre el puerto a **cualquier** IP, anulando el propósito de "mínimo privilegio" del laboratorio.

### Seguridad y reversión
No se mezclan reglas manuales de `nftables` con UFW durante esta práctica, para evitar conflictos de precedencia difíciles de depurar.
Reversión: `sudo ufw status numbered` → `sudo ufw delete <n>` → `sudo ufw reload`

**Punto de control 5 completado**

---

## 10. Paso 6 — Validar desde ambos extremos y logs

**Objetivo:** distinguir aplicación, ruta y política mediante evidencia cruzada servidor/cliente.

**En `lukas3` (servidor):**
```bash
curl -I http://127.0.0.1:8080
sudo ss -lntp "sport = :8080"
journalctl -u tas-http -n 20 --no-pager
```

**En `lukas2` (cliente, sesión SSH aparte):**
```bash
curl -v --connect-timeout 3 http://192.168.1.185:8080
```

**En `lukas3`, revisión de logs de firewall:**
```bash
sudo journalctl -k -g "UFW" -n 30 --no-pager
```

### Explicación de cada comando

- `curl -I` local → confirma que el servicio sigue sirviendo contenido correctamente después de activar UFW (aísla: ¿el problema, si lo hubiera, sería del servicio o del firewall?).
- `curl -v --connect-timeout 3` desde el cliente → prueba real de extremo a extremo, con timeout corto para no esperar indefinidamente si el firewall bloquea silenciosamente.
- `journalctl -k -g "UFW"` → filtra el log del kernel (`-k`) por las líneas que contienen "UFW" (`-g`), mostrando tráfico auditado y bloqueado.

### Resultado obtenido — prueba desde `lukas2`

```
*   Trying 192.168.1.185:8080...
* Connected to 192.168.1.185 (192.168.1.185) port 8080
> GET / HTTP/1.1
< HTTP/1.0 200 OK
< Server: SimpleHTTP/0.6 Python/3.12.3
< Content-Length: 19

Nodo TAS operativo
* Closing connection
```

**Conexión exitosa de extremo a extremo** desde el único origen autorizado para el puerto 8080.

### Resultado obtenido — logs de UFW

```
[UFW AUDIT] IN=enp0s3 SRC=192.168.1.1 DST=192.168.1.185 PROTO=ICMP TYPE=8 CODE=0
[UFW BLOCK]  IN=enp0s3 SRC=192.168.1.1 DST=224.0.0.1 PROTO=2 (IGMP)
[UFW AUDIT]  IN=enp0s3 SRC=192.168.1.1 DST=224.0.0.1 PROTO=2 (IGMP)
```

### Interpretación de los logs

- `SRC=192.168.1.1` → tráfico proveniente del **router/gateway**, no de un cliente de prueba.
- `DST=224.0.0.1, PROTO=2` → tráfico **IGMP** (multicast), típico de un router anunciando grupos multicast en la red local — ruido normal de fondo, sin relación con el laboratorio, bloqueado correctamente por no coincidir con ninguna regla `allow`.
- La línea `TYPE=8 CODE=0` → un **ICMP echo request** (ping) del router hacia `lukas3`, registrado como `AUDIT` (no bloqueado, ya que UFW por defecto no filtra ICMP a menos que se configure explícitamente).

**Conclusión:** el logging está activo y funcionando, capturando tráfico real no solicitado. No se generó un bloqueo directo al puerto 8080 desde un origen no autorizado durante esta sesión (se habría necesitado una tercera IP intentando acceder al 8080 para ese caso específico), pero el mecanismo de auditoría quedó demostrado y documentado.

### Matriz final de evidencia — servidor/cliente × servicio/socket/firewall

| Capa                         | Comando de evidencia                     | Resultado                                   |
| ---------------------------- | ---------------------------------------- | ------------------------------------------- |
| Red (enlace/IP/ruta)         | `ping`, `tracepath`, `ip route get`      | conectividad directa, 1 salto               |
| Proceso                      | `systemctl status tas-http`              | activo, corriendo como `www-data`           |
| Socket                       | `ss -lntp`                               | `0.0.0.0:8080` escuchando, PID correcto     |
| Servicio (local)             | `curl -I` en `lukas3`                    | `200 OK`                                    |
| Servicio (remoto autorizado) | `curl -v` desde `lukas2`                 | conecta y recibe `Nodo TAS operativo`       |
| Firewall (auditoría)         | `journalctl -k -g UFW`                   | logging activo, tráfico de red capturado    |
| Administración (SSH)         | sesión PowerShell viva tras `ufw enable` |  reglas `[1]` y `[3]` preservaron el acceso |

### Error frecuente
Interpretar timeout, rechazo de conexión y error de DNS como el mismo síntoma — cada uno apunta a una capa distinta del problema (firewall silencioso, servicio caído, o resolución de nombres, respectivamente).

### Seguridad y reversión
Se capturan solo los metadatos necesarios en los logs; se evita exponer direcciones públicas o credenciales. Reversión: eliminar regla de prueba, recargar (`ufw reload`) y repetir validación.

**Punto de control 6 completado**

---

## 11. Incidentes documentados durante la ejecución

Esta sección resume los tres hallazgos no triviales del laboratorio, útiles como referencia de diagnóstico futuro.

### 11.1 — Falso positivo de conexión (condición de carrera)

**Síntoma:** `curl: (7) Failed to connect to 127.0.0.1 port 8080` inmediatamente después de que `systemctl status` mostrara el servicio como `active (running)`.

**Causa real:** el `curl` se ejecutó a los ~100ms del arranque del proceso, antes de que el socket estuviera listo para aceptar conexiones.

**Cómo se distinguió de un problema real:** un rechazo de firewall habría producido timeout (esperar y luego fallar), no un rechazo inmediato de conexión. `ss -lntp` confirmó momentos después que el socket sí existía y estaba escuchando correctamente.

**Lección:** no asumir causa por el primer síntoma — verificar con `ss` antes de sospechar de permisos o firewall.

### 11.2 — Permisos "perdidos" tras montar un filesystem

**Síntoma:** `/srv/proyecto` mostraba modo `755 root:root` en vez del `0750` configurado explícitamente en un laboratorio anterior.

**Causa real:** al montar `/dev/sdb1` sobre `/srv/proyecto`, los permisos visibles pasan a ser los de la raíz del filesystem recién creado (`mkfs.ext4` usa `755 root:root` por defecto), no los que tenía el directorio vacío antes del montaje.

**Lección:** los permisos configurados sobre un punto de montaje **antes** de montar quedan ocultos bajo el filesystem montado — hay que reconfigurarlos después del montaje si se necesita un modo específico.

### 11.3 — Origen real de administración distinto al planeado

**Síntoma:** la regla de SSH se diseñó inicialmente solo para `192.168.1.184` (`lukas2`), pero la sesión de administración activa (PowerShell) provenía de `192.168.1.144` (PC anfitriona Windows).

**Cómo se detectó antes del incidente:** verificación explícita con `echo $SSH_CONNECTION` **antes** de ejecutar `ufw enable`, en vez de asumir el origen de conexión.

**Solución aplicada:** se agregó una regla adicional específica (`192.168.1.144/32`) en vez de abrir SSH a todo el rango `/24`, preservando el principio de mínimo privilegio.

**Lección:** nunca activar una política `deny incoming` sin confirmar explícitamente, en el momento, desde qué IP se está administrando la máquina.

---

## 12. Resumen de la solución

| Elemento | Decisión tomada | Por qué |
|---|---|---|
| Identificación del problema | Diagnóstico por capas (red → proceso → socket → servicio → firewall) | Evita conclusiones apresuradas ("el puerto está cerrado") sin evidencia |
| Servicio de prueba | `systemd-run` transitorio, corriendo como `www-data` | Mínimo privilegio: no se ejecuta el servicio como root |
| Política de firewall | `deny incoming` por defecto + reglas puntuales por IP `/32` | Reduce superficie de ataque al máximo posible dado el escenario |
| Acceso SSH | Dos reglas específicas (`lukas2` y PC Windows), verificadas contra la sesión real activa | Evita perder acceso administrativo al activar el firewall |
| Acceso al 8080 | Restringido a `192.168.1.184/32`, filtrado además por interfaz `enp0s3` | Solo el cliente de laboratorio definido puede acceder |
| Logging | `ufw logging medium` | Permite auditar tráfico bloqueado y detectar accesos no autorizados |
