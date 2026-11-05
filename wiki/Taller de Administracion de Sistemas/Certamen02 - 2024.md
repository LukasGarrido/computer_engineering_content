
## DNS

**1. Diagnóstico**

bash

```bash
sudo systemctl status named
sudo journalctl -u named -xe --no-pager | tail -50
sudo cat /etc/bind/named.conf.local
sudo cat /etc/bind/named.conf.options
sudo cat /etc/bind/zones/db.tas2025.local
ip -4 addr show ens18 | grep inet
sudo ss -tulpn
sudo grep -A3 nameservers /etc/netplan/*.yaml
```

**2. Corregir la zona `tas2025.local`**

bash

```bash
sudo vim /etc/bind/zones/db.tas2025.local
```

Contenido final:

```
;
; BIND data file for local loopback interface
;
$TTL    604800
@       IN      SOA     ns1.tas2025.local. admin.tas2025.local. (
                              6         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;

; name servers - NS records
@       IN      NS      ns1.tas2025.local.

ns1         IN      A       10.33.195.252
@           IN      A       10.33.195.252
www         IN      A       10.33.195.252
wordpress   IN      A       10.33.195.252
```

Cambios respecto al original: se eliminó el bloque `zone "certamen2.tas"` que estaba dentro del archivo, se corrigió la IP de `.208` a `.252`, se apuntó el SOA a `ns1.tas2025.local.` y se agregó el registro `wordpress`.

**3. Validar y aplicar bind**

bash

```bash
sudo named-checkconf -z
sudo systemctl restart named
```

**4. Corregir el DNS del sistema (netplan)**

bash

```bash
sudo vim /etc/netplan/00-tas2025-nameserver.yaml
```

Se cambió `- 10.33.195.208` por `- 127.0.0.1`. Luego:

bash

```bash
sudo chmod 600 /etc/netplan/*.yaml
sudo netplan apply
```

**5. Usar el bind local en la VM**

bash

```bash
sudo systemctl disable --now systemd-resolved
sudo rm /etc/resolv.conf
printf 'nameserver 127.0.0.1\nsearch tas2025.local\n' | sudo tee /etc/resolv.conf
```

**6. Pruebas en la VM**

bash

```bash
dig ns1.tas2025.local +short
dig @ns1.tas2025.local tas2025.local NS +short
dig wordpress.tas2025.local +short
ping -c 2 wordpress.tas2025.local
```

**7. Prueba desde Windows**

Configuración del DNS del adaptador Wi-Fi (`ncpa.cpl`, Propiedades, IPv4) con preferido `10.33.195.252` y alternativo `8.8.8.8`. Luego:

powershell

```powershell
nslookup wordpress.tas2025.local
```

**Cosas que probamos y no fueron necesarias**

- La zona `certamen2.tas` (bloque en `named.conf.local` y archivo `db.certamen2.tas`). Puedes quitarlos para dejar todo limpio.
- Los comandos `resolvectl`, que no lograron que resolved usara el bind.
- Agregar la IP `.208` con `ip addr add`, que era temporal y ya no está.

Si quieres limpiar la zona sobrante:

bash

```bash
sudo vim /etc/bind/named.conf.local
sudo rm /etc/bind/zones/db.certamen2.tas
sudo named-checkconf -z
sudo systemctl restart named
```

---

## MySQL (10 pts)

bash

```bash
sudo mysql -e "ALTER USER 'wp_user'@'%' IDENTIFIED BY 'tas2025'; FLUSH PRIVILEGES;"
```

**Por qué:** `wp_user` recibía `Access denied` al conectarse. Se restableció su contraseña para que coincida con la que usa `wp-config.php` (`tas2025`), y desde entonces entra sin error.

Nota: yo había puesto `password` (la del enunciado) antes de ver el `wp-config.php`, y después la dejé en `tas2025`. No sabemos con certeza cuál era la original. Lo comprobado es que antes no entraba y ahora sí, con la misma contraseña que usa WordPress.

### WordPress (15 pts)

bash

```bash
sudo vim /sitios/wp-tas2025/wp-config.php
```

Cambio: `define( 'DB_NAME', 'wp_db' );` → `define( 'DB_NAME', 'wordpress_db' );`

**Por qué:** WordPress apuntaba a `wp_db`, que está vacía. Las 12 tablas (`wp_posts`, `wp_options`, etc.) están en `wordpress_db`.

### Apache (40 pts)

bash

```bash
sudo systemctl disable --now nginx
sudo systemctl enable --now apache2
sudo chmod 755 /sitios/wp-tas2025
sudo find /sitios/wp-tas2025 -type d -exec chmod 755 {} \;
```

**Por qué:**

- **Nginx deshabilitado:** ocupaba el puerto 80 con su página por defecto, y WordPress no se servía.
- **Apache habilitado:** ya tenía el VirtualHost de `www.tas2025.local` apuntando a `/sitios/wp-tas2025`, pero estaba deshabilitado.
- **`chmod 755` en la raíz del sitio:** el directorio no tenía el bit de ejecución, así que `www-data` no podía entrar (error `403`).
- **`chmod 755` en los subdirectorios:** `wp-includes` y otros tenían el mismo problema, y daban error `500`.