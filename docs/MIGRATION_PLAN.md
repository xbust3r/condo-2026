# Plan de Migración — condo-py → Condo-backdmin (Next.js)

**Proyecto:** condo-py API (FastAPI) → Condo-backdmin (Next.js Admin)
**Responsable:** Bulma S
**Creado:** 2026-04-27
**Última actualización:** 2026-04-28
**Estado:** ✅ Migration completa — 29/29 módulos integrados

---

## Resumen

| Módulo condo-py | Estado Backdmin | Prioridad | Fase |
|---|---|---|---|
| residents | ✅ portal existente | 🔴 Alta | 1 |
| announcements | ✅ | 🔴 Alta | 1 |
| charges | ✅ | 🔴 Alta | 2 |
| accounts_receivable | ✅ | 🔴 Alta | 2 |
| charge_types | ✅ | 🔴 Alta | 2 |
| payments | ✅ | 🔴 Alta | 2 |
| receipts | ✅ | 🟡 Media | 2 |
| incidents | ✅ | 🟡 Media | 3 |
| documents | ✅ | 🟡 Media | 3 |
| visitors | ✅ | 🟡 Media | 3 |
| amenities | ✅ | 🟡 Media | 3 |
| meetings | ✅ | 🟡 Media | 4 |
| votes | ✅ | 🟡 Media | 4 |
| packages | ✅ | 🟢 Baja | 4 |
| notifications | ✅ | 🟢 Baja | 4 |
| audit_logs | ✅ | 🟢 Baja | 4 |
| user_profiles | ✅ | 🟢 Baja | 4 |
| ledger_entries | ✅ | 🟢 Baja | 5 |
| resident_profiles | ✅ admin view | 🔵 Extra | — |

---

## Módulos YA integrados ✅

`buildings`, `buildings_types`, `condominiums`, `condominium_roles`, `permissions`, `units`, `unit_occupancies`, `unit_ownerships`, `unit_types`, `users`

---

## FASES DE MIGRACIÓN

### 🔵 FASE 1 — Comunicación y Registro (2 módulos)
**Objetivo:** Funcionalidad básica operativa del condominio

#### 1. `announcements` — Avisos
- `POST /announcements` — crear aviso
- `GET /announcements` — listar con filtros
- `GET /announcements/{id}` — detalle
- `GET /announcements/condominium/{id}/active` — activos (público)
- `PUT /announcements/{id}` — editar
- `DELETE /announcements/{id}` — eliminar suave
- Campos clave: `title`, `content`, `condominium_id`, `priority`, `is_active`, `published_at`

#### 2. `residents` — Residentes/Inquilinos
- `GET /residents/dashboard` — dashboard consolidado
- `GET /residents/profile` — preferencias del residente
- `PUT /residents/profile` — actualizar preferencias
- `GET /residents/incidents` — incidentes del residente
- `GET /residents/packages` — paquetes del residente
- `GET /residents/visitors` — visitantes registrados
- **Nota:** Este módulo trabaja con el perfil del usuario logueado. La UI del admin necesita ver todos los residentes con sus unidades asociadas.

---

### 🔴 FASE 2 — Sistema Financiero (5 módulos)
**Objetivo:** El flujo de cobro y pago del condominio

#### 3. `charge_types` — Catálogo de tipos de cargo
- `GET /charge-types` — listar
- `POST /charge-types` — crear
- `GET /charge-types/{id}` — detalle
- `GET /charge-types/code/{code}` — por código
- `PUT /charge-types/{id}` — editar
- `DELETE /charge-types/{id}` — eliminar suave
- Campos clave: `code`, `name`, `description`, `is_recurrent`, `amount`, `is_active`

#### 4. `charges` — Cargos (genera AR)
- `POST /charges` — crear cargo
- `GET /charges` — listar
- `GET /charges/{id}` — detalle
- `PUT /charges/{id}` — editar
- `DELETE /charges/{id}` — eliminar suave
- `POST /charges/{id}/restore` — restaurar
- `DELETE /charges/{id}/hard` — eliminar permanente
- Campos clave: `condominium_id`, `charge_type_id`, `description`, `amount`, `is_recurrent`, `due_date`, `period`

#### 5. `accounts_receivable` — Cuentas por Cobrar
- `POST /accounts-receivable` — crear AR
- `POST /accounts-receivable/generate-from-charge` — generar AR desde cargo
- `GET /accounts-receivable` — listar con filtros
- `GET /accounts-receivable/{id}` — detalle
- `GET /accounts-receivable/unit/{unit_id}/summary` — resumen de deuda por unidad
- `GET /accounts-receivable/overdue` — morosos
- `PUT /accounts-receivable/{id}` — editar
- `POST /accounts-receivable/{id}/payment` — registrar pago
- Campos clave: `unit_id`, `charge_id`, `amount`, `pending_amount`, `status` (pending/partial/paid/overdue), `due_date`

#### 6. `payments` — Pagos
- `POST /payments` — registrar pago (+ genera receipt)
- `GET /payments` — listar con filtros
- `GET /payments/{id}` — detalle
- `GET /payments/uuid/{uuid}` — por UUID
- Campos clave: `ar_id`, `amount`, `payment_date`, `payment_method`, `reference_number`

#### 7. `receipts` — Recibos
- `GET /receipts` — listar
- `GET /receipts/{id}` — detalle
- `GET /receipts/number/{number}` — por número secuencial
- `GET /receipts/unit/{unit_id}` — recibos por unidad
- Campos clave: `receipt_number` (formato: `C{condo}-{YYYYMM}-{NNNNNN}`), `payment_id`, `amount`, `issue_date`

---

### 🟡 FASE 3 — Operaciones (4 módulos)
**Objetivo:** Gestión diaria del condominio

#### 8. `incidents` — Reporte de Incidentes/Mantenimiento
- `POST /incidents` — crear reporte
- `GET /incidents` — listar
- `GET /incidents/{id}` — detalle
- `GET /incidents/my` — mis incidentes
- `PATCH /incidents/{id}` — actualizar (admin/staff)
- `POST /incidents/{id}/assign` — asignar
- `POST /incidents/{id}/escalate` — escalar
- `POST /incidents/{id}/complete` — completar
- `POST /incidents/{id}/close` — cerrar
- `POST /incidents/{id}/cancel` — cancelar
- Campos clave: `title`, `description`, `unit_id`, `priority`, `status`, `assigned_to`, `category`

#### 9. `documents` — Gestión Documental
- `POST /documents` — subir/registrar
- `GET /documents` — listar
- `GET /documents/{id}` — detalle
- `PUT /documents/{id}` — actualizar metadata
- `DELETE /documents/{id}` — eliminar suave
- Campos clave: `title`, `file_url`, `document_type`, `condominium_id`, `uploaded_by`, `tags`

#### 10. `visitors` — Registro de Visitantes
- `POST /visitors` — registrar visitante
- `GET /visitors` — listar
- `GET /visitors/{id}` — detalle
- `GET /visitors/unit/{unit_id}` — visitas por unidad (host)
- `PATCH /visitors/{id}` — actualizar (host)
- `POST /visitors/{id}/cancel` — cancelar
- `POST /visitors/{id}/check-in` — registrar entrada
- `POST /visitors/{id}/check-out` — registrar salida
- Campos clave: `visitor_name`, `dni`, `unit_id`, `host_user_id`, `check_in`, `check_out`, `access_code`, `status`

#### 11. `amenities` — Amenidades/Áreas Comunes
- `POST /amenities` — crear
- `GET /amenities` — listar
- `GET /amenities/{id}` — detalle
- `PUT /amenities/{id}` — editar
- `DELETE /amenities/{id}` — eliminar suave
- Campos clave: `name`, `description`, `condominium_id`, `capacity`, `schedule`, `requires_booking`, `image_url`

---

### 🟢 FASE 4 — Gobernanza y Utilidades (4 módulos)
**Objetivo:** Funcionalidad de asambleas y herramientas

#### 12. `meetings` — Asambleas y Reuniones
- `POST /meetings` — crear
- `GET /meetings` — listar
- `GET /meetings/{id}` — detalle
- `GET /meetings/condominium/{id}/upcoming` — próximas
- `PUT /meetings/{id}` — editar
- `POST /meetings/{id}/approve` — aprobar
- `POST /meetings/{id}/cancel` — cancelar
- Campos clave: `title`, `meeting_type`, `date`, `location`, `condominium_id`, `status`, `agenda`

#### 13. `votes` — Sistema de Votación
- `POST /votes` — crear votación
- `GET /votes` — listar
- `GET /votes/{id}` — detalle
- `PATCH /votes/{id}` — actualizar (draft)
- `POST /votes/{id}/publish` — publicar
- `POST /votes/{id}/cancel` — cancelar
- `POST /votes/{id}/cast` — votar
- `GET /votes/{id}/results` — resultados
- `GET /votes/{id}/records` — registros (admin)
- Campos clave: `title`, `description`, `meeting_id`, `vote_type`, `options`, `end_date`, `status`

#### 14. `packages` — Paquetería/Entregas
- `POST /packages` — registrar paquete
- `GET /packages` — listar
- `GET /packages/{id}` — detalle
- `GET /packages/condominium/{condominium_id}/pending` — pendientes (conserje)
- `GET /packages/unit/{unit_id}` — por unidad
- `PUT /packages/{id}` — actualizar
- `POST /packages/{id}/deliver` — marcar entregado
- `POST /packages/{id}/cancel` — cancelar
- Campos clave: `unit_id`, `recipient_name`, `carrier`, `tracking_number`, `received_at`, `pickup_code`, `status`

#### 15. `notifications` — Notificaciones
- `GET /notifications` — listar (usuario auth)
- `GET /notifications/{id}` — detalle
- `GET /notifications/unread-count` — conteo sin leer
- `PATCH /notifications/{id}/read` — marcar leído
- `PATCH /notifications/mark-all-read` — marcar todos leídos
- `DELETE /notifications/{id}` — eliminar suave
- **Nota:** Este módulo es de uso interno del sistema. El admin puede ver el log de notificaciones de usuarios.

---

### ⚪ FASE 5 — Auditoría y Ledger (2 módulos)
**Objetivo:** Historial y trazabilidad

#### 16. `audit_logs` — Log de Auditoría (solo lectura)
- `GET /audit-logs` — listar con filtros
- `GET /audit-logs/{id}` — detalle
- `GET /audit-logs/resource/{rt}/{rid}` — por recurso
- `GET /audit-logs/user/{uid}` — por usuario
- Campos clave: `user_id`, `action`, `resource_type`, `resource_id`, `timestamp`, `ip_address`, `details`

#### 17. `user_profiles` — Perfiles de Usuario
- `POST /user-profiles` — crear perfil
- `GET /user-profiles/{user_id}` — obtener por user_id
- `PUT /user-profiles/{user_id}` — actualizar
- Campos clave: `user_id`, `phone`, `emergency_contact`, `notification_preferences`, `avatar_url`

#### 18. `ledger_entries` — Entradas de Libro Mayor
- **Dependiente de:** Fase 2 (payments, charges, accounts_receivable)
- Módulo contable que registra movimientos financieros. Cada payment y charge genera entradas en el ledger.
- Esperar a que la Fase 2 esté completa antes de integrar.

---

## Estructura de Cada Módulo en Next.js

Para cada módulo, crear:

```
src/app/(dashboard)/{module-name}/
├── page.tsx              — lista con DataTable
├── new/page.tsx           — formulario crear
└── [id]/page.tsx          — detalle / editar

src/components/condominium/
├── {module-name}-form.tsx
├── {module-name}-columns.tsx  (columnas DataTable)
└── {module-name}-card.tsx    (opcional)
```

**Dependencias共享:**
- `DataTable` ya existe en `src/components/data-table.tsx`
- Usar el mismo patrón de `units`, `buildings`, `condominiums` como referencia
- Consumir endpoints desde `/api/v1/{module-slug}` (configurar proxy o URL directa)

---

## Notas de Implementación

1. **Orden de implementación por fase es importante:** Fase 1 y 2 son independientes de las siguientes. Fase 3 y 4 pueden ir en paralelo entre sí pero dependen de Fase 1.
2. **Residents es especial:** No tiene CRUD full desde admin — es una vista del perfil de users vinculado a unidades. Revisar `unit_occupancies` para obtener la relación.
3. **Notifications es read-only para admin:** Solo listar y marcar leídas. No crear notificaciones manualmente.
4. **Audit_logs es solo lectura:** No crear, editar ni eliminar.
5. **Ledger_entries:** Depende de que payments y charges estén funcionando. Implementar al final.
6. **Validaciones del API:** Respetar validaciones noted in routes (e.g., PAY-01: amount ≤ pending balance en payments)

---

## Checklist de Entrega por Fase

- [ ] `{module}` list page con DataTable
- [ ] `{module}` create form
- [ ] `{module}` detail/edit page
- [ ] Integración con API (`lib/api.ts` o similar)
- [ ] Tipos TypeScript del response
- [ ] Tests básicos (si aplica)
