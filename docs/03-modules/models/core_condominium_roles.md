---
type: db-table
system: condominios
status: active
tags:
  - database
  - table
  - core
  - roles
---

# 🗄️ Tabla: core_condominium_roles

## 📝 Descripción
Tabla de roles administrativos u operativos por condominio.

Responde a la pregunta: **¿qué puede administrar un usuario dentro de un condominio determinado?**

Esto separa permisos administrativos del concepto de residencia o propiedad.

---

## 🏗️ Estructura propuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador estable externo |
| condominium_id | BIGINT | FK → [[core_condominiums]] |
| user_id | BIGINT | FK → [[users]] |
| role | VARCHAR(40) | super_admin / condominium_admin / building_manager / security_staff / maintenance_staff / support_staff |
| status | VARCHAR(30) | active / inactive / historical |
| start_date | DATE | Inicio de vigencia |
| end_date | DATE | Fin de vigencia |
| created_at | DATETIME / TIMESTAMP | Fecha de creación |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización |
| deleted_at | DATETIME / TIMESTAMP | Soft delete |

---

## 🔗 Relaciones (Foreign Keys)
- **Depende de:** [[core_condominiums]], [[users]]

---

## 📋 Reglas de negocio
- un admin no necesita vivir en el condominio
- un usuario puede administrar múltiples condominios
- los permisos administrativos son contextuales, no globales
- esta tabla debe alimentar la interfaz administrativa y el RBAC por condominio
