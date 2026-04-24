# Análisis de Integración: users · roles · propietarios · tipo de ocupación
## Proyecto: backdmin — condo-py
**Autor:** Misato K (Coordinadora)
**Fecha:** 2026-04-24
**Destinatario:** Lelouch (Architect) — para asignación de responsables

---

## 1. Resumen Ejecutivo

Los cuatro módulos forman la columna vertebral de la identidad y autorización de usuarios en el sistema. La integración ya está parcialmente implementada (phase 1e completa), pero quedan **brechas de consistencia, datos y lógica de negocio** que deben resolverse antes de cerrar el módulo.

---

## 2. Inventario de Módulos

### 2.1 `core_users` ✅ Implementado
**Tabla:** `users`
**Rutas:** `/users`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| email | VARCHAR(255) | Unique |
| password_hash | VARCHAR(255) | |
| status | ENUM('active','suspended','inactive','locked') | |
| email_verified_at | DATETIME | |
| last_login_at | DATETIME | |
| failed_login_attempts | INT | |
| locked_until | DATETIME | |
| token_version | INT | invalidación de sesiones |
| created_at | DATETIME | |
| updated_at | DATETIME | |
| deleted_at | DATETIME | soft delete |

**Entidad:** `UserEntity` — tiene `full_name` calculado desde profile
**Usecase:** `UserUseCase` — create, list, get, update, soft_delete, suspend, restore, activate
**Endpoint clave:** `GET /users/{id}/consolidated-view` — devuelve user + profile + roles + ownerships + occupancies

---

### 2.2 `core_user_profiles` ✅ Implementado
**Tabla:** `user_profiles` (1:1 con users)

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| user_id | BIGINT FK → users.id | Unique |
| first_name | VARCHAR(100) | |
| last_name | VARCHAR(100) | |
| document_type | ENUM('dni','ce','passport','other') | |
| document_number | VARCHAR(20) | |
| phone | VARCHAR(20) | |
| birth_date | DATE | agregado en migración 018 |
| created_at | DATETIME | |
| updated_at | DATETIME | |

**Entidad:** `UserProfileEntity`
**Rutas:** `/user-profiles`

---

### 2.3 `core_condominium_roles` ✅ Implementado
**Tabla:** `core_condominium_roles`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK | |
| user_id | BIGINT FK → users.id | |
| role | ENUM(...) | 8 roles válidos |
| status | ENUM('active','inactive','historical') | |
| scope | ENUM('condominium','unit','building') | desde mig. 021 |
| building_id | BIGINT NULL | desde mig. 021 |
| start_date | DATE | |
| end_date | DATE | |
| created_at | DATETIME | |

**Roles válidos:** `super_admin`, `condominium_admin`, `board_member`, `finance_reviewer`, `security_staff`, `maintenance_staff`, `operations_staff`
**Rutas:** `/condominium-roles` — 12 endpoints

**Reglas de negocio implementadas:**
- RBAC-01: 1 `condominium_admin` por condominio (validación en usecase)
- RBAC-02: `super_admin` no asignable por API
- RBAC-05: scope enforcement en `require_permission()` (parcial — building/unit)

---

### 2.4 `core_occupancy_types` ✅ Implementado (migración 025 — 2026-04-23)
**Tabla:** `core_occupancy_types`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| code | VARCHAR(50) | ej. `resident_owner` |
| name | VARCHAR(255) | ej. `Propietario Residente` |
| description | TEXT | |
| scope | ENUM('system','condominium') | |
| condominium_id | BIGINT NULL | para tipos custom |
| requires_authorization | BOOL | |
| allows_primary | BOOL | |
| is_active | BOOL | |
| sort_order | INT | |
| created_at | DATETIME | |

**Seed (5 tipos base):**

| ID | code | name | requires_auth | allows_primary |
|----|------|------|---------------|----------------|
| 1 | resident_owner | Propietario Residente | ❌ | ✅ |
| 2 | tenant | Inquilino | ✅ | ✅ |
| 3 | family_member | Familiar | ✅ | ❌ |
| 4 | office_user | Usuario de Oficina | ✅ | ❌ |
| 5 | occasional_user | Usuario Ocasional | ✅ | ❌ |

---

### 2.5 `core_unit_occupancies` ✅ Implementado (migración 013 + 026)
**Tabla:** `core_unit_occupancies` — quién vive en qué unidad

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| unit_id | BIGINT FK | |
| user_id | BIGINT FK → users.id | |
| occupancy_type_id | BIGINT FK → core_occupancy_types.id | **migrado de string** |
| status | ENUM('active','inactive','historical','pending') | |
| start_date | DATE | |
| end_date | DATE | |
| is_primary | BOOL | |
| authorized_by_user_id | BIGINT FK NULL | |
| notes | TEXT | |

**Entidad:** `UnitOccupancyEntity`
**Rutas:** `/unit-occupancies`

---

### 2.6 `core_unit_ownerships` 🔄 En construcción (migración 012)
**Tabla:** `core_unit_ownerships` — quién es dueño de qué unidad

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| unit_id | BIGINT FK | |
| user_id | BIGINT FK → users.id | |
| ownership_type_id | BIGINT FK | |
| percentage | DECIMAL(5,2) | porcentaje de propiedad |
| status | ENUM('active','inactive','historical') | |
| start_date | DATE | |
| end_date | DATE | |
| created_at | DATETIME | |

**Estado:** DDD module existente en `src/library/dddpy/core_unit_ownerships/` — migraciones 012 aplicadas

---

### 2.7 `core_permissions` + `core_role_permissions` ✅ Implementado
**Tablas:** `core_permissions` (022) + `core_role_permissions` (023)
**Rutas:** `/permissions` + `/role_permissions`
**Servicio:** `PermissionService` en `library/dddpy/auth/permission_service.py`

| Tabla | Función |
|-------|---------|
| core_permissions | Catálogo de ~30 permisos (resource.action) |
| core_role_permissions | Pivot rol → permisos con scope_override |

---

## 3. Diagrama de Relaciones

```
users (1)──────(1) user_profiles
  │
  │  N:N via core_condominium_roles
  │
  └───(N) core_condominium_roles ──(FK)─── core_condominiums
                │
                │  N:N via core_role_permissions
                │
                └───(N) core_role_permissions ──(FK)─── core_permissions
                                   │
                                   │  (residency es cálculo, no asignación)
                                   │  RBAC-03: resident = UnitOccupancyEntity
                                   │  con occupancy_type IN ('resident_owner','tenant')
                                   │
users ──(N) core_unit_occupancies ──(FK)─── core_occupancy_types
  │
  │ (ownership)
  │
  └───(N) core_unit_ownerships ──(FK)─── ownership_type
```

**Clave:** `core_unit_occupancies.occupancy_type_id` → `core_occupancy_types.id`
La migración 026 ya migró de string codes → FK IDs.

---

## 4. Brechas de Integración Detectadas

### 4.1 Brecha ALTA — `OccupancyTypeEntity` desactualizado
**Archivo:** `src/library/dddpy/core_occupancy_types/domain/occupancy_type_entity.py`
**Problema:** La entidad aún usa campos old: `occupancy_type: str` en `UnitOccupancyEntity.to_dict()` sigue referenciando `occupancy_type_code` (string). El campo correcto es `occupancy_type_id` (FK bigint).
**Impacto:** `get_effective_resident_context()` en `PermissionService` aún compara strings (`"resident_owner"`, `"tenant"`) en lugar de usar los IDs del catálogo (1, 2).
**Fix requerido:** Actualizar mapper + query repository para usar `occupancy_type_id` en vez de `occupancy_type` string.

### 4.2 Brecha ALTA — `get_effective_resident_context` con lógica híbrida
**Archivo:** `src/library/dddpy/auth/permission_service.py`
**Problema:**
```python
if occ.occupancy_type not in ("resident_owner", "tenant"):  # STRING comparison
```
Debería comparar contra `occupancy_type_id` (1, 2) del catálogo. La migración 026 ya migró la columna a FK, pero el servicio aún opera con strings.
**Fix requerido:** Consultar el catálogo `core_occupancy_types` para obtener los IDs de los tipos que otorgan rol `resident`, o almacenar `allows_primary=True AND requires_authorization=False` como proxy.

### 4.3 Brecha MEDIA — `consolidated-view` no incluye ownerships ni occupancy details
**Archivo:** `src/library/dddpy/core_users/usecase/user_usecase.py`
**Problema:** El endpoint `GET /users/{id}/consolidated-view` hace JOIN con `core_unit_ownerships` y `core_unit_occupancies` pero no enriquece con los datos del catálogo (`occupancy_type_name`, `ownership_type_name`).
**Fix requerido:** Los queries de ownership y occupancy deben hacer JOIN con los catálogos correspondientes.

### 4.4 Brecha MEDIA — `core_occupancy_types` permite crear tipos por condominium
**Archivo:** `OccupancyTypeEntity._validate_invariants()`
**Problema:** El flag `scope = "condominium"` existe para permitir tipos custom por condominio, pero no hay ningún endpoint ni usecase para crear/gestionar esos tipos custom. El catálogo está huérfano.
**Fix requerido:** Definir `OccupancyTypeUseCase` con endpoints CRUD para que admins de condominio puedan crear tipos propios.

### 4.5 Brecha BAJA — RBAC-03: `resident` se calcula dinámicamente
**Problema:** `get_effective_resident_context()` calcula el rol `resident` en cada request consultando `core_unit_occupancies`. Para usuarios con muchas ocupaciones (ej. propietario de una unidad, inquilino de otra), no hay forma de determinar cuál es la "primaria" a nivel de contexto general.
**Fix requerido:** Ya existe `is_primary` en `core_unit_occupancies` — el código debería usarlo:
```python
get_primary_active(user_id, unit_id)  # ya existe en UnitOccupancyQueryRepositoryImpl
```
Pero `PermissionService.get_effective_resident_context()` no filtra por `is_primary=True`.

### 4.6 Brecha BAJA — Sin endpoint para listar users por condominium con rol
**Problema:** `/users` lista todos los usuarios del sistema. `/condominium-roles/condominium/{condominium_id}` lista los roles. No hay forma directa de obtener "todos los usuarios que tienen rol en condominio X".
**Fix sugerido:** Crear `GET /condominiums/{condominium_id}/users` que combine filters de users + roles + profiles, con paginación.

---

## 5. Dependencias entre Módulos

```
migration 011 ──→ core_users + core_user_profiles
migration 012 ──→ core_unit_ownerships
migration 013 ──→ core_unit_occupancies (old occupancy_type string)
migration 014 ──→ core_condominium_roles
migration 021 ──→ extiende core_condominium_roles (scope, building_id)
migration 022 ──→ core_permissions
migration 023 ──→ core_role_permissions
migration 025 ──→ core_occupancy_types (catálogo)
migration 026 ──→ migra occupancy_type string → occupancy_type_id FK
                              ↑
                           DEPENDE DE 025
```

---

## 6. Recomendaciones de Fix por Prioridad

### PRIORIDAD 1 (antes de cerrar phase 2)
1. **Actualizar `UnitOccupancyQueryRepository`** para usar FK `occupancy_type_id` en vez de string `occupancy_type`
2. **Corregir `PermissionService.get_effective_resident_context()`** para comparar por `occupancy_type_id IN (1, 2)` (IDs del seed de `resident_owner` y `tenant`)
3. **Enriquecer `consolidated-view`** con JOIN a catálogos de occupancy_types y ownership_types

### PRIORIDAD 2 (después de phase 2)
4. **Crear `OccupancyTypeUseCase`** con endpoints CRUD para gestión de tipos (especialmente custom por condominio)
5. **Filtrar `is_primary=True`** en `get_effective_resident_context()`
6. **Agregar `GET /condominiums/{id}/users`** endpoint

---

## 7. Asignación de Responsables Sugerida

| Módulo / Fix | Sugerencia |
|---|---|
| OccupancyTypeQueryRepository + mapper | Bulma |
| PermissionService fix (ID vs string) | Bulma |
| consolidated-view enrichment | Bulma |
| OccupancyTypeUseCase CRUD | Bulma |
| Endpoint /condominiums/{id}/users | Lelouch |

---

## 8. Estado de Migraciones

| # | Archivo | Estado |
|---|---------|--------|
| 011 | refactor_users_auth_profile | ✅ aplicada |
| 012 | create_core_unit_ownerships | ✅ aplicada |
| 013 | create_core_unit_occupancies | ✅ aplicada |
| 014 | create_core_condominium_roles | ✅ aplicada |
| 021 | extend_condominium_roles_scope_building | ✅ aplicada |
| 022 | create_core_permissions | ✅ aplicada |
| 023 | create_core_role_permissions | ✅ aplicada |
| 025 | create_core_occupancy_types | ✅ aplicada |
| 026 | migrate_unit_occupancies_to_occupancy_type_id | ✅ aplicada |

Todas las migraciones relacionadas están aplicadas. El estado de la base es coherente.

---

*Documento preparado por Misato K — Coordinación condo-py*
*Para asignación de tasks, favor revisar con Lelouch (Architect)*
