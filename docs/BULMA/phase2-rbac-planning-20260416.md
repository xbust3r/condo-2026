# Phase 2 — RBAC Planning
**Date:** 2026-04-16
**Author:** Misato K · **Repo:** `/home/miguel/servers/condo-py`

---

## Resumen Ejecutivo

Se extiende el sistema RBAC existente (`core_condominium_roles`) con un modelo de permisos granular basado en recursos y acciones. El modelo permite control por scope (`global` / `condominium` / `unit` / `building`), con roles predefinidos y una tabla pivot que mapea roles a permisos específicos.

---

## Modelo de Datos

### Tablas Involucradas

| Tabla | Cambio |
|-------|--------|
| `core_condominium_roles` | Modify: agregar `scope`, `building_id`, unique constraint para `condominium_admin` |
| `core_permissions` | **Nueva**: catálogo de permisos estático |
| `core_role_permissions` | **Nueva**: pivot rol → permisos |

---

### Estructura `core_condominium_roles` (modificada)

```sql
ALTER TABLE core_condominium_roles
  ADD COLUMN scope       VARCHAR(20) DEFAULT 'condominium',
  ADD COLUMN building_id BIGINT NULL,
  ADD CONSTRAINT unique_condo_admin_role
    UNIQUE (condominium_id, role)
    -- solo para role='condominium_admin'
```

**Scopes válidos:** `condominium` | `unit` | `building`

---

### Estructura `core_permissions` (nueva)

```sql
CREATE TABLE core_permissions (
  id          BIGINT PK AUTO_INCREMENT,
  code        VARCHAR(100) UNIQUE NOT NULL,  -- 'condominium.read', 'finance.approve', etc.
  resource    VARCHAR(50)  NOT NULL,          -- 'condominium', 'unit', 'finance', 'incident'
  action      VARCHAR(30)  NOT NULL,          -- 'read', 'create', 'update', 'delete', 'approve', 'export'
  scope_default VARCHAR(20) DEFAULT 'condominium',
  description VARCHAR(255),
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Seed data (~30 rows):**

```
condominium.read       | condominium | read    | condominium
condominium.create     | condominium | create  | condominium
condominium.update     | condominium | update  | condominium
condominium.delete     | condominium | delete  | global

building.read          | building    | read    | condominium
building.create        | building    | create  | condominium
building.update        | building    | update  | condominium
building.delete        | building    | delete  | global

unit.read              | unit        | read    | unit
unit.create            | unit        | create  | condominium
unit.update            | unit        | update  | condominium
unit.delete            | unit        | delete  | global

user.read              | user        | read    | condominium
user.assign_role       | user        | assign  | condominium

role.read              | role        | read    | condominium
role.assign            | role        | assign  | condominium

finance.read           | finance     | read    | condominium
finance.approve        | finance     | approve | condominium
finance.export         | finance     | export  | condominium
finance.write          | finance     | write   | condominium

incident.read          | incident    | read    | condominium
incident.create        | incident    | create  | unit
incident.update        | incident    | update  | condominium

maintenance.read       | maintenance | read    | condominium
maintenance.create     | maintenance | create  | unit
maintenance.update     | maintenance | update  | condominium

announcement.read      | announcement | read    | condominium
announcement.create    | announcement | create  | condominium
announcement.delete    | announcement | delete  | condominium

visitor_log.read       | visitor_log  | read    | condominium
visitor_log.write      | visitor_log  | write   | condominium
```

---

### Estructura `core_role_permissions` (nueva)

```sql
CREATE TABLE core_role_permissions (
  role              VARCHAR(40) NOT NULL,
  permission_code   VARCHAR(100) NOT NULL,
  scope_override    VARCHAR(20) NULL,  -- NULL = usa default del permission
  PRIMARY KEY (role, permission_code),
  FOREIGN KEY (permission_code) REFERENCES core_permissions(code)
);
```

**Seed data:**

```
super_admin        → todos los permisos (28 rows)
condominium_admin  → todos exceto finance.approve, finance.export (global only)
board_member       → finance.read, finance.approve, finance.export, condominium.read
finance_reviewer   → finance.read, finance.approve, finance.export, announcement.read
security_staff     → incident.read, incident.create, incident.update, visitor_log.read, visitor_log.write, unit.read, building.read
maintenance_staff  → maintenance.read, maintenance.create, maintenance.update, building.read, unit.read
operations_staff   → announcement.read, announcement.create, building.read, visitor_log.read, amenity.read, amenity.write, booking.read, booking.write
resident           → incident.read, incident.create, maintenance.read, maintenance.create, unit.read, announcement.read
```

---

## Reglas de Negocio

### RBAC-01: `condominium_admin` = 1 por condominio
```python
# En create/update del usecase
if role == 'condominium_admin':
    existing = repo.get_active(condominium_id, role='condominium_admin')
    if existing:
        raise ValueError("Ya existe un condominium_admin en este condominio")
```

### RBAC-02: `super_admin` no asignable por API
```python
# En CondominiumRoleUseCase.create/update
if role == 'super_admin':
    raise PermissionError("super_admin solo se asigna via seed de DB")
```

### RBAC-03: `resident` es cálculo, no asignación
```python
# Se calcula dinámicamente desde core_unit_occupancies
def get_effective_resident_context(user_id, unit_id):
    occ = occupancy_repo.get_primary_active(user_id, unit_id)
    if occ and occ.type in ('resident_owner', 'tenant'):
        return {'role': 'resident', 'scope': 'unit', 'unit_id': unit_id}
    return None
```

### RBAC-04: `maintenance_staff` / `operations_staff` por building
```sql
-- Un staff puede tener N buildings asignados via N filas
SELECT * FROM core_condominium_roles
WHERE user_id=? AND role IN ('maintenance_staff','operations_staff')
AND building_id IN (?,?,?);
```

### RBAC-05: Scope enforcement en permission check
```python
def require_permission(user, resource, action, scope, target_id=None):
    # global:   sin FK a condominium/unit
    # condominium: recurso.condominium_id == ctx.condominium_id
    # unit:     recurso.unit_id == ctx.unit_id AND unidad.condominium_id == ctx.condominium_id
    # building: recurso.building_id == ctx.building_id
```

---

## Migraciones

| # | Archivo | Descripción |
|---|---------|-------------|
| 021 | `021_extend_condominium_roles_scope_building.sql` | Agrega `scope`, `building_id` + unique constraint `condominium_admin` |
| 022 | `022_create_core_permissions.sql` | Crea tabla + seed 30 permisos |
| 023 | `023_create_core_role_permissions.sql` | Crea pivot + seed mapping roles→permisos |

---

## Permisos Detallados por Rol

| Permiso | super_admin | condo_admin | board_member | finance_reviewer | security_staff | maintenance_staff | operations_staff | resident |
|---------|-------------|-------------|--------------|------------------|----------------|-------------------|------------------|----------|
| condominium.read | ✅ | ✅ | ✅ | | | | | |
| condominium.create | ✅ | ✅ | | | | | | |
| condominium.update | ✅ | ✅ | | | | | | |
| condominium.delete | ✅ | | | | | | | |
| building.read | ✅ | ✅ | | | ✅ | ✅ | ✅ | |
| building.create | ✅ | ✅ | | | | | | |
| building.update | ✅ | ✅ | | | | | | |
| building.delete | ✅ | | | | | | | |
| unit.read | ✅ | ✅ | | | ✅ | ✅ | | ✅ |
| unit.create | ✅ | ✅ | | | | | | |
| unit.update | ✅ | ✅ | | | | | | |
| unit.delete | ✅ | | | | | | | |
| user.read | ✅ | ✅ | | | | | | |
| user.assign_role | ✅ | ✅ | | | | | | |
| role.read | ✅ | ✅ | | | | | | |
| role.assign | ✅ | ✅ | | | | | | |
| finance.read | ✅ | ✅ | ✅ | ✅ | | | | |
| finance.approve | ✅ | | ✅ | ✅ | | | | |
| finance.export | ✅ | | ✅ | ✅ | | | | |
| finance.write | ✅ | ✅ | | | | | | |
| incident.read | ✅ | ✅ | | | ✅ | | | ✅ |
| incident.create | ✅ | ✅ | | | ✅ | | | ✅ |
| incident.update | ✅ | ✅ | | | ✅ | | | |
| maintenance.read | ✅ | ✅ | | | | ✅ | | ✅ |
| maintenance.create | ✅ | ✅ | | | | ✅ | | ✅ |
| maintenance.update | ✅ | ✅ | | | | ✅ | | |
| announcement.read | ✅ | ✅ | | ✅ | | | ✅ | ✅ |
| announcement.create | ✅ | ✅ | | | | | ✅ | |
| announcement.delete | ✅ | ✅ | | | | | | |
| visitor_log.read | ✅ | ✅ | | | ✅ | | ✅ | |
| visitor_log.write | ✅ | ✅ | | | ✅ | | | |

---

## Tareas de Implementación

### Fase 1: Migraciones (Archivos .py en alembic/versions/)
- [ ] `021_extend_condominium_roles_scope_building.py`
- [ ] `022_create_core_permissions.py`
- [ ] `023_create_core_role_permissions.py`

### Fase 2: Domain Layer
- [ ] Crear `dddpy/core_permissions/` (domain, infrastructure, usecase)
- [ ] Crear `dddpy/core_role_permissions/`
- [ ] Entidades: `PermissionEntity`, `RolePermissionEntity`
- [ ] Repos: `PermissionQueryRepository`, `RolePermissionQueryRepository`
- [ ] Excepciones: `PermissionNotFound`, `RolePermissionNotFound`

### Fase 3: Permission Check Engine
- [ ] `rbac_dependencies.py` refactor: `require_permission(resource, action)` nuevo
- [ ] `PermissionService`: `has_permission(user, resource, action, scope, target_id)`
- [ ] `get_effective_resident_context(user_id, unit_id)` — cálculo dinámic

### Fase 4: Usecase Updates
- [ ] `CondominiumRoleUseCase`: validar `condominium_admin` unique, `super_admin` no asignable
- [ ] `CondominiumRoleEntity`: agregar `VALID_SCOPES = {'condominium', 'unit', 'building'}`

### Fase 5: Routes + Enforcement
- [ ] Proteger endpoints existentes con `require_permission()`
- [ ] Seed `super_admin` en DB (bootstrap)
- [ ] Tests de integración RBAC

---

## Dependencias

- `core_condominium_roles` existe (migración 014)
- `core_unit_occupancies` existe (migración 013) — para cálculo `resident`
- No hay nuevas dependencias de módulos

---

## Riesgos

| Riesgo | Mitigación |
|--------|------------|
| Breaking change en `rbac_dependencies` actual | Mantener `require_condominium_role()` como wrapper compatible |
| Performance en `has_permission` con N queries | Cachear permisos en memoria por sesión/user |
| `resident` calculado en cada request | Materializar en `core_condominium_roles` con trigger o job async |
