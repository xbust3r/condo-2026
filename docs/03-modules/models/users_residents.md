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

Se reemplaza por estas tablas especializadas:
- [[core_unit_ownerships]] → propiedad/titularidad
- [[core_unit_occupancies]] → ocupación/uso
- [[core_condominium_roles]] → administración por condominio

Y la unidad base oficial pasa a ser:
- [[core_units]]

---

## 📋 Estado
- **Estado funcional:** deprecado
- **Estado documental:** mantener solo como referencia histórica de transición
- **Implementación nueva:** prohibido usar esta tabla como diseño objetivo