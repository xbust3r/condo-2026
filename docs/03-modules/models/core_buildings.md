---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
  - core-module
---

# 🗄️ Tabla: core_buildings

## 📝 Descripción

Almacena la información de las torres, bloques o edificios que pertenecen a un condominio.

Cada `core_buildings` representa una unidad física independiente dentro de un condominio. Es el núcleo de la estructura operativa del sistema — de él dependen las unidades inmobiliarias (`core_unitys`), los residentes (`users_residents`), y futura lógica de cobranza, tickets y reportes segmentados por edificio.

---

## 🏗️ Estructura Final (post-migración 002)

| Campo | Tipo | Nullable | Default | Descripción |
|-------|------|---------|--------|-------------|
| id | BIGINT | NO | autoincrement | PK interna |
| uuid | CHAR(36) | NO | UUID() | Identificador estable externo |
| condominium_id | BIGINT | NO | — | FK → core_condominiums |
| building_type_id | BIGINT | YES | NULL | FK → core_buildings_types |
| code | VARCHAR(50) | NO | — | Código operativo único por condominio |
| name | VARCHAR(255) | NO | — | Nombre visible del edificio |
| short_name | VARCHAR(50) | YES | NULL | Alias para UI, dashboards, reportes |
| description | TEXT | YES | NULL | Notas administrativas o descripción física |
| built_area | DECIMAL(12,4) | YES | NULL | Área construida total en m² |
| common_area | DECIMAL(12,4) | YES | NULL | Área común asociada al edificio en m² |
| coefficient | DECIMAL(9,6) | YES | NULL | Coeficiente de participación (0.000000 - 100.000000) |
| floors_count | INT | NO | 0 | Cantidad de pisos sobre nivel |
| basements_count | INT | NO | 0 | Cantidad de sótanos |
| units_planned | INT | NO | 0 | Número de unidades proyectadas/esperadas |
| sort_order | INT | NO | 0 | Orden de visualización en listados |
| status | INT | NO | 1 | Estado operativo (1=activo, 0=inactivo) |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | Fecha de última actualización |
| deleted_at | DATETIME | YES | NULL | Soft delete — fecha de eliminación lógica |

---

## 🔗 Relaciones (Foreign Keys)

```
core_buildings
├── core_condominiums (condominium_id)     — UN BUILDING PERTENECE A UN CONDOMINIO
├── core_buildings_types (building_type_id) — UN BUILDING PUEDE TENER UN TIPO (O NO)
└── core_unitys (vía building_id)          — UN BUILDING TIENE MUCHAS UNIDADES
```

| FK | Target | ON DELETE | Notas |
|----|--------|-----------|-------|
| condominium_id | core_condominiums.id | RESTRICT | No se puede borrar condominio con edificios |
| building_type_id | core_buildings_types.id | SET NULL | Si se elimina un tipo, el edificio queda sin tipo |

---

## 📐 Campos Derivados del Análisis Competitivo

### `short_name` — Alias operativo

**Referencia:** Buildium, AppFolio, DoorLoop — todos tienen campo corto para identificar edificios en interfaces compactas.

**Usos:**
- Etiquetas en mapas/walkthroughs visuales
- Filtros rápidos en mobile
- Nombres de torre en notificaciones push
- Reportes de ocupación por edificio
- Dashboards compactos

**Límite:** hasta 50 caracteres. Para UI estrictas (mobile), considerar truncate a 20-30 en capa de presentación.

---

### `coefficient` — Coeficiente de participación

**Referencia:** sistemas de copropiedad reales (AppFolio, Buildium) usan coeficiente para prorrateo de gastos comunes, distribución de votes, y cálculo de porcentajes de propiedad.

**Cálculo:** el coeficiente representa el peso proporcional del edificio dentro del condominio. Un edificio con coefficient=25.5 tiene el 25.5% de participación.

**Validación:** CHECK constraint fuerza rango 0-100. La validación de que la suma de coeficientes de todos los edificios sea 100 se maneja en **capa de negocio**, no en DB.

---

### `built_area` y `common_area` — Separación de áreas

**Problema original:** el campo `size` era ambiguo — mezclaba área construida con área de terreno.

**Solución:** dos campos separados con precisión DECIMAL(12,4) para manejar bienes raíces con exactitud centimétrica.

**Usos:**
- Reportes inmobiliarios
- Métricas comparativas entre edificios
- Cálculo de densidad (unidades por m²)
- Distribución de costos de mantenimiento por área

---

## ⛓️ Constraints de Negocio

Los siguientes CHECK constraints existen en la BD y no deben removerse:

| Constraint | Validación | Propósito |
|------------|------------|-----------|
| ck_core_buildings_built_area_positive | built_area >= 0 | No permitir áreas negativas |
| ck_core_buildings_common_area_positive | common_area >= 0 | No permitir áreas comunes negativas |
| ck_core_buildings_coefficient_range | coefficient BETWEEN 0 AND 100 | Coeficiente siempre válido |
| ck_core_buildings_floors_count_positive | floors_count >= 0 | No pisos negativos |
| ck_core_buildings_basements_count_positive | basements_count >= 0 | No sótanos negativos |
| ck_core_buildings_units_planned_positive | units_planned >= 0 | No unidades negativas |
| ck_core_buildings_sort_order_positive | sort_order >= 0 | No orden negativo |

---

## 📇 Índices

| Índice | Columnas | Tipo | Propósito |
|--------|----------|------|-----------|
| ix_core_buildings_condominium_code | (condominium_id, code) | UNIQUE | Código único por condominio |
| ix_core_buildings_condominium_id | (condominium_id) | INDEX | FK lookups y filtros por condominio |
| ix_core_buildings_building_type_id | (building_type_id) | INDEX | Filtros por tipo de edificio |
| ix_core_buildings_status | (status) | INDEX | Filtros por estado operativo |
| ix_core_buildings_condominium_status | (condominium_id, status) | INDEX | Listados filtrados por condominio + estado |
| ix_core_buildings_condominium_sort | (condominium_id, sort_order) | INDEX | Orden visual natural |

---

## 🧠 Reglas de Negocio Obligatorias

1. **No crear edificio sin condominium_id válido** — el FK enforced a nivel BD
2. **No repetir code dentro del mismo condominio** — unique constraint compuesto
3. **No permitir valores negativos en áreas ni contadores** — CHECK constraints
4. **No permitir coefficient fuera de rango 0-100** — CHECK constraint
5. **Listados públicos deben excluir eliminados** — filter WHERE deleted_at IS NULL
6. **Restore disponible** — soft delete reversible hasta que haya lógica depuración
7. **Si un edificio tiene unidades activas, no permitir eliminación física** — validar en capa de negocio antes de hard delete

---

## 🔄 Soft Delete

`deleted_at` permite eliminación lógica sin pérdida de datos.

**Comportamiento:**
- DELETE physically →sets deleted_at al timestamp actual
- POST /restore → limpia deleted_at
- GET /list → excluye deleted por defecto
- GET /list?include_deleted=true → incluye todos

**No hacer:** no hay cascada física. Si el edificio tiene `core_unitys` asociadas con status activo, la eliminación lógica se permite pero la física debe bloquearse en capa de negocio.

---

## 🚫 Lo que NO está en esta tabla (y por qué)

| Campo | Razón de exclusión |
|-------|-------------------|
| `legacy_code` | Solo como campo transitorio para migraciones reales. No смысла sin datos legacy |
| `address` | Va en `core_condominiums` o en `core_unitys`, no en edificio |
| `manager_id` | Pertenece a relación separate (users con rol de gestión) |

---

## 📊 Estrategia de Expansión Futura

Esta tabla es el eje de segmentación operativa. Una vez que `core_unitys` esté vinculada:

- **Anuncios segmentados por edificio** — notificación push a residentes de X torre
- **Tickets e incidencias por torre** — filtro automático por building_id
- **Ocupación por edificio** — count de units activas por building
- **Dashboards por bloque** — métricas agregadas a nivel de edificio
- **Cobranza por edificio** — prorrateo basado en coefficient
- **Reportes financieros por torre** — separación clara de costos comunes

La estructura actual soporta todo esto sin cambios adicionales.

---

## 🗂️ Archivos Relacionados

- Migración: `src/alembic/versions/002_refactor_core_buildings.py`
- Migraciones correctivas: `004_fix_buildings_unique_constraint.py`, `005_fix_buildings_fk_actions.py`
- Seed: `seeds/seed_core_buildings_types.py`
- Tablero de tareas: `docs/07-roadmap/core_buildings-task-order.md`
- Módulo DDD: `library/dddpy/core_buildings/` (implementado en Tareas 3-7) ✅
- Tipo de edificio: `docs/03-modules/models/core_buildings_types.md`
- Unidades: `docs/03-modules/models/core_unitys.md`
- Análisis competitivo: `docs/05-research/competitive-analysis-condo-systems.md`

---

**Última actualización:** 2026-04-13 (post-migraciones 002, 004, 005)
**Estado del módulo:** ✅ OPERATIVO — 10/10 tareas completadas | 2 migraciones correctivas aplicadas