# ♟️ Roadmap de Corrección — Auth Hardening + Naming Cleanup

> Fecha: 2026-04-15
> Autor: Lelouch S
> Estado: 🟡 Propuesto para ejecución inmediata
> Objetivo: endurecer el módulo `auth` recién implementado para que deje de ser solo funcional y pase a ser seguro, consistente y listo para escalar.

---

## 1. Diagnóstico ejecutivo

El módulo `auth` ya funciona, pero todavía presenta debilidades de diseño que lo dejan expuesto.

### Estado actual
- login funcional
- refresh token rotation funcional
- logout y logout-all funcionales a nivel refresh session
- `/auth/me` funcional
- sesiones persistidas en `auth_sessions`

### Problema central
Hoy el sistema revoca sesiones en DB, pero el **access token JWT puede seguir siendo válido hasta expirar**.

Eso significa que una sesión “cerrada” o una cuenta suspendida puede seguir entrando por una ventana de tiempo no deseada.

---

## 2. Objetivos del frente

1. eliminar fallas críticas de seguridad
2. endurecer el flujo de sesión
3. aplicar control contextual real al usuario autenticado
4. alinear naming del módulo con el estándar final del dominio
5. dejar base sana para RBAC contextual posterior

---

## 3. Problemas detectados

## 3.1 Secret JWT inseguro por defecto
### Hallazgo
`jwt_service.py` usa un fallback como:
- `dev-secret-change-in-production`

### Riesgo
Si la variable de entorno falta o está mal cargada, el backend firma tokens con una clave predecible.

### Corrección obligatoria
- eliminar fallback inseguro
- requerir env obligatorio
- fallar al boot si no existe secret válido
- idealmente separar:
  - `JWT_ACCESS_SECRET`
  - `JWT_REFRESH_SECRET` si en el futuro refresh también migra a JWT

### Prioridad
🔴 Crítica

---

## 3.2 Revocación incompleta de sesión
### Hallazgo
`logout` y `logout-all` revocan refresh sessions, pero **no invalidan access tokens ya emitidos**.

### Riesgo
Un token emitido antes del logout puede seguir accediendo a rutas protegidas hasta su expiración.

### Corrección obligatoria
Elegir una de estas estrategias y aplicarla de forma consistente:

#### Opción recomendada
**`token_version` en `users`**
- agregar `token_version INT NOT NULL DEFAULT 0`
- incluir `token_version` en el JWT access token
- en `get_current_user()` validar que el token version del JWT coincida con DB
- en `logout-all`, suspensión, reset de password o compromise → incrementar `token_version`

#### Opción alternativa
**`session_uuid` o `jti` por token**
- emitir access token con `jti` o `session_uuid`
- verificarlo contra DB en cada request protegida

### Recomendación final
Implementar **`token_version` primero**. Es más simple, claro y suficiente para esta fase.

### Prioridad
🔴 Crítica

---

## 3.3 `get_current_user()` no valida estado operativo del usuario
### Hallazgo
La dependencia de auth valida token y existencia del usuario, pero no endurece contra:
- `inactive`
- `suspended`
- `locked`
- usuario con `deleted_at`

### Riesgo
Un JWT válido puede seguir operando para una cuenta que ya no debería estar activa.

### Corrección obligatoria
En `get_current_user()`:
- cargar estado actual del usuario
- rechazar acceso si `status != active`
- rechazar acceso si `locked_until > now`
- rechazar acceso si `deleted_at IS NOT NULL`

### Prioridad
🔴 Crítica

---

## 3.4 Protección de timing incompleta en login
### Hallazgo
Cuando el usuario no existe, se ejecuta un dummy `sha256`; cuando sí existe, se hace verify de password real.

### Riesgo
Los tiempos no son equivalentes. Eso no evita de verdad la enumeración por timing.

### Corrección obligatoria
- usar un hash bcrypt dummy estático y verificar contra ese hash cuando el usuario no exista
- mantener el mismo flujo temporal de comparación

### Prioridad
🟠 Alta

---

## 3.5 Refresh rotation pierde metadata de sesión
### Hallazgo
Al rotar refresh token, la nueva sesión se crea sin conservar:
- `user_agent`
- `ip_address`

### Riesgo
Se pierde trazabilidad y capacidad de auditoría operacional.

### Corrección obligatoria
- al hacer refresh, copiar `user_agent` e `ip_address` de la sesión anterior
- opcional: actualizar `last_used_at` si luego agregan ese campo

### Prioridad
🟠 Alta

---

## 3.6 Acoplamiento excesivo entre auth y perfil humano
### Hallazgo
`AuthUserRepository` hace JOIN directo `users + user_profiles` para devolver identidad.

### Riesgo
Cambios de perfil pueden romper auth por una razón que no debería incumbirle.

### Corrección recomendada
Separar conceptualmente:
- `AuthPrincipal` o `AuthenticatedUser` → datos mínimos de autenticación
- `AuthMeView` o response assembler → composición users + profile para `/auth/me`

### Recomendación pragmática
No romper todo ahora.
Primero asegurar el módulo.
Luego refactorizar a:
- repositorio auth mínimo
- query/assembler específico para `/auth/me`

### Prioridad
🟡 Media

---

## 3.7 Naming inconsistente en documentos y perfil
### Hallazgo
En el proyecto se empujó el estándar:
- `document_type`
- `document_number`

Pero en `auth`/`profiles` aparecen variantes como:
- `doc_type`
- `doc_identity`

### Riesgo
- inconsistencia en APIs
- deuda técnica en frontend
- contract drift entre módulos
- migraciones futuras más dolorosas

### Corrección obligatoria de naming
Alinear al naming final:
- `doc_type` → `document_type`
- `doc_identity` → `document_number`

Y en respuestas JSON:
- no devolver `doc_identity`
- devolver `document_type`
- devolver `document_number`

### Recomendación adicional
Revisar si todavía queda naming viejo en:
- `users`
- `user_profiles`
- `auth`
- docs
- schemas Pydantic
- responses

### Prioridad
🟠 Alta

---

## 3.8 Integridad explícita de `auth_sessions`
### Hallazgo
El modelo SQLAlchemy no deja visible FK explícita en `user_id`.

### Riesgo
Si la migración no la puso correctamente, la integridad depende de la suerte.

### Corrección obligatoria
- validar migración real de `auth_sessions`
- asegurar FK a `users(id)`
- indexar correctamente `user_id`, `refresh_token_hash`, `deleted_at`, `expires_at`

### Prioridad
🟠 Alta

---

## 3.9 Tokens opacos de refresh mejorables
### Hallazgo
El refresh token actual usa UUID v4.

### Riesgo
No es un desastre, pero es menos robusto que un token opaco generado con `secrets`.

### Corrección recomendada
Migrar a:
- `secrets.token_urlsafe(48)` o similar

### Prioridad
🟡 Media

---

## 4. Orden exacto de ejecución

## Fase 1 — Seguridad crítica
1. eliminar secret JWT por defecto
2. validar estado actual del usuario en `get_current_user()`
3. implementar invalidación real de access tokens vía `token_version`

### Criterio de cierre
- el backend no inicia sin secret válido
- un usuario suspendido no puede acceder aunque tenga JWT vigente
- `logout-all` o suspensión invalidan access tokens previamente emitidos

---

## Fase 2 — Endurecimiento de sesión
4. corregir dummy bcrypt para timing uniforme
5. preservar `user_agent` e `ip_address` en refresh rotation
6. revisar integridad/FK de `auth_sessions`

### Criterio de cierre
- login tiene flujo temporal más homogéneo
- la trazabilidad de sesión se mantiene tras refresh
- `auth_sessions` queda íntegra y auditable

---

## Fase 3 — Cleanup semántico
7. corregir naming `doc_*` → `document_*`
8. alinear response de `/auth/me`
9. revisar docs y schemas para eliminar nombres viejos

### Shape objetivo de `/auth/me`
```json
{
  "success": true,
  "message": "Identity retrieved",
  "data": {
    "user": {
      "id": 1,
      "uuid": "...",
      "email": "user@example.com",
      "status": "active",
      "email_verified_at": null,
      "created_at": "..."
    },
    "profile": {
      "uuid": "...",
      "first_name": "...",
      "last_name": "...",
      "phone": "...",
      "document_type": "DNI",
      "document_number": "12345678"
    }
  }
}
```

### Criterio de cierre
- no quedan `doc_type` ni `doc_identity` expuestos públicamente
- contrato JSON consistente con el estándar final

---

## 5. Asignación recomendada

## Misato — coordinación y criterio
Debe encargarse de:
- congelar contrato final de `/auth/me`
- aprobar estrategia `token_version`
- validar matriz de estados que bloquean acceso
- revisar naming final `document_type` / `document_number`
- revisar que Bulma no meta una solución parche para invalidez de token

## Bulma — ejecución
Debe encargarse de:
- migración y campo `token_version`
- modificación de JWT payload + dependency
- endurecer `get_current_user()`
- corregir dummy timing check
- preservar metadata en refresh
- renombrar contratos/document fields inconsistentes

---

## 6. Checklist operativo para Bulma

### Seguridad
- [ ] eliminar fallback insecure de JWT secret
- [ ] agregar validación de secret al boot
- [ ] agregar `token_version` a `users`
- [ ] incluir `token_version` en access token
- [ ] validar `token_version` en `get_current_user()`
- [ ] invalidar tokens en `logout-all`, suspensión y eventos críticos

### Estado de usuario
- [ ] bloquear `inactive`
- [ ] bloquear `suspended`
- [ ] bloquear `locked_until > now`
- [ ] bloquear `deleted_at != null`

### Sesiones
- [ ] preservar `user_agent`
- [ ] preservar `ip_address`
- [ ] validar FK e índices de `auth_sessions`
- [ ] evaluar migración posterior a refresh token opaco con `secrets`

### Naming
- [ ] `doc_type` → `document_type`
- [ ] `doc_identity` → `document_number`
- [ ] actualizar repository queries
- [ ] actualizar `UserIdentity`
- [ ] actualizar `/auth/me`
- [ ] actualizar docs

---

## 7. Criterios de aceptación final

Este frente se considera cerrado cuando:
- una sesión revocada ya no conserva acceso operativo por JWT viejo
- una cuenta suspendida o bloqueada no entra aunque tenga token vigente
- el backend falla si no tiene secret correcto
- `/auth/me` devuelve naming consistente
- no quedan respuestas públicas con `doc_identity`
- la trazabilidad de sesión se mantiene tras refresh

---

## 8. Veredicto final

El módulo `auth` ya mueve piezas, pero todavía no protege bien al Rey.

La prioridad no es agregar más endpoints por reflejo.
La prioridad es **cerrar las brechas de seguridad y semántica** antes de seguir expandiendo el castillo.

Primero:
- secret seguro
- invalidación real
- validación de estado
- naming consistente

Luego sí, el resto del tablero.
