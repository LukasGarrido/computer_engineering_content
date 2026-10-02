# Taller de Administración de Sistemas — Índice de Asignatura (MOC)

Este índice centraliza los Objetos Virtuales de Aprendizaje (OVA), guías de contenidos teóricos y bitácoras prácticas de configuración de servidores Linux para la asignatura de **Taller de Administración de Sistemas** (USM - EIN-090B).

---

## 01. Teoría y Unidades de Aprendizaje (OVA)

### Objetos Virtuales de Aprendizaje (OVA)
- [OVA 01 — Máquinas Virtuales, Hipervisores y Contenedores](./OVA_01_Maquinas_Virtuales_y_Contenedores.md)
  - *Diferencias fundamentales entre VM y Contenedores, hipervisores Tipo 1 vs Tipo 2, namespaces, cgroups, imágenes inmutables y arquitecturas de despliegue híbridas.*
- [OVA 02 — Datos, Control de Acceso y Servicios Fundamentales de Red](./OVA_02_Datos_Acceso_y_Servicios_Red.md)
  - *Montaje persistente por UUID (`/etc/fstab`), permisos avanzados (setgid, sticky bit, ACL), cortafuegos UFW, asignación DHCP con Kea y resolución DNS con BIND 9.*

### Guía Global de Contenidos Teóricos y Prácticos
- [Guía Completa de Contenidos (Programa EIN-090B)](./01_Teoria/taller_administracion_sistemas_contenidos.md)
  - **1. Distribuciones e Instalación:** Familias Linux (Debian, RHEL, Arch, Alpine), particionamiento (GPT/MBR), LVM e instalación automatizada (`cloud-init`).
  - **2. Administración Remota:** Configuración segura de SSH, llaves criptográficas, redirección de puertos (SSH Tunneling) y multiplexores (`tmux`, `screen`).
  - **3. Redes y Cortafuegos:** Configuración de red con `netplan` e `iproute2`, tablas de rutas y filtrado de paquetes con `ufw`, `iptables` y `nftables`.
  - **4. Gestión de Servicios:** Arquitectura de `systemd`, administración con `systemctl`, inspección de logs con `journalctl` y servidores web (Nginx, Apache).
  - **5. Sistemas de Archivos y Almacenamiento:** Formateo (ext4, xfs), volúmenes lógicos con LVM, permisos POSIX, bit setgid, sticky bit y ACLs (`getfacl`/`setfacl`).
  - **6. Seguridad y Paquetes:** Gestión de repositorios (`apt`, `dnf`), compilación desde fuente, directivas de `sudoers` y auditoría del sistema.
  - **7. Virtualización y Contenedores:** Hipervisores (KVM/VirtualBox), motor Docker, `docker-compose`, redes bridge/host y gestión de volúmenes persistentes.

---

## 02. Configuraciones y Laboratorios Prácticos

### Laboratorios de Operaciones en Servidor (VM)
- [Lab 1/4 — Almacenamiento, Sistemas de Archivos y Permisos](./02_Laboratorios/lab-almacenamiento-permisos.md)
  - *Operación 1 de 4 · 105 min · Módulo RDA2*
    - Creación de volumen persistente con identificación por **UUID** (`/etc/fstab`).
    - Formateo ext4, montaje en `/srv/proyecto` y política grupal automática.
    - Permisos POSIX avanzados: **setgid**, sticky bit y ACLs (`setfacl`/`getfacl`).
    - Justificación de mínimo privilegio para colaboración entre operadores.
- [Lab 2/4 — Diagnóstico de Red y Firewall Inicial](./02_Laboratorios/lab-diagnostico-red-firewall.md)
  - *Operación 2 de 4 · 105 min · Módulo RDA1/RDA3*
    - Distinción práctica entre proceso, socket, puerto, servicio y firewall como capas independientes.
    - Habilitación selectiva del puerto 8080 solo desde la red de laboratorio.
    - Configuración de política UFW por defecto (deny incoming) preservando acceso SSH.
    - Diagnóstico con `ss -tulpn`, `systemctl`, `journalctl` y `nc`.
- [Lab 4/4 — DNS Autoritativo Local con BIND 9](./02_Laboratorios/lab-dns-bind9.md)
  - *Operación 4 de 4 · 105 min · Módulo RDA1/RDA2/RDA3*
    - Publicación de zona directa e inversa para `pruebatas.test`.
    - Configuración de BIND 9: `named.conf.local`, archivos de zona, registros SOA/NS/A/PTR.
    - Restricción de consultas a la red de laboratorio (`allow-query`).
    - Validación del servicio con `dig` (directa e inversa) y análisis de logs.

---

## Herramientas y Comandos Clave por Dominio

| Dominio                  | Comandos Esenciales                                                                 |        |                       |                                                    |
| :----------------------- | :---------------------------------------------------------------------------------- | ------ | --------------------- | -------------------------------------------------- |
| **Redes y Diagnóstico**  | `ip a`, `ip route`, `netplan apply`, `ss -tulpn`, `ping`, `dig`, `traceroute`, `nc` |        |                       |                                                    |
| **Servicios y Procesos** | `systemctl status                                                                   | start  | stop                  | enable`, `journalctl -u`, `htop`, `ps aux`, `tmux` |
| **Almacenamiento y LVM** | `lsblk`, `fdisk`, `blkid`, `pvcreate`, `vgcreate`, `lvcreate`, `mount`, `df -h`     |        |                       |                                                    |
| **Permisos y Seguridad** | `chmod`, `chown`, `setfacl`, `getfacl`, `ufw status                                 | enable | allow`, `sudo visudo` |                                                    |
| **Contenedores**         | `docker run`, `docker-compose up -d`, `docker ps`, `docker logs`, `docker exec`     |        |                       |                                                    |



## Secciones del Directorio

- [01_Teoria](./01_Teoria)
- [02_Laboratorios](./02_Laboratorios)
- [03_certamen](./03_certamen)
