# Taller de Administración de Sistemas — Índice de Asignatura (MOC)

Este índice centraliza los Objetos Virtuales de Aprendizaje (OVA), guías de contenidos teóricos y bitácoras prácticas de configuración de servidores Linux para la asignatura de **Taller de Administración de Sistemas** (USM - EIN-090B).

---

## 01. Teoría y Unidades de Aprendizaje (OVA)

### Objetos Virtuales de Aprendizaje (OVA)
- [[OVA_01_Maquinas_Virtuales_y_Contenedores|OVA 01 — Máquinas Virtuales, Hipervisores y Contenedores]]
  - *Diferencias fundamentales entre VM y Contenedores, hipervisores Tipo 1 vs Tipo 2, namespaces, cgroups, imágenes inmutables y arquitecturas de despliegue híbridas.*
- [[OVA_02_Datos_Acceso_y_Servicios_Red|OVA 02 — Datos, Control de Acceso y Servicios Fundamentales de Red]]
  - *Montaje persistente por UUID (`/etc/fstab`), permisos avanzados (setgid, sticky bit, ACL), cortafuegos UFW, asignación DHCP con Kea y resolución DNS con BIND 9.*

### Guía Global de Contenidos Teóricos y Prácticos
- [[taller_administracion_sistemas_contenidos|Guía Completa de Contenidos (Programa EIN-090B)]]
  - **1. Distribuciones e Instalación:** Familias Linux (Debian, RHEL, Arch, Alpine), particionamiento (GPT/MBR), LVM e instalación automatizada (`cloud-init`).
  - **2. Administración Remota:** Configuración segura de SSH, llaves criptográficas, redirección de puertos (SSH Tunneling) y multiplexores (`tmux`, `screen`).
  - **3. Redes y Cortafuegos:** Configuración de red con `netplan` e `iproute2`, tablas de rutas y filtrado de paquetes con `ufw`, `iptables` y `nftables`.
  - **4. Gestión de Servicios:** Arquitectura de `systemd`, administración con `systemctl`, inspección de logs con `journalctl` y servidores web (Nginx, Apache).
  - **5. Sistemas de Archivos y Almacenamiento:** Formateo (ext4, xfs), volúmenes lógicos con LVM, permisos POSIX, bit setgid, sticky bit y ACLs (`getfacl`/`setfacl`).
  - **6. Seguridad y Paquetes:** Gestión de repositorios (`apt`, `dnf`), compilación desde fuente, directivas de `sudoers` y auditoría del sistema.
  - **7. Virtualización y Contenedores:** Hipervisores (KVM/VirtualBox), motor Docker, `docker-compose`, redes bridge/host y gestión de volúmenes persistentes.

---

## 02. Configuraciones y Laboratorios Prácticos

### Bitácora de Configuración de Servidores (VM)
- [[bitacora_laboratorio_ubuntu_server|Bitácora de Laboratorio — Configuración de Ubuntu Server 24.04]]
  - *Procedimiento paso a paso en VirtualBox:*
    - Acceso SSH y gestión de usuarios (`lukas`).
    - Configuración de interfaz de red Bridged e IP estática mediante Netplan.
    - Diagnóstico y resolución de conflictos de IPs y rutas por defecto (`ip route`).
    - Reglas de filtrado de tráfico en UFW.
    - Despliegue y verificación del servidor web Nginx.
    - Cheatsheet de comandos esenciales de administración de sistemas.

---

## Herramientas y Comandos Clave por Dominio

| Dominio                  | Comandos Esenciales                                                                 |        |                       |                                                    |
| :----------------------- | :---------------------------------------------------------------------------------- | ------ | --------------------- | -------------------------------------------------- |
| **Redes y Diagnóstico**  | `ip a`, `ip route`, `netplan apply`, `ss -tulpn`, `ping`, `dig`, `traceroute`, `nc` |        |                       |                                                    |
| **Servicios y Procesos** | `systemctl status                                                                   | start  | stop                  | enable`, `journalctl -u`, `htop`, `ps aux`, `tmux` |
| **Almacenamiento y LVM** | `lsblk`, `fdisk`, `blkid`, `pvcreate`, `vgcreate`, `lvcreate`, `mount`, `df -h`     |        |                       |                                                    |
| **Permisos y Seguridad** | `chmod`, `chown`, `setfacl`, `getfacl`, `ufw status                                 | enable | allow`, `sudo visudo` |                                                    |
| **Contenedores**         | `docker run`, `docker-compose up -d`, `docker ps`, `docker logs`, `docker exec`     |        |                       |                                                    |

