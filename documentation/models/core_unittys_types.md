---
type: db-table
system: condominios
status: active
tags:
  - database
  - catalog
---

# 🗄️ Tabla: core_unittys_types

## 📝 Descripción
Catálogo de los diferentes tipos de unidades inmobiliarias (ej. Apartamento, Penthouse, Local, Estacionamiento).

---

## 🏗️ Estructura

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| name | VARCHAR(255) | Nombre del tipo de unidad |
| code | VARCHAR(50) | Código interno |
| description | TEXT | Descripción detallada |

---

## 🔗 Relaciones (Foreign Keys)
- **Tiene muchos:** [[core_unitys]]