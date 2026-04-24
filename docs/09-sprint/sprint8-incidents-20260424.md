# Sprint 8 — `core_incidents` — Maintenance Ticketing System

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable arquitectura:** Lelouch vi Britannia
**Responsable implementación:** Bulma

---

## Overview

Un sistema de tickets de mantenimiento/incidencias permite a residentes y propietarios reportar problemas en las unidades o áreas comunes del condominio. Es el módulo más directamente orientado al usuario final (residentes) después de la autenticación.

**Flujo básico:**
1. Usuario crea un ticket de incidencia en una unidad
2. Admin/board_member lo revisa, asigna prioridad y categoría
3. Se asigna a staff de mantenimiento o contractor externo
4. Se da seguimiento hasta resolución
5. Usuario recibe notificación de estado (cuando esté implementado `core_notifications`)

---

## Entidades del Dominio

### `IncidentEntity`

```
IncidentEntity
├── id: int
├── uuid: str
├── condominium_id: int
├── building_id: int (opcional — null si es área común)
├── unit_id: int
├── reported_by_user_id: int  ← quién reporta (debe tener occupancy u ownership activo)
├── assigned_to_user_id: int (nullable)  ← staff o contractor
├── category: IncidentCategory (enum)
├── priority: IncidentPriority (enum)
├── status: IncidentStatus (enum)
├── title: str (max 150)
├── description: str (text)
├── photos: List[str] (urls a uploads, nullable)
├── internal_notes: str (nullable)  ← solo visible para staff/admin
├── resolution_notes: str (nullable)  ← notas de resolución al cerrar
├── scheduled_date: date (nullable)
├── completed_date: date (nullable)
├── created_at, updated_at, deleted_at
└── is_escalated: bool (default false)
```

### Enums

**`IncidentStatus`:**
```
pending   → abierto, sin asignar
open      → revisado, en cola
in_progress → asignado y en ejecución
resolved  → arreglado, pendiente de confirmación
closed    → cerrado (confirmado por usuario o auto)
cancelled → cancelado por admin
```

**`IncidentPriority`:**
```
low      → no urgente
medium   → atención normal
high     → dentro de 48h
urgent   → inmediata (potencial daño estructural o seguridad)
```

**`IncidentCategory`:**
```
plumbing        → plomería
electrical     → eléctrico
structural     → estructural
common_areas   → áreas comunes
elevator       → ascensor
painting       → pintura
cleaning       → limpieza
pest_control   → control de plagas
security       → seguridad
other          → otro
```

---

## Integración con el Sistema Existente

### Dependencias del modelo actual

| Dependencia | Para qué se usa |
|---|---|
| `core_condominiums.id` | Cada incident pertenece a un condominio |
| `core_buildings.id` | Puede ser null (área común global) o edificio específico |
| `core_units.id` | El incident se reporta en una unidad específica |
| `core_unit_occupancies.user_id` | Validar que quien reporta tiene relación con la unidad (`reported_by_user_id`) |
| `core_unit_ownerships.user_id` | Alternativamente, puede reportar un propietario |
| `users.id` | Reported_by + assigned_to |
| `core_condominium_roles.role` | Solo usuarios con rol `condominium_admin`, `maintenance_staff`, `board_member` pueden crear/admin tickets. Residents pueden reportar. |

### Validaciones de negocio

**INC-01:** El usuario que reporta (`reported_by_user_id`) debe tener un `UnitOccupancyEntity` activo O un `UnitOwnershipEntity` activo en la unidad `unit_id` del incident. Caso contrario → 403.

**INC-02:** Solo usuarios con rol `condominium_admin`, `board_member` o `maintenance_staff` pueden asignar/reasignar un ticket. Residents pueden solo crear y ver los suyos.

**INC-03:** Un ticket con `priority = urgent` auto-set `is_escalated = true`.

**INC-04:** Un ticket solo puede pasar a `status = closed` si `completed_date` está seteado.

**INC-05:** El campo `assigned_to_user_id` es nullable. Un ticket sin asignar aparece en el queue de `maintenance_staff`.

---

## Estructura DDD propuesta

```
src/library/dddpy/core_incidents/
├── domain/
│   ├── incident_entity.py         ← IncidentEntity + enums
│   ├── incident_exception.py      ← IncidentNotFound, UnauthorizedIncidentAccess
│   ├── incident_repository.py     ← ABC (cmd)
│   └── incident_query_repository.py ← ABC (query)
├── infrastructure/
│   ├── dbincident.py              ← SQLAlchemy model (core_incidents table)
│   ├── incident_cmd_repository.py  ← Create, update, delete
│   └── incident_query_repository.py ← Queries enriquecidas
├── usecase/
│   ├── incident_cmd_usecase.py
│   ├── incident_query_usecase.py
│   ├── incident_factory.py
│   └── incident_cmd_schema.py      ← Pydantic input schemas
└── api/
    └── incidents/routes_incidents.py
```

### Migración sugerida

```sql
CREATE TABLE core_incidents (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  uuid VARCHAR(36) NOT NULL UNIQUE,
  condominium_id BIGINT NOT NULL,
  building_id BIGINT NULL,
  unit_id BIGINT NOT NULL,
  reported_by_user_id BIGINT NOT NULL,
  assigned_to_user_id BIGINT NULL,
  category VARCHAR(40) NOT NULL,
  priority VARCHAR(20) NOT NULL DEFAULT 'medium',
  status VARCHAR(30) NOT NULL DEFAULT 'pending',
  title VARCHAR(150) NOT NULL,
  description TEXT,
  photos JSON,
  internal_notes TEXT,
  resolution_notes TEXT,
  scheduled_date DATE NULL,
  completed_date DATE NULL,
  is_escalated BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT NOW(),
  updated_at DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  deleted_at DATETIME NULL,
  FOREIGN KEY (condominium_id) REFERENCES core_condominiums(id),
  FOREIGN KEY (building_id) REFERENCES core_buildings(id),
  FOREIGN KEY (unit_id) REFERENCES core_units(id),
  FOREIGN KEY (reported_by_user_id) REFERENCES users(id),
  FOREIGN KEY (assigned_to_user_id) REFERENCES users(id),
  INDEX idx_condo_status (condominium_id, status),
  INDEX idx_unit (unit_id),
  INDEX idx_assigned (assigned_to_user_id),
  INDEX idx_reported_by (reported_by_user_id)
);
```

---

## Endpoints propuestos

| Método | Endpoint | Permiso | Descripción |
|---|---|---|---|
| POST | `/incidents` | Authenticated | Crear incident (validado contra occupancy/ownership) |
| GET | `/incidents` | Authenticated + filtros | Listar (filtros: condo, status, priority, category, building, unit) |
| GET | `/incidents/{id}` | Authenticated | Detalle de un incident |
| GET | `/incidents/{uuid}` | Authenticated | Detalle por UUID |
| PATCH | `/incidents/{id}` | Admin/staff | Actualizar status, priority, assign, notes |
| POST | `/incidents/{id}/assign` | Admin/staff | Asignar a user_id |
| POST | `/incidents/{id}/escalate` | Admin | Escalar |
| POST | `/incidents/{id}/complete` | Admin/staff | Marcar como completado (set completed_date) |
| POST | `/incidents/{id}/close` | Admin | Cerrar |
| POST | `/incidents/{id}/cancel` | Admin | Cancelar |
| GET | `/incidents/my` | Authenticated | Mis incidents (reported_by = me) |
| GET | `/condominiums/{id}/incidents` | Authenticated | Incidents de un condominio (paginados) |

---

## Queries enriquecidas (M-10)

Igual que en M-05 para roles, los listados de incidents deben devolver:
- `reported_by_user_full_name` (from user_profiles)
- `assigned_to_user_full_name` (from user_profiles)
- `condominium_name`
- `building_name` (nullable)
- `unit_code`

Esto sigue el patrón `_bulk_enrich` ya establecido.

---

## RBAC — Permisos necesarios (nuevos)

```
incidents:create     → cualquier authenticated user con occupancy/ownership en la unidad
incidents:read       → mismo condominio ( OWNER/ TENANT + role staff/admin)
incidents:update     → maintenance_staff, board_member, condominium_admin
incidents:assign     → board_member, condominium_admin
incidents:escalate   → condominium_admin
incidents:delete     → condominium_admin
```

Seed sugerido en `core_permissions`:
```python
("incidents:create", "Create maintenance incidents"),
("incidents:read", "View incidents"),
("incidents:update", "Update incident status/priority"),
("incidents:assign", "Assign incidents to staff"),
("incidents:escalate", "Escalate urgent incidents"),
("incidents:delete", "Cancel/delete incidents"),
```

---

## Notas de diseño

1. **Photos/uploads:** El campo `photos` es JSON array de URLs. La subida de archivos es un paso posterior ( `core_documents` puede reutilizarse para esto). Por ahora se acepta que venga vacío o con URLs pre-subidas.

2. **Área común sin unit:** Si `building_id` es null, el incident es de área común global. `unit_id` también podría ser null en ese caso — considerar si el incident puede no tener unidad.

3. **Notificaciones (Phase 4 al final):** Cuando exista `core_notifications`, cada cambio de status de incident debería disparar una notificación a `reported_by_user_id` y optionally a `assigned_to_user_id`.

4. **Dashboard para staff:** El endpoint `GET /incidents?assigned_to_user_id=X&status=open,in_progress` sirve como queue de trabajo del staff.

---

## Tasks para Bulma (implementación)

| Task | Descripción |
|---|---|
| T-1 | Crear migración `040_create_core_incidents.sql` |
| T-2 | Implementar DDD completo `core_incidents` (entity, repos, usecases) |
| T-3 | Implementar routes + RBAC decorator |
| T-4 | Queries enriquecidas con `_bulk_enrich` (reported_by full name, unit_code, etc.) |
| T-5 | Seed de permisos en `core_permissions` |

---

## Siguiente paso

@Bulma — mientras implementas, si necesitas que agregue campos adicionales al modelo o ajustes en las validaciones, avísame. El modelo es flexible mientras se respete el patrón DDD.
