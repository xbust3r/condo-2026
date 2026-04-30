# ROADMAP PRIORIDAD — 5 HIGH's Phase 1

**Fecha:** 2026-04-14
**Última actualización:** 2026-04-30
**Equipo:** Misato (coordinación + revisión) / Bulma (ejecución)
**Módulo referencia:** `core_buildings`

## Regla de guerra
- No abrir expansión nueva hasta cerrar estos 5 HIGH.
- `core_buildings` = baseline oficial.

---

## HIGH-1 · `core_condominiums` — Bypass de capas en `restore`

**Problema:** `CondominiumUseCase.restore()` tocaba `repository.restore()` directo — rompía disciplina de capas.

**Fix:**
1. Exponer `restore(id)` en `CondominiumCmdUseCase`
2. Llamar `self.condominium_cmd_usecase.restore(id)` desde el facade
3. Agregar contrato `restore()` a `CondominiumRepository` (ABC del dominio)
4. Confirmar que `soft_delete()` y `restore()` viven en el repository correcto

**Archivo crítico:**
- `usecase/condominium_usecase.py` línea 185
- `domain/condominium_repository.py`

**Label para handoff:** `#high1-condominiums-bypass`

**Estado:** ✅ CERRADO (commit `3ad3f55` — 2026-04-14)

---

## HIGH-2 · `core_condominiums` — Respuesta inconsistente en `delete`

**Problema:** `delete()` respondía con `existing.deleted_at` (snapshot previo), no con el estado real post-soft-delete.

**Fix:**
1. En `CondominiumCmdUseCase.delete()` → llamar `self.repository.soft_delete(id)`
2. En `CondominiumUseCase.delete()` → retornar `{"id": id, "deleted_at": <timestamp real>}` post-operación
3. Verificar que `soft_delete()` en el repository actualiza y retorna el `deleted_at` correcto

**Archivo crítico:**
- `usecase/condominium_usecase.py` líneas 160-175
- `infrastructure/condominium_cmd_repository.py`

**Label para handoff:** `#high2-condominiums-delete-response`

**Estado:** ✅ CERRADO (commit `3ad3f55` — 2026-04-14)

---

## HIGH-3 · `core_units` — Queries sin filtro `deleted_at`

**Problema:** `get_by_unit_number_in_building` y `get_by_code_in_building` no filtraban `deleted_at IS NULL` — reintroducían entidades eliminadas al flujo.

**Fix:**
1. Agregar `.filter(DBUnits.deleted_at.is_(None))` a `get_by_unit_number_in_building`
2. Agregar `.filter(DBUnits.deleted_at.is_(None))` a `get_by_code_in_building`

**Archivo crítico:**
- `infrastructure/unit_query_repository.py` líneas 50-90

**Label para handoff:** `#high3-unities-deleted-at`

**Estado:** ✅ CERRADO (commit `3ad3f55` — 2026-04-14)

---

## HIGH-4 · `core_condominiums` — Tipado débil en repositories

**Problema:** 4 métodos devolviendo `Optional[object]` y `list_all()` devolviendo `List[object]` — rompía type safety en todo el chain.

**Fix:**
1. `get_by_id` → `Optional[CondominiumEntity]`
2. `get_by_uuid` → `Optional[CondominiumEntity]`
3. `get_by_code` → `Optional[CondominiumEntity]`
4. `get_by_name` → `Optional[CondominiumEntity]`
5. `list_all` → `tuple[List[CondominiumEntity], int]`

**Archivo crítico:**
- `infrastructure/condominium_query_repository.py` líneas 20, 32, 44, 56, 68

**Label para handoff:** `#high4-condominiums-typing`

**Estado:** ✅ CERRADO (commit `3ad3f55` — 2026-04-14)

---

## HIGH-5 · Homologación transversal de soft delete

**Problema:** políticas inconsistentes entre módulos — algunos filtran `deleted_at`, otros no.

**Fix:**
Auditar y asegurar que en TODOS los módulos:
- `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name` excluyen eliminados por defecto
- `list_all` tiene `include_deleted` como puerta explícita
- `delete` responde con estado post-operación real
- `restore` pasa por cmd_usecase

**Módulos auditados:**
- `core_condominiums` ✅
- `core_buildings` ✅ (baseline, ya cumplía)
- `core_buildings_types` ✅
- `core_units` ✅
- `core_unit_types` ✅

**Label para handoff:** `#high5-transversal-soft-delete`

**Estado:** ✅ CERRADO (auditoría completada 2026-04-14, documentada en `high5-transversal-audit-20260414.md`)

---

## Verificación final (2026-04-30)

| HIGH | Descripción | Estado verificado |
|---|---|---|
| HIGH-1 | `restore()` por cmd_usecase | ✅ `condominium_cmd_usecase.restore(id)` en línea 185 |
| HIGH-2 | `delete()` retorna `deleted_at` real | ✅ re-fetch post-delete con `get_by_id_any_status` |
| HIGH-3 | Queries filtran `deleted_at` en `core_units` | ✅ filtros presentes en `unit_query_repository.py` |
| HIGH-4 | Tipado `Optional[object]` → `Optional[CondominiumEntity]` | ✅ tipos correctos |
| HIGH-5 | Auditoría transversal soft delete | ✅ `get_by_id_any_status` en todos los módulos |

**DB:** última migración aplicada `050_add_user_profile_extra_fields`
**RBAC:** `core_permissions` (63 permisos) + `core_role_permissions` (88 mappings) — enforcement activo en 17 módulos (commit `a8650b6`)
**Phase 2:** Implementada — tabla `core_permissions` + `core_role_permissions` seedeadas, enforcement endpoint-level activo

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*
