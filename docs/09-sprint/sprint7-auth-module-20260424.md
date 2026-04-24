# Sprint 7 — `core_auth` DDD Authentication Module

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable arquitectura:** Lelouch vi Britannia
**Responsable implementación:** Bulma

---

## Estado Actual del Módulo

El módulo `core_auth` YA EXISTE en `/src/library/dddpy/auth/` con la siguiente estructura:

```
auth/
├── domain/
│   ├── auth_exception.py
│   ├── auth_session.py     ← entity sesión activa
│   ├── auth_token.py       ← TokenPair, AccessTokenPayload
│   └── user_identity.py    ← identidad con profile
├── infrastructure/
│   ├── auth_session_repository.py  ← gestión refresh tokens (SHA-256 hashed)
│   ├── auth_user_repository.py   ← verify password, token_version
│   ├── dbauth_session.py         ← SQLAlchemy model (auth_sessions table)
│   └── jwt_service.py            ← create/decode access tokens
├── usecase/
│   ├── auth_cmd_schema.py  ← LoginSchema, RefreshSchema, LogoutSchema
│   └── auth_usecase.py     ← login, refresh, logout, logout_all, me
└── api/auth/
    ├── auth_dependencies.py  ← get_current_user (JWT validation)
    ├── rbac_dependencies.py
    └── routes_auth.py
```

### Lo que YA está implementado ✅

| Capability | Status | Notas |
|---|---|---|
| Login email+password | ✅ | Constant-time dummy bcrypt para no-enumeración |
| JWT access token (15 min) | ✅ | HS256, con `token_version` en payload |
| Refresh token rotation | ✅ | UUID v4, hashed SHA-256 en DB, 7 días TTL |
| Logout (revoke session) | ✅ | Soft-delete de auth_session |
| `logout_all` + token_version | ✅ | Invalida TODOS los JWT activos |
| `get_current_user` dependency | ✅ | Valida token_version vs DB en cada request |
| Rate limiting / account lock | ✅ | 5 intentos → 30 min lock |
| `GET /auth/me` | ✅ | Identity con profile |
| `POST /auth/logout` | ✅ | |
| `POST /auth/refresh` | ✅ | |

### Lo que FALTA (brechas de integridad) 🔴

| Gap | Descripción | Impacto |
|---|---|---|
| **AUTH-01** — Sin `POST /auth/password/change` | Users no pueden cambiar su contraseña. `logout_all` existe pero sin flow de cambio de contraseña, un usuario comprometido no puede invalidar sesiones. | ALTO |
| **AUTH-02** — Sin `POST /auth/register` (self-signup) | No existe endpoint para registro público de usuarios. El sistema solo acepta usuarios creados internamente. | ALTO (si se quiere OAuth o onboarding público) |
| **AUTH-03** — Sin `POST /auth/password/reset` (olvidé mi contraseña) | No hay flujo de reset de contraseña (email con token). Dependiendo del modelo de negocio esto puede ser obligatorio. | MEDIO (si hay signup) |
| **AUTH-04** — Sin endpoint `POST /auth/logout-all` en routes | `AuthUseCase.logout_all()` existe pero `routes_auth.py` no expone `POST /auth/logout-all`. El usuario no tiene forma de invocar invalidación global. | ALTO |

---

## Análisis de Brechas

### AUTH-01 — `POST /auth/password/change`

**Descripción:** El flujo completo de cambio de contraseña requiere:
1. Autenticación (JWT válido)
2. Verificación de contraseña actual
3. Actualización de `password_hash` en `users`
4. Incremento de `token_version` (invalida todos los JWT activos)
5. Revocación de todas las `auth_sessions` del usuario

**Ubicación de implementación:**
- `AuthUseCase.change_password(user_id, old_password, new_password)`
- `AuthUserRepository.update_password(user_id, new_password_hash)` — necesita ser añadido
- `routes_auth.py`: `POST /auth/password/change` con body `{current_password, new_password}`

**Seguridad:**
- El cambio de contraseña debe invalidar todas las sesiones existentes (`logout_all` internally)
- `token_version` debe incrementarse para invalidar todos los JWT antes de su TTL (15 min)
- La nueva contraseña debe cumplir policy (mínimo 8 chars, no igual al email, no en dictionary común)

**Validaciones:**
- `old_password` debe verificarse contra el hash actual
- `new_password` no puede ser igual a `old_password`
- Policy de password strength

### AUTH-02 — `POST /auth/register` (self-signup)

**Descripción:** Registro público de usuarios. Dependiendo del modelo de negocio puede ser necesario o no. Si el onboarding es solo interno (admin crea usuarios), este endpoint no es prioritario.

**Si se implementa:**
- `RegistrationSchema`: `email`, `password`, `first_name`, `last_name`
- `AuthUseCase.register(schema)` → crea user + user_profile
- Envío de email de verificación (`email_verified_at` se setea en NULL inicialmente)
- Rate limiting: 1 registro por IP por hora

**Preliminar:** Esperar confirmación del equipo sobre si self-signup es requerido antes de implementarlo. Si no es necesario, descartar esta brecha y marcar AUTH-02 como N/A.

### AUTH-03 — `POST /auth/password/reset`

**Descripción:** Flujo "olvidé mi contraseña":
1. User pide reset con su email
2. Sistema genera token de reset (UUID,存入 DB con TTL 1 hora)
3. Email enviado con link contendo token
4. User hace POST con token + nueva contraseña

**Requiere:**
- Nueva tabla `auth_password_resets` (token_hash, user_id, expires_at)
- `AuthUseCase.request_password_reset(email)` → genera token, NO envía email (mock OK)
- `AuthUseCase.confirm_password_reset(token, new_password)` → valida token, actualiza password
- `routes_auth.py`: `POST /auth/password/reset/request` + `POST /auth/password/reset/confirm`

**Preliminar:** Depende de AUTH-02. Si no hay registro público, este flujo puede no ser prioritario. Confirmar con el equipo.

### AUTH-04 — `POST /auth/logout-all` en routes

**Descripción:** `routes_auth.py` no tiene el endpoint `POST /auth/logout-all`. El método `AuthUseCase.logout_all()` existe pero no es accesible por API.

**Fix:**
```python
@auth_routes.post("/logout-all")
@api_handler
def logout_all(user: UserIdentity = Depends(get_current_user)) -> dict:
    response = AuthUseCase().logout_all(user_id=user.id)
    return response.dict()
```

---

## Scope Definido para Sprint 7

### Must Have ( cerrar antes de Phase 4 )

- [ ] **AUTH-01** — `POST /auth/password/change` (con invalidación global de sesiones)
- [ ] **AUTH-04** — `POST /auth/logout-all` expuesto en routes

### Should Have (si hay tiempo )

- [ ] **AUTH-03** — `POST /auth/password/reset/request` + `/confirm` (sin envío de email real — mock OK)
- [ ] **AUTH-02** — Registro self-signup (solo si el modelo de negocio lo requiere — confirmar primero)

### Dependencias

- `AuthUseCase` necesita nuevo método `change_password()`
- `AuthUserRepository` necesita nuevo método `update_password()`
- Verificar que tabla `users` tenga columna `password_hash` (debe existir de migraciones previas)
- `routes_auth.py` necesita los nuevos endpoints

---

## Arquitectura Propuesta

```
routes_auth.py
├── POST /auth/login              ✅ (existing)
├── POST /auth/refresh             ✅ (existing)
├── POST /auth/logout             ✅ (existing)
├── POST /auth/logout-all         🆕 AUTH-04
├── POST /auth/password/change    🆕 AUTH-01
├── POST /auth/password/reset/request   🆕 AUTH-03 (should have)
├── POST /auth/password/reset/confirm    🆕 AUTH-03 (should have)
├── POST /auth/register           🆕 AUTH-02 (confirmar si aplica)
├── GET  /auth/me                 ✅ (existing)
└── GET  /auth/health             ✅ (existing)
```

---

## Asignación

| Task | Responsable |
|---|---|
| AUTH-01: `POST /auth/password/change` | Bulma |
| AUTH-04: `POST /auth/logout-all` en routes | Bulma |
| AUTH-03: password reset flow | Bulma (si hay tiempo) |
| AUTH-02: self-signup | **Esperar confirmación del equipo** antes de implementar |

---

## Siguiente Paso

Confirmar con el equipo si AUTH-02 (self-signup) aplica. Si no, Sprint 7 se cierra con AUTH-01 + AUTH-04 + AUTH-03 opcional y se puede avanzar a Phase 4.
