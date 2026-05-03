# Task — `payment_pending_total` + occupancy activas

**Developer:** Bulma S
**Architect:** Lelouch S
**Date:** 2026-05-03
**Source:** `#flujo-de-interfaz` — Mike Ross + Lelouch S
**Status:** ✅ Completada (2026-05-03)
**Repo:** `/home/miguel/servers/condo-py`

---

## Problema

El cálculo actual de `payment_pending_total` en `resident_query_repository.py` solo consulta `core_unit_ownerships`:

```sql
FROM core_accounts_receivable ar
JOIN core_unit_ownerships ow ON ow.unit_id = ar.unit_id
WHERE ow.user_id = :uid ...
```

Esto cubre **propietarios**, pero un **inquilino con occupancy activa** (sin ownership) no ve su estado de deuda — aunque por regla de negocio debe verlo.

---

## Regla de negocio (definida por Lelouch + Mike Ross)

> **Un inquilino con occupancy activa asume todas las obligaciones de la unidad donde vive** — deudas, pagos, multas, cumplimiento — y también sus beneficios operativos.

Consecuencia directa:
- **owner activo** → ve estado financiero de su unidad
- **tenant/inquilino activo** → también ve estado financiero de su unidad
- **Occupancy vencida** → **no cuenta**

---

## Regla técnica

1. El ajuste va en `resident_query_repository.py` — **no crear endpoint nuevo**
2. El cálculo de `payment_pending_total` debe considerar unidades vinculadas al usuario por:
   - `core_unit_ownerships` (propietario)
   - **o** `core_unit_occupancies` activas (`end_date IS NULL` / vigencia activa)
3. **Deduplicación obligatoria**: si el mismo usuario aparece como owner + occupant en la misma unidad, **no se duplica** deuda ni cargos. Usar `UNION / DISTINCT` o deduplicación por AR, no suma ciega.
4. Solo contar AR con estado: `NOT IN ('paid', 'cancelled')` y `deleted_at IS NULL`
5. No alterar el shape del response de `/residents/dashboard` — mantener el contrato actual

---

## Cambio requerido

**Archivo:** `src/library/dddpy/core_residents/infrastructure/resident_query_repository.py`
**Método:** `get_dashboard_summary()`

**Lógica nueva:**
```python
# 1. Obtener units por ownership
owner_units = session.execute(text("""
    SELECT DISTINCT ow.unit_id
    FROM core_unit_ownerships ow
    WHERE ow.user_id = :uid
"""), {"uid": user_id}).scalars().all()

# 2. Obtener units por occupancy activa
occupancy_units = session.execute(text("""
    SELECT DISTINCT occ.unit_id
    FROM core_unit_occupancies occ
    WHERE occ.user_id = :uid
      AND occ.end_date IS NULL
"""), {"uid": user_id}).scalars().all()

# 3. UNION deduplicada
all_unit_ids = set(owner_units) | set(occupancy_units)

# 4. Sumar AR de esas unidades (sin duplicados)
payment_pending = session.execute(text("""
    SELECT COALESCE(SUM(ar.amount - ar.paid_amount), 0) AS pending
    FROM core_accounts_receivable ar
    WHERE ar.unit_id IN :unit_ids
      AND ar.condominium_id = :condo_id
      AND ar.status NOT IN ('paid', 'cancelled')
      AND ar.deleted_at IS NULL
"""), {"unit_ids": tuple(all_unit_ids), "condo_id": condominium_id}).scalar() or 0.0
```

**Notas:**
- Usar `tuple(all_unit_ids)` para el `IN` de SQLAlchemy
- `set(...) | set(...)` deduplica antes de consultar
- Mantener el mismo retorno: `{"payment_pending_total": float(payment_pending), ...}`

---

## Casos que deben quedar cubiertos

| Caso | Esperado |
|---|---|
| Solo owner | Ve deuda de sus unidades via ownership |
| Solo tenant activo | Ve deuda de sus unidades via occupancy activa |
| Owner + tenant sobre misma unidad | Ve deuda una sola vez (no duplicado) |
| Tenant con occupancy vencida | **No ve deuda** — occupancy vencida no cuenta |
| Usuario con varias unidades válidas | Suma correcta sin duplicado |

---

## Criterios de aceptación

- [x] `payment_pending_total` incluye AR de ownerships **y** occupancies activas ✅
- [x] Doble vínculo (owner + occupant en misma unidad) no duplica montos ✅
- [x] Occupancy vencida queda excluida ✅
- [x] El response shape de `/residents/dashboard` no cambia ✅
- [x] No se añadieron endpoints ni fetches nuevos ✅
- [x] Diff con explicación breve de la deduplicación ✅

---

## Verificación (Misato)

**Funcional:**
- owner ve deuda correcta
- tenant activo ve deuda correcta
- occupancy vencida queda fuera
- doble vínculo no duplica montos

**Técnica:**
- shape de `/residents/dashboard` sin cambios
- query con rendimiento aceptable (sin N+1)
- diff limpio y documentado

---

## Archivos a tocar

| Archivo | Cambio |
|---|---|
| `src/library/dddpy/core_residents/infrastructure/resident_query_repository.py` | Ajustar `get_dashboard_summary()` para UNION ownerships + occupancies activas con deduplicación |
| `docs/BULMA/flow-verify-planning-20260503.md` | Marcar gap como resuelto |

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*