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
Almacena la información de todos los usuarios registrados en el sistema de condominios.

---

## 🏗️ Estructura

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| first_name | VARCHAR(255) | Nombre(s) del usuario |
| last_name | VARCHAR(255) | Apellido(s) del usuario |
| email | VARCHAR(255) | Correo electrónico |
| password | VARCHAR(255) | Contraseña (Hash) |
| doc_identity | VARCHAR(50) | Documento de identidad |
| phone | VARCHAR(20) | Teléfono de contacto |
| status | VARCHAR(50) | Estado (activo, inactivo, suspendido) |

---

## 🔗 Relaciones (Foreign Keys)
- **Tiene muchos:** [[users_residents]]