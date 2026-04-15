---
type: db-table
system: condominios
status: deprecated
tags:
  - database
  - table
  - pivot
  - deprecated
deprecated: true
deprecated_since: 2026-04-15
deprecated_reason: >
  Mezcla identidad, propiedad, ocupación y contexto físico en una sola tabla.
  Reemplazada por core_unit_ownerships + core_unit_occupancies + core_condominium_roles.
  NO eliminar hasta validación con datos reales (fallback de emergencia).
remove_after_validation: true
---

# 🗄️ Tabla: users_residents

## 📝 Descripción
**Tabla deprecada a nivel de diseño.**

Originalmente intentaba modelar en una sola relación quién vive, quién es dueño y qué vínculo tiene un usuario con una unidad.

Ese enfoque ya no es suficiente para el dominio real del proyecto.

---

## ⚠️ Problema arquitectónico
La tabla mezclaba en una sola estructura:
- identidad del usuario
- propiedad patrimonial
- ocupación/residencia
- contexto físico redundante (`condominium_id`, `building_id`, `unity_id`)
- estados y tipos demasiado ambiguos

Eso rompe escalabilidad cuando un usuario puede:
- ser propietario de múltiples unidades
- vivir en una o varias unidades
- ser inquilino en otra unidad
- pertenecer a múltiples condominios
- administrar un condominio sin vivir allí

---

## ✅ Reemplazo oficial
No debe implementarse como solución final.

## ✅ Reemplazo oficial
Se reemplaza por estas tablas especializadas (Bloque C — implementadas 2026-04-15):
- [[core_unit_ownerships]] → propiedad/titularidad
- [[core_unit_occupancies]] → ocupación/uso
- [[core_condominium_roles]] → administración por condominio

Y la unidad base oficial pasa a ser:
- [[core_units]]

---

## 🚫 Estado
- **Estado funcional:** DEPRECADO — no usar en código nuevo
- **Tabla DB:** presente como fallback de emergencia hasta validación con datos reales
- **Eliminación física:** pendiente — se elimina cuando se valide que ownerships + occupancies + roles cubren el 100% de los flujos
- **Código Python:** NO existe módulo DDD para esta tabla
- **Migración de datos:** pendiente (si se requiere)