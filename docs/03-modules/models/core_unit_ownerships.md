---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
  - core
  - ownership
---

# 🗄️ Tabla: core_unit_ownerships

## 📝 Descripción
Tabla de relación patrimonial entre usuarios y unidades.

Responde a la pregunta: **¿quién es dueño de qué unidad y desde cuándo?**

No modela ocupación. No modela permisos administrativos. Solo titularidad.

---

## 🏗️ Estructura propuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador estable externo |
| unit_id | BIGINT | FK → [[core_units]] |
| user_id | BIGINT | FK → [[users]] |
| ownership_type | VARCHAR(30) | owner / co_owner |
| ownership_percentage | DECIMAL(5,2) | Porcentaje de propiedad |
| status | VARCHAR(30) | active / inactive / historical |
| start_date | DATE | Inicio de vigencia |
| end_date | DATE | Fin de vigencia |
| notes | TEXT | Notas internas |
| created_at | DATETIME / TIMESTAMP | Fecha de creación |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización |
| deleted_at | DATETIME / TIMESTAMP | Soft delete |

---

## 🔗 Relaciones (Foreign Keys)
- **Depende de:** [[core_units]], [[users]]

---

## 📋 Reglas de negocio
- un usuario puede tener N unidades
- una unidad puede tener 1 o N propietarios
- un propietario no necesariamente vive en la unidad
- la titularidad debe tener historial temporal
- si hay copropiedad, `ownership_percentage` debe permitir distribuir la participación
