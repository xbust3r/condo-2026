# 📋 Módulos a Crear — condo-py
> Generado: 2026-04-13 | Basado en: `07-roadmap/module-roadmap.md` (Lelouch S)
> Orden: SECUENCIAL — ejecutar en este orden, sin saltar fases.

---

## FASE 1 — Núcleo Inmobiliario

| # | Módulo | Descripción | Estado |
|---|---|---|---|
| 01 | `core_condominiums` | Gestión de condominios | ✅ Implementado |
| 02 | `core_buildings` | Torres/edificios dentro del condominio | ✅ Implementado |
| 03 | `core_buildings_types` | Catálogo: residencial, comercial, mixto | ✅ Implementado |
| 04 | `core_units` | Unidades/departamentos dentro de cada edificio | ✅ Implementado |
| 05 | `core_unit_types` | Catálogo: apartamento, casa, local comercial | ✅ Implementado |

---

## FASE 2 — Identidad, Acceso y Ocupación

| # | Módulo | Descripción | Estado |
|---|---|---|---|
| 06 | `users` | Usuarios autenticables en el sistema (users + user_profiles) | ✅ Implementado |
| 07 | `user_profiles` | Perfil humano desacoplado de autenticación | ✅ Implementado |
| 08 | `core_unit_ownerships` | Relación patrimonial usuario ↔ unidad | 🔄 En construcción |
| 09 | `core_unit_occupancies` | Relación de ocupación/uso usuario ↔ unidad | 🔄 En construcción |
| 10 | `core_condominium_roles` | Roles administrativos por condominio | 🔄 En construcción |
| 11 | `auth` | Autenticación JWT/OAuth2 + RBAC contextual | ❌ Pendiente |

---

## FASE 3 — Cuentas, Cargos y Recibos

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 12 | `accounts_receivable` | Cuentas por cobrar por unidad | Crítica |
| 13 | `charges` | Cargos recurrentes (cuota mensual) y extraordinarios | Crítica |
| 14 | `receipts` | Generación de recibos por cargo/pago | Alta |
| 15 | `payments` | Registro de pagos y conciliación | Alta |
| 16 | `ledger` | Estado de cuenta por unidad / historial contable | Alta |

---

## FASE 4 — Comunicación y Operación Básica

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 17 | `announcements` | Anuncios/comunicados a residentes | Media-Alta |
| 18 | `notifications` | Notificaciones email/SMS/push/in-app | Media-Alta |
| 19 | `documents` | Repositorio de documentos (actas, reglamentos) | Media-Alta |
| 20 | `tickets` | Incidencias / solicitudes de mantenimiento | Media |

---

## FASE 5 — Experiencia Residente

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 21 | `resident_portal` | Portal web para residentes (estado de cuenta, docs, tickets) | Media |
| 22 | `amenity_booking` | Reserva de áreas comunes | Media |
| 23 | `visitors` | Registro previo de visitas/invitados | Media |
| 24 | `packages` | Registro de paquetería | Baja-Media |

---

## FASE 6 — Gobernanza y Capa Premium

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 25 | `meeting_minutes` | Actas de reuniones de board/assambleas | Baja |
| 26 | `voting` | Votaciones digitales / e-voting | Baja |
| 27 | `audit_trail` | Log de auditoría avanzado | Baja |
| 28 | `integrations` | Webhooks / API pública / integraciones externas | Baja |
| 29 | `dashboards` | Reporting ejecutivo y analítica | Baja |

---

## Total: 29 módulos

**Implementados:** 7 (01-07, incluyendo users y user_profiles)
**En construcción:** 3 (08, 09, 10 — Bloque C)
**Pendientes:** 19
