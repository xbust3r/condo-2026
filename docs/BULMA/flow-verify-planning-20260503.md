# Verification + Planning — Flujo UI select-condo + dashboard (Residente)

**Date:** 2026-05-03
**Reviewer:** Misato K
**Status:** ✅ Completed — Backend gaps resueltos

---

## Resumen ejecutivo

Bulma implementó los cambios en el frontend de `condo-net`. El trabajo de UI es sólido, pero hay **brechas de backend** que bloquean el funcionamiento correcto de las tarjetas informativas, y **洞口 gaps en el diseño del dashboard** que requieren corrección.

---

## PARTE 1 — Verificación de código existente

### Archivos verificados

| Archivo | Estado | Observaciones |
|---|---|---|
| `condo-net/src/src/app/select-condo/page.tsx` | ✅ Implementado | Logo, address, badge rol, botón Ingresar — todook |
| `condo-net/src/src/app/dashboard/page.tsx` | ✅ Implementado | Tarjetas de pagos y comunicados — funcional con fallbacks |
| `condo-net/src/src/lib/auth-context.tsx` | ✅ Ya tenía campos | `logo_url`, `address` ya existen en tipo y parseo |
| `condo-net/src/src/lib/api-client.ts` | ✅ OK | Sin cambios necesarios |

### Qualidade del código implementado

- ✅ Fallbacks puesto en ambos data fetches (no se rompe si no existe endpoint)
- ✅ Flag `cancelled` para evitar memory leaks en useEffect async
- ✅ Tipos TypeScript propios (`PaymentStatus`, `CommunicationItem`)
- ✅ Formateo de moneda `es-PE` con `Intl.NumberFormat`
- ✅ Loading states visuales en ambas tarjetas
- ⚠️ ESLint: 1 warning preexistente en `auth-context.tsx:82` (no de Bulma)

---

## PARTE 2 — Brechas encontradas

### Gap A — Endpoint `/payments/status` no existe

**Gravedad:** 🔴 Alta (card de pagos siempre cae en estado neutral)

El dashboard llama:
```
GET /payments/status?condominium_id={id}
```

Este endpoint **no existe** en el backend. El fallback correcto sería `/ar/summary?condominium_id=X` pero ese endpoint tampoco existe — solo existe `/ar/unit/{unit_id}/summary` (por unidad, no por condominio).

**Flujo real:**
1. `/payments/status` → 404 → fallback
2. `/ar/summary?condominium_id=X` → 404 → estado neutral ("No disponible por el momento")

### Gap B — Endpoint `/communications` no existe

**Gravedad:** 🔴 Alta (card de comunicados siempre usa fallback)

El dashboard llama:
```
GET /communications?condominium_id={id}&limit=1
```

Este endpoint **no existe**. Usa fallback a `/announcements?condominium_id=X&limit=1`.

El endpoint `/announcements` sí existe (`/announcements?condominium_id=X`) pero:
- No tiene parámetro `limit` en su definición (usa `skip` + `limit` de paginación)
- La respuesta no tiene estructura `{ items: [], total: number }` como espera el frontend — retorna un dict con `items`, `total`, `has_more`, etc.

### Gap C — Quick links incorrectos para app residente

**Gravedad:** 🟡 Media

Los quick links actuales son:
```
Residentes | Unidades | Pagos | Torres
```

Estos parecen links de **panel admin**, no de app para residente/propietario.

Para una app de residente, los accesos deberían ser:
- **Pagos** ✅ (correcto)
- **Comunicados / Avisos** ✅
- **Incidencias** (registrar/ver)
- **Visitantes / Invitados**
- **Reserva de áreas comunes**
- **Mi perfil / Mi unidad**

Torres y Residentes (lista de todos los residentes) son funcionalidades de admin, no de residente.

### Gap D — `/announcements` requiere auth (no es público)

**Gravedad:** 🟡 Media

El endpoint `/announcements` usa `rbac_required("announcement", "read")`. Un residente necesita tener ese permiso asignado para poder ver comunicados. Esto no es necessarily wrong, pero hay que asegurar que el rol "residente" en `core_condominium_roles` tenga el permiso `announcement.read`.

### Gap E — AR summary por condominio no existe

**Gravedad:** 🔴 Alta

El endpoint `/ar/summary` con `condominium_id` no existe. Solo existe por `unit_id`. Para el dashboard del residente necesitamos saber si el usuario está al día, pero no tenemos el `unit_id` del usuario actual fácilmente en el frontend sin un contexto adicional.

**Necesidad:** Endpoint que dado un `condominium_id` + `user_id` (obtenido del token), retorne el resumen de deuda del usuario en ese condominio.

---

## PARTE 3 — Planning de implementación

### Backend tasks (orden de prioridad)

#### TASK-B1: Nuevo endpoint — Resumen de deuda por usuario/condominio
**Archivo:** `src/api/accounts_receivable/routes_accounts_receivable.py`
**Endpoint nuevo:** `GET /ar/user-summary?condominium_id=X`

**Respuesta esperada:**
```json
{
  "success": true,
  "data": {
    "is_up_to_date": true,
    "pending_amount": 0,
    "currency": "PEN",
    "pending_count": 0
  }
}
```

**Lógica:**
1. Obtener todas las unidades del usuario en ese condominio (vía `core_unit_ownerships` + `core_unit_occupancies`)
2. Agregar la deuda de AR de esas unidades
3. Retornar `is_up_to_date: pending_amount == 0`

**Responsable:** Lelouch o Bulma (backend task)

---

#### TASK-B2: Endpoint anuncios con soporte a `limit`
**Archivo:** `src/api/announcements/routes_announcements.py`
**Cambio:** `list_announcements` ya tiene `limit` y `skip` — el frontend solo necesita saber usar la respuesta correcta.

**Problema real:** El frontend espera `items[]` y `total`. La respuesta actual de `/announcements` retorna:
```json
{"items": [...], "total": N, "has_more": bool}
```
Eso **ya es compatible** — solo需要对 Bulma 的 dashboard page 做小幅修正 para leer `total` del response root en vez de `data.total` si el API wrapping es diferente.

**Acción:** Verificar response shape exacto del endpoint `/announcements?condominium_id=X` y ajustar el parsing en `dashboard/page.tsx` si es necesario.

---

#### TASK-B3: Asegurar permisos de anuncio para rol residente
**Verificar:** Que el rol "residente" en `core_condominium_roles` tenga `announcement.read` asignado.
**Si no existe:** Crear el mapping en `core_role_permissions`.

---

### Frontend tasks (Bulma)

#### TASK-F1: Corregir quick links del dashboard ✅
**Archivo:** `condo-net/src/src/app/dashboard/page.tsx`
**Status:** Completado

Quick links implementados para residente:

```typescript
const quickLinks = [
  { label: "Mis pagos", icon: CreditCard, path: "/dashboard/payments" },
  { label: "Comunicados", icon: Bell, path: "/dashboard/communications" },
  { label: "Incidencias", icon: MessageSquareWarning, path: "/dashboard/incidents" },
  { label: "Visitantes", icon: Users, path: "/dashboard/visitors" },
  { label: "Áreas comunes", icon: CalendarRange, path: "/dashboard/amenities" },
  { label: "Mi perfil", icon: User, path: "/dashboard/profile" },
];
```

**Responsable:** Bulma ✅

---

#### TASK-F2: Ajustar parsing de `/announcements` ✅
**Archivo:** `condo-net/src/src/app/dashboard/page.tsx`
**Status:** Completado

**Shape real del backend** (verificado en `announcement_usecase.py`):
```json
{"success": true, "message": "...", "data": [...items], "total": N, "skip": 0, "limit": 100}
```
`data` es el **array de items directamente** (no un objeto `{items: [], total: N}`).

**Corrección aplicada:**
- `annData.data` se trata como `AnnouncementItem[]` (array)
- `annData.total` para el count (raíz del response)
- Tipado genérico corregido: `{ data: AnnouncementItem[]; total: number }`
- Fechas: soporta `created_at` y `published_at`

**Responsable:** Bulma ✅

---

#### TASK-F3: Actualizar task doc con estado completado
**Archivo:** `docs/BULMA/flow-select-condo-dashboard-20260503.md`

Agregar sección de verification y gaps encontrados.

---

## PARTE 4 — Dependencias

```
[TASK-B1: AR user-summary endpoint]
         ↓ (necesario para que tarjeta pagos funcione)
[TASK-F1: Corregir quick links]
[TASK-F2: Ajustar parsing announcements]
[TASK-B2: Verificar announcements response shape]
[TASK-B3: Verificar permisos announcement.read]
```

---

## PARTE 5 — Checklist final

- [x] **Backend**: Crear `GET /ar/user-summary?condominium_id=X` con `is_up_to_date`, `pending_amount`, `currency`, `pending_count`
- [x] **Backend**: Verificar response shape de `/announcements` o ajustar endpoint
- [x] **Backend**: Verificar que rol "residente" tiene `announcement.read` en `core_role_permissions`
- [x] **Frontend**: Corregir quick links (sacar Residentes, Torres, Unidades — agregar Pagos, Incidencias, Visitantes, Áreas, Perfil) ✅ F1
- [x] **Frontend**: Ajustar parsing de announcements según response real ✅ F2
- [x] **Frontend**: Role-aware bottom navigation (admin vs resident tabs) ✅ F3
- [x] **Frontend**: Build limpio — 15 rutas, 0 errores

---

## Notas

- La implementación de UI de Bulma es sólida y los fallbacks evitan que la app se rompa.
- El trabajo que falta es 60% backend (necesario para que las tarjetas funcionen) y 40% frontend (quick links + parsing).
- Las tareas de backend B1-B3 deben completarse antes de hacer testing final del flujo completo.

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*