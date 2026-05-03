# Amenity Bookings — Sprint A

**Fecha:** 2026-05-02  
**Autor:** Bulma S  
**Status:** ✅ Completado (balance wire-up completado)

---

## Migraciones DB

- [x] `053_create_amenity_bookings` — `booking_price`, `security_deposit_amount`, `is_reservable` en amenities; `origin_type`/`origin_id` en AR; tabla `core_amenity_bookings` (18 cols, 7 FKs); tabla `core_amenity_deposit_movements`
- [x] `054_seed_booking_permissions` — 8 permisos RBAC (amenities.* + bookings.*)

---

## Modelo de Dominio `core_amenity_bookings`

- [x] `BookingEntity` — estados, transiciones, invariantes, `to_dict`
- [x] 4 excepciones: NotFound, ValidationError, OverlapError, StatusError
- [x] `DBBooking` + `BookingMapper` + repos cmd/query con solape horario

---

## Lógica de Negocio `BookingUseCase`

- [x] CRUD completo con validaciones: unidad↔edificio, owner↔unidad, solape horario, snapshots
- [x] `confirm()` — genera 2 ARs separadas (fee + garantía) con `origin_type`/`origin_id`
- [x] `cancel()` — soft-delete con razón
- [x] `complete()` — marca completada
- [x] `return_deposit()` — devolución total con trazabilidad
- [x] `apply_deposit()` — aplicación parcial/total con registro de movimiento

---

## API Routes

11 endpoints en `/bookings` con RBAC:
- CRUD + confirm + cancel + complete + deposit/return + deposit/apply

---

## Extensiones a Modelos Existentes

- [x] `AmenityEntity`, `DBAmenity`, schemas, usecase, routes — +3 campos
- [x] `AREntity`, `DBAR`, `ARMapper` — +origin_type/origin_id
- [x] `main.py` — registro de `booking_routes`
- [x] Seeds amenities actualizados con pricing/deposit

---

## Archivos

- 18 nuevos + 12 modificados
- Todo compila ✅

---

## ✅ Completado

- Balance wire-up: módulo `core_balance_summary` con 3 endpoints (condominio, edificio, unidad) + rubros separados (mantenimiento, reservas áreas comunes, garantías en custodia)

---

## Meta

| Campo | Valor |
|---|---|
| Sprint | A |
| Estado | Completado |
| siguiente paso | Balance wire-up |
