# Phase 1 Module Review — 2026-04-14
**Reviewer:** Bulma S · **Repo:** `/home/miguel/servers/condo-py`
**Modules:** `core_condominiums`, `core_buildings`, `core_buildings_types`, `core_unities`, `core_unities_types`

---

## Eje 1: Disciplina de Capas
## Eje 2: Consistencia de Soft Delete
## Eje 3: Tipado Explícito
## Eje 4: Dominio
## Eje 5: Patrón DDD

---

## Resumen Ejecutivo

Los módulos Phase 1 muestran una base arquitectónica sólida con separación clara de capas, repositories con contratos abstractos, cmd/query usecases y entidades con comportamiento. El mayor problema encontrado es un **violación de tipado crítica** en `core_condominiums` que rompe Eje 3 de forma silenciosa.

---

## 🔴 Módulo: `core_condominiums` (PATRÓN)

### Estructura de archivos
```
core_condominiums/
├── domain/
│   ├── condominium_entity.py       ← entidad
│   ├── condominium_exception.py    ← excepciones semánticas
│   ├── condominium_repository.py   ← ABC mixto (cmd+query)
│   ├── condominium_cmd_repository.py
│   ├── condominium_query_repository.py
│   ├── condominium_data.py        ← frozen dataclasses
│   └── condominium_success.py
├── infrastructure/
│   ├── condominium_cmd_repository.py
│   ├── condominium_query_repository.py
│   ├── condominium_mapper.py
│   └── dbcondominiums.py
└── usecase/
    ├── condominium_usecase.py      ← FACADE
    ├── condominium_cmd_usecase.py
    ├── condominium_query_usecase.py
    ├── condominium_factory.py
    └── condominium_cmd_schema.py
```

---

### Eje 1 — Disciplina de Capas: ⚠️ 3/5

| Criterio | Estado | Notas |
|---|---|---|
| Facade no toca infraestructura | ⚠️ | `CondominiumUseCase.restore()` accede directo a `repository.restore()` — rompe Eje 1 |
| Repos no devuelven `object` | ❌ | **CRÍTICO: `CondominiumQueryRepositoryImpl` devuelve `Optional[object]`** |
| Cmd/Query orquestan lógica | ✅ | Separation CMD/QUERY bien respetada |

**Problemas:**

**ISSUE-C1-HIGH — `CondominiumQueryRepositoryImpl` return type `Optional[object]`**
- **Path:** `src/library/dddpy/core_condominiums/infrastructure/condominium_query_repository.py`
- **Líneas:** 22, 35, 48, 61
- **Evidencia:**
```python
# Línea 22
def get_by_id(self, id: int) -> Optional[object]:   # ← DEBE SER Optional[CondominiumEntity]

# Línea 35
def get_by_uuid(self, uuid: str) -> Optional[object]:  # ← DEBE SER Optional[CondominiumEntity]

# Línea 48
def get_by_code(self, code: str) -> Optional[object]:  # ← DEBE SER Optional[CondominiumEntity]

# Línea 61
def get_by_name(self, name: str) -> Optional[object]:  # ← DEBE SER Optional[CondominiumEntity]
```
- **Impacto:** El contrato de dominio declara `Optional[CondominiumEntity]` pero la implementación infra devuelve `Optional[object]`. Esto rompe polimorfismo y any() en herramientas de análisis estático.
- **Acción:** Cambiar `Optional[object]` → `Optional[CondominiumEntity]` en las 4 firmas y en `list_all`.

**ISSUE-C2-MED — `restore()` accede a infraestructura sin pasar por cmd_usecase**
- **Path:** `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py`
- **Línea:** 118
- **Evidencia:**
```python
def restore(self, id: int):
    ...
    restored = self.condominium_cmd_usecase.repository.restore(id)  # ← toca infra directo
```
- **Acción:** Exponer `restore()` en `CondominiumCmdUseCase` y llamar desde allí.

---

### Eje 2 — Soft Delete: ⚠️ 4/5

| Criterio | Estado | Notas |
|---|---|---|
| `get_by_*` excluye eliminados | ✅ | `list_all` excluye por defecto; `get_by_*` no filtra — inconsistente |
| `list_all` tiene `include_deleted` | ✅ | Puerta explícita correcta |
| `delete/restore` estado real | ❌ | `restore` retorna estado anterior al soft delete, no estado post-restore |

**ISSUE-C3-HIGH — `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name` no filtran eliminados**
- **Path:** `src/library/dddpy/core_condominiums/infrastructure/condominium_query_repository.py`
- Las queries en `get_by_id` (línea 22), `get_by_uuid`, `get_by_code`, `get_by_name` NO aplican `deleted_at IS NULL`. Un registro soft-deleteado se sigue encontrando por estos métodos.
- **Contraste con `core_buildings` y `core_unities`:** estos SÍ filtran `deleted_at.is_(None)` correctamente.
- **Acción:** Agregar `.filter(DBCondominiums.deleted_at.is_(None))` a las 4 queries `get_by_*`.

**ISSUE-C4-MED — `delete` retorna `deleted_at` anterior en lugar de estado post-operación**
- **Path:** `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py`, línea 100
- **Evidencia:**
```python
def delete(self, id: int):
    existing = self.condominium_query_usecase.get_by_id(id)  # deleted_at antes del delete
    ...
    data={"id": id, "deleted_at": existing.deleted_at}  # ← devuelve estado ANTES de la operación
```
- **Acción:** Retornar `{"id": id, "deleted_at": <nuevo_deleted_at>}` real post-operación.

---

### Eje 3 — Tipado Explícito: ⚠️ 2/5

| Criterio | Estado | Notas |
|---|---|---|
| Sin `Optional[object]` | ❌ | CRÍTICO: 4 métodos devolviendo `Optional[object]` |
| Entidades bien definidas | ✅ | `CondominiumEntity` definida correctamente |
| Query results tipados | ⚠️ | `list_all` retorna `tuple[List[object], int]` — debería ser `tuple[List[CondominiumEntity], int]` |

**ISSUE-C5-HIGH — Mismo issue de C1 propagado a `list_all`**
- **Path:** `src/library/dddpy/core_condominiums/infrastructure/condominium_query_repository.py`, línea 70
```python
def list_all(...) -> tuple[List[object], int]:  # ← DEBE SER tuple[List[CondominiumEntity], int]
```

---

### Eje 4 — Dominio: ✅ 4/5

| Criterio | Estado | Notas |
|---|---|---|
| Entidades con comportamiento | ✅ | `to_dict()`, `is_deleted()`, `is_active()` |
| Invariantes en dominio | ⚠️ | `_validate_invariants()` existe pero nunca se llama |
| Excepciones semánticas | ✅ | 3 excepciones con semántica clara |

**ISSUE-C6-LOW — `_validate_invariants()` nunca se invoca**
- `CondominiumEntity` tiene `_validate_invariants()` con validaciones de negocio, pero no se llama en el constructor ni en los factory methods.
- **Acción:** Llamar `_validate_invariants()` en el constructor post-asignación de campos.

---

### Eje 5 — Patrón DDD: ⚠️ 4/5

| Criterio | Estado | Notas |
|---|---|---|
| Contracts bien definidos | ✅ | ABCs con contratos abstractos |
| cmd/query separados | ✅ | `CondominiumCmdUseCase` / `CondominiumQueryUseCase` separados |
| Infraestructura aislada | ⚠️ | Issue C2 (restore toca infra) |

---

### Summary: `core_condominiums`

| Eje | Score | Issues |
|---|---|---|
| 1. Disciplina de Capas | 3/5 | C1 (HIGH), C2 (MED) |
| 2. Soft Delete | 4/5 | C3 (HIGH), C4 (MED) |
| 3. Tipado Explícito | 2/5 | C1 (HIGH), C5 (HIGH) |
| 4. Dominio | 4/5 | C6 (LOW) |
| 5. Patrón DDD | 4/5 | C2 (MED) |

---

## 🟡 Módulo: `core_buildings`

### Estructura de archivos
```
core_buildings/
├── domain/
│   ├── building_entity.py
│   ├── building_exception.py
│   ├── building_repository.py  ← ABC mixto (legacy)
│   ├── building_cmd_repository.py
│   ├── building_query_repository.py
│   ├── building_data.py
│   └── building_success.py
├── infrastructure/
│   ├── building_cmd_repository.py
│   ├── building_query_repository.py
│   ├── building_mapper.py
│   └── dbbuildings.py
└── usecase/
    ├── building_usecase.py
    ├── building_cmd_usecase.py
    ├── building_query_usecase.py
    ├── building_factory.py
    └── building_cmd_schema.py
```

---

### Eje 1 — Disciplina de Capas: ✅ 4/5

- **Cmd/Query separation:** correcta (`BuildingCmdUseCase` / `BuildingQueryUseCase`)
- **`count_active_units` en raw SQL:** evita dependencia circular con `core_unities` — solución elegante
- **⚠️ `BuildingUseCase` facade toca queries de tipos dentro del mismo use case:** `_enrich_building_with_type()` hace llamada a `BuildingTypeUseCase().get_by_id()` dentro del facade. Esto no es touch de infra pero sí crea acoplamiento cross-module en el facade. Acceptable por ahora.

**ISSUE-B1-MED — `BuildingUseCase` no tiene método `restore` implementado**
- El `BuildingCmdUseCase` tiene `restore()`, pero `BuildingUseCase` facade no lo expone como endpoint público (solo `delete` y `hard_delete`).

---

### Eje 2 — Soft Delete: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| `get_by_*` excluye eliminados | ✅ | `get_by_id`, `get_by_uuid`, `get_by_code_in_condominium` todos filtran `deleted_at IS NULL` |
| `list_all` tiene `include_deleted` | ✅ | Puerta explícita correcta |
| `delete/restore` estado real | ✅ | `soft_delete` y `restore` operan correctamente |

---

### Eje 3 — Tipado Explícito: ✅ 5/5

- Todos los métodos de repository devuelven tipos explícitos (`Optional[BuildingEntity]`, `tuple[List[BuildingEntity], int]`)
- Entidades bien definidas con `to_dict()`, `is_deleted()`, `is_active()`
- Sin retornos genéricos

---

### Eje 4 — Dominio: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| Entidades con comportamiento | ✅ | `_validate_invariants()`, `is_deleted()`, `is_active()` |
| Invariantes en dominio | ✅ | Validaciones: built_area ≥ 0, coefficient 0-100, floors ≥ 0, etc. |
| Excepciones semánticas | ✅ | 6 excepciones: `BuildingNotFound`, `RepeatedBuildingCode`, `BuildingHasActiveUnits`, etc. |

**Notable:** `BuildingEntity._validate_invariants()` se ejecuta automáticamente en el constructor y valida todas las reglas de negocio.

---

### Eje 5 — Patrón DDD: ✅ 5/5

- Contracts (ABCs) bien definidos: `BuildingRepository`, `BuildingCmdRepository`, `BuildingQueryRepository`
- `cmd`/`query` separados en 3 capas: domain contracts → infrastructure impl → usecase
- Infraestructura limpiamente aislada
- **Legacy `BuildingRepository` ABC mixto persiste** (`domain/building_repository.py`) pero no se usa en código activo. Debería marcarse como deprecated o eliminarse.

---

### Summary: `core_buildings`

| Eje | Score | Issues |
|---|---|---|
| 1. Disciplina de Capas | 4/5 | B1 (MED) |
| 2. Soft Delete | 5/5 | — |
| 3. Tipado Explícito | 5/5 | — |
| 4. Dominio | 5/5 | — |
| 5. Patrón DDD | 5/5 | Legacy ABC残余 (LOW) |

**Acción recomendada:** Agregar método `restore()` al facade `BuildingUseCase`.

---

## 🟡 Módulo: `core_buildings_types`

### Estructura de archivos
```
core_buildings_types/
├── domain/
│   ├── building_type_entity.py
│   ├── building_type_exception.py
│   ├── building_type_repository.py  ← ABC muy minimalista (solo find_by_id, find_by_uuid)
│   ├── building_type_cmd_repository.py
│   ├── building_type_query_repository.py
│   ├── building_type_data.py
│   └── building_type_success.py
├── infrastructure/
│   ├── building_type_cmd_repository.py
│   ├── building_type_query_repository.py
│   ├── building_type_mapper.py
│   └── dbbuildingtype.py
└── usecase/
    ├── building_type_usecase.py
    ├── building_type_cmd_usecase.py
    ├── building_type_query_usecase.py
    ├── building_type_factory.py
    └── building_type_cmd_schema.py
```

---

### Eje 1 — Disciplina de Capas: ⚠️ 4/5

**ISSUE-BT1-LOW — `BuildingTypeUseCase` no tiene cmd/query separation**
- `BuildingTypeUseCase` usa `self._cmd_usecase` y `self._query_usecase` internamente pero NO expone métodos `create/update/delete/restore` diferenciados como cmd/query.
- Todos los métodos públicos (create, get_by_id, list_all, update, soft_delete, restore, hard_delete) están en el MISMO facade.
- El `BuildingTypeCmdUseCase` y `BuildingTypeQueryUseCase` EXISTEN pero `BuildingTypeUseCase` no los usa como fachada diferenciada — los usa como helpers internos.
- **No rompe funcionalidad**, pero no es el patrón cmd/query diferenciado que se pide en Eje 5.

---

### Eje 2 — Soft Delete: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| `get_by_*` excluye eliminados | ✅ | `get_by_id`, `get_by_uuid`, `get_by_code_in_scope` filtran `deleted_at IS NULL` |
| `list_all` tiene `include_deleted` | ✅ | Puerta explícita correcta |
| `delete/restore` estado real | ✅ | `soft_delete`/`restore` operan correctamente |

---

### Eje 3 — Tipado Explícito: ✅ 5/5

- Todos los retornos tipados explícitamente
- Excepciones rich en semántica (10 clases de excepciones con mensajes contextualizados)
- `is_global` / `is_custom` como properties del dominio

---

### Eje 4 — Dominio: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| Entidades con comportamiento | ✅ | `_validate_invariants()`, `is_deleted()`, `is_active()`, `can_be_modified()`, `can_be_deleted()`, `is_global`, `is_custom` |
| Invariantes en dominio | ✅ | Validación de `sort_order ≥ 0` |
| Excepciones semánticas | ✅ | 10 excepciones con semántica precisa y codes 400-422 diferenciados |

**Destacado:** Módulo con mejor diseño de excepciones del set Phase 1.

---

### Eje 5 — Patrón DDD: ⚠️ 4/5

- Domain contracts: `BuildingTypeRepository`, `BuildingTypeCmdRepository`, `BuildingTypeQueryRepository` ✅
- **Problema:** `BuildingTypeUseCase` es un solo facade que consume ambos cmd/query usecases internamente. El patrón cmd/query diferenciado no se refleja en la interfaz pública — todas las operaciones (cmd y query) están en el mismo facade.

**ISSUE-BT2-LOW — `BuildingTypeRepository` (ABC mixto) no se usa**
- Existe solo con `find_by_id` y `find_by_uuid`. No es usado por código activo — podría eliminarse.

---

### Summary: `core_buildings_types`

| Eje | Score | Issues |
|---|---|---|
| 1. Disciplina de Capas | 4/5 | BT1 (LOW) |
| 2. Soft Delete | 5/5 | — |
| 3. Tipado Explícito | 5/5 | — |
| 4. Dominio | 5/5 | — |
| 5. Patrón DDD | 4/5 | BT1 (LOW), BT2 (LOW) |

**Acción recomendada:** Considerar separar `BuildingTypeQueryUseCase` como fachada Query pública y `BuildingTypeCmdUseCase` como fachada CMD pública, similar a como está estructurado `core_buildings`.

---

## 🟡 Módulo: `core_unities`

### Estructura de archivos
```
core_unities/
├── domain/
│   ├── unity_entity.py
│   ├── unity_exception.py
│   ├── unity_repository.py  ← ABC mixto (legacy)
│   ├── unity_cmd_repository.py
│   ├── unity_query_repository.py
│   ├── unity_data.py
│   └── unity_success.py
├── infrastructure/
│   ├── unity_cmd_repository.py
│   ├── unity_query_repository.py
│   ├── unity_mapper.py
│   └── dbunities.py
└── usecase/
    ├── unity_usecase.py
    ├── unity_cmd_usecase.py
    ├── unity_query_usecase.py
    ├── unity_factory.py
    └── unity_cmd_schema.py
```

---

### Eje 1 — Disciplina de Capas: ✅ 4/5

- `UnityCmdUseCase` / `UnityQueryUseCase` separados correctamente
- `_enrich_unity_with_type()` dentro del facade crea acoplamiento con `core_unities_types` — aceptable por necesidad de enriquecer respuestas, pero podría moverse a un projector/assembler
- **`_validate_building()` usa `BuildingUseCase().get_by_id()`** — esto crea importación dinámica de todo el modulo `core_buildings`. Funcional pero pesado para una simple validación de existencia.

---

### Eje 2 — Soft Delete: ⚠️ 4/5

| Criterio | Estado | Notas |
|---|---|---|
| `get_by_*` excluye eliminados | ✅ | `get_by_id`, `get_by_uuid` filtran `deleted_at IS NULL` |
| `get_by_unit_number_in_building` | ⚠️ | **NO filtra `deleted_at`** — puede devolver unidad eliminada |
| `get_by_code_in_building` | ⚠️ | **NO filtra `deleted_at`** — puede devolver código duplicado de unidad eliminada |
| `list_all` tiene `include_deleted` | ✅ | Puerta correcta |
| `delete/restore` estado real | ✅ | Correcto |

**ISSUE-U1-HIGH — `get_by_unit_number_in_building` no filtra `deleted_at`**
- **Path:** `src/library/dddpy/core_unities/infrastructure/unity_query_repository.py`, líneas 52-68
- Falta `.filter(DBUnities.deleted_at.is_(None))` en la query de `get_by_unit_number_in_building`
- Impacto: al restaurar una unidad y crear otra con el mismo número, el check de duplicado puede pasar por alto la unidad eliminada con mismo número en estado "deleted" en DB.

**ISSUE-U2-HIGH — `get_by_code_in_building` no filtra `deleted_at`**
- **Path:** `src/library/dddpy/core_unities/infrastructure/unity_query_repository.py`, líneas 70-85
- Mismo problema que U1 para el campo `code`.

---

### Eje 3 — Tipado Explícito: ✅ 5/5

- Todos los retornos tipados con `UnityEntity`
- `UnityEntity` bien definida con constants `VALID_OCCUPANCY_STATUSES`
- Sin retornos genéricos

---

### Eje 4 — Dominio: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| Entidades con comportamiento | ✅ | `_validate_invariants()`, `is_deleted()`, `is_active()`, `VALID_OCCUPANCY_STATUSES` |
| Invariantes en dominio | ✅ | Valida `private_area ≥ 0`, `coefficient 0-100`, `occupancy_status` válido |
| Excepciones semánticas | ✅ | 8 excepciones con semántica clara |

**Destacado:** `UnityEntity.VALID_OCCUPANCY_STATUSES` como class constant es buena práctica.

---

### Eje 5 — Patrón DDD: ⚠️ 4/5

- Domain contracts correctos: `UnityRepository`, `UnityCmdRepository`, `UnityQueryRepository`
- **Legacy `UnityRepository` ABC mixto** persiste sin uso activo
- `count_active_residents()` usa raw SQL con check de tabla existente — buena estrategia defensiva

---

### Summary: `core_unities`

| Eje | Score | Issues |
|---|---|---|
| 1. Disciplina de Capas | 4/5 | — |
| 2. Soft Delete | 4/5 | U1 (HIGH), U2 (HIGH) |
| 3. Tipado Explícito | 5/5 | — |
| 4. Dominio | 5/5 | — |
| 5. Patrón DDD | 4/5 | Legacy ABC残余 (LOW) |

**Acción recomendada:** Agregar `deleted_at IS NULL` a `get_by_unit_number_in_building` y `get_by_code_in_building`.

---

## 🟡 Módulo: `core_unities_types`

### Estructura de archivos
```
core_unities_types/
├── domain/
│   ├── unity_type_entity.py
│   ├── unity_type_exception.py
│   ├── unity_type_repository.py  ← ABC minimalista
│   ├── unity_type_cmd_repository.py
│   ├── unity_type_query_repository.py
│   ├── unity_type_data.py
│   └── unity_type_success.py
├── infrastructure/
│   ├── unity_type_cmd_repository.py
│   ├── unity_type_query_repository.py
│   ├── unity_type_mapper.py
│   └── dbunitytype.py
└── usecase/
    ├── unity_type_usecase.py
    ├── unity_type_cmd_usecase.py
    ├── unity_type_query_usecase.py
    ├── unity_type_factory.py
    └── unity_type_cmd_schema.py
```

---

### Eje 1 — Disciplina de Capas: ⚠️ 4/5

**ISSUE-UT1-LOW — Mismo patrón que `core_buildings_types`**: `UnityTypeUseCase` consume `_cmd` y `_query` internamente pero no expone interfaces cmd/query diferenciadas. Todas las operaciones (cmd y query) en el mismo facade.

---

### Eje 2 — Soft Delete: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| `get_by_*` excluye eliminados | ✅ | `get_by_id`, `get_by_uuid`, `get_by_code_in_scope` filtran `deleted_at IS NULL` |
| `list_all` tiene `include_deleted` | ✅ | Puerta correcta |
| `delete/restore` estado real | ✅ | Correcto |

---

### Eje 3 — Tipado Explícito: ✅ 5/5

- Retornos tipados con `UnityTypeEntity`
- `is_global` / `is_custom` como properties

---

### Eje 4 — Dominio: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| Entidades con comportamiento | ✅ | `_validate_invariants()`, `is_deleted()`, `is_active()`, `can_be_modified()`, `can_be_deleted()`, `is_global`, `is_custom` |
| Invariantes en dominio | ✅ | Valida `sort_order ≥ 0` |
| Excepciones semánticas | ✅ | 9 excepciones con codes 400-422 diferenciados |

**Notable:** `usage_class` como campo de dominio adicional muestra expansión correcta del modelo.

---

### Eje 5 — Patrón DDD: ⚠️ 4/5

- Domain contracts correctos: `UnityTypeRepository`, `UnityTypeCmdRepository`, `UnityTypeQueryRepository`
- Mismo issue que `core_buildings_types` con el facade unify
- `get_active_in_scope()` es un método de query con semántica de validación — buen diseño

---

### Summary: `core_unities_types`

| Eje | Score | Issues |
|---|---|---|
| 1. Disciplina de Capas | 4/5 | UT1 (LOW) |
| 2. Soft Delete | 5/5 | — |
| 3. Tipado Explícito | 5/5 | — |
| 4. Dominio | 5/5 | — |
| 5. Patrón DDD | 4/5 | UT1 (LOW) |

---

## 📋 Issues Priorizados

### 🔴 HIGH (deben resolverse en Sprint 1)

| ID | Módulo | Description |
|---|---|---|
| C1 | `condominiums` | `CondominiumQueryRepositoryImpl` devuelve `Optional[object]` en 4 métodos en lugar de `Optional[CondominiumEntity]` |
| C3 | `condominiums` | `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name` no filtran `deleted_at IS NULL` — soft delete inconsistente |
| C5 | `condominiums` | `list_all` devuelve `tuple[List[object], int]` — debería ser tipado con `CondominiumEntity` |
| U1 | `unities` | `get_by_unit_number_in_building` no filtra `deleted_at` — puede devolver unidad eliminada |
| U2 | `unities` | `get_by_code_in_building` no filtra `deleted_at` — puede devolver código duplicado de unidad eliminada |

### 🟡 MEDIUM (deben resolverse en Sprint 2)

| ID | Módulo | Description |
|---|---|---|
| C2 | `condominiums` | `CondominiumUseCase.restore()` toca infraestructura directamente (`repository.restore`) sin pasar por `cmd_usecase` |
| C4 | `condominiums` | `delete()` retorna `deleted_at` anterior en data response — debe retornar el nuevo estado post-operación |

### 🟢 LOW (deben resolverse en Sprint 3-4)

| ID | Módulo | Description |
|---|---|---|
| B1 | `buildings` | `BuildingUseCase` no expone método `restore()` público |
| C6 | `condominiums` | `_validate_invariants()` existe en `CondominiumEntity` pero nunca se invoca |
| BT1 | `buildings_types` | `BuildingTypeUseCase` facade unificado — cmd/query separados pero no expuestos como fachadas diferenciadas |
| BT2 | `buildings_types` | `BuildingTypeRepository` ABC legacy sin uso activo |
| UT1 | `unities_types` | `UnityTypeUseCase` mismo issue que BT1 |

### ⚪ LEGACY CLEANUP (Sprint 4+)

| ID | Módulo | Description |
|---|---|---|
| L1 | `buildings` | `BuildingRepository` ABC mixto sin uso activo |
| L2 | `unities` | `UnityRepository` ABC mixto sin uso activo |

---

## 📊 Matriz de Cumplimiento por Módulo

| Módulo | Eje 1 | Eje 2 | Eje 3 | Eje 4 | Eje 5 | Score Global |
|---|---|---|---|---|---|---|
| `core_condominiums` | 3/5 | 4/5 | 2/5 | 4/5 | 4/5 | **17/25** ⚠️ |
| `core_buildings` | 4/5 | 5/5 | 5/5 | 5/5 | 5/5 | **24/25** ✅ |
| `core_buildings_types` | 4/5 | 5/5 | 5/5 | 5/5 | 4/5 | **23/25** ✅ |
| `core_unities` | 4/5 | 4/5 | 5/5 | 5/5 | 4/5 | **22/25** ✅ |
| `core_unities_types` | 4/5 | 5/5 | 5/5 | 5/5 | 4/5 | **23/25** ✅ |

---

## Recomendaciones de Acción

### `core_condominiums` (prioridad CRÍTICA)
1. Corregir tipos de retorno de `CondominiumQueryRepositoryImpl` (`Optional[object]` → `Optional[CondominiumEntity]`) — **alto impacto en type safety**
2. Agregar `.filter(deleted_at.is_(None))` a `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name`
3. Exponer `restore()` en `CondominiumCmdUseCase` y redirigir desde el facade
4. Hacer que `delete()` retorne el `deleted_at` real post-operación
5. Llamar `_validate_invariants()` en el constructor

### `core_buildings`
1. Agregar `restore()` al facade `BuildingUseCase`

### `core_buildings_types`
1. Evaluar separar `BuildingTypeQueryUseCase` y `BuildingTypeCmdUseCase` como fachadas públicas diferenciadas (opcional — actualmente funcional)

### `core_unities`
1. Agregar `.filter(DBUnities.deleted_at.is_(None))` a `get_by_unit_number_in_building` y `get_by_code_in_building`

### `core_unities_types`
1. Mismo refinamiento de cmd/query facade separation que `core_buildings_types` (opcional)

### Limpieza general (Sprint 4+)
1. Eliminar `BuildingRepository`, `UnityRepository` ABC legacy sin uso activo
