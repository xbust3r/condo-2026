# SPRINT 16 — Reserva de Amenities: Motor de Políticas

**Fecha base:** 2026-05-03  
**Revisión arquitectónica prioritaria:** Lelouch S  
**Coordinación:** Misato K  
**Ejecución:** Bulma S  
**Proyecto:** condo-py

---

## 0. Dictamen ejecutivo

Se aprueba la dirección general de Misato (**motor de políticas configurable, no reglas hardcodeadas**), pero el planning original necesitaba una corrección táctica importante.

El error de fondo era mezclar en una sola capa tres problemas distintos:

1. **Política** → quién puede reservar y con qué límites  
2. **Disponibilidad** → slots, ventanas, aforo, bloqueos  
3. **Asignación** → booking, waitlist, prioridad, reasignación

Si esas tres piezas se mezclan, el sistema se vuelve frágil y opaco. La solución correcta para condo-py es:

- mantener la **cascada de políticas en 3 capas**
- separar **policy / availability / allocation**
- incorporar **auditoría, concurrencia e idempotencia desde el inicio**
- ejecutar el trabajo con flujo controlado por Misato y **Bulma con una sola tarea activa a la vez**

Ese será el tablero oficial.

---

## 1. Problema que resolvemos

El sistema debe soportar reservas de amenities en condominios con alta variabilidad operativa:

- condominios con muchas unidades y pocos recursos compartidos
- amenities con comportamientos distintos (`piscina`, `parrilla`, `SUM`, `guest suite`, `gym`)
- reglas específicas por condominio y por amenity
- feriados y horas pico con demanda muy superior a la oferta

### Ejemplos reales del problema

- **Piscina**: aforo limitado + demasiadas unidades + necesidad de limitar reservas por unidad por mes
- **Parrilla/SUM en feriados**: todos quieren el mismo día; el sistema debe favorecer equidad, no solo velocidad
- **Gym/Piscina**: operan por slots cortos
- **SUM/Parrilla**: suelen operar por ventanas largas o reservas discretas

### Principio rector

**No vamos a modelar cada excepción del mundo.**  
Vamos a modelar un conjunto corto de primitivas configurables que puedan combinarse.

Jaque mate al `if/else` infinito.

---

## 2. Auditoría del estado actual del código (hecha sobre repo real)

Esta sección reemplaza la parte especulativa del planning inicial. Se revisó el código real antes de redefinir el sprint.

### 2.1 Lo que ya existe en booking

Archivo auditado:  
`src/library/dddpy/core_amenity_bookings/usecase/booking_usecase.py`

`BookingUseCase.create()` ya hace:

- validación de que el amenity existe y es reservable
- validación `unit -> building`
- validación `owner -> unit`
- detección de solapamiento vía `find_overlapping()`
- snapshot de unidad y owner
- creación del booking con estado inicial `draft` o `pending_approval`

### 2.2 Lo que ya existe en amenity

Archivo auditado:  
`src/library/dddpy/core_amenities/infrastructure/dbamenity.py`

`core_amenities` ya tiene campos relevantes:

- `max_capacity`
- `booking_duration_min`
- `requires_approval`
- `booking_price`
- `security_deposit_amount`
- `is_reservable`
- `scope` / `building_id`

Esto significa que **parte del modelo de disponibilidad ya existe**, aunque todavía no está separado de una estrategia completa de booking/policies.

### 2.3 Lo que ya existe a nivel condominio

Archivo auditado:  
`src/alembic/versions/056_add_condominium_amenity_settings.py`

`amenity_settings` en `core_condominiums` **no resuelve políticas de reserva**. Hoy solo cubre flags contables:

- `enable_amenity_booking_charges`
- `include_amenity_bookings_in_receipts`
- `include_amenity_bookings_in_building_balance`
- `include_amenity_bookings_in_condominium_balance`

Conclusión: **no existe todavía un policy engine**.

### 2.4 Gaps reales confirmados

No existe hoy:

- límite de reservas por unidad por período
- límite de reservas activas por unidad
- elegibilidad configurable (`owner_only`, `good_standing_only`, etc.)
- modelo de invitados / tamaño de grupo
- waitlist
- prioridad configurable con trazabilidad
- lifecycle completo de waitlist
- diferencia formal entre `slots continuos` y `ventanas discretas`
- contrato de `effective policy`
- snapshot auditable de la decisión de asignación
- idempotencia / estrategia explícita de concurrencia para alta demanda

---

## 3. Correcciones arquitectónicas sobre el planning inicial

### 3.1 Se mantiene

Estas decisiones de Misato se conservan porque son correctas:

- ✅ motor de políticas en 3 capas
- ✅ evitar hardcodear reglas por condominio
- ✅ usar prioridad configurable (`fifo`, `less_usage_first`, `equal_share`)
- ✅ dividir la implementación en fases manejables

### 3.2 Se corrige

Se introducen estas correcciones obligatorias:

1. **Fase 0 obligatoria**: auditoría + contrato del motor  
2. **Separación explícita** entre policy, availability y allocation  
3. **Modelo híbrido** de políticas: campos tipados + JSON para edge cases  
4. **Concurrencia e idempotencia desde temprano**, no al final  
5. **Guest count / reserva grupal** como parte del modelo base  
6. **Waitlist auditable**, no solo una cola ciega  
7. **Parámetro de ventana de evaluación** para `less_usage_first`  
8. **Soporte para dos modelos operativos**:
   - `CONTINUOUS_SLOTS`
   - `DISCRETE_WINDOWS`

---

## 4. Arquitectura aprobada

## 4.1 Cascada de políticas

Se mantiene la cascada original:

```text
1. Global del condominio
2. Por tipo de amenity
3. Override por amenity específico
```

### Regla de precedencia

El nivel inferior sobreescribe al superior **solo para el campo definido**.  
No se reemplaza el objeto completo.

Ejemplo:

- Global: `max_reservations_per_period = 2`
- Tipo `POOL`: `max_active_reservations = 1`
- Amenity específico `pool_tower_a`: `max_capacity_per_slot = 50`

**Effective policy resultante:**

- `max_reservations_per_period = 2`
- `max_active_reservations = 1`
- `max_capacity_per_slot = 50`

### Contrato obligatorio: `EffectiveAmenityPolicy`

Antes de implementar lógica, debe existir un contrato único resuelto por código.

```python
class EffectiveAmenityPolicy:
    scope_level: str
    eligibility_mode: str
    max_reservations_per_period: int | None
    period_unit: str | None              # day | week | month
    period_value: int | None             # e.g. 1 month, 3 months
    max_active_reservations: int | None
    max_guests: int | None
    priority_policy: str                 # fifo | less_usage_first | equal_share | owner_only
    priority_window_unit: str | None     # month | quarter | year
    priority_window_value: int | None
    waitlist_mode: str                   # auto_confirm | notify_and_confirm | admin_review
    approval_mode: str                   # auto | amenity_requires_approval | admin_only
    blocked_dates: list[str]
    advance_booking_days: int | None
    cancel_window_hours: int | None
    slot_mode: str                       # CONTINUOUS_SLOTS | DISCRETE_WINDOWS
    slot_interval_min: int | None
    max_capacity_per_slot: int | None
    extra_rules_json: dict
```

Este contrato es el rey del tablero. Ningún use case debe interpretar políticas por su cuenta.

---

## 5. Separación por capas

## 5.1 Policy layer

Responde:

- ¿quién puede reservar?
- ¿cuántas veces?
- ¿con qué límites?
- ¿qué política de prioridad aplica?

Incluye:

- elegibilidad
- fairness
- límites por período
- límites activos
- invitados
- owner vs tenant vs guest rules
- ventana de evaluación para prioridad

## 5.2 Availability layer

Responde:

- ¿qué se puede reservar y cuándo?
- ¿cómo se parte el tiempo?
- ¿qué días están bloqueados?
- ¿cuál es el aforo real por slot?

Incluye:

- `slot_mode`
- intervalos
- ventanas discretas
- horarios operativos
- aforo
- bloqueos / feriados
- booking window / cancel window

## 5.3 Allocation layer

Responde:

- ¿la reserva entra directa o va a waitlist?
- ¿quién sube cuando alguien cancela?
- ¿cómo se audita la decisión?

Incluye:

- booking creation
- waitlist lifecycle
- scoring
- reasignación
- notificación
- expiración
- conversión a booking

---

## 6. Modelo de datos propuesto

La propuesta original de `policy_type + key + value` es demasiado genérica para el core del sistema.  
Se reemplaza por un **modelo híbrido**: campos tipados para reglas núcleo + JSON para extensiones raras.

## 6.1 Nueva tabla `core_amenity_policies`

Una fila representa un scope de política.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador |
| `condominium_id` | FK | Condominio |
| `scope_level` | ENUM | `CONDOMINIUM` / `AMENITY_TYPE` / `AMENITY` |
| `amenity_type` | VARCHAR NULL | `POOL`, `GRILL`, `SUM`, etc. |
| `amenity_id` | FK NULL | Override puntual |
| `eligibility_mode` | VARCHAR | `all_residents`, `owner_only`, `good_standing_only` |
| `max_reservations_per_period` | INT NULL | límite principal |
| `period_unit` | VARCHAR NULL | `day`, `week`, `month`, `quarter` |
| `period_value` | INT NULL | e.g. `1`, `3` |
| `max_active_reservations` | INT NULL | reservas activas simultáneas |
| `max_guests` | INT NULL | invitados máximos |
| `priority_policy` | VARCHAR | `fifo`, `less_usage_first`, `equal_share` |
| `priority_window_unit` | VARCHAR NULL | ventana de evaluación |
| `priority_window_value` | INT NULL | e.g. `1 month`, `3 months` |
| `waitlist_mode` | VARCHAR | `auto_confirm`, `notify_and_confirm`, `admin_review` |
| `approval_mode` | VARCHAR | `auto`, `amenity_requires_approval`, `admin_only` |
| `extra_rules_json` | JSON NULL | edge cases |
| `is_active` | BOOL | flag de vigencia |
| `version` | INT | versionado simple |

## 6.2 Nueva tabla `core_amenity_availability_rules`

Separa disponibilidad de policy.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador |
| `amenity_id` | FK | Amenity específico |
| `slot_mode` | ENUM | `CONTINUOUS_SLOTS` / `DISCRETE_WINDOWS` |
| `slot_interval_min` | INT NULL | para slots continuos |
| `window_start_time` | TIME NULL | para ventanas discretas |
| `window_end_time` | TIME NULL | para ventanas discretas |
| `max_capacity_per_slot` | INT | aforo utilizable |
| `advance_booking_days` | INT NULL | hasta cuántos días antes se puede reservar |
| `cancel_window_hours` | INT NULL | cancelación mínima |
| `blocked_dates_json` | JSON NULL | feriados / cierres |
| `opening_hours_json` | JSON NULL | horario operativo |
| `is_active` | BOOL | vigencia |

## 6.3 Extensión a `core_amenity_bookings`

Se agregan campos al booking existente en vez de crear una entidad paralela innecesaria.

| Campo nuevo | Tipo | Motivo |
|---|---|---|
| `guest_count` | INT | tamaño real del grupo |
| `allocation_source` | VARCHAR | `DIRECT`, `WAITLIST`, `ADMIN_OVERRIDE` |
| `waitlist_entry_id` | FK NULL | trazabilidad |
| `idempotency_key` | VARCHAR NULL | protección contra reintentos |
| `policy_snapshot_json` | JSON NULL | effective policy usada |
| `allocation_reason_json` | JSON NULL | por qué fue aceptada / reasignada |

## 6.4 Nueva tabla `core_amenity_usage_logs`

Para fairness y reportes.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador |
| `amenity_id` | FK | Amenity |
| `unit_id` | FK | Unidad |
| `user_id` | FK | Usuario |
| `booking_id` | FK | Booking asociado |
| `guest_count` | INT | uso real |
| `used_at` | DATETIME | timestamp de uso |
| `source_status` | VARCHAR | `completed`, `attended`, etc. |

## 6.5 Nueva tabla `core_amenity_waitlist`

Waitlist con lifecycle completo.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador |
| `amenity_id` | FK | Amenity |
| `unit_id` | FK | Unidad |
| `user_id` | FK | Usuario |
| `booking_date` | DATE | Fecha solicitada |
| `requested_start_at` | DATETIME | inicio |
| `requested_end_at` | DATETIME | fin |
| `guest_count` | INT | grupo solicitado |
| `status` | VARCHAR | `WAITING`, `NOTIFIED`, `CONFIRMED`, `EXPIRED`, `CANCELLED`, `CONVERTED` |
| `priority_score_snapshot` | DECIMAL | score guardado |
| `priority_reason_json` | JSON | explicación auditable |
| `effective_policy_snapshot_json` | JSON | política aplicada |
| `expires_at` | DATETIME NULL | deadline para confirmar |
| `notified_at` | DATETIME NULL | timestamp de aviso |
| `converted_booking_id` | FK NULL | trazabilidad |

## 6.6 Nueva tabla `core_amenity_allocation_audit`

Para defender decisiones frente a reclamos.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador |
| `amenity_id` | FK | Amenity |
| `booking_id` | FK NULL | Booking relacionado |
| `waitlist_entry_id` | FK NULL | Waitlist relacionada |
| `decision_type` | VARCHAR | `BOOKING_ACCEPTED`, `BOOKING_REJECTED`, `WAITLIST_INSERTED`, `WAITLIST_PROMOTED` |
| `decision_reason` | VARCHAR | motivo corto |
| `decision_context_json` | JSON | detalle |
| `created_at` | DATETIME | traza |

---

## 7. Reglas de negocio obligatorias

## 7.1 Elegibilidad

El sistema debe poder resolver, al menos:

- `all_residents`
- `owner_only`
- `good_standing_only`
- `owner_or_tenant`
- `admin_override`

## 7.2 Uso por período

Ejemplos:

- `max_reservations_per_period = 2`, `period = month`
- `max_active_reservations = 1`
- `max_guests = 5`

## 7.3 Prioridad

Políticas mínimas:

- `fifo`
- `less_usage_first`
- `equal_share`

### Regla nueva obligatoria

`less_usage_first` **debe parametrizar su ventana de evaluación**.

Ejemplos:

- último mes
- últimos 3 meses
- trimestre actual

Sin esa ventana, la política es ambigua.

## 7.4 Waitlist lifecycle

La waitlist no puede quedarse en un limbo.

Lifecycle mínimo:

```text
WAITING
  -> NOTIFIED
  -> CONFIRMED
  -> CONVERTED

WAITING
  -> EXPIRED

WAITING
  -> CANCELLED
```

Si el modo es `notify_and_confirm`, debe existir un `expires_at`.  
Si el usuario no confirma a tiempo, la plaza pasa al siguiente.

## 7.5 Reserva grupal

Una reserva no es igual a una persona.  
Debe existir `guest_count`, porque el aforo real depende del grupo, no del número de bookings.

## 7.6 Concurrencia

El enemigo real del sistema no es la tabla: es el doble booking bajo alta demanda.

Se define como obligatorio desde fase temprana:

- operación de asignación dentro de transacción
- verificación final de capacidad antes de persistir
- estrategia de `idempotency_key` para retries
- constraints/índices útiles para lookup por amenity+fecha
- tests de concurrencia mínima en integración

---

## 8. Algoritmo de asignación aprobado

## 8.1 Flujo general

```text
Solicitud
  -> validar integridad básica
  -> resolver effective policy
  -> validar elegibilidad / límites / ventanas
  -> resolver disponibilidad real del slot
      -> si hay capacidad: crear booking
      -> si no hay capacidad: waitlist
  -> registrar allocation audit
```

## 8.2 Flujo de reasignación

```text
Se libera capacidad
  -> buscar waitlist elegible
  -> recalcular o reutilizar score según policy
  -> seleccionar candidato
  -> notificar o convertir automáticamente
  -> registrar auditoría completa
```

## 8.3 Score de prioridad

La estrategia debe ser configurable por política:

- `snapshot_on_join`
- `recompute_on_reassign`

### Dictamen

Por defecto, se recomienda:

- `fifo` -> `snapshot_on_join`
- `less_usage_first` -> `recompute_on_reassign`
- `equal_share` -> `recompute_on_reassign`

Eso preserva equidad donde importa y estabilidad donde conviene.

---

## 9. Plan de implementación corregido

Se conserva la idea de fases, pero se agrega **Fase 0** y se redistribuyen responsabilidades.

## Fase 0 — Auditoría + contrato del motor

**Objetivo:** eliminar ambigüedad antes de tocar persistencia.  
**Responsable:** Lelouch (arquitectura)  
**Coordinación:** Misato  
**Ejecución puntual de validaciones de código si hace falta:** Bulma

### Entregables

1. Auditoría del booking existente documentada
2. Contrato `EffectiveAmenityPolicy`
3. Definición formal de `slot_mode`
4. Estrategia de concurrencia / idempotencia
5. Lista final de tablas y columnas aprobadas

### Definition of Done

No queda ninguna ambigüedad sobre:

- precedencia de políticas
- merge/override
- waitlist lifecycle
- score policy
- slot model
- guest_count
- concurrencia

---

## Fase 1 — Policy foundation + trazabilidad

**Objetivo:** construir el policy engine núcleo y dejar trazabilidad temprana.  
**Responsable de implementación:** Bulma  
**Review arquitectónico:** Lelouch  
**Coordinación:** Misato

### Tareas

1. Crear `core_amenity_policies`
2. Extender `core_amenity_bookings` con `guest_count`, `allocation_source`, `idempotency_key`, `policy_snapshot_json`, `allocation_reason_json`
3. Crear `core_amenity_allocation_audit`
4. Implementar `PolicyResolver` con cascada `CONDOMINIUM -> AMENITY_TYPE -> AMENITY`
5. Implementar validaciones:
   - `validate_eligibility()`
   - `validate_usage_limit()`
   - `validate_active_reservations()`
   - `validate_guest_limit()`
6. Registrar motivo de rechazo y snapshot de política
7. Tests de integración para límites por período y reservas activas

### Definition of Done

- una unidad puede ser rechazada por límite mensual con motivo auditable
- una unidad puede ser rechazada por límite de reservas activas
- la decisión deja snapshot de política y razón de negocio

---

## Fase 2 — Availability model + concurrencia segura

**Objetivo:** modelar disponibilidad correctamente y blindar el booking bajo demanda.  
**Responsable de implementación:** Bulma  
**Review arquitectónico:** Lelouch  
**Coordinación:** Misato

### Tareas

1. Crear `core_amenity_availability_rules`
2. Definir y soportar `slot_mode`:
   - `CONTINUOUS_SLOTS`
   - `DISCRETE_WINDOWS`
3. Implementar validaciones:
   - `validate_booking_window()`
   - `validate_cancel_window()`
   - `validate_blocked_dates()`
   - `validate_capacity()` usando `guest_count`
4. Implementar cálculo de disponibilidad real
5. Endurecer `BookingUseCase.create()` con:
   - transacción de asignación
   - chequeo final de capacidad
   - soporte de `idempotency_key`
6. Endpoint `GET /amenities/{id}/availability?date=YYYY-MM-DD`
7. Tests de concurrencia / retries / capacidad

### Definition of Done

- el sistema distingue piscina por slots de parrilla por ventana discreta
- una reserva no sobrepasa aforo por grupo
- retries no generan doble booking lógico

---

## Fase 3 — Waitlist + prioridad + reporting final

**Objetivo:** resolver alta demanda con fairness auditable.  
**Responsable de implementación:** Bulma  
**Review arquitectónico:** Lelouch  
**Coordinación:** Misato

### Tareas

1. Crear `core_amenity_waitlist`
2. Crear `core_amenity_usage_logs`
3. Implementar `PriorityCalculator`:
   - `fifo`
   - `less_usage_first`
   - `equal_share`
4. Implementar lifecycle completo de waitlist
5. Implementar `WaitlistAllocator` con `snapshot_on_join` / `recompute_on_reassign`
6. Trigger de notificación / expiración / conversión
7. Endpoints:
   - `GET /amenities/{id}/waitlist`
   - `POST /amenities/{id}/waitlist/{entry_id}/confirm`
8. Reporting:
   - usage report
   - métricas de rechazo
   - métricas de waitlist/promoción/expiración
9. Tests end-to-end de alta demanda

### Definition of Done

- slot lleno -> waitlist
- cancelación/liberación -> promoción según policy
- cada decisión deja score + razón + snapshot de política

---

## 10. Endpoints propuestos

```text
# Policies
GET    /amenities/{id}/policies
POST   /amenities/{id}/policies
PUT    /amenities/{id}/policies/{policy_id}

# Availability
GET    /amenities/{id}/availability?date=YYYY-MM-DD

# Bookings
POST   /amenities/{id}/bookings
GET    /amenities/{id}/bookings
DELETE /bookings/{id}

# Waitlist
GET    /amenities/{id}/waitlist
POST   /amenities/{id}/waitlist/{entry_id}/confirm
POST   /amenities/{id}/waitlist/{entry_id}/cancel

# Reporting
GET    /amenities/{id}/usage-report?period=month
GET    /amenities/{id}/allocation-audit?date=YYYY-MM-DD
```

---

## 11. Decisiones de producto que siguen abiertas

Estas preguntas deben responderse antes de cerrar Fase 1/Fase 2, pero ya están mejor enmarcadas:

1. **¿Políticas por API o admin UI?**  
   Recomendación: API primero, UI después.

2. **¿Waitlist automática o con aprobación?**  
   Recomendación: soportar estrategia configurable:
   - `auto_confirm`
   - `notify_and_confirm`
   - `admin_review`

3. **¿La prioridad se fija al entrar o se recalcula?**  
   Recomendación: configurable por política, no global.

4. **¿Propietarios e inquilinos compiten igual?**  
   Recomendación: default igualitario, con `eligibility_mode` configurable.

5. **¿Qué amenities usan slot continuo vs ventana discreta?**  
   Recomendación inicial:
   - `POOL`, `GYM` -> `CONTINUOUS_SLOTS`
   - `GRILL`, `SUM`, `EVENT_ROOM` -> `DISCRETE_WINDOWS`

---

## 12. Riesgos y mitigación

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| Mezclar policy con scheduling | Alta | Separar tablas y servicios desde Fase 0 |
| Puro JSON vuelva inqueryable el sistema | Alta | Modelo híbrido tipado + JSON opcional |
| Waitlist injusta o inexplicable | Alta | allocation audit + score snapshot + reason json |
| Doble booking por carrera | Alta | transacción + chequeo final + idempotency |
| Alcance del sprint se descontrole | Media | una sola tarea activa para Bulma |
| Política `less_usage_first` ambigua | Media | ventana de evaluación obligatoria |

---

## 13. Flujo operativo oficial: Misato ↔ Bulma ↔ Lelouch

Esta sección adopta expresamente la instrucción operativa ya usada en condo-py para evitar caos de ejecución.

### Regla de coordinación

- **Misato controla el tablero**
- **Bulma ejecuta la tarea activa**
- **Lelouch define criterio, revisa arquitectura y bloquea desvíos**
- Solo se etiqueta a quien sigue en el turno

### Ciclo obligatorio

1. Misato habilita **una sola tarea activa** para Bulma
2. Bulma implementa esa tarea y responde **solo a Misato**
3. Misato revisa
4. Si hay observaciones, la tarea vuelve a Bulma
5. Si la revisión queda limpia y el cambio toca arquitectura crítica, **Lelouch valida el gate**
6. Solo entonces Misato habilita la siguiente tarea

### Regla crítica

**No se avanza a la siguiente tarea mientras la actual tenga observaciones abiertas.**

Esto reemplaza la asignación original donde Fase 2 quedaba directamente en manos de Lelouch como implementador.  
En condo-py la ejecución debe quedar centralizada en Bulma; Lelouch actúa como arquitecto y revisor de cierre.

---

## 14. Backlog secuencial para Bulma

Para respetar el flujo operativo, estas son las tareas en orden.  
**Solo una puede estar activa a la vez.**

### B0 — Levantamiento de booking actual
- ~~pendiente~~ → ✅ **LISTO** (Bulma, 2026-05-04)
- confirmar `BookingUseCase.create()`
- confirmar `find_overlapping()`
- confirmar qué campos actuales se reutilizan
- entregar nota breve a Misato

### B1 — Migración de políticas + booking extensions
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ `uq_bookings_idempotency` unicidad real
- ✅ `ck_policies_scope` blindaje de invariantes
- ✅ downgrade corregido

### B2 — PolicyResolver
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ DBPolicy alineado con migración 062 (nullable donde corresponde)
- ✅ `amenity_type` canónico en `core_amenities` + `_lookup_amenity_type()` directo
- ✅ Tests `tests/test_policy_resolver.py` (19 tests)

### B3 — Validaciones policy en BookingUseCase
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ `field_provenance` + `_scope_filter()` — sin contaminación entre tipos
- ✅ `approval_mode` semánticamente correcto (auto/amenity_requires_approval/admin_only)

### B4 — Availability rules
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ `cancel_window_hours` conectado a `cancel()`
- ✅ `_check_slot_compliance()` con enforcement real para CONTINUOUS y DISCRETE
- ✅ Tests `test_booking_policy_validator.py` (35/35)

### B5 — Concurrencia/idempotencia + base para waitlist
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ Named lock por amenity (GET_LOCK/RELEASE_LOCK)
- ✅ Idempotencia en Phase 0 (antes de lock)
- ✅ Tests `test_b5_concurrency.py` (10/10)
- ⚠️ FKs en waitlist (a `core_amenities`, `core_amenity_bookings`) quedan para B6

### B6 — Waitlist + promotion/reallocation
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ `promote()` crea booking solo en `auto_confirm`, no en `notify_and_confirm` ni `admin_review`
- ✅ `DISCRETE_WINDOWS` overlap → waitlist (no muerte por overlap)
- ⚠️ Tests para `notify_and_confirm`, `admin_review`, `confirm_entry()` por reforzar (no bloqueante)

### B7 — Reporting + usage history
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ `BOOKING_REJECTED` productor conectado en `booking_usecase.create()`
- ✅ Bug fix: `waitlist_mode = None` (disabled), no más forced default
- ✅ `waitlist_conversion_rate` filtra por `booking_date`, no `created_at`
- ✅ Tests: 16 passed (9 unit + 7 integration)
- ⚠️ Nota no bloqueante: `Query.get()` legacy en `waitlist_usecase.py` → migrar a `Session.get()`

---

## Estado final del Sprint 16

| Bloque | Estado |
|---|---|
| B0 — Levantamiento | ✅ APROBADO |
| B1 — Migración policies | ✅ APROBADO |
| B2 — PolicyResolver | ✅ APROBADO |
| B3 — Validaciones policy | ✅ APROBADO |
| B4 — Availability rules | ✅ APROBADO |
| B5 — Concurrencia/idempotencia | ✅ APROBADO |
| B6 — Waitlist + promotion | ✅ APROBADO |
| B7 — Reporting + audit | ✅ APROBADO |

### B2 — `PolicyResolver`
- resolver cascade/merge
- devolver `EffectiveAmenityPolicy`
- tests de precedencia

### B3 — Validaciones de policy
- límites por período
- reservas activas
- guest limit
- eligibility
- rejection audit

### B4 — Availability rules
- crear `core_amenity_availability_rules`
- soportar slot modes
- blocked dates / booking window / cancel window

### B5 — Concurrencia / idempotencia
- endurecer create booking
- chequeo final de capacidad
- idempotency key
- tests de retry

### B6 — Waitlist model
- crear `core_amenity_waitlist`
- lifecycle completo
- expiración / confirmación

### B7 — Priority engine
- `fifo`
- `less_usage_first`
- `equal_share`
- ventana de evaluación parametrizable

### B8 — Reporting y observabilidad
- usage logs
- allocation audit API
- métricas de rechazo / promoción / expiración

---

## 15. Criterio de cierre del módulo

El módulo de políticas de amenities no se considera cerrado hasta que:

- exista contrato único de `EffectiveAmenityPolicy`
- estén soportados ambos `slot_mode`
- exista `guest_count`
- exista waitlist con lifecycle completo
- exista trazabilidad de cada decisión crítica
- existan tests de integración suficientes
- Misato no tenga observaciones abiertas
- Lelouch valide que no hay acoplamiento arquitectónico roto

---

## 16. Veredicto final

El planning original de Misato tenía una base correcta, pero incompleta.  
Este documento lo reemplaza como **versión operativa oficial** del sprint 16.

### Dirección final

- sí al motor de políticas en 3 capas
- no a una tabla genérica sin tipado para todo
- no a meter waitlist antes de resolver availability y concurrencia
- sí a auditabilidad desde Fase 1
- sí a Bulma como ejecutora única por tarea activa
- sí a Misato como control de flujo
- sí a Lelouch como criterio arquitectónico prioritario

Con esto, el sistema deja de ser una idea vaga y pasa a ser una máquina de guerra razonable.

---

*Documento consolidado y corregido por Lelouch S sobre base de planning inicial de Misato K.*
