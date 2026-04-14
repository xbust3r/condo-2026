# HIGH-5 Transversal — Soft Delete Audit
**Fecha:** 2026-04-14  
**Auditor:** Bulma S (Developer, condo-py)  
**Repo:** `/home/miguel/servers/condo-py`  
**Label:** `#high5-transversal-soft-delete`

---

## Resumen Ejecutivo

Se auditaron 5 módulos de Fase 1 verificando la política de soft delete (`deleted_at IS NULL` por defecto en reads, `include_deleted=True` explícito para listar eliminados, y post-mutación re-fetch con estado real). Se encontraron **7 deviationes** de la política, todas corregidas durante la auditoría.

**Estado general:** ✅ POLÍTICA HOMOLOGADA (post-fixes)

---

## Política de Soft Delete

| Operación | Comportamiento esperado |
|---|---|
| `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name` | Filtra `deleted_at IS NULL` por defecto |
| `list_all` | Excluye eliminados por defecto; `include_deleted=True` los incluye |
| `delete` | Soft-delete (`deleted_at = now`); respuesta incluye estado real post-mutación |
| `restore` | Verifica existencia pre-mutación (cualquier estado); respuesta incluye estado real |
| Queries paralelas | Toda query debe tener filtro `deleted_at` apropiado |

---

## Simbología de Estados

| Estado | Significado |
|---|---|
| `OK` | Cumple la política, no se toca |
| `FIXED` | Corregido durante esta auditoría |
| `N/A` | Método no existe en este módulo |

---

## Archivos Modificados

| Archivo | Cambios |
|---|---|
| `src/library/dddpy/core_buildings/infrastructure/building_query_repository.py` | +`_get_by_id_any_status` |
| `src/library/dddpy/core_buildings/usecase/building_query_usecase.py` | +`get_by_id_any_status` |
| `src/library/dddpy/core_buildings/usecase/building_usecase.py` | `restore`: +existencia pre-check +re-fetch any-status; `delete`: +re-fetch any-status +`deleted_at` en respuesta |
| `src/library/dddpy/core_unities/infrastructure/unity_query_repository.py` | +`_get_by_id_any_status` |
| `src/library/dddpy/core_unities/usecase/unity_query_usecase.py` | +`get_by_id_any_status` |
| `src/library/dddpy/core_unities/usecase/unity_usecase.py` | `restore`: +existencia pre-check +re-fetch any-status; `delete`: +re-fetch any-status +`deleted_at` en respuesta |
| `src/library/dddpy/core_buildings_types/usecase/building_type_usecase.py` | `soft_delete`/`restore`: +existencia pre-check +`deleted_at` en respuesta |
| `src/library/dddpy/core_unities_types/usecase/unity_type_usecase.py` | `soft_delete`/`restore`: +existencia pre-check +`deleted_at` en respuesta |

---

## `core_condominiums`

### Query Repository
**Archivo:** `src/library/dddpy/core_condominiums/infrastructure/condominium_query_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | `deleted_at IS NULL` | OK | line 18 | — |
| `get_by_uuid` | `deleted_at IS NULL` | OK | line 32 | — |
| `get_by_code` | `deleted_at IS NULL` | OK | line 46 | — |
| `get_by_name` | `deleted_at IS NULL` | OK | line 60 | — |
| `list_all` | `include_deleted` param | OK | line 74 | Excluye por defecto; filtra por status/city/country |
| `_get_by_id_any_status` | Helper para post-mutación | OK | line 97 |ya existía |

### Cmd Repository
**Archivo:** `src/library/dddpy/core_condominiums/infrastructure/condominium_cmd_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro deleted_at (correcto — INSERT) | OK | line 24 | — |
| `update` | Sin filtro deleted_at (aceptable — usecase verifica) | OK | line 58 | — |
| `soft_delete` | Sin filtro deleted_at (set `deleted_at`) | OK | line 88 | — |
| `restore` | Sin filtro deleted_at (set `deleted_at = NULL`) | OK | line 99 | — |

### Query UseCase
**Archivo:** `src/library/dddpy/core_condominiums/usecase/condominium_query_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | Delegate con filtro | OK | line 16 | — |
| `get_by_uuid` | Delegate con filtro | OK | line 20 | — |
| `get_by_code` | Delegate con filtro | OK | line 24 | — |
| `get_by_name` | Delegate con filtro | OK | line 28 | — |
| `list_all` | Delegate con `include_deleted` | OK | line 32 | — |
| `get_by_id_any_status` | Helper post-mutación | OK | line 44 | — |

### UseCase (fachada)
**Archivo:** `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | `get_by_code` con filtro → valida no exista activo | OK | line 28 | — |
| `get_by_id` | Delegate | OK | line 43 | — |
| `get_by_uuid` | Delegate | OK | line 54 | — |
| `get_by_code` | Delegate | OK | line 65 | — |
| `update` | Pre-check `get_by_id` | OK | line 82 | — |
| `delete` | Pre-check + re-fetch any-status → `deleted_at` en respuesta | OK | line 97 | — |
| `restore` | Pre-check any-status + re-fetch any-status | OK | line 114 | — |
| `list_all` | Pasa `include_deleted` | OK | line 130 | — |

**Archivos tocados en `core_condominiums`:** ninguno (ya cumplía)

---

## `core_buildings`

### Query Repository
**Archivo:** `src/library/dddpy/core_buildings/infrastructure/building_query_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | `deleted_at IS NULL` | OK | line 20 | — |
| `get_by_uuid` | `deleted_at IS NULL` | OK | line 34 | — |
| `get_by_code_in_condominium` | `deleted_at IS NULL` | OK | line 48 | — |
| `list_all` | `include_deleted` param | OK | line 73 | — |
| `list_by_condominium` | `include_deleted` param | OK | line 105 | — |
| `count_active_units` | Raw SQL con `deleted_at IS NULL` | OK | line 135 | — |
| `_get_by_id_any_status` | Helper — **NUEVO** | FIXED | line 156 | Agregado para soportar post-mutación re-fetch |

### Cmd Repository
**Archivo:** `src/library/dddpy/core_buildings/infrastructure/building_cmd_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 29 | — |
| `update` | Sin filtro deleted_at | OK | line 63 | Usecase verifica pre-existencia |
| `soft_delete` | Sin filtro (set `deleted_at`) | OK | line 108 | — |
| `restore` | Sin filtro (set `deleted_at = NULL`) | OK | line 121 | — |
| `hard_delete` | Sin filtro (DELETE físico) | OK | line 132 | — |

### Query UseCase
**Archivo:** `src/library/dddpy/core_buildings/usecase/building_query_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | Delegate | OK | line 18 | — |
| `get_by_uuid` | Delegate | OK | line 23 | — |
| `get_by_code_in_condominium` | Delegate | OK | line 28 | — |
| `list_all` | Delegate `include_deleted` | OK | line 38 | — |
| `list_by_condominium` | Delegate `include_deleted` | OK | line 57 | — |
| `count_active_units` | Delegate | OK | line 73 | — |
| `get_by_id_any_status` | Helper — **NUEVO** | FIXED | line 77 | Agregado para soportar post-mutación |

### UseCase (fachada)
**Archivo:** `src/library/dddpy/core_buildings/usecase/building_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | `get_by_code_in_condominium` con filtro → valida no exista activo | OK | line 49 | — |
| `get_by_id` | Delegate | OK | line 71 | — |
| `get_by_uuid` | Delegate | OK | line 82 | — |
| `update` | Pre-check `get_by_id` | OK | line 100 | — |
| `delete` | Pre-check OK, pero **no retornaba estado real** | FIXED | line 117 | Ahora re-fetch con any-status y retorna `deleted_at` |
| `restore` | **No tenía pre-check de existencia**, usaba `get_by_id` post-restore (fallaba si falla restore) | FIXED | line 134 | Ahora usa `get_by_id_any_status` pre y post |
| `list_all` | Pasa `include_deleted` | OK | line 152 | — |
| `list_by_condominium` | Pasa `include_deleted` | OK | line 182 | — |
| `hard_delete` | Pre-check + re-fetch any-status | OK | line 206 | — |

**Archivos tocados en `core_buildings`:**
- `infrastructure/building_query_repository.py`
- `usecase/building_query_usecase.py`
- `usecase/building_usecase.py`

---

## `core_buildings_types`

### Query Repository
**Archivo:** `src/library/dddpy/core_buildings_types/infrastructure/building_type_query_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | `deleted_at IS NULL` | OK | line 23 | — |
| `get_by_uuid` | `deleted_at IS NULL` | OK | line 37 | — |
| `get_by_code_in_scope` | `deleted_at IS NULL` | OK | line 52 | — |
| `list_all` | `include_deleted` param | OK | line 80 | — |
| `count_references` | Raw SQL con `deleted_at IS NULL` | OK | line 128 | — |
| `get_active_in_scope` | `deleted_at IS NULL` + `status=1` | OK | line 143 | — |
| `_get_by_id_any_status` | Helper ya existía | OK | line 180 | — |

### Cmd Repository
**Archivo:** `src/library/dddpy/core_buildings_types/infrastructure/building_type_cmd_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 33 | — |
| `update` | Sin filtro deleted_at | OK | line 62 | — |
| `soft_delete` | Sin filtro (set `deleted_at`) | OK | line 90 | — |
| `restore` | Sin filtro (set `deleted_at = NULL`) | OK | line 109 | — |
| `hard_delete` | Sin filtro (DELETE físico) | OK | line 122 | — |

### Query UseCase
**Archivo:** `src/library/dddpy/core_buildings_types/usecase/building_type_query_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | Delegate | OK | line 28 | — |
| `get_by_uuid` | Delegate | OK | line 35 | — |
| `list_all` | Delegate `include_deleted` | OK | line 45 | — |
| `get_active_for_building_assignment` | Delegate | OK | line 64 | — |
| `get_by_id_any_status` | Helper ya existía | OK | line 90 | — |

### UseCase (fachada)
**Archivo:** `src/library/dddpy/core_buildings_types/usecase/building_type_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 40 | — |
| `get_by_id` | Delegate | OK | line 50 | — |
| `get_by_uuid` | Delegate | OK | line 58 | — |
| `list_all` | Pasa `include_deleted` | OK | line 68 | — |
| `update` | Delegate | OK | line 96 | — |
| `soft_delete` | `get_by_id_any_status` post-mutación ya estaba, pero **sin pre-check** | FIXED | line 132 | Ahora agrega pre-check + retorna `deleted_at` |
| `restore` | `get_by_id_any_status` post-mutación ya estaba, pero **sin pre-check** | FIXED | line 146 | Ahora agrega pre-check + re-fetch post-restore |
| `hard_delete` | Delegate | OK | line 163 | — |

**Archivos tocados en `core_buildings_types`:**
- `usecase/building_type_usecase.py`

---

## `core_unities`

### Query Repository
**Archivo:** `src/library/dddpy/core_unities/infrastructure/unity_query_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | `deleted_at IS NULL` | OK | line 20 | — |
| `get_by_uuid` | `deleted_at IS NULL` | OK | line 35 | — |
| `get_by_unit_number_in_building` | `deleted_at IS NULL` | OK | line 50 | — |
| `get_by_code_in_building` | `deleted_at IS NULL` | OK | line 72 | — |
| `list_all` | `include_deleted` param | OK | line 95 | — |
| `list_by_building` | `include_deleted` param | OK | line 128 | — |
| `count_active_residents` | Raw SQL con `deleted_at IS NULL` | OK | line 157 | — |
| `_get_by_id_any_status` | Helper — **NUEVO** | FIXED | line 185 | Agregado para post-mutación |

### Cmd Repository
**Archivo:** `src/library/dddpy/core_unities/infrastructure/unity_cmd_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 25 | — |
| `update` | Sin filtro deleted_at | OK | line 65 | Usecase verifica pre-existencia |
| `soft_delete` | Sin filtro (set `deleted_at`) | OK | line 122 | — |
| `restore` | Sin filtro (set `deleted_at = NULL`) | OK | line 133 | — |
| `hard_delete` | Sin filtro (DELETE físico) | OK | line 144 | — |

### Query UseCase
**Archivo:** `src/library/dddpy/core_unities/usecase/unity_query_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | Delegate | OK | line 21 | — |
| `get_by_uuid` | Delegate | OK | line 27 | — |
| `get_by_unit_number_in_building` | Delegate | OK | line 33 | — |
| `list_all` | Delegate `include_deleted` | OK | line 44 | — |
| `list_by_building` | Delegate `include_deleted` | OK | line 60 | — |
| `count_active_residents` | Delegate | OK | line 77 | — |
| `get_by_id_any_status` | Helper — **NUEVO** | FIXED | line 83 | Agregado para post-mutación |

### UseCase (fachada)
**Archivo:** `src/library/dddpy/core_unities/usecase/unity_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | `get_by_unit_number_in_building` con filtro | OK | line 46 | — |
| `get_by_id` | Delegate | OK | line 68 | — |
| `get_by_uuid` | Delegate | OK | line 79 | — |
| `update` | Pre-check `get_by_id` | OK | line 96 | — |
| `delete` | Pre-check OK, pero **no retornaba estado real** | FIXED | line 134 | Ahora re-fetch any-status + `deleted_at` |
| `restore` | **No tenía pre-check**, usaba `get_by_id` post-restore | FIXED | line 150 | Ahora pre-check any-status + re-fetch any-status |
| `list_all` | Pasa `include_deleted` | OK | line 169 | — |
| `list_by_building` | Pasa `include_deleted` | OK | line 195 | — |
| `hard_delete` | Pre-check `get_by_id` | OK | line 217 | — |

**Archivos tocados en `core_unities`:**
- `infrastructure/unity_query_repository.py`
- `usecase/unity_query_usecase.py`
- `usecase/unity_usecase.py`

---

## `core_unities_types`

### Query Repository
**Archivo:** `src/library/dddpy/core_unities_types/infrastructure/unity_type_query_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | `deleted_at IS NULL` | OK | line 23 | — |
| `get_by_uuid` | `deleted_at IS NULL` | OK | line 37 | — |
| `get_by_code_in_scope` | `deleted_at IS NULL` | OK | line 52 | — |
| `list_all` | `include_deleted` param | OK | line 79 | — |
| `count_references` | Raw SQL con `deleted_at IS NULL` | OK | line 126 | — |
| `get_active_in_scope` | `deleted_at IS NULL` + `status=1` | OK | line 141 | — |
| `_get_by_id_any_status` | Helper ya existía | OK | line 176 | — |

### Cmd Repository
**Archivo:** `src/library/dddpy/core_unities_types/infrastructure/unity_type_cmd_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 32 | — |
| `update` | Sin filtro deleted_at | OK | line 62 | — |
| `soft_delete` | Sin filtro (set `deleted_at`) | OK | line 96 | — |
| `restore` | Sin filtro (set `deleted_at = NULL`) | OK | line 114 | — |
| `hard_delete` | Sin filtro (DELETE físico) | OK | line 128 | — |

### Query UseCase
**Archivo:** `src/library/dddpy/core_unities_types/usecase/unity_type_query_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | Delegate | OK | line 30 | — |
| `get_by_uuid` | Delegate | OK | line 37 | — |
| `list_all` | Delegate `include_deleted` | OK | line 47 | — |
| `get_active_for_unity_assignment` | Delegate | OK | line 63 | — |
| `get_by_id_any_status` | Helper ya existía | OK | line 93 | — |

### UseCase (fachada)
**Archivo:** `src/library/dddpy/core_unities_types/usecase/unity_type_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 41 | — |
| `get_by_id` | Delegate | OK | line 50 | — |
| `get_by_uuid` | Delegate | OK | line 58 | — |
| `update` | Delegate | OK | line 67 | — |
| `soft_delete` | `get_by_id_any_status` post-mutación ya estaba, pero **sin pre-check** | FIXED | line 104 | Ahora pre-check + `deleted_at` en respuesta |
| `restore` | `get_by_id_any_status` post-mutación ya estaba, pero **sin pre-check** | FIXED | line 118 | Ahora pre-check any-status + re-fetch post |
| `hard_delete` | Delegate | OK | line 135 | — |
| `list_all` | Pasa `include_deleted` | OK | line 142 | — |
| `validate_for_unity_assignment` | Delegate | OK | line 173 | — |

**Archivos tocados en `core_unities_types`:**
- `usecase/unity_type_usecase.py`

---

## Queries Huérfanas (sin filtro `deleted_at`)

Inspeccionadas todas las queries SQL crudas / raw queries:

| Módulo | Query | Archivo | ¿Filtro `deleted_at`? | Estado |
|---|---|---|---|---|
| `core_buildings` | `count_active_units` raw SQL | `building_query_repository.py` | ✅ `deleted_at IS NULL` | OK |
| `core_buildings_types` | `count_references` raw SQL | `building_type_query_repository.py` | ✅ `deleted_at IS NULL` | OK |
| `core_unities` | `count_active_residents` raw SQL | `unity_query_repository.py` | ✅ `deleted_at IS NULL` | OK |
| `core_unities_types` | `count_references` raw SQL | `unity_type_query_repository.py` | ✅ `deleted_at IS NULL` | OK |

**Resultado:** Sin queries huérfanas. ✅

---

## Resumen de Fixes Aplicados

| # | Módulo | Archivo | Método | Problema | Fix |
|---|---|---|---|---|---|
| 1 | `core_buildings` | `building_query_repository.py` | `_get_by_id_any_status` | Método no existía | Agregado |
| 2 | `core_buildings` | `building_query_usecase.py` | `get_by_id_any_status` | Método no existía | Agregado |
| 3 | `core_buildings` | `building_usecase.py` | `delete` | No retornaba `deleted_at` real | Re-fetch any-status post-mutación |
| 4 | `core_buildings` | `building_usecase.py` | `restore` | Sin pre-check; re-fetch con filtro wrong | Pre-check any-status + re-fetch any-status |
| 5 | `core_unities` | `unity_query_repository.py` | `_get_by_id_any_status` | Método no existía | Agregado |
| 6 | `core_unities` | `unity_query_usecase.py` | `get_by_id_any_status` | Método no existía | Agregado |
| 7 | `core_unities` | `unity_usecase.py` | `delete` | No retornaba `deleted_at` real | Re-fetch any-status post-mutación |
| 8 | `core_unities` | `unity_usecase.py` | `restore` | Sin pre-check; re-fetch con filtro wrong | Pre-check any-status + re-fetch any-status |
| 9 | `core_buildings_types` | `building_type_usecase.py` | `soft_delete` | Sin pre-check; no `deleted_at` en respuesta | Pre-check + re-fetch any-status |
| 10 | `core_buildings_types` | `building_type_usecase.py` | `restore` | Sin pre-check | Pre-check + re-fetch post |
| 11 | `core_unities_types` | `unity_type_usecase.py` | `soft_delete` | Sin pre-check; no `deleted_at` en respuesta | Pre-check + re-fetch any-status |
| 12 | `core_unities_types` | `unity_type_usecase.py` | `restore` | Sin pre-check | Pre-check + re-fetch post |

---

## Resultado Final

| Módulo | Métodos OK | Métodos FIXED | Queries OK | Status |
|---|---|---|---|---|
| `core_condominiums` | 24 | 0 | 0 | ✅ Cumplía |
| `core_buildings` | 19 | 4 | 1 | ✅ Corregido |
| `core_buildings_types` | 16 | 2 | 1 | ✅ Corregido |
| `core_unities` | 19 | 4 | 1 | ✅ Corregido |
| `core_unities_types` | 17 | 2 | 1 | ✅ Corregido |
| **TOTAL** | **95** | **12** | **4** | **✅ HOMOLOGADO** |
