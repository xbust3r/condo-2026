# ♟️ Roadmap Detallado — Users, Ownership, Occupancy y Roles

> Fecha: 2026-04-15
> Autor: Lelouch S
> Estado: 🟡 Propuesto para ejecución
> Contexto: rediseño integral del módulo `users` y corrección de naming del núcleo inmobiliario para soportar propietarios, inquilinos, familiares, residentes y administradores en múltiples condominios.

---

## 1. Decisión arquitectónica oficial

### 1.1 Identidad única
El sistema debe manejar **una sola identidad base por persona**.

No se crearán tablas separadas de `admin_users` y `resident_users`.

La persona existe una sola vez en `users`.
Luego se relaciona por contexto con:
- propiedades que posee
- unidades que ocupa
- condominios que administra

### 1.2 Separación de responsabilidades
Se separan cuatro ejes que antes estaban mezclados:

1. **Identidad** → `users`
2. **Perfil humano** → `user_profiles`
3. **Titularidad / propiedad** → `core_unit_ownerships`
4. **Ocupación / uso** → `core_unit_occupancies`
5. **Administración / permisos por condominio** → `core_condominium_roles`

### 1.3 Naming oficial del núcleo
Se aprueba el cambio:
- `core_unitys` ❌
- `core_unities` ⚠️ transición intermedia ya descartada
- `core_units` ✅ nombre oficial final

Y, por consistencia del estándar `core_`, las nuevas tablas serán:
- `core_units`
- `core_unit_ownerships`
- `core_unit_occupancies`
- `core_condominium_roles`

### 1.4 Tabla a retirar
La tabla `users_residents` queda **deprecada a nivel de diseño**.
No debe implementarse como solución final.

Su responsabilidad será reemplazada por:
- `core_unit_ownerships`
- `core_unit_occupancies`

---

## 2. Problema de negocio que este rediseño resuelve

El negocio exige que un mismo usuario pueda:
- ser propietario de varias unidades
- vivir en una o varias unidades
- ser inquilino en una unidad que no le pertenece
- ser familiar autorizado en otra unidad
- pertenecer a varios condominios
- administrar uno o más condominios sin vivir en ellos

Por eso, un solo campo `type` en una tabla pivote simple no alcanza.

---

## 3. Modelo objetivo

## 3.1 `users`
Identidad y autenticación.

Campos mínimos:
- `id`
- `uuid`
- `email`
- `password_hash`
- `status`
- `email_verified_at`
- `last_login_at`
- `failed_login_attempts`
- `locked_until`
- `created_at`
- `updated_at`
- `deleted_at`

Reglas:
- `email` unique y normalizado en minúscula
- nunca guardar `password`, siempre `password_hash`
- `status` controlado por enum/catálogo

## 3.2 `user_profiles`
Perfil humano desacoplado de autenticación.

Campos mínimos:
- `user_id`
- `first_name`
- `last_name`
- `display_name`
- `phone`
- `document_type`
- `document_number`
- `avatar_url`
- `birth_date` opcional
- `created_at`
- `updated_at`

## 3.3 `core_units`
Unidad inmobiliaria física.

Campos mínimos:
- `id`
- `uuid`
- `building_id`
- `unit_type_id`
- `code`
- `number`
- `name`
- `description`
- `private_area`
- `coefficient`
- `floor_number`
- `floor_label`
- `occupancy_status`
- `status`
- `created_at`
- `updated_at`
- `deleted_at`

## 3.4 `core_unit_ownerships`
Relación patrimonial: quién es dueño de qué.

Campos mínimos:
- `id`
- `uuid`
- `unit_id`
- `user_id`
- `ownership_type` (`owner`, `co_owner`)
- `ownership_percentage`
- `status`
- `start_date`
- `end_date`
- `notes`
- `created_at`
- `updated_at`
- `deleted_at`

## 3.5 `core_unit_occupancies`
Relación de ocupación/uso de la unidad.

Campos mínimos:
- `id`
- `uuid`
- `unit_id`
- `user_id`
- `occupancy_type` (`resident_owner`, `tenant`, `family_member`, `office_user`, `occasional_user`)
- `status`
- `start_date`
- `end_date`
- `is_primary`
- `authorized_by_user_id` opcional
- `notes`
- `created_at`
- `updated_at`
- `deleted_at`

## 3.6 `core_condominium_roles`
Rol administrativo/operativo por condominio.

Campos mínimos:
- `id`
- `uuid`
- `condominium_id`
- `user_id`
- `role` (`super_admin`, `condominium_admin`, `building_manager`, `security_staff`, `maintenance_staff`, `support_staff`)
- `status`
- `start_date`
- `end_date`
- `created_at`
- `updated_at`
- `deleted_at`

---

## 4. Reglas de negocio que deben quedar explícitas

### Propiedad
- un usuario puede ser propietario de N unidades
- una unidad puede tener uno o varios propietarios
- un propietario no necesariamente ocupa la unidad
- un propietario puede vivir en una o varias de sus unidades

### Ocupación
- una unidad puede tener múltiples ocupantes según reglas del negocio
- un inquilino nunca implica propiedad
- un familiar puede estar autorizado sin ser propietario
- la ocupación debe tener vigencia temporal (`start_date`, `end_date`)

### Administración
- un admin puede no vivir en el condominio
- un admin puede administrar uno o varios condominios
- los permisos de administración deben depender del contexto del condominio

### Historial
- toda relación importante debe poder saber desde cuándo aplica y hasta cuándo aplicó
- el sistema debe responder quién era dueño/ocupante/admin en una fecha determinada

---

## 5. Fases de implementación

## Fase 1 — Definición y naming del core
### Objetivo
Cerrar naming oficial y limpiar el tablero antes de construir código.

### Tareas
1. oficializar `core_units` como reemplazo de `core_unitys`
2. documentar deprecación de `users_residents`
3. documentar nuevas tablas `core_unit_ownerships`, `core_unit_occupancies`, `core_condominium_roles`
4. alinear roadmap y lista de módulos

### Entregables
- documentación actualizada
- nombres oficiales aprobados
- alcance congelado

---

## Fase 2 — Modelo físico y migraciones
### Objetivo
Dejar la base lista para crecer sin deuda semántica.

### Tareas
1. cambiar tabla base `core_unitys` → `core_units`
2. revisar FKs que hoy dependan de `unity_id`
3. decidir naming de transición:
   - recomendado final: `unit_id`
   - tolerable temporal: `unity_id` si evita ruptura excesiva
4. diseñar migraciones de:
   - `users`
   - `user_profiles`
   - `core_unit_ownerships`
   - `core_unit_occupancies`
   - `core_condominium_roles`
5. definir índices, unique constraints y checks

### Entregables
- esquema SQL alineado al dominio real
- integridad referencial correcta
- constraints documentados

---

## Fase 3 — DDD modules y contratos
### Objetivo
Implementar los módulos siguiendo el estándar del proyecto.

### Módulos a crear o corregir
- `users`
- `user_profiles` (si se modela como módulo independiente; recomendado)
- `core_units`
- `core_unit_ownerships`
- `core_unit_occupancies`
- `core_condominium_roles`

### Tareas
1. domain entities
2. exceptions
3. repository contracts
4. SQLAlchemy models
5. mappers
6. cmd/query repositories
7. use cases
8. factories
9. response contracts uniformes

### Entregables
- módulos DDD consistentes
- mapeo limpio DB ↔ dominio
- reglas semánticas aisladas del framework

---

## Fase 4 — APIs y permisos
### Objetivo
Separar experiencia admin y experiencia usuario sin duplicar identidad.

### Tareas
1. exponer endpoints de administración por condominio
2. exponer endpoints de lectura para portal usuario
3. aplicar RBAC por contexto
4. permitir que un mismo usuario vea sus distintas unidades/condominios según contexto

### Entregables
- endpoints admin
- endpoints portal usuario
- acceso contextual correcto

---

## Fase 5 — Datos semilla y casos reales
### Objetivo
Validar que el modelo sirve en escenarios del negocio.

### Casos que deben pasar
1. propietario con varios departamentos y ninguna residencia activa
2. propietario que vive en una unidad y alquila otra
3. inquilino en una unidad sin propiedad
4. familiar autorizado sin propiedad
5. admin que no vive en el condominio
6. usuario con acceso a propiedades en múltiples condominios

### Entregables
- seeds de prueba
- validación funcional del modelo
- huecos detectados antes de producción

---

## 6. Orden recomendado de ejecución

1. corregir documentación y naming oficial
2. redefinir `core_units`
3. diseñar `users` y `user_profiles`
4. diseñar `core_unit_ownerships`
5. diseñar `core_unit_occupancies`
6. diseñar `core_condominium_roles`
7. eliminar `users_residents` del roadmap final
8. implementar permisos contextuales
9. validar con seeds y flujos reales

---

## 7. Asignación recomendada de trabajo

### Misato
Responsable de coordinación técnica y cierre de arquitectura.

Debe:
- convertir esta documentación en backlog ejecutable
- dividir tareas por módulo
- revisar naming y consistencia final
- validar que Bulma no mezcle ownership con occupancy
- recordar el estándar de etiquetado correcto al reportar o pedir apoyo

### Bulma
Responsable de ejecución técnica del cambio.

Debe:
- aterrizar migraciones y modelos
- aplicar el estándar DDD del proyecto
- mantener separados identidad, propiedad, ocupación y rol administrativo

---

## 8. Riesgos a evitar

- volver a meter todo en `users_residents`
- usar un solo campo `type` para relaciones distintas
- mezclar autenticación con perfil humano
- mezclar permisos administrativos con ocupación
- dejar `core_unitys` vivo en código nuevo
- dejar documentación contradiciendo los nombres finales

---

## 9. Veredicto final

La arquitectura correcta para este dominio no es:
- usuario = residente

La arquitectura correcta es:
- usuario = identidad
- ownership = propiedad
- occupancy = ocupación
- role = administración contextual

Ese es el movimiento que evita deuda técnica cuando el sistema empiece a manejar múltiples condominios, múltiples unidades y perfiles híbridos.
