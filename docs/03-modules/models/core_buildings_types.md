---
type: db-table
system: condominios
status: active
tags:
  - database
  - catalog
  - scope
  - ddd
---

# 🗄️ Tabla: `core_buildings_types`

## 📝 Descripción

Catálogo de tipos de edificios con soporte para **alcance (scope)**:

- **Global (`condominium_id = NULL`)**: tipos disponibles para todos los condominios. Reservados para el sistema (`is_system = 1`). No editables ni eliminables por usuarios.
- **Custom (`condominium_id = [id]`)**: tipos privados de un condominio específico. Creados, editados y eliminables (soft delete) por administradores del condominio.

---

## 🏗️ Estructura (post-migración 006)

| Campo | Tipo | Nullable | Default | Descripción |
|-------|------|----------|---------|-------------|
| `id` | `BIGINT` | NO | auto | PK |
| `uuid` | `CHAR(36)` | NO | `UUID()` | Identificador único universal |
| `condominium_id` | `BIGINT` | **YES** | `NULL` | FK al condominio. `NULL` = global/sistema |
| `code` | `VARCHAR(50)` | NO | — | Código interno (único **por scope**) |
| `name` | `VARCHAR(255)` | NO | — | Nombre del tipo |
| `description` | `TEXT` | YES | `NULL` | Descripción detallada |
| `is_system` | `SMALLINT` | NO | `0` | `1` = tipo de sistema (global, no editable) |
| `sort_order` | `INT` | NO | `0` | Orden de aparición en listados |
| `status` | `INT` | NO | `1` | `1` = activo, `0` = inactivo |
| `deleted_at` | `DATETIME` | YES | `NULL` | Soft delete (si no es `NULL`, está eliminado) |
| `created_at` | `DATETIME` | NO | `CURRENT_TIMESTAMP` | Fecha de creación |
| `updated_at` | `DATETIME` | NO | `CURRENT_TIMESTAMP ON UPDATE` | Última actualización |

---

## 🔍 Índices y Foreign Keys

| Índice | Columnas | Tipo | Notas |
|--------|----------|------|-------|
| `ix_core_buildings_types_condominium_code` | `(condominium_id, code)` | Index | Búsqueda por scope |
| `fk_buildings_types_condominium` | `condominium_id → core_condominiums(id)` | FK | `ON DELETE SET NULL`, `ON UPDATE CASCADE` |

### Notas sobre unicidad

MySQL no soporta índices parciales/filtados. La restricción de unicidad por scope `(condominium_id, code)` para registros **activos** se maneja en la **capa de aplicación** (método `get_by_code_in_scope()` en el query repository).

Un registro soft-deleted con el mismo `(condominium_id, code)` que uno activo **no viola la restricción** a nivel de índice — la aplicación verifica esto al restaurar.

### Foreign Key: `core_buildings.building_type_id`

```sql
ON DELETE SET NULL    -- Si se elimina un tipo, los edificios quedan sin tipo (tipo=null)
ON UPDATE CASCADE    -- Si cambia el PK del tipo, se actualiza automáticamente en edificios
```

---

## 🔗 Relaciones

```text
core_buildings_types
├── 1 ← ∞ core_buildings (building_type_id)
└── 0/1 → core_condominiums (condominium_id)
```

---

## 🚫 Reglas de negocio

| Regla | Detalle |
|-------|---------|
| Global ≠ editable | Tipos con `is_system = 1` (`condominium_id = NULL`) no se pueden modificar ni eliminar |
| Custom por condominio | Tipos custom solo son accesibles desde el condominio que los creó |
| Código único por scope | No puede haber dos tipos activos con el mismo `code` dentro del mismo `condominium_id` |
| Soft delete reversible | `deleted_at` permite recuperación; el hard delete está bloqueado si hay edificios referenciando |
| Tipos inactivos no usables | Un edificio no puede asignarse a un tipo con `status = 0` |
| Asignación a edificios | Un edificio solo puede usar tipos globales o custom del mismo condominio |

---

## 📦 Tipos base (seed, migraciones 003 y 006)

| Code | Name | Scope | is_system |
|------|------|-------|-----------|
| `RESIDENTIAL` | Residencial | Global | 1 |
| `COMMERCIAL` | Comercial | Global | 1 |
| `MIXED` | Mixto | Global | 1 |
| `SERVICES` | Servicios | Global | 1 |

Seed idempotente: migraciones 003 y 006 usan `INSERT ... ON DUPLICATE KEY UPDATE`.

---

## 🔄 Migraciones relevantes

| Migración | Cambio |
|-----------|--------|
| `001_create_initial` | Crea tabla con `UNIQUE(code)` global |
| `003_seed_core_buildings_types` | Seed base con upsert idempotente |
| `006_add_building_types_scope` | Añade `condominium_id`, `is_system`, `sort_order`, `deleted_at` + índice scope + FK a condominiums |
| `007_fix_building_type_fk_cascade` | FK `core_buildings.building_type_id` → `ON UPDATE CASCADE` |

---

## 🌐 API — Endpoints

### Base URL
`/building-types`

### Endpoints disponibles

| Método | Path | Descripción |
|--------|------|-------------|
| `POST` | `/building-types` | Crear tipo (global o custom) |
| `GET` | `/building-types/{id}` | Obtener tipo por ID |
| `GET` | `/building-types/uuid/{uuid}` | Obtener tipo por UUID |
| `PUT` | `/building-types/{id}` | Actualizar tipo (no system) |
| `DELETE` | `/building-types/{id}` | Soft delete (no system) |
| `POST` | `/building-types/{id}/restore` | Restaurar tipo eliminado |
| `DELETE` | `/building-types/{id}/hard` | Hard delete (no system, sin refs) |
| `GET` | `/building-types` | Listar tipos con filtros |

### Filtros de listado

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `condominium_id` | int | `null` | Filtra tipos para un condominio (incluye globales) |
| `include_system` | bool | `true` | Incluir tipos globales de sistema |
| `status` | int | `null` | Filtrar por estado (`1`=activo, `0`=inactivo) |
| `include_deleted` | bool | `false` | Incluir registros con `deleted_at` |
| `skip` | int | `0` | Paginación |
| `limit` | int | `100` | Máximo 500 |

### Ejemplo: crear tipo custom
```json
POST /building-types
{
  "condominium_id": 5,
  "code": "PARKING",
  "name": "Estacionamiento",
  "description": "Área de estacionamiento",
  "sort_order": 1
}
```

### Ejemplo: crear tipo global
```json
POST /building-types
{
  "condominium_id": null,
  "code": "INDUSTRIAL",
  "name": "Industrial"
}
```

---

## 🏛️ Módulo DDD

Ubicación: `src/library/dddpy/core_buildings_types/`

```
core_buildings_types/
├── domain/
│   ├── building_type_entity.py          # Entidad con is_global/is_custom
│   ├── building_type_data.py            # CreateBuildingTypeData, UpdateBuildingTypeData
│   ├── building_type_exception.py       # 8 excepciones de negocio
│   ├── building_type_success.py         # Mensajes de éxito
│   ├── building_type_repository.py      # Interfaz base
│   ├── building_type_cmd_repository.py  # Create, update, delete
│   └── building_type_query_repository.py # Queries + get_active_in_scope
├── infrastructure/
│   ├── dbbuildingtype.py               # SQLAlchemy model
│   ├── building_type_mapper.py
│   ├── building_type_cmd_repository.py  # Implementación cmd
│   └── building_type_query_repository.py # Implementación query
└── usecase/
    ├── building_type_cmd_schema.py     # Pydantic schemas
    ├── building_type_cmd_usecase.py    # Lógica de comandos
    ├── building_type_query_usecase.py  # Lógica de consultas
    ├── building_type_usecase.py        # Fachada completa
    └── building_type_factory.py        # Factory pattern
```

### Excepciones de negocio

| Excepción | HTTP | Cuándo |
|-----------|------|--------|
| `BuildingTypeNotFound` | 404 | Tipo no existe o está eliminado |
| `DuplicateBuildingTypeCode` | 409 | Código duplicado en el mismo scope |
| `BuildingTypeIsSystem` | 403 | Intento de modificar/eliminar tipo de sistema |
| `BuildingTypeIsInUse` | 409 | Hard delete con edificios referenciando |
| `BuildingTypeIsInactive` | 422 | Asignar tipo inactivo a edificio |
| `BuildingTypeIsDeleted` | 422 | Asignar tipo soft-deleted a edificio |
| `BuildingTypeNotAccessible` | 403 | Tipo custom de otro condominio |
| `InvalidBuildingTypeScope` | 400 | Crear tipo system con `condominium_id` |

### Método clave: `validate_for_building_assignment(type_id, condominium_id)`

Expuesto en `BuildingTypeUseCase`. Llamado por `core_buildings` al crear/actualizar un edificio. Verifica:
1. Tipo existe y no está eliminado
2. Tipo tiene `status = 1`
3. Tipo es global **o** pertenece al mismo `condominium_id`

---

## ✅ Checklist de validación (DoD)

- [x] `building_type_id = NULL` en edificio → permitido (sin tipo asignado)
- [x] Crear edificio con tipo global → debe pasar
- [x] Crear edificio con tipo custom del mismo condominio → debe pasar
- [x] Crear edificio con tipo custom de otro condominio → **bloquear** (403)
- [x] Crear edificio con tipo inactivo (`status = 0`) → **bloquear** (422)
- [x] Crear edificio con tipo soft-deleted → **bloquear** (422)
- [x] Soft delete de tipo referenciado → pasa (edificios quedan con `building_type_id = NULL`)
- [x] Hard delete de tipo referenciado → **bloquear** (409)
- [x] Soft delete / hard delete de tipo system → **bloquear** (403)
- [x] Restaurar tipo → pasa
- [x] Seed idempotente (sin `COUNT(*) > 0`)
- [x] Tests cubriendo reglas de negocio

---

## 📁 Archivos modificados/creados

| Archivo | Cambio |
|---------|--------|
| `alembic/versions/006_add_building_types_scope.py` | Nueva migración: scope columns + backfill |
| `alembic/versions/007_fix_building_type_fk_cascade.py` | Nueva migración: FK `ON UPDATE CASCADE` |
| `alembic/versions/003_seed_core_buildings_types.py` | Corregido: upsert idempotente |
| `seeds/seed_core_buildings_types.py` | Corregido: upsert idempotente |
| `library/dddpy/core_buildings_types/` | Nuevo módulo DDD completo (19 archivos) |
| `api/buildings_types/routes_building_types.py` | Nuevo: API routes |
| `library/dddpy/core_buildings/usecase/building_cmd_usecase.py` | Integrada validación de tipo |
| `library/dddpy/core_buildings/usecase/building_usecase.py` | Enriquecida respuesta con tipo |
| `tests/test_core_buildings_types.py` | Tests completos |
