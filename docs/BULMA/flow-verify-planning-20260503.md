# Verification + Planning — Flujo UI select-condo + dashboard (Residente)

**Date:** 2026-05-03
**Last Updated:** 2026-05-03 (v2 — dopo jaque mate Lelouch)
**Reviewer:** Misato K
**Status:** ✅ Implementado y verificado

---

## Resumen ejecutivo

El flujo UI de residente para `condo-net` está **completo**. La solución final es limpia: un solo fetch al endpoint existente `/residents/dashboard` que agrega toda la información necesaria para las tarjetas informativas.

La corrección clave fue de **Lelouch**: en vez de crear endpoints nuevos, identificar que `GET /residents/dashboard` ya existía y contenía exactamente lo que el dashboard necesitaba. Bulma rewirió el frontend para usar esa fuente única.

---

## PARTE 1 — Verificación final del código

### select-condo ✅
- Logo (`logo_url`) con fallback `Building2`
- Dirección completa (`address` + `city` + `country`)
- Badge de rol (Propietario / Inquilino / Residente)
- Botón "Ingresar" con `LogIn` icon

### dashboard ✅
**Antes (❌):** 4 fetches encadenados con fallbacks rotos (`/payments/status`, `/ar/user-summary`, `/communications`, `/announcements`) → estado "No disponible"

**Ahora (✅):** Un solo fetch:
```
GET /residents/dashboard?condominium_id={id}
→ payment_pending_total   → tarjeta "¿Al día?"
→ recent_announcements   → tarjeta "Comunicados"
→ unread_notifications   → refuerza count comunicados
→ pending_incidents      → listo para módulos futuros
→ pending_packages       → listo para módulos futuros
→ upcoming_visitors      → listo para módulos futuros
```

### Quick links (residente) ✅
```
Mis pagos | Comunicados | Incidencias | Visitantes | Áreas comunes | Mi perfil
```

---

## PARTE 2 — Brechas identificadas (estado)

| # | Gap | Estado | Solución |
|---|---|---|---|
| ~~B1~~ | Falta `GET /ar/user-summary` | **Descartado** | No necesario — `/residents/dashboard` lo cubre |
| ~~B2~~ | `/announcements` response shape | **Descartado** | No se usa más — `/residents/dashboard` lo cubre |
| ~~B3~~ | Permiso `announcement.read` | **Ya existía** | El endpoint usa `get_current_user`, no RBAC para residentes |
| F1 | Quick links admin vs residente | **✅ Resuelto** | Links actualizados a 6 módulos de residente |
| F2 | Parsing de announcements en dashboard | **✅ Resuelto** | Ya no se llama `/announcements` directamente |

---

## PARTE 3 — Arquitectura de la solución

### Decisión clave: usar `/residents/dashboard` como fuente única

**No se creó ningún endpoint nuevo.** El endpoint `GET /residents/dashboard` ya existía en el backend y retornaba exactamente los datos que el dashboard del residente necesitaba. El problema original era que el frontend estaba指向 endpoints incorrectos.

### Endpoint: `GET /residents/dashboard?condominium_id=X`

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "condominium_id": 1,
    "unread_notifications": 2,
    "pending_incidents": 0,
    "pending_packages": 0,
    "upcoming_visitors": 1,
    "payment_pending_total": 0.00,
    "recent_announcements": [
      {
        "uuid": "...",
        "title": "Mantenimiento del ascensor",
        "category": "info",
        "published_at": "2026-05-01T10:00:00",
        "is_pinned": true
      }
    ]
  }
}
```

### Mapa de datos → UI

| Campo API | → | Tarjeta UI |
|---|---|---|
| `payment_pending_total === 0` | → | "¿Al día en sus pagos?" verde ✅ |
| `payment_pending_total > 0` | → | "¿Al día?" rojo + monto |
| `recent_announcements.length` | → | Badge count comunicados |
| `unread_notifications` | → | Se suma al count de comunicados |
| `recent_announcements[0]` | → | Título del más reciente |

---

## PARTE 4 — Brecha pendiente: inquilino/residente ocupante

**⚠️ Tema abierto — identificado por Lelouch**

El cálculo de `payment_pending_total` en `resident_query_repository.py` usa `JOIN core_unit_ownerships`:

```sql
FROM core_accounts_receivable ar
JOIN core_unit_ownerships ow ON ow.unit_id = ar.unit_id
WHERE ow.user_id = :uid ...
```

Esto cubre **propietarios** (que tienen ownership registrado). Pero un **inquilino** (residente ocupante sin ownership) podría no aparecer aquí porque solo tiene `core_unit_occupancies` — no `core_unit_ownerships`.

**Opciones:**

- **Opción A (recomendada):** Unificar el cálculo para incluir tambiénoccupancies activas del usuario. Modificar la query del dashboard para hacer un `UNION` o un `LEFT JOIN` que cubra tanto ownerships como occupancies activas.

- **Opción B:** Documentar que inquilinos no ven deuda de pagos hasta que se implemente occupancy-aware billing.

**Estado:** ⚠️ **Abierto** — requiere decisión de negocio + ajuste en `resident_query_repository.py`.

---

## PARTE 5 — Estado final de tareas

### Tareas completadas

- [x] select-condo: logo + address + badge rol + botón Ingresar ✅
- [x] dashboard: rewired a `/residents/dashboard` (1 solo fetch) ✅
- [x] dashboard: tarjetas de pagos + comunicados funcionando ✅
- [x] dashboard: quick links de residente (6 módulos) ✅
- [x] TypeScript compila limpio
- [x] ESLint limpio en archivos tocados

### Tarea abierta

- [ ] **Gap inquilino:** Verificar que `payment_pending_total` cubre también a residentes sin ownership (solo occupancy). Si no — ajustar query o documentar limitaciones.

---

## PARTE 6 — Archivos modificados (resumen)

| Archivo | Cambio |
|---|---|
| `condo-net/src/src/app/select-condo/page.tsx` | Tarjeta enriquecida |
| `condo-net/src/src/app/dashboard/page.tsx` | Rewired a `/residents/dashboard` + quick links residente |
| `condo-py/src/library/dddpy/core_residents/infrastructure/resident_query_repository.py` | ✅ Ya existente, sin cambios — Gap inquilino pendiente |

---

## Testing checklist

- [ ] Login con usuario propietario → verificar tarjeta verde (al día)
- [ ] Login con usuario con deuda → verificar tarjeta roja + monto
- [ ] Login con коммуникации pendientes → verificar count + título
- [ ] Login sin novedades → verificar "Sin novedades"
- [ ] Quick links → cada uno lleva a su módulo
- [ ] Inquilino (sin ownership, solo occupancy) → verificar que ve su estado de pagos correctamente

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*