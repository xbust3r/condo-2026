# ♟️ Plan de Corrección de Naming — `core_unitys` / `core_unities` → `core_units`

> Fecha: 2026-04-15
> Autor: Lelouch S
> Estado: 🟡 Propuesto — pendiente de ejecución
> Contexto: el estándar final aprobado para el módulo inmobiliario base es **`core_units`**. Cualquier naming previo (`core_unitys`, `core_unities`) queda obsoleto.

---

## 1. Decisión arquitectónica oficial

El nombre correcto final del módulo, tabla, rutas y documentación es:
- **`core_units`**

No deben coexistir tres variantes del mismo concepto.

### Naming descartado
- `core_unitys` ❌
- `core_unities` ❌

### Naming final aprobado
- `core_units` ✅

---

## 2. Alcance del cambio

Se debe alinear en los cuatro frentes:
1. **Base de datos** → `core_units`
2. **Arquitectura / DDD** → `core_units/`
3. **API** → `/units`
4. **Documentación / roadmap / tests** → referencias uniformes

---

## 3. Criterio operativo

### NO hacer
- no mantener alias viejos indefinidamente
- no dejar mitad del sistema en `unities` y mitad en `units`
- no crear diseño nuevo sobre naming viejo

### SÍ hacer
- corregir migraciones históricas si la DB será recreada
- corregir código fuente, repositorios, imports y rutas
- corregir documentación y tests
- usar `unit_id` como FK final recomendado

---

## 4. Cambios exactos recomendados

### Base de datos
- `core_unitys` → `core_units`
- `core_unities` → `core_units`
- `unity_id` → `unit_id` (recomendado final)
- `unity_type_id` → `unit_type_id` (recomendado final)
- `core_unittys_types` → `core_unit_types` (recomendado final)

### Código
- `src/library/dddpy/core_unities/` → `src/library/dddpy/core_units/`
- clases, mappers, repositorios y use cases deben migrar de semántica `unity` a `unit`
- rutas: `/unities` → `/units`

### Documentación
- barrer todas las menciones de `core_unitys` y `core_unities`
- dejar solo una nota histórica de transición cuando aporte contexto

---

## 5. Orden recomendado

1. congelar naming oficial
2. corregir documentación
3. corregir migraciones/modelos
4. corregir módulo DDD
5. corregir API
6. corregir tests
7. recrear DB y validar instalación limpia

---

## 6. Riesgos a vigilar

- imports rotos por rename masivo
- FKs mezcladas (`unity_id` en unas tablas y `unit_id` en otras)
- docs contradictorias
- rutas antiguas expuestas sin necesidad

---

## 7. Veredicto

El sistema no debe seguir cargando un naming defectuoso en su corazón inmobiliario.

La jugada correcta es cerrar el tema ahora y dejar una sola verdad:
- `core_units`
- `core_unit_ownerships`
- `core_unit_occupancies`
- `core_condominium_roles`
