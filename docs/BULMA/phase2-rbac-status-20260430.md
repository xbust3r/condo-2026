# Phase 2 — RBAC Implementation Status

**Última actualización:** 2026-04-30
**Commit:** `a8650b6`
**Estado:** ✅ Implementado (tablas + enforcement)

---

## Resumen

| Componente | Estado |
|---|---|
| Tabla `core_permissions` | ✅ 63 permisos seedeados |
| Tabla `core_role_permissions` | ✅ 88 mappings seedeados |
| Tabla `core_condominium_roles` | ✅ extendida con scope/building_id |
| Endpoint enforcement (`rbac_required`) | ✅ 17/35 módulos protegidos |

---

## Permisos por Recurso (63 total)

| Recurso | Permisos |
|---|---|
| `amenities` | read, create, update, delete |
| `announcement` | read, write, create, delete |
| `ar` (accounts_receivable) | read, write, delete |
| `audit` | read |
| `building` | read, create, update, delete |
| `charge` | read, write, delete |
| `charge_type` | read, write |
| `condominium` | read, create, update, delete |
| `document` | read, write, delete |
| `finance` | read, write, approve, export |
| `incident` | read, create, update, delete, escalate, assign |
| `ledger` | read, write, export |
| `maintenance` | read, create, update |
| `notifications` | read, read_all, delete |
| `payment` | read, write, delete |
| `receipt` | read, write |
| `role` | read, assign |
| `unit` | read, create, update, delete |
| `user` | read, assign_role |
| `visitors` | read, create, checkin, cancel |
| `visitor_log` | read, write |

---

## Roles y Permisos (88 mappings)

| Rol | Permisos asignados |
|---|---|
| `board_member` | condominium.read, finance.read/approve/export |
| `condominium_admin` | 20 permisos: todos los recursos operación + finanzas + usuarios |
| `finance_reviewer` | finance.read/approve/export, announcement.read, role.read |
| `maintenance_staff` | maintenance.read/create/update, building.read, unit.read |
| `operations_staff` | announcement.read/create, building.read, visitor_log.read/write, amenity.read/create, unit.read |
| `resident` | incident.read/create, maintenance.read/create, unit.read, announcement.read |
| `security_staff` | incident.read/create/update, visitors.read/create/checkin/cancel, building.read, unit.read, visitor_log.read/write |
| `super_admin` | todos los permisos (todos los recursos) |

---

## Módulos con RBAC Enforcement (17)

| Módulo | Permisos | Estado |
|---|---|---|
| `buildings` | building.read/write/delete | ✅ |
| `units` | unit.read/write/delete | ✅ |
| `unit_types` | unit_type.read/write | ✅ |
| `charges` | charge.read/write/delete | ✅ |
| `incidents` | incident.read/create/update/delete/escalate/assign | ✅ |
| `visitors` | visitors.read/create/checkin/cancel | ✅ |
| `votes` | votes.read/create/cancel/vote | ✅ |
| `payments` | payment.read/write/delete | ✅ (nuevo) |
| `receipts` | receipt.read/write | ✅ (nuevo) |
| `accounts_receivable` | ar.read/write/delete | ✅ (nuevo) |
| `charge_types` | charge_type.read/write | ✅ (nuevo) |
| `ledger_entries` | ledger.read/write | ✅ (nuevo) |
| `announcements` | announcement.read/write/delete | ✅ (nuevo) |
| `documents` | document.read/write/delete | ✅ (nuevo) |
| `amenities` | amenities.read/create/update/delete | ✅ (nuevo) |
| `condominiums` | condominium.read/create/update/delete | ✅ (nuevo) |
| `audit_logs` | audit.read | ✅ (nuevo) |

---

## Módulos Sin RBAC Endpoint Enforcement (18)

| Módulo | Razón |
|---|---|
| `auth` | Endpoints públicos (login, register) |
| `notifications` | Auth per-user via `get_current_user` (no necesita RBAC global) |
| `permissions` | Solo super_admin via seed |
| `role_permissions` | Solo super_admin via seed |
| `condominium_roles` | Solo super_admin via seed |
| `occupancy_types` | Catálogo/config, sin control granular |
| `building_types` | Catálogo/config, sin control granular |
| `unit_occupancies` | Hereda permisos de unit/role |
| `unit_ownerships` | Hereda permisos de unit/role |
| `user_profiles` | Hereda de user.auth |
| `users` | Hereda de user.auth |
| `residents` | Perfil calculado desde occupancy |
| `meetings` | Hereda de announcement permissions |
| `packages` | Baja prioridad operativa |
| `votes` sub-tables | Gobernados por module padre |
| `core_*` modules internos | Infrastructure-only, sin API routes públicas |

---

## Reglas RBAC Implementadas

### RBAC-01: `condominium_admin` = 1 por condominio
```python
if role == 'condominium_admin':
    existing = repo.get_active(condominium_id, role='condominium_admin')
    if existing:
        raise ValueError("Ya existe un condominium_admin en este condominio")
```

### RBAC-02: `super_admin` no asignable por API
```python
if role == 'super_admin':
    raise PermissionError("super_admin solo se asigna via seed de DB")
```

### RBAC-03: `resident` es cálculo, no asignación
```python
def get_effective_resident_context(user_id, unit_id):
    occ = occupancy_repo.get_primary_active(user_id, unit_id)
    if occ and occ.type in ('resident_owner', 'tenant'):
        return {'role': 'resident', 'scope': 'unit', 'unit_id': unit_id}
```

### RBAC-04: Scope enforcement
```python
def require_permission(user, resource, action, scope, target_id=None):
    # global: sin FK a condominium/unit
    # condominium: recurso.condominium_id == ctx.condominium_id
    # unit: recurso.unit_id == ctx.unit_id
    # building: recurso.building_id == ctx.building_id
```

---

## Historial de Cambios

| Fecha | Commit | Cambio |
|---|---|---|
| 2026-04-14 | 3ad3f55 | Phase 1 — 5 HIGHs corregidos |
| 2026-04-24 | sprint15 | Backdmin — 28 detail pages + contexts |
| 2026-04-29 | e85660c | Incidente DNS condopy-api resuelto |
| 2026-04-30 | 0130239 | Tablas financieras creadas + limpieza migraciones |
| 2026-04-30 | a8650b6 | Phase 2 RBAC enforcement — 11 módulos protegidos |

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*
