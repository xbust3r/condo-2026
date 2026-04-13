# Roadmap de Módulos — condo-py

> Objetivo: definir el orden correcto de implementación para que `condo-py` construya primero su núcleo de negocio y no tenga que rehacer relaciones, permisos o finanzas después.

---

## Principio rector

El orden correcto no es “hacer features bonitas primero”.

El orden correcto es:

1. **modelo estructural del condominio**
2. **identidad y relaciones humanas**
3. **cuentas, cargos y recibos**
4. **operación diaria del residente**
5. **gobernanza e integraciones**

Si inviertes ese orden, terminas parchando pagos sobre entidades mal modeladas. Eso siempre acaba mal.

---

## Fase 1 — Núcleo inmobiliario

### Prioridad máxima
1. `core_condominiums`
2. `core_buildings`
3. `core_buildings_types`
4. `core_unitys`
5. `core_unittys_types`

### Objetivo
Tener modelada la estructura física completa:
- condominio
- edificios/torres
- departamentos/unidades
- tipos de edificio
- tipos de unidad

### Regla de diseño
Antes de pasar a usuarios, cada unidad debe poder responder con claridad:
- a qué condominio pertenece
- a qué edificio pertenece
- qué tipo de unidad es
- cuál es su código/número interno
- cuál es su estado

### Resultado esperado
El sistema ya puede representar correctamente el mundo físico del negocio.

---

## Fase 2 — Identidad, acceso y ocupación

### Prioridad alta
6. `users`
7. `users_residents`
8. auth / RBAC

### Objetivo
Modelar quién vive, quién alquila, quién administra y quién puede entrar al sistema.

### Lo mínimo que debe existir aquí
- usuarios autenticables
- roles del sistema
- relación usuario ↔ unidad
- tipo de relación:
  - propietario
  - residente
  - inquilino
  - familiar
  - administrador
- fechas de vigencia de ocupación
- usuario principal por unidad cuando aplique

### Regla de diseño clave
No mezclar “usuario” con “residente”.

- **Usuario** = identidad del sistema
- **Residente/Inquilino/Propietario** = rol o relación de negocio

Eso evita caos cuando una persona:
- es propietaria pero no vive ahí,
- alquila una unidad,
- administra otra,
- o tiene acceso a más de un inmueble.

---

## Fase 3 — Cuentas, cargos y recibos

### Prioridad crítica
9. módulo de cuentas por cobrar
10. módulo de cargos/recibos
11. módulo de pagos
12. módulo de estado de cuenta / ledger

### Sí, tu intuición aquí es correcta
Después de estructura + usuarios, el siguiente gran bloque debe ser:
- **recibos de pago**
- **cuentas**
- **cargos**
- **historial de pagos**

Ese es el corazón del producto. Ahí empieza a vivir de verdad.

### Lo que este bloque debe soportar
- cuota mensual por unidad
- cargos extraordinarios
- mora/intereses
- descuentos o ajustes
- estado de cuenta por unidad
- recibo emitido
- pago registrado
- saldo pendiente
- historial contable básico

### Recomendación táctica
No empieces con “contabilidad completa”.
Empieza con **accounts receivable sólido**:
- qué se debe
- quién lo debe
- cuándo vence
- qué se pagó
- qué falta

### Resultado esperado
Con esto ya puedes operar el flujo más importante del condominio:
**unidad → obligación → recibo → pago → saldo**

---

## Fase 4 — Comunicación y operación básica

### Prioridad media-alta
13. anuncios/comunicados
14. notificaciones
15. documentos
16. tickets o incidencias

### Objetivo
Dar valor diario al residente y a la administración.

### Capacidades mínimas
- publicar comunicados
- enviar avisos de cobro
- adjuntar documentos
- consultar reglamentos/actas/archivos
- reportar incidencias o solicitudes

### Razón estratégica
Sin esto, el sistema cobra pero no acompaña la operación cotidiana.

---

## Fase 5 — Experiencia residente

### Prioridad media
17. portal de residentes
18. reservas de áreas comunes
19. visitas/invitados
20. paquetería

### Objetivo
Entrar al terreno donde productos como Condo Control se vuelven fuertes.

### Nota táctica
Esto no debe adelantarse a finanzas.
Es valioso, sí, pero no sustituye el núcleo operativo ni el flujo de cobranza.

---

## Fase 6 — Gobernanza y capa premium

### Prioridad posterior
21. actas y reuniones
22. votaciones digitales
23. auditoría avanzada
24. integraciones externas
25. dashboards y reporting ejecutivo

### Objetivo
Completar la propuesta competitiva para condominios más maduros o administradoras profesionales.

---

## Orden recomendado resumido

### Secuencia correcta
1. Condominios
2. Edificios
3. Tipos de edificio
4. Unidades/departamentos
5. Tipos de unidad
6. Usuarios
7. Residentes / inquilinos / relaciones de ocupación
8. Auth + roles
9. Cuentas por cobrar
10. Recibos / cargos
11. Pagos
12. Estado de cuenta
13. Comunicados / notificaciones / documentos
14. Incidencias / mantenimiento básico
15. Portal residente
16. Reservas / visitas / extras
17. Gobernanza / votaciones / reporting avanzado

---

## Qué no haría todavía

No metería aún:
- app móvil nativa
- IA
- microservicios
- contabilidad compleja tipo ERP
- integraciones bancarias profundas desde el día 1

Primero hay que dominar el tablero base.

---

## Primera propuesta de sprints

## Sprint 1
- cerrar `core_condominiums`
- implementar `core_buildings`
- implementar `core_buildings_types`

## Sprint 2
- implementar `core_unitys`
- implementar `core_unittys_types`
- validar relaciones y constraints

## Sprint 3
- implementar `users`
- implementar `users_residents`
- diseñar roles y permisos

## Sprint 4
- módulo de cuentas por cobrar
- cargos recurrentes
- recibos

## Sprint 5
- pagos
- estado de cuenta
- notificaciones de vencimiento

## Sprint 6
- documentos
- comunicados
- incidencias

---

## Veredicto final

Tu intuición va bien, pero con un ajuste importante:

> **sí**: primero estructura inmobiliaria  
> **sí**: después usuarios/residentes/inquilinos  
> **sí**: luego recibos, pagos y cuentas  
> **pero**: mete auth/roles junto al bloque de usuarios, no después

Ese es el orden correcto.

Si haces pagos antes de modelar bien unidades, ocupación y permisos, luego tendrás que reconstruir media base.

Y eso, estratégicamente, es regalar piezas.
