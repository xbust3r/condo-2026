# Sprint 14 — `core_dashboards` — Executive Reporting

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable:** Lelouch vi Britannia + sub-agentes

---

## Overview

Dashboards de reporting ejecutivo para admins y board members del condominio. Consolida métricas de todos los módulos en vistas agregadas.

**No es un módulo DDD tradicional.** Es un facade de lectura que consume datos de los módulos existentes y los transforma en métricas útiles.

---

## Dashboards por Rol

### 1. Condominium Admin Dashboard (`GET /condominiums/{id}/dashboard`)

```json
{
  "condominium_id": 1,
  "condominium_name": "Torre Norte",
  "as_of": "2026-04-24T16:00:00Z",
  
  "units": {
    "total": 120,
    "occupied": 115,
    "vacant": 5
  },
  
  "financial": {
    "ar_pending_total": 125000.00,
    "ar_overdue_30_days": 45000.00,
    "ar_overdue_90_days": 12000.00,
    "collections_this_month": 89000.00,
    "collection_rate_percent": 78.5
  },
  
  "incidents": {
    "open_total": 23,
    "by_priority": {"urgent": 2, "high": 5, "medium": 12, "low": 4},
    "avg_resolution_days": 4.2
  },
  
  "visitors": {
    "registered_today": 18,
    "checked_in_now": 6,
    "pending_today": 12
  },
  
  "announcements": {
    "active_count": 3,
    "pinned": [{"id": 1, "title": "...", "published_at": "..."}]
  },
  
  "votes": {
    "active_count": 1,
    "pending_results": 0
  }
}
```

### 2. Finance Dashboard (`GET /condominiums/{id}/finance`)

```json
{
  "condominium_id": 1,
  "as_of": "2026-04-24",
  
  "accounts_receivable": {
    "total_pending": 125000.00,
    "by_status": {
      "current": 68000.00,
      "30_days": 45000.00,
      "90_days": 12000.00
    }
  },
  
  "collections": {
    "this_month": {
      "expected": 113500.00,
      "collected": 89000.00,
      "rate_percent": 78.5
    },
    "last_12_months": [
      {"month": "2025-05", "expected": 110000, "collected": 105000},
      ...
    ]
  },
  
  "charges": {
    "active_charge_types": 3,
    "recurring_monthly": 98000.00
  },
  
  "recent_payments": [
    {"id": 1, "amount": 3500.00, "unit_code": "101", "date": "2026-04-22", "receipt_number": "C001-202604-000001"}
  ]
}
```

### 3. Operations Dashboard (`GET /condominiums/{id}/operations`)

```json
{
  "condominium_id": 1,
  "as_of": "2026-04-24",
  
  "incidents": {
    "open": 23,
    "resolved_this_month": 41,
    "by_category": {
      "plumbing": 12,
      "electrical": 8,
      "elevator": 3,
      ...
    },
    "avg_resolution_hours": 72
  },
  
  "visitors": {
    "today": {"registered": 18, "checked_in": 6, "no_show": 2},
    "this_week": 87
  },
  
  "packages": {
    "pending_delivery": 7,
    "delivered_this_week": 23
  },
  
  "amenity_bookings": {
    "active_bookings": 4,
    "pending_requests": 2
  }
}
```

---

## Notas de Implementación

### Estructura
Este módulo NO tiene entity ni repository DDD tradicional. Es un **query-only facade**.

```
src/library/dddpy/core_dashboards/
├── usecase/
│   ├── condominium_dashboard_usecase.py   ← Admin summary
│   ├── finance_dashboard_usecase.py      ← Financial metrics
│   └── operations_dashboard_usecase.py  ← Operations metrics
└── api/
    └── dashboards/routes_dashboards.py
```

### Consulta de datos
Los usecases hacen queries directas a los repositorios existentes:
- `ArQueryRepositoryImpl` → `list_all(condominium_id, status, ...)` para AR
- `UnitOwnershipQueryRepositoryImpl` → counts para occupancy
- `IncidentQueryRepositoryImpl` → counts + avg resolution
- `VisitorQueryRepositoryImpl` → counts por fecha
- etc.

No crea nuevas tablas ni migraciones. Es plug-and-play con lo que ya existe.

### Autenticación
Todos los endpoints requieren `get_current_user` + RBAC `dashboard:read` (admin/board_member/condominium_admin).

---

## Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/condominiums/{id}/dashboard` | Admin dashboard completo |
| GET | `/condominiums/{id}/finance` | Finance summary |
| GET | `/condominiums/{id}/operations` | Operations summary |
| GET | `/condominiums/{id}/summary` | Alias rápido para `/dashboard` |

---

## Tasks

| Task | Descripción |
|---|---|
| T-1 | `condominium_dashboard_usecase.py` — aggregate all modules |
| T-2 | `finance_dashboard_usecase.py` — AR + payments aggregation |
| T-3 | `operations_dashboard_usecase.py` — incidents + visitors + packages |
| T-4 | API routes |
| T-5 | RBAC seed `dashboards:read` |
