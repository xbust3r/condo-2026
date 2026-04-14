---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
---

# 🗄️ Tabla: core_unities

## 📝 Descripción
Representa las unidades inmobiliarias individuales de un edificio: apartamentos, locales, oficinas,PH, etc. Es la pieza central del núcleo inmobiliario — donde convergen ocupación, residentes, cobranza y reportes.

---

## 🏗️ Estructura (post-refactor 008)

| Campo | Tipo | Nullable | Default | Descripción |
|-------|------|----------|---------|-------------|
| id | BIGINT | NO | autoincrement | PK interna |
| uuid | CHAR(36) | NO | UUID() | Identificador estable externo |
| building_id | BIGINT | NO | — | FK → [[core_buildings]] |
| unity_type_id | BIGINT | YES | NULL | FK → [[core_unittys_types]] |
| unit_number | VARCHAR(50) | YES | — | Identidad física visible (ej. 101, A-12, PH-1) |
| code | VARCHAR(50) | YES | NULL | Código operativo interno |
| name | VARCHAR(255) | YES | NULL | Nombre comercial/display opcional |
| description | TEXT | YES | NULL | Notas administrativas internas |
| private_area | DECIMAL(12,4) | YES | NULL | Área privada útil en m² |
| coefficient | DECIMAL(9,6) | YES | NULL | Coeficiente de copropiedad/prorrateo (0-100) |
| floor_number | INT | YES | NULL | Piso numérico para lógica y orden |
| floor_label | VARCHAR(30) | YES | NULL | Etiqueta UI (ej. Sótano 1, Mezzanine, PH) |
| occupancy_status | VARCHAR(30) | NO | vacant | Estado: vacant\|occupied\|reserved\|maintenance\|blocked |
| sort_order | INT | NO | 0 | Orden visual dentro del edificio |
| status | INT | NO | 1 | Estado operativo (1=activo, 0=inactivo) |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | Última actualización |
| deleted_at | DATETIME | YES | NULL | Soft delete (nulo = activo) |

---

## 🔗 Relaciones (Foreign Keys)

| FK | Referencia | ON DELETE | ON UPDATE |
|----|------------|-----------|-----------|
| building_id | [[core_buildings]].id | RESTRICT | CASCADE |
| unity_type_id | [[core_unittys_types]].id | SET NULL | CASCADE |

---

## 🔑 Índices

| Índice | Columnas | Tipo | Propósito |
|--------|----------|------|-----------|
| ix_core_unities_building_id | building_id | normal | FK + filtro por edificio |
| ix_core_unities_unity_type_id | unity_type_id | normal | Filtro por tipo de unidad |
| ix_core_unities_status | status | normal | Filtro por estado operativo |
| ix_core_unities_building_status | (building_id, status) | composite | Listados por edificio+estado |
| ix_core_unities_building_sort | (building_id, sort_order) | composite | Orden visual por edificio |
| ix_core_unities_building_floor | (building_id, floor_number) | composite | Agrupación por piso |
| ix_core_unities_building_occupancy | (building_id, occupancy_status) | composite | Filtro operativo por ocupación |
| ux_core_unities_building_unit_number | (building_id, unit_number) | UNIQUE | Unicidad dentro del edificio |
| ux_core_unities_building_code | (building_id, code) | UNIQUE | Unicidad de código interno |

---

## ⚙️ Constraints

| Nombre | Expresión | Propósito |
|--------|-----------|-----------|
| ck_core_unities_private_area_positive | private_area >= 0 | Área no puede ser negativa |
| ck_core_unities_coefficient_range | coefficient >= 0 AND coefficient <= 100 | Coeficiente en rango válido |
| ck_core_unities_sort_order_positive | sort_order >= 0 | Orden no negativo |
| ck_core_unities_occupancy_status_valid | occupancy_status IN ('vacant','occupied','reserved','maintenance','blocked') | Solo valores permitidos |

---

## 🔄 Campos eliminados en refactor 008

| Campo viejo | Razón |
|-------------|-------|
| `type` | Redundante con `unity_type_id` |
| `size` | Reemplazado por `private_area` con mejor precisión |
| `percentage` | Reemplazado por `coefficient` con mejor precisión |
| `floor` | Reemplazado por `floor_number` + `floor_label` |
| UNIQUE(code) global | Reemplazado por UNIQUE compuesto (building_id, code) |

---

## 📦 Módulo DDD

Ubicación: `src/library/dddpy/core_unities/`

```
core_unities/
├── domain/
│   ├── unity_entity.py       — Entidad de dominio con invariantes
│   ├── unity_data.py         — CreateData / UpdateData (dataclasses)
│   ├── unity_exception.py    — Excepciones de dominio
│   ├── unity_success.py      — Mensajes de éxito
│   ├── unity_repository.py   — Contrato genérico
│   ├── unity_cmd_repository.py   — Interfaz de escritura
│   └── unity_query_repository.py — Interfaz de lectura
├── infrastructure/
│   ├── dbunitys.py               — Modelo SQLAlchemy
│   ├── unity_mapper.py           — Mapper DB ↔ Entity
│   ├── unity_cmd_repository.py   — Implementación de escritura
│   └── unity_query_repository.py — Implementación de lectura
└── usecase/
    ├── unity_cmd_schema.py       — Schemas Pydantic (create/update)
    ├── unity_cmd_usecase.py      — Lógica de escritura
    ├── unity_query_usecase.py    — Lógica de lectura
    ├── unity_usecase.py          — Fachada con enriquecimiento
    └── unity_factory.py         — Factory de use cases
```

---

## 🌐 API Routes

Prefijo: `/unities`

| Método | Path | Descripción |
|--------|------|-------------|
| POST | /unities | Crear unidad |
| GET | /unities/{id} | Obtener por ID |
| GET | /unities/uuid/{uuid} | Obtener por UUID |
| PUT | /unities/{id} | Actualizar |
| DELETE | /unities/{id} | Soft delete |
| POST | /unities/{id}/restore | Restaurar |
| DELETE | /unities/{id}/hard | Hard delete (bloqueado si tiene residentes) |
| GET | /unities | Listar con filtros |
| GET | /unities/building/{building_id} | Listar por edificio |

---

## 📋 Reglas de negocio

- Una unidad debe pertenecer a un edificio existente y activo
- `unit_number` debe ser único dentro del mismo edificio (constraint DB + validación app)
- `occupancy_status` y `status` son ejes independientes:
  - `status` = vive operativamente (1) o no (0)
  - `occupancy_status` = vacante/ocupada/reservada/mantenimiento/bloqueada
- Soft delete (deleted_at) no elimina registros con historial
- Hard delete solo si no hay residentes activos asociados
- El módulo valida contra `core_unittys_types` si el FK existe; no crashea si el módulo no está implementado aún

---

## 🔗 Dependencias

- **Requiere:** [[core_buildings]], [[core_unittys_types]]
- **Tiene muchos:** [[users_residents]] (residentes por unidad)
- **Futuro:** ledger/cobranza por unidad, tickets por unidad, documentos por unidad
