---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
---

# 🗄️ Tabla: users

## 📝 Descripción
Almacena la identidad base y las credenciales de autenticación de todos los usuarios del sistema.

No debe mezclar perfil humano, propiedad, ocupación ni permisos administrativos. Es la pieza central de identidad.

---

## 🏗️ Estructura propuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador único universal del usuario |
| email | VARCHAR(255) | Correo electrónico único |
| password_hash | VARCHAR(255) | Hash de contraseña |
| status | VARCHAR(50) | active / inactive / suspended / locked |
| email_verified_at | DATETIME / TIMESTAMP | Verificación de correo |
| last_login_at | DATETIME / TIMESTAMP | Último acceso |
| failed_login_attempts | INT | Intentos fallidos acumulados |
| locked_until | DATETIME / TIMESTAMP | Bloqueo temporal si aplica |
| created_at | DATETIME / TIMESTAMP | Fecha de creación del registro |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización |
| deleted_at | DATETIME / TIMESTAMP | Soft delete |

---

## 🔗 Relaciones (Foreign Keys)
- **Tiene uno:** `user_profiles`
- **Tiene muchos:** [[core_unit_ownerships]]
- **Tiene muchos:** [[core_unit_occupancies]]
- **Tiene muchos:** [[core_condominium_roles]]

---

## 📋 Reglas de negocio
- `email` debe ser unique y normalizado en minúscula
- no se guarda `password`, solo `password_hash`
- el perfil humano se separa de autenticación
- la relación con unidades o condominios se modela por contexto, no en esta tabla