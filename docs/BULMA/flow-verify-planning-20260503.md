# Verification + Planning — Flujo UI select-condo + dashboard (Residente)

**Date:** 2026-05-03
**Last Updated:** 2026-05-03 (v3 — gap inquilino cerrado)
**Reviewer:** Misato K
**Status:** ✅ Todo completo — sin items pendientes

---

## Resumen ejecutivo

El flujo UI de residente para `condo-net` está **completo**. La solución final es limpia: un solo fetch al endpoint existente `/residents/dashboard` que agrega toda la información necesaria para las tarjetas informativas.

La corrección clave fue de **Lelouch**: en vez de crear endpoints nuevos, identificar que `GET /residents/dashboard` ya existía y contenía exactamente lo que el dashboard necesitaba. Bulma rewirió el frontend para usar esa fuente única. El gap de inquilinos fue resuelto después con un ajuste en la query del repository.

---

## PARTE 1 — Implementación completada

### select-condo ✅
- Logo (`logo_url`) con fallback `Building2`
- Dirección completa (`address` + `city` + `country`)
- Badge de rol (Propietario / Inquilino / Residente)
- Botón "Ingresar" con `LogIn` icon

### dashboard ✅
**Antes (❌):** 4 fetches encadenados con fallbacks rotos → estado "No disponible"
**Ahora (✅):** Un solo fetch a `/residents/dashboard?condominium_id={id}`

### Quick links (residente) ✅
```
Mis pagos | Comunicados | Incidencias | Visitantes | Áreas comunes | Mi perfil
```

---

## PARTE 2 — Arquitectura de la solución

### Decisión clave: usar `/residents/dashboard` como fuente única

**No se creó ningún endpoint nuevo.** El endpoint existente cubría todo — solo había que pointing el frontend a la ruta correcta.

### Response del endpoint

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

## PARTE 3 — Gap inquilino: RESUELTO ✅

**Problema:** `payment_pending_total` solo consultaba `core_unit_ownerships` — cubría propietarios pero no inquilinos con occupancy activa.

**Solución:** `get_dashboard_summary()` ahora hace UNION de ownerships + occupancies activas con deduplicación:

```python
# Paso 1: units vía ownership
owner_units = SELECT DISTINCT unit_id FROM core_unit_ownerships WHERE user_id = :uid

# Paso 2: units vía occupancy activa
occupancy_units = SELECT DISTINCT unit_id FROM core_unit_occupancies
                  WHERE user_id = :uid AND end_date IS NULL

# Paso 3: UNION deduplicado (Python set — O(n), sin duplicado)
all_unit_ids = set(owner_units) | set(occupancy_units)

# Paso 4: AR de esas unidades (no paid, no cancelled, no deleted)
```

**Casos cubiertos:**
- ✅ Solo owner → ve deuda correctamente
- ✅ Solo tenant activo → ve deuda correctamente
- ✅ Owner + tenant misma unidad → sin duplicado de montos
- ✅ Occupancy vencida → excluida (`end_date IS NULL`)
- ✅ Múltiples unidades válidas → suma correcta sin duplicado

**Tests:** 27 pasan (14 integración con MySQL real + 13 unitarios puros)

---

## PARTE 4 — Estado final de todas las tareas

### Tareas completadas

- [x] select-condo: logo + address + badge rol + botón Ingresar ✅
- [x] dashboard: rewired a `/residents/dashboard` (1 solo fetch) ✅
- [x] dashboard: tarjetas de pagos + comunicados funcionando ✅
- [x] dashboard: quick links de residente (6 módulos) ✅
- [x] Gap inquilino: UNION ownerships + occupancies activas ✅
- [x] TypeScript compila limpio
- [x] ESLint limpio en archivos tocados
- [x] 27 tests pasando (14 DB + 13 unitarios)

---

## PARTE 5 — Archivos modificados

| Archivo | Cambio |
|---|---|
| `condo-net/src/src/app/select-condo/page.tsx` | Tarjeta enriquecida |
| `condo-net/src/src/app/dashboard/page.tsx` | Rewired a `/residents/dashboard` + quick links residente |
| `condo-py/src/library/dddpy/core_residents/infrastructure/resident_query_repository.py` | UNION ownerships + occupancies activas con deduplicación |
| `condo-py/tests/test_resident_dashboard_payment.py` | 14 tests integración |
| `condo-py/tests/test_resident_dashboard_payment_unit.py` | 13 tests unitarios puros |

---

## PARTE 6 — Testing checklist (estado completo)

- [x] Login con usuario propietario → verificar tarjeta verde (al día)
- [x] Login con usuario con deuda → verificar tarjeta roja + monto
- [x] Login con kommunikationen pendientes → verificar count + título
- [x] Login sin novedades → verificar "Sin novedades"
- [x] Quick links → cada uno lleva a su módulo
- [x] Inquilino (sin ownership, solo occupancy) → ✅ 27 tests verificando correcta

---

## Cierre

**Sin items pendientes.** El flujo UI completo para residentes de `condo-net` está implementado, verificado y documentado.

- Flow: Login → select-condo → dashboard ✅
- Tarjeta de selección: logo + address + rol + botón Ingresar ✅
- Dashboard: 2 tarjetas informativas + 6 quick links ✅
- Gap inquilino resuelto ✅
- 27 tests pasando ✅

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*