---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
---

# 🗄️ Tabla: core_condominiums

## 📝 Descripción
Almacena la información principal de los complejos o conjuntos residenciales.

---

## 🏗️ Estructura

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| name | VARCHAR(255) | Nombre del condominio |
| code | VARCHAR(50) | Código identificador |
| description | TEXT | Descripción o detalles adicionales |
| size | DECIMAL(10,2) | Tamaño o área total |
| percentage | DECIMAL(5,2) | Coeficiente de copropiedad total |

---

## 🔗 Relaciones (Foreign Keys)
- **Tiene muchos:** [[core_buildings]], [[users_residents]]