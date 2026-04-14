# 📋 Módulos a Crear — condo-py
> Generado: 2026-04-13 | Basado en: `07-roadmap/module-roadmap.md` (Lelouch S)
> Orden: SECUENCIAL — ejecutar en este orden, sin saltar fases.

---

## FASE 1 — Núcleo Inmobiliario

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 01 | `core_condominiums` | Gestión de condominios | ✅ Ya existe |
| 02 | `core_buildings` | Torres/edificios dentro del condominio | Alta |
| 03 | `core_buildings_types` | Catálogo: residencial, comercial, mixto | Alta |
| 04 | `core_unities` | Unidades/departamentos dentro de cada edificio | Alta |
| 05 | `core_unittys_types` | Catálogo: apartamento, casa, local comercial | Alta |

---

## FASE 2 — Identidad, Acceso y Ocupación

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 06 | `users` | Usuarios autenticables en el sistema | Crítica |
| 07 | `users_residents` | Tabla pivote: usuario ↔ unidad (propietario/inquilino/familiar) | Crítica |
| 08 | `auth` | Autenticación JWT/OAuth2 + RBAC (admin, board, resident, concierge, accountant) | Crítica |

---

## FASE 3 — Cuentas, Cargos y Recibos

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 09 | `accounts_receivable` | Cuentas por cobrar por unidad | Crítica |
| 10 | `charges` | Cargos recurrentes (cuota mensual) y extraordinarios | Crítica |
| 11 | `receipts` | Generación de recibos por cargo/pago | Alta |
| 12 | `payments` | Registro de pagos y conciliación | Alta |
| 13 | `ledger` | Estado de cuenta por unidad / historial contable | Alta |

---

## FASE 4 — Comunicación y Operación Básica

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 14 | `announcements` | Anuncios/comunicados a residentes | Media-Alta |
| 15 | `notifications` | Notificaciones email/SMS/push/in-app | Media-Alta |
| 16 | `documents` | Repositorio de documentos (actas, reglamentos) | Media-Alta |
| 17 | `tickets` | Incidencias / solicitudes de mantenimiento | Media |

---

## FASE 5 — Experiencia Residente

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 18 | `resident_portal` | Portal web para residentes (estado de cuenta, docs, tickets) | Media |
| 19 | `amenity_booking` | Reserva de áreas comunes | Media |
| 20 | `visitors` | Registro previo de visitas/invitados | Media |
| 21 | `packages` | Registro de paquetería | Baja-Media |

---

## FASE 6 — Gobernanza y Capa Premium

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 22 | `meeting_minutes` | Actas de reuniones de board/assambleas | Baja |
| 23 | `voting` | Votaciones digitales / e-voting | Baja |
| 24 | `audit_trail` | Log de auditoría avanzado | Baja |
| 25 | `integrations` | Webhooks / API pública / integraciones externas | Baja |
| 26 | `dashboards` | Reporting ejecutivo y analítica | Baja |

---

## Total: 26 módulos

**Ya implementado:** 1 (`core_condominiums`)
**Por implementar:** 25

---

## Orden de implementación recomendado

```
Sprint 1 → 01, 02, 03
Sprint 2 → 04, 05
Sprint 3 → 06, 07, 08
Sprint 4 → 09, 10, 11
Sprint 5 → 12, 13
Sprint 6 → 14, 15, 16, 17
Sprint 7 → 18, 19
Sprint 8 → 20, 21
Sprint 9 → 22, 23, 24
Sprint 10+ → 25, 26
```

> **Nota:** Este orden es SECUENCIAL. No avanzar a la siguiente fase sin cerrar la anterior.
