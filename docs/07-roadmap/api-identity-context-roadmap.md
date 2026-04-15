# ♟️ Roadmap API — Auth, Users y Contexto de Negocio

> Fecha: 2026-04-15
> Autor: Lelouch S
> Estado: 🟡 Propuesto para ejecución
> Objetivo: cerrar la capa de APIs que aún falta sobre el rediseño de identidad, perfiles, ownership, occupancy y roles por condominio.

---

## 1. Veredicto de estado actual

El backend **ya tiene APIs estructurales** para el núcleo inmobiliario y las relaciones nuevas:
- `core_condominiums`
- `core_buildings`
- `core_buildings_types`
- `core_units`
- `core_unit_types`
- `core_unit_ownerships`
- `core_unit_occupancies`
- `core_condominium_roles`

Eso cubre CRUD base.

Lo que **todavía falta** para que el producto deje de ser solo estructura y se convierta en una API utilizable por frontend es:

1. **Auth / sesión**
2. **Users**
3. **User profiles**
4. **APIs agregadas de contexto**
5. **RBAC contextual aplicado en rutas**

---

## 2. Principio arquitectónico

No queremos un frontend obligado a armar el rompecabezas con 5 llamadas crudas por pantalla.

La capa API faltante debe resolver dos necesidades diferentes:

### Portal admin
- gestionar usuarios
- buscar por email/documento
- ver propiedades, ocupaciones y roles
- asignar ownerships/occupancies/roles
- operar por condominio

### Portal usuario
- iniciar sesión
- ver su perfil
- ver sus unidades
- ver en qué condominio está actuando
- entender si es propietario, ocupante o admin

---

## 3. Bloques de trabajo

## BLOQUE E — Auth API
### Objetivo
Dar entrada y control de sesión al sistema.

### Endpoints mínimos obligatorios
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`
- `POST /auth/verify-email`
- `POST /auth/resend-verification`
- `GET /auth/me`
- `GET /auth/health`

### Reglas
- `login` por email + password
- emitir access token + refresh token si el stack ya está listo
- no exponer detalles de si el email existe en flujos de recovery
- `me` debe devolver identidad base + contexto mínimo

### Entregables
- módulo `auth/` DDD o capa de use cases equivalente
- rutas FastAPI
- validación de credenciales
- esquema de tokens/sesión

### Responsable sugerido
- **Bulma:** implementación
- **Misato:** revisión de contrato y seguridad

---

## BLOQUE F — Users API
### Objetivo
Exponer la identidad base como recurso administrable.

### Endpoints mínimos obligatorios
- `POST /users`
- `GET /users`
- `GET /users/{id}`
- `GET /users/uuid/{uuid}`
- `PUT /users/{id}`
- `DELETE /users/{id}`
- `POST /users/{id}/restore`
- `POST /users/{id}/suspend`
- `POST /users/{id}/activate`
- `GET /users/health`

### Filtros mínimos en listado
- `email`
- `status`
- `document_number` (si se decide join con profile o índice denormalizado)
- `include_deleted`

### Reglas
- `email` unique y normalizado
- no exponer `password_hash`
- suspensión y activación deben ser explícitas
- `users_residents` no participa aquí

### Entregables
- rutas API
- schemas cmd/query
- filtros admin útiles
- response contracts consistentes

### Responsable sugerido
- **Bulma:** implementación
- **Misato:** definición final de filtros y shape de respuesta

---

## BLOQUE G — User Profiles API
### Objetivo
Separar el perfil humano de la autenticación y exponerlo como recurso claro.

### Endpoints mínimos obligatorios
- `POST /user-profiles`
- `GET /user-profiles/{user_id}`
- `PUT /user-profiles/{user_id}`
- `GET /user-profiles/health`

### Opcionales muy recomendados
- `GET /user-profiles/by-document`
- `GET /user-profiles/by-phone`

### Reglas
- documento dividido en `document_type` + `document_number`
- teléfono normalizado
- el perfil no debe duplicar credenciales

### Entregables
- módulo `user_profiles`
- rutas FastAPI
- validaciones de documento/teléfono

### Responsable sugerido
- **Bulma:** implementación
- **Misato:** validación de contrato y reglas de negocio

---

## BLOQUE H — APIs agregadas de contexto
### Objetivo
Dar al frontend endpoints de producto, no solo CRUDs técnicos.

### Endpoints mínimos obligatorios
- `GET /users/{id}/ownerships`
- `GET /users/{id}/occupancies`
- `GET /users/{id}/roles`
- `GET /users/{id}/contexts`
- `GET /me/contexts`
- `GET /units/{id}/summary`
- `GET /condominiums/{id}/admins`

### Qué debe devolver `/users/{id}/contexts`
Una respuesta agregada con:
- user
- profile
- condominiums relacionados
- units donde es owner
- units donde es occupant
- roles administrativos activos
- contexto actual si aplica

### Qué debe devolver `/me/contexts`
La misma idea, pero para el usuario autenticado.

### Qué debe devolver `/units/{id}/summary`
- unit
- building
- condominium
- owners activos
- occupancies activas
- occupancy_status actual

### Qué debe devolver `/condominiums/{id}/admins`
- usuarios con roles admin activos en ese condominio
- rol
- vigencia

### Reglas
- estas APIs son de consumo real de frontend
- deben evitar N+1 conceptual del lado del cliente
- son las APIs que convierten el modelo en producto

### Responsable sugerido
- **Bulma:** implementación técnica
- **Misato:** priorización y definición de shape final por pantalla

---

## BLOQUE I — RBAC contextual
### Objetivo
Aplicar permisos reales sobre las APIs, no solo guardar roles en tabla.

### Lo mínimo que debe existir
- dependencia/middleware para usuario autenticado
- resolución de roles por `core_condominium_roles`
- verificación por contexto de condominio
- separación de permisos admin vs usuario portal

### Reglas mínimas
- un rol global no reemplaza el rol contextual
- admin de condominio A no administra condominio B por accidente
- un usuario puede tener múltiples contextos válidos

### Endpoints o capacidades derivadas
- guard para rutas admin
- guard para lectura de contexto propio
- posible header/query de `current_condominium_id` o equivalente controlado

### Responsable sugerido
- **Misato:** definición de la matriz de permisos
- **Bulma:** implementación técnica de guards/dependencies

---

## 4. Orden correcto de ejecución

### Sprint API-1
**Bloque E — Auth**
- login
- me
- refresh
- logout
- verify/reset base

### Sprint API-2
**Bloque F — Users**
- CRUD base
- activate/suspend
- filtros admin

### Sprint API-3
**Bloque G — User Profiles**
- CRUD base de perfil
- búsqueda por documento/teléfono

### Sprint API-4
**Bloque H — Context APIs**
- `/users/{id}/contexts`
- `/me/contexts`
- `/units/{id}/summary`
- `/condominiums/{id}/admins`

### Sprint API-5
**Bloque I — RBAC contextual**
- guards
- matrix de permisos
- endurecimiento de rutas

---

## 5. Priorización dura

### Prioridad 1 — imprescindible
- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/refresh`
- `GET /users`
- `GET /users/{id}`
- `POST /users`
- `GET /user-profiles/{user_id}`
- `PUT /user-profiles/{user_id}`
- `GET /me/contexts`

### Prioridad 2 — producto usable
- suspend/activate users
- forgot/reset password
- verify/resend verification
- `/users/{id}/contexts`
- `/units/{id}/summary`
- `/condominiums/{id}/admins`

### Prioridad 3 — hardening
- RBAC contextual completo
- búsqueda por documento/teléfono
- validaciones y auditoría adicional

---

## 6. Reparto recomendado Misato vs Bulma

## Misato — coordinación y control del tablero
Debe hacerse cargo de:
1. congelar el contrato de cada endpoint antes de que Bulma codifique
2. definir shape de respuesta para admin portal y user portal
3. definir matriz RBAC contextual
4. revisar consistencia entre APIs nuevas y modelo de dominio
5. evitar que el frontend quede atado a CRUDs demasiado crudos

### Checklist de Misato
- ¿el endpoint resuelve un caso de uso real o solo expone tabla?
- ¿el contrato sirve al admin portal?
- ¿el contrato sirve al portal usuario?
- ¿el contexto de condominio está claro?
- ¿el permiso está resuelto por rol contextual y no global?

## Bulma — ejecución
Debe hacerse cargo de:
1. crear módulos/rutas faltantes
2. implementar schemas y use cases
3. aplicar shared response schemas
4. agregar health endpoints
5. asegurar imports limpios, sin circularidades ni rutas incoherentes
6. validar que todo responda en `7501`

### Checklist de Bulma
- no duplicar lógica entre `users` y `user_profiles`
- no exponer `password_hash`
- no usar `users_residents` para nuevas APIs
- no meter permisos admin como campo global del usuario
- no dejar endpoints sin filtros útiles
- no romper naming ya corregido (`units`, no `unities`)

---

## 7. Criterios de aceptación por bloque

### Auth
- login funciona
- `me` responde con identidad válida
- refresh funciona
- password reset no filtra existencia de usuarios

### Users
- CRUD operativo
- filtros útiles
- activación/suspensión explícita
- soft delete/restore consistentes

### Profiles
- perfil desacoplado de auth
- actualización correcta
- documento/teléfono validados

### Context APIs
- frontend puede renderizar dashboard sin 8 llamadas manuales
- ownership/occupancy/roles salen agregados correctamente

### RBAC
- rutas admin protegidas por contexto
- usuario sin rol no administra por accidente
- cambio de condominio no escala permisos indebidos

---

## 8. Riesgos a evitar

- construir `auth` sin pensar en `me/contexts`
- exponer CRUD de users sin endpoints agregados de producto
- mezclar perfil y autenticación otra vez
- usar rol global del usuario como permiso final
- dejar a frontend resolviendo toda la inteligencia de negocio
- revivir `users_residents` por comodidad

---

## 9. Siguiente movimiento recomendado

Si quieren avanzar sin desperdiciar piezas, la orden correcta es:

1. **Misato** define contrato de `auth/me` y `me/contexts`
2. **Bulma** implementa `auth` base
3. **Misato** congela contrato `users` + `user_profiles`
4. **Bulma** implementa esos dos módulos
5. **Ambas** cierran context APIs
6. **Al final** endurecen RBAC contextual

---

## 10. Veredicto final

El rediseño de tablas ya ganó la apertura.
Ahora falta convertir esa ventaja posicional en una API de producto real.

La jugada correcta no es crear 20 endpoints sueltos por reflejo.
La jugada correcta es cerrar primero:
- auth
- users
- profiles
- contexts
- RBAC

Si eso queda bien, el frontend avanza con tablero limpio.
Si queda mal, volverán a improvisar joins mentales en cada pantalla.

Y eso sería perder una partida ganada.
