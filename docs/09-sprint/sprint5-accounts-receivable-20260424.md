# Sprint 5 — Phase 3: Accounts Receivable · Cargos · Recibos · Pagos · Ledger
## Proyecto: condo-py (backdmin)
**Autor:** Misato K — Coordinación
**Fecha:** 2026-04-24
**Asignado a:** Bulma S (Dev)
**Estado:** Sprint Planning

---

## 1. Contexto y Dependencias

Phase 2 (Identidad, acceso y ocupación) se cerró en commit `4ac2f45`. La base estructural actual soporta correctamente la facturación:

- `core_condominiums` → cada unidad pertenece a un condominio
- `core_units` → cada unidad tiene `condominium_id`, `building_id`, `unit_type_id`
- `core_users` + `core_user_profiles` → identidad del deudor
- `core_unit_ownerships` → quién es el propietario legal (sujeto a cargo)
- `core_unit_occupancies` → quién ocupa la unidad (inquilino = deudor secundario)
- `core_condominium_roles` → permisos para crear cargos, aprobar pagos, exportar estados

**Regla de negocio que se hereda:** El flujo de cobranza va siempre atado a `core_units`. No hay cargo sin unidad.

---

## 2. Inventario de Módulos Phase 3

### 2.1 `accounts_receivable` — Cuentas por Cobrar
**Tabla:** `core_accounts_receivable`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK → core_condominiums | |
| unit_id | BIGINT FK → core_units | obligación attached a unidad |
| debtor_user_id | BIGINT FK → users | who owes |
| reference_code | VARCHAR(50) | código interno del cargo |
| description | TEXT | |
| amount | DECIMAL(12,2) | |
| currency | VARCHAR(3) | default 'PEN' |
| status | ENUM('pending','partial','paid','overdue','cancelled') | |
| due_date | DATE | |
| period | VARCHAR(7) | 'YYYY-MM' para cuotas mensuales |
| charge_id | BIGINT FK NULL | si viene de un cargo recurrente |
| created_at | DATETIME | |
| updated_at | DATETIME | |
| deleted_at | DATETIME | |

**Estado:** No existe aún. Crear DDD module + migración.

**Reglas de negocio:**
- AR-01: `amount` debe ser > 0
- AR-02: `status` solo cambia en secuencia válida: `pending → partial → paid` o `pending → overdue → paid`
- AR-03: `unit_id` obligatorio, `debtor_user_id` obligatorio

---

### 2.2 `charges` — Cargos Recurrentes y Extraordinarios
**Tabla:** `core_charges`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK | |
| charge_type_id | BIGINT FK → core_charge_types | catálogo |
| unit_id | BIGINT FK NULL | null = cargo a todo el condominio |
| description | TEXT | |
| amount | DECIMAL(12,2) | |
| is_recurrent | BOOL | si es cuota mensual |
| period_pattern | VARCHAR(7) NULL | 'YYYY-MM' o null si extraordinario |
| start_date | DATE | inicio de vigencia |
| end_date | DATE NULL | fin de vigencia (null = indefinido) |
| status | ENUM('active','inactive','expired') | |
| created_at | DATETIME | |
| updated_at | DATETIME | |

**Tabla:** `core_charge_types` (catálogo seed)

| code | name | is_global | description |
|------|------|----------|-------------|
| monthly_fee | Cuota Mensual | true | Cuota ordinaria del condominio |
| special_assessment | Cargo Extraordinario | false | Aproado por asamblea |
| reserve_fund | Fondo de Reserva | true | Aportación al fondo de reserva |
| penalty | Multa | false | Por mora o incumplimiento |
| utility | Servicio Común | true | Agua, gas, mantenimiento áreas |

**Estado:** No existe aún. Crear DDD module + migración + seeds.

---

### 2.3 `receipts` — Generación de Recibos
**Tabla:** `core_receipts`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK | |
| unit_id | BIGINT FK | |
| ar_id | BIGINT FK → core_accounts_receivable | |
| receipt_number | VARCHAR(30) | correlativo |
| issued_at | DATETIME | |
| payer_user_id | BIGINT FK | quien paga |
| amount_paid | DECIMAL(12,2) | |
| payment_method | ENUM('cash','bank_transfer','yape','plin','card','other') | |
| reference | VARCHAR(100) NULL | nro operación |
| notes | TEXT NULL | |

**Reglas de negocio:**
- REC-01: `receipt_number` único por condominio (formato: `C{cod_condominio}-{YYYY}{MM}-{correlativo:06d}`)
- REC-02: Al emitir recibo, actualizar `status` del AR asociado
- REC-03: Un AR puede generar múltiples recibos (pago parcial = varios recibos)

---

### 2.4 `payments` — Registro de Pagos
**Tabla:** `core_payments`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK | |
| unit_id | BIGINT FK | |
| ar_id | BIGINT FK → core_accounts_receivable | |
| receipt_id | BIGINT FK NULL | receipt generado (opcional) |
| payer_user_id | BIGINT FK | |
| amount | DECIMAL(12,2) | |
| payment_method | ENUM(...) | |
| reference | VARCHAR(100) NULL | |
| paid_at | DATETIME | |
| created_at | DATETIME | |

**Reglas de negocio:**
- PAY-01: `amount` no puede exceder el saldo pendiente del AR
- PAY-02: Al registrar pago, recalcular `status` del AR (`pending → partial` o `overdue → partial`)
- PAY-03: Un pago genera un `receipt` automáticamente (relación 1:1)

---

### 2.5 `ledger` — Estado de Cuenta por Unidad
**Tabla:** `core_ledger_entries`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK | |
| unit_id | BIGINT FK | |
| entry_type | ENUM('charge','payment','adjustment','balance_forward') | |
| ar_id | BIGINT FK NULL | si viene de AR |
| payment_id | BIGINT FK NULL | si viene de pago |
| description | TEXT | |
| debit | DECIMAL(12,2) | cargo (amount owe) |
| credit | DECIMAL(12,2) | pago |
| balance | DECIMAL(12,2) | saldo acumulado |
| period | VARCHAR(7) | 'YYYY-MM' |
| created_at | DATETIME | |

**Reglas de negocio:**
- LED-01: `balance` se calcula como saldo anterior + debit - credit (no almacenar, recalcular con SUM)
- LED-02: Cada `charge` genera un `ledger_entry` de tipo `charge`
- LED-03: Cada `payment` genera un `ledger_entry` de tipo `payment`
- LED-04: `GET /units/{unit_id}/ledger` devuelve estado de cuenta con todos los entries ordenados por `created_at`

---

## 3. Modelo de Datos Integrado

```
core_charge_types (seed: 5 tipos)
       ↓ FK
core_charges ──────── condominium_id → core_condominiums
       │                         └── unit_id → core_units (nullable)
       │                                  └── owner/occupant → users
       │                                            ↓ FK
       ↓ FK (genera)              core_accounts_receivable
core_ledger_entries  ←←←←←←←←←←←←←←←← AR + payments
       │                         
       │ (1:1 genera)
       ↓
core_receipts
```

---

## 4. Estructura DDD por Módulo

Cada módulo sigue el patrón DDD del proyecto:

```
{modulo}/
├── domain/
│   ├── {modulo}_entity.py
│   ├── {modulo}_data.py
│   ├── {modulo}_exception.py
│   ├── {modulo}_success.py
│   ├── {modulo}_cmd_repository.py
│   └── {modulo}_query_repository.py
├── infrastructure/
│   ├── db{modulo}.py
│   ├── {modulo}_mapper.py
│   ├── {modulo}_cmd_repository.py
│   └── {modulo}_query_repository.py
└── usecase/
    ├── {modulo}_cmd_schema.py
    ├── {modulo}_cmd_usecase.py
    ├── {modulo}_query_usecase.py
    ├── {modulo}_usecase.py
    └── {modulo}_factory.py
```

Ruta API: `src/api/{modulo}/routes_{modulo}.py`

---

## 5. Migraciones Requeridas

| # | Archivo | Descripción |
|---|---------|-------------|
| 027 | `027_create_core_charge_types.sql` | Catálogo de tipos de cargo + seed |
| 028 | `028_create_core_charges.sql` | Tabla de cargos |
| 029 | `029_create_core_accounts_receivable.sql` | Tabla de cuentas por cobrar |
| 030 | `030_create_core_payments.sql` | Tabla de pagos |
| 031 | `031_create_core_receipts.sql` | Tabla de recibos |
| 032 | `032_create_core_ledger_entries.sql` | Tabla del libro mayor |

---

## 6. Endpoints Mínimos por Módulo

### `/charges`
- `POST /charges` — crear cargo
- `GET /charges` — listar con filtros (condominium_id, unit_id, status, is_recurrent)
- `GET /charges/{id}`
- `PUT /charges/{id}` — actualizar monto/descripción
- `DELETE /charges/{id}` — soft delete

### `/accounts-receivable`
- `POST /accounts-receivable` — generar AR desde cargo (batch por unidad o individual)
- `GET /accounts-receivable` — listar (status, condominium_id, unit_id, debtor_user_id)
- `GET /accounts-receivable/{id}`
- `GET /accounts-receivable/summary/{unit_id}` — resumen de deuda actual

### `/payments`
- `POST /payments` — registrar pago
- `GET /payments` — listar (condominium_id, unit_id, ar_id, status)
- `GET /payments/{id}`

### `/receipts`
- `GET /receipts` — listar (condominium_id, unit_id)
- `GET /receipts/{id}`
- `GET /receipts/unit/{unit_id}` — recibos por unidad

### `/units/{unit_id}/ledger`
- `GET /units/{unit_id}/ledger` — estado de cuenta completo (entries + saldo pendiente)

### `/condominiums/{id}/summary`
- `GET /condominiums/{id}/summary` — deuda total del condominio por estado

---

## 7. Roadmap FIN — Estado de Tareas (Completado 2026-05-01)

| # | Tarea | Estado | PR | Notas |
|---|-------|--------|-----|-------|
| FIN-01 | Spec funcional distribución | ✅ Cerrada | — | Sección 3 de este doc |
| FIN-02 | Extender core_charges | ✅ | #1 | Migración 051 + validación scope |
| FIN-03 | Actualizar dominio charges | ✅ | #1 | Entity, data, mapper, schemas, usecase |
| FIN-04 | Crear ProrationService | ✅ | #2 | Servicio de dominio puro |
| FIN-05 | Prorrateo por torre | ✅ | #3 | Consolidado con FIN-06 |
| FIN-06 | Prorrateo por condominio | ✅ | #3 | Consolidado con FIN-05 |
| FIN-07 | Redondeo determinístico | ✅ | #2 | Incluido: residual → mayor coeff |
| FIN-08 | Refactor generate_from_charge | ✅ | #4 | Bug corregido: entry.amount |
| FIN-09 | Resolver deudor por unidad | ✅ | #5 | Prioridad: ocupante → propietario |
| FIN-10 | Idempotencia AR | ✅ | #5 | exists_by_charge_period_unit() |
| FIN-11 | Recurrencia mensual | ✅ | #6 | generate_recurring() |
| FIN-12 | Validar payments/receipts/ledger | ✅ | #7 | Sin cambios requeridos |
| FIN-13 | Tests | ✅ | #8 | 13 tests standalone pasando |
| FIN-14 | Documentación y handoff | ✅ | #9 | Este doc |

### Archivos nuevos
- `src/alembic/versions/051_add_charge_scope_distribution.py`
- `src/library/dddpy/core_charges/domain/proration_service.py`
- `src/library/dddpy/core_charges/usecase/proration_usecase.py`
- `tests/test_proration_pipeline.py`
- `docs/09-sprint/fin-12-validation-payments-receipts-ledger.md`

### Módulos modificados
- `core_charges/` — scope, building_id, distribution_mode, validaciones 3-capas
- `core_accounts_receivable/` — generate_from_charge refactor, debtor, idempotency, recurrence

### Módulos NO tocados
- `core_payments` ✅ | `core_receipts` ✅ | `core_ledger_entries` ✅

---

## 8. Permisos RBAC (extensión Phase 2)

| code | resource | action | scope_default |
|------|----------|--------|---------------|
| charge.create | charge | create | condominium |
| charge.read | charge | read | condominium |
| charge.update | charge | update | condominium |
| charge.delete | charge | delete | global |
| receipt.read | receipt | read | condominium |
| receipt.export | receipt | export | condominium |

---

## 9. Notas de Diseño (no negociables)

1. **Unidad es el centro del universo financiero.** Todo cargo, pago y estado de cuenta parte de `core_units`.
2. **No se tocan `payments`, `receipts` ni `ledger`.** Se validan, no se rehacen.
3. **Decimal handling:** `Decimal(12,2)` para todos los montos. Nunca `float`.
4. **Ledger es append-only.** Solo se añade, nunca se modifica.
5. **El prorrateo vive entre `charge` y `AR`.** charge = intención. AR = obligación concreta por unidad.

---

*Documento preparado por Misato K — Coordinación*
*Basado en análisis de Lelouch S (2026-05-01)*
*Implementado por Bulma S (2026-05-01) — Roadmap completado: 14/14 ✅*
