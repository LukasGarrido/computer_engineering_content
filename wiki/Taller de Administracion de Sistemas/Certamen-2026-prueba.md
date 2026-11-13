
**Problemas por resolver:**

Cada servicio tiene un problema específico que se describe a continuación. La solución correcta de cada problema otorga puntos en función de la complejidad de la tarea.

1. **Hostname con su nombre**
2. **DNS** (35 puntos):
3. **MySQL** (10 puntos):
4. **WordPress** (15 puntos):
5. **Apache** (40 puntos): Debe desplegar sobre el puerto 80

---

## Hostname

### Objetivo

Cambiar el nombre del equipo (hostname) de `tas-c2-2025` a `lukas`.

### 1.1 Verificar el hostname actual

**Comando:**

```bash
hostnamectl
```

**Salida:**


```text
 Static hostname: tas-c2-2025
       Icon name: computer-vm
         Chassis: vm
      Machine ID: 268d393b39794bdab8afb3d6202feed8
         Boot ID: 0e6964e355df42a69fe09368e5bae3ae
  Virtualization: kvm
Operating System: Ubuntu 22.04.5 LTS
          Kernel: Linux 5.15.0-202-generic
    Architecture: x86-64
 Hardware Vendor: QEMU
  Hardware Model: Standard PC _i440FX + PIIX, 1996_
```

### 1.2 Cambiar el hostname

**Comando:**

```bash
sudo hostnamectl set-hostname lukas
```

**Salida:**

```text
(sin salida, el comando se ejecutó correctamente)
```

### 1.3 Verificar el cambio

**Comando:**

```bash
hostnamectl
```

**Salida:**

```text
 Static hostname: lukas
       Icon name: computer-vm
         Chassis: vm
      Machine ID: 268d393b39794bdab8afb3d6202feed8
         Boot ID: 0e6964e355df42a69fe09368e5bae3ae
  Virtualization: kvm
Operating System: Ubuntu 22.04.5 LTS
          Kernel: Linux 5.15.0-202-generic
    Architecture: x86-64
 Hardware Vendor: QEMU
  Hardware Model: Standard PC _i440FX + PIIX, 1996_
```

---

## DNS

# Resumen de comandos: Reparación del servicio DNS (BIND9)

## 1. Verificar la red del equipo

**Comando:**
```bash
ip a
```

**Salida (relevante):**
```text
2: ens18: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether bc:24:11:db:59:f3 brd ff:ff:ff:ff:ff:ff
    inet 10.33.195.179/25 metric 100 brd 10.33.195.255 scope global dynamic ens18
```

## 2. Revisar el estado del servicio

**Comando:**
```bash
sudo systemctl status named
```

**Salida:**
```text
● named.service - BIND Domain Name Server
     Loaded: loaded (/lib/systemd/system/named.service; dis>
     Active: active (running) since Thu 2026-11-12 15:58:32>
       Docs: man:named(8)
   Main PID: 1261 (named)
      Tasks: 8 (limit: 4553)
     Memory: 27.4M
             └─1261 /usr/sbin/named -u bind
```

## 3. Verificar puertos en escucha

**Comando:**
```bash
sudo ss -tulpn | grep named
```

**Salida (resumida):**
```text
udp   UNCONN 0   0   10.33.195.179:53   0.0.0.0:*   users:(("named",pid=1261,fd=32))
udp   UNCONN 0   0       127.0.0.1:53   0.0.0.0:*   users:(("named",pid=1261,fd=25))
tcp   LISTEN 0   10  10.33.195.179:53   0.0.0.0:*   users:(("named",pid=1261,fd=33))
tcp   LISTEN 0   10      127.0.0.1:53   0.0.0.0:*   users:(("named",pid=1261,fd=27))
tcp   LISTEN 0   5       127.0.0.1:953  0.0.0.0:*   users:(("named",pid=1261,fd=43))
```

## 4. Validar la sintaxis de la configuración

**Comando:**
```bash
sudo named-checkconf
```

**Salida:**
```text
(sin salida: la sintaxis es correcta)
```

## 5. Revisar los archivos de configuración

**Comandos:**
```bash
cd /etc/bind
ls
cat named.conf.local
cat named.conf.options
```

**Salida de `ls`:**
```text
bind.keys  db.local                  rndc.key
db.0       named.conf                zones
db.127     named.conf.default-zones  zones.rfc1918
db.255     named.conf.local
db.empty   named.conf.options
```

**Salida de `cat named.conf.local` (ANTES de corregir):**
```text
zone "tas2025.local" {
    type master;
    file "/etc/bind/zones/db.tas2026-.local"; # zone file path
};
```

**Salida de `cat named.conf.options`:**
```text
options {
        directory "/var/cache/bind";

        recursion yes;
        allow-recursion { any; };
        listen-on { any; };
        allow-transfer { none; };

        forwarders {
          10.33.192.131;
          8.8.8.8;
        };

        dnssec-validation auto;

        listen-on-v6 { any; };
};
```

## 6. Revisar la carpeta de zonas

**Comando:**
```bash
ls -l /etc/bind/zones/
```

**Salida:**
```text
total 4
-rw-r--r-- 1 root bind 378 Nov  6 19:21 db.tas2026.local
```

## 7. Revisar el archivo de zona (ANTES de corregir)

**Comando:**
```bash
cat /etc/bind/zones/db.tas2026.local
```

**Salida:**
```text
;
; BIND data file for local loopback interface
;
$TTL    604800
@       IN      SOA     tas2026.local. admin.tas2026.local. (
                              4         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;

; name servers - NS records
    IN      NS      ns1.tas2026.local.

ns1.tas2026.local.          IN      A       10.33.195.196
@       IN      A       10.33.195.196
```

## 8. Corregir el archivo de zona (IP y serial)

**Comando:**
```bash
sudo vim /etc/bind/zones/db.tas2026.local
```

**Cambios realizados:**
- Registros A: `10.33.195.196` → `10.33.195.179`
- Serial: `4` → `5`

**Verificación:**
```bash
cat /etc/bind/zones/db.tas2026.local
```

**Salida:**
```text
;
; BIND data file for local loopback interface
;
$TTL    604800
@       IN      SOA     tas2026.local. admin.tas2026.local. (
                              5         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;

; name servers - NS records
    IN      NS      ns1.tas2026.local.

ns1.tas2026.local.          IN      A       10.33.195.179
@       IN      A       10.33.195.179
```

## 9. Validar la zona, reiniciar y habilitar el servicio

**Comandos:**
```bash
sudo named-checkconf
sudo named-checkzone tas2026.local /etc/bind/zones/db.tas2026.local
sudo systemctl restart named
sudo systemctl enable named
```

**Salida:**
```text
zone tas2026.local/IN: loaded serial 5
OK
Synchronizing state of named.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable named
Created symlink /etc/systemd/system/bind9.service → /lib/systemd/system/named.service.
Created symlink /etc/systemd/system/multi-user.target.wants/named.service → /lib/systemd/system/named.service.
```

## 10. Primera prueba de resolución (FALLÓ)

**Comandos:**
```bash
dig @127.0.0.1 tas2026.local
dig @127.0.0.1 ns1.tas2026.local
```

**Salida (resumida):**
```text
;; WARNING: .local is reserved for Multicast DNS
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1
;; AUTHORITY SECTION:
.    10800   IN   SOA   a.root-servers.net. nstld.verisign-grs.com. 2026111200 1800 900 604800 86400
```

**Diagnóstico:** `NXDOMAIN` sin flag `aa`. En `named.conf.local` la zona seguía como `tas2025.local`, por lo que BIND no servía `tas2026.local`.

## 11. Corregir el nombre de zona en named.conf.local

**Comando:**
```bash
sudo vim /etc/bind/named.conf.local
```

**Cambio realizado:** `zone "tas2025.local"` → `zone "tas2026.local"`

**Verificación:**
```bash
cat /etc/bind/named.conf.local
```

**Salida:**
```text
zone "tas2026.local" {
    type master;
    file "/etc/bind/zones/db.tas2026.local"; # zone file path
};
```

## 12. Validar, reiniciar y probar (OK)

**Comandos:**
```bash
sudo named-checkconf
sudo systemctl restart named
dig @127.0.0.1 tas2026.local +short
dig @127.0.0.1 ns1.tas2026.local
```

**Salida:**
```text
10.33.195.179

;; WARNING: .local is reserved for Multicast DNS
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 53173
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;ns1.tas2026.local.             IN      A

;; ANSWER SECTION:
ns1.tas2026.local.      604800  IN      A       10.33.195.179

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
```

## 13. Verificación final contra la IP real y estado del servicio

**Comandos:**
```bash
dig @10.33.195.179 tas2026.local +short
dig @10.33.195.179 ns1.tas2026.local +short
systemctl is-enabled named
systemctl is-active named
```

**Salida:**
```text
10.33.195.179
10.33.195.179
enabled
active
```
