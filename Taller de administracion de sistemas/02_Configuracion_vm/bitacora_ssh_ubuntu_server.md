# Bitácora: Configuración de SSH en Ubuntu Server 24.04

Registro de los pasos, comandos y problemas resueltos al configurar acceso SSH
a una VM de Ubuntu Server 24.04 corriendo en VirtualBox, desde un host Windows.

---

## 1. Verificar que el servicio SSH está instalado y activo

Ubuntu Server 24.04 suele instalar `openssh-server` desde el instalador, pero se
confirma igual:

```bash
sudo systemctl status ssh
```

Si no estuviera instalado, el comando habría sido:

```bash
sudo apt update && sudo apt install openssh-server -y
sudo systemctl enable --now ssh
```

**Resultado esperado:** `active (running)` y las líneas `Server listening on 0.0.0.0 port 22`
y `Server listening on :: port 22` en los logs.

---

## 2. Primer intento de conexión — falló

Desde Windows (PowerShell), con la IP que la VM mostraba en ese momento:

```powershell
ssh lukas@10.0.2.15/24
ssh lukas@10.0.2.15
ssh -p 2222 lukas@localhost
ssh -p 2222 lukas@10.0.2.15
```

### Problema 1 — `10.0.2.15/24` inválido
```
ssh: Could not resolve hostname 10.0.2.15/24: Host desconocido.
```
**Causa:** se incluyó la máscara de red (`/24`) como parte del hostname. SSH no
acepta notación CIDR en el destino, solo la IP.

**Solución:** usar solo la IP, sin la máscara → `ssh lukas@10.0.2.15`.

### Problema 2 — `Connection timed out`
```
ssh: connect to host 10.0.2.15 port 22: Connection timed out
```
**Causa raíz:** la VM tenía el adaptador de red en modo **NAT**, el modo por
defecto de VirtualBox. En NAT, la VM vive en una red interna aislada
(`10.0.2.0/24`) que **no es alcanzable directamente desde el host Windows** —
solo la VM puede salir hacia afuera, no al revés.

### Problema 3 — `Connection refused` en `localhost:2222`
```
ssh: connect to host localhost port 2222: Connection refused
```
**Causa:** `localhost` apunta a la propia máquina Windows, no a la VM. No había
ningún servicio SSH corriendo en Windows, por lo tanto la conexión fue rechazada
de inmediato (a diferencia del timeout, que indica que el paquete ni siquiera
llegó a un destino que responda).

---

## 3. Diagnóstico: identificar el adaptador de red correcto

Antes de cambiar la configuración de la VM, se revisó qué adaptador de red
usaba realmente el host Windows para salir a internet:

```powershell
ipconfig
```

Del resultado se identificaron varios adaptadores, y se descartaron los
virtuales:

| Adaptador       | IP                                      | Uso                              |
| --------------- | --------------------------------------- | -------------------------------- |
| Wi-Fi           | 192.168.1.144 (con gateway 192.168.1.1) | Conexión real a internet         |
| Ethernet 2      | 192.168.56.1 (sin gateway)              | VirtualBox Host-Only Adapter     |
| vEthernet (WSL) | 172.24.240.1 (sin gateway)              | Adaptador virtual de WSL/Hyper-V |

**Regla usada:** el adaptador correcto es el único con **puerta de enlace
predeterminada** configurada, ya que eso confirma que es la salida real a la
red/internet.

---

## 4. Solución: cambiar la VM de modo NAT a Adaptador Puente (Bridged)

1. Apagar la VM por completo.
2. En VirtualBox: **Configuración de la VM → Red → Adaptador 1 → Conectado a:
   Adaptador puente**.
3. En el desplegable "Nombre", seleccionar el adaptador **Wi-Fi** real (no el
   Host-Only ni el de WSL).
4. Encender la VM.

Con esto, la VM pasa a ser un dispositivo más dentro de la red WiFi real
(`192.168.1.0/24`), en vez de vivir en una red NAT aislada.

---

## 5. Verificación dentro de la VM

```bash
ip addr show
```

**Resultado:** la interfaz `enp0s3` ahora mostraba:

```
inet 192.168.1.183/24 ... scope global dynamic enp0s3
```

Ya en el mismo rango que el Wi-Fi del host Windows (`192.168.1.144`) →
confirma que el modo puente quedó bien configurado.

Se verificó también el estado del servicio y los puertos en escucha:

```bash
sudo systemctl status ssh
sudo ss -tulpn
```

**Resultado relevante:**
```
tcp   LISTEN   0   4096   0.0.0.0:22
tcp   LISTEN   0   4096   [::]:22
```
Confirma que `sshd` escucha en todas las interfaces IPv4 e IPv6, puerto 22.

---

## 6. Conexión exitosa

Desde Windows, con la IP nueva y sin especificar puerto (aún no se había
cambiado del 22 por defecto):

```powershell
ssh lukas@192.168.1.183
```

Se aceptó la huella digital del servidor la primera vez (`yes`), se ingresó la
contraseña, y la conexión quedó establecida correctamente.

---

## Resumen de causa raíz

El problema completo se debió a una sola causa: **la VM estaba en modo de red
NAT**, que aísla a la VM del resto de la red del host. Los distintos errores
(`timed out`, `refused`, hostname inválido) fueron síntomas de estar probando
distintas combinaciones de IP/puerto sin haber resuelto ese problema de fondo.
Cambiar a **modo puente** resolvió el problema, dándole a la VM una IP real y
alcanzable dentro de la LAN.

---

## Comandos clave usados en esta sesión

```bash
# En la VM (Ubuntu Server)
sudo systemctl status ssh
ip addr show
sudo ss -tulpn

# En Windows (PowerShell)
ipconfig
ssh lukas@192.168.1.183
```

---
