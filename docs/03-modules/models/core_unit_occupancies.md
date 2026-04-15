---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
  - core
  - occupancy
---

# 🗄️ Tabla: core_unit_occupancies

## 📝 Descripción
Tabla de relación de ocupación o uso entre usuarios y unidades.

Responde a la pregunta: **¿quién ocupa, usa o tiene autorización sobre una unidad y bajo qué condición?**

No modela propiedad. Para eso existe `core_unit_ownerships`.

---

## 🏗️ Estructura propuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador estable externo |
| unit_id | BIGINT | FK → [[core_units]] |
| user_id | BIGINT | FK → [[users]] |
| occupancy_type | VARCHAR(40) | resident_owner / tenant / family_member / office_user / occasional_user |
| status | VARCHAR(30) | active / inactive / historical / pending |
| start_date | DATE | Inicio de vigencia |
| end_date | DATE | Fin de vigencia |
| is_primary | BOOLEAN | Marca si es ocupación principal |
| authorized_by_user_id | BIGINT | FK opcional → [[users]] |
| notes | TEXT | Notas internas |
| created_at | DATETIME / TIMESTAMP | Fecha de creación |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización |
| deleted_at | DATETIME / TIMESTAMP | Soft delete |

---

## 🔗 Relaciones (Foreign Keys)
- **Depende de:** [[core_units]], [[users]]

---

## 📋 Reglas de negocio
- un inquilino puede ocupar una unidad sin ser propietario
- un familiar puede estar asociado sin ser propietario
- un propietario puede también aparecer como ocupante si vive ahí
- toda ocupación debe tener vigencia temporal
- el historial de ocupación debe preservarse para trazabilidad
