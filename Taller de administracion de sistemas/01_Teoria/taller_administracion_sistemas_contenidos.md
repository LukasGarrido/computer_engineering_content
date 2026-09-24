# Taller de Administración de Sistemas (EIN-090B)
### Guía de contenidos: teoría y ejemplos prácticos

> Basado en el programa de asignatura de la Universidad Técnica Federico Santa María.
> Prerrequisitos: Sistemas Operativos, Redes de Computadores, Linux a nivel usuario.

---

## Índice

1. [Distribuciones, ambientes e instalación de sistemas operativos](#1-distribuciones-ambientes-e-instalación-de-sistemas-operativos)
2. [Administración remota](#2-administración-remota)
3. [Redes y cortafuegos](#3-redes-y-cortafuegos)
4. [Servicios](#4-servicios)
5. [Sistemas de archivos](#5-sistemas-de-archivos)
6. [Seguridad y administración de paquetes de software](#6-seguridad-y-administración-de-paquetes-de-software)
7. [Virtualización y contenedores](#7-virtualización-y-contenedores)

---

## 1. Distribuciones, ambientes e instalación de sistemas operativos

### 1.1 Teoría

Una **distribución Linux (distro)** es un sistema operativo completo construido sobre el kernel de Linux, más un conjunto de herramientas, gestor de paquetes y filosofía de configuración.

Familias principales que conviene distinguir para un administrador de sistemas:

| Familia | Ejemplos | Gestor de paquetes | Uso típico |
|---|---|---|---|
| Debian-based | Debian, Ubuntu | APT (`.deb`) | Servidores, escritorio |
| Red Hat-based | RHEL, CentOS Stream, Rocky, Fedora | DNF/YUM (`.rpm`) | Empresa, servidores |
| SUSE | openSUSE, SLES | Zypper (`.rpm`) | Empresa |
| Arch-based | Arch, Manjaro | Pacman | Rolling release, aprendizaje |
| Independientes | Alpine | APK | Contenedores (muy liviana) |

**Ambientes de instalación** que un sysadmin debe manejar:

- **Bare metal**: instalación directa sobre hardware físico.
- **Virtualizado**: sobre un hipervisor (KVM, VirtualBox, ESXi).
- **Cloud**: instancias en AWS/GCP/Azure a partir de imágenes (AMI, etc.).
- **Automatizado**: instalación desatendida vía *kickstart* (RHEL) o *preseed*/*cloud-init* (Debian/Ubuntu).

Conceptos clave del proceso de instalación:

- **Particionamiento**: esquema clásico MBR vs GPT; particiones típicas `/`, `/boot`, `swap`, `/home`, `/var`.
- **LVM (Logical Volume Manager)**: permite redimensionar particiones lógicas sin depender de límites físicos del disco.
- **Bootloader**: GRUB2 es el estándar en la mayoría de las distros modernas.
- **Kernel vs espacio de usuario**: el kernel gestiona hardware y recursos; el espacio de usuario corre los programas.

### 1.2 Ejemplos prácticos

**Ver la distribución y versión del kernel:**
```bash
cat /etc/os-release
uname -a
```

**Instalación desatendida con cloud-init (ejemplo mínimo, `user-data`):**
```yaml
#cloud-config
hostname: srv-web01
users:
  - name: admin
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
      - ssh-ed25519 AAAA...
packages:
  - nginx
  - htop
runcmd:
  - systemctl enable nginx
```

**Gestión de LVM (crear un volumen lógico):**
```bash
pvcreate /dev/sdb
vgcreate vg_data /dev/sdb
lvcreate -L 20G -n lv_app vg_data
mkfs.ext4 /dev/vg_data/lv_app
mount /dev/vg_data/lv_app /srv/app
```

**Ver particiones y layout de disco:**
```bash
lsblk
fdisk -l
```

---

## 2. Administración remota

### 2.1 Teoría

La administración remota permite operar un servidor sin acceso físico a él. Es la base del trabajo diario de un sysadmin, especialmente en entornos de nube o data center.

- **SSH (Secure Shell)**: protocolo estándar para acceso remoto cifrado (puerto 22 por defecto). Reemplaza a Telnet/rlogin, que envían datos en texto plano.
- **Autenticación**: por contraseña (menos segura) o por **llaves públicas/privadas** (recomendada). La llave privada nunca sale de la máquina del administrador.
- **Herramientas asociadas**: `scp`/`rsync` (transferencia de archivos), `ssh-agent` (gestión de llaves en memoria), **tunneling/port forwarding** (exponer un servicio remoto de forma segura).
- **Automatización remota**: herramientas como **Ansible** ejecutan tareas en muchos servidores a la vez sobre SSH, sin agentes instalados en el destino.
- **Multiplexores de terminal**: `tmux`/`screen` permiten mantener sesiones vivas aunque se corte la conexión.

### 2.2 Ejemplos prácticos

**Generar un par de llaves y copiarla al servidor:**
```bash
ssh-keygen -t ed25519 -C "admin@laptop"
ssh-copy-id admin@192.168.1.50
```

**Conectarse y deshabilitar login por contraseña (más seguro) en `/etc/ssh/sshd_config`:**
```
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
```
```bash
systemctl restart sshd
```

**Copiar archivos de forma remota:**
```bash
scp informe.pdf admin@192.168.1.50:/home/admin/
rsync -avz ./proyecto/ admin@192.168.1.50:/srv/proyecto/
```

**Túnel SSH para acceder a un servicio interno (ej. una base de datos que solo escucha en localhost del servidor remoto):**
```bash
ssh -L 5432:localhost:5432 admin@192.168.1.50
# ahora localhost:5432 en tu máquina apunta al Postgres del servidor
```

**Sesión persistente con tmux:**
```bash
tmux new -s despliegue
# ... trabajo ...
# Ctrl+B, D para desconectar sin cerrar el proceso
tmux attach -t despliegue
```

**Playbook básico de Ansible (ejecutar un comando en varios hosts):**
```yaml
- hosts: webservers
  become: yes
  tasks:
    - name: Actualizar paquetes
      apt:
        update_cache: yes
        upgrade: dist
```

---

## 3. Redes y cortafuegos

### 3.1 Teoría

Un servidor no vive aislado: necesita configuración de red correcta y reglas que controlen qué tráfico entra y sale.

- **Capas relevantes**: direccionamiento IP (v4/v6), máscaras de subred, gateway, DNS.
- **Interfaces de red**: en Linux moderno se gestionan con `ip` (reemplaza a `ifconfig`) y `NetworkManager`/`netplan`/`systemd-networkd` según la distro.
- **Cortafuegos (firewall)**: filtra paquetes según reglas (puerto, IP origen/destino, protocolo). En Linux el motor de bajo nivel es **netfilter**, gestionado mediante:
  - `iptables` (clásico, basado en cadenas: INPUT, OUTPUT, FORWARD).
  - `nftables` (sucesor moderno de iptables).
  - `firewalld` (capa de administración con "zonas", usado en RHEL/Fedora).
  - `ufw` (interfaz simplificada sobre iptables, usada en Ubuntu).
- **NAT**: traducción de direcciones, fundamental para que redes privadas salgan a internet.
- **Conceptos de seguridad de red**: principio de menor privilegio (cerrar todo por defecto, abrir solo lo necesario), segmentación de red, *rate limiting*.

### 3.2 Ejemplos prácticos

**Ver y configurar interfaces:**
```bash
ip addr show
ip route show
ip addr add 192.168.1.100/24 dev eth0
```

**Reglas básicas con `ufw` (Ubuntu):**
```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp        # SSH
ufw allow 80,443/tcp    # Web
ufw enable
ufw status verbose
```

**Reglas equivalentes con `nftables`:**
```bash
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }
nft add rule inet filter input tcp dport 22 accept
nft add rule inet filter input tcp dport {80,443} accept
nft add rule inet filter input ct state established,related accept
```

**Diagnóstico de red:**
```bash
ping -c 4 8.8.8.8
traceroute google.com
ss -tulpn          # puertos y servicios escuchando
dig midominio.cl   # consultas DNS
```

**NAT básico (compartir salida a internet, ejemplo típico de router/gateway):**
```bash
nft add rule inet nat postrouting oifname "eth0" masquerade
```

---

## 4. Servicios

### 4.1 Teoría

Un "servicio" es un programa que corre en segundo plano (*daemon*) proveyendo una función: web, correo, base de datos, DNS, etc.

- **systemd**: es el sistema de inicio (init) y gestor de servicios en la mayoría de las distros modernas (Ubuntu, Debian, RHEL, Fedora). Reemplazó a SysVinit.
  - **Unit files** (`.service`) describen cómo arrancar, detener y supervisar un proceso.
  - `systemctl` es la herramienta para controlar servicios.
  - `journalctl` consulta los logs centralizados por systemd (journal).
- **Servicios comunes de un sysadmin**:
  - **Web**: Nginx, Apache.
  - **Base de datos**: MySQL/MariaDB, PostgreSQL.
  - **DNS**: BIND, dnsmasq.
  - **Correo**: Postfix, Dovecot.
  - **Sincronización de tiempo**: `chronyd`/`ntpd` (crítico para logs, certificados y Kerberos).
- **Alta disponibilidad**: `systemd` permite reinicio automático ante fallas (`Restart=always`) y dependencias entre servicios (`After=`, `Requires=`).

### 4.2 Ejemplos prácticos

**Controlar un servicio con systemd:**
```bash
systemctl status nginx
systemctl start nginx
systemctl enable nginx     # arranque automático en boot
systemctl restart nginx
```

**Ver logs de un servicio:**
```bash
journalctl -u nginx -f          # seguir en tiempo real
journalctl -u nginx --since "1 hour ago"
```

**Crear un servicio propio (`/etc/systemd/system/miapp.service`):**
```ini
[Unit]
Description=Mi aplicación Python
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/miapp/app.py
Restart=always
User=miapp
WorkingDirectory=/opt/miapp

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload
systemctl enable --now miapp
```

**Configuración mínima de Nginx como proxy inverso (`/etc/nginx/sites-available/app`):**
```nginx
server {
    listen 80;
    server_name miapp.cl;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
    }
}
```

---

## 5. Sistemas de archivos

### 5.1 Teoría

El sistema de archivos define cómo se organizan y acceden los datos en el disco.

- **Tipos comunes en Linux**:
  - **ext4**: el más usado, estable, con *journaling* (registro de cambios que evita corrupción tras un corte de energía).
  - **XFS**: buen rendimiento con archivos grandes, usado en RHEL por defecto.
  - **Btrfs / ZFS**: sistemas modernos con snapshots, compresión y checksums integrados.
  - **NTFS/FAT32**: relevantes para interoperar con Windows/dispositivos externos.
- **Jerarquía estándar de Linux (FHS)**: `/etc` (configuración), `/var` (datos variables, logs), `/home` (usuarios), `/usr` (programas), `/tmp` (temporales), `/proc` y `/sys` (interfaces virtuales al kernel).
- **Montaje**: un sistema de archivos debe *montarse* en un punto del árbol (`/mnt`, `/media`) para ser accesible; `/etc/fstab` define montajes automáticos al arrancar.
- **Permisos**: modelo clásico Unix (usuario/grupo/otros, lectura-escritura-ejecución) y **ACLs** (listas de control de acceso) para permisos más granulares.
- **Cuotas de disco**: limitan cuánto espacio puede usar un usuario o grupo.
- **RAID**: combina discos para redundancia (RAID1), rendimiento (RAID0) o ambos (RAID5/6/10).

### 5.2 Ejemplos prácticos

**Ver uso de disco y sistemas de archivos montados:**
```bash
df -hT
mount | column -t
du -sh /var/log/*
```

**Montar un disco nuevo de forma persistente:**
```bash
mkfs.ext4 /dev/sdb1
mkdir /srv/datos
echo "/dev/sdb1  /srv/datos  ext4  defaults  0 2" >> /etc/fstab
mount -a
```

**Permisos y ACLs:**
```bash
chmod 750 /srv/datos
chown usuario:grupo /srv/datos

# ACL: dar acceso de lectura a un usuario específico sin cambiar el owner
setfacl -m u:auditor:rx /srv/datos
getfacl /srv/datos
```

**Cuotas de disco (después de habilitar `usrquota` en fstab):**
```bash
quotacheck -cug /srv/datos
edquota -u usuario1
repquota /srv/datos
```

**RAID por software con `mdadm` (RAID1, espejo):**
```bash
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc
mkfs.ext4 /dev/md0
```

---

## 6. Seguridad y administración de paquetes de software

### 6.1 Teoría

**Gestión de paquetes**: cada distro tiene un gestor que resuelve dependencias e instala software de forma reproducible.

| Distro | Comando | Formato |
|---|---|---|
| Debian/Ubuntu | `apt` | `.deb` |
| RHEL/Fedora | `dnf` | `.rpm` |
| openSUSE | `zypper` | `.rpm` |
| Alpine | `apk` | `.apk` |

**Actualizaciones**: mantener el sistema parchado es la primera línea de defensa. Distinguir entre:
- Actualizaciones de seguridad (críticas, deben aplicarse rápido).
- Actualizaciones de versión mayor (requieren pruebas previas).

**Seguridad del sistema — pilares básicos**:
- **Principio de menor privilegio**: usuarios sin privilegios por defecto, `sudo` para elevar puntualmente.
- **Hardening**: deshabilitar servicios innecesarios, cerrar puertos, `SELinux`/`AppArmor` (control de acceso obligatorio, más allá de los permisos Unix clásicos).
- **Detección de intrusos**: `fail2ban` (bloquea IPs tras intentos fallidos de login), auditoría con `auditd`.
- **Gestión de vulnerabilidades**: escaneo de CVEs conocidos en los paquetes instalados.
- **Backups**: parte de la seguridad es poder recuperarse de un incidente, no solo prevenirlo.

### 6.2 Ejemplos prácticos

**Actualizar el sistema (Debian/Ubuntu):**
```bash
apt update && apt upgrade -y
apt list --upgradable
```

**Actualizar el sistema (RHEL/Fedora):**
```bash
dnf check-update
dnf upgrade -y
```

**Instalar/remover paquetes:**
```bash
apt install fail2ban -y
apt remove --purge paquete-viejo
apt autoremove
```

**Configurar `fail2ban` para proteger SSH (`/etc/fail2ban/jail.local`):**
```ini
[sshd]
enabled = true
port = 22
maxretry = 5
bantime = 3600
```
```bash
systemctl enable --now fail2ban
fail2ban-client status sshd
```

**Ver estado de SELinux (RHEL) o AppArmor (Ubuntu):**
```bash
getenforce                # SELinux: Enforcing / Permissive / Disabled
aa-status                 # AppArmor
```

**Auditar usuarios con privilegios y accesos:**
```bash
last -a                   # últimos logins
grep sudo /etc/group      # quién puede usar sudo
journalctl _COMM=sudo     # historial de comandos con sudo
```

---

## 7. Virtualización y contenedores

### 7.1 Teoría

Dos formas complementarias de aprovechar un mismo servidor físico corriendo múltiples cargas de trabajo aisladas entre sí.

**Virtualización (VMs)**: un **hipervisor** virtualiza el hardware para que cada máquina virtual corra su propio kernel completo.

- **Tipo 1 (bare metal)**: corre directamente sobre el hardware (KVM, ESXi, Xen). Se usa en servidores/data centers.
- **Tipo 2 (hosted)**: corre como aplicación sobre un SO anfitrión (VirtualBox, VMware Workstation). Se usa en estaciones de trabajo/desarrollo.
- Aislamiento fuerte (a nivel de hardware virtual), pero con más overhead y arranque más lento.

**Contenedores**: comparten el kernel del host y se aíslan mediante mecanismos del propio kernel de Linux:

- **Namespaces**: controlan **qué ve** un proceso (PID, red, mount, usuario, hostname, IPC). Cada contenedor cree estar solo en la máquina.
- **cgroups**: controlan **cuánto puede usar** un proceso (CPU, memoria, disco, red), evitando que un contenedor consuma todos los recursos del host.
- **Docker** empaqueta ambos mecanismos junto con un sistema de imágenes por capas, facilitando su uso.
- **OCI** (Open Container Initiative) estandariza el formato de imágenes y runtime para que distintas herramientas (Docker, Podman, containerd) sean compatibles entre sí.
- Arranque casi instantáneo y bajo overhead, a cambio de un aislamiento más débil que una VM (comparten kernel).

**Cuándo usar cada una**:
- VM: se necesitan distintos sistemas operativos, o aislamiento de seguridad muy fuerte (multi-tenant estricto).
- Contenedor: se necesita desplegar rápido, escalar horizontalmente, y todas las cargas usan el mismo tipo de kernel (Linux).
- **Orquestación**: cuando hay muchos contenedores, se usan herramientas como **Kubernetes** o **Docker Swarm** para gestionarlos (despliegue, escalado, autorecuperación).

### 7.2 Ejemplos prácticos

**Crear una VM con KVM/libvirt (línea de comandos):**
```bash
virt-install \
  --name vm-web01 \
  --vcpus 2 --memory 2048 \
  --disk size=20 \
  --cdrom /iso/ubuntu-24.04.iso \
  --network network=default
```

**Gestión básica de VMs:**
```bash
virsh list --all
virsh start vm-web01
virsh shutdown vm-web01
```

**Contenedores con Docker — comandos básicos:**
```bash
docker run -d --name web -p 8080:80 nginx
docker ps
docker logs -f web
docker exec -it web bash
docker stop web && docker rm web
```

**Límites de recursos en un contenedor (equivalente manual a cgroups):**
```bash
docker run -d --name app --memory=512m --cpus=0.5 miapp:latest
```

**Dockerfile mínimo (construir una imagen propia):**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```
```bash
docker build -t miapp:latest .
docker run -d -p 5000:5000 miapp:latest
```

**Orquestación básica con `docker compose` (varios servicios juntos):**
```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secreto
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```
```bash
docker compose up -d
docker compose logs -f
```

## Bibliografía del ramo

- **Texto guía**: Nemeth, E., Snyder, G., et al. *UNIX and Linux System Administration Handbook* (5th Edition), 2017.
- **Complementaria**: Dean, A. K. *Linux Administration Cookbook*, 2018.
