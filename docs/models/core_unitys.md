---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
---

# 🗄️ Tabla: core_unitys

## 📝 Descripción
Representa las unidades inmobiliarias individuales, como apartamentos, casas o locales comerciales.

---

## 🏗️ Estructura

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador único universal de la unidad |
| name | VARCHAR(255) | Nombre descriptivo de la unidad |
| code | VARCHAR(50) | Código de la unidad |
| description | TEXT | Notas adicionales |
| size | DECIMAL(10,2) | Área privada |
| percentage | DECIMAL(5,2) | Coeficiente de copropiedad individual |
| type | VARCHAR(100) | Categoría (residencial, comercial, etc.) |
| floor | INT | Piso o nivel donde se ubica |
| unit | VARCHAR(50) | Número de unidad (ej. Apto 101) |
| building_id | BIGINT | FK → [[core_buildings]] |
| unity_type_id | BIGINT | FK → [[core_unittys_types]] |
| created_at | DATETIME / TIMESTAMP | Fecha de creación del registro |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización del registro |

---

## 🔗 Relaciones (Foreign Keys)
- **Depende de:** [[core_buildings]], [[core_unittys_types]]
- **Tiene muchos:** [[users_residents]]