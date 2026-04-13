# ♟️ core_buildings — Orden de Trabajo y Control de Ejecución

> Fecha: 2026-04-13
> Autor: Lelouch S
> **ESTADO: ✅ CERRADO — 2026-04-13**
> Arquitecto: Lelouch S | Coordinator: Misato K | Dev: Bulma S
> Commits: 9 (c6d3f47 → 6bde035)
> Objetivo: dejar un tablero único para construir el módulo `core_buildings` con orden, criterios de revisión y flujo operativo entre Misato y Bulma.

---

## 1. Objetivo del módulo

Implementar `core_buildings` como módulo real de negocio, no solo como tabla inicial.

Debe quedar preparado para servir como base de:
- estructura física del condominio
- relación con unidades (`core_unitys`)
- segmentación operativa por edificio
- filtros administrativos
- futura expansión a cobranza, tickets, reportes y portal residente

---

## 2. Cambios obligatorios sobre el diseño actual

### 2.1 Eliminar redundancia de tipos
**Acción:** eliminar campo `type` de `core_buildings`.

**Motivo:**
`type` duplica la responsabilidad de `building_type_id` y abre la puerta a inconsistencias.

**Regla final:**
- El tipo de edificio se representa **solo** con `building_type_id`.

---

### 2.2 Corregir unicidad de `code`
**Acción:** eliminar `UNIQUE(code)` global.

**Reemplazo recomendado:**
- `UNIQUE(condominium_id, code)`

**Opcional recomendado:**
- `UNIQUE(condominium_id, name)`

**Motivo:**
El código del edificio debe ser único dentro del condominio, no a nivel global del sistema.

---

### 2.3 Mejorar precisión de negocio
**Acción:** reemplazar campos numéricos ambiguos.

**Cambios:**
- eliminar `size`
- eliminar `percentage`
- agregar:
  - `built_area DECIMAL(12,4)`
  - `common_area DECIMAL(12,4)`
  - `coefficient DECIMAL(9,6)`

**Motivo:**
- `size` mezcla significados distintos
- `percentage` queda corto para coeficientes reales
- se necesita precisión útil para operación y finanzas futuras

---

### 2.4 Agregar constraints
**Constraints mínimos recomendados:**
- `built_area >= 0`
- `common_area >= 0`
- `coefficient >= 0 AND coefficient <= 100`
- `floors_count >= 0`
- `basements_count >= 0`
- `sort_order >= 0`
- `units_planned >= 0`

**Motivo:**
La base no debe aceptar basura operativa.

---

### 2.5 Agregar índices operativos
**Índices mínimos:**
- índice por `condominium_id`
- índice por `building_type_id`
- índice por `status`
- índice compuesto por `(condominium_id, status)`

**Motivo:**
Mejorar filtros, listados y joins futuros.

---

### 2.6 Agregar borrado lógico
**Acción:** agregar `deleted_at`.

**Motivo:**
Mantener consistencia con `core_condominiums` y permitir soft delete/restauración.

---

## 3. Estructura final recomendada para `core_buildings`

| Campo | Tipo sugerido | Descripción |
|---|---|---|
| id | BIGINT | PK interna |
| uuid | CHAR(36) / UUID | Identificador estable externo |
| condominium_id | BIGINT | FK al condominio |
| building_type_id | BIGINT | FK al catálogo de tipo de edificio |
| code | VARCHAR(50) | Código operativo único dentro del condominio |
| name | VARCHAR(255) | Nombre visible del edificio |
| short_name | VARCHAR(50) | Alias corto para UI/reportes |
| description | TEXT | Descripción o notas administrativas |
| built_area | DECIMAL(12,4) | Área construida total del edificio |
| common_area | DECIMAL(12,4) | Área común asociada al edificio |
| coefficient | DECIMAL(9,6) | Coeficiente de participación del edificio |
| floors_count | INT | Cantidad de pisos sobre nivel |
| basements_count | INT | Cantidad de sótanos |
| units_planned | INT | Número de unidades esperadas/proyectadas |
| sort_order | INT | Orden visual/manual en listados |
| status | INT o ENUM | Estado operativo del edificio |
| created_at | DATETIME / TIMESTAMP | Fecha de creación |
| updated_at | DATETIME / TIMESTAMP | Fecha de actualización |
| deleted_at | DATETIME / TIMESTAMP NULL | Fecha de borrado lógico |

---

## 4. Explicación de los campos nuevos

### `short_name`
Alias breve del edificio.

**Para qué sirve:**
- interfaces compactas
- filtros rápidos
- dashboards
- vistas tipo Torre A / Torre B / Norte / Sur

---

### `built_area`
Área construida total del edificio.

**Para qué sirve:**
- reportes inmobiliarios
- métricas comparativas
- reglas futuras de distribución o análisis

---

### `common_area`
Área común asociada al edificio.

**Para qué sirve:**
- separar áreas comunes del área construida
- evitar ambigüedad del antiguo campo `size`

---

### `coefficient`
Coeficiente de participación del edificio dentro del condominio.

**Para qué sirve:**
- copropiedad
- prorrateos
- finanzas futuras
- cálculos más precisos que `percentage`

---

### `floors_count`
Cantidad de pisos del edificio.

**Para qué sirve:**
- estructura física
- validaciones futuras
- mantenimiento
- reporting operativo

---

### `basements_count`
Cantidad de sótanos.

**Para qué sirve:**
- estacionamientos
- depósitos
- accesos subterráneos
- soporte a reglas futuras

---

### `units_planned`
Número esperado o proyectado de unidades del edificio.

**Para qué sirve:**
- comparar planeado vs registrado
- control operativo
- validación de carga inicial

---

### `sort_order`
Orden manual de visualización del edificio.

**Para qué sirve:**
- definir el orden sin depender del `id`
- controlar UI y reportes

---

### `deleted_at`
Marca temporal de borrado lógico.

**Para qué sirve:**
- soft delete
- restauración
- auditoría
- evitar pérdida física inmediata

---

## 5. Reglas de negocio obligatorias

- No crear edificio sin `condominium_id` válido.
- No crear edificio con `building_type_id` inexistente o inactivo.
- No repetir `code` dentro del mismo condominio.
- No permitir valores negativos en áreas ni contadores.
- No permitir `coefficient` fuera de rango.
- Los listados deben excluir eliminados por defecto.
- Debe existir flujo de restore.
- Si un edificio tiene unidades activas, no permitir eliminación física.

---

## 6. Relación estratégica con análisis competitivo

El módulo `core_buildings` debe quedar listo para alimentar en el futuro:
- anuncios segmentados por edificio
- tickets e incidencias por torre
- ocupación por edificio
- dashboards por bloque
- operaciones por edificio
- agregación futura de cuentas o indicadores por torre

La idea no es solo guardar torres; la idea es construir una pieza reutilizable del núcleo operativo.

---

## 7. Lista oficial de tareas

## Tarea 1 — Ajustar migración Alembic de `core_buildings`
**Objetivo:**
- eliminar `type`
- reemplazar uniques
- agregar campos nuevos
- agregar constraints
- agregar índices
- agregar `deleted_at`

**Entregable:**
- migración consistente y alineada al diseño final

---

## Tarea 2 — Actualizar documentación `core_buildings.md`
**Objetivo:**
- reflejar estructura final aprobada
- describir campos
- describir relaciones
- documentar reglas de negocio

**Entregable:**
- documento técnico/funcional alineado con la DB real

---

## Tarea 3 — Crear capa de dominio
**Objetivo:**
- modelar entidad de negocio
- definir invariantes
- crear contratos de repositorio

**Entregable:**
- `entity`, `data`, `exception`, `success`, `repository`, `cmd_repository`, `query_repository`

---

## Tarea 4 — Crear capa de infraestructura
**Objetivo:**
- modelo DB
- mapper
- cmd repository
- query repository

**Entregable:**
- persistencia funcional alineada con la migración

---

## Tarea 5 — Crear schemas y use cases
**Objetivo:**
- create
- update
- delete
- restore
- get/list/filter

**Entregable:**
- `cmd_schema`, `cmd_usecase`, `query_usecase`, `usecase`, `factory`

---

## Tarea 6 — Exponer rutas API
**Objetivo:**
- rutas REST consistentes con `core_condominiums`
- filtros por `condominium_id`, `status`, `building_type_id`, `include_deleted`
- endpoint de restore

**Entregable:**
- archivo de rutas listo para montarse en la app

---

## Tarea 7 — Registrar módulo en `main.py`
**Objetivo:**
- incluir router
- dejar visible el módulo en la API principal

**Entregable:**
- módulo registrado y operativo

---

## Tarea 8 — Crear tests mínimos
**Objetivo:**
- crear edificio
- validar duplicado de `code` por condominio
- validar soft delete
- validar restore
- validar filtros

**Entregable:**
- cobertura mínima funcional del módulo

---

## Tarea 9 — Preparar catálogo base de `core_buildings_types`
**Objetivo:**
- registrar tipos base:
  - residencial
  - comercial
  - mixto
  - servicios

**Entregable:**
- seed/base catalog listo para usarse

---

## Tarea 10 — Revisión final funcional y arquitectónica
**Objetivo:**
- validar consistencia DDD
- validar naming
- validar integración con `core_unitys`
- validar readiness para siguientes módulos

**Entregable:**
- aprobación final del módulo

---

## 8. Orden obligatorio de ejecución

1. migración
2. documentación
3. dominio
4. infraestructura
5. use cases
6. rutas API
7. montaje en app
8. tests
9. seed catálogo
10. revisión final

No saltar tareas. No abrir la siguiente sin cerrar la actual.

---

## 9. Flujo operativo entre Misato y Bulma

### Regla de coordinación
- **Misato** controla el tablero.
- **Bulma** ejecuta la tarea activa.
- Solo se etiqueta a quien sigue en el turno.

### Ciclo obligatorio
1. Misato etiqueta a Bulma con **una sola tarea activa**.
2. Bulma desarrolla y responde etiquetando **solo a Misato**.
3. Misato revisa.
4. Si hay errores, Misato devuelve la tarea a Bulma.
5. Si no hay observaciones, Misato habilita la siguiente tarea.
6. Repetir hasta cerrar el módulo.

### Regla crítica
No avanzar a la siguiente tarea mientras la actual tenga observaciones abiertas.

---

## 10. Criterio final de cierre

El módulo `core_buildings` se considera cerrado solo cuando:
- la migración esté correcta
- la documentación esté alineada
- el dominio exista
- la infraestructura exista
- los use cases estén funcionales
- las rutas estén expuestas
- el módulo esté montado en `main.py`
- existan tests mínimos
- exista catálogo base
- Misato no tenga observaciones pendientes

---

## Dictamen final

Este documento es el tablero oficial de ejecución de `core_buildings`.

No improvisen jugadas fuera de orden.
Primero estructura. Luego validación. Luego módulo real.
Así se gana la partida.
