# Módulos del Sistema condo-py

**Última actualización:** 2026-04-30
**Estado:** 29 módulos implementados — todos los módulos Phase 1 y Phase 2 cerrados

---

## Estado General

| Estado | Significado |
|---|---|
| ✅ | Implementado completamente en Python + DDD + API routes + tabla DB |
| ⚠️ | Deprecado o en limpieza |

---

## Módulos Implementados

### ✅ Módulo shared — Componentes Compartidos
**Ruta:** `src/library/dddpy/shared/`

Decorators, schemas, logging, MySQL/PostgreSQL session manager, utils.

---

### ✅ Módulo example — Plantilla de Referencia DDD
**Ruta:** `src/library/dddpy/example/`

Plantilla que define el patrón arquitectónico. **NO es lógica de negocio real.**

---

### ✅ core_condominiums — Gestión de Condominios
**Ruta:** `src/library/dddpy/core_condominiums/`
**Tabla DB:** `core_condominiums`
**API:** `src/api/condominiums/routes_condominiums.py`

---

### ✅ core_buildings — Torres/Edificios
**Ruta:** `src/library/dddpy/core_buildings/`
**Tabla DB:** `core_buildings`
**API:** `src/api/buildings/routes_buildings.py`

---

### ✅ core_buildings_types — Tipos de Edificio
**Ruta:** `src/library/dddpy/core_buildings_types/`
**Tabla DB:** `core_buildings_types`
**API:** `src/api/buildings_types/routes_building_types.py`

---

### ✅ core_units — Unidades Inmobiliarias
**Ruta:** `src/library/dddpy/core_units/`
**Tabla DB:** `core_units`
**API:** `src/api/units/routes_units.py`

---

### ✅ core_unit_types — Tipos de Unidad
**Ruta:** `src/library/dddpy/core_unit_types/`
**Tabla DB:** `core_unit_types`
**API:** `src/api/unit_types/routes_unit_types.py`

---

### ✅ core_unit_ownerships — Titularidad de Unidades
**Ruta:** `src/library/dddpy/core_unit_ownerships/`
**Tabla DB:** `core_unit_ownerships`
**API:** `src/api/unit_ownerships/routes_unit_ownerships.py`

---

### ✅ core_unit_occupancies — Ocupación de Unidades
**Ruta:** `src/library/dddpy/core_unit_occupancies/`
**Tabla DB:** `core_unit_occupancies`
**API:** `src/api/unit_occupancies/routes_unit_occupancies.py`

---

### ✅ core_condominium_roles — Roles por Condominio
**Ruta:** `src/library/dddpy/core_condominium_roles/`
**Tabla DB:** `core_condominium_roles`
**API:** `src/api/condominium_roles/routes_condominium_roles.py`

---

### ✅ core_charge_types — Catálogo de Tipos de Cargo
**Ruta:** `src/library/dddpy/core_charge_types/`
**Tabla DB:** `core_charge_types` (5 tipos seedeados)
**API:** `src/api/charge_types/routes_charge_types.py`

---

### ✅ core_charges — Cargos Recurrentes y Extraordinarios
**Ruta:** `src/library/dddpy/core_charges/`
**Tabla DB:** `core_charges`
**API:** `src/api/charges/routes_charges.py`

---

### ✅ core_accounts_receivable — Cuentas por Cobrar
**Ruta:** `src/library/dddpy/core_accounts_receivable/`
**Tabla DB:** `core_accounts_receivable`
**API:** `src/api/accounts_receivable/routes_accounts_receivable.py`

---

### ✅ core_payments — Pagos
**Ruta:** `src/library/dddpy/core_payments/`
**Tabla DB:** `core_payments`
**API:** `src/api/payments/routes_payments.py`

---

### ✅ core_receipts — Recibos de Pago
**Ruta:** `src/library/dddpy/core_receipts/`
**Tabla DB:** `core_receipts`
**API:** `src/api/receipts/routes_receipts.py`

---

### ✅ core_ledger_entries — Libro Mayor por Unidad
**Ruta:** `src/library/dddpy/core_ledger_entries/`
**Tabla DB:** `core_ledger_entries` (8 filas seedeadas)
**API:** `src/api/ledger_entries/routes_ledger.py`

---

### ✅ core_announcements — Avisos
**Ruta:** `src/library/dddpy/core_announcements/`
**Tabla DB:** `core_announcements`
**API:** `src/api/announcements/routes_announcements.py`

---

### ✅ core_meetings — Asambleas
**Ruta:** `src/library/dddpy/core_meetings/`
**Tabla DB:** `core_meetings`
**API:** `src/api/meetings/routes_meetings.py`

---

### ✅ core_documents — Documentos
**Ruta:** `src/library/dddpy/core_documents/`
**Tabla DB:** `core_documents`
**API:** `src/api/documents/routes_documents.py`

---

### ✅ core_incidents — Incidentes
**Ruta:** `src/library/dddpy/core_incidents/`
**Tabla DB:** `core_incidents`
**API:** `src/api/incidents/routes_incidents.py`

---

### ✅ core_notifications — Notificaciones
**Ruta:** `src/library/dddpy/core_notifications/`
**Tabla DB:** `core_notifications`
**API:** `src/api/notifications/routes_notifications.py`

---

### ✅ core_visitors — Registro de Visitantes
**Ruta:** `src/library/dddpy/core_visitors/`
**Tabla DB:** `core_visitors`
**API:** `src/api/visitors/routes_visitors.py`

---

### ✅ core_amenities — Amenidades
**Ruta:** `src/library/dddpy/core_amenities/`
**Tabla DB:** `core_amenities`
**API:** `src/api/amenities/routes_amenities.py`

---

### ✅ core_packages — Paquetería
**Ruta:** `src/library/dddpy/core_packages/`
**Tabla DB:** `core_packages`
**API:** `src/api/packages/routes_packages.py`

---

### ✅ core_votes — Votaciones
**Ruta:** `src/library/dddpy/core_votes/`
**Tabla DB:** `core_votes`
**API:** `src/api/votes/routes_votes.py`

---

### ✅ core_audit_logs — Log de Auditoría
**Ruta:** `src/library/dddpy/core_audit_logs/`
**Tabla DB:** `core_audit_logs`
**API:** `src/api/audit_logs/routes_audit_logs.py`

---

### ✅ core_residents — Perfil Residente
**Ruta:** `src/library/dddpy/core_residents/`
**Tabla DB:** `core_resident_profiles`
**API:** `src/api/residents/routes_residents.py`

---

### ✅ core_permissions — Catálogo de Permisos RBAC
**Ruta:** `src/library/dddpy/core_permissions/`
**Tabla DB:** `core_permissions` (63 permisos seedeados)
**API:** `src/api/permissions/routes_permissions.py`

---

### ✅ core_role_permissions — Mapeo Rol → Permisos
**Ruta:** `src/library/dddpy/core_role_permissions/`
**Tabla DB:** `core_role_permissions` (88 mappings seedeados)
**API:** `src/api/role_permissions/routes_role_permissions.py`

---

### ✅ users — Usuarios del Sistema
**Tabla DB:** `users` (auth: email, password_hash, status, security fields)
**API:** `src/api/users/routes_users.py`

---

### ✅ user_profiles — Perfil Humano
**Tabla DB:** `user_profiles` (1:1 con users: first_name, last_name, doc_identity, phone)
**API:** `src/api/user_profiles/routes_user_profiles.py`

---

### ✅ auth_sessions — Sesiones de Auth
**Tabla DB:** `auth_sessions`

---

## Módulos Deprecados

### ⚠️ users_residents — Tabla Deprecada
**Estado:** DEPRECADO — solo referencia histórica. NO usar en código nuevo.
**Reemplazo:** `core_unit_ownerships` + `core_unit_occupancies` + `core_condominium_roles`

---

## Estado de Tablas DB (2026-04-30)

```
alembic_version           auth_sessions
core_accounts_receivable  core_announcements
core_audit_logs          core_buildings
core_buildings_types     core_charge_types
core_charges             core_condominium_roles
core_condominiums        core_documents
core_incidents           core_ledger_entries
core_notifications      core_packages
core_payments           core_permissions
core_receipts            core_resident_profiles
core_role_permissions    core_unit_occupancies
core_unit_ownerships     core_unit_types
core_units              core_visitors
user_profiles            users
users_residents
```

**Total: 29 tablas de negocio + 1 alembic_version**

---

## Hitos Cerrados

| Fecha | Hito |
|---|---|
| 2026-04-14 | Fase 1 — 5 HIGHs corregidos (soft delete, tipado, capas) |
| 2026-04-24 | Sprint 1-15 backdmin — 28 detail pages + contexts |
| 2026-04-29 | Incidente DNS condopy-api resuelto + documentado |
| 2026-04-30 | Tablas financieras creadas (charges, AR, payments, receipts) |

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*
