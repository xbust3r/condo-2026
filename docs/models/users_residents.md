---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
  - pivot
---

# 🗄️ Tabla: users_residents

## 📝 Descripción
Tabla pivote que asigna qué usuarios viven o son dueños de qué unidades, registrando su rol.

---

## 🏗️ Estructura

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| condominium_id | BIGINT | FK → [[core_condominiums]] |
| building_id | BIGINT | FK → [[core_buildings]] |
| unity_id | BIGINT | FK → [[core_unitys]] |
| type | VARCHAR(100) | Rol (Propietario, Inquilino, etc.) |
| status | VARCHAR(50) | Estado de la residencia (vigente, histórico) |
| user_id | BIGINT | FK → [[users]] |

---

## 🔗 Relaciones (Foreign Keys)
- **Depende de:** [[core_condominiums]], [[core_buildings]], [[core_unitys]], [[users]]