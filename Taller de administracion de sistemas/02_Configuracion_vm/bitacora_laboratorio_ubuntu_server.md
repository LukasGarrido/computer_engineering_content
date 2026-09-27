# Bitácora de Laboratorio: Administración de Ubuntu Server 24.04

Resumen completo de comandos ejecutados, archivos de configuración (con su
contenido íntegro) y problemas resueltos durante la configuración de una VM
Ubuntu Server 24.04 en VirtualBox, en el orden real en que ocurrieron.

**Entorno:**
- Host: Windows (PowerShell)
- Hipervisor: VirtualBox
- Huésped: Ubuntu Server 24.04, usuario `lukas`
- Interfaz de red de la VM: `enp0s3`
- Red local: `192.168.1.0/24`, gateway `192.168.1.1`
- IP final asignada a la VM: `192.168.1.183`

---

## Índice

1. [SSH — acceso remoto](#1-ssh--acceso-remoto)
2. [Red — modo Bridged en VirtualBox](#2-red--modo-bridged-en-virtualbox)
3. [IP estática con Netplan](#3-ip-estática-con-netplan)
4. [Conflicto de IPs entre dos VMs](#4-conflicto-de-ips-entre-dos-vms)
5. [Ruta por defecto faltante](#5-ruta-por-defecto-faltante)
6. [Firewall (ufw)](#6-firewall-ufw)
7. [DNS](#7-dns)
8. [Servicio: Nginx](#8-servicio-nginx)
9. [Sistemas de archivos y LVM (en progreso)](#9-sistemas-de-archivos-y-lvm-en-progreso)
10. [Archivos de configuración — versión final](#10-archivos-de-configuración--versión-final)
11. [Cheatsheet de comandos](#11-cheatsheet-de-comandos)

---

## 1. SSH — acceso remoto

### Verificar / instalar el servicio (dentro de la VM)
```bash
sudo systemctl status ssh
# si no estuviera instalado:
sudo apt update && sudo apt install openssh-server -y
sudo systemctl enable --now ssh
```

### Intentos fallidos (desde PowerShell en Windows)
```powershell
ssh lukas@10.0.2.15/24
# ssh: Could not resolve hostname 10.0.2.15/24: Host desconocido.
# Causa: no se puede incluir la máscara /24 en el destino de ssh.

ssh lukas@10.0.2.15
# ssh: connect to host 10.0.2.15 port 22: Connection timed out
# Causa: la VM estaba en modo de red NAT (red interna aislada de VirtualBox,
# no alcanzable desde el host).

ssh -p 2222 lukas@localhost
# ssh: connect to host localhost port 2222: Connection refused
# Causa: localhost apunta al propio Windows, no a la VM.
```

### Diagnóstico de adaptadores de red en Windows
```powershell
ipconfig
```
Se identificó el adaptador real (con IP y gateway) frente a los virtuales:

| Adaptador | IP | Gateway | ¿Real? |
|---|---|---|---|
| Wi-Fi | 192.168.1.144 | 192.168.1.1 | ✅ Sí — el que se usó |
| Ethernet 2 (VirtualBox Host-Only) | 192.168.56.1 | — | ❌ No |
| vEthernet (WSL) | 172.24.240.1 | — | ❌ No |

### Verificación final dentro de la VM
```bash
ip addr show
sudo systemctl status ssh
sudo ss -tulpn
```
```
tcp   LISTEN   0   4096   0.0.0.0:22
tcp   LISTEN   0   4096   [::]:22
```

### Conexión exitosa
```powershell
ssh lukas@192.168.1.183
```

---

## 2. Red — modo Bridged en VirtualBox

**Pasos aplicados en VirtualBox (VM apagada):**

1. Configuración de la VM → **Red** → Adaptador 1.
2. "Conectado a": cambiar de **NAT** a **Adaptador puente**.
3. "Nombre": seleccionar el adaptador físico real → **Wi-Fi** (Intel Wi-Fi, en este caso).
4. Encender la VM.

Con esto la VM pasó de vivir en la red aislada `10.0.2.0/24` (NAT) a ser un
dispositivo más dentro de la LAN real `192.168.1.0/24`.

---

## 3. IP estática con Netplan

### Ubicar el archivo
```bash
ls /etc/netplan/
cat /etc/netplan/*.yaml
```

### Editar
```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

### Contenido aplicado (versión correcta y completa)
```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - 192.168.1.183/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [1.1.1.1, 8.8.8.8]
```

| Campo | Valor | Función |
|---|---|---|
| `dhcp4: no` | — | Desactiva IP automática por DHCP |
| `addresses` | `192.168.1.183/24` | IP fija + máscara de subred |
| `routes → via` | `192.168.1.1` | Gateway / ruta por defecto |
| `nameservers` | `1.1.1.1`, `8.8.8.8` | Servidores DNS |

### Aplicar y verificar
```bash
sudo netplan apply
ip addr show
```

---

## 4. Conflicto de IPs entre dos VMs

**Síntoma:** dos VMs distintas quedaron con la misma IP estática
`192.168.1.183` en sus respectivos `50-cloud-init.yaml` → fallas
intermitentes de conexión y DNS (dos dispositivos no pueden compartir una
misma IP en la red).

**Solución:** se cambió la IP estática de una de las VMs a una dirección
distinta dentro del mismo rango.

**Efecto secundario — SSH rechazó la conexión:**
Windows tenía guardada la huella digital (fingerprint) del servidor asociada
a esa IP; al haber dos servidores distintos usándola, SSH lo interpretó como
alerta de seguridad.
```powershell
ssh-keygen -R 192.168.1.183
```
Esto limpia la entrada de `known_hosts`, permitiendo reconectar (pidiendo
confirmar la huella nueva).

---

## 5. Ruta por defecto faltante

**Síntoma**, tras corregir el conflicto de IPs:
```bash
ping -c 3 8.8.8.8
# ping: connect: Network is unreachable

dig google.com
# ;; communications error to 127.0.0.53#53: timed out
```

**Diagnóstico:**
```bash
ip route show
# 192.168.1.0/24 dev enp0s3 proto kernel scope link src 192.168.1.183
```
Solo existía la ruta local; faltaba la ruta por defecto.

**Causa raíz:** al editar el YAML para cambiar la IP (paso 4), se omitió por
error la sección `routes`, quedando así (versión rota):
```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - 192.168.1.183/24
      nameservers:
        addresses: [1.1.1.1, 8.8.8.8]
```

**Solución:** se restauró la sección `routes` (ver contenido correcto en la
sección 3 / sección 10).
```bash
sudo netplan apply
```

**Verificación:**
```bash
ip route show
# default via 192.168.1.1 dev enp0s3 proto static
# 192.168.1.0/24 dev enp0s3 proto kernel scope link src 192.168.1.183

ping -c 3 8.8.8.8      # 0% packet loss
dig google.com         # respuesta correcta
```

**Concepto clave:** una IP + máscara solo permite hablar con la red local
("los vecinos del barrio"); la ruta por defecto es la que indica a quién
entregarle el tráfico que va fuera de esa red ("la salida del barrio hacia
la carretera"), normalmente el router.

---

## 6. Firewall (ufw)

```bash
sudo ufw status verbose                # estado inicial: inactivo

sudo ufw default deny incoming         # política por defecto: bloquear entrante
sudo ufw default allow outgoing        # permitir saliente

sudo ufw allow 22/tcp                  # permitir SSH ANTES de activar (crítico)

sudo ufw enable                        # activar firewall
sudo ufw status verbose                # verificar
```

**Estado resultante:**
```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
22/tcp (v6)                ALLOW IN    Anywhere (v6)
```

M�s adelante se agregó también:
```bash
sudo ufw allow 80/tcp                  # para Nginx (sección 8)
```

---

## 7. DNS

```bash
resolvectl status
```
```
Global
         Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
  resolv.conf mode: stub

Link 2 (enp0s3)
    Current Scopes: DNS
Current DNS Server: 8.8.8.8
       DNS Servers: 1.1.1.1 8.8.8.8
```

```bash
cat /etc/resolv.conf
```
```
nameserver 127.0.0.53
options edns0 trust-ad
search .
```
(`127.0.0.53` es el stub resolver local de `systemd-resolved`, que reenvía
las consultas a los DNS reales configurados en Netplan).

```bash
sudo systemctl status systemd-resolved
sudo systemctl restart systemd-resolved   # usado durante el diagnóstico de la sección 5

dig google.com
```

**DNS local de prueba, en Windows** (no en la VM):
```powershell
notepad C:\Windows\System32\drivers\etc\hosts
```
Línea agregada:
```
192.168.1.183    servidor.local
```
Permite `ssh lukas@servidor.local` en vez de usar la IP directamente.

---

## 8. Servicio: Nginx

```bash
sudo apt update
sudo apt install nginx -y

sudo systemctl status nginx
curl localhost

sudo ufw allow 80/tcp
sudo ufw status verbose
```

**Prueba final**, desde el navegador en Windows:
```
http://192.168.1.183
```
→ Página de bienvenida de Nginx cargada correctamente.

Personalización opcional:
```bash
sudo nano /var/www/html/index.nginx-debian.html
```

---

## 9. Sistemas de archivos y LVM (en progreso)

```bash
df -hT
lsblk
mount | grep sda
```

**Resultado:**
```
Filesystem                        Type   Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv ext4    12G  4.7G  6.0G  44% /
/dev/sda2                         ext4   2.0G  104M  1.7G   6% /boot
```
```
sda                         8:0    0   25G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0    2G  0 part /boot
└─sda3                      8:3    0   23G  0 part
  └─ubuntu--vg-ubuntu--lv 252:0    0 11.5G  0 lvm  /
```

**Estructura identificada (LVM):**
```
sda3 (23G, contenedor LVM)
  → Volumen Físico (PV)
    → Grupo de Volúmenes (VG)
      → Volumen Lógico (LV): ubuntu--vg-ubuntu--lv (11.5G) → montado en /
```

**Hallazgo:** el LV raíz (11.5G) usa menos que el espacio disponible en
`sda3` (23G) → hay espacio libre sin asignar dentro del VG.

### Pendiente — próximos comandos a ejecutar
```bash
sudo pvs      # ver volumen físico y tamaño
sudo vgs      # ver grupo de volúmenes y espacio libre (VFree)
sudo lvs      # ver volumen(es) lógico(s) actuales
```

### Checklist del módulo
- [ ] Ejecutar y revisar `pvs` / `vgs` / `lvs`.
- [ ] Agrandar el volumen lógico raíz con el espacio libre (`lvextend` + `resize2fs`).
- [ ] Agregar un disco virtual nuevo en VirtualBox (Configuración → Almacenamiento → Agregar disco duro SATA).
- [ ] Formatear el disco nuevo (`mkfs.ext4 /dev/sdb1`), montarlo y dejarlo persistente en `/etc/fstab`.
- [ ] Practicar permisos Unix y ACLs (`chmod`, `chown`, `setfacl`, `getfacl`).
- [ ] (Opcional) Cuotas de disco por usuario.

---

## 10. Archivos de configuración — versión final

### `/etc/netplan/50-cloud-init.yaml`
```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - 192.168.1.183/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [1.1.1.1, 8.8.8.8]
```

### `/etc/resolv.conf` (gestionado automáticamente, no editar a mano)
```
nameserver 127.0.0.53
options edns0 trust-ad
search .
```

### Estado de `ufw` (`sudo ufw status verbose`)
```
Status: active
Default: deny (incoming), allow (outgoing), disabled (routed)

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
22/tcp (v6)                ALLOW IN    Anywhere (v6)
80/tcp                     ALLOW IN    Anywhere
80/tcp (v6)                ALLOW IN    Anywhere (v6)
```

### `ip route show` (esperado, con la red funcionando)
```
default via 192.168.1.1 dev enp0s3 proto static
192.168.1.0/24 dev enp0s3 proto kernel scope link src 192.168.1.183
```

### `/etc/hosts` en Windows (`C:\Windows\System32\drivers\etc\hosts`)
```
192.168.1.183    servidor.local
```

---

## 11. Cheatsheet de comandos

```bash
# --- Diagnóstico de red ---
ip addr show
ip route show
resolvectl status
dig google.com
ping -c 3 8.8.8.8

# --- SSH / servicios ---
sudo systemctl status <servicio>
sudo systemctl restart <servicio>
sudo ss -tulpn

# --- Firewall ---
sudo ufw status verbose
sudo ufw allow <puerto>/tcp
sudo ufw enable

# --- Netplan ---
cat /etc/netplan/*.yaml
sudo nano /etc/netplan/50-cloud-init.yaml
sudo netplan apply

# --- Discos y sistemas de archivos ---
df -hT
lsblk
sudo pvs
sudo vgs
sudo lvs
```

```powershell
# --- Windows ---
ipconfig
ssh usuario@IP
ssh -p PUERTO usuario@IP
ssh-keygen -R IP_ANTIGUA
notepad C:\Windows\System32\drivers\etc\hosts
```

---

## Pendientes generales del laboratorio

- [ ] Terminar módulo de sistemas de archivos (LVM + disco nuevo + permisos).
- [ ] Endurecer SSH: cambiar puerto, deshabilitar login por contraseña
      (pausado intencionalmente — foco actual es aprendizaje, no producción).
- [ ] Seguridad y administración de paquetes (`apt`, `fail2ban`, hardening básico).
- [ ] Virtualización y contenedores (Docker).
