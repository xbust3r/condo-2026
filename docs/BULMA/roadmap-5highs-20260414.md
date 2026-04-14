# ROADMAP PRIORIDAD — 5 HIGH's Phase 1

**Fecha:** 2026-04-14
**Equipo:** Misato (coordinación + revisión) / Bulma (ejecución)
**Módulo referencia:** `core_buildings`

## Regla de guerra
- No abrir expansión nueva hasta cerrar estos 5 HIGH.
- `core_buildings` = baseline oficial.

---

## HIGH-1 · `core_condominiums` — Bypass de capas en `restore`

**Problema:** `CondominiumUseCase.restore()` toca `repository.restore()` directo — rompe disciplina de capas.

**Fix:**
1. Exponer `restore(id)` en `CondominiumCmdUseCase`
2. Llamar `self.condominium_cmd_usecase.restore(id)` desde el facade
3. Agregar contrato `restore()` a `CondominiumRepository` (ABC del dominio)
4. Confirmar que `soft_delete()` y `restore()` viven en el repository correcto

**Archivo crítico:**
- `usecase/condominium_usecase.py` línea 95
- `domain/condominium_repository.py`

**Label para handoff:** `#high1-condominiums-bypass`

---

## HIGH-2 · `core_condominiums` — Respuesta inconsistente en `delete`

**Problema:** `delete()` responde con `existing.deleted_at` (snapshot previo), no con el estado real post-soft-delete.

**Fix:**
1. En `CondominiumCmdUseCase.delete()` → llamar `self.repository.soft_delete(id)` 
2. En `CondominiumUseCase.delete()` → retornar `{"id": id, "deleted_at": <timestamp real>}` post-operación
3. Verificar que `soft_delete()` en el repository actualiza y retorna el `deleted_at` correcto

**Archivo crítico:**
- `usecase/condominium_usecase.py` líneas 83-100
- `infrastructure/condominium_cmd_repository.py`

**Label para handoff:** `#high2-condominiums-delete-response`

---

## HIGH-3 · `core_unities` — Queries sin filtro `deleted_at`

**Problema:** `get_by_unit_number_in_building` y `get_by_code_in_building` no filtran `deleted_at IS NULL` — reintroducen entidades eliminadas al flujo.

**Fix:**
1. Agregar `.filter(DBUnities.deleted_at.is_(None))` a `get_by_unit_number_in_building`
2. Agregar `.filter(DBUnities.deleted_at.is_(None))` a `get_by_code_in_building`

**Archivo crítico:**
- `infrastructure/unity_query_repository.py` líneas 52-85

**Label para handoff:** `#high3-unities-deleted-at`

---

## HIGH-4 · `core_condominiums` — Tipado débil en repositories

**Problema:** 4 métodos devolviendo `Optional[object]` y `list_all()` devolviendo `List[object]` — rompe type safety en todo el chain.

**Fix:**
1. `get_by_id` → `Optional[CondominiumEntity]`
2. `get_by_uuid` → `Optional[CondominiumEntity]`
3. `get_by_code` → `Optional[CondominiumEntity]`
4. `get_by_name` → `Optional[CondominiumEntity]`
5. `list_all` → `tuple[List[CondominiumEntity], int]`

**Archivo crítico:**
- `infrastructure/condominium_query_repository.py` líneas 22, 35, 48, 61, 70

**Label para handoff:** `#high4-condominiums-typing`

---

## HIGH-5 · Homologación transversal de soft delete

**Problema:** políticas inconsistentes entre módulos — algunos filtran `deleted_at`, otros no.

**Fix:**
Auditar y asegurar que en TODOS los módulos:
- `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name` excluyen eliminados por defecto
- `list_all` tiene `include_deleted` como puerta explícita
- `delete` responde con estado post-operación real
- `restore` pasa por cmd_usecase

**Módulos a auditar:**
- `core_condominiums` ← ya en fix HIGH-1 y HIGH-2
- `core_buildings` ← baseline, ya cumple
- `core_buildings_types`
- `core_unities` ← ya en fix HIGH-3
- `core_unities_types`

**Label para handoff:** `#high5-transversal-soft-delete`

---

## Orden de ejecución

```
Sprint 1: HIGH-1 + HIGH-2 (core_condominiums — mismo módulo, mismo sprint)
Sprint 2: HIGH-4 (core_condominiums — tipado, mismo módulo)
Sprint 3: HIGH-3 (core_unities — queries)
Sprint 4: HIGH-5 (transversal — todos los módulos)
```

## Handoff etiquetas

Cada handoff entre Bulma → Misato debe usar:
- Label del issue (`#high1-condominiums-bypass`)
- Path del archivo modificado
- Antes / Después
- Test incluido: sí/no

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*