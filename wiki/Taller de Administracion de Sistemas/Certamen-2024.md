**Problemas por resolver:**

1. **DNS** 
2. **MySQL** 
3. **WordPress**
4. **Apache** 

---

## DNS

**Diagnostico** 

Los registros A de la zona `tas2025.local` apuntaban a **`10.33.195.208`**, pero la IP real de la VM es **`10.33.195.239`**. Por eso los nombres `tas2025.local`, `www` y `ns1` resolvían a una IP incorrecta.

Problemas secundarios:
- El servicio `named` estaba **detenido** (`inactive (dead)`) y **deshabilitado** en el arranque.

---

### 1. Diagnóstico de red


```bash
ip route
```

```
default via 10.33.195.129 dev ens18 proto dhcp src 10.33.195.239 metric 100
10.33.192.131 via 10.33.195.129 dev ens18 proto dhcp src 10.33.195.239 metric 100
10.33.195.128/25 dev ens18 proto kernel scope link src 10.33.195.239 metric 100
10.33.195.129 dev ens18 proto dhcp scope link src 10.33.195.239 metric 100
```


```bash
ip a
```

```
2: ens18: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
    inet 10.33.195.239/25 metric 100 brd 10.33.195.255 scope global dynamic ens18
```

---

### 2. Estado del servicio


```bash
sudo systemctl status named
```

```
○ named.service - BIND Domain Name Server
     Active: inactive (dead)
```


```bash
sudo systemctl start named
sudo systemctl status named
```

```
● named.service - BIND Domain Name Server
     Active: active (running) since Wed 2026-11-11 18:12:04
   Main PID: 1243 (named)
```

---

### 3. Verificación de puertos

```bash
sudo ss -tulpn | grep named
```

```
udp   UNCONN 0  0   10.33.195.239:53   0.0.0.0:*   users:(("named",pid=1243,fd=31))
udp   UNCONN 0  0       127.0.0.1:53   0.0.0.0:*   users:(("named",pid=1243,fd=25))
tcp   LISTEN 0  10  10.33.195.239:53   0.0.0.0:*   users:(("named",pid=1243,fd=33))
tcp   LISTEN 0  10      127.0.0.1:53   0.0.0.0:*   users:(("named",pid=1243,fd=27))
... (también en [::1] y puerto 953 para rndc)
```

BIND escucha en el puerto 53 (TCP/UDP) en `127.0.0.1` y `10.33.195.239`.

---

### 4. Revisión de la configuración

```bash
sudo named-checkconf
```

```
(sin salida = sin errores)
```

```bash
cat /etc/bind/named.conf.local
```

```
zone "tas2025.local" {
    type master;
    file "/etc/bind/zones/db.tas2025.local"; # zone file path
};
```

```bash
cat /etc/bind/named.conf.options
```

```
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

---

### 5. Archivo de zona con el error

```bash
sudo named-checkzone tas2025.local /etc/bind/zones/db.tas2025.local
```

```
zone tas2025.local/IN: loaded serial 4
OK
```

> La sintaxis era válida, pero los datos eran incorrectos.

```bash
cat /etc/bind/zones/db.tas2025.local
```

```
$TTL    604800
@       IN      SOA     tas2025.local. admin.tas2025.local. (
                              4         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
    IN      NS      ns1.tas2025.local.

ns1.tas2025.local.          IN      A       10.33.195.208   <-- IP incorrecta
@       IN      A       10.33.195.208                       <-- IP incorrecta
www     IN      A       10.33.195.208                       <-- IP incorrecta
```

---

### 6. Corrección

```bash
sudo vim /etc/bind/zones/db.tas2025.local
```

Cambios realizados:

- Serial: `4` → `5`
- Todas las IPs: `10.33.195.208` → `10.33.195.239`

```
$TTL    604800
@       IN      SOA     tas2025.local. admin.tas2025.local. (
                              5         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
    IN      NS      ns1.tas2025.local.

ns1.tas2025.local.          IN      A       10.33.195.239
@       IN      A       10.33.195.239
www     IN      A       10.33.195.239
```

---

### 7. Aplicar y verificar

```bash
sudo named-checkzone tas2025.local /etc/bind/zones/db.tas2025.local
```

```
zone tas2025.local/IN: loaded serial 5
OK
```

```bash
sudo rndc reload
```

```
server reload successful
```

```bash
dig @127.0.0.1 tas2025.local +short
dig @127.0.0.1 www.tas2025.local +short
dig @127.0.0.1 ns1.tas2025.local +short
```

```
10.33.195.239
10.33.195.239
10.33.195.239
```

---
### Problema 2 dns

La VM no resolvía `www.tas2025.local`. `/etc/netplan/00-tas2025-nameserver.yaml` tenía como servidor DNS **`10.33.195.208`** (IP incorrecta), por lo que systemd-resolved no consultaba al BIND local (`10.33.195.239`). La consulta caía en `10.33.192.131`, que no conoce la zona `tas2025.local`.

---

### 1. Síntoma


```bash
curl -I http://www.tas2025.local
```

```
curl: (6) Could not resolve host: www.tas2025.local
```

### 2. Comprobar que BIND sí funciona


```bash
dig @127.0.0.1 www.tas2025.local +short
```

```
10.33.195.239
```

### 3. Ver qué DNS usa la VM


```bash
resolvectl status | head -20
```

```
Current DNS Server: 10.33.192.131
DNS Servers: 10.33.195.208 10.33.192.131      <-- IP equivocada
DNS Domain: cs.ilab.cl cs.ilab.usm.cl tas2025.local
```

### 4. Localizar el origen del error


```bash
ls /etc/netplan
cat /etc/netplan/00-tas2025-nameserver.yaml
```

yaml

```yaml
network:
    version: 2
    ethernets:
        ens18:
            nameservers:
                addresses:
                - 10.33.195.208            <-- IP incorrecta
                search: [ tas2025.local, cs.ilab.cl ]
```

### 5. Corrección

```bash
sudo vim /etc/netplan/00-tas2025-nameserver.yaml
```

Cambio: `10.33.195.208` → `10.33.195.239`

yaml

```yaml
                addresses:
                - 10.33.195.239
```

### 6. Aplicar

```bash
sudo netplan apply
resolvectl status | head -20
```

```
Link 2 (ens18)
   DNS Servers: 10.33.195.239
    DNS Domain: cs.ilab.cl tas2025.local
```

### 7. Verificación


```bash
dig @10.33.195.239 www.tas2025.local +short
resolvectl query www.tas2025.local
```

```
10.33.195.239
www.tas2025.local: 10.33.195.239   -- link: ens18
-- Data from: network
```
### 8. Habilitar named

```bash
sudo systemctl enable named
```

```
Synchronizing state of named.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable named
Created symlink /etc/systemd/system/bind9.service → /lib/systemd/system/named.service.
Created symlink /etc/systemd/system/multi-user.target.wants/named.service → /lib/systemd/system/named.service.
```

---

## MySQL

### Problemas encontrados

1. **MariaDB estaba detenido y deshabilitado** en el arranque.
2. **`wp-config.php` apuntaba a la base equivocada**: `DB_NAME` era `wp_db` (vacía), cuando la base con las tablas de WordPress es `wordpress_db`.
3. **Permisos incorrectos en `/sitios/wp-tas2025`**: los directorios tenían `drw-r--r--` (sin bit de ejecución), por lo que nadie podía entrar, ni siquiera Apache. El propietario era `tas` y no `www-data`.

la contraseña de `wp_user` la establecí yo (`tas2025`) con `ALTER USER`, coincide con la que ya figuraba en `wp-config.php`.

---

### 1. Iniciar MariaDB

```bash
sudo systemctl start mysql
sudo systemctl status mysql
```

```
● mariadb.service - MariaDB 10.6.22 database server
     Active: active (running) since Wed 2026-11-11 18:30:01
     Status: "Taking your SQL requests now..."
```

```bash
sudo ss -tulpn | grep -E 'mysql|3306'
```

```
tcp   LISTEN 0   80   127.0.0.1:3306   0.0.0.0:*   users:(("mariadbd",pid=1565,fd=22))
```

---

### 2. Diagnóstico de bases de datos y usuarios


```bash
sudo mysql -e "SHOW DATABASES;"
```

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| wordpress_db       |
| wp_db              |
+--------------------+
```


```bash
sudo mysql -e "SELECT user,host FROM mysql.user;"
```

```
+-------------+-----------+
| User        | Host      |
+-------------+-----------+
| wp_user     | %         |
| mariadb.sys | localhost |
| mysql       | localhost |
| root        | localhost |
+-------------+-----------+
```


```bash
sudo mysql -e "SHOW GRANTS FOR 'wp_user'@'%';"
```

```
GRANT USAGE ON *.* TO `wp_user`@`%` IDENTIFIED BY PASSWORD '*118E11B5...'
GRANT ALL PRIVILEGES ON `wp_db`.* TO `wp_user`@`%`
GRANT ALL PRIVILEGES ON `wordpress_db`.* TO `wp_user`@`%`
```


```bash
sudo mysql -e "SHOW TABLES FROM wordpress_db;"
sudo mysql -e "SHOW TABLES FROM wp_db;"
```

```
wordpress_db -> 12 tablas (wp_commentmeta, wp_comments, wp_links, wp_options,
                wp_postmeta, wp_posts, wp_term_relationships, wp_term_taxonomy,
                wp_termmeta, wp_terms, wp_usermeta, wp_users)
wp_db        -> vacía (sin tablas)
```

---

### 3. Contraseña de `wp_user`

```bash
sudo mysql -e "ALTER USER 'wp_user'@'%' IDENTIFIED BY 'tas2025'; FLUSH PRIVILEGES;"
```

```
(sin salida = éxito)
```

---

### 4. Localizar WordPress

```bash
sudo find / -xdev -type d -name "wp-content" 2>/dev/null
```

```
/sitios/wp-tas2025/wp-content
```

WordPress está en **`/sitios/wp-tas2025/`**, fuera de `/var/www`.

---

### 5. Permisos con error

```bash
ls -ld /sitios /sitios/wp-tas2025
```

```
drwxr-xr-x 3 root root     4096 Nov 12  2025 /sitios
drw-r--r-- 5 tas  www-data 4096 Nov 13  2025 /sitios/wp-tas2025      <-- sin bit "x"
```

```bash
sudo grep -E "DB_NAME|DB_USER|DB_PASSWORD|DB_HOST|table_prefix" /sitios/wp-tas2025/wp-config.php
```

```
define( 'DB_NAME', 'wp_db' );        <-- base equivocada
define( 'DB_USER', 'wp_user' );
define( 'DB_PASSWORD', 'tas2025' );
define( 'DB_HOST', 'localhost' );
$table_prefix = 'wp_';
```

---

### 6. Corrección de propietario y permisos

```bash
sudo chown -R www-data:www-data /sitios/wp-tas2025
sudo chmod 755 /sitios /sitios/wp-tas2025
sudo find /sitios/wp-tas2025 -type d -exec chmod 755 {} \;
sudo find /sitios/wp-tas2025 -type f -exec chmod 644 {} \;
```

```bash
ls -ld /sitios/wp-tas2025/wp-*
```

```
drwxr-xr-x  9 www-data www-data  4096 Nov 12  2025 /sitios/wp-tas2025/wp-admin
-rw-r--r--  1 www-data www-data  3476 Nov 11 19:12 /sitios/wp-tas2025/wp-config.php
drwxr-xr-x  6 www-data www-data  4096 Nov 12  2025 /sitios/wp-tas2025/wp-content
drwxr-xr-x 30 www-data www-data 16384 Nov 12  2025 /sitios/wp-tas2025/wp-includes
... (archivos .php con 644)
```

---

### 7. Corrección de `wp-config.php`

```bash
sudo vim /sitios/wp-tas2025/wp-config.php
```

Cambio: `DB_NAME` de `wp_db` a `wordpress_db`.

php

```php
define( 'DB_NAME', 'wordpress_db' );
define( 'DB_USER', 'wp_user' );
define( 'DB_PASSWORD', 'tas2025' );
define( 'DB_HOST', 'localhost' );
$table_prefix = 'wp_';
```

---

### 8. Verificación

```bash
php -l /sitios/wp-tas2025/wp-config.php
```

```
No syntax errors detected in /sitios/wp-tas2025/wp-config.php
```

```bash
mysql -u wp_user -ptas2025 -h 127.0.0.1 wordpress_db -e "SHOW TABLES;"
```

```
+------------------------+
| Tables_in_wordpress_db |
+------------------------+
| wp_commentmeta         |
| wp_comments            |
| wp_links               |
| wp_options             |
| wp_postmeta            |
| wp_posts               |
| wp_term_relationships  |
| wp_term_taxonomy       |
| wp_termmeta            |
| wp_terms               |
| wp_usermeta            |
| wp_users               |
+------------------------+
```

```bash
sudo mysql wordpress_db -e "SELECT option_name, option_value FROM wp_options WHERE option_name IN ('siteurl','home');"
```

```
+-------------+--------------------------+
| option_name | option_value             |
+-------------+--------------------------+
| home        | http://www.tas2025.local |
| siteurl     | http://www.tas2025.local |
+-------------+--------------------------+
```

---

### 9. Habilitar MariaDB en el arranque

```bash
sudo systemctl enable mariadb
```

```
Synchronizing state of mariadb.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable mariadb
Created symlink /etc/systemd/system/multi-user.target.wants/mariadb.service → /lib/systemd/system/mariadb.service.
```

---

## Wordpress

### Problemas

1. **Nginx ocupaba el puerto 80** y servía la página por defecto de `/var/www/html`, por lo que Apache no podía arrancar y WordPress no se veía.
2. **Apache estaba detenido y deshabilitado** en el arranque.
3. **WordPress estaba fuera de `/var/www`** (en `/sitios/wp-tas2025`) con permisos y base de datos incorrectos (ver resumen de MySQL).

Lo que ya estaba bien: el VirtualHost `wp-tas2025.conf` estaba habilitado, con `DocumentRoot /sitios/wp-tas2025`, y `apache2ctl configtest` daba `Syntax OK`.

---

### 1. Estado inicial de Apache

```bash
systemctl status apache2 --no-pager
```

```
○ apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; disabled; vendor preset: enabled)
     Active: inactive (dead)
```


```bash
sudo apache2ctl configtest
```

```
AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to suppress this message
Syntax OK
```

---

### 2. Detectar quién respondía en el puerto 80



```bash
curl -I http://localhost
```

```
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Content-Length: 10671
```


```bash
sudo ss -tulpn | grep ':80'
```

```
tcp   LISTEN 0   511   0.0.0.0:80   0.0.0.0:*   users:(("nginx",pid=771,fd=6),("nginx",pid=770,fd=6),("nginx",pid=769,fd=6))
tcp   LISTEN 0   511      [::]:80      [::]:*   users:(("nginx",pid=771,fd=7),("nginx",pid=770,fd=7),("nginx",pid=769,fd=7))
```

---

### 3. Revisar los sitios de Apache


```bash
ls -l /etc/apache2/sites-enabled/ /etc/apache2/sites-available/
```

```
/etc/apache2/sites-available/:
-rw-r--r-- 1 root root 1332 Mar 18  2024 000-default.conf
-rw-r--r-- 1 root root 6338 Mar 18  2024 default-ssl.conf
-rw-r--r-- 1 root root  393 Nov 12  2025 wp-tas2025.conf

/etc/apache2/sites-enabled/:
lrwxrwxrwx 1 root root 34 Nov 12  2025 wp-tas2025.conf -> ../sites-available/wp-tas2025.conf
```


```bash
grep -rn "DocumentRoot" /etc/apache2/sites-available/
```

```
000-default.conf:12:       DocumentRoot /var/www/html
wp-tas2025.conf:5:        DocumentRoot /sitios/wp-tas2025
default-ssl.conf:5:           DocumentRoot /var/www/html
```

---

### 4. Corrección: liberar el puerto 80 y arrancar Apache

```bash
sudo systemctl stop nginx
sudo systemctl disable nginx
sudo systemctl start apache2
sudo systemctl enable apache2
```

```
Removed /etc/systemd/system/multi-user.target.wants/nginx.service.
Created symlink /etc/systemd/system/multi-user.target.wants/apache2.service → /lib/systemd/system/apache2.service.
```

---

### 5. Verificación


```bash
systemctl status apache2 --no-pager
```

```
● apache2.service - The Apache HTTP Server
     Loaded: loaded (...; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2026-11-11 19:27:25 UTC
```

```bash
curl -I http://localhost
```

```
HTTP/1.1 200 OK
Server: Apache/2.4.52 (Ubuntu)
Link: <http://www.tas2025.local/index.php?rest_route=/>; rel="https://api.w.org/"
Link: <http://www.tas2025.local/>; rel=shortlink
Content-Type: text/html; charset=UTF-8
```

Las cabeceras `Link` son generadas por WordPress, así que el sitio carga y conecta con la base de datos.

---

## Corrección de módulos PHP 

### Problema

WordPress reportaba **PHP 8.1.2-1ubuntu2.22 funcional**, pero con los módulos **cURL, Multibyte String, XML, GD (Imágenes) y ZIP** sin instalar. Sin ellos, WordPress no puede hacer peticiones HTTP, procesar texto multibyte, manejar XML, redimensionar imágenes ni descomprimir paquetes (plugins, temas, actualizaciones).

---

### 1. Instalar los módulos


```bash
sudo apt update
sudo apt install -y php-curl php-mbstring php-xml php-gd php-zip
```

### 2. Reiniciar Apache para cargarlos


```bash
sudo systemctl restart apache2
```

### 3. Verificar que PHP los carga


```bash
php -m | grep -E "curl|mbstring|xml|gd|zip"
```

```
curl
gd
libxml
mbstring
xml
xmlreader
xmlwriter
zip
```

### 4. Verificar Apache y el sitio por nombre DNS


```bash
systemctl status apache2 --no-pager
curl -I http://www.tas2025.local
```

```
Active: active (running) since Wed 2026-11-11 19:39:23 UTC; 20s ago
```

```
HTTP/1.1 200 OK
Server: Apache/2.4.52 (Ubuntu)
Link: <http://www.tas2025.local/index.php?rest_route=/>; rel="https://api.w.org/"
Link: <http://www.tas2025.local/>; rel=shortlink
Content-Type: text/html; charset=UTF-8
```
