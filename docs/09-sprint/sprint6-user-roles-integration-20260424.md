# Sprint 6 — Análisis de Integración: Users · Roles · Propietarios · Occupancy Types
**Proyecto:** backdmin (condo-py)
**Fecha:** 2026-04-24
**Autor:** Bulma Briefs — Capsule Corp I+D
**Estado:** ANÁLISIS

---

## 1. Contexto General

Los 4 módulos bajo análisis gobiernan la identidad, autorización y relación patrimonial de los actores del sistema:

```
core_users              — Identidad y autenticación
core_condominium_roles — Roles administrativos por condominio
core_unit_ownerships   — Relación propietario ↔ unidad
core_unit_occupancies  — Relación ocupante ↔ unidad (vía occupancy_type)
core_occupancy_types   — Catálogo de tipos de ocupación
```

**Lo que ya existe (Phase 1e):** `GET /users/{id}/consolidated-view` retorna user + profile + roles + ownerships + occupancies. Eso es buen punto de partida, pero la integración tiene huecos.

---

## 2. Inventario de Entidades y Relaciones

### 2.1 Entidades y campos clave

| Módulo | Entidad | PK | FKs directos | Status lifecycle |
|---|---|---|---|---|
| `core_users` | UserEntity | id, uuid | — | active / suspended / locked / inactive / pending |
| `core_condominium_roles` | CondominiumRoleEntity | id, uuid | condominium_id, user_id, building_id | active / inactive / historical |
| `core_unit_ownerships` | UnitOwnershipEntity | id, uuid | unit_id, user_id | active / inactive / historical |
| `core_unit_occupancies` | UnitOccupancyEntity | id, uuid | unit_id, user_id, occupancy_type_id | active / inactive / historical |
| `core_occupancy_types` | OccupancyTypeEntity | id, uuid | condominium_id (opcional) | is_active (booleano, no FK) |

### 2.2 Relaciones entre módulos

```
User (1) ←─── (N) CondominiumRole   ←─── (1) Condominium
User (1) ←─── (N) UnitOwnership     ←─── (1) Unit
User (1) ←─── (N) UnitOccupancy     ←─── (1) Unit
                                         └── (N) OccupancyType
```

---

## 3. Hallazgos por Módulo

### 3.1 `core_users` ✅ — Estado: FUNCIONAL

**Lo que está bien:**
- Ciclo de vida de status completo (active → suspended → locked → inactive)
- `token_version` se incrementa en soft-delete y suspend → invalida JWTs inmediatamente
- `get_consolidated_view()` ya junta roles + ownerships + occupancies
- Soft-delete + restore + suspend + activate

**Hallazgos:**
- El `consolidated-view` no incluye nombre del condominio ni código de unidad en las relaciones — queda como IDs numéricos. Para un admin, esto es inútil sin joins.

### 3.2 `core_condominium_roles` ✅ — Estado: FUNCIONAL

**Lo que está bien:**
- 7 roles definidos: super_admin, condominium_admin, board_member, finance_reviewer, security_staff, maintenance_staff, operations_staff
- 3 scopes: condominium / building / unit
- Validación de invariants en entity (`_validate_invariants()`)
- Listados por condominio y por usuario

**Hallazgos:**
- **No hay cascade en soft-delete de usuario:** si se soft-deletea un usuario, sus roles quedan huérfanos con `user_id` pointing to a deleted user. No hay query que filtre roles con user.deleted_at IS NOT NULL.
- **No hay endpoint de "roles activos por condominio + rol específico":** no existe `GET /condominium-roles/condominium/{id}/role/{role}`.
- **No hay validación de unicidad:** ¿se puede asignar el mismo rol al mismo usuario en el mismo condominium dos veces?

### 3.3 `core_unit_ownerships` ✅ — Estado: FUNCIONAL (con reservas)

**Lo que está bien:**
- ownership_type: owner / co_owner
- ownership_percentage (DECIMAL 5,2 — 0 a 100)
- Histórico: start_date / end_date permite archival
- Listados por unit y por user

**Hallazgos:**
- **Validación OWN-01 (CRÍTICA):** No existe validación de que la suma de `ownership_percentage` de todos los `active` co-owners de una unidad no supere 100%.
  ```python
  # Esto debería existir en create/update:
  total = db.query(DBUnitOwnership).filter(
      DBUnitOwnership.unit_id == unit_id,
      DBUnitOwnership.status == "active",
      DBUnitOwnership.deleted_at.is_(None)
  ).all()
  sum_pct = sum(o.ownership_percentage for o in total)
  assert sum_pct + new_percentage <= 100
  ```
- **OWN-02:** ¿Un usuario puede ser owner Y co_owner de la misma unidad al mismo tiempo? No hay validación.
- **No hay cascade en soft-delete de usuario:** mismo problema que en roles.
- **No hay enriquecimiento con datos de unidad:** listar ownerships sin el código de unidad es inútil para un admin.

### 3.4 `core_unit_occupancies` — Estado: REVISAR

**Nota:** Este módulo no estaba en los 4 originales, pero está en el `consolidated-view` y depende directamente de `core_occupancy_types`.

**Lo que está bien:**
- Históricos con start/end dates
- `is_primary` flag para distinguir ocupante principal

**Hallazgos:**
- **`occupancy_type_id` NO tiene FK** en `DBUnitOccupancy` → `core_occupancy_types.id`. El campo existe como BigInteger pero sin constraint.
- **OCC-01:** No hay validación de que un usuario no tenga dos `active` occupancies de tipo `primary` en la misma unidad.
- **No hay cascade:** si se elimina un `OccupancyType`, las occupancy records quedan con `occupancy_type_id` inválido.

### 3.5 `core_occupancy_types` ✅ — Estado: FUNCIONAL

**Lo que está bien:**
- Scope: system (global) vs condominium (custom por condo)
- Flags: `requires_authorization`, `allows_primary`
- Catálogo ya funciona con soft-delete

**Hallazgos:**
- **Sin FK en `occupancy_type_id` en `DBUnitOccupancy`** — esto rompería cualquier join entre occupancy y su tipo en la DB si hay orphan records.

---

## 4. Integración: Canvas Completo del Actor

### 4.1 Flujos que deben existir

```
[Crear usuario]
  1. POST /users → crea user + user_profile (profile separado)
  2. POST /condominium-roles → asignar rol en condominio
  3. POST /unit-ownerships → asignar propiedad
  4. POST /unit-occupancies → asignar ocupación
  ⚠ Ninguno de estos pasos es transaccionalmente atómico.

[Consultar "¿Quién es el residente principal de la Torre A, Unidad 301?"]
  → Hoy: query manual en 3 tablas
  → Esperado: 1 endpoint consolidado con nombres

[Cambiar propiedad de unidad]
  1. PUT /unit-ownerships/{id}/end_date = hoy
  2. POST /unit-ownerships (nuevo owner)
  3. Validar OWN-01: % total ≤ 100
  ⚠ No existe endpoint wrapper que haga esto atómico.

[Desactivar usuario (soft-delete)]
  1. Soft-delete user (incrementa token_version)
  2. ¿Los roles se marcan como historical automáticamente? → NO.
  3. ¿Las ownerships se cierran con end_date? → NO.
  4. ¿Las occupancies se cierran? → NO.
  ⚠ Datos huérfanos guaranteed.
```

### 4.2 Lo que falta como módulos integrados

| # | Funcionalidad | Módulo afectado | Prioridad |
|---|---|---|---|
| M-01 | Validación OWN-01: % total ≤ 100 por unidad | core_unit_ownerships | ALTA |
| M-02 | Cascade soft-delete: roles + ownerships + occupancies cuando user se elimina | core_users + roles + ownerships + occupancies | ALTA |
| M-03 | FK constraint en occupancy_type_id → core_occupancy_types.id | core_unit_occupancies | ALTA |
| M-04 | Endpoint enriquecido: list de ownerships con código de unidad + nombre de condo | core_unit_ownerships | MEDIA |
| M-05 | Endpoint enriquecido: list de roles con nombre de usuario + nombre de condo | core_condominium_roles | MEDIA |
| M-06 | Validación OCC-01: un solo primary occupant por unidad | core_unit_occupancies | MEDIA |
| M-07 | Unique constraint: (user_id, condominium_id, role) active — sin duplicados | core_condominium_roles | MEDIA |
| M-08 | Unique constraint: (user_id, unit_id, occupancy_type_id) active, is_primary=true | core_unit_occupancies | MEDIA |
| M-09 | Consolidated view mejorado: incluir nombre condo, código unidad, tipo ocupación | core_users | BAJA (ya existe estructura) |
| M-10 | Historial completo de transiciones de propiedad/ocupación por unidad | core_unit_ownerships + core_unit_occupancies | BAJA |

---

## 5. Validaciones de Negocio Pendientes ( Rules )

| ID | Descripción | Ubicación |
|---|---|---|
| OWN-01 | Suma de ownership_percentage active de una unidad ≤ 100 | `UnitOwnershipUseCase.create()` / `update()` |
| OWN-02 | Un usuario no puede ser owner y co_owner de la misma unidad al mismo tiempo | `UnitOwnershipUseCase` |
| OCC-01 | Solo un occupancy record active con `is_primary=true` por unidad | `UnitOccupancyUseCase` |
| ROLE-01 | No duplicar (user_id, condominium_id, role, status=active) | `CondominiumRoleUseCase` |
| USR-01 | Al hacer soft-delete de usuario, cascade a roles, ownerships, occupancies (marcar historical o fechar) | `UserUseCase.soft_delete()` |

---

## 6. Recomendación de Arquitectura

### 6.1 Immediate (Sprint 6 — esta semana)
Implementar M-01, M-02, M-03 como hotfixes de integridad referencial. Son blockers para que el sistema no entre en estado inconsistente.

### 6.2 Short-term (Sprint 7)
Implementar M-04, M-05, M-07, M-08 — queries enriquecidas y constraints de unicidad.

### 6.3 Medium-term
Implementar un servicio `ActorContextService` que orqueste la creación de un actor completo (user + profile + role + ownership + occupancy) en una sola transacción, con rollback.

---

## 7. Asignación Sugerida de Responsables

| Módulo/Tarea | Responsable sugerido |
|---|---|
| M-01 + M-02 (ownerships + cascade) | Dev front-end: @Mike / Dev back: @Lelouch |
| M-03 (FK occupancy_type) | Dev back: @Lelouch |
| M-04 (enriched ownership queries) | Dev back: @Lelouch |
| M-05 (enriched role queries) | Dev back: @Bulma |
| M-07 + M-08 (unique constraints) | Dev back: @Bulma |
| M-06 (OCC-01 primary validation) | Dev back: @Lelouch |
| M-09 (consolidated view improvement) | Dev back: @Bulma |

---

## 8. Dependencias de Migración

Ninguna de las tareas M-01 a M-10 requiere migración nueva de tabla. Las validaciones son lógica de aplicación. La M-03 requiere ALTER TABLE para agregar FK si no existe (verificar con `SHOW CREATE TABLE core_unit_occupancies`).

---

## 9. Checklist demerge de Integración

- [ ] OWN-01: validar % total ≤ 100 al crear/actualizar ownership
- [ ] OWN-02: validar no duplicidad owner+co_owner por unidad
- [ ] ROLE-01: unique constraint (user, condo, role) active
- [ ] OCC-01: solo un primary occupant por unidad
- [ ] USR-01: cascade soft-delete a roles/ownerships/occupancies
- [ ] FK `occupancy_type_id` → `core_occupancy_types.id`
- [ ] Queries enriquecidas: ownerships con unit_code + condo_name
- [ ] Queries enriquecidas: roles con user full name + condo_name
- [ ] Consolidated view mejorado
- [ ] Tests de integración cubriendo los flujos del §4.1
