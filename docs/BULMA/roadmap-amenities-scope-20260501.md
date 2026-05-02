# Roadmap Técnico — Amenities por Condominio y por Edificio

**Proyecto:** condo-py
**Autor técnico:** Lelouch S, Bulma S (code review)
**Asignado a:** Bulma S
**Fecha:** 2026-05-01
**Estado:** ✅ Implementado — MVP CERRADO
**Commits:** `1a77b73` (backend) + `5a1b9d4` (UI)
**Prioridad:** 🔴 Alta
**Sprint sugerido:** Sprint 1 (MVP)

---

## 1. Problema Actual

`core_amenities` actualmente solo tiene `condominium_id` comoFK. No existe relación con edificios, lo que limita los amenities a nivel condominio únicamente.

### Hoy sí soporta:
- Piscina pública del condominio
- Cancha de fútbol del condominio
- Lavandería común
- Gimnasio general
- Parrillas comunes

### Hoy no soporta:
- Piscina exclusiva de un edificio
- Gimnasio exclusivo de torre
- Parrilla privada por edificio
- Zona de reuniones / cafetería / cine / karaoke por edificio

---

## 1b. Verificación de Código (Bulma S — 2026-05-01)

Revisión directa del módulo `core_amenities`. Confirmado:

| Aspecto | Estado |
|---|---|
| `core_amenities` solo tiene `condominium_id` como FK | ✅ Confirmado |
| `AmenityEntity` no tiene campo `scope` ni `building_id` | ✅ Confirmado |
| `CreateAmenitySchema` solo acepta `condominium_id` | ✅ Confirmado |
| Queries filtran exclusivamente por `condominium_id` | ✅ Confirmado |
| `list_active` requiere `condominium_id` obligatorio | ✅ Confirmado |
| Ningún acoplamiento externo (reservas/dashboards) referencia `core_amenities` | ✅ Confirmado |
| No existen seeds de amenities | ✅ Confirmado |
| No existen tests de amenities | ✅ Confirmado |

**Traducción literal del código:**
> Hoy **todo** amenity es del condominio. Si creas "piscina edificio A", cualquier edificio la ve. No hay segmentación.

**Ventaja hallada:** Cambio autocontenido en el módulo — no se rompe nada fuera.

---

## 2. Arquitectura Propuesta

### 2.1 Nuevo modelo de datos

`core_amenities` — agregar columnas:

| Campo | Tipo | Nullable | Descripción |
|---|---|---|---|
| `scope` | ENUM('CONDOMINIUM','BUILDING') | NOT NULL | Alcance del amenity |
| `building_id` | BigInteger | NULL | FK a `core_buildings.id` (nullable) |

### 2.2 Reglas de negocio

| scope | building_id | Válido? |
|---|---|---|
| CONDOMINIUM | NULL | ✅ Sí |
| CONDOMINIUM | valor | ❌ No |
| BUILDING | valor | ✅ Sí |
| BUILDING | NULL | ❌ No |

### 2.3 Validación cruzada
- Si `scope = BUILDING`, el `building_id` obligatoriamente debe pertenecer al mismo `condominium_id`
-CHECK constraint a nivel DB para garantizar integridad

### 2.4 Índice compuesto sugerido
```sql
INDEX ix_amenities_scope_lookup (condominium_id, scope, building_id)
```

---

## 3. Scope del Sprint 1 (MVP)

### Fase 1 — Discovery ✅ LISTO
- Relevar todos los archivos que tocan `amenities` — Lelouch + Bulma code review completada
- Confirmado por código: sin acoplamientos externos

### Fase 2 — Migración DB
- Nueva migración Alembic: agregar `scope` + `building_id`
- Backfill: todos los amenities existentes → `scope = CONDOMINIUM`, `building_id = NULL`
- Agregar CHECK constraint
- Crear índice compuesto

**Salida:** migración idempotente, sin pérdida de datos.

### Fase 3 — Rediseño de Dominio
- Actualizar `AmenityEntity` con campos `scope` y `building_id`
- Actualizar `AmenityMapper`
- Actualizar `DBAmenity`
- Actualizar `CreateAmenitySchema` y `UpdateAmenitySchema`
- Agregar validación cruzada scope/building

### Fase 4 — Backend / CRUD
- Ajustar `AmenityUseCase`
- Ajustar `AmenityQueryRepository` (listados filtrados por scope y building)
- Ajustar `AmenityCmdRepository`
- Actualizar routes si corresponde
- Agregar endpoint o filtro por `building_id`

### Fase 5 — Semántica de Lectura
- **Vista condominio:** ve amenities globales del condominio (`scope = CONDOMINIUM`)
- **Vista edificio:** ve amenities globales del condominio (`scope = CONDOMINIUM`) + amenidades exclusivas de ese edificio (`scope = BUILDING AND building_id = X`)
- **Edificio A no debe ver exclusivas de edificio B**

### Fase 6 — Seeds
- Seed con amenities de ambos scopes:
  - Ejemplo: piscina general (`CONDOMINIUM`)
  - Ejemplo: gimnasio edificio A (`BUILDING`)
  - Ejemplo: parrilla edificio B (`BUILDING`)

### Fase 7 — UI / Panel Administrativo
- Selector de alcance: **Condominio** / **Edificio**
- Si elige **Edificio**: mostrar selector de edificio
- En listados: badge visible `General` / `Exclusiva edificio`
- Campos de respuesta API: incluir `scope` y `building_id`

### Fase 8 — Testing
**Casos obligatorios:**
1. Crear amenidad de condominio (`scope = CONDOMINIUM`)
2. Crear amenidad de edificio (`scope = BUILDING`)
3. Rechazar `building_id` de otro condominio
4. Listar amenidades correctas por edificio
5. Asegurar que edificio A no herede exclusivas de B
6. Migración de datos legacy sin pérdida

---

## 4. Sprint 2 (Futuro — fuera del MVP)

Solo activar si el negocio lo confirma:

- Reservas avanzadas por scope
- Permisos finos por amenidad
- Reporting por scope
- Soporte `UNIT` (amenities por unidad individual)

---

## 5b. Implementación Realizada (Bulma S — 2026-05-01)

**Branch:** `feature/fin-09-10-debtor-idempotency`
**Commit:** `1a77b73` — `feat(amenities): add scope (CONDOMINIUM|BUILDING) + building_id support`

| Componente | Archivos | Líneas |
|---|---|---|
| Migración DB | `052_add_amenity_scope_and_building.py` | +79 |
| Dominio | `amenity_entity.py` (+propiedades scope, invariantes) | +39 |
| Schemas | `amenity_cmd_schema.py` (+model_validator Pydantic) | +34 |
| UseCase | `amenity_usecase.py` (+validación cruzada, listados) | +98 |
| Repositorio queries | `amenity_query_repository.py` (+semántica lectura) | +124 |
| Repositorio cmd | `amenity_cmd_repository.py` | +16 |
| Mapper | `amenity_mapper.py` | +10 |
| Routes API | `routes_amenities.py` | +21 |
| Seeds | `seed_amenities.py` (10 amenities mixtos) | +186 |
| Tests | `test_core_amenities.py` (31 tests, 100% pass) | +451 |
| **Total** | **12 archivos** | **+1031** |

**Fases completadas:** ✅ Discovery ✅ DB ✅ Dominio ✅ Backend ✅ Semántica lectura ✅ Seeds ✅ Tests

**Queda pendiente:** nada — MVP completo ✅

---

## 5c. Detalle de lo Implementado

### Migración DB
- `scope` VARCHAR(20) — backfill automático de existentes → `CONDOMINIUM`
- `building_id` FK nullable a `core_buildings` (ON DELETE SET NULL)
- Índice compuesto `(condominium_id, scope, building_id)`
- 100% backward-compatible, sin pérdida de datos

### Dominio (`AmenityEntity`)
- `is_condominium_scope` / `is_building_scope` — computed properties
- `scope_label` — retorna `"General"` o `"Exclusiva edificio"`
- Validación de invariantes en constructor

### Validación (schemas)
- `model_validator` Pydantic — rechaza combinaciones inválidas antes del usecase
- CONDOMINIUM + building_id informado → rechazo
- BUILDING + building_id null → rechazo

### UseCase
- Verifica que `building_id` pertenezca al mismo `condominium_id`
- Rechaza edificios de otro condominio y edificios inexistentes

### Semántica de lectura
- `?condominium_id=X` → solo amenities `CONDOMINIUM`
- `?condominium_id=X&building_id=Y` → `CONDOMINIUM` + `BUILDING` para ese edificio
- Edificio A no ve exclusivas de edificio B

### Seeds
10 amenities mixtos:
- **Condominio (4):** piscina general, cancha fútbol, lavandería, parrillas
- **Edificio (6):** gimnasio torre A, SUM edificio B, cine, karaoke, cafetería, parrilla rooftop

### Tests — 31 casos
- Entidad: scope properties, invariantes, to_dict
- Schemas: combinaciones válidas e inválidas
- UseCase: ambos scopes, rechazo building cruzado, rechazo inexistente
- Listados: semántica edificio vs condominio
- Backward compatibility: defaults sin scope explícito

### UI/Admin ✅ Completado (commit `5a1b9d4`)
- **`AmenitiesForm`:** selector scope con íconos Globe/Building, Zod `.refine()` validación condicional, badge visual en tiempo real, pre-fill correcto en edición
- **`amenities-table-config.tsx`:** columna "Alcance" con badge `General` (gris) / `Exclusiva edificio` (azul)
- **Página detalle:** badge scope header + campo "Alcance" en card info
- **API client (`api.ts`):** `scope` incluido en create/update payloads
- **Models (`models.ts`):** `Amenity.scope?: "CONDOMINIUM" | "BUILDING"` + `scope_label?: string`

**11/11 criterios de aceptación ✅ MVP CERRADO**

---

## 5. Estimación y Plan de Ejecución

| Fase | Días estimados | Estado |
|---|---|---|
| Discovery | 0.5 | ✅ Completado |
| DB + dominio | 0.5–1 | ✅ Completado |
| Backend CRUD/listados/validaciones | 1–1.5 | ✅ Completado |
| UI/admin | 0.5–1 | ✅ Completado |
| Seeds + Tests | 0.5–1 | ✅ Completado |
| **Total MVP** | **3 a 5 días** | ✅ Hecho (~1 día real) |

> ⚠️ Sin acoplamientos externos detectados — la estimación de 3-4 días de Bulma es realista.

### Orden de ejecución (según Bulma)
1. **Migración DB** — `scope` ENUM + `building_id` nullable + backfill + CHECK + índice
2. **Dominio** — refactor de `AmenityEntity`, mapper, schemas, interfaces repositorio
3. **Backend** — usecase con validación cruzada, queries con filtro scope/building, semántica de lectura
4. **API** — ajustar routes para aceptar `building_id` y `scope`
5. **Seeds + Tests** — coverage de todos los casos de aceptación

### Notas de Bulma
- Ningún módulo externo depende de `core_amenities` — cambio autocontenido
- No hay seeds ni tests existentes — hay que crearlos desde cero

---

## 6. Archivos Identificados como Impactados

### Modelo / Entidad
- `src/library/dddpy/core_amenities/domain/amenity_entity.py`
- `src/library/dddpy/core_amenities/infrastructure/dbamenity.py`
- `src/library/dddpy/core_amenities/infrastructure/amenity_mapper.py`

### Schemas
- `src/library/dddpy/core_amenities/usecase/amenity_cmd_schema.py`

### Use Case
- `src/library/dddpy/core_amenities/usecase/amenity_usecase.py`

### Repositorios
- `src/library/dddpy/core_amenities/domain/amenity_cmd_repository.py`
- `src/library/dddpy/core_amenities/domain/amenity_query_repository.py`
- `src/library/dddpy/core_amenities/infrastructure/amenity_cmd_repository.py`
- `src/library/dddpy/core_amenities/infrastructure/amenity_query_repository.py`

### API Routes
- `src/api/amenities/routes_amenities.py`

### Migración
- `src/alembic/versions/036_create_core_amenities.py` (migración base — crear nueva)

### Seeds
- `src/seeds/` (crear/actualizar seed de amenities)

---

## 7. Decisión Arquitectónica Clave

| Hacer | No hacer |
|---|---|
| Usar la misma tabla `core_amenities` | No duplicar tablas por tipo |
| Agregar `scope` + `building_id` | No crear endpoints separados por scope |
| Soportar `CONDOMINIUM` + `BUILDING` | No implementar `UNIT` todavía |
| Migración backward-compatible | No romper datos existentes |

---

## 8. Criterios de Aceptación — Estado

- [x] Puedo crear un amenity con `scope = CONDOMINIUM` y `building_id = null`
- [x] Puedo crear un amenity con `scope = BUILDING` y `building_id` válido
- [x] El sistema rechaza creación con `scope = CONDOMINIUM` y `building_id` informado
- [x] El sistema rechaza creación con `scope = BUILDING` y `building_id = null`
- [x] El sistema rechaza `building_id` cuyo edificio no pertenece al `condominium_id` del amenity
- [x] Listado por condominio solo muestra amenities con `scope = CONDOMINIUM`
- [x] Listado por edificio muestra amenities del condominio + exclusivas de ese edificio
- [x] Edificio A no ve exclusivas de edificio B
- [x] Datos existentes migrados sin pérdida con `scope = CONDOMINIUM`
- [x] Badge visible en listados: `General` vs `Exclusiva edificio` ✅
- [x] Tests covering these cases pass (31/31)
