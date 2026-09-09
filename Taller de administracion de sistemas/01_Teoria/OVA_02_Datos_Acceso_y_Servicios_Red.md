

---
# Misión general

## Operación Nodo Base

Recibirás una VM Ubuntu funcional del Bloque 1. Deberás agregar almacenamiento, controlar acceso, proteger servicios, entregar configuración de red con Kea y publicar nombres con BIND 9. El objetivo no es copiar comandos: es demostrar por qué funciona y cómo recuperarlo.

- **Antes:** Snapshot, consola, inventario, parámetros reales y respaldo.
- **Durante:** Implementación, pruebas en servidor y cliente, logs e hipótesis.
- **Después:** Evidencia mínima, reversión ensayada y relación con el proyecto.

## Ruta de cuatro operaciones

**Clase 5 — Custodiar el dato** Volumen persistente por UUID y colaboración con mínimo privilegio.

**Clase 6 — Controlar acceso** Diagnóstico local-remoto y UFW sin perder administración.

**Clase 7 — Entrega configuración** DORA, concesión y reserva mediante Kea en red aislada.

**Clase 8 — Publicar nombres** Autoridad directa/inversa con BIND 9 y pruebas específicas.

## Preparar el laboratorio

Los segmentos y nombres siguientes son parámetros del entorno, no una receta fija. Registra los valores asignados por el docente o por tu plataforma.

> **⚠️ Advertencia crítica** El servidor DHCP debe operar únicamente en una red virtual aislada o expresamente autorizada. No uses un adaptador puente hacia la red doméstica o institucional.

### Topología funcional

**Administración** SSH controlado + consola → `srv-infra` (NIC admin · NIC lab · disco adicional) → `cli-linux` (validación real de DHCP y DNS)

### Una VM durante el bloque

- **Beneficio:** reduce preparación y muestra interacción entre servicios.
- **Límite:** almacenamiento, DHCP y DNS comparten un punto único de falla. No representa alta disponibilidad productiva.

### AWS no es equivalente

Permite practicar almacenamiento, diagnóstico, firewall y DNS. Una VPC estándar administra DHCP y no reproduce el broadcast DORA de Kea como la red L2 aislada de Proxmox o VirtualBox.

---

## Clase 5 - Almacenamiento, sistemas de archivos y permisos
*RDA2 - MINIMO PRIVILEGIO - PERSISTENCA*

**Problema técnico**: El equipo del futuro CMS necesita un volumen persistente y compartido. Dos operadores deben colaborar sin abrir el directorio a todos ni depender de nombres de disco inestables.

**Misión**: Construir /srv/proyecto sobre un volumen identificado por UUID y justificar una política grupal que se mantenga para archivos nuevos.

Renderizada:

|Concepto|Definición|
|---|---|
|Dispositivo|Medio o volumen visible para el kernel. No es lo mismo que una partición ni un punto de montaje.|
|Sistema de archivos|Estructura que organiza datos y metadatos sobre un volumen; ext4 es una opción habitual en Ubuntu.|
|UUID|Identificador estable del sistema de archivos. Evita depender de nombres como /dev/sdb que pueden variar.|
|setgid|En un directorio, hace que los objetos nuevos hereden el grupo del directorio. No concede por sí solo permisos de escritura.|
|sticky bit|En un directorio compartido, limita el borrado a propietario del archivo, del directorio o root; /tmp es el caso típico.|
|ACL|Excepción granular adicional a propietario/grupo/otros. Aporta valor cuando el modelo de grupos no basta y debe documentarse.|
## Tutorial embebido

Abre un paso a la vez. Los comandos incluyen parámetros del laboratorio; valida cada valor antes de ejecutarlo.

---

## 1. Confirmar recuperación e identificar el disco

**Objetivo**
Evitar operar sobre el disco del sistema.

**Acción**
Confirma snapshot o respaldo, consola disponible y compara inventario antes/después.

```bash
lsblk -e7 -o NAME,PATH,SIZE,TYPE,FSTYPE,UUID,MOUNTPOINTS,MODEL
sudo blkid
findmnt --real
df -hT
sudo du -xhd1 /srv 2>/dev/null
```

**Resultado esperado**
El disco adicional aparece sin montaje y puede distinguirse por tamaño/modelo.

**Validación**
Registra por qué `<DISCO_OBJETIVO>` es el objetivo y qué evidencia descarta el disco raíz.

**Error frecuente**
Suponer que siempre será `/dev/sdb`.

**Seguridad y reversión**
No ejecutes particionado hasta identificar el dispositivo con dos evidencias.
Reversión: Si no coincide el inventario, detente; no hay cambio que revertir.

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## 2. Crear partición y sistema de archivos

**Objetivo**
Preparar el volumen de datos.

**Acción**
Particiona solo el disco confirmado y crea ext4.

```bash
sudo parted <DISCO_OBJETIVO> --script mklabel gpt mkpart primary ext4 1MiB 100%
lsblk <DISCO_OBJETIVO>
sudo mkfs.ext4 <PARTICION_OBJETIVO>
```

**Resultado esperado**
La partición informa FSTYPE ext4 y un UUID nuevo.

**Validación**
```bash
sudo blkid <PARTICION_OBJETIVO>
```

**Error frecuente**
Aplicar mkfs al disco o partición equivocados destruye datos.

**Seguridad y reversión**
Esta acción es destructiva. Exige snapshot y autorización sobre el disco vacío.
Reversión: Restaurar snapshot si el objetivo fue incorrecto; no improvisar recuperación sobre datos valiosos.

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## 3. Probar montaje temporal

**Objetivo**
Validar el volumen antes de hacerlo persistente.

**Acción**
Crea el punto, monta y ejecuta una prueba de escritura.

```bash
sudo install -d -m 0750 /srv/proyecto
sudo mount <PARTICION_OBJETIVO> /srv/proyecto
findmnt /srv/proyecto
sudo touch /srv/proyecto/.prueba && sudo rm /srv/proyecto/.prueba
```

**Resultado esperado**
findmnt relaciona origen, ext4 y /srv/proyecto; la prueba termina sin error.

**Validación**
```bash
findmnt -no SOURCE,FSTYPE,OPTIONS /srv/proyecto
```

**Error frecuente**
Confundir directorio existente con volumen realmente montado.

**Seguridad y reversión**
Valida con findmnt, no solo con ls.
Reversión: `sudo umount /srv/proyecto`

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## 4. Persistir por UUID y validar sin reiniciar

**Objetivo**
Montar de forma reproducible evitando dependencia de /dev/sdX.

**Acción**
Respalda fstab, obtiene UUID y agrega una entrada adaptada.

```bash
sudo cp -a /etc/fstab /etc/fstab.b2.bak
sudo blkid <PARTICION_OBJETIVO>
# Editar /etc/fstab:
UUID=<UUID_REAL> /srv/proyecto ext4 defaults,nofail 0 2
sudo findmnt --verify --verbose
sudo mount -a
findmnt /srv/proyecto
```

**Resultado esperado**
La verificación no informa errores y mount -a conserva el volumen montado.

**Validación**
```bash
sudo umount /srv/proyecto && sudo mount -a && findmnt /srv/proyecto
```

**Error frecuente**
Reiniciar para "probar" una línea no validada.

**Seguridad y reversión**
Mantén consola y respaldo. `nofail` evita que un volumen de datos opcional detenga el arranque, pero no oculta la necesidad de monitorearlo.
Reversión: `sudo cp -a /etc/fstab.b2.bak /etc/fstab && sudo mount -a`

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## 5. Implementar política grupal con setgid

**Objetivo**
Permitir colaboración sin 777.

**Acción**
Crea el grupo cmsops, incorpora operadores y configura herencia grupal.

```bash
sudo groupadd -f cmsops
sudo usermod -aG cmsops <USUARIO_1>
sudo usermod -aG cmsops <USUARIO_2>
sudo install -d -o root -g cmsops -m 2770 /srv/proyecto/compartido
stat -c "%A %a %U %G %n" /srv/proyecto/compartido
```

**Resultado esperado**
El modo muestra setgid y grupo cmsops; solo propietario/grupo tienen acceso.

**Validación**
Abre sesiones nuevas para ambos usuarios, crea archivos con cada uno y compara stat.

**Error frecuente**
El cambio de grupo no se refleja en una sesión ya abierta.

**Seguridad y reversión**
Usa `newgrp` solo para prueba controlada; en operación, nueva sesión.
Reversión: Retira usuarios del grupo y restaura propietario/modo documentados.

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## 6. Evaluar umask, sticky bit y ACL

**Objetivo**
Justificar cuándo cada mecanismo aporta valor.

**Acción**
Prueba umask 0007 para colaboración; analiza sticky bit y agrega una ACL solo si existe una excepción real.

```bash
umask 0007
touch /srv/proyecto/compartido/prueba-umask
stat -c "%A %a %G %n" /srv/proyecto/compartido/prueba-umask
# Excepción justificada de solo lectura:
sudo setfacl -m u:<AUDITOR>:r-X /srv/proyecto/compartido
getfacl /srv/proyecto/compartido
```

**Resultado esperado**
El archivo nuevo no queda accesible a otros; la excepción ACL se ve explícitamente.

**Validación**
```bash
namei -l /srv/proyecto/compartido/prueba-umask; getfacl ...
```

**Error frecuente**
Agregar ACL por costumbre y perder claridad sobre permisos efectivos.

**Seguridad y reversión**
Prefiere grupos. Sticky bit no reemplaza el control grupal de un repositorio colaborativo.
Reversión: `sudo setfacl -x u: /srv/proyecto/compartido`

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## Clase 6 - Diagnóstico de red y firewall inicial
*RDA1 - RDA3 - Diagnóstico por capas*

**Problema técnico**: Un servicio responde en el propio servidor, pero el cliente no logra conectarse. Abrir todos los puertos ocultaría la causa y ampliaría la superficie de ataque.

**Misión**: Distinguir proceso, socket, puerto, servicio y firewall; habilitar 8080 solo desde la red de laboratorio sin perder SSH.

| Concepto | Definición |
|---|---|
| Proceso | Programa en ejecución con PID, usuario y recursos. Puede existir sin escuchar una red. |
| Socket | Extremo de comunicación que vincula protocolo, dirección y puerto con un proceso. |
| Puerto | Número lógico de transporte. Un puerto abierto requiere un socket escuchando y una ruta permitida. |
| Servicio | Capacidad administrada, a menudo por systemd; su unidad, proceso y puerto son evidencias diferentes. |
| UFW | Interfaz para declarar políticas de firewall. Aplica reglas sobre Netfilter mediante el backend del sistema. |
| Política por defecto | Comportamiento base para tráfico sin regla específica. Denegar entrada reduce superficie, pero exige preservar administración. |

## Tutorial embebido

Abre un paso a la vez. Los comandos incluyen parámetros del laboratorio; valida cada valor antes de ejecutarlo.

---

## 1. Construir una línea base de red

**Objetivo**
Registrar estado antes de modificar.

**Acción**
Observa enlaces, direcciones, rutas y resolución.

```bash
ip -br link
ip -br address
ip route
resolvectl status 2>/dev/null || cat /etc/resolv.conf
ping -c 2 <IP_CLIENTE_LAB>
tracepath <IP_CLIENTE_LAB>
```

**Resultado esperado**
Se identifica interfaz administrativa, interfaz de laboratorio y ruta usada hacia el cliente.

**Validación**
```bash
ip route get <IP_CLIENTE_LAB>
```

**Error frecuente**
Diagnosticar DNS antes de comprobar enlace, IP y ruta.

**Seguridad y reversión**
Los segmentos son referenciales: usa los datos registrados en Preparación.
Reversión: No hay cambios; conserva la línea base para comparación.

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## 2. Relacionar servicio, proceso y socket

**Objetivo**
Evitar concluir "el puerto está abierto" sin evidencia.

**Acción**
Inspecciona servicios y sockets antes de aplicar firewall.

```bash
systemctl --failed
sudo ss -lntup
systemctl status tas-http --no-pager
journalctl -u tas-http -n 30 --no-pager
```

**Resultado esperado**
Cada socket muestra protocolo, dirección local, puerto y proceso cuando hay permisos.

**Validación**
Explica qué evidencia corresponde al servicio y cuál al socket.

**Error frecuente**
Un servicio activo puede escuchar solo en 127.0.0.1 o fallar después de iniciar.

**Seguridad y reversión**
No mates procesos sin revisar unidad, logs y dependencia.
Reversión: No aplica todavía.

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## 3. Levantar un servicio HTTP controlado

**Objetivo**
Crear un objetivo simple para pruebas locales y remotas.

**Acción**
Crea un directorio mínimo para el servicio y una unidad transitoria administrada por systemd.

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

**Resultado esperado**
HTTP responde localmente y ss muestra escucha en 0.0.0.0:8080.

**Validación**
```bash
curl -I http://<IP_SRV_INFRA>:8080
```
desde servidor y cliente.

**Error frecuente**
El usuario del servicio no puede atravesar el directorio o leer index.html.

**Seguridad y reversión**
Comprueba acceso como www-data; no abras permisos a todos ni incorpores el servicio al grupo colaborativo completo sin justificar.
Reversión: `sudo systemctl stop tas-http; sudo rm -f /srv/proyecto/web-prueba/index.html; sudo rmdir /srv/proyecto/web-prueba`

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## 4. Diseñar UFW antes de activarlo

**Objetivo**
Preservar administración y aplicar mínimo acceso.

**Acción**
Confirma consola, identifica origen administrativo y registra reglas actuales.

```bash
sudo ufw status verbose
sudo ufw show added
sudo cp -a /etc/ufw /etc/ufw.b2.bak
# Verifica <RED_ADMIN_CIDR> y <RED_LAB_CIDR> antes de seguir
```

**Resultado esperado**
Existe una vía de consola y las redes reales están documentadas.

**Validación**
Un compañero valida que la regla SSH coincide con el origen de

---

## Clase 7 - DHCP con Kea
*RDA1 - RDA2 - REDAISLADA OBLIGATORIA*

**Problema técnico**: El cliente necesita configuración reproducible y una reserva estable. Una IP manual resuelve el síntoma, pero no demuestra que el servicio DHCP opere correctamente.

**Misión**: Configurar Kea DHCP4 en la interfaz aislada, observar DORA y validar concesión, opciones y reserva desde servidor y cliente.

| Concepto | Definición |
|---|---|
| DORA | Discover, Offer, Request y Acknowledge: intercambio inicial con el que el cliente obtiene una concesión. |
| Pool | Rango dinámico dentro de una subred. No debe incluir direcciones estáticas ni reservas si la política las excluye. |
| Concesión | Asignación temporal registrada por servidor y cliente; tiene tiempos de renovación y expiración. |
| Reserva | Asignación estable basada en un identificador del cliente, normalmente MAC en este laboratorio. |
| Opción DHCP | Dato adicional como DNS, dominio o gateway. No publiques un router que no existe. |
| Broadcast inicial | El cliente aún no conoce su configuración; por eso el descubrimiento necesita alcance de capa 2 o relay. |

## Tutorial embebido

Abre un paso a la vez. Los comandos incluyen parámetros del laboratorio; valida cada valor antes de ejecutarlo.

---

## 1. Auditar aislamiento y parámetros

**Objetivo**
Evitar afectar redes reales.

**Acción**
Confirma que solo alcanza el segmento virtual autorizado y que no hay otro DHCP.

```bash
ip -br link
ip -br address show <INTERFAZ_LAB>
ip route show dev <INTERFAZ_LAB>
sudo ss -lunp "sport = :67"
```

**Resultado esperado**
La interfaz de laboratorio está activa, tiene IP estática y no está puenteada a una red real.

**Validación**
Documenta plataforma, nombre de red virtual y evidencia de aislamiento.

**Error frecuente**
Usar modo puente en VirtualBox para "tener Internet".

**Seguridad y reversión**
DETENTE si la interfaz alcanza una LAN doméstica o institucional.
Reversión: Desconecta el adaptador de laboratorio o apaga Kea desde consola.

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## 2. Instalar y reconocer Kea

**Objetivo**
Ubicar servicio, configuración y concesiones.

**Acción**
Instala el metapaquete Kea recomendado por Ubuntu y registra los componentes antes de editar.

```bash
sudo apt update
sudo apt install kea
systemctl status kea-dhcp4-server --no-pager
dpkg -L kea-dhcp4-server | less
sudo cp -a /etc/kea/kea-dhcp4.conf /etc/kea/kea-dhcp4.conf.b2.bak
```

**Resultado esperado**
Existe el binario kea-dhcp4, la unidad y el archivo de configuración respaldado. Los componentes adicionales no se habilitan sin una necesidad definida.

**Validación**
```bash
command -v kea-dhcp4; systemctl cat kea-dhcp4-server
```

**Error frecuente**
Confundir Kea con el antiguo isc-dhcp-server o habilitar la API de control sin requerirla.

**Seguridad y reversión**
ISC DHCP es antecedente; la práctica no se basa en software obsoleto. El agente de control requiere autenticación y no es necesario para este laboratorio.
Reversión: Restaura el archivo respaldado y detén la unidad.

**Punto de control completado**
Lo marqué después de validar y guardar evidencia.

---

## 3. Construir la configuración mínima

**Objetivo**
Definir interfaz, concesiones y subred conscientemente.

**Acción**
Edita JSON con los valores reales; omite routers si no existe gateway funcional.

```json
{
  "Dhcp4": {
    "interfaces-config": {"interfaces": ["<INTERFAZ_LAB>"]},
    "lease-database": {"type":"memfile","persist":true,"name":"/var/lib/kea/kea-leases4.csv"},
    "valid-lifetime": 3600,
    "renew-timer": 900,
    "rebind-timer": 1800,
    "subnet4": [{
      "subnet": "<RED_LAB_CIDR>",
      "pools": [{"pool":"<POOL_INICIO> - <POOL_FIN>"}],
      "option-data": [
        {"name":"domain-name-servers","data":"<IP_SRV_INFRA>"},
        {"name":"domain-name","data":"equipoXX.tas.test"}
      ],
      "reservations": [{"hw-address":"<MAC_CLIENTE>","ip-address":"<IP_RESERVA_CLIENTE>"}]
    }]
  }
}
```

**Resultado esperado**
La subred contiene pool, el servidor tiene IP dentro de la subred y la reserva no colisiona con política de dinámicos.

**Validación**
Revisión cruzada: interfaz, CIDR, rangos, DNS, dominio y MAC.

**Error frecuente**
JSON no acepta comentarios ni comas finales.

**Seguridad y reversión**
No publiques gateway ficticio. Si existe gateway autorizado, agrega option-data routers

---

## Clase 8 - DNS autoritativo local con BIND 9
*RDA1 - RDA2 - RDA3*

**Problema técnico**; El futuro CMS requiere nombres verificables. Editar /etc/hosts ocultaría el problema y no demuestra autoridad, zona inversa, TTL ni operación del servicio DNS.

**Misión**; Publicar una zona directa e inversa local, restringir consultas a la red de laboratorio y recuperar una falla usando validadores, dig y logs.

| Concepto | Definición |
|---|---|
| Nombre | Etiqueta que identifica un nodo o servicio dentro de un contexto DNS. |
| Dominio | Espacio jerárquico de nombres, por ejemplo equipoXX.tas.test. |
| Zona | Porción administrada por una autoridad DNS y descrita en archivos o una base de datos. |
| FQDN | Nombre completo hasta la raíz. En archivos de zona, el punto final evita concatenar $ORIGIN. |
| TTL | Tiempo durante el cual una respuesta puede permanecer en caché. Afecta propagación y recuperación. |
| Serial | Versión de la zona en el SOA. Debe incrementarse al modificar datos que deban reconocer otros servidores. |

# Tutorial embebido — Configuración de DNS con BIND

Abre un paso a la vez. Los comandos incluyen parámetros del laboratorio; valida cada valor antes de ejecutarlo.

---

## 1. Definir autoridad y datos de zona

**Objetivo** Separar nombre, dominio, zona y registro antes de configurar.

**Acción** Registra dominio, zona inversa, IP del servidor y nombres que el proyecto usará.

```
Dominio: equipoXX.tas.test
Servidor NS: ns1.equipoXX.tas.test.
Web futuro: www.equipoXX.tas.test.
Correo futuro: mail.equipoXX.tas.test.
Zona inversa: <ZONA_INVERSA>
```

**Resultado esperado** Los nombres terminan en punto cuando son FQDN dentro de archivos de zona.

**Validación** Explica qué parte administra la zona directa y cuál la inversa.

**Error frecuente** Calcular zona inversa asumiendo siempre /24.

**Seguridad y reversión** Los segmentos cambian: confirma prefijo y delegación con el docente. Reversión: No hay cambios todavía.

**Punto de control completado** Lo marqué después de validar y guardar evidencia.

---

## 2. Instalar BIND y respaldar

**Objetivo** Reconocer unidades, archivos y herramientas de validación.

**Acción** Instala servidor y utilidades; respalda antes de editar.

```bash
sudo apt update
sudo apt install bind9 bind9-utils dnsutils
systemctl status bind9 --no-pager
sudo cp -a /etc/bind /etc/bind.b2.bak
```

**Resultado esperado** `named`, `named-checkconf`, `named-checkzone` y `dig` están disponibles.

**Validación**

```bash
command -v named-checkconf named-checkzone dig
```

**Error frecuente** Editar zonas sin respaldar ni identificar archivo incluido.

**Seguridad y reversión** No guardes claves TSIG ni secretos en evidencias. Reversión: Restaura `/etc/bind` desde copia y valida antes de recargar.

**Punto de control completado** Lo marqué después de validar y guardar evidencia.

---

## 3. Restringir escucha, consultas y recursión

**Objetivo** Operar como autoridad local con superficie controlada.

**Acción** Ajusta `named.conf.options` con valores reales.

```
options {
    directory "/var/cache/bind";
    listen-on { 127.0.0.1; <IP_SRV_INFRA>; };
    listen-on-v6 { none; };
    allow-query { localhost; <RED_LAB_CIDR>; };
    recursion no;
};
```

**Resultado esperado** BIND escucha solo en localhost/IP de laboratorio y no actúa como resolvedor abierto.

**Validación**

```bash
sudo named-checkconf; sudo ss -lntup | grep :53
```

**Error frecuente** Permitir `any` o publicar recursión abierta.

**Seguridad y reversión** Si se habilita IPv6, debe existir diseño y pruebas reales; no publiques AAAA sin servicio IPv6. Reversión: Restaura `named.conf.options` y ejecuta `named-checkconf`.

**Punto de control completado** Lo marqué después de validar y guardar evidencia.

---

## 4. Declarar zonas directa e inversa

**Objetivo** Vincular cada zona con su archivo autoritativo.

**Acción** Agrega declaraciones en `named.conf.local`.

```
zone "equipoXX.tas.test" {
    type primary;
    file "/etc/bind/zones/db.equipoXX.tas.test";
};

zone "<ZONA_INVERSA>" {
    type primary;
    file "/etc/bind/zones/db.reverse";
};
```

**Resultado esperado** Cada zona tiene tipo `primary` y archivo legible por BIND.

**Validación**

```bash
sudo named-checkconf
```

**Error frecuente** Confundir dominio directo con nombre de zona inversa.

**Seguridad y reversión** Usa nombres/paths coherentes y permisos mínimos de lectura. Reversión: Retira declaraciones agregadas, valida y recarga.

**Punto de control completado** Lo marqué después de validar y guardar evidencia.

---

## 5. Crear zona directa con serial

**Objetivo** Publicar registros aplicados al proyecto.

**Acción** Crea el archivo y adapta IP, contactos y serial.

```
$TTL 300
@   IN SOA ns1.equipoXX.tas.test. admin.equipoXX.tas.test. (
        2026080501 ; Serial
        3600       ; Refresh
        900        ; Retry
        604800     ; Expire
        300 )      ; Negative TTL

    IN NS  ns1.equipoXX.tas.test.

ns1  IN A     <IP_SRV_INFRA>
www  IN A     <IP_SRV_INFRA>
app  IN CNAME www.equipoXX.tas.test.
mail IN A     <IP_SRV_INFRA>
@    IN MX 10 mail.equipoXX.tas.test.
@    IN TXT   "bloque2-validado"
```

**Resultado esperado** A, CNAME, NS, MX y TXT tienen sintaxis válida; el serial sigue una convención documentada.

**Validación**

```bash
sudo named-checkzone equipoXX.tas.test /etc/bind/zones/db.equipoXX.tas.test
```

**Error frecuente** Omitir el punto final en destinos completos y duplicar el dominio.

**Seguridad y reversión** TXT no debe contener tokens, contraseñas ni datos personales. Reversión: Restaura archivo respaldado, incrementa serial si revierte una versión ya publicada.

**Punto de control completado** Lo marqué después de validar y guardar evidencia.

---

## 6. Crear zona inversa y validar

**Objetivo** Resolver IP a nombre mediante PTR.

**Acción** Crea el archivo según el prefijo real; el ejemplo de host solo aplica si la zona es /24.

```
$TTL 300
@   IN SOA ns1.equipoXX.tas.test. admin.equipoXX.tas.test. (
        2026080501 ; Serial
        3600       ; Refresh
        900        ; Retry
        604800     ; Expire
        300 )      ; Negative TTL

    IN NS  ns1.equipoXX.tas.test.

<ULTIMO_OCTETO_SRV> IN PTR ns1.equipoXX.tas.test.
```

**Validar**

```bash
sudo named-checkzone <ZONA_INVERSA> /etc/bind/zones/db.reverse
```

**Resultado esperado** La zona inversa valida y PTR apunta a un FQDN.

**Validación** Confirma con docente cómo expresar el owner si la red no es /24.

**Error frecuente** Copiar `20.10.in-addr.arpa` aunque cambie el segmento.

**Seguridad y reversión** La zona inversa depende del prefijo/delegación real, no de una convención de la OVA. Reversión: Restaura el archivo de zona anterior y su serial.

**Punto de control completado** Lo marqué después de validar y guardar evidencia.

---

## 7. Recargar, abrir 53 y probar autoridad

**Objetivo** Validar desde servidor y cliente, por UDP y TCP.

**Acción** Valida todo, recarga y limita firewall a la interfaz de laboratorio.

```bash
sudo named-checkconf
sudo rndc reload

sudo ufw allow in on <INTERFAZ_LAB> from <RED_LAB_CIDR> to any port 53 proto udp comment "DNS lab UDP"
sudo ufw allow in on <INTERFAZ_LAB> from <RED_LAB_CIDR> to any port 53 proto tcp comment "DNS lab TCP"

dig @<IP_SRV_INFRA> www.equipoXX.tas.test A +norecurse
dig @<IP_SRV_INFRA> -x <IP_SRV_INFRA> +norecurse
dig @<IP_SRV_INFRA> equipoXX.tas.test MX +norecurse
dig @<IP_SRV_INFRA> equipoXX.tas.test TXT +norecurse
dig @<IP_SRV_INFRA> www.equipoXX.tas.test A +tcp +norecurse
```

**Resultado esperado** Respuestas autoritativas correctas, directa/inversa y TCP/UDP 53 disponibles desde cli-linux.

**Validación** Busca flag `aa`, `SERVER`, `ANSWER`, `TTL` y nombre final; revisa `journalctl -u bind9`.

**Error frecuente** Consultar sin `@servidor` y terminar usando otro DNS del cliente.

**Seguridad y reversión** DNS usa UDP y TCP 53; no habilites solo UDP. Reversión: Elimina las dos reglas UFW por número, restaura zonas, valida y `rndc reload`.