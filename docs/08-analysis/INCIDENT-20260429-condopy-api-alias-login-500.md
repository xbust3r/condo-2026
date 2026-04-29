# INCIDENTE: Login 500 — `condopy-api` alias DNS faltante en red Docker

## Proyecto
- **Sistema:** `condo-py` (API backend) + `condobackdmin` (frontend Next.js)
- **Fecha:** 2026-04-29
- **Severidad:** 🔴 Alta — Login completamente roto
- **Resolvedor:** Misato K (Coordinadora)
- **Reportado por:** Mike Ross

---

## 1. Resumen Ejecutivo

El login en `condobackdmin` fallaba con **500 Internal Server Error** en `POST /auth/login`. El frontend proxy intentaba conectar a `http://condopy-api:7501` pero el hostname no se resolvía (`ENOTFOUND`). El API real estaba corriendo sin problemas.

---

## 2. Síntomas

```
POST http://condobackdmin.test/api-proxy/auth/login → 500
Error: getaddrinfo ENOTFOUND condopy-api
```

- El backend de Next.js (`condobackdmin`) funciona normalmente ✅
- El contenedor `backend-corps-dev-condo-py_backend` está **Up** ✅
- El health endpoint del API responde correctamente ✅
- Solo falla la resolución DNS interna del alias `condopy-api` ❌

---

## 3. Root Cause

El contenedor `backend-corps-dev-condo-py_backend` fue **recreado** (hace ~4 horas, probablemente restart automático). Al reconectarse a la red Docker `services_network`, Docker **no le asignó el alias `condopy-api`** pese a que `docker-compose.yml` lo declara:

```yaml
# docker-compose.yml
services:
  backend:
    networks:
      default:
        aliases:
          - condopy-api   # ← este alias no se attachó al reconectar
```

**Comportamiento observado:** Docker permite que un contenedor existente se reconecte a una red externa sin volver a evaluar los aliases definidos en el compose. El alias solo se aplica en el primer `docker network connect` o al hacer `up`.

---

## 4. Solución Aplicada

```bash
# Desconectar y reconectar con el alias correcto
docker network disconnect services_network backend-corps-dev-condo-py_backend
docker network connect --alias condopy-api services_network backend-corps-dev-condo-py_backend
```

**Verificación:**
```bash
# Confirmar alias en la red
docker inspect backend-corps-dev-condo-py_backend \
  --format '{{json .NetworkSettings.Networks}}' | python3 -m json.tool

# Probar resolución
docker exec backend-corps-dev-condo-py_backend \
  curl -s http://condopy-api:7501/health

# Probar endpoint real
docker exec backend-corps-dev-condo-py_backend \
  wget -qO- http://localhost:7501/health
```

**Resultado:**
```json
{"success":true,"message":"API is running","data":{"status":"healthy"}}
```

---

## 5. Containers y Redes Involucrados

| Contenedor | Red | Aliases |
|---|---|---|
| `backend-corps-dev-condo-py_backend` | `services_network` | `condopy-api`, `mysql` |
| `backend-corps-dev-condo-backdmin_backend` | `services_network` | _(sin aliases)_ |

El frontend usa `NEXT_PUBLIC_API_URL=/api-proxy` que hace proxy a `API_INTERNAL_URL=http://condopy-api:7501`.

---

## 6. Prevención

### Opción A — Fix permanente en `docker-compose.yml`
Usar `--force-recreate` al hacer `up` para asegurar que los aliases se evalúen:

```bash
make down && make up
```

### Opción B — Healthcheck de resolución DNS
Agregar un script de startup que verifique la resolución antes de levantar el servicio:

```python
# startup_check.py
import socket
def check_dns(hostname, expected_alias):
    try:
        ips = socket.gethostbyname_ex(hostname)
        assert expected_alias in ips[0] or expected_alias in ips[2], \
            f"Alias {expected_alias} not found for {hostname}"
    except socket.gaierror:
        raise RuntimeError(f"DNS lookup failed for {hostname}")
```

### Opción C — Script de red idempotente
Crear un script `scripts/ensure-network-aliases.sh` que pueda correrse en cualquier momento:

```bash
#!/bin/bash
CONTAINER="backend-corps-dev-condo-py_backend"
ALIAS="condopy-api"
NETWORK="services_network"

if ! docker inspect "$CONTAINER" --format '{{json .NetworkSettings.Networks}}' | \
     python3 -c "import sys,json; nets=json.load(sys.stdin); exit(0 if '$ALIAS' in nets.get('$NETWORK',{}).get('Aliases',[]) else 1)"; then
  echo "[FIX] Reconnecting $CONTAINER with alias $ALIAS"
  docker network disconnect "$NETWORK" "$CONTAINER"
  docker network connect --alias "$ALIAS" "$NETWORK" "$CONTAINER"
fi
```

---

## 7. Líneas de Tiempo

| Hora | Evento |
|---|---|
| ~12:40 | Contenedor `condo-py` se recrea (restart) |
| ~16:44 | Mike reporta error 500 en login |
| ~16:49 | Alias `condopy-api` reconectado manualmente |
| ~16:50 | Login verificado funcional |

---

## 8. Lesson Learned

> Docker no re-aplica los `aliases` de `docker-compose.yml` cuando un contenedor ya existente se reconecta a una red externa (`network_mode: external`). Los aliases solo se asignan en el primer attach o con `docker-compose up --force-recreate`.

**Regla:** Después de cualquier restart/recreate de un contenedor en red externa, verificar que los aliases DNS estén presentes.

---

## 9. Contactos

| Rol | Nombre | Discord |
|---|---|---|
| Architect | Lelouch | @Lelouch S |
| Dev | Bulma | @Bulma S |
| Coordinator | Misato | @Misato K |
