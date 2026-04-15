---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
  - core
---

# 🗄️ Tabla: core_units

## 📝 Descripción
Representa las unidades inmobiliarias individuales del sistema: departamentos, oficinas, tiendas, estacionamientos, depósitos u otras unidades operativas dentro de un edificio.

Es la pieza central del núcleo inmobiliario y reemplaza el naming anterior `core_unitys`/`core_unities`.

---

## 🏗️ Estructura propuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador estable externo |
| building_id | BIGINT | FK → [[core_buildings]] |
| unit_type_id | BIGINT | FK → `core_unit_types` o naming vigente del catálogo |
| code | VARCHAR(50) | Código operativo interno |
| number | VARCHAR(50) | Identidad visible de la unidad (101, A-12, PH-1) |
| name | VARCHAR(255) | Nombre opcional o alias de la unidad |
| description | TEXT | Descripción administrativa |
| private_area | DECIMAL(12,4) | Área privada |
| coefficient | DECIMAL(9,6) | Coeficiente de copropiedad/prorrateo |
| floor_number | INT | Piso numérico |
| floor_label | VARCHAR(30) | Etiqueta amigable del piso |
| occupancy_status | VARCHAR(30) | vacant / occupied / reserved / maintenance / blocked |
| status | VARCHAR(30) | active / inactive |
| created_at | DATETIME / TIMESTAMP | Fecha de creación |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización |
| deleted_at | DATETIME / TIMESTAMP | Soft delete |

---

## 🔗 Relaciones (Foreign Keys)
- **Depende de:** [[core_buildings]]
- **Tiene muchos:** [[core_unit_ownerships]]
- **Tiene muchos:** [[core_unit_occupancies]]

---

## 📋 Reglas de negocio
- una unidad pertenece a un único edificio
- `number` debe ser único dentro del edificio
- `occupancy_status` no reemplaza la ocupación histórica; solo resume estado actual
- la relación con personas no vive en esta tabla, sino en `core_unit_ownerships` y `core_unit_occupancies`

---

## ⚠️ Nota de transición
Toda referencia previa a:
- `core_unitys`
- `core_unities`

debe migrar al nombre final oficial:
- `core_units`
