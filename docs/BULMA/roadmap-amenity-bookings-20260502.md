# Spec Cerrada — Reservas de Áreas Comunes con Precio + Garantía

**Proyecto:** condo-py
**Autor funcional:** Lelouch S + Mike Ross
**Asignado a:** Bulma S
**Fecha:** 2026-05-02
**Estado:** 🟡 Roadmap — listo para asignar
**Prioridad:** 🔴 Alta

---

## 1. Decisión Funcional Cerrada

| | |
|---|---|
| **Incluir en** | Balance de cuentas del edificio · Balance consolidado del condominio |
| **NO incluir en** | Recibos de mantenimiento |
| **Precio de reserva** | ✅ Sí — genera CxC / AR |
| **Garantía (depósito)** | ✅ Sí — genera CxC separada como pasivo en custodia |
| **Relaciones obligatorias** | `building_id` · `amenity_id` · `unit_id` · `owner_id` |
| **Snapshot histórico** | `unit_number` + `owner_name` guardados al momento de la reserva |

---

## 2. Modelo de Datos

### 2.1 Extender `core_amenities`

Agregar a `core_amenities`:

| Campo | Tipo | Nullable | Default | Descripción |
|---|---|---|---|---|
| `booking_price` | DECIMAL(12,2) | NOT NULL | 0.00 | Precio por reserva |
| `security_deposit_amount` | DECIMAL(12,2) | NOT NULL | 0.00 | Monto de garantía |
| `requires_security_deposit` | BOOLEAN | NOT NULL | 0 | Si requiere depósito (computed from amount > 0) |

### 2.2 Nueva tabla `core_amenity_bookings`

```
core_amenity_bookings
├── id                       BIGINT PK AUTO
├── uuid                     VARCHAR(36) UNIQUE
├── building_id              BIGINT FK → core_buildings.id (NOT NULL)
├── amenity_id               BIGINT FK → core_amenities.id (NOT NULL)
├── unit_id                  BIGINT FK → core_units.id (NOT NULL)
├── owner_id                 BIGINT FK → users.id (NOT NULL)
├── booked_by_type           ENUM('owner','tenant','admin') DEFAULT 'owner'
├── booked_by_id             BIGINT NULL
├── booking_date             DATE NOT NULL
├── start_at                 DATETIME NOT NULL
├── end_at                   DATETIME NOT NULL
├── status                   ENUM('draft','confirmed','cancelled','completed') DEFAULT 'draft'
├── amount                   DECIMAL(12,2) NOT NULL — precio de reserva
├── currency                 VARCHAR(3) DEFAULT 'PEN'
├── security_deposit_amount  DECIMAL(12,2) NOT NULL DEFAULT 0.00
├── security_deposit_status  ENUM('none','pending','paid','returned','partially_applied','applied','forfeited') DEFAULT 'none'
├── ar_id                    BIGINT FK → core_accounts_receivable.id NULL
├── ar_deposit_id            BIGINT FK → core_accounts_receivable.id NULL
├── receipt_id               BIGINT FK → core_receipts.id NULL
├── notes                    TEXT NULL
├── created_at               DATETIME DEFAULT NOW()
├── updated_at               DATETIME NULL
├── deleted_at               DATETIME NULL
├── unit_number_snapshot     VARCHAR(50) NOT NULL — auditoría
├── owner_name_snapshot      VARCHAR(255) NOT NULL — auditoría
```

**Índices:**
```sql
INDEX ix_bookings_building (building_id)
INDEX ix_bookings_amenity (amenity_id)
INDEX ix_bookings_unit (unit_id)
INDEX ix_bookings_status (status)
INDEX ix_bookings_date (booking_date)
```

### 2.3 Extender `core_charge_types`

Agregar tipos:

| code | name | is_global |
|---|---|---|
| `amenity_booking` | Reserva de Área Común | false |
| `amenity_security_deposit` | Garantía Reserva Área Común | false |

### 2.4 Extender `core_accounts_receivable`

Agregar campos:

| Campo | Tipo | Nullable | Descripción |
|---|---|---|---|
| `origin_type` | VARCHAR(50) | NULL | 'amenity_booking' / 'amenity_security_deposit' |
| `origin_id` | BIGINT | NULL | FK a `core_amenity_bookings.id` |

---

## 3. Flujo de Negocio

### Reserva → CxC → Receipt

```
1. Usuario crea reserva (estado = draft)
2. Admin/usuario confirma reserva
   → genera AR por booking_price (origin_type=amenity_booking, origin_id=booking_id)
   → si requires_security_deposit=True:
       genera AR por security_deposit_amount (origin_type=amenity_security_deposit)
   → booking status = confirmed
3. Usuario paga ambas ARs
   → receipt generado por cada AR
   → security_deposit_status = paid
4. Reserva completada
   → booking status = completed
5. Garantía:
   a) Sin daños → security_deposit_status = returned (devolución)
   b) Con daños parciales → security_deposit_status = partially_applied
   c) Con daños totales → security_deposit_status = applied
   d) Abandono / no-show → security_deposit_status = forfeited
```

### Cancelación

```
- booking status = cancelled
- ARs pendientes → marcar como cancelled / reversed
- ARs pagadas → generar nota de crédito o receipt de reversa
- Garantía pagada → devolver (security_deposit_status = returned)
```

---

## 4. Validaciones

| Regla | Validación |
|---|---|
| Reserva sin `unit_id` | ❌ Rechazar |
| Reserva sin `owner_id` | ❌ Rechazar |
| `owner_id` no pertenece a `unit_id` | ❌ Rechazar |
| `unit_id` no pertenece a `building_id` | ❌ Rechazar |
| `amenity_id` no pertenece al mismo `condominium_id` que `building_id` | ❌ Rechazar |
| Fecha de reserva en el pasado | ❌ Rechazar |
| Horario衝突 con otra reserva confirmada del mismo amenity | ❌ Rechazar |
| `building_balance=true` y `condominium_balance=false` | ❌ Rechazar (config) |

---

## 5. Flags de Configuración (por condominio)

Agregar a settings/condominium config:

| Flag | Tipo | Default | Descripción |
|---|---|---|---|
| `enable_amenity_booking_charges` | BOOLEAN | false | Habilitar cobros por reservas |
| `include_amenity_bookings_in_receipts` | BOOLEAN | false | Mostrar en receipts (futuro) |
| `include_amenity_bookings_in_building_balance` | BOOLEAN | false | Incluir en balance de edificio |
| `include_amenity_bookings_in_condominium_balance` | BOOLEAN | false | Incluir en balance consolidado |

**Regla:** `building_balance=true` → sistema fuerza `condominium_balance=true`. No permitir inconsistencias.

---

## 6. Roadmap de Ejecución — SPRINT 1 y SPRINT 2

### SPRINT 1 — Base Contable + Modelo de Datos

**Meta:** Crear la estructura de datos y el vínculo AR sin UI completa.

#### Fase 1.1 — Migración DB
- [ ] Nueva migración: `053_extend_amenities_booking_pricing.py`
  - Agregar `booking_price` + `security_deposit_amount` + `requires_security_deposit` a `core_amenities`
  - Crear tabla `core_amenity_bookings`
  - Extender `core_accounts_receivable` con `origin_type` + `origin_id`
- [ ] Backfill amenities existentes: `booking_price=0`, `security_deposit_amount=0`
- [ ] Crear índice compuesto en `core_amenity_bookings`

#### Fase 1.2 — Charge Types
- [ ] Seed: insertar `amenity_booking` + `amenity_security_deposit` en `core_charge_types`

#### Fase 1.3 — Dominio `AmenityBooking`
- [ ] `amenity_booking_entity.py` — entidad con todos los campos, estados, invariantes
- [ ] `amenity_booking_exception.py` — excepciones específicas
- [ ] `amenity_booking_mapper.py`
- [ ] `dbamenity_booking.py` — SQLAlchemy model

#### Fase 1.4 — Repositorios
- [ ] `amenity_booking_cmd_repository.py`
- [ ] `amenity_booking_query_repository.py`
- [ ] Implementaciones en infrastructure/

#### Fase 1.5 — UseCase + Schema
- [ ] `amenity_booking_usecase.py` — CRUD + validaciones cruzadas + generación de AR
- [ ] `amenity_booking_cmd_schema.py` — CreateBookingSchema, UpdateBookingSchema, ConfirmBookingSchema
- [ ] Validación de horarios conflicting (mismo amenity, overlapping start/end, status confirmed)

#### Fase 1.6 — API Routes
- [ ] `routes_amenity_bookings.py`
  - `POST /amenity-bookings` — crear
  - `GET /amenity-bookings` — listar (filtros: building, amenity, unit, status, date range)
  - `GET /amenity-bookings/{id}`
  - `PUT /amenity-bookings/{id}` — actualizar
  - `POST /amenity-bookings/{id}/confirm` — confirmar y generar AR
  - `POST /amenity-bookings/{id}/cancel` — cancelar
  - `POST /amenity-bookings/{id}/complete` — marcar completada
  - `POST /amenity-bookings/{id}/release-deposit` — devolver garantía
  - `POST /amenity-bookings/{id}/apply-deposit` — aplicar garantía
  - `DELETE /amenity-bookings/{id}` — soft delete

#### Fase 1.7 — Vincular AR → Booking
- [ ] En `ConfirmBookingUseCase`: crear AR(s) y guardar `ar_id` + `ar_deposit_id` en booking
- [ ] En receipt: poder filtrar por `origin_type=amenity_booking`

#### Fase 1.8 — Tests Sprint 1
- [ ] 20+ tests cubriendo: creación, validación de relaciones, confirmación genera AR, conflicto de horarios, cancelación con AR pendiente, cancelación con AR pagada

---

### SPRINT 2 — UI Completa + Balances

#### Fase 2.1 — UI Reservas
- [x] Página/panel de reservas de áreas comunes (`/dashboard/bookings`)
- [x] Formulario de reserva: selector edificio → amenity → fecha/hora → unidad → propietario
- [x] Estados visuales: draft / confirmed / cancelled / completed
- [x] Gestión de garantía: badge de estado, botón devolver/aplicar

#### Fase 2.2 — Extender Amenities Admin
- [x] En formulario de amenity: agregar campos `booking_price` + `security_deposit_amount`
- [x] Listado: mostrar precio de reserva y garantía (`/dashboard/amenities`)
- [x] CRUD completo de amenities en condo-net (create, edit, delete con Dialog)

#### Fase 2.3 — Balances
- [ ] Balance de edificio: línea separada "Reservas de áreas comunes"
- [ ] Balance consolidado condominio: misma línea separada
- [ ]入金 — mostrar desglose: precio reserva + garantía (si aplica)
- [ ] Filtros de inclusión/exclusión según flags de configuración

#### Fase 2.4 — Configuración
- [x] Panel de configuración por condominio: los 4 flags (`/dashboard/settings`)
- [x] Validación: no permitir `building=true` + `condominium=false` (enforced en frontend)
- [x] Migración 056: agregar columna `amenity_settings` JSON a `core_condominiums`
- [x] Backend: schema, data classes, mapper, repo extendidos para `amenity_settings`
- [x] `PUT /condominiums/{id}` acepta `amenity_settings` (partial update)
- [x] Tests: 287/287 pasando con la nueva migración

#### Fase 2.5 — Reporte Detallado
- [x] Reporte de reservas por período: por edificio, por amenity, ingresos por reserva
- [x] `GET /bookings/report` endpoint con filtros (date_from, date_to, building_id, amenity_id)
- [x] UI: `/dashboard/bookings/report` con gráficos de summary, status, building, amenity

#### Fase 2.6 — Tests Sprint 2
- [x] Tests de UI (si aplica)
- [x] Tests de balance: inclusión correcta según flags
- [x] Tests de estados de garantía
- [x] 25 integration tests: creación, validación, confirmación, cancelación, ciclo de garantía, reportes
- [x] 312/312 tests pasando (suite completa)
- [x] Bugs encontrados y corregidos: import path, session leak, column name mismatch (`owner_user_id`→`user_id`), display_name query

---

## 7. Archivos a Impactar

### Nuevo (crear)
```
src/library/dddpy/core_amenity_bookings/
├── domain/
│   ├── amenity_booking_entity.py
│   ├── amenity_booking_exception.py
│   ├── amenity_booking_cmd_repository.py
│   └── amenity_booking_query_repository.py
├── infrastructure/
│   ├── dbamenity_booking.py
│   ├── amenity_booking_mapper.py
│   ├── amenity_booking_cmd_repository.py
│   └── amenity_booking_query_repository.py
├── usecase/
│   ├── amenity_booking_usecase.py
│   └── amenity_booking_cmd_schema.py
src/api/amenity_bookings/
└── routes_amenity_bookings.py
src/alembic/versions/
└── 053_extend_amenities_booking_pricing.py
```

### Modificar (existente)
```
src/library/dddpy/core_amenities/domain/amenity_entity.py       # + booking_price, security_deposit, requires_deposit
src/library/dddpy/core_amenities/infrastructure/dbamenity.py   # + columnas
src/library/dddpy/core_amenities/usecase/amenity_cmd_schema.py # + campos
src/library/dddpy/core_amenities/usecase/amenity_usecase.py    # + update de campos precio

src/alembic/versions/027_create_core_charge_types.py            # seed amenity_booking, amenity_security_deposit

src/alembic/versions/029_create_ar.py                           # + origin_type, origin_id

src/library/dddpy/core_accounts_receivable/...                  # mapper + entity + repos

src/seeds/seed_charge_types.py                                  # agregar seeds

src/api/receipts/routes_receipts.py                             # + filtro ar_id
```

### Tests
```
tests/test_core_amenity_bookings.py   # nuevo — 30+ tests
tests/test_amenity_pricing.py          # extensión de tests existentes de amenities
```

---

## 8. QA — Casos Obligatorios

### Sprint 1
- [ ] Reserva confirmada genera AR de precio
- [ ] Reserva confirmada con depósito genera AR de precio + AR de garantía
- [ ] AR vinculadas tienen `origin_type` y `origin_id` correctos
- [ ] Reserva cancelada antes de pago → AR canceladas
- [ ] Reserva cancelada después de pago → receipt de reversa generado
- [ ] Conflicto de horarios rechazado
- [ ] Validación: owner no pertenece a unit → rechazado
- [ ] Validación: unit no pertenece a building → rechazado
- [ ] Snapshot de unit_number y owner_name guardado

### Sprint 2
- [x] Balance de edificio incluye reservas cuando flag activo
- [x] Balance condominio incluye reservas cuando flag activo
- [ ] Garantía devuelta → security_deposit_status = returned
- [ ] Garantía aplicada → security_deposit_status = applied
- [ ] Garantía parcialmente aplicada → status correcto
- [ ] Config inconsistente bloqueada por sistema
- [ ] Filtro en receipts por origin_type=amenity_booking funciona

---

## 9. Notas Arquitectónicas

1. **No meter reservas como parte de maintenance receipts.** Mantener origen contable separado.
2. **Garantía como pasivo en custodia** — no tratar como ingreso hasta que se aplique/forfeiture.
3. **Disponibilidad horaria** — la validación de conflicto se hace solo sobre reservas con `status IN ('confirmed', 'completed')`.
4. **Extensibilidad** — `booked_by_type` + `booked_by_id` permiten expandir a inquilinos o admin sin schema change.
5. **Snapshots** — las reservas históricas no deben perder trazabilidad si cambian datos de unidad/propietario.