# ♟️ Plan de Corrección de Naming — `core_unitys` → `core_unities`

> Fecha: 2026-04-14
> Autor: Lelouch S
> Estado: 🟡 Propuesto — pendiente de ejecución
> Contexto: Mike Ross confirmó que la tabla debe llamarse **`core_unities`** y que la base de datos será recreada, por lo que **no se requiere migración de rename sobre datos existentes**.

---

## 1. Decisión arquitectónica

La forma correcta en inglés es:
- **unity** = unidad conceptual / armonía / motor gráfico en otros contextos
- **unit** = unidad física/operativa/inmobiliaria
- plural correcto: **units**

Sin embargo, el proyecto ya construyó su semántica de negocio alrededor de **unity** como entidad de dominio. Para evitar mezclar dos cambios al mismo tiempo, la corrección mínima pedida por negocio es:

- **tabla SQL**: `core_unities`
- **migraciones históricas**: corregidas para crear/usar `core_unities`
- **FKs y queries SQL**: corregidos a `core_unities`

### Decisión de alcance
En esta fase, el plan propone **alinear toda la arquitectura al nuevo nombre `core_unities`** también en:
- módulo Python
- clases de infraestructura
- documentación
- rutas API
- tests

Porque dejar:
- módulo `core_unitys`
- tabla `core_unities`

sería una incoherencia innecesaria.

---

## 2. Objetivo del cambio

Corregir el naming del módulo para que el sistema quede consistente en los cuatro frentes:

1. **Base de datos** → `core_unities`
2. **Arquitectura / DDD** → `core_unities/`
3. **API** → idealmente `/unities`
4. **Documentación / roadmap / tests** → referencias uniformes

Aprovechamos que la base será borrada para evitar una migración de rename sobre datos vivos.

---

## 3. Principio operativo clave

### NO hacer
- no crear una migración nueva solo para renombrar `core_unitys` a `core_unities`
- no mantener alias viejos indefinidamente
- no dejar mitad del sistema en `unitys` y mitad en `unities`

### SÍ hacer
- **editar las migraciones históricas** que crean o referencian la tabla
- **editar el código fuente** para que nazca ya correcto desde cero
- recrear la base con el nombre correcto

Eso evita deuda, parches y doble semántica.

---

## 4. Alcance exacto del cambio

## 4.1 Base de datos
Cambiar todas las referencias de tabla:
- `core_unitys` → `core_unities`

### Afecta
- `001_create_initial.py`
- `008_refactor_core_unitys.py` → debe pasar a operar sobre `core_unities`
- cualquier FK en migraciones futuras o correctivas
- consultas SQL crudas en repositorios (`count_active_units`, etc.)

### También revisar
- `users_residents.unity_id` sigue llamándose `unity_id` o se renombra a `unit_id`

**Recomendación arquitectónica:**
- dejar **`unity_id` temporalmente** si quieren minimizar ruptura inmediata
- pero el naming correcto final sería **`unit_id`** si de verdad van a limpiar inglés del dominio completo

Para no abrir otra guerra en este sprint, recomiendo:
- **tabla** → `core_unities`
- **FK column existente** → `unity_id` por ahora

Luego se decide si se hace limpieza total de `unity` → `unit`.

---

## 4.2 Código DDD / estructura de carpetas
Renombrar módulo completo:

- `src/library/dddpy/core_unitys/` → `src/library/dddpy/core_unities/`

Y dentro del módulo:
- `dbunitys.py` → `dbunities.py` o mejor `db_units.py`
- `unity_*` nombres de clase/archivo se pueden mantener temporalmente o corregirse por fases

### Recomendación pragmática
Para no mezclar naming de dominio con naming SQL en una sola batalla, hacer dos capas:

#### Fase A — obligatoria ahora
- carpeta módulo: `core_unities`
- imports: `library.dddpy.core_unities.*`
- modelo SQL: `__tablename__ = 'core_unities'`

#### Fase B — opcional posterior
Revisar si quieren renombrar también:
- `UnityEntity` → `UnitEntity`
- `UnityUseCase` → `UnitUseCase`
- `unity_id` → `unit_id`

**Mi recomendación:** no hacer Fase B ahora. Sería otro frente de guerra.

---

## 4.3 API
Si el objetivo es consistencia real, la ruta debería pasar de:
- `/unitys`

a:
- `/unities`

### Recomendación
- **nuevo path oficial:** `/unities`
- si no hay clientes productivos aún, eliminar `/unitys`
- si sí hay consumo temporal interno, se puede mantener alias corto por una sola fase

Dado que estás corrigiendo antes de consolidar producto, mi recomendación es:
- **corregir ya a `/unities`**
- no perpetuar `/unitys`

---

## 4.4 Documentación
Actualizar referencias en:
- `README.md`
- `docs/03-modules/models/core_unitys.md` → renombrar archivo
- `docs/07-roadmap/module-list.md`
- `docs/07-roadmap/module-roadmap.md`
- `docs/04-bulma/MODULES.md`
- `docs/06-competitor-analysis/*` si menciona el nombre del módulo
- task orders existentes (`core_unitys-task-order.md`)

### Regla
No debe quedar documentación mezclada con ambos nombres salvo una nota histórica breve.

---

## 4.5 Tests
Actualizar:
- `tests/test_core_unitys.py` → `tests/test_core_unities.py`
- fixtures/imports relacionados
- cualquier assert que verifique nombre de tabla, ruta o mensajes

---

## 5. Estrategia de base de datos (aprovechando reset)

Como Mike indicó que borrará las tablas de la DB:

### Estrategia correcta
1. corregir migraciones históricas en git
2. borrar DB / recrear esquema limpio
3. correr migraciones desde cero
4. verificar que la tabla creada sea `core_unities`
5. verificar que todos los FKs apunten a `core_unities`

### Ventaja
- no hay que escribir migración de rename
- no hay que mantener compatibilidad doble en la DB
- el historial del proyecto queda más limpio para instalaciones nuevas

### Riesgo controlado
Reescribir migraciones históricas es aceptable **solo porque no se va a preservar una base ya migrada**.

---

## 6. Lista exacta de cambios técnicos

## 6.1 Migraciones
### Cambiar en `001_create_initial.py`
- `core_unitys` → `core_unities`
- FK de `users_residents.unity_id` debe referenciar `core_unities.id`
- `op.drop_table('core_unitys')` → `op.drop_table('core_unities')`

### Cambiar en `008_refactor_core_unitys.py`
**Opciones:**

#### Opción recomendada
- renombrar archivo a algo como:
  - `008_refactor_core_unities.py`
- mantener mismo revision id si aún no quieren reescribir cadena completa
- cambiar todo el contenido para operar sobre `core_unities`

#### Opción más limpia
- renombrar archivo + revision id + docstrings para que ya nazca consistente

Como vas a resetear DB, **la opción más limpia es preferible**.

---

## 6.2 Repositorios / SQL crudo
Cambiar referencias SQL:
- `SELECT COUNT(*) FROM core_unitys ...` → `core_unities`
- cualquier `ALTER TABLE core_unitys` → `core_unities`
- cualquier metadata query sobre `TABLE_NAME = 'core_unitys'` → `core_unities`

Especial atención en:
- `core_buildings/infrastructure/building_query_repository.py`
- `core_unities` query/cmd repositories
- migraciones Alembic

---

## 6.3 Estructura de código
Renombrar al menos:
- `src/library/dddpy/core_unitys/` → `src/library/dddpy/core_unities/`
- `src/api/unitys/` → `src/api/unities/`
- imports en `main.py`
- factories, repositories, mappers, usecases, tests

---

## 6.4 Documentación y artefactos
Renombrar:
- `docs/03-modules/models/core_unitys.md` → `core_unities.md`
- `docs/07-roadmap/core_unitys-task-order.md` → `core_unities-task-order.md`
- menciones de texto en docs internas

---

## 7. Orden de ejecución recomendado

## Tarea 1 — Congelar naming objetivo
**Decisión oficial:**
- tabla: `core_unities`
- módulo: `core_unities`
- API: `/unities`
- docs/tests: `unities`

**Responsable:** Mike + Lelouch

---

## Tarea 2 — Reescribir migraciones históricas
Editar migraciones existentes para que creen y modifiquen `core_unities` desde cero.

**Responsable propuesto:** Bulma S
**Revisión:** Misato K

---

## Tarea 3 — Renombrar módulo DDD y rutas API
Cambiar carpetas, imports, routers y referencias internas.

**Responsable propuesto:** Bulma S
**Revisión:** Misato K

---

## Tarea 4 — Renombrar documentación
Actualizar toda referencia escrita en docs/README/task orders.

**Responsable propuesto:** Misato K
**Apoyo:** Bulma S

---

## Tarea 5 — Renombrar tests y fixtures
Asegurar que el paquete de pruebas refleje el naming nuevo.

**Responsable propuesto:** Bulma S
**Revisión:** Misato K

---

## Tarea 6 — Recrear DB y validar instalación limpia
Una vez corregido el código:
- borrar tablas
- correr migraciones desde cero
- validar schema final
- validar healthcheck y endpoints

**Responsable operativo:** Mike / entorno
**Verificación técnica:** Misato K + Bulma S

---

## Tarea 7 — Smoke test final de arquitectura
Validar:
- tabla real = `core_unities`
- `users_residents` referencia correcta
- `count_active_units()` consulta tabla correcta
- API responde por `/unities`
- no quedan imports o docs colgando con `unitys`

**Revisión arquitectónica final:** Lelouch S

---

## 8. Qué NO recomiendo hacer ahora

### No recomiendo en este mismo movimiento:
- renombrar toda la semántica de dominio `Unity*` → `Unit*`
- renombrar `unity_id` → `unit_id`
- renombrar `core_unittys_types` al mismo tiempo si eso abre otra cadena masiva

### Razón
Eso ya no sería un ajuste de tabla; sería una refactorización lingüística global del dominio. Se puede hacer, pero es otro sprint.

El objetivo inmediato es:
- corregir el nombre incorrecto más visible
- dejar DB y arquitectura consistentes
- evitar otra ola de bugs por ambición innecesaria

---

## 9. Riesgos

### Riesgo 1 — referencias rotas por imports
Al renombrar carpeta/módulo, muchos imports pueden romperse.

**Mitigación:**
- búsqueda global por `core_unitys`
- búsqueda global por `/unitys`
- búsqueda global por `core_unitys.md`

### Riesgo 2 — migración histórica mal alineada
Si se edita `001` pero no `008`, el tablero se rompe.

**Mitigación:**
- revisar todas las migraciones relacionadas antes de recrear DB

### Riesgo 3 — docs viejas contradiciendo código nuevo

**Mitigación:**
- no cerrar tarea hasta barrer docs y tests también

---

## 10. Criterios de aceptación

La corrección se considera completa cuando:

- no exista ninguna tabla `core_unitys` en DB nueva
- exista `core_unities`
- todas las FKs apunten a `core_unities`
- el módulo Python y rutas API usen naming consistente
- tests pasen
- healthcheck del módulo responda bien
- documentación no mezcle ambos nombres salvo una nota histórica puntual

---

## 11. Veredicto final

Sí: la corrección debe hacerse.

Dado que la DB será reiniciada, **la estrategia correcta no es migrar el rename, sino corregir el origen**:
- migraciones históricas
- código
- rutas
- docs
- tests

Eso evita cargar por meses una palabra mal escrita en el corazón del sistema.

En ajedrez esto es simple: si todavía puedes recolocar la pieza antes de fijar la apertura, lo haces ahora. Más tarde costará el doble.
