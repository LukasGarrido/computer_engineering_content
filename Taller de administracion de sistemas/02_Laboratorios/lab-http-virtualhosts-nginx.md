# Laboratorio: HTTP y Virtual Hosts (adaptado a nginx)

**C9 · 105 minutos · Operador Web**
**Objetivo general:** publicar dos sitios (portal y soporte) sobre la misma IP y puerto, diferenciados por nombre.
**Autor:** lukas3

---

## 1. Problema técnico

Publicar `portal` y `soporte` sobre la misma IP y puerto (80), diferenciados por nombre de host, en vez de depender de IPs o puertos distintos por sitio.

## 2. Misión

Configurar un servidor web con dos Virtual Hosts (server blocks en nginx), separar contenido y permisos, restringir el sitio por defecto y el firewall, y validar con pruebas cruzadas cliente/servidor.

---

## 3. Fundamentos conceptuales

| Concepto | Definición |
|---|---|
| **Petición HTTP** | Mensaje del cliente con método, ruta, versión y cabeceras. La cabecera `Host` permite seleccionar un sitio por nombre. |
| **Respuesta HTTP** | Estado, cabeceras y cuerpo entregados por el servidor. Un código describe el resultado; no explica por sí solo la causa. |
| **Virtual Host / Server Block** | Configuración que permite servir sitios distintos desde una misma IP y puerto según el nombre solicitado. En Apache se llama Virtual Host; en nginx, server block — mismo concepto, sintaxis distinta. |
| **DocumentRoot / root** | Directorio raíz desde el que un sitio publica archivos. No debe confundirse con la raíz del sistema (`/`). |
| **GET y HEAD** | GET solicita representación y cuerpo; HEAD solicita las mismas cabeceras sin el cuerpo, útil para pruebas rápidas. |
| **Access y error log** | El access log registra solicitudes; el error log explica problemas de configuración, permisos o ejecución. |

---

## 4. Decisión de plataforma: nginx en vez de Apache

El documento original del laboratorio está escrito para Apache (`apache2`, `a2ensite`, `<VirtualHost>`). Se decidió adaptar íntegramente a **nginx**, ya que es el servidor que se usará en el proyecto real (WordPress + nginx). La tabla siguiente resume las equivalencias usadas durante todo el laboratorio:

| Concepto | Apache (documento original) | nginx (implementado) |
|---|---|---|
| Paquete | `apache2` | `nginx` |
| Unidad systemd | `apache2` | `nginx` |
| Validar sintaxis | `apache2ctl configtest` | `nginx -t` |
| Ver configuración activa | `apache2ctl -S` | `nginx -T` |
| Habilitar sitio | `a2ensite sitio.conf` | `ln -s sites-available/sitio.conf sites-enabled/` (manual, no hay script equivalente) |
| Deshabilitar sitio | `a2dissite sitio.conf` | `rm sites-enabled/sitio.conf` (el archivo original queda intacto en `sites-available`) |
| Bloque de sitio | `<VirtualHost *:80>...</VirtualHost>` | `server { listen 80; ... }` |
| Nombre de host | `ServerName` | `server_name` |
| Raíz de contenido | `DocumentRoot` | `root` (dentro del bloque `server`) |
| Control de rutas | `<Directory>` + `Require all granted` | `location { try_files ...; }` |
| Usuario del proceso | `www-data` | `www-data` (igual en Ubuntu) |

---

## 5. Entorno de trabajo

| Rol | Host | IP |
|---|---|---|
| Servidor web (`srv-web`) | `lukas3` | `192.168.1.185/24` |
| Cliente de laboratorio (`cli-linux`) | `lukas2` | `192.168.1.184/24` |
| Dominio base | — | `pruebatas.test` (mismo dominio del laboratorio de DNS previo) |
| Servidor DNS autoritativo | `lukas3` (BIND9) | `192.168.1.185` |

---

## 6. Preparación previa — registros DNS faltantes

Antes del paso 1 del laboratorio, se detectó que la zona `pruebatas.test` (creada en el laboratorio de DNS) no contenía los nombres `portal` ni `soporte`, necesarios para este laboratorio.

### Edición de la zona

Archivo: `/etc/bind/zones/db.pruebatas.test`

**Cambios aplicados:**
1. Serial incrementado de `2026092701` a `2026092702` (obligatorio en cada modificación de zona).
2. Registros nuevos agregados al final del archivo:
```
portal IN A 192.168.1.185
soporte IN A 192.168.1.185
```

### Validación y recarga

```bash
sudo named-checkzone pruebatas.test /etc/bind/zones/db.pruebatas.test
sudo rndc reload
```

### Incidente — consulta al DNS equivocado

**Síntoma:** `dig portal.pruebatas.test` (sin especificar servidor) devolvió `NXDOMAIN`, con la respuesta proveniente de `127.0.0.53` (el resolver local `systemd-resolved` de Ubuntu), no del propio BIND.

**Causa:** por defecto, `dig` sin `@servidor` consulta al DNS configurado del sistema operativo (`1.1.1.1`/`8.8.8.8` vía `systemd-resolved`), que no tiene autoridad ni conocimiento de `pruebatas.test` — intentó resolverlo contra internet real y devolvió NXDOMAIN legítimamente.

**Solución:** especificar explícitamente el servidor en cada consulta relacionada con la zona de laboratorio:
```bash
dig @192.168.1.185 portal.pruebatas.test +short
dig @192.168.1.185 soporte.pruebatas.test +short
```

**Resultado:** ambos devolvieron `192.168.1.185` correctamente.

**Lección documentada:** en cualquier máquina que no tenga su DNS del sistema apuntando al servidor de laboratorio, toda consulta relacionada con la zona local debe incluir `@<IP_del_servidor_DNS>` explícitamente — de lo contrario, el resultado dependerá del resolver por defecto del sistema operativo, no del servidor que se está probando.

---

## 7. Paso 1 — Preflight: demostrar DNS y línea base

**Objetivo:** confirmar dependencias antes de instalar nada.

```bash
dig @192.168.1.185 portal.pruebatas.test +short
dig @192.168.1.185 soporte.pruebatas.test +short
ip -br a
sudo ufw status verbose
ip route
systemctl --failed
```

### Explicación de cada comando

- `dig +short` → versión resumida de `dig`, solo la respuesta final (IP), sin las secciones completas de un `dig` normal.
- `ip -br a` → confirma la IP actual de la interfaz (`192.168.1.185/24`).
- `ufw status verbose` → confirma que SSH sigue accesible antes de instalar y modificar más reglas.
- `ip route` → confirma la ruta por defecto y el segmento local.
- `systemctl --failed` → confirma que no hay servicios fallando antes de sumar uno nuevo.

### Resultado obtenido

```
192.168.1.185
192.168.1.185
```
```
enp0s3   UP   192.168.1.185/24
```
```
Status: active
[ SSH .184, 8080 .184, SSH .144, DNS UDP/TCP .0/24 ]
```
```
default via 192.168.1.1 dev enp0s3 proto static
192.168.1.0/24 dev enp0s3 proto kernel scope link src 192.168.1.185
```
```
0 loaded units listed.
```

Ambos nombres resuelven a la IP esperada, la vía administrativa (SSH) sigue disponible, no hay servicios caídos.

### Error frecuente
Continuar aunque el DNS entregue una IP distinta a la esperada.

### Seguridad
No cambiar firewall sin consola o sesión de recuperación disponible.

**✅ Punto de control 1 completado**

---

## 8. Paso 2 — Instalar e identificar nginx

**Objetivo:** relacionar paquete, proceso, unidad y socket — no asumir que "instalado" significa "funcionando correctamente".

```bash
sudo apt update
sudo apt install nginx
systemctl status nginx --no-pager
sudo ss -lntp | grep :80
sudo nginx -t
curl -I http://127.0.0.1/
journalctl -u nginx --since "10 minutes ago"
```

### Explicación de cada comando

- `apt install nginx` → instala el servidor web; en Ubuntu, nginx arranca automáticamente tras la instalación, con su propia unidad systemd ya configurada.
- `systemctl status nginx` → confirma que el servicio está activo.
- `ss -lntp | grep :80` → filtra directamente el puerto de interés, mismo patrón usado en laboratorios anteriores con el 8080 y el 53.
- `nginx -t` → valida la sintaxis de toda la configuración (equivalente a `named-checkconf` en BIND o `apache2ctl configtest` en Apache).
- `curl -I http://127.0.0.1/` → prueba local de la página por defecto.
- `journalctl -u nginx` → logs recientes del servicio.

### Resultado obtenido

```
LISTEN  0.0.0.0:80   nginx (2 procesos: master + worker)
LISTEN  [::]:80      nginx
```
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
```
HTTP/1.1 200 OK
Server: nginx/1.24.0 (Ubuntu)
Content-Length: 615
```

nginx instalado, escuchando en ambos protocolos IP (v4/v6), sintaxis válida, sirviendo la página por defecto correctamente.

### Error frecuente
Confundir "active" (proceso corriendo) con "sitio correctamente configurado" — son evidencias distintas, igual que en el laboratorio de red/firewall con `tas-http`.

### Seguridad
Autorizar el puerto 80 solo desde la red definida, mientras el laboratorio sea interno (aplicado en el paso 5).

**✅ Punto de control 2 completado**

---

## 9. Paso 3 — Crear dos raíces con permisos mínimos

**Objetivo:** separar contenido de `portal` y `soporte`, con el mismo principio de mínimo privilegio aplicado en laboratorios anteriores (usuario `www-data`, no root).

```bash
sudo install -d -o root -g www-data -m 0750 /var/www/portal /var/www/soporte
printf "%s\n" "Portal Nodo Sur" | sudo tee /var/www/portal/index.html >/dev/null
printf "%s\n" "Soporte Nodo Sur" | sudo tee /var/www/soporte/index.html >/dev/null
sudo chmod 0644 /var/www/portal/index.html /var/www/soporte/index.html
```

### Explicación de cada comando

- `install -d -o root -g www-data -m 0750 ...` → crea ambos directorios en una sola llamada, dueño `root`, grupo `www-data`, modo `0750` (dueño todo, grupo lee+entra, otros nada).
- `printf ... | sudo tee ... >/dev/null` → mismo patrón usado en laboratorios anteriores: escribe contenido con privilegios elevados sin perder el `sudo` en la redirección (`sudo echo ... > archivo` fallaría porque la redirección la ejecuta el shell sin privilegios).
- `chmod 0644` → los archivos HTML quedan `rw-r--r--`: dueño lee/escribe, grupo y otros solo leen. **Distinto** al `0640` usado con el servicio Python del laboratorio de firewall — aquí se permite lectura amplia porque nginx sirve contenido estático que no requiere ocultarse de "otros" usuarios del sistema, solo protegerse de escritura no autorizada.

### Validación

```bash
namei -l /var/www/portal/index.html
sudo -u www-data test -r /var/www/portal/index.html && echo "legible por www-data"
sudo -u www-data test -r /var/www/soporte/index.html && echo "legible por www-data"
```

### Resultado obtenido

```
f: /var/www/portal/index.html
drwxr-xr-x root root     /
drwxr-xr-x root root     var
drwxr-xr-x root root     www
drwxr-x--- root www-data portal
                          index.html - Permission denied   ← con usuario lukas3
legible por www-data
legible por www-data
```

### Interpretación — aparente contradicción resuelta

El "Permission denied" del `namei -l` corresponde al usuario que ejecuta el comando (`lukas3`, sin `sudo`), que no es dueño ni pertenece al grupo `www-data` del directorio `portal` (modo `0750`) — cae en la categoría "otros", sin acceso. Esto **no es un error**: es exactamente el comportamiento esperado del mínimo privilegio. La prueba real de acceso (`sudo -u www-data test -r ...`) confirma que el usuario que efectivamente importa —el que corre nginx— sí puede leer el archivo.

**Lección documentada:** `namei -l` sin `sudo` valida el acceso del usuario que lo ejecuta, no el del proceso del servicio. Para validar el acceso real del servicio hay que simular ese usuario explícitamente con `sudo -u <usuario_del_servicio>`.

### Error frecuente
Usar `chmod 777` para evitar razonar sobre la ruta de permisos.

### Seguridad
Solo lectura para código estático; cualquier necesidad de escritura futura debe otorgarse de forma acotada y justificada, no por defecto.

**✅ Punto de control 3 completado**

---

## 10. Paso 4 — Definir y habilitar Server Blocks

**Objetivo:** que nginx seleccione contenido según la cabecera `Host` de la petición.

### 1. Respaldo previo

```bash
sudo cp -a /etc/nginx/sites-available /etc/nginx/sites-available.b3.bak
```

### 2. Configuración de `portal`

Archivo: `/etc/nginx/sites-available/portal.conf`

```nginx
server {
    listen 80;
    server_name portal.pruebatas.test;

    root /var/www/portal;
    index index.html;

    access_log /var/log/nginx/portal_access.log;
    error_log /var/log/nginx/portal_error.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### 3. Configuración de `soporte`

Archivo: `/etc/nginx/sites-available/soporte.conf`

```nginx
server {
    listen 80;
    server_name soporte.pruebatas.test;

    root /var/www/soporte;
    index index.html;

    access_log /var/log/nginx/soporte_access.log;
    error_log /var/log/nginx/soporte_error.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Explicación de cada directiva

- **`listen 80`** → puerto de escucha, equivalente a `<VirtualHost *:80>`.
- **`server_name`** → nombre que nginx compara contra la cabecera `Host` de la petición para elegir este bloque. Equivalente a `ServerName`.
- **`root`** → raíz de contenido del sitio, dentro del bloque `server` (a diferencia de Apache, donde `DocumentRoot` es una directiva independiente).
- **`index index.html`** → archivo por defecto al pedir `/`.
- **`access_log` / `error_log`** → logs separados por sitio, tal como exige el laboratorio, equivalentes a `CustomLog`/`ErrorLog`.
- **`location / { try_files $uri $uri/ =404; }`** → diferencia estructural clave respecto a Apache: nginx no usa `<Directory>` + `Require all granted`, sino bloques `location` que definen cómo resolver cada ruta. `try_files` intenta servir el archivo tal cual, luego como directorio, y devuelve `404` si nada coincide.

### 4. Habilitar los sitios (enlace simbólico manual, sin `a2ensite`)

```bash
sudo ln -s /etc/nginx/sites-available/portal.conf /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/soporte.conf /etc/nginx/sites-enabled/
```

### 5. Validar y recargar

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 6. Validación de configuración activa

```bash
sudo nginx -T | grep -A2 "server_name"
```

### Resultado obtenido

```
server_name portal.pruebatas.test;
root /var/www/portal;

server_name soporte.pruebatas.test;
root /var/www/soporte;
```

Ambos server blocks reconocidos y activos, cada uno con su propia raíz.

### Pruebas locales — diferenciación por nombre

```bash
curl -I -H "Host: portal.pruebatas.test" http://127.0.0.1/
curl -I -H "Host: soporte.pruebatas.test" http://127.0.0.1/
curl -s -H "Host: portal.pruebatas.test" http://127.0.0.1/
curl -s -H "Host: soporte.pruebatas.test" http://127.0.0.1/
```

**Resultado:** ambos devolvieron `200 OK`, con contenido diferenciado (`Portal Nodo Sur` / `Soporte Nodo Sur`) desde la misma IP y puerto — confirmando el objetivo central del laboratorio.

### Error frecuente
Crear el archivo de configuración pero olvidar el enlace simbólico en `sites-enabled` o el `reload` posterior — en nginx, a diferencia de Apache, no hay un comando único que combine ambas acciones.

### Seguridad
Validar sintaxis (`nginx -t`) antes de cada `reload`; el proceso worker no debe correr como root (se mantiene la configuración por defecto, que usa `www-data`).

**✅ Punto de control 4 completado**

---

## 11. Paso 5 — Controlar sitio por defecto y firewall

**Objetivo:** reducir respuestas ambiguas y limitar la superficie expuesta.

### 1. Deshabilitar el sitio por defecto

```bash
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

En nginx, quitar el enlace simbólico de `sites-enabled` es el equivalente a `a2dissite` — el archivo original permanece intacto en `sites-available/default`, por lo que la acción es reversible sin pérdida de datos.

### 2. Autorizar el puerto 80 solo desde la red de clientes

```bash
sudo ufw allow from 192.168.1.0/24 to any port 80 proto tcp comment "HTTP portal-soporte"
sudo ufw status numbered
```

**Decisión de diseño:** se usó `192.168.1.0/24` (red completa) en vez de una IP puntual, siguiendo el mismo criterio aplicado con el servicio DNS — un servidor web típicamente sirve a más de un cliente.

### Resultado — estado final de UFW

```
[ 1] 22/tcp                     ALLOW IN    192.168.1.184   # SSH administracion
[ 2] 8080/tcp on enp0s3         ALLOW IN    192.168.1.184   # TAS laboratorio
[ 3] 22/tcp                     ALLOW IN    192.168.1.144   # SSH admin windows
[ 4] 53/udp on enp0s3           ALLOW IN    192.168.1.0/24  # DNS lab UDP
[ 5] 53/tcp on enp0s3           ALLOW IN    192.168.1.0/24  # DNS lab TCP
[ 6] 22/tcp                     ALLOW IN    192.168.1.0/24  # (temporal, ver incidente abajo)
[ 7] 80/tcp                     ALLOW IN    192.168.1.0/24  # HTTP portal-soporte
```

### Validación

```bash
sudo nginx -T | grep -B2 "server_name _"
curl -I -H "Host: portal.pruebatas.test" http://127.0.0.1/
```

El primer comando no devolvió resultados — confirmando que el bloque por defecto (`server_name _;`) ya no está activo. El segundo confirmó que `portal` sigue respondiendo `200 OK` con normalidad tras el cambio.

### Error frecuente
Abrir el puerto ampliamente (o usar reglas de firewall genéricas como "Apache Full") antes de aplicar TLS o sin justificar el origen — se mantuvo la restricción a la red del laboratorio en vez de abrir a cualquier origen.

### Seguridad
Se conservó el acceso SSH en todo momento antes de modificar reglas adicionales.

**✅ Punto de control 5 completado**

---

## 12. Incidente documentado — pérdida de acceso SSH durante el laboratorio

**Síntoma:** en medio del laboratorio, la sesión SSH desde PowerShell dejó de responder (`Connection timed out`).

### Diagnóstico

Se verificó la IP actual de la máquina administradora con `ipconfig` en Windows, encontrando `192.168.1.73` (vía Wi-Fi) — una IP distinta a la `192.168.1.144` autorizada en la regla `[3]` de UFW, creada en un laboratorio anterior.

**Causa raíz real:** el usuario se había desplazado a una red física distinta (fuera de la red doméstica donde se configuró originalmente el laboratorio). Ninguna IP de esa nueva red coincidía con las reglas UFW existentes, que estaban atadas a IPs específicas de la red de origen.

### Resolución aplicada

Al no tener acceso a la consola gráfica de VirtualBox desde la ubicación remota, se optó por reconectar por SSH desde la red disponible en ese momento y ampliar temporalmente la regla:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 22 proto tcp
```

Esta regla (visible como `[6]` en el estado final de UFW, sin comentario por ser un ajuste de urgencia) permite SSH desde todo el rango `192.168.1.0/24`, en vez de una IP puntual — una relajación temporal y consciente de la política de mínimo privilegio, documentada aquí para que sea revertida cuando se confirme una IP fija de administración.

**Lección documentada:** una política de firewall basada en IPs puntuales (`/32`) es más segura, pero frágil ante cambios de red del administrador — especialmente en escenarios de trabajo remoto o movilidad. Una alternativa más robusta a futuro sería una VPN hacia la red de administración, en vez de depender de listas de IPs específicas que deben actualizarse manualmente cada vez que cambia el origen.

### Pendiente de seguimiento
Restringir nuevamente la regla `[6]` a una IP puntual (o eliminarla en favor de las reglas `[1]`/`[3]` ya existentes) una vez confirmada una IP de administración estable.

---

## 13. Paso 6 — Validar, documentar y cerrar

**Objetivo:** demostrar el resultado final y preparar el procedimiento de reversión.

```bash
curl -sS -D - -o /dev/null http://portal.pruebatas.test/
curl -sS http://soporte.pruebatas.test/
sudo journalctl -u nginx --since "15 minutes ago" --no-pager
curl -I -H "Host: soporte.pruebatas.test" http://127.0.0.1/
sudo nginx -t
```

### Explicación de cada comando

- `curl -sS -D - -o /dev/null` → modo silencioso salvo errores (`-sS`), mostrando solo las cabeceras de respuesta (`-D -` las envía a stdout) y descartando el cuerpo (`-o /dev/null`) — útil para inspeccionar únicamente el intercambio HTTP.
- `curl -sS http://soporte.pruebatas.test/` → trae el contenido completo, confirmando el texto exacto servido.
- `journalctl -u nginx --since "15 minutes ago"` → correlación temporal de los eventos del servicio durante la ventana de trabajo.
- Prueba cruzada final con `Host: soporte...` contra `127.0.0.1`, confirmando una vez más la resolución por nombre desde el propio servidor.
- `nginx -t` repetido como última validación de sintaxis antes de cerrar.

### Matriz final de evidencia — cliente-servidor

| Prueba | Origen | Resultado |
|---|---|---|
| `portal.pruebatas.test` vía `Host` header | `lukas3` (local) | ✅ `200 OK`, contenido "Portal Nodo Sur" |
| `soporte.pruebatas.test` vía `Host` header | `lukas3` (local) | ✅ `200 OK`, contenido "Soporte Nodo Sur" |
| `portal.pruebatas.test` | `lukas2` (remoto) | ✅ `200 OK`, resuelto por DNS real |
| `soporte.pruebatas.test` | `lukas2` (remoto) | ✅ `200 OK`, resuelto por DNS real |
| Sitio por defecto (`server_name _`) | — | ✅ eliminado, ya no responde de forma ambigua |
| `nginx -t` | — | ✅ sintaxis válida en todo momento antes de cada reload |

### Error frecuente
Guardar capturas de evidencia sin comando, hora o interpretación — en esta bitácora cada resultado se documenta junto al comando exacto que lo produjo.

### Seguridad
No se registraron cookies, cabeceras sensibles ni direcciones no saneadas en la evidencia recolectada.

### Reversión (procedimiento probado, no solo teórico)

```bash
# Deshabilitar sitios nuevos
sudo rm /etc/nginx/sites-enabled/portal.conf /etc/nginx/sites-enabled/soporte.conf

# Restaurar sitio por defecto
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Restaurar respaldo completo si fuera necesario
sudo rm -rf /etc/nginx/sites-available
sudo cp -a /etc/nginx/sites-available.b3.bak /etc/nginx/sites-available

sudo nginx -t
sudo systemctl reload nginx

# Revertir regla de firewall del paso 5
sudo ufw status numbered
sudo ufw delete <número_de_regla_80>
```

**✅ Punto de control 6 completado — Laboratorio finalizado**

---

## 14. Resumen de la solución

| Elemento | Decisión tomada | Por qué |
|---|---|---|
| Servidor web | nginx en vez de Apache (documento original) | coherencia con el stack real del proyecto (WordPress + nginx) |
| Separación de sitios | Server blocks distintos, cada uno con su `root`, `access_log` y `error_log` | aislar contenido y diagnóstico por sitio |
| Permisos de contenido | `0750` en directorios, `0644` en archivos, dueño `root`/grupo `www-data` | mínimo privilegio: nginx puede leer, otros usuarios del sistema no pueden atravesar el directorio |
| Habilitación de sitios | Enlaces simbólicos manuales (`ln -s`) | nginx no incluye scripts equivalentes a `a2ensite`/`a2dissite` |
| Sitio por defecto | Eliminado de `sites-enabled` | evita respuestas ambiguas ante nombres no reconocidos |
| Firewall (puerto 80) | Restringido a `192.168.1.0/24` | permite múltiples clientes de la red de laboratorio, no solo uno |
| Firewall (SSH, incidente) | Regla temporal ampliada a `192.168.1.0/24` | necesidad operativa real al cambiar de red administrativa; pendiente de re-endurecer |
| Registros DNS | Agregados `portal` y `soporte` a la zona existente | requisito previo no cubierto por el laboratorio de DNS original |

## 15. Incidentes documentados — resumen

1. **DNS sin registros previos**: `portal` y `soporte` no existían en la zona; se agregaron antes de iniciar el laboratorio propiamente dicho.
2. **Consulta al resolver equivocado**: `dig` sin `@servidor` consultó al DNS del sistema en vez del servidor de laboratorio, produciendo un falso `NXDOMAIN`.
3. **Pérdida de acceso SSH por cambio de red física**: el administrador se desplazó a una red distinta a la de origen, invalidando la regla de firewall basada en IP puntual; resuelto con una ampliación temporal documentada, pendiente de re-endurecer.
4. **Aparente contradicción de permisos**: `namei -l` (ejecutado como `lukas3`) reportó "Permission denied" mientras `sudo -u www-data test -r` confirmaba acceso — ambos resultados correctos, evaluando usuarios distintos.

---

*Documento generado como bitácora de laboratorio — incluye comandos ejecutados, salidas reales obtenidas, adaptación completa de Apache a nginx, y los incidentes reales resueltos en vivo durante la ejecución.*
