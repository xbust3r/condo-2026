---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
---

# 🗄️ Tabla: core_buildings

## 📝 Descripción
Almacena la información de las torres, bloques o edificios que pertenecen a un condominio.

---

## 🏗️ Estructura

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador único universal del edificio |
| name | VARCHAR(255) | Nombre o letra de la torre/bloque |
| code | VARCHAR(50) | Código identificador |
| description | TEXT | Descripción física o notas |
| size | DECIMAL(10,2) | Área construida |
| percentage | DECIMAL(5,2) | Coeficiente de participación |
| type | VARCHAR(100) | Categoría del edificio |
| condominium_id | BIGINT | FK → [[core_condominiums]] |
| building_type_id | BIGINT | FK → [[core_buildings_types]] |
| created_at | DATETIME / TIMESTAMP | Fecha de creación del registro |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización del registro |

---

## 🔗 Relaciones (Foreign Keys)
- **Depende de:** [[core_condominiums]], [[core_buildings_types]]
- **Tiene muchos:** [[core_unitys]], [[users_residents]]