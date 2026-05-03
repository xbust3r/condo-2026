# Task — Flujo UI: select-condo + dashboard (residente)

**Developer:** Bulma S
**Date:** 2026-05-03
**Repo:** `/home/miguel/servers/condo-net`
**Source:** `#flujo-de-interfaz` — Mike Ross
**Status:** ✅ Completada (2026-05-03)

---

## Contexto

`condo-net` es el frontend mobile-first para residentes/propietarios del sistema `condo-py`.
El flujo actual es:

1. Login (`/login`)
2. Selección de condominio (`/select-condo`)
3. Dashboard (`/dashboard`)

El flujo descrito en el ticket es el flujo **RESIDENTE/PROPIETARIO** (no admin).
Las tarjetas de selection y dashboard deben reflejar info del residente, no del admin.

---

## Cambios requeridos

### 1. `/select-condo` — Tarjeta de condominio

**Archivo:** `src/src/app/select-condo/page.tsx`

La tarjeta actual solo muestra: icono genérico, nombre, ciudad, código.

**Falta agregar:**

| Campo | Fuente | Notas |
|---|---|---|
| Logotipo del condominio | `condo.logo_url` | Mostrar imagen o placeholder si no existe |
| Dirección completa | `condo.address` | Mostrar dirección fiscal/dirección del condo |
| Estado del usuario en ese condominio | `condo.role` o similar | Mostrar texto: "Propietario" / "Inquilino" / "Residente" |
| Botón "Ingresar" con etiqueta clara | — | Reemplazar la flecha `ChevronRight` por un botón tipo `Button` con texto "Ingresar" |

**Diseño de la tarjeta:**
- Logo a la izquierda (recuadro 48x48, rounded)
- Nombre + dirección + ciudad en el centro
- Badge de rol (Propietario/Inquilino) debajo del nombre
- Botón "Ingresar" a la derecha

---

### 2. `/dashboard` — Dashboard residente

**Archivo:** `src/src/app/dashboard/page.tsx`

El dashboard actual solo tiene 4 iconos de acceso rápido + tarjeta de info del condominio.

**Falta agregar (encima de los iconos):**

#### Tarjeta 1 — Estado de pagos
- Título: "¿Al día en sus pagos?"
- Si está al día: mensaje verde + check icon
- Si tiene deuda: mensaje rojo + monto pendiente
- Fuente de datos: consumir `GET /accounts-receivable?unit_id=X` (o endpoint de ledger por unidad) y calcular saldo pendiente

#### Tarjeta 2 — Comunicados / Notificaciones pendientes
- Título: "Comunicados"
- Si hay nuevos: mostrar badge con count + título del comunicado más reciente
- Si no hay: mensaje "Sin novedades"
- Fuente de datos: consumir `GET /announcements` filtrado por `condominium_id` activo

**Los iconos de acceso rápido permanecen** (Residentes, Unidades, Pagos, Torres — o los que correspondan al rol residente).

---

## Archivos a tocar

| Archivo | Cambio |
|---|---|
| `src/src/app/select-condo/page.tsx` | Enriquecer tarjeta con logo, address, role badge, botón "Ingresar" |
| `src/src/app/dashboard/page.tsx` | Agregar 2 tarjetas informativas encima de quick links |

---

## Notas técnicas

- El `useAuth()` hook ya provee `user.condominiums[]` con los datos del condominio seleccionado.
- Para el estado de pagos, buscar endpoint en `condo-py` que dé saldo por unidad. Revisar `core_ledger_entries` o `core_accounts_receivable`.
- Para comunicados, usar `GET /announcements` con `condominium_id` del contexto.
- Si no existe endpoint de saldo pendiente por unidad, crear el ticket complementario para el backend.
- Los cambios son puramente frontend (UI/UX), no requieren cambios de API por ahora salvo que se descubra que falta algún endpoint.

---

## Checklist de implementación

- [x] select-condo: agregar `logo_url` a la tarjeta (con placeholder Building2)
- [x] select-condo: agregar `address` completo
- [x] select-condo: agregar badge de rol (Propietario/Inquilino/Residente)
- [x] select-condo: cambiar ChevronRight por botón "Ingresar"
- [x] dashboard: agregar tarjeta "Estado de pagos" (lógica al día / con deuda)
- [x] dashboard: agregar tarjeta "Comunicados" (count + más reciente)
- [x] Probar flujo completo: login → select-condo → dashboard
- [x] auth-context: agregar `address`, `logo_url`, `ownerships` al UserContext
- [x] Build verificado: compilación exitosa en Next.js 16 (Turbopack)

---

## Notas de implementación

- `address` y `logo_url` ya existían en la entidad `CondominiumEntity` del backend — solo se agregó el mapeo en auth-context
- Balance se obtiene por unidad usando `GET /balances/unit/{unit_id}` (endpoint creado en Sprint A)
- Los `ownerships` vienen del endpoint `GET /me/contexts` — se exponen ahora en `UserContext`
- El badge de rol prioriza: Propietario > Inquilino > Administrador > Residente

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*