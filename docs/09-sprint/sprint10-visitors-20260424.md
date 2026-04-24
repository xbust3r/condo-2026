# Sprint 10 — `core_visitors` — Visitor Management

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable arquitectura:** Lelouch vi Britannia
**Responsable implementación:** Lelouch + sub-agentes

---

## Overview

Gestión de visitantes e invitados del condominio. Permite a residentes/propietarios registrar visitantes esperados, y al staff de seguridad llevar un registro/log de entradas reales.

**Diferencia con lo existente:** El RBAC seed ya menciona un `visitors log` pero no existe como módulo DDD. Este Sprint construye el módulo `core_visitors` completo.

---

## Modelo de Datos

### `VisitorEntity`

```
VisitorEntity
├── id: int
├── uuid: str
├── condominium_id: int
├── building_id: int (nullable — null si es visita global)
├── unit_id: int              ← unidad que recibe la visita
├── host_user_id: int         ← residente/propietario que registró la visita
├── visitor_name: str         ← nombre del visitante
├── visitor_document_type: str (nullable)  ← CI, Pasaporte, etc.
├── visitor_document_number: str (nullable)
├── visitor_phone: str (nullable)
├── expected_date: date
├── expected_time: time
├── actual_checkin_at: datetime (nullable)
├── actual_checkout_at: datetime (nullable)
├── status: VisitorStatus    ← pending, checked_in, checked_out, cancelled, no_show
├── visit_purpose: str       ← family, delivery, service, maintenance, other
├── access_code: str (nullable)  ← código de acceso generado (4-6 dígitos o QR)
├── notes: str (nullable)
├── created_at, updated_at, deleted_at
└── Enrichment: host_user_full_name, unit_code, building_name, condominium_name
```

### Enums

**VisitorStatus:**
```
pending     → registrado, esperando
checked_in  → llegó y fue registrado por seguridad
checked_out → salió
cancelled   → cancelado por el host
no_show     → no se presentó ese día
```

**VisitPurpose:**
```
family        → visita familiar
delivery      → delivery/paquetería
service       → servicio técnico (plomero, eléctrico, etc.)
maintenance   → mantenimiento programado
other         → otro
```

---

## Integración con el Sistema

| Dependencia | Para qué se usa |
|---|---|
| `core_condominiums.id` | Visitas por condominio |
| `core_buildings.id` | Puede ser edificio específico o null (todo el condo) |
| `core_units.id` | Unidad receptora |
| `core_unit_occupancies.user_id` | Validar que `host_user_id` tiene occupancy activo en `unit_id` (VIS-01) |
| `core_unit_ownerships.user_id` | Alternativamente, puede ser propietario activo |
| RBAC permissions | `visitors:create` (host), `visitors:read` (host de la unidad), `security_staff` puede hacer check-in/check-out |

---

## Reglas de Negocio

**VIS-01:** El usuario que registra una visita (`host_user_id`) debe tener un `UnitOccupancyEntity` activo O un `UnitOwnershipEntity` activo en la unidad `unit_id`. Caso contrario → 403.

**VIS-02:** El `access_code` se genera automáticamente (6 dígitos aleatorios) si no se provee. Debe ser único por condominio/fecha.

**VIS-03:** Solo `security_staff` o `condominium_admin` pueden hacer `check_in` y `check_out`. Un host puede cancelar una visita pendiente.

**VIS-04:** Una visita solo puede pasar a `checked_out` si ya está en `checked_in`.

**VIS-05:** Visitas con `expected_date < today` sin check-in se marcan como `no_show` (job nocturno o lazy evaluation al consultar).

---

## Estructura DDD

```
src/library/dddpy/core_visitors/
├── domain/
│   ├── visitor_entity.py
│   ├── visitor_exception.py
│   ├── visitor_repository.py    ← ABC cmd
│   └── visitor_query_repository.py ← ABC query
├── infrastructure/
│   ├── dbvisitor.py
│   ├── visitor_mapper.py
│   ├── visitor_cmd_repository.py
│   └── visitor_query_repository.py  ← con _bulk_enrich
├── usecase/
│   ├── visitor_cmd_schema.py
│   ├── visitor_cmd_usecase.py
│   ├── visitor_query_usecase.py
│   └── visitor_factory.py
└── api/
    └── visitors/routes_visitors.py
```

### Migración

```sql
CREATE TABLE core_visitors (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  uuid VARCHAR(36) NOT NULL UNIQUE,
  condominium_id BIGINT NOT NULL,
  building_id BIGINT NULL,
  unit_id BIGINT NOT NULL,
  host_user_id BIGINT NOT NULL,
  visitor_name VARCHAR(150) NOT NULL,
  visitor_document_type VARCHAR(20) NULL,
  visitor_document_number VARCHAR(50) NULL,
  visitor_phone VARCHAR(30) NULL,
  expected_date DATE NOT NULL,
  expected_time TIME NOT NULL,
  actual_checkin_at DATETIME NULL,
  actual_checkout_at DATETIME NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  visit_purpose VARCHAR(30) NOT NULL DEFAULT 'other',
  access_code VARCHAR(10) NULL,
  notes TEXT NULL,
  created_at DATETIME NOT NULL DEFAULT NOW(),
  updated_at DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  deleted_at DATETIME NULL,
  FOREIGN KEY (condominium_id) REFERENCES core_condominiums(id),
  FOREIGN KEY (unit_id) REFERENCES core_units(id),
  FOREIGN KEY (host_user_id) REFERENCES users(id),
  INDEX idx_condo_date_status (condominium_id, expected_date, status),
  INDEX idx_unit (unit_id),
  INDEX idx_host (host_user_id),
  INDEX idx_access_code (condominium_id, access_code),
);
```

---

## Endpoints

| Método | Endpoint | Permiso | Descripción |
|---|---|---|---|
| POST | `/visitors` | Auth (VIS-01) | Registrar visita |
| GET | `/visitors` | Auth + filtros | Listar (filtros: condo, building, unit, status, date range) |
| GET | `/visitors/{id}` | Auth | Detalle |
| GET | `/visitors/uuid/{uuid}` | Auth | Detalle por UUID |
| GET | `/visitors/my` | Auth | Mis visitas registradas |
| GET | `/visitors/unit/{unit_id}` | Auth (host) | Visitas de una unidad |
| PATCH | `/visitors/{id}` | Auth (host) | Editar (notas, expected_time) |
| POST | `/visitors/{id}/cancel` | Auth (host) | Cancelar |
| POST | `/visitors/{id}/check-in` | Security/staff | Registrar llegada |
| POST | `/visitors/{id}/check-out` | Security/staff | Registrar salida |
| GET | `/condominiums/{id}/visitors` | Auth | Visitas de condominio (paginadas) |
| GET | `/visitors/access-code/{code}` | Security | Buscar por access code (para security desk) |

---

## Queries enriquecidas (M-11)

Mismo patrón `_bulk_enrich` que en roles y incidents:
- `host_user_full_name` (from user_profiles)
- `unit_code`
- `building_name`
- `condominium_name`

---

## RBAC

```
visitors:create   → registrar visitas
visitors:read     → ver visitas propias o del edificio (security/admin)
visitors:checkin  → hacer check-in/check-out (security_staff)
visitors:cancel   → cancelar visita (host o admin)
```

---

## Tasks

| Task | Descripción |
|---|---|
| T-1 | Migración 044 `core_visitors` |
| T-2 | DDD domain layer |
| T-3 | Infrastructure + _bulk_enrich |
| T-4 | Usecases (cmd + query) |
| T-5 | API routes |
| T-6 | Seed RBAC permissions |
