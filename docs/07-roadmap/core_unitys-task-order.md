# ♟️ core_unitys — Orden de Trabajo y Control de Ejecución

> Fecha: 2026-04-14
> Autor: Lelouch S
> **ESTADO: 🟡 EN REVISIÓN — pendiente de aprobación**
> Arquitecto: Lelouch S | Coordinator: Misato K | Dev: Bulma S
> Objetivo: dejar un tablero único para rediseñar e implementar `core_unitys` como módulo real de negocio, con criterios claros de base de datos, lógica, naming, constraints, y flujo de ejecución.

---

## 1. Objetivo del módulo

Implementar `core_unitys` como pieza central del núcleo inmobiliario del sistema, no como simple tabla de departamentos.

Debe quedar preparada para servir como base de:
- ocupación por unidad
- relación con residentes
- futura cobranza y ledger por unidad
- tickets/incidencias segmentadas
- documentos por inmueble
- reportes operativos y financieros
- portal residente

La unidad es el punto donde convergen propiedad, ocupación y operación. Si esta pieza se diseña mal, todo lo demás nace torcido.

---

## 2. Diagnóstico del diseño actual

El diseño actual en `001_create_initial.py` define esta tabla:
- `id`
- `uuid`
- `name`
- `code`
- `description`
- `size`
- `percentage`
- `type`
- `floor`
- `unit`
- `building_id`
- `unity_type_id`
- `status`
- `created_at`
- `updated_at`

### Problemas detectados

1. `type` duplica responsabilidad de `unity_type_id`.
2. `unit` tiene mal naming y semántica débil.
3. `size` es ambiguo: no distingue área privada, construida o vendible.
4. `percentage` tiene nombre y precisión pobres para copropiedad real.
5. `code` aparece con unicidad global, lo cual no escala bien a negocio real.
6. No existe `deleted_at` para soft delete.
7. No existen constraints numéricos mínimos.
8. No existen índices estratégicos para filtros operativos.
9. No existe estado de ocupación (`occupancy_status`).
10. El módulo Python `src/library/dddpy/core_unitys/` no existe todavía.

---

## 3. Cambios obligatorios sobre el diseño actual

### 3.1 Eliminar redundancia de tipos
**Acción:** eliminar campo `type`.

**Motivo:**
El tipo de unidad debe representarse exclusivamente con `unity_type_id`.

**Regla final:**
- el tipo formal vive en catálogo (`core_unittys_types`)
- no se acepta texto libre paralelo

---

### 3.2 Corregir naming operativo
**Acción:** renombrar `unit` → `unit_number`.

**Motivo:**
`unit` es demasiado genérico. `unit_number` comunica mejor que representa la identidad física visible de la unidad.

**Ejemplos válidos:**
- `101`
- `A-12`
- `PH-1`
- `LOCAL-03`

---

### 3.3 Corregir campos numéricos ambiguos
**Acción:**
- eliminar `size`
- eliminar `percentage`
- agregar:
  - `private_area DECIMAL(12,4)`
  - `coefficient DECIMAL(9,6)`

**Motivo:**
- `size` mezcla significados distintos
- `percentage` se queda corta para reglas reales de copropiedad
- el modelo debe ser preciso para crecer hacia finanzas, prorrateos y reportes

---

### 3.4 Mejorar semántica de piso
**Acción:** reemplazar `floor` por:
- `floor_number INT NULL`
- `floor_label VARCHAR(30) NULL` (opcional recomendado)

**Motivo:**
En la operación real, no todo piso se representa bien como entero: sótanos, mezzanine, PH, lobby, rooftop.

**Regla sugerida:**
- `floor_number` para orden/lógica
- `floor_label` para UI/presentación

---

### 3.5 Agregar estado de ocupación
**Acción:** agregar `occupancy_status VARCHAR(30)` o smallint/enum equivalente.

**Valores iniciales sugeridos:**
- `vacant`
- `occupied`
- `reserved`
- `maintenance`
- `blocked`

**Motivo:**
`status` operativo no cubre el estado real de ocupación. La competencia trabaja con este eje porque impacta reportes, comunicación, cobranza y operación.

---

### 3.6 Agregar orden visual
**Acción:** agregar `sort_order INT NOT NULL DEFAULT 0`.

**Motivo:**
Permite ordenar unidades en UI/reportes sin depender del `id`.

---

### 3.7 Agregar borrado lógico
**Acción:** agregar `deleted_at DATETIME NULL`.

**Motivo:**
Una unidad con historial de residentes, cobros, tickets o documentos no debe desaparecer físicamente salvo proceso excepcional.

---

## 4. Estructura final recomendada para `core_unitys`

| Campo | Tipo sugerido | Nullable | Default | Descripción |
|---|---|---|---|---|
| id | BIGINT | NO | autoincrement | PK interna |
| uuid | CHAR(36) / UUID | NO | UUID() | Identificador estable externo |
| building_id | BIGINT | NO | — | FK al edificio |
| unity_type_id | BIGINT | YES | NULL | FK al catálogo de tipo de unidad |
| unit_number | VARCHAR(50) | NO | — | Identidad física visible de la unidad |
| code | VARCHAR(50) | YES | NULL | Código operativo interno/importación |
| name | VARCHAR(255) | YES | NULL | Nombre visible/comercial opcional |
| description | TEXT | YES | NULL | Notas administrativas |
| private_area | DECIMAL(12,4) | YES | NULL | Área privada útil de la unidad |
| coefficient | DECIMAL(9,6) | YES | NULL | Coeficiente de copropiedad/prorrateo |
| floor_number | INT | YES | NULL | Piso numérico para lógica y orden |
| floor_label | VARCHAR(30) | YES | NULL | Etiqueta de piso para UI |
| occupancy_status | VARCHAR(30) | NO | `vacant` | Estado de ocupación |
| sort_order | INT | NO | 0 | Orden visual/manual |
| status | INT | NO | 1 | Estado operativo |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | Fecha de actualización |
| deleted_at | DATETIME | YES | NULL | Soft delete |

---

## 5. Qué columnas eliminar, renombrar o conservar

### Eliminar
- `type`
- `size`
- `percentage`
- `unit`
- `floor`

### Renombrar / reemplazar
- `unit` → `unit_number`
- `size` → `private_area`
- `percentage` → `coefficient`
- `floor` → `floor_number`

### Conservar
- `id`
- `uuid`
- `name` (pero opcional)
- `code` (pero no como identidad única global)
- `description`
- `building_id`
- `unity_type_id`
- `status`
- `created_at`
- `updated_at`

### Agregar
- `floor_label`
- `occupancy_status`
- `sort_order`
- `deleted_at`

---

## 6. Constraints exactos recomendados

### 6.1 Unicidad
**Eliminar:**
- `UNIQUE(code)` global

**Crear:**
- `UNIQUE(building_id, unit_number)`
- `UNIQUE(building_id, code)` solo si `code` se decide obligatorio/operativo

**Nota:**
Si `code` queda opcional, evaluar permitir múltiples `NULL` y mantener unicidad solo para valores no nulos según comportamiento MySQL.

---

### 6.2 CHECK constraints
Crear como mínimo:

- `ck_core_unitys_private_area_positive`
  - `private_area IS NULL OR private_area >= 0`

- `ck_core_unitys_coefficient_range`
  - `coefficient IS NULL OR (coefficient >= 0 AND coefficient <= 100)`

- `ck_core_unitys_sort_order_positive`
  - `sort_order >= 0`

- `ck_core_unitys_floor_number_range`
  - opcional en fase 1 si se usa un rango operativo razonable
  - ejemplo: `floor_number IS NULL OR floor_number >= -20`

- `ck_core_unitys_occupancy_status_valid`
  - si usan CHECK en lugar de catálogo/enum:
  - `occupancy_status IN ('vacant','occupied','reserved','maintenance','blocked')`

---

### 6.3 Foreign keys
**building_id**
- referencia: `core_buildings.id`
- acción recomendada: `ON DELETE RESTRICT`
- `ON UPDATE CASCADE`

**unity_type_id**
- referencia: `core_unittys_types.id`
- acción recomendada: `ON DELETE SET NULL`
- `ON UPDATE CASCADE` o `SET NULL` según política del proyecto

---

## 7. Índices exactos recomendados

### Índices mínimos
- `ix_core_unitys_building_id` → `(building_id)`
- `ix_core_unitys_unity_type_id` → `(unity_type_id)`
- `ix_core_unitys_status` → `(status)`

### Índices compuestos operativos
- `ix_core_unitys_building_status` → `(building_id, status)`
- `ix_core_unitys_building_sort` → `(building_id, sort_order)`
- `ix_core_unitys_building_floor` → `(building_id, floor_number)`
- `ix_core_unitys_building_occupancy` → `(building_id, occupancy_status)`

### Índices únicos
- `ux_core_unitys_building_unit_number` → `(building_id, unit_number)`
- `ux_core_unitys_building_code` → `(building_id, code)` si aplica

---

## 8. Reglas de negocio obligatorias

- No crear unidad sin `building_id` válido.
- No crear unidad bajo edificio eliminado lógicamente.
- No crear unidad con `unity_type_id` inexistente o inactivo.
- No repetir `unit_number` dentro del mismo edificio.
- No permitir áreas negativas.
- No permitir `coefficient` fuera de rango.
- Los listados deben excluir eliminados por defecto.
- Debe existir restore.
- No permitir hard delete si la unidad tiene residentes activos o relaciones operativas posteriores.
- Si el edificio padre está inactivo/eliminado, no debe permitirse alta operativa de nuevas unidades.

---

## 9. Observaciones de modelado que deben respetarse

### 9.1 `name` no debe ser identidad principal
`name` puede existir para UX o naming comercial, pero no debe desplazar a `unit_number`.

### 9.2 `code` no debe ser obligatorio por dogma
Si el negocio no necesita un código interno separado, no debe forzarse solo por costumbre técnica.

### 9.3 `occupancy_status` y `status` no son lo mismo
- `status` = vive el registro operativamente o no
- `occupancy_status` = vacante, ocupada, reservada, mantenimiento, bloqueada

### 9.4 No meter deuda o propietario directo en esta tabla
Los datos de ownership, tenancy, balance o cuentas deben vivir en módulos/relaciones separadas.

### 9.5 No repetir jerarquía completa en tablas hijas si no hay razón real
Cuando se implemente `users_residents`, usar `unity_id` como raíz principal. Si además se persisten `building_id` y `condominium_id`, se deberá validar consistencia estricta.

---

## 10. Relación estratégica con análisis competitivo

Los productos serios del mercado no tratan la unidad como simple catálogo. La tratan como nodo operativo de:
- ocupación
- residentes/tenancy
- estado de cuenta
- documentos
- tickets
- comunicación segmentada

Por eso este módulo debe quedar listo para alimentar en el futuro:
- ledger por unidad
- cobranza por unidad
- estado de ocupación en dashboards
- portal residente
- indicadores de morosidad/ocupación
- incidencias y documentación asociada

El error clásico sería modelarla como “otro CRUD”. Ese camino sacrifica la reina por un peón.

---

## 11. Lista oficial de tareas

## Tarea 1 — Diseñar migración de refactor sobre `core_unitys`
**Objetivo:**
- eliminar campos ambiguos
- agregar campos nuevos
- corregir uniqueness
- agregar índices y constraints
- agregar `deleted_at`

**Entregable:**
- migración Alembic nueva, separada de `001_create_initial.py`

**Responsable propuesto:** Bulma S
**Revisión:** Misato K

---

## Tarea 2 — Crear/ajustar documentación del modelo
**Objetivo:**
Actualizar `docs/03-modules/models/core_unitys.md` con estructura final, reglas de negocio, índices y constraints.

**Entregable:**
- documento actualizado y coherente con migración real

**Responsable propuesto:** Misato K
**Apoyo:** Bulma S

---

## Tarea 3 — Implementar módulo DDD `core_unitys`
**Objetivo:**
Crear la estructura completa:

```
core_unitys/
├── domain/
│   ├── unity_entity.py
│   ├── unity_data.py
│   ├── unity_exception.py
│   ├── unity_success.py
│   ├── unity_repository.py
│   ├── unity_cmd_repository.py
│   └── unity_query_repository.py
├── infrastructure/
│   ├── dbunitys.py
│   ├── unity_mapper.py
│   ├── unity_cmd_repository.py
│   └── unity_query_repository.py
└── usecase/
    ├── unity_cmd_schema.py
    ├── unity_cmd_usecase.py
    ├── unity_query_usecase.py
    ├── unity_usecase.py
    └── unity_factory.py
```

**Responsable propuesto:** Bulma S
**Revisión arquitectónica:** Lelouch S
**Coordinación:** Misato K

---

## Tarea 4 — Exponer API routes
**Objetivo:**
Agregar endpoints siguiendo patrón de `core_buildings`.

### Endpoints mínimos
- `POST /unitys`
- `GET /unitys/{id}`
- `GET /unitys/uuid/{uuid}`
- `PUT /unitys/{id}`
- `DELETE /unitys/{id}`
- `POST /unitys/{id}/restore`
- `DELETE /unitys/{id}/hard`
- `GET /unitys`
- `GET /unitys/building/{building_id}`

**Responsable propuesto:** Bulma S
**Revisión:** Misato K

---

## Tarea 5 — Reglas de eliminación y restauración
**Objetivo:**
Implementar:
- soft delete por defecto
- restore
- hard delete bloqueado si hay dependencias activas

**Dependencias a revisar:**
- `users_residents`
- futuras tablas financieras/documentales

**Responsable propuesto:** Bulma S
**Revisión funcional:** Misato K

---

## Tarea 6 — Testing mínimo obligatorio
**Objetivo:**
Cubrir al menos:
- create válido
- rechazo de duplicado por `(building_id, unit_number)`
- filtros por building/status
- soft delete y restore
- hard delete bloqueado con dependencias
- validaciones de área/coefficient

**Responsable propuesto:** Bulma S
**Revisión:** Misato K

---

## Tarea 7 — Integración con `core_buildings`
**Objetivo:**
Validar que `core_buildings.count_active_units()` siga coherente con el nuevo modelo y naming.

**Observación:**
Actualmente el conteo usa SQL crudo sobre `core_unitys` con `status = 1`. Revisar si debe además excluir `deleted_at IS NOT NULL`.

**Regla final sugerida:**
- unidad activa = `status = 1 AND deleted_at IS NULL`

**Responsable propuesto:** Misato K
**Apoyo:** Bulma S

---

## 12. Orden recomendado de ejecución

1. aprobar diseño final del schema
2. crear migración Alembic
3. actualizar documentación
4. implementar DDD module
5. exponer rutas API
6. ajustar conteos/relaciones con edificios
7. agregar tests
8. revisión final funcional/arquitectónica

No invertir este orden. Si se implementa código antes de cerrar el schema, solo se fabrica retrabajo.

---

## 13. Criterios de revisión para Misato

Misato debe validar:
- coherencia entre documentación y migración
- naming correcto (`unit_number`, `private_area`, `coefficient`)
- eliminación real de redundancias (`type`)
- unicidad compuesta correcta
- constraints presentes
- índices alineados a queries reales
- semántica correcta de soft delete
- consistencia con estrategia del dominio y roadmap

---

## 14. Criterios de ejecución para Bulma

Bulma debe ejecutar con estas reglas:
- no inventar campos fuera del plan sin aprobación
- no volver a introducir `type` texto libre
- no dejar `code` con unicidad global
- no usar `name` como identidad principal
- no omitir `deleted_at`
- no omitir tests mínimos
- seguir el patrón de `core_buildings` para estructura, pero no copiar ciegamente donde la semántica de unidad difiere

---

## 15. Riesgos si se ejecuta mal

- inconsistencias entre tipo libre y catálogo
- unidades duplicadas dentro del mismo edificio
- imposibilidad de crecer hacia cobranza/ledger
- soft delete inexistente y pérdida de trazabilidad
- conteos erróneos por no excluir eliminados
- deuda técnica mayor al pasar a residentes/finanzas

---

## 16. Condición para pasar a implementación

**No ejecutar desarrollo del módulo hasta tener aprobación explícita.**

Flujo recomendado:
1. Mike revisa este plan
2. aprueba o ajusta
3. Misato coordina ejecución
4. Bulma implementa
5. Lelouch hace revisión arquitectónica final

---

## 17. Veredicto final

`core_unitys` debe dejar de ser una tabla genérica y convertirse en una pieza operativa real del sistema.

La jugada correcta no es “hacer CRUD de departamentos”.
La jugada correcta es construir la base que luego sostendrá ocupación, residentes, cobro, tickets y reportes sin rehacer media arquitectura.

Ese es el movimiento que protege al Rey.
