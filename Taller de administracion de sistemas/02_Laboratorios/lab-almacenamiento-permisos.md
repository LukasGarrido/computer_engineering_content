# Laboratorio: Almacenamiento, Sistemas de Archivos y Permisos

**Operación 1 de 4 · 105 minutos**
**Módulo:** RDA2 — Mínimo privilegio, Persistencia
**Autor:** lukas3

---

## 1. Problema técnico

El equipo del futuro CMS necesita un volumen persistente y compartido. Dos operadores deben colaborar sin abrir el directorio a todos ni depender de nombres de disco inestables (como `/dev/sdb`, que puede cambiar entre reinicios).

## 2. Misión

Construir `/srv/proyecto` sobre un volumen identificado por **UUID** (no por nombre de dispositivo) y justificar una política grupal que se mantenga automáticamente para los archivos nuevos que se creen ahí.

---

## 3. Fundamentos conceptuales

| Concepto | Definición |
|---|---|
| **Dispositivo** | Medio o volumen visible para el kernel. No es lo mismo que una partición ni un punto de montaje. |
| **Sistema de archivos** | Estructura que organiza datos y metadatos sobre un volumen; ext4 es habitual en Ubuntu. |
| **UUID** | Identificador estable del sistema de archivos. Evita depender de nombres como `/dev/sdb`, que pueden variar entre arranques según el orden en que el kernel detecta los discos. |
| **setgid** | En un directorio, hace que los objetos nuevos hereden el grupo del directorio. No concede por sí solo permisos de escritura. |
| **sticky bit** | En un directorio compartido, limita el borrado a propietario del archivo, del directorio, o root. `/tmp` es el caso típico. No aplica a este laboratorio porque el control ya lo da el grupo cerrado. |
| **ACL** | Excepción granular adicional a propietario/grupo/otros. Aporta valor cuando el modelo de grupos no basta (ej. un auditor externo de solo lectura) y debe documentarse por qué se usó. |

---

## 4. Entorno de trabajo

- VM en VirtualBox, Ubuntu con LVM
- Disco del sistema: `/dev/sda` (25G) → `/boot` en `sda2`, `/` sobre LVM en `sda3`
- Disco agregado para el laboratorio: `/dev/sdb` (25G), vacío, añadido desde el hipervisor (VM apagada → Configuración → Almacenamiento → Añadir disco duro)

---

## 5. Paso 1 — Confirmar recuperación e identificar el disco

**Objetivo:** evitar operar sobre el disco del sistema.

```bash
lsblk -e7 -o NAME,PATH,SIZE,TYPE,FSTYPE,UUID,MOUNTPOINTS,MODEL
sudo blkid
findmnt --real
df -hT
```

### Explicación de cada comando

- `lsblk -e7 ...` → lista los dispositivos de bloque. `-e7` excluye los loop devices (ruido de snaps). Las columnas elegidas muestran tamaño, tipo de filesystem, UUID y dónde está montado cada uno, todo en una sola vista.
- `blkid` → muestra UUID y tipo de filesystem de cada partición reconocida.
- `findmnt --real` → lista solo los montajes "reales" (descarta pseudo-filesystems como `proc`, `sysfs`).
- `df -hT` → muestra uso de espacio en disco, en formato legible (`-h`) y con el tipo de filesystem (`-T`).

### Resultado obtenido

```
sda  25G disk                                              VBOX
├─sda1  1M part
├─sda2  2G part ext4  c1db26e3-...  /boot
└─sda3  23G part LVM2_m kqgwRw-...
  └─ubuntu--vg-ubuntu--lv  11.5G lvm ext4  22cff091-...  /
sdb  25G disk                                              VBOX
sr0  1024M rom
```

### Validación — evidencia de que `/dev/sdb` es el disco correcto

1. **Sin sistema de archivos ni particiones**: `FSTYPE` vacío, sin sub-particiones (`sdb1`, etc.) → nunca se ha usado.
2. **No aparece en `findmnt --real` ni en `df -hT`** → no está montado en ningún punto crítico, a diferencia de `sda3`/LVM, que sostiene la raíz `/`.

**Disco objetivo confirmado: `/dev/sdb`**

### Error frecuente
Suponer que el disco nuevo siempre será `/dev/sdb` sin verificar — en otros entornos podría ser `/dev/sdc`, `/dev/vdb`, `/dev/nvme1n1`, etc.

### Seguridad y reversión
No se ejecuta particionado hasta identificar el dispositivo con al menos dos evidencias. Si el inventario no coincide, se detiene el proceso; no hay cambio que revertir en este paso.

**Punto de control 1 completado**

---

## 6. Paso 2 — Crear partición y sistema de archivos

**Objetivo:** preparar el volumen de datos.

```bash
sudo parted /dev/sdb --script mklabel gpt mkpart primary ext4 1MiB 100%
lsblk /dev/sdb
sudo mkfs.ext4 /dev/sdb1
```

### Explicación de cada comando

- `parted /dev/sdb --script mklabel gpt mkpart primary ext4 1MiB 100%`
  - `--script` → modo no interactivo (sin confirmaciones manuales)
  - `mklabel gpt` → crea una tabla de particiones nueva tipo GPT (estándar moderno, reemplaza al viejo MBR)
  - `mkpart primary ext4 1MiB 100%` → crea una partición primaria desde el 1er MiB (margen de alineación) hasta el 100% del disco
- `lsblk /dev/sdb` → verifica que la partición `sdb1` se creó correctamente
- `mkfs.ext4 /dev/sdb1` → formatea la **partición** (no el disco completo) con sistema de archivos ext4. Antes de esto, `sdb1` era solo espacio crudo; después, permite crear archivos y carpetas.

### Resultado obtenido

```
NAME   SIZE TYPE MOUNTPOINTS
sdb     25G disk
└─sdb1  25G part
```

```
mke2fs 1.47.0 (5-Feb-2023)
Creating filesystem with 6553088 4k blocks and 1638400 inodes
Filesystem UUID: e1075b87-a305-4208-aff1-15c5ba570935
...
Writing superblocks and filesystem accounting information: done
```

**UUID de la partición: `e1075b87-a305-4208-aff1-15c5ba570935`** (se reutiliza en el paso 4)

### Error frecuente
Aplicar `mkfs` al disco completo o a la partición equivocada destruye datos existentes.

### Seguridad y reversión
Esta acción es **destructiva**. Exige snapshot y autorización previa sobre el disco vacío. Si el objetivo fue incorrecto, se restaura desde snapshot — no se improvisa recuperación sobre datos valiosos.

** Punto de control 2 completado**

---

## 7. Paso 3 — Probar montaje temporal

**Objetivo:** validar el volumen antes de hacerlo persistente.

```bash
sudo install -d -m 0750 /srv/proyecto
sudo mount /dev/sdb1 /srv/proyecto
findmnt /srv/proyecto
sudo touch /srv/proyecto/.prueba && sudo rm /srv/proyecto/.prueba
```

### Explicación de cada comando

- `install -d -m 0750 /srv/proyecto` → crea el directorio (equivalente a `mkdir -p`) con permisos `0750` de una sola vez: dueño con todo, grupo con lectura+entrada, otros sin nada.
- `mount /dev/sdb1 /srv/proyecto` → "engancha" la partición en ese punto de montaje. A partir de este comando, todo lo que se escriba en `/srv/proyecto` va físicamente a `sdb1`, no al disco del sistema.
- `findmnt /srv/proyecto` → confirma que el montaje ocurrió de verdad. Es más confiable que `ls`, que no distingue una carpeta montada de una carpeta vacía normal.
- `touch ... && rm ...` → prueba rápida de escritura/borrado para confirmar que el filesystem funciona.

### Resultado obtenido

```
TARGET        SOURCE    FSTYPE OPTIONS
/srv/proyecto /dev/sdb1 ext4   rw,relatime
```

La prueba de escritura terminó sin error.

### Error frecuente
Confundir un directorio existente con un volumen realmente montado (por eso se valida con `findmnt`, no solo mirando la carpeta).

### Seguridad y reversión
Reversión: `sudo umount /srv/proyecto`

**Punto de control 3 completado**

---

## 8. Paso 4 — Persistir por UUID y validar sin reiniciar

**Objetivo:** montar de forma reproducible evitando dependencia de `/dev/sdX`, cuyo nombre puede cambiar entre arranques.

```bash
sudo cp -a /etc/fstab /etc/fstab.b2.bak
sudo blkid /dev/sdb1

# Línea agregada a /etc/fstab:
UUID=e1075b87-a305-4208-aff1-15c5ba570935 /srv/proyecto ext4 defaults,nofail 0 2

sudo findmnt --verify --verbose
sudo umount /srv/proyecto
sudo mount -a
findmnt /srv/proyecto
sudo systemctl daemon-reload
```

### Explicación de cada comando

- `cp -a /etc/fstab /etc/fstab.b2.bak` → respaldo del archivo antes de editarlo. `-a` preserva permisos, dueño y timestamps.
- `blkid /dev/sdb1` → confirma el UUID exacto a usar (evita errores de tipeo).
- **Línea agregada en `/etc/fstab`** — cada campo:

| Campo | Valor | Significado |
|---|---|---|
| 1 | `UUID=e1075b87-...` | identifica el filesystem sin depender del nombre de dispositivo |
| 2 | `/srv/proyecto` | punto de montaje |
| 3 | `ext4` | tipo de filesystem |
| 4 | `defaults,nofail` | `defaults` = opciones estándar (rw, suid, exec, etc.); `nofail` = si el disco no aparece al arrancar, el sistema bootea igual, sin quedar atascado en modo emergencia |
| 5 | `0` | flag de `dump` (respaldo legacy, en desuso, se deja en 0) |
| 6 | `2` | orden de `fsck` al bootear (0 = no chequear, 1 = raíz, 2 = el resto de los filesystems) |

- `findmnt --verify --verbose` → valida la sintaxis de `fstab` **antes** de confiar en ella, sin necesidad de reiniciar.
- `umount` + `mount -a` → simula un arranque: desmonta lo hecho a mano y deja que el sistema lo monte solo leyendo `fstab`. Es la prueba real de que la línea nueva funciona.
- `systemctl daemon-reload` → limpia el warning de que systemd tenía en caché la versión anterior de `fstab`.

### Resultado obtenido

```
/srv/proyecto
   [ ] target exists
   [ ] userspace options: nofail
   [ ] UUID=e1075b87-... translated to /dev/sdb1
   [ ] source /dev/sdb1 exists
   [ ] FS type is ext4

0 parse errors, 0 errors, 2 warnings
```

```
TARGET        SOURCE    FSTYPE OPTIONS
/srv/proyecto /dev/sdb1 ext4   rw,relatime
```

Las 2 advertencias (`[W]`) no eran errores: una era sobre el `dump` no usado, la otra sobre el caché de systemd (resuelta con `daemon-reload`).

### Error frecuente
Reiniciar la máquina para "probar" una línea de `fstab` no validada — si hay un error de sintaxis, el sistema puede no arrancar correctamente.

### Seguridad y reversión
Se mantiene consola y respaldo disponibles. `nofail` evita que un volumen de datos opcional detenga el arranque, pero no reemplaza el monitoreo del disco.
Reversión: `sudo cp -a /etc/fstab.b2.bak /etc/fstab && sudo mount -a`

**Punto de control 4 completado**

---

## 9. Paso 5 — Implementar política grupal con setgid

**Objetivo:** permitir colaboración entre dos operadores sin usar `chmod 777`.

```bash
sudo useradd -m -s /bin/bash lukas3.1
sudo passwd lukas3.1

sudo groupadd -f cmsops
sudo usermod -aG cmsops lukas3
sudo usermod -aG cmsops lukas3.1

sudo install -d -o root -g cmsops -m 2770 /srv/proyecto/compartido
stat -c "%A %a %U %G %n" /srv/proyecto/compartido
```

### Explicación de cada comando

- `useradd -m -s /bin/bash lukas3.1` → crea el segundo usuario operador; `-m` crea su directorio home, `-s /bin/bash` define su shell.
- `groupadd -f cmsops` → crea el grupo `cmsops`; `-f` evita error si ya existiera.
- `usermod -aG cmsops <usuario>` → agrega el usuario al grupo. **`-a` (append) es crítico**: sin él, el usuario pierde todos sus demás grupos secundarios.
- `install -d -o root -g cmsops -m 2770 /srv/proyecto/compartido` → crea la carpeta compartida con:
  - dueño `root`, grupo `cmsops`
  - modo `2770`: el **`2` inicial es el bit setgid**

### Desglose del modo `2770`

- `2` → **setgid**: todo archivo/carpeta nuevo creado dentro hereda automáticamente el grupo `cmsops`, sin importar qué usuario lo cree.
- `7` (dueño) → root: lectura + escritura + ejecución
- `7` (grupo) → cmsops: lectura + escritura + ejecución
- `0` (otros) → nada

### Resultado obtenido

```
drwxrws--- 2770 root cmsops /srv/proyecto/compartido
```

La `s` en la posición de ejecución del grupo (`rws` en vez de `rwx`) es el indicador visual de que setgid está activo.

### Detalle importante: sesiones y grupos

Los grupos secundarios se cargan al iniciar sesión. Una sesión de `lukas3` ya abierta **antes** de ejecutar `usermod -aG` no reconoce el grupo nuevo hasta:
- abrir una sesión nueva (recomendado para operación real), o
- usar `newgrp cmsops` para una prueba puntual en una sub-shell (no recomendado como práctica habitual)

### Prueba de colaboración real

```bash
# Como lukas3 (con newgrp o sesión nueva):
touch /srv/proyecto/compartido/archivo-lukas3.txt
stat -c "%U %G %n" /srv/proyecto/compartido/archivo-lukas3.txt

# Como lukas3.1 (sesión separada, ej. su - lukas3.1):
touch /srv/proyecto/compartido/archivo-lukas3.1.txt
stat -c "%U %G %n" /srv/proyecto/compartido/archivo-lukas3.1.txt
```

**Resultado:** ambos archivos, creados por usuarios distintos, con grupo `cmsops` heredado automáticamente. Confirma que setgid funciona: sin él, cada archivo habría heredado el grupo primario personal de su creador, y el otro usuario no habría podido escribir sobre él.

### Error frecuente
Olvidar el `-a` en `usermod`, o esperar que el cambio de grupo se refleje en una sesión ya abierta.

### Seguridad y reversión
`newgrp` se usa solo para prueba controlada; en operación real, sesión nueva. Reversión: retirar usuarios del grupo y restaurar propietario/modo documentados.

**Punto de control 5 completado**

---

## 10. Paso 6 — Evaluar umask, sticky bit y ACL

**Objetivo:** justificar cuándo cada mecanismo aporta valor real, evitando aplicarlos "por costumbre".

```bash
umask 0007
touch /srv/proyecto/compartido/prueba-umask
stat -c "%A %a %G %n" /srv/proyecto/compartido/prueba-umask

sudo setfacl -m u:lukas3.1:r-X /srv/proyecto/compartido
getfacl /srv/proyecto/compartido

namei -l /srv/proyecto/compartido/prueba-umask

# Reversión de la ACL:
sudo setfacl -x u:lukas3.1 /srv/proyecto/compartido
```

### Explicación de cada comando

- `umask 0007` → define qué permisos se **restan por defecto** a los archivos nuevos creados en la sesión actual. El `0007` resta todo acceso a "otros" (último dígito), como capa extra de seguridad además del setgid.
- `setfacl -m u:lukas3.1:r-X /srv/proyecto/compartido` → agrega una **ACL** (Access Control List): otorga a un usuario específico permiso de lectura + entrada a subcarpetas (`r-X`), sin necesidad de que sea parte del grupo `cmsops`. Uso típico: un auditor externo que solo necesita revisar contenido, no colaborar.
- `getfacl` → muestra las ACL activas sobre el directorio.
- `namei -l` → recorre la ruta completa mostrando los permisos efectivos en cada nivel (útil para diagnosticar por qué un acceso falla o funciona).
- `setfacl -x` → elimina la entrada ACL agregada (reversión).

### Sobre el sticky bit — análisis, no implementación

El sticky bit **no se activa** en este laboratorio. Justificación conceptual:

> El sticky bit sirve cuando *cualquier usuario* puede escribir en un directorio compartido pero cada quien debe poder borrar únicamente lo suyo (el caso clásico es `/tmp`, donde conviven procesos de todos los usuarios del sistema). En `/srv/proyecto/compartido`, el control de acceso ya está resuelto de forma más estricta por el grupo cerrado `cmsops` (modo `2770`, sin acceso para "otros"). Agregar sticky bit aquí sería redundante y no resolvería ningún riesgo adicional — el filtro real es la pertenencia al grupo, no el borrado selectivo.

### Error frecuente
Agregar ACL "por costumbre" sin una excepción real que la justifique — esto oscurece el modelo de permisos y dificulta el diagnóstico futuro (siempre revisar con `getfacl`/`namei -l` si hay ACL antes de asumir que el modelo es solo dueño/grupo/otros).

### Seguridad y reversión
Se prefieren los grupos sobre las ACL como mecanismo principal. El sticky bit no reemplaza el control grupal en un repositorio colaborativo cerrado.
Reversión: `sudo setfacl -x u:lukas3.1 /srv/proyecto/compartido`

**Punto de control 6 completado**

---

## 11. Resumen de la solución

| Elemento | Decisión tomada | Por qué |
|---|---|---|
| Identificación del disco | `/dev/sdb`, confirmado por ausencia de FSTYPE y de mountpoint | Evita destruir el disco del sistema |
| Persistencia del montaje | UUID en `/etc/fstab` con `nofail` | Independiente del nombre de dispositivo; no bloquea el arranque si el disco falla |
| Colaboración entre operadores | Grupo `cmsops` + directorio con `setgid` (`2770`) | Herencia automática de grupo, sin abrir a "otros" ni usar `777` |
| Permisos por defecto | `umask 0007` | Refuerza que "otros" nunca tenga acceso, incluso por descuido |
| Excepciones puntuales | ACL de solo lectura para casos no cubiertos por el grupo | Documentada explícitamente, no usada como mecanismo principal |
| Borrado selectivo | Sticky bit **no aplicado** | El control ya lo da el grupo cerrado; sticky bit sería redundante aquí |

## 12. Qué pasaría en caso de falla (justificación de `nofail`)

Si el disco `/dev/sdb` no estuviera disponible en un arranque futuro (desconectado, dañado, etc.), la opción `nofail` en `fstab` permite que el sistema complete el arranque normalmente, dejando `/srv/proyecto` sin montar en vez de detener el proceso de boot en modo de emergencia. Esto es apropiado porque es un volumen de datos adicional, no crítico para el sistema operativo — pero requiere monitoreo activo (alertas de espacio o de montaje) para detectar el problema a tiempo.
