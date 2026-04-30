# zrok Tunnel — Acceso Público a condo-py

> Configuración del túnel zrok para exponer el API local a internet durante desarrollo.

---

## URL pública

```
https://condopy.share.zrok.io
```

**Endpoints de prueba:**
- `/health` → `{"success":true,"message":"API is running"}`
- `/docs` → Swagger UI
- `/openapi.json` → OpenAPI spec

---

## Prerrequisitos

- [zrok](https://zrok.io/) instalado (`zrok version` → v1.1.11+)
- Cuenta zrok configurada (`zrok status` → Account Token + Ziti Identity `<<SET>>`)
- Puerto 7501 del container expuesto al host (ver `docker-compose.yml`)

---

## Configuración

### 1. Puerto expuesto en docker-compose

```yaml
# docker-compose.yml
services:
  backend:
    ports:
      - "7501:7501"    # ← expone uvicorn al host
```

### 2. Reservar share público (URL persistente)

Solo se hace **una vez**. El nombre `condopy` es la URL pública.

```bash
zrok reserve public http://localhost:7501 --backend-mode proxy --unique-name condopy
```

### 3. Iniciar el túnel

```bash
# Manual (se cae al cerrar terminal)
zrok share reserved condopy --headless

# Persistente (sobrevive al cierre de terminal)
nohup zrok share reserved condopy --headless > /tmp/zrok-condopy.log 2>&1 &
```

### 4. Verificar

```bash
curl https://condopy.share.zrok.io/health
# {"success":true,"message":"API is running","data":{"status":"healthy"},"errors":null}
```

---

## Inicio automático (systemd)

Crear `/etc/systemd/system/zrok-condopy.service`:

```ini
[Unit]
Description=zrok tunnel for condo-py
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=miguel
ExecStart=/usr/bin/zrok share reserved condopy --headless
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now zrok-condopy
```

---

## Comandos útiles

| Comando | Descripción |
|---|---|
| `zrok overview` | Listar shares activos |
| `zrok status` | Estado de la cuenta/conexión |
| `pgrep -af "zrok share"` | Ver procesos zrok corriendo |
| `tail -f /tmp/zrok-condopy.log` | Ver logs del túnel |
| `pkill -f "zrok share reserved condopy"` | Detener el túnel |

---

## Troubleshooting

| Problema | Solución |
|---|---|
| `bad gateway!` | El túnel no está corriendo o recién inició (darle ~5s) |
| `connection refused` | El container Docker no está corriendo o el puerto 7501 no está expuesto |
| `invalid unique name` | El nombre debe ser alfanumérico, minúsculas, 4-32 caracteres |
| URL cambia cada vez | Usar `zrok reserve` (persistente) en vez de `zrok share public` (efímero) |
