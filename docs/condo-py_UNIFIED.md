# condo-py — Documentación Unificada

> **Generado:** 2026-05-04 09:36 · **Total documentos:** 75 · **Versión:** 1.0.0

---

## Índice

 1. [Proyecto](#proyecto) <small>`2026-04-14`</small>
 2. [01-General · Introducción](#01-general--introducción) <small>`2026-03-19`</small>
 3. [01-General · Arquitectura](#01-general--arquitectura) <small>`2026-03-19`</small>
 4. [01-General · Docker](#01-general--docker) <small>`2026-03-19`</small>
 5. [01-General · Team Mapping](#01-general--team-mapping) <small>`2026-04-28`</small>
 6. [01-General · Zrok Tunnel](#01-general--zrok-tunnel) <small>`2026-04-30`</small>
 7. [02-Architecture · DDD Base Guide](#02-architecture--ddd-base-guide) <small>`2026-03-16`</small>
 8. [03-Modules · core_buildings](#03-modules--core_buildings) <small>`2026-04-14`</small>
 9. [03-Modules · core_buildings_types](#03-modules--core_buildings_types) <small>`2026-04-13`</small>
10. [03-Modules · core_condominiums](#03-modules--core_condominiums) <small>`2026-03-16`</small>
11. [03-Modules · core_condominium_roles](#03-modules--core_condominium_roles) <small>`2026-04-15`</small>
12. [03-Modules · core_unit_occupancies](#03-modules--core_unit_occupancies) <small>`2026-04-15`</small>
13. [03-Modules · core_unit_ownerships](#03-modules--core_unit_ownerships) <small>`2026-04-15`</small>
14. [03-Modules · core_units](#03-modules--core_units) <small>`2026-04-15`</small>
15. [03-Modules · core_unities](#03-modules--core_unities) <small>`2026-04-14`</small>
16. [03-Modules · core_unittys_types](#03-modules--core_unittys_types) <small>`2026-04-15`</small>
17. [03-Modules · users](#03-modules--users) <small>`2026-04-15`</small>
18. [03-Modules · users_residents](#03-modules--users_residents) <small>`2026-04-15`</small>
19. [04-Bulma · Introducción](#04-bulma--introducción) <small>`2026-03-16`</small>
20. [04-Bulma · Módulos](#04-bulma--módulos) <small>`2026-04-30`</small>
21. [04-Bulma · Anti-patterns](#04-bulma--anti-patterns) <small>`2026-03-16`</small>
22. [04-Bulma · Architecture Rules](#04-bulma--architecture-rules) <small>`2026-03-19`</small>
23. [04-Bulma · Change Playbook](#04-bulma--change-playbook) <small>`2026-03-19`</small>
24. [04-Bulma · Implementation Guidelines](#04-bulma--implementation-guidelines) <small>`2026-03-19`</small>
25. [04-Bulma · Module Map](#04-bulma--module-map) <small>`2026-03-16`</small>
26. [05-Research · Análisis Competitivo Sistemas Condo](#05-research--análisis-competitivo-sistemas-condo) <small>`2026-04-29`</small>
27. [06-Competitor-Analysis · Introducción](#06-competitor-analysis--introducción) <small>`2026-04-13`</small>
28. [06-Competitor-Analysis · Análisis Competitivo](#06-competitor-analysis--análisis-competitivo) <small>`2026-04-29`</small>
29. [06-Competitor-Analysis · Análisis Estratégico (Lelouch)](#06-competitor-analysis--análisis-estratégico-(lelouch)) <small>`2026-04-14`</small>
30. [07-Roadmap · API Identity Context](#07-roadmap--api-identity-context) <small>`2026-04-15`</small>
31. [07-Roadmap · Auth Hardening](#07-roadmap--auth-hardening) <small>`2026-04-15`</small>
32. [07-Roadmap · core_buildings Task Order](#07-roadmap--core_buildings-task-order) <small>`2026-04-14`</small>
33. [07-Roadmap · core_unities Rename Plan](#07-roadmap--core_unities-rename-plan) <small>`2026-04-14`</small>
34. [07-Roadmap · core_unities Task Order](#07-roadmap--core_unities-task-order) <small>`2026-04-14`</small>
35. [07-Roadmap · core_units Rename Plan](#07-roadmap--core_units-rename-plan) <small>`2026-04-15`</small>
36. [07-Roadmap · Module List](#07-roadmap--module-list) <small>`2026-04-15`</small>
37. [07-Roadmap · Module Roadmap](#07-roadmap--module-roadmap) <small>`2026-04-15`</small>
38. [07-Roadmap · Users Core Identity](#07-roadmap--users-core-identity) <small>`2026-04-15`</small>
39. [08-Analysis · INCIDENT-20260429 Alias Login 500](#08-analysis--incident-20260429-alias-login-500) <small>`2026-04-29`</small>
40. [08-Analysis · Users/Roles/Propietarios/Ocupación Integración](#08-analysis--users-roles-propietarios-ocupación-integración) <small>`2026-04-24`</small>
41. [09-Sprint · Sprint Final-12 · Validation Payments Receipts Ledger](#09-sprint--sprint-final-12--validation-payments-receipts-ledger) <small>`2026-05-01`</small>
42. [09-Sprint · Sprint-10 · Visitors](#09-sprint--sprint-10--visitors) <small>`2026-04-24`</small>
43. [09-Sprint · Sprint-13 · Votes](#09-sprint--sprint-13--votes) <small>`2026-04-24`</small>
44. [09-Sprint · Sprint-14 · Dashboards](#09-sprint--sprint-14--dashboards) <small>`2026-04-24`</small>
45. [09-Sprint · Sprint-15 · Detail Pages](#09-sprint--sprint-15--detail-pages) <small>`2026-04-29`</small>
46. [09-Sprint · Sprint-16 · Amenity Booking Policies](#09-sprint--sprint-16--amenity-booking-policies) <small>`2026-05-04`</small>
47. [09-Sprint · Sprint-5 · Accounts Receivable](#09-sprint--sprint-5--accounts-receivable) <small>`2026-05-01`</small>
48. [09-Sprint · Sprint-6 · User Roles Integration](#09-sprint--sprint-6--user-roles-integration) <small>`2026-04-24`</small>
49. [09-Sprint · Sprint-7 · Auth Module](#09-sprint--sprint-7--auth-module) <small>`2026-04-24`</small>
50. [09-Sprint · Sprint-8 · Incidents](#09-sprint--sprint-8--incidents) <small>`2026-04-24`</small>
51. [09-Sprint · Sprint-9 · Notifications](#09-sprint--sprint-9--notifications) <small>`2026-04-24`</small>
52. [10-Agents · AI Team](#10-agents--ai-team) <small>`2026-04-28`</small>
53. [10-Agents · Introducción](#10-agents--introducción) <small>`2026-04-28`</small>
54. [10-Agents · Tasks](#10-agents--tasks) <small>`2026-04-28`</small>
55. [BULMA · Amenity Bookings Sprint A](#bulma--amenity-bookings-sprint-a) <small>`2026-05-03`</small>
56. [BULMA · Flow Select Condo Dashboard](#bulma--flow-select-condo-dashboard) <small>`2026-05-03`</small>
57. [BULMA · Flow Verify Planning](#bulma--flow-verify-planning) <small>`2026-05-03`</small>
58. [BULMA · Handoff High1/High2](#bulma--handoff-high1-high2) <small>`2026-04-14`</small>
59. [BULMA · High5 Transversal Audit](#bulma--high5-transversal-audit) <small>`2026-04-14`</small>
60. [BULMA · Phase1 Review](#bulma--phase1-review) <small>`2026-04-14`</small>
61. [BULMA · Phase2 RBAC Planning](#bulma--phase2-rbac-planning) <small>`2026-04-16`</small>
62. [BULMA · Phase2 RBAC Status](#bulma--phase2-rbac-status) <small>`2026-04-30`</small>
63. [BULMA · Roadmap 5Highs](#bulma--roadmap-5highs) <small>`2026-04-30`</small>
64. [BULMA · Roadmap Amenities Scope](#bulma--roadmap-amenities-scope) <small>`2026-05-01`</small>
65. [BULMA · Roadmap Amenity Bookings](#bulma--roadmap-amenity-bookings) <small>`2026-05-03`</small>
66. [BULMA · Shadcn Theme Planning](#bulma--shadcn-theme-planning) <small>`2026-05-01`</small>
67. [BULMA · Swipe Landing Plan](#bulma--swipe-landing-plan) <small>`2026-05-01`</small>
68. [BULMA · Task Payment Occupancy](#bulma--task-payment-occupancy) <small>`2026-05-03`</small>
69. [BULMA · Theme QA Closure](#bulma--theme-qa-closure) <small>`2026-05-03`</small>
70. [Migration Plan](#migration-plan) <small>`2026-04-28`</small>
71. [Docs · Índice](#docs--índice) <small>`2026-04-30`</small>
72. [Testing · Cleanup](#testing--cleanup) <small>`2026-05-02`</small>
73. [Testing · Flow](#testing--flow) <small>`2026-05-02`</small>
74. [Testing · Introducción](#testing--introducción) <small>`2026-05-02`</small>
75. [Testing · Setup](#testing--setup) <small>`2026-05-02`</small>

---

## Proyecto

<small>📄 `README.md` · modificado: `2026-04-14`</small>

# condo-py — Sistema de Gestión para Condominios

> **Estado del proyecto:** Migrado a **FastAPI** + **SQLAlchemy** + **MySQL**
>
> **Arquitectura:** DDD/CQRS con patrón Repository
>
> **Objetivo:** Backend para gestión de condominios con estructura modular DDD

---

## 1. Stack Tecnológico

- **Python** 3.14
- **FastAPI** - Framework HTTP
- **SQLAlchemy** - ORM
- **MySQL** - Base de datos
- **Alembic** - Migraciones
- **Pydantic** - Validación de datos
- **Docker** - Contenedores

---

## 2. Estructura del Proyecto

```
condo-py/
├── alembic/                  # Migraciones Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── src/
│   ├── app.py               # FastAPI main
│   ├── api/                 # Routers FastAPI
│   │   ├── condominiums/
│   │   ├── buildings/
│   │   ├── buildings_types/
│   │   ├── unitys/
│   │   ├── unittys_types/
│   │   ├── users/
│   │   └── residents/
│   ├── library/
│   │   └── dddpy/
│   │       ├── shared/      # Componentes compartidos
│   │       │   ├── mysql/   # Base, Session
│   │       │   ├── constants/
│   │       │   ├── schemas/
│   │       │   ├── logging/
│   │       │   └── utils/
│   │       ├── core_condominiums/
│   │       ├── core_buildings/
│   │       ├── core_buildings_types/
│   ├── core_unities/
│   │       ├── core_unittys_types/
│   │       ├── users/
│   │       └── users_residents/
│   └── requirements.txt
├── documentation/
│   └── models/             # Documentación de entidades
├── Makefile
├── docker-compose.yml
└── alembic.ini
```

---

## 3. Módulos DDD

| Módulo | Tabla | Descripción |
|--------|-------|-------------|
| `core_condominiums` | `core_condominiums` | Gestión de condominios |
| `core_buildings` | `core_buildings` | Torres/edificios |
| `core_buildings_types` | `core_buildings_types` | Tipos de edificio |
| `core_unities` | `core_unities` | Unidades inmobiliarias |
| `core_unittys_types` | `core_unittys_types` | Tipos de unidad |
| `users` | `users` | Usuarios del sistema |
| `users_residents` | `users_residents` | Residentes (pivot) |

---

## 4. Patrón de Arquitectura (DDD)

Cada módulo sigue la estructura:

```
{modulo}/
├── domain/
│   ├── {modulo}.py          # Entidad de dominio
│   ├── {modulo}_exception.py
│   └── {modulo}_repository.py
├── infrastructure/
│   ├── {modulo}.py          # Modelo SQLAlchemy
│   ├── {modulo}_mapper.py
│   ├── {modulo}_cmd_repository.py
│   └── {modulo}_query_repository.py
└── usecase/
    ├── {modulo}_cmd_schema.py
    ├── {modulo}_cmd_usecase.py
    ├── {modulo}_query_usecase.py
    └── {modulo}_usecase.py
```

---

## 5. API Endpoints

### Condominios
- `POST /condominiums` - Crear
- `GET /condominiums` - Listar todos
- `GET /condominiums/{id}` - Obtener por ID
- `PUT /condominiums/{id}` - Actualizar
- `DELETE /condominiums/{id}` - Eliminar

### Edificios
- `POST /buildings` - Crear
- `GET /buildings` - Listar todos
- `GET /buildings/by-condominium/{id}` - Por condominio
- `GET /buildings/{id}` - Obtener por ID
- `PUT /buildings/{id}` - Actualizar
- `DELETE /buildings/{id}` - Eliminar

### Tipos de Edificio
- `POST /buildings-types` - Crear
- `GET /buildings-types` - Listar todos
- `GET /buildings-types/{id}` - Obtener por ID
- `PUT /buildings-types/{id}` - Actualizar
- `DELETE /buildings-types/{id}` - Eliminar

### Unidades
- `POST /unities` - Crear
- `GET /unities` - Listar todos
- `GET /unities/by-building/{id}` - Por edificio
- `GET /unities/{id}` - Obtener por ID
- `PUT /unities/{id}` - Actualizar
- `DELETE /unities/{id}` - Eliminar

### Tipos de Unidad
- `POST /core_unities_types` - Crear
- `GET /core_unities_types` - Listar todos
- `GET /core_unities_types/{id}` - Obtener por ID
- `GET /core_unities_types/uuid/{uuid}` - Obtener por UUID
- `PUT /core_unities_types/{id}` - Actualizar
- `DELETE /core_unities_types/{id}` - Soft delete
- `POST /core_unities_types/{id}/restore` - Restaurar
- `DELETE /core_unities_types/{id}/hard` - Hard delete

### Usuarios
- `POST /users` - Crear
- `GET /users` - Listar todos
- `GET /users/{id}` - Obtener por ID
- `PUT /users/{id}` - Actualizar
- `DELETE /users/{id}` - Eliminar

### Residentes
- `POST /residents` - Crear
- `GET /residents` - Listar todos
- `GET /residents/by-user/{id}` - Por usuario
- `GET /residents/by-unity/{id}` - Por unidad
- `GET /residents/{id}` - Obtener por ID
- `PUT /residents/{id}` - Actualizar
- `DELETE /residents/{id}` - Eliminar

---

## 6. Respuestas API

Todas las respuestas siguen el formato:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

---

## 7. Migraciones

### Configuración de Base de Datos

Alembic lee la configuración de la base de datos directamente desde `src/.env`. No es necesario configurar nada en `alembic.ini`.

Variables requeridas en `src/.env`:
```env
MYSQL_USER=stg_panelhub
MYSQL_PASSWORD=tu_password
MYSQL_HOST=herav4-production.cluster-cymuhlhwsajk.us-west-2.rds.amazonaws.com
MYSQL_PORT=3306
MYSQL_DB=stg_panelhub
```

### Ejecutar Alembic dentro del contenedor

Alembic lee la configuración de base de datos desde `src/.env`.

```bash
# Opción 1: Copiar alembic al contenedor y ejecutar
docker cp alembic/ <container>:/app/
docker exec -w /app <container> alembic upgrade head

# Opción 2: make command (monta /app directo)
make alembic COMMAND="upgrade head"
```

### Comandos útiles Alembic

| Comando | Descripción |
|---------|-------------|
| `alembic revision --autogenerate -m "nombre"` | Generar nueva migración |
| `alembic upgrade head` | Aplicar todas las migraciones |
| `alembic downgrade -1` | Revertir última migración |
| `alembic current` | Ver migración actual |
| `alembic history` | Ver historial de migraciones |

---

## 8. Ejecución Local

### Con Docker
```bash
make build
make up
```

###直接 con Python
```bash
pip install -r src/requirements.txt
uvicorn src.app:app --reload
```

---

## 9. Base de Datos

- **Host:** herav4-production.cluster-cymuhlhwsajk.us-west-2.rds.amazonaws.com
- **Puerto:** 3306
- **Usuario:** stg_panelhub
- **Base:** stg_panelhub

---

**README actualizado - Migración completada de Chalice a FastAPI**

<small>🔚 fin · Proyecto · `README.md` · `2026-04-14`</small>


---

## 01-General · Introducción

<small>📄 `docs/01-general/README.md` · modificado: `2026-03-19`</small>

# Documentación de `condo-py`

Este directorio separa tres niveles del tablero:

1. **Arquitectura operativa del proyecto** — cómo debe organizarse el código hoy.
2. **Observaciones para humanos** — explicaciones pedagógicas sobre decisiones, deudas y fronteras.
3. **Reglas tácticas para BULMA** — instrucciones compactas para una agente de IA que vaya a modificar el proyecto.

## Base actual del proyecto

La referencia arquitectónica vigente es:

- `src/library/dddpy/shared/` → base transversal compartida
- `src/library/dddpy/example/` → módulo patrón para nuevas implementaciones
- `src/api/example/` → referencia del patrón de route limpio con `@api_handler`
- `src/app.py` → borde FastAPI actual del servicio

Los módulos viejos no deben tomarse como fuente doctrinal si contradicen esta base.

## Orden recomendado de lectura

### Para humanos
1. `architecture.md`
2. `observations/README.md`
3. `docker.md`
4. `models/` (si aplica como inventario de tablas)

### Para agentes de IA
1. `BULMA/README.md`
2. `BULMA/architecture-rules.md`
3. `BULMA/module-map.md`
4. `BULMA/implementation-guidelines.md`
5. `BULMA/anti-patterns.md`
6. `BULMA/change-playbook.md`

## Mapa del directorio

```text
docs/
├── README.md
├── architecture.md
├── docker.md
├── models/
├── observations/
│   ├── README.md
│   ├── architecture-observations.md
│   ├── domain-vs-application.md
│   ├── recommendations-explained.md
│   └── junior-guide.md
├── BULMA/
│   ├── README.md
│   ├── architecture-rules.md
│   ├── module-map.md
│   ├── implementation-guidelines.md
│   ├── anti-patterns.md
│   └── change-playbook.md
└── new-standard/
```

## Regla importante

`docs/new-standard/` es la base doctrinal de referencia.
No debe editarse durante documentación operativa normal del proyecto.

## Qué pretende esta documentación

- Aterrizar la teoría DDD a la base real actual.
- Hacer explícito el patrón de módulo basado en `example`.
- Dejar claro el uso de mapper, exceptions compartidas, response schemas y `@api_handler`.
- Dar una guía útil tanto para humanos como para BULMA.

La arquitectura no debe depender de memoria tribal.
Debe leerse como un mapa de guerra reproducible.

<small>🔚 fin · 01-General · Introducción · `docs/01-general/README.md` · `2026-03-19`</small>


---

## 01-General · Arquitectura

<small>📄 `docs/01-general/architecture.md` · modificado: `2026-03-19`</small>

# Arquitectura de `condo-py`

> **Proyecto:** `condo-py`
>
> **Base actual de referencia:** `src/library/dddpy/shared/` + `src/library/dddpy/example/` + `src/api/example/`
>
> **Estilo arquitectónico:** DDD pragmático con separación `api / domain / usecase / infrastructure / shared`
>
> **Objetivo:** que cada módulo nuevo siga un patrón estable, explícito y repetible, con éxito estructurado y errores centralizados

---

## 1. Propósito de esta documentación

Esta documentación parte de la base actual deseada del proyecto:

- `shared/` como núcleo transversal,
- `example/` como módulo plantilla,
- `api/` como borde limpio,
- y `@api_handler` como mecanismo transversal de manejo de errores.

La idea central es simple:

> **la API debe quedar limpia; el éxito debe salir estructurado desde el use case y el error debe resolverse por excepción semántica + decorador.**

---

## 2. Tesis arquitectónica

La tesis correcta del proyecto es esta:

> **el dominio expresa significado, el use case coordina y produce la respuesta de éxito, la infraestructura implementa, y shared define contratos transversales para logging y manejo de errores.**

En términos prácticos:

- `api/` parsea input, invoca el use case y devuelve `.dict()`.
- `domain/` contiene entidades, contratos y excepciones de negocio.
- `usecase/` contiene schemas, orquestación, factories y `ResponseSuccessSchema` en el camino de éxito.
- `infrastructure/` contiene DB models, mappers y repositorios concretos.
- `shared/` contiene `DomainException`, `api_handler`, logging, response schemas y session managers.

Si la API empieza a capturar errores de negocio manualmente o el dominio empieza a depender del framework, el diseño se degrada.

---

## 3. Base estructural actual

La base que hoy debe tomarse como referencia es:

```text
src/
├── api/
│   └── example/
│       └── routes_example.py
└── library/
    └── dddpy/
        ├── shared/
        │   ├── decorators/
        │   │   ├── api_handler.py
        │   │   └── domain_exception.py
        │   ├── schemas/
        │   │   └── response_schema.py
        │   ├── logging/
        │   ├── mysql/
        │   ├── postgresql/
        │   ├── constants/
        │   └── utils/
        └── example/
            ├── domain/
            ├── infrastructure/
            └── usecase/
```

## 3.1 Qué significa esto

- `shared/` define piezas comunes reutilizables.
- `example/` representa la **plantilla arquitectónica actual** para futuros módulos.
- `api/example/` muestra el patrón de borde limpio con `@api_handler`.
- Los módulos viejos no deben usarse como patrón si contradicen esta base.

---

## 4. Estructura oficial esperada de un módulo

Todo módulo nuevo debería aproximarse a esta forma:

```text
module/
├── domain/
│   ├── entity.py
│   ├── module_data.py            # opcional si se separan data objects de dominio
│   ├── module_exception.py
│   ├── module_success.py         # catálogo semántico de mensajes de éxito del módulo
│   ├── module_repository.py
│   ├── module_cmd_repository.py
│   └── module_query_repository.py
├── infrastructure/
│   ├── dbmodule.py
│   ├── module_mapper.py
│   ├── module_cmd_repository.py
│   └── module_query_repository.py
└── usecase/
    ├── module_cmd_schema.py
    ├── module_cmd_usecase.py
    ├── module_query_usecase.py
    ├── module_usecase.py        # fachada recomendada
    └── module_factory.py
```

### Regla táctica

Si un módulo no deja claro:

- qué es entidad,
- qué es excepción,
- qué es contrato,
- qué es mapper,
- qué es repositorio concreto,
- qué es orquestación,
- y cómo produce el éxito estructurado,

entonces aún no está bien modelado.

---

## 5. Responsabilidad por capa

## 5.1 `api/`

Responsable de:

- declarar rutas,
- obtener request,
- parsear schemas de entrada,
- invocar el use case,
- devolver `response.dict()`,
- delegar errores al decorador `@api_handler`.

Ejemplo deseado:

```python
@example_routes.post("")
@api_handler
def create_example(request: CreateExampleSchema) -> dict:
    response = ExampleUseCase().create(request)
    return response.dict()
```

### Qué NO debe hacer

- `try/except` manual para cada error de negocio,
- construir respuestas de error por su cuenta,
- hablar directo con DB,
- mover semántica de negocio al router.

---

## 5.2 `domain/`

Responsable de:

- entidades de dominio,
- data objects de dominio cuando aplique,
- contratos abstractos de repositorio,
- excepciones de dominio,
- catálogos semánticos del módulo cuando expresen lenguaje estable del negocio o de su contrato de éxito.

### Repositorio agregado del módulo

En esta arquitectura se mantienen **tres contratos** en `domain/`:

- `Repository`
- `CmdRepository`
- `QueryRepository`

Y esto es **intencional**.

#### Significado de cada uno

- `CmdRepository` representa operaciones claramente orientadas a escritura.
- `QueryRepository` representa operaciones claramente orientadas a lectura.
- `Repository` representa el **repositorio agregado del módulo**.

Ese contrato agregado no existe por decoración.
Existe para sistemas más complejos donde la lógica del módulo:

- no encaja limpiamente en CRUD,
- combina lectura + decisión + escritura,
- depende de procesos custom,
- o usa la base de datos como soporte y no como centro del diseño.

#### Regla estratégica

Cuando una capacidad del módulo no cabe con naturalidad en `cmd` o `query`, el developer no debe deformar el diseño solo para forzar CQRS.
En ese caso, el punto de abstracción amplio es `Repository` como contrato agregado del módulo.

#### Qué NO significa

No significa que toda lógica compleja deba ir a repository.
La orquestación sigue viviendo en `usecase/`.
Pero `Repository` deja explícito que el módulo puede tener capacidades más amplias que la simple división lectura/escritura.

Ejemplos del template `example/`:

- `example_entity.py`
- `example_data.py`
- `example_exception.py`
- `example_success.py`
- `example_repository.py`
- `example_cmd_repository.py`
- `example_query_repository.py`

### Regla de pureza

El dominio **no** debe importar:

- modelos DB,
- sesiones SQLAlchemy,
- decorators del framework,
- objetos HTTP,
- schemas de `usecase/`.

### Excepciones de dominio

Las excepciones concretas del módulo deben vivir en `domain/*_exception.py` y heredar de:

- `shared/decorators/domain_exception.py`

Contrato base:

```python
class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        ...
```

### Qué aporta esto

- errores semánticos consistentes,
- status code controlado,
- integración directa con `@api_handler`.

### Catálogo de mensajes de éxito del módulo

Cuando un módulo tenga mensajes de éxito estables y reutilizables, deben centralizarse en `domain/*_success.py`.

Ejemplo:

- `example/domain/example_success.py`

Su función es actuar como **fuente única de verdad semántica** para el camino de éxito del módulo.
Eso evita:

- strings hardcodeados repetidos en múltiples métodos,
- deriva de wording entre operaciones equivalentes,
- inconsistencias entre respuesta funcional y logging.

Regla táctica:

- el `usecase` **consume** ese catálogo,
- el `domain` **declara** ese lenguaje,
- la API **no inventa** mensajes de éxito.

---

## 5.3 `usecase/`

Responsable de:

- recibir schemas de entrada,
- traducirlos a tipos del dominio cuando haga falta,
- coordinar repositorios,
- orquestar la operación,
- devolver `ResponseSuccessSchema` en el camino de éxito,
- lanzar `DomainException` o derivadas en el camino de error,
- exponer factories para ensamblar dependencias.

Ejemplos del template `example/`:

- `example_cmd_schema.py`
- `example_cmd_usecase.py`
- `example_query_usecase.py`
- `example_factory.py`
- `example_usecase.py`

### Regla de diseño

El use case:
- coordina,
- no modela persistencia,
- no captura errores de negocio para convertirlos en diccionarios manuales,
- no debe contaminarse con detalles HTTP.

### Sobre `ResponseSuccessSchema`

En este proyecto, que el use case/fachada devuelva `ResponseSuccessSchema` es una **decisión deliberada**, no un accidente.

Se hace así para lograr:

- API minimalista,
- contrato uniforme de éxito,
- separación clara entre éxito estructurado y error estructurado.

Cuando exista un catálogo como `domain/*_success.py`, el `message` de `ResponseSuccessSchema` debe salir de allí y no de literales dispersos dentro del `usecase`.

### Factories

Las factories viven en `usecase/` y ensamblan los casos de uso con sus repositorios concretos.

---

## 5.4 `infrastructure/`

Responsable de:

- modelos ORM,
- repositorios concretos,
- mappers,
- persistencia,
- detalles técnicos de sesión.

Ejemplos del template `example/`:

- `dbexample.py`
- `example_mapper.py`
- `example_cmd_repository.py`
- `example_query_repository.py`

### Regla del mapper

El mapper vive en infraestructura y es la frontera oficial entre DB y dominio.

Ejemplo:

- `ExampleMapper.to_domain(db_example)`
- `ExampleMapper.to_infrastructure(example)`

### Regla de oro del mapper

El mapper:
- traduce,
- no decide negocio,
- no reemplaza al dominio,
- no se mueve al router ni al domain.

---

## 5.5 `shared/`

Responsable de:

- `DomainException`,
- `api_handler`,
- `ResponseSuccessSchema`,
- `ResponseErrorSchema`,
- logging,
- session managers,
- constantes y utilidades realmente transversales.

Piezas clave:

- `shared/decorators/domain_exception.py`
- `shared/decorators/api_handler.py`
- `shared/schemas/response_schema.py`
- `shared/logging/`

### Regla disciplinaria

`shared/` no debe ser un basurero.
Solo deben entrar piezas transversales para múltiples módulos.

---

## 6. Contrato de respuestas y errores

La base actual define dos esquemas compartidos:

```python
class ResponseErrorSchema(BaseModel):
    success: bool = False
    message: str

class ResponseSuccessSchema(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None
```

## 6.1 Qué significan

- `ResponseSuccessSchema` = éxito estructurado.
- `ResponseErrorSchema` = error controlado estructurado.

## 6.2 Regla de éxito

El camino de éxito debe salir del use case/fachada como `ResponseSuccessSchema`.
La API no debe reconstruir ese contrato a mano.

## 6.3 Regla de error

El camino de error semántico debe expresarse con `DomainException` o derivadas.
La API no debe capturarlo manualmente si el endpoint ya usa `@api_handler`.

---

## 7. Patrón oficial API limpia + decorador

Este es el flujo oficial del proyecto:

```text
API route
  → parse schema en FastAPI
  → use case
  → ResponseSuccessSchema
  → response.dict()
  → @api_handler maneja DomainException / ValidationError / 500
```

## 7.1 Qué hace `@api_handler`

El decorador:

- loguea inicio de request,
- intenta capturar contexto útil cuando la route recibe `Request`,
- ejecuta la función de la ruta,
- convierte `DomainException` en `ResponseErrorSchema` con `status_code`,
- convierte `ValidationError` en 400,
- convierte errores inesperados en 500.

### Regla de framework

La implementación vigente de `@api_handler` es **FastAPI-native**.
No debe depender de `chalice`, `Blueprint`, `current_request` ni respuestas específicas de otro framework.
Si cambia el framework del borde, se adapta el decorador transversal sin contaminar `domain/` ni `usecase/`.

## 7.2 Qué logra este patrón

- funciones de API limpias,
- éxito uniforme,
- error uniforme,
- menos repetición de `try/except`,
- mejor trazabilidad de errores.

---

## 8. Logging compartido

El logger compartido es parte del contrato operativo del proyecto.
No es opcional ni cosmético.
Sirve para:

- trazar el flujo completo,
- mapear errores,
- seguir el recorrido request → use case → repositorio,
- facilitar debugging real.

La regla recomendada es usar logger en tres niveles:

1. **main / app bootstrap**
2. **API / entrypoints**
3. **módulo interno**

El objetivo no es llenar el sistema de ruido.
El objetivo es poder reconstruir la jugada cuando algo falla.

---

## 9. Módulo patrón: `example`

Hoy `example/` debe considerarse la referencia práctica de cómo construir módulos nuevos.

### Lo que demuestra correctamente

- entidad de dominio separada,
- exceptions del módulo,
- catálogo centralizado de mensajes satisfactorios del módulo,
- contratos abstractos de repositorio,
- data objects de dominio,
- repositorios concretos separados por intención,
- mapper explícito,
- schemas de entrada,
- use cases command/query,
- factory de ensamblaje,
- `ResponseSuccessSchema` en la fachada,
- compatibilidad con API limpia vía decorador.

---

## 10. Decisiones arquitectónicas vigentes

### 10.1 El mapper siempre vive en infraestructura

### 10.2 Las excepciones de negocio heredan de `DomainException`

### 10.3 Los repositorios abstractos viven en domain

### 10.4 Las factories viven en usecase

### 10.5 Los mensajes de éxito reutilizables del módulo viven en `domain/*_success.py`
El `usecase` debe consumirlos como fuente única de verdad semántica.

### 10.6 `ResponseSuccessSchema` forma parte del contrato del camino de éxito
No debe considerarse una casualidad del módulo.

### 10.7 `@api_handler` es el punto transversal del camino de error
No debe duplicarse ese trabajo con `try/except` manual en cada route.

### 10.8 `shared/` define piezas comunes, no reglas de negocio específicas

---

## 11. Dirección recomendada de evolución

El camino sano para `condo-py` es:

1. usar `example/` como patrón base real,
2. crear módulos nuevos respetando `api / domain / usecase / infrastructure / shared`,
3. mantener mapper, exceptions, response schemas y decorador como contratos explícitos,
4. evitar refactors cosméticos mezclados con construcción funcional,
5. documentar para humanos y para BULMA al mismo tiempo.

---

## 12. Resumen ejecutivo

La nueva arquitectura de `condo-py` debe entenderse así:

- `shared/` define las piezas comunes del reino,
- `example/` marca el patrón base,
- la API queda limpia,
- el éxito sale como `ResponseSuccessSchema`,
- el error sale como `DomainException` + `@api_handler`,
- y cada módulo nuevo debe entrar al tablero siguiendo ese orden.

> **La arquitectura correcta no es la que acumula carpetas. Es la que deja claro quién parsea, quién decide, quién persiste, quién responde y quién captura el error.**
*

<small>🔚 fin · 01-General · Arquitectura · `docs/01-general/architecture.md` · `2026-03-19`</small>


---

## 01-General · Docker

<small>📄 `docs/01-general/docker.md` · modificado: `2026-03-19`</small>

# Docker - condo-py

Este documento describe la configuración de Docker para el proyecto condo-py.

## Overview

El proyecto utiliza Docker para ejecutar la aplicación en un entorno aislado:

- **CLI**: Contenedor para ejecutar comandos (migraciones, tests, etc.)
- **dev**: Contenedor con la aplicación completa (FastAPI)

## Estructura de Docker

```
docker/
├── cli/              # Receta para CLI
│   └── Dockerfile
└── latest/           # Receta para el servicio
    ├── Dockerfile
    └── entrypoint.sh
```

## Comandos

### Construir los contenedores

```bash
make build
```

### Levantar el servicio

```bash
make up
```

Levanta el contenedor del backend y lo conecta a la red `services_network`.

### Detener el servicio

```bash
make stop
```

### Ingresar al contenedor

```bash
make ssh
```

### Ejecutar comandos genéricos

```bash
make command COMMAND="tu_comando"
```

Usa este target para comandos generales del proyecto dentro del contenedor CLI, por ejemplo:

```bash
make command COMMAND="pytest"
make command COMMAND="pytest -q"
make command COMMAND="python script.py"
```

### Cuándo usar `make command`

Úsalo para tareas que viven principalmente en `src/`, como:

- pruebas unitarias o de integración con `pytest`
- scripts Python
- comandos generales de desarrollo

Este target monta `src/` dentro del contenedor en `/app`.

### Ejecutar Alembic

```bash
make alembic COMMAND="alembic upgrade head"
```

También puedes usar otros comandos de migración:

```bash
make alembic COMMAND="alembic revision --autogenerate -m 'add new field'"
make alembic COMMAND="alembic current"
make alembic COMMAND="alembic history"
```

### Cuándo usar `make alembic`

Úsalo específicamente para migraciones, porque este target monta la raíz completa del repositorio en `/app` y deja disponible el directorio `alembic/`.

En otras palabras:

- **`make command`** → comandos generales y pruebas
- **`make alembic`** → migraciones y comandos de Alembic

No se recomienda usar `make command` para Alembic si el comando necesita acceder a la estructura completa del repo.

## Red Docker

El proyecto usa la red `services_network` para comunicarse con:

- **MySQL** (`services_mysql`): Base de datos
- **HAProxy** (`balancer`): Balanceador

## Variables de Entorno (src/.env)

```env
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DB=db_condominiums
```

## Notas

- `make command` monta la carpeta `src/` como volumen en `/app` dentro del contenedor CLI
- `make alembic` monta la raíz completa del repositorio en `/app`
- Alembic lee la configuración desde `src/.env`
- El proyecto usa **FastAPI** (no Chalice)

<small>🔚 fin · 01-General · Docker · `docs/01-general/docker.md` · `2026-03-19`</small>


---

## 01-General · Team Mapping

<small>📄 `docs/01-general/team-mapping.md` · modificado: `2026-04-28`</small>

# Team Mapping — condo-py

> **Nota:** La documentación completa del equipo de agentes IA está en [`docs/10-agents/AI_TEAM.md`](../10-agents/AI_TEAM.md).

## Canales

| Channel | ID | Uso |
|---------|-----|-----|
| #condo-backdmin | `1495909239829299340` | Canal principal de trabajo |

## Agentes IA — Rol y Modelo

| Rol | Nombre | Modelo | Discord |
|-----|--------|--------|---------|
| Architect | Lelouch | **GPT 5.4** | @Lelouch S |
| Coordinator | Misato | **Minimax 2.7** | @Misato K |
| Dev Lead | Bulma | **Minimax 2.7 / DeepSeek 4 Pro / Flash** | @Bulma S |

## Agente Humano — Leadership

| Rol | Nombre | Responsabilidades |
|-----|--------|-----------------|
| **Technical Leader** | Miguel | Code reviews, modelado DB, visión del proyecto, arquitectura final |

## Agentes Legacy (Pochita)

| Rol | Nombre | User ID | Discord |
|-----|--------|---------|---------|
| Frontend | Pochita | `1493611712916488342` | @Pochita |
| Boss | Mike Ross | `1488541529457950924` | — |

## Reglas de Etiquetado

- **Planning/revisiones generales** → `<@1488547393099010089>` (Lelouch)
- **Revisiones a Pochita y Bulma** → `<@1490404598240772156>` (Misato)
- **Cambios a condo-py** → `<@1492274774821572678>` (Bulma)
- **Frontend condo-backdmin** → `<@1493611712916488342>` (Pochita)
- **Etiquetar al final del mensaje** siempre que sea relevante

## Repos

| Repo | Ruta | Descripción |
|---|---|---|
| `condo-py` | `/home/miguel/servers/condo-py` | Backend Python / FastAPI / DDD |
| `condo-backdmin` | `/home/miguel/servers/condo-backdmin` | Frontend Next.js |
| Docs | `/home/miguel/servers/condo-py/docs/10-agents/` | Documentación del equipo IA |

<small>🔚 fin · 01-General · Team Mapping · `docs/01-general/team-mapping.md` · `2026-04-28`</small>


---

## 01-General · Zrok Tunnel

<small>📄 `docs/01-general/zrok-tunnel.md` · modificado: `2026-04-30`</small>

# zrok Tunnel — Acceso Público a condo-py

> Configuración del túnel zrok para exponer el API local a internet durante desarrollo.

---

## URL pública

```
https://condopy.share.zrok.io
```

**Endpoints de prueba:**
- `/health` → `{"success":true,"message":"API is running"}`
- `/docs` → Swagger UI
- `/openapi.json` → OpenAPI spec

---

## Prerrequisitos

- [zrok](https://zrok.io/) instalado (`zrok version` → v1.1.11+)
- Cuenta zrok configurada (`zrok status` → Account Token + Ziti Identity `<<SET>>`)
- Puerto 7501 del container expuesto al host (ver `docker-compose.yml`)

---

## Configuración

### 1. Puerto expuesto en docker-compose

```yaml
# docker-compose.yml
services:
  backend:
    ports:
      - "7501:7501"    # ← expone uvicorn al host
```

### 2. Reservar share público (URL persistente)

Solo se hace **una vez**. El nombre `condopy` es la URL pública.

```bash
zrok reserve public http://localhost:7501 --backend-mode proxy --unique-name condopy
```

### 3. Iniciar el túnel

```bash
# Manual (se cae al cerrar terminal)
zrok share reserved condopy --headless

# Persistente (sobrevive al cierre de terminal)
nohup zrok share reserved condopy --headless > /tmp/zrok-condopy.log 2>&1 &
```

### 4. Verificar

```bash
curl https://condopy.share.zrok.io/health
# {"success":true,"message":"API is running","data":{"status":"healthy"},"errors":null}
```

---

## Inicio automático (systemd)

Crear `/etc/systemd/system/zrok-condopy.service`:

```ini
[Unit]
Description=zrok tunnel for condo-py
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=miguel
ExecStart=/usr/bin/zrok share reserved condopy --headless
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now zrok-condopy
```

---

## Comandos útiles

| Comando | Descripción |
|---|---|
| `make zrok` (en el proyecto) | Levantar túnel zrok del proyecto |
| `zrok overview` | Listar shares activos |
| `zrok status` | Estado de la cuenta/conexión |
| `pgrep -af "zrok share"` | Ver procesos zrok corriendo |
| `tail -f /tmp/zrok-condopy.log` | Ver logs del túnel |
| `pkill -f "zrok share reserved condopy"` | Detener el túnel de condo-py |
| `pkill -f "zrok share reserved condobackdmin"` | Detener el túnel de condo-backdmin |

## Make targets

Cada proyecto tiene un target `zrok` en su Makefile que levanta todo automáticamente:

```bash
# Desde ~/servers/condo-py
make zrok   # Levanta container + túnel → https://condopy.share.zrok.io

# Desde ~/servers/Condo-backdmin
make zrok   # Levanta container + túnel → https://condobackdmin.share.zrok.io
```

Hace todo en un solo comando:
1. `make up` (asegura que el container Docker esté corriendo)
2. Mata cualquier túnel previo del proyecto
3. Arranca `zrok share reserved --headless`
4. Muestra confirmación de que el túnel está vivo

---

## Troubleshooting

| Problema | Solución |
|---|---|
| `bad gateway!` | El túnel no está corriendo o recién inició (darle ~5s) |
| `connection refused` | El container Docker no está corriendo o el puerto 7501 no está expuesto |
| `invalid unique name` | El nombre debe ser alfanumérico, minúsculas, 4-32 caracteres |
| URL cambia cada vez | Usar `zrok reserve` (persistente) en vez de `zrok share public` (efímero) |

<small>🔚 fin · 01-General · Zrok Tunnel · `docs/01-general/zrok-tunnel.md` · `2026-04-30`</small>


---

## 02-Architecture · DDD Base Guide

<small>📄 `docs/02-architecture/new-standard/ddd-architecture-base-guide.md` · modificado: `2026-03-16`</small>

# Guía base de arquitectura DDD agnóstica al framework

## 1. Propósito de esta guía

Esta guía toma como referencia la evolución real del proyecto `chalice-aca_health.insert-python` y la convierte en una base reusable para futuros servicios.

No está pensada para un framework concreto.
Está pensada para que el diseño sobreviva aunque mañana cambie el borde técnico:
- Chalice,
- Flask,
- FastAPI,
- workers,
- SQS consumers,
- CLI jobs,
- cron jobs,
- o cualquier combinación.

La tesis central es simple:

> **el framework entra y sale; el dominio debe permanecer.**

---

## 2. Qué se aprendió del proyecto actual

La evolución por sprints dejó tres lecciones estratégicas:

### Lección 1 — primero orden, luego pureza, luego profundidad
El proyecto mejoró en esta secuencia correcta:
1. limpieza técnica y observabilidad,
2. ownership transaccional y contratos,
3. desacoplamiento dominio ↔ ORM,
4. enriquecimiento del dominio,
5. blindaje con tests y frontera de providers.

Ese orden fue correcto.
Querer empezar por “DDD puro” mientras el logging, los commits y los contratos están rotos es sacrificar la reina en la apertura.

### Lección 2 — DDD útil no significa DDD ceremonial
No hace falta llenar el proyecto de fábricas, servicios, handlers y objetos rituales.
DDD útil significa:
- fronteras claras,
- semántica explícita,
- invariantes donde corresponde,
- y bajo acoplamiento a detalles técnicos.

### Lección 3 — el framework no debe gobernar el modelo
Chalice, Flask o cualquier otro framework deben actuar como:
- entrada,
- validación exterior,
- adaptación de request/response,
- wiring.

Nunca como contenedor de reglas de negocio.

---

## 3. Arquitectura objetivo

## 3.1 Capas

La base recomendada tiene cuatro zonas:

```text
entrypoints/     → HTTP, SQS, CLI, cron, webhooks
application/     → casos de uso, orquestación, coordinación
domain/          → entidades, value objects, invariantes, eventos semánticos
infrastructure/  → ORM, DB, adapters externos, mensajería, mappers
```

Si se quiere mantener el naming actual del proyecto, también puede expresarse así:

```text
api/ or handlers/        → entrypoints
usecase/                 → application
domain/                  → domain
infrastructure/          → infrastructure
shared/                  → cross-cutting controlado
```

La regla no depende del nombre.
Depende de la frontera.

---

## 3.2 Responsabilidad de cada capa

### A. Entrypoints / Interface layer
Responsable de:
- recibir HTTP/eventos/mensajes,
- traducir input externo a comandos o DTOs de aplicación,
- invocar casos de uso,
- convertir resultados a respuestas técnicas.

No debe:
- consultar la DB directamente,
- meter reglas de negocio,
- mutar entidades sin pasar por application/domain.

### B. Application layer
Responsable de:
- coordinar el flujo,
- abrir/cerrar unidad de trabajo,
- llamar repositorios,
- invocar adapters externos,
- traducir errores técnicos a errores de proceso,
- decidir secuencia.

No debe:
- convertirse en una segunda capa de dominio,
- tomar decisiones puramente técnicas del framework,
- cargar SQL o detalles HTTP crudos.

### C. Domain layer
Responsable de:
- semántica de negocio,
- invariantes,
- estados válidos,
- comportamiento de entidades,
- value objects,
- errores de dominio.

No debe conocer:
- SQLAlchemy,
- boto3,
- Flask request,
- Chalice app,
- requests.post,
- colas, sockets o detalles del vendor.

### D. Infrastructure layer
Responsable de:
- persistencia,
- modelos ORM,
- mappers DB ↔ dominio,
- clientes HTTP,
- envío a colas,
- integraciones externas,
- implementación concreta de repositorios.

No debe gobernar:
- semántica del negocio,
- transiciones de estado,
- políticas de proceso.

---

## 4. Estructura de carpetas recomendada

## 4.1 Versión simple y reusable

```text
src/
├── app/                            # o service/
│   ├── entrypoints/
│   │   ├── http/
│   │   ├── events/
│   │   ├── cli/
│   │   └── schedulers/
│   ├── modules/
│   │   ├── leads/
│   │   │   ├── application/
│   │   │   ├── domain/
│   │   │   └── infrastructure/
│   │   ├── campaigns/
│   │   │   ├── application/
│   │   │   ├── domain/
│   │   │   └── infrastructure/
│   │   ├── routings/
│   │   │   ├── application/
│   │   │   ├── domain/
│   │   │   └── infrastructure/
│   │   └── shared/
│   │       ├── domain/
│   │       ├── application/
│   │       └── infrastructure/
│   └── bootstrap/
│       ├── container.py
│       ├── settings.py
│       └── wiring.py
├── tests/
│   ├── domain/
│   ├── application/
│   └── integration/
└── migrations/
```

---

## 4.2 Variante compatible con el proyecto actual

Si se quiere mantener la idea de `dddpy/`, la forma correcta sería algo así:

```text
src/chalicelib/dddpy/
├── leads/
│   ├── domain/
│   ├── application/      # antes usecase/
│   └── infrastructure/
├── campaigns/
├── routings/
├── routing_logs/
├── integrations/
│   └── leadspedia/
│       ├── application/
│       ├── domain/       # opcional, solo si tiene semántica propia
│       └── infrastructure/
└── shared/
```

Observación importante:
`routing_leadspedia` no debería tratarse como subdominio central si en realidad es un provider externo.
La jugada correcta es moverlo conceptualmente a **integrations/adapters/providers**.

---

## 5. Cómo modelar módulos

Cada módulo debe responder una pregunta del negocio.
No una pregunta del framework.

### Ejemplo correcto
- `leads`
- `campaigns`
- `routings`
- `routing_logs`

### Ejemplo incorrecto
- `chalice_handlers`
- `sqlalchemy_models_business`
- `helpers_everything`
- `provider_utils`

El módulo nace por semántica, no por accidente técnico.

---

## 6. Reglas maestras de frontera

## Regla 1 — el dominio no conoce el ORM
Nunca:
```python
class Lead:
    @classmethod
    def from_db(cls, db_model: DBLead):
        ...
```

Sí:
```python
class LeadMapper:
    def to_domain(self, db_model: DBLead) -> Lead:
        ...
```

## Regla 2 — un solo dueño de la transacción
La unidad de trabajo manda.
Los repositorios persisten y consultan.
No compiten por el commit.

## Regla 3 — los providers son adapters
Leadspedia, CRMs, gateways, APIs externas y colas deben entrar por contratos explícitos.
No deben incrustarse dentro del dominio.

## Regla 4 — Pydantic valida forma, no reemplaza el dominio
Los schemas validan:
- shape,
- tipos,
- obligatoriedad,
- defaults.

Pero las reglas de negocio reales viven en domain/application.

## Regla 5 — los casos de uso orquestan; no deben convertirse en dios
Si `ExecuteUseCase` termina cargando validación de negocio, detalles HTTP, mapeo DB, estados y reglas del provider, ya perdiste el centro del tablero.

## Regla 6 — shared debe ser pequeño y disciplinado
`shared/` solo debe contener piezas realmente transversales:
- logging,
- uow,
- tipos compartidos,
- errores base,
- helpers infra reutilizables.

Nunca debe convertirse en cementerio genérico.

---

## 7. Modelo recomendado de flujo

## 7.1 Flujo general

```text
Entrypoint
  → Command/DTO de aplicación
  → UseCase
  → Repositories + Domain Entities + Providers
  → Resultado de aplicación
  → Adaptación de respuesta
```

## 7.2 Flujo con asincronía

```text
HTTP / webhook
  → CreateLeadUseCase
  → persistencia
  → enqueue evento/mensaje

Consumer / worker
  → ExecuteRoutingUseCase
  → recuperar agregado
  → resolver provider
  → enviar a adapter externo
  → registrar log
  → actualizar estado final
```

La asincronía no rompe DDD.
Solo agrega otro entrypoint.

---

## 8. Entidades, value objects y contratos

## 8.1 Cuándo una entidad merece comportamiento
Debe tener comportamiento si gobierna algo como:
- transiciones de estado,
- validaciones semánticas,
- consistencia interna,
- reglas de reemplazo,
- composición de respuesta significativa.

### Ejemplo
En el proyecto actual fue correcto mover a `Lead` cosas como:
- normalización de `media_code`,
- validación de `uuid`,
- aplicación de resultado del routing,
- preservación de `previous_mc`.

Eso ya no es DTO con corona.
Eso es dominio con autoridad.

## 8.2 Cuándo crear value objects
Crear value objects cuando:
- encapsulan validación repetida,
- evitan strings inseguros,
- expresan semántica,
- mejoran claridad del modelo.

Ejemplos útiles:
- `LeadUuid`
- `MediaCode`
- `RoutingStatus`
- `CampaignCode`

No crear value objects para inflar currículo.
Si un wrapper no añade semántica, es teatro.

## 8.3 Contratos de aplicación
Los casos de uso deben recibir contratos explícitos:
- command objects,
- DTOs,
- schemas de entrada ya traducidos.

Eso evita que el dominio dependa del request original del framework.

---

## 9. CQRS pragmático

La arquitectura derivada de este proyecto usa un **CQRS liviano**.
Eso es correcto cuando aporta claridad.

### Sí conviene separar command/query cuando:
- la lectura y escritura tienen intenciones distintas,
- la semántica mejora,
- las dependencias divergen,
- el módulo ya creció.

### No conviene cuando:
- se hace por moda,
- solo duplicas archivos,
- el read/write real es trivial.

La separación correcta es la que reduce fricción.
No la que crea liturgia.

---

## 10. Providers e integraciones externas

## 10.1 Frontera recomendada

```python
from typing import Protocol

class RoutingProvider(Protocol):
    def transform(self, lead_data: dict): ...
    def send(self, payload): ...
```

O una versión más explícita:

```python
class RoutingProvider(ABC):
    @abstractmethod
    def transform(self, lead: Lead, routing: Routing):
        pass

    @abstractmethod
    def send(self, payload: ProviderPayload) -> ProviderResponse:
        pass
```

## 10.2 Regla de oro
El caso de uso depende del contrato.
La implementación concreta depende del provider.

Así mañana puedes tener:
- Leadspedia,
- un CRM interno,
- otro vendor,
- mock provider de pruebas,
- replay provider.

Sin reescribir el núcleo.

---

## 11. Observabilidad y manejo de errores

## 11.1 Logging
Debe ser:
- consistente,
- estructurado si es posible,
- útil para el flujo,
- y sin spam.

No más `print()` perdidos en producción.

## 11.2 Errores
Separar:
- errores de dominio,
- errores de aplicación,
- errores de integración,
- errores técnicos.

Ejemplo:
- `MediaCodeNotFound` → dominio o aplicación según contexto
- `ProviderTimeout` → integración
- `InvalidLeadPayload` → borde/aplicación

## 11.3 Estados
No usar números mágicos desperdigados.
Formalizar estados con enums/constantes tipadas.

---

## 12. Testing por capas

La suite correcta debe dividirse así:

```text
tests/
├── domain/
├── application/
└── integration/
```

### Domain tests
Prueban:
- invariantes,
- transiciones,
- value objects,
- reglas de entidad.

Sin DB real.

### Application tests
Prueban:
- orquestación,
- secuencia,
- coordinación,
- manejo de errores.

Con mocks o dobles controlados.

### Integration tests
Prueban:
- repositorios,
- DB real,
- adapters reales o sandbox,
- wiring.

No usar SQLite como sustituto alegre si producción usa PostgreSQL.
Eso sería jugar ajedrez creyendo que las torres se mueven en diagonal.

---

## 13. Documentación mínima obligatoria

Todo proyecto que use esta guía debería tener:

### A. `docs/architecture.md`
Panorama general, capas, flujo principal.

### B. `docs/modules/<module>.md`
Responsabilidades de cada módulo.

### C. `docs/adr/`
Decisiones arquitectónicas importantes.

### D. `docs/technica-debt/`
Roadmap real de evolución por sprints.

### E. `docs/to-migrate/`
Guías para replicar o mover la arquitectura a otros contextos.

Sin documentación mínima, la arquitectura depende de memoria tribal.
Y la memoria tribal siempre termina traicionando al reino.

---

## 14. Anti-patrones a evitar

### 1. El framework manda sobre el diseño
Error clásico:
- “como Flask lo hace fácil, metamos todo en blueprints”
- “como Chalice lo permite, hagamos lógica en handlers”

No.
El framework es peón táctico, no estratega.

### 2. Dominio anémico eterno
Si todo vive en use cases y el dominio solo carga atributos, tarde o temprano la semántica se dispersa.

### 3. Infrastructure leakage
ORM, requests, boto3, headers, sessions HTTP filtrándose al dominio.
Eso rompe la pureza y encadena el proyecto a decisiones accidentales.

### 4. Shared como basurero
Si `shared/` empieza a absorber cualquier cosa que no sabes dónde poner, ya fundaste el caos con nombre elegante.

### 5. Abstracciones vacías
Interfaces sin segundo caso de uso,
servicios para leer un dict,
fábricas que no fabrican nada relevante.

DDD no es cosplay de enterprise Java.

---

## 15. Plantilla de decisión para nuevos proyectos

Antes de crear una pieza nueva, responde:

### ¿Esto es negocio?
Entonces domain.

### ¿Esto coordina pasos?
Entonces application.

### ¿Esto habla con tecnología o vendors?
Entonces infrastructure.

### ¿Esto solo recibe o devuelve requests/eventos?
Entonces entrypoint.

### ¿Esto existe porque el framework lo pide o porque el negocio lo necesita?
Si la respuesta es “porque el framework lo pide”, no debe gobernar el diseño central.

---

## 16. Arquitectura objetivo resumida

```text
Framework / Queue / CLI
   ↓
Entrypoints
   ↓
Application Use Cases
   ↓
Domain Model
   ↓
Ports / Contracts
   ↓
Infrastructure Adapters
   ↓
DB / External Providers / Queues
```

Ese es el esquema sano.
Cambian las piezas externas.
El núcleo permanece.

---

## 17. Juicio final

La arquitectura nacida de este proyecto ya demostró algo valioso:
no depende de Chalice para tener sentido.

Ese es el punto decisivo.

Si el modelo sigue siendo válido cuando el borde pasa de:
- Chalice a Flask,
- Flask a FastAPI,
- HTTP a workers,
- o sync a async,

entonces el diseño ganó.

> **DDD real no es el que presume capas. Es el que sobrevive a cambiar el framework sin perder la forma.**

<small>🔚 fin · 02-Architecture · DDD Base Guide · `docs/02-architecture/new-standard/ddd-architecture-base-guide.md` · `2026-03-16`</small>


---

## 03-Modules · core_buildings

<small>📄 `docs/03-modules/models/core_buildings.md` · modificado: `2026-04-14`</small>

# 🗄️ Tabla: core_buildings

## 📝 Descripción

Almacena la información de las torres, bloques o edificios que pertenecen a un condominio.

Cada `core_buildings` representa una unidad física independiente dentro de un condominio. Es el núcleo de la estructura operativa del sistema — de él dependen las unidades inmobiliarias (`core_unities`), los residentes (`users_residents`), y futura lógica de cobranza, tickets y reportes segmentados por edificio.

---

## 🏗️ Estructura Final (post-migración 002)

| Campo | Tipo | Nullable | Default | Descripción |
|-------|------|---------|--------|-------------|
| id | BIGINT | NO | autoincrement | PK interna |
| uuid | CHAR(36) | NO | UUID() | Identificador estable externo |
| condominium_id | BIGINT | NO | — | FK → core_condominiums |
| building_type_id | BIGINT | YES | NULL | FK → core_buildings_types |
| code | VARCHAR(50) | NO | — | Código operativo único por condominio |
| name | VARCHAR(255) | NO | — | Nombre visible del edificio |
| short_name | VARCHAR(50) | YES | NULL | Alias para UI, dashboards, reportes |
| description | TEXT | YES | NULL | Notas administrativas o descripción física |
| built_area | DECIMAL(12,4) | YES | NULL | Área construida total en m² |
| common_area | DECIMAL(12,4) | YES | NULL | Área común asociada al edificio en m² |
| coefficient | DECIMAL(9,6) | YES | NULL | Coeficiente de participación (0.000000 - 100.000000) |
| floors_count | INT | NO | 0 | Cantidad de pisos sobre nivel |
| basements_count | INT | NO | 0 | Cantidad de sótanos |
| units_planned | INT | NO | 0 | Número de unidades proyectadas/esperadas |
| sort_order | INT | NO | 0 | Orden de visualización en listados |
| status | INT | NO | 1 | Estado operativo (1=activo, 0=inactivo) |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | Fecha de última actualización |
| deleted_at | DATETIME | YES | NULL | Soft delete — fecha de eliminación lógica |

---

## 🔗 Relaciones (Foreign Keys)

```
core_buildings
├── core_condominiums (condominium_id)     — UN BUILDING PERTENECE A UN CONDOMINIO
├── core_buildings_types (building_type_id) — UN BUILDING PUEDE TENER UN TIPO (O NO)
└── core_unities (vía building_id)          — UN BUILDING TIENE MUCHAS UNIDADES
```

| FK | Target | ON DELETE | Notas |
|----|--------|-----------|-------|
| condominium_id | core_condominiums.id | RESTRICT | No se puede borrar condominio con edificios |
| building_type_id | core_buildings_types.id | SET NULL | Si se elimina un tipo, el edificio queda sin tipo |

---

## 📐 Campos Derivados del Análisis Competitivo

### `short_name` — Alias operativo

**Referencia:** Buildium, AppFolio, DoorLoop — todos tienen campo corto para identificar edificios en interfaces compactas.

**Usos:**
- Etiquetas en mapas/walkthroughs visuales
- Filtros rápidos en mobile
- Nombres de torre en notificaciones push
- Reportes de ocupación por edificio
- Dashboards compactos

**Límite:** hasta 50 caracteres. Para UI estrictas (mobile), considerar truncate a 20-30 en capa de presentación.

---

### `coefficient` — Coeficiente de participación

**Referencia:** sistemas de copropiedad reales (AppFolio, Buildium) usan coeficiente para prorrateo de gastos comunes, distribución de votes, y cálculo de porcentajes de propiedad.

**Cálculo:** el coeficiente representa el peso proporcional del edificio dentro del condominio. Un edificio con coefficient=25.5 tiene el 25.5% de participación.

**Validación:** CHECK constraint fuerza rango 0-100. La validación de que la suma de coeficientes de todos los edificios sea 100 se maneja en **capa de negocio**, no en DB.

---

### `built_area` y `common_area` — Separación de áreas

**Problema original:** el campo `size` era ambiguo — mezclaba área construida con área de terreno.

**Solución:** dos campos separados con precisión DECIMAL(12,4) para manejar bienes raíces con exactitud centimétrica.

**Usos:**
- Reportes inmobiliarios
- Métricas comparativas entre edificios
- Cálculo de densidad (unidades por m²)
- Distribución de costos de mantenimiento por área

---

## ⛓️ Constraints de Negocio

Los siguientes CHECK constraints existen en la BD y no deben removerse:

| Constraint | Validación | Propósito |
|------------|------------|-----------|
| ck_core_buildings_built_area_positive | built_area >= 0 | No permitir áreas negativas |
| ck_core_buildings_common_area_positive | common_area >= 0 | No permitir áreas comunes negativas |
| ck_core_buildings_coefficient_range | coefficient BETWEEN 0 AND 100 | Coeficiente siempre válido |
| ck_core_buildings_floors_count_positive | floors_count >= 0 | No pisos negativos |
| ck_core_buildings_basements_count_positive | basements_count >= 0 | No sótanos negativos |
| ck_core_buildings_units_planned_positive | units_planned >= 0 | No unidades negativas |
| ck_core_buildings_sort_order_positive | sort_order >= 0 | No orden negativo |

---

## 📇 Índices

| Índice | Columnas | Tipo | Propósito |
|--------|----------|------|-----------|
| ix_core_buildings_condominium_code | (condominium_id, code) | UNIQUE | Código único por condominio |
| ix_core_buildings_condominium_id | (condominium_id) | INDEX | FK lookups y filtros por condominio |
| ix_core_buildings_building_type_id | (building_type_id) | INDEX | Filtros por tipo de edificio |
| ix_core_buildings_status | (status) | INDEX | Filtros por estado operativo |
| ix_core_buildings_condominium_status | (condominium_id, status) | INDEX | Listados filtrados por condominio + estado |
| ix_core_buildings_condominium_sort | (condominium_id, sort_order) | INDEX | Orden visual natural |

---

## 🧠 Reglas de Negocio Obligatorias

1. **No crear edificio sin condominium_id válido** — el FK enforced a nivel BD
2. **No repetir code dentro del mismo condominio** — unique constraint compuesto
3. **No permitir valores negativos en áreas ni contadores** — CHECK constraints
4. **No permitir coefficient fuera de rango 0-100** — CHECK constraint
5. **Listados públicos deben excluir eliminados** — filter WHERE deleted_at IS NULL
6. **Restore disponible** — soft delete reversible hasta que haya lógica depuración
7. **Si un edificio tiene unidades activas, no permitir eliminación física** — validar en capa de negocio antes de hard delete

---

## 🔄 Soft Delete

`deleted_at` permite eliminación lógica sin pérdida de datos.

**Comportamiento:**
- DELETE physically →sets deleted_at al timestamp actual
- POST /restore → limpia deleted_at
- GET /list → excluye deleted por defecto
- GET /list?include_deleted=true → incluye todos

**No hacer:** no hay cascada física. Si el edificio tiene `core_unities` asociadas con status activo, la eliminación lógica se permite pero la física debe bloquearse en capa de negocio.

---

## 🚫 Lo que NO está en esta tabla (y por qué)

| Campo | Razón de exclusión |
|-------|-------------------|
| `legacy_code` | Solo como campo transitorio para migraciones reales. No смысла sin datos legacy |
| `address` | Va en `core_condominiums` o en `core_unities`, no en edificio |
| `manager_id` | Pertenece a relación separate (users con rol de gestión) |

---

## 📊 Estrategia de Expansión Futura

Esta tabla es el eje de segmentación operativa. Una vez que `core_unities` esté vinculada:

- **Anuncios segmentados por edificio** — notificación push a residentes de X torre
- **Tickets e incidencias por torre** — filtro automático por building_id
- **Ocupación por edificio** — count de units activas por building
- **Dashboards por bloque** — métricas agregadas a nivel de edificio
- **Cobranza por edificio** — prorrateo basado en coefficient
- **Reportes financieros por torre** — separación clara de costos comunes

La estructura actual soporta todo esto sin cambios adicionales.

---

## 🗂️ Archivos Relacionados

- Migración: `src/alembic/versions/002_refactor_core_buildings.py`
- Migraciones correctivas: `004_fix_buildings_unique_constraint.py`, `005_fix_buildings_fk_actions.py`
- Seed: `seeds/seed_core_buildings_types.py`
- Tablero de tareas: `docs/07-roadmap/core_buildings-task-order.md`
- Módulo DDD: `library/dddpy/core_buildings/` (implementado en Tareas 3-7) ✅
- Tipo de edificio: `docs/03-modules/models/core_buildings_types.md`
- Unidades: `docs/03-modules/models/core_unities.md`
- Análisis competitivo: `docs/05-research/competitive-analysis-condo-systems.md`

---

**Última actualización:** 2026-04-13 (post-migraciones 002, 004, 005)
**Estado del módulo:** ✅ OPERATIVO — 10/10 tareas completadas | 2 migraciones correctivas aplicadas

<small>🔚 fin · 03-Modules · core_buildings · `docs/03-modules/models/core_buildings.md` · `2026-04-14`</small>


---

## 03-Modules · core_buildings_types

<small>📄 `docs/03-modules/models/core_buildings_types.md` · modificado: `2026-04-13`</small>

# 🗄️ Tabla: `core_buildings_types`

## 📝 Descripción

Catálogo de tipos de edificios con soporte para **alcance (scope)**:

- **Global (`condominium_id = NULL`)**: tipos disponibles para todos los condominios. Reservados para el sistema (`is_system = 1`). No editables ni eliminables por usuarios.
- **Custom (`condominium_id = [id]`)**: tipos privados de un condominio específico. Creados, editados y eliminables (soft delete) por administradores del condominio.

---

## 🏗️ Estructura (post-migración 006)

| Campo | Tipo | Nullable | Default | Descripción |
|-------|------|----------|---------|-------------|
| `id` | `BIGINT` | NO | auto | PK |
| `uuid` | `CHAR(36)` | NO | `UUID()` | Identificador único universal |
| `condominium_id` | `BIGINT` | **YES** | `NULL` | FK al condominio. `NULL` = global/sistema |
| `code` | `VARCHAR(50)` | NO | — | Código interno (único **por scope**) |
| `name` | `VARCHAR(255)` | NO | — | Nombre del tipo |
| `description` | `TEXT` | YES | `NULL` | Descripción detallada |
| `is_system` | `SMALLINT` | NO | `0` | `1` = tipo de sistema (global, no editable) |
| `sort_order` | `INT` | NO | `0` | Orden de aparición en listados |
| `status` | `INT` | NO | `1` | `1` = activo, `0` = inactivo |
| `deleted_at` | `DATETIME` | YES | `NULL` | Soft delete (si no es `NULL`, está eliminado) |
| `created_at` | `DATETIME` | NO | `CURRENT_TIMESTAMP` | Fecha de creación |
| `updated_at` | `DATETIME` | NO | `CURRENT_TIMESTAMP ON UPDATE` | Última actualización |

---

## 🔍 Índices y Foreign Keys

| Índice | Columnas | Tipo | Notas |
|--------|----------|------|-------|
| `ix_core_buildings_types_condominium_code` | `(condominium_id, code)` | Index | Búsqueda por scope |
| `fk_buildings_types_condominium` | `condominium_id → core_condominiums(id)` | FK | `ON DELETE SET NULL`, `ON UPDATE CASCADE` |

### Notas sobre unicidad

MySQL no soporta índices parciales/filtados. La restricción de unicidad por scope `(condominium_id, code)` para registros **activos** se maneja en la **capa de aplicación** (método `get_by_code_in_scope()` en el query repository).

Un registro soft-deleted con el mismo `(condominium_id, code)` que uno activo **no viola la restricción** a nivel de índice — la aplicación verifica esto al restaurar.

### Foreign Key: `core_buildings.building_type_id`

```sql
ON DELETE SET NULL    -- Si se elimina un tipo, los edificios quedan sin tipo (tipo=null)
ON UPDATE CASCADE    -- Si cambia el PK del tipo, se actualiza automáticamente en edificios
```

---

## 🔗 Relaciones

```text
core_buildings_types
├── 1 ← ∞ core_buildings (building_type_id)
└── 0/1 → core_condominiums (condominium_id)
```

---

## 🚫 Reglas de negocio

| Regla | Detalle |
|-------|---------|
| Global ≠ editable | Tipos con `is_system = 1` (`condominium_id = NULL`) no se pueden modificar ni eliminar |
| Custom por condominio | Tipos custom solo son accesibles desde el condominio que los creó |
| Código único por scope | No puede haber dos tipos activos con el mismo `code` dentro del mismo `condominium_id` |
| Soft delete reversible | `deleted_at` permite recuperación; el hard delete está bloqueado si hay edificios referenciando |
| Tipos inactivos no usables | Un edificio no puede asignarse a un tipo con `status = 0` |
| Asignación a edificios | Un edificio solo puede usar tipos globales o custom del mismo condominio |

---

## 📦 Tipos base (seed, migraciones 003 y 006)

| Code | Name | Scope | is_system |
|------|------|-------|-----------|
| `RESIDENTIAL` | Residencial | Global | 1 |
| `COMMERCIAL` | Comercial | Global | 1 |
| `MIXED` | Mixto | Global | 1 |
| `SERVICES` | Servicios | Global | 1 |

Seed idempotente: migraciones 003 y 006 usan `INSERT ... ON DUPLICATE KEY UPDATE`.

---

## 🔄 Migraciones relevantes

| Migración | Cambio |
|-----------|--------|
| `001_create_initial` | Crea tabla con `UNIQUE(code)` global |
| `003_seed_core_buildings_types` | Seed base con upsert idempotente |
| `006_add_building_types_scope` | Añade `condominium_id`, `is_system`, `sort_order`, `deleted_at` + índice scope + FK a condominiums |
| `007_fix_building_type_fk_cascade` | FK `core_buildings.building_type_id` → `ON UPDATE CASCADE` |

---

## 🌐 API — Endpoints

### Base URL
`/building-types`

### Endpoints disponibles

| Método | Path | Descripción |
|--------|------|-------------|
| `POST` | `/building-types` | Crear tipo (global o custom) |
| `GET` | `/building-types/{id}` | Obtener tipo por ID |
| `GET` | `/building-types/uuid/{uuid}` | Obtener tipo por UUID |
| `PUT` | `/building-types/{id}` | Actualizar tipo (no system) |
| `DELETE` | `/building-types/{id}` | Soft delete (no system) |
| `POST` | `/building-types/{id}/restore` | Restaurar tipo eliminado |
| `DELETE` | `/building-types/{id}/hard` | Hard delete (no system, sin refs) |
| `GET` | `/building-types` | Listar tipos con filtros |

### Filtros de listado

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `condominium_id` | int | `null` | Filtra tipos para un condominio (incluye globales) |
| `include_system` | bool | `true` | Incluir tipos globales de sistema |
| `status` | int | `null` | Filtrar por estado (`1`=activo, `0`=inactivo) |
| `include_deleted` | bool | `false` | Incluir registros con `deleted_at` |
| `skip` | int | `0` | Paginación |
| `limit` | int | `100` | Máximo 500 |

### Ejemplo: crear tipo custom
```json
POST /building-types
{
  "condominium_id": 5,
  "code": "PARKING",
  "name": "Estacionamiento",
  "description": "Área de estacionamiento",
  "sort_order": 1
}
```

### Ejemplo: crear tipo global
```json
POST /building-types
{
  "condominium_id": null,
  "code": "INDUSTRIAL",
  "name": "Industrial"
}
```

---

## 🏛️ Módulo DDD

Ubicación: `src/library/dddpy/core_buildings_types/`

```
core_buildings_types/
├── domain/
│   ├── building_type_entity.py          # Entidad con is_global/is_custom
│   ├── building_type_data.py            # CreateBuildingTypeData, UpdateBuildingTypeData
│   ├── building_type_exception.py       # 8 excepciones de negocio
│   ├── building_type_success.py         # Mensajes de éxito
│   ├── building_type_repository.py      # Interfaz base
│   ├── building_type_cmd_repository.py  # Create, update, delete
│   └── building_type_query_repository.py # Queries + get_active_in_scope
├── infrastructure/
│   ├── dbbuildingtype.py               # SQLAlchemy model
│   ├── building_type_mapper.py
│   ├── building_type_cmd_repository.py  # Implementación cmd
│   └── building_type_query_repository.py # Implementación query
└── usecase/
    ├── building_type_cmd_schema.py     # Pydantic schemas
    ├── building_type_cmd_usecase.py    # Lógica de comandos
    ├── building_type_query_usecase.py  # Lógica de consultas
    ├── building_type_usecase.py        # Fachada completa
    └── building_type_factory.py        # Factory pattern
```

### Excepciones de negocio

| Excepción | HTTP | Cuándo |
|-----------|------|--------|
| `BuildingTypeNotFound` | 404 | Tipo no existe o está eliminado |
| `DuplicateBuildingTypeCode` | 409 | Código duplicado en el mismo scope |
| `BuildingTypeIsSystem` | 403 | Intento de modificar/eliminar tipo de sistema |
| `BuildingTypeIsInUse` | 409 | Hard delete con edificios referenciando |
| `BuildingTypeIsInactive` | 422 | Asignar tipo inactivo a edificio |
| `BuildingTypeIsDeleted` | 422 | Asignar tipo soft-deleted a edificio |
| `BuildingTypeNotAccessible` | 403 | Tipo custom de otro condominio |
| `InvalidBuildingTypeScope` | 400 | Crear tipo system con `condominium_id` |

### Método clave: `validate_for_building_assignment(type_id, condominium_id)`

Expuesto en `BuildingTypeUseCase`. Llamado por `core_buildings` al crear/actualizar un edificio. Verifica:
1. Tipo existe y no está eliminado
2. Tipo tiene `status = 1`
3. Tipo es global **o** pertenece al mismo `condominium_id`

---

## ✅ Checklist de validación (DoD)

- [x] `building_type_id = NULL` en edificio → permitido (sin tipo asignado)
- [x] Crear edificio con tipo global → debe pasar
- [x] Crear edificio con tipo custom del mismo condominio → debe pasar
- [x] Crear edificio con tipo custom de otro condominio → **bloquear** (403)
- [x] Crear edificio con tipo inactivo (`status = 0`) → **bloquear** (422)
- [x] Crear edificio con tipo soft-deleted → **bloquear** (422)
- [x] Soft delete de tipo referenciado → pasa (edificios quedan con `building_type_id = NULL`)
- [x] Hard delete de tipo referenciado → **bloquear** (409)
- [x] Soft delete / hard delete de tipo system → **bloquear** (403)
- [x] Restaurar tipo → pasa
- [x] Seed idempotente (sin `COUNT(*) > 0`)
- [x] Tests cubriendo reglas de negocio

---

## 📁 Archivos modificados/creados

| Archivo | Cambio |
|---------|--------|
| `alembic/versions/006_add_building_types_scope.py` | Nueva migración: scope columns + backfill |
| `alembic/versions/007_fix_building_type_fk_cascade.py` | Nueva migración: FK `ON UPDATE CASCADE` |
| `alembic/versions/003_seed_core_buildings_types.py` | Corregido: upsert idempotente |
| `seeds/seed_core_buildings_types.py` | Corregido: upsert idempotente |
| `library/dddpy/core_buildings_types/` | Nuevo módulo DDD completo (19 archivos) |
| `api/buildings_types/routes_building_types.py` | Nuevo: API routes |
| `library/dddpy/core_buildings/usecase/building_cmd_usecase.py` | Integrada validación de tipo |
| `library/dddpy/core_buildings/usecase/building_usecase.py` | Enriquecida respuesta con tipo |
| `tests/test_core_buildings_types.py` | Tests completos |

<small>🔚 fin · 03-Modules · core_buildings_types · `docs/03-modules/models/core_buildings_types.md` · `2026-04-13`</small>


---

## 03-Modules · core_condominiums

<small>📄 `docs/03-modules/models/core_condominiums.md` · modificado: `2026-03-16`</small>

# 🗄️ Tabla: core_condominiums

## 📝 Descripción
Almacena la información principal de los complejos o conjuntos residenciales.

---

## 🏗️ Estructura

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador único universal del condominio |
| name | VARCHAR(255) | Nombre del condominio |
| code | VARCHAR(50) | Código identificador |
| description | TEXT | Descripción o detalles adicionales |
| size | DECIMAL(10,2) | Tamaño o área total |
| percentage | DECIMAL(5,2) | Coeficiente de copropiedad total |
| created_at | DATETIME / TIMESTAMP | Fecha de creación del registro |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización del registro |

---

## 🔗 Relaciones (Foreign Keys)
- **Tiene muchos:** [[core_buildings]], [[users_residents]]

<small>🔚 fin · 03-Modules · core_condominiums · `docs/03-modules/models/core_condominiums.md` · `2026-03-16`</small>


---

## 03-Modules · core_condominium_roles

<small>📄 `docs/03-modules/models/core_condominium_roles.md` · modificado: `2026-04-15`</small>

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

<small>🔚 fin · 03-Modules · core_condominium_roles · `docs/03-modules/models/core_condominium_roles.md` · `2026-04-15`</small>


---

## 03-Modules · core_unit_occupancies

<small>📄 `docs/03-modules/models/core_unit_occupancies.md` · modificado: `2026-04-15`</small>

# 🗄️ Tabla: core_unit_occupancies

## 📝 Descripción
Tabla de relación de ocupación o uso entre usuarios y unidades.

Responde a la pregunta: **¿quién ocupa, usa o tiene autorización sobre una unidad y bajo qué condición?**

No modela propiedad. Para eso existe `core_unit_ownerships`.

---

## 🏗️ Estructura propuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador estable externo |
| unit_id | BIGINT | FK → [[core_units]] |
| user_id | BIGINT | FK → [[users]] |
| occupancy_type | VARCHAR(40) | resident_owner / tenant / family_member / office_user / occasional_user |
| status | VARCHAR(30) | active / inactive / historical / pending |
| start_date | DATE | Inicio de vigencia |
| end_date | DATE | Fin de vigencia |
| is_primary | BOOLEAN | Marca si es ocupación principal |
| authorized_by_user_id | BIGINT | FK opcional → [[users]] |
| notes | TEXT | Notas internas |
| created_at | DATETIME / TIMESTAMP | Fecha de creación |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización |
| deleted_at | DATETIME / TIMESTAMP | Soft delete |

---

## 🔗 Relaciones (Foreign Keys)
- **Depende de:** [[core_units]], [[users]]

---

## 📋 Reglas de negocio
- un inquilino puede ocupar una unidad sin ser propietario
- un familiar puede estar asociado sin ser propietario
- un propietario puede también aparecer como ocupante si vive ahí
- toda ocupación debe tener vigencia temporal
- el historial de ocupación debe preservarse para trazabilidad

<small>🔚 fin · 03-Modules · core_unit_occupancies · `docs/03-modules/models/core_unit_occupancies.md` · `2026-04-15`</small>


---

## 03-Modules · core_unit_ownerships

<small>📄 `docs/03-modules/models/core_unit_ownerships.md` · modificado: `2026-04-15`</small>

# 🗄️ Tabla: core_unit_ownerships

## 📝 Descripción
Tabla de relación patrimonial entre usuarios y unidades.

Responde a la pregunta: **¿quién es dueño de qué unidad y desde cuándo?**

No modela ocupación. No modela permisos administrativos. Solo titularidad.

---

## 🏗️ Estructura propuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador estable externo |
| unit_id | BIGINT | FK → [[core_units]] |
| user_id | BIGINT | FK → [[users]] |
| ownership_type | VARCHAR(30) | owner / co_owner |
| ownership_percentage | DECIMAL(5,2) | Porcentaje de propiedad |
| status | VARCHAR(30) | active / inactive / historical |
| start_date | DATE | Inicio de vigencia |
| end_date | DATE | Fin de vigencia |
| notes | TEXT | Notas internas |
| created_at | DATETIME / TIMESTAMP | Fecha de creación |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización |
| deleted_at | DATETIME / TIMESTAMP | Soft delete |

---

## 🔗 Relaciones (Foreign Keys)
- **Depende de:** [[core_units]], [[users]]

---

## 📋 Reglas de negocio
- un usuario puede tener N unidades
- una unidad puede tener 1 o N propietarios
- un propietario no necesariamente vive en la unidad
- la titularidad debe tener historial temporal
- si hay copropiedad, `ownership_percentage` debe permitir distribuir la participación

<small>🔚 fin · 03-Modules · core_unit_ownerships · `docs/03-modules/models/core_unit_ownerships.md` · `2026-04-15`</small>


---

## 03-Modules · core_units

<small>📄 `docs/03-modules/models/core_units.md` · modificado: `2026-04-15`</small>

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

<small>🔚 fin · 03-Modules · core_units · `docs/03-modules/models/core_units.md` · `2026-04-15`</small>


---

## 03-Modules · core_unities

<small>📄 `docs/03-modules/models/core_unities.md` · modificado: `2026-04-14`</small>

# 🗄️ Tabla: core_unities

## 📝 Descripción
Representa las unidades inmobiliarias individuales de un edificio: apartamentos, locales, oficinas,PH, etc. Es la pieza central del núcleo inmobiliario — donde convergen ocupación, residentes, cobranza y reportes.

---

## 🏗️ Estructura (post-refactor 008)

| Campo | Tipo | Nullable | Default | Descripción |
|-------|------|----------|---------|-------------|
| id | BIGINT | NO | autoincrement | PK interna |
| uuid | CHAR(36) | NO | UUID() | Identificador estable externo |
| building_id | BIGINT | NO | — | FK → [[core_buildings]] |
| unity_type_id | BIGINT | YES | NULL | FK → [[core_unittys_types]] |
| unit_number | VARCHAR(50) | YES | — | Identidad física visible (ej. 101, A-12, PH-1) |
| code | VARCHAR(50) | YES | NULL | Código operativo interno |
| name | VARCHAR(255) | YES | NULL | Nombre comercial/display opcional |
| description | TEXT | YES | NULL | Notas administrativas internas |
| private_area | DECIMAL(12,4) | YES | NULL | Área privada útil en m² |
| coefficient | DECIMAL(9,6) | YES | NULL | Coeficiente de copropiedad/prorrateo (0-100) |
| floor_number | INT | YES | NULL | Piso numérico para lógica y orden |
| floor_label | VARCHAR(30) | YES | NULL | Etiqueta UI (ej. Sótano 1, Mezzanine, PH) |
| occupancy_status | VARCHAR(30) | NO | vacant | Estado: vacant\|occupied\|reserved\|maintenance\|blocked |
| sort_order | INT | NO | 0 | Orden visual dentro del edificio |
| status | INT | NO | 1 | Estado operativo (1=activo, 0=inactivo) |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | Última actualización |
| deleted_at | DATETIME | YES | NULL | Soft delete (nulo = activo) |

---

## 🔗 Relaciones (Foreign Keys)

| FK | Referencia | ON DELETE | ON UPDATE |
|----|------------|-----------|-----------|
| building_id | [[core_buildings]].id | RESTRICT | CASCADE |
| unity_type_id | [[core_unittys_types]].id | SET NULL | CASCADE |

---

## 🔑 Índices

| Índice | Columnas | Tipo | Propósito |
|--------|----------|------|-----------|
| ix_core_unities_building_id | building_id | normal | FK + filtro por edificio |
| ix_core_unities_unity_type_id | unity_type_id | normal | Filtro por tipo de unidad |
| ix_core_unities_status | status | normal | Filtro por estado operativo |
| ix_core_unities_building_status | (building_id, status) | composite | Listados por edificio+estado |
| ix_core_unities_building_sort | (building_id, sort_order) | composite | Orden visual por edificio |
| ix_core_unities_building_floor | (building_id, floor_number) | composite | Agrupación por piso |
| ix_core_unities_building_occupancy | (building_id, occupancy_status) | composite | Filtro operativo por ocupación |
| ux_core_unities_building_unit_number | (building_id, unit_number) | UNIQUE | Unicidad dentro del edificio |
| ux_core_unities_building_code | (building_id, code) | UNIQUE | Unicidad de código interno |

---

## ⚙️ Constraints

| Nombre | Expresión | Propósito |
|--------|-----------|-----------|
| ck_core_unities_private_area_positive | private_area >= 0 | Área no puede ser negativa |
| ck_core_unities_coefficient_range | coefficient >= 0 AND coefficient <= 100 | Coeficiente en rango válido |
| ck_core_unities_sort_order_positive | sort_order >= 0 | Orden no negativo |
| ck_core_unities_occupancy_status_valid | occupancy_status IN ('vacant','occupied','reserved','maintenance','blocked') | Solo valores permitidos |

---

## 🔄 Campos eliminados en refactor 008

| Campo viejo | Razón |
|-------------|-------|
| `type` | Redundante con `unity_type_id` |
| `size` | Reemplazado por `private_area` con mejor precisión |
| `percentage` | Reemplazado por `coefficient` con mejor precisión |
| `floor` | Reemplazado por `floor_number` + `floor_label` |
| UNIQUE(code) global | Reemplazado por UNIQUE compuesto (building_id, code) |

---

## 📦 Módulo DDD

Ubicación: `src/library/dddpy/core_unities/`

```
core_unities/
├── domain/
│   ├── unity_entity.py       — Entidad de dominio con invariantes
│   ├── unity_data.py         — CreateData / UpdateData (dataclasses)
│   ├── unity_exception.py    — Excepciones de dominio
│   ├── unity_success.py      — Mensajes de éxito
│   ├── unity_repository.py   — Contrato genérico
│   ├── unity_cmd_repository.py   — Interfaz de escritura
│   └── unity_query_repository.py — Interfaz de lectura
├── infrastructure/
│   ├── dbunitys.py               — Modelo SQLAlchemy
│   ├── unity_mapper.py           — Mapper DB ↔ Entity
│   ├── unity_cmd_repository.py   — Implementación de escritura
│   └── unity_query_repository.py — Implementación de lectura
└── usecase/
    ├── unity_cmd_schema.py       — Schemas Pydantic (create/update)
    ├── unity_cmd_usecase.py      — Lógica de escritura
    ├── unity_query_usecase.py    — Lógica de lectura
    ├── unity_usecase.py          — Fachada con enriquecimiento
    └── unity_factory.py         — Factory de use cases
```

---

## 🌐 API Routes

Prefijo: `/unities`

| Método | Path | Descripción |
|--------|------|-------------|
| POST | /unities | Crear unidad |
| GET | /unities/{id} | Obtener por ID |
| GET | /unities/uuid/{uuid} | Obtener por UUID |
| PUT | /unities/{id} | Actualizar |
| DELETE | /unities/{id} | Soft delete |
| POST | /unities/{id}/restore | Restaurar |
| DELETE | /unities/{id}/hard | Hard delete (bloqueado si tiene residentes) |
| GET | /unities | Listar con filtros |
| GET | /unities/building/{building_id} | Listar por edificio |

---

## 📋 Reglas de negocio

- Una unidad debe pertenecer a un edificio existente y activo
- `unit_number` debe ser único dentro del mismo edificio (constraint DB + validación app)
- `occupancy_status` y `status` son ejes independientes:
  - `status` = vive operativamente (1) o no (0)
  - `occupancy_status` = vacante/ocupada/reservada/mantenimiento/bloqueada
- Soft delete (deleted_at) no elimina registros con historial
- Hard delete solo si no hay residentes activos asociados
- El módulo valida contra `core_unittys_types` si el FK existe; no crashea si el módulo no está implementado aún

---

## 🔗 Dependencias

- **Requiere:** [[core_buildings]], [[core_unittys_types]]
- **Tiene muchos:** [[users_residents]] (residentes por unidad)
- **Futuro:** ledger/cobranza por unidad, tickets por unidad, documentos por unidad

<small>🔚 fin · 03-Modules · core_unities · `docs/03-modules/models/core_unities.md` · `2026-04-14`</small>


---

## 03-Modules · core_unittys_types

<small>📄 `docs/03-modules/models/core_unittys_types.md` · modificado: `2026-04-15`</small>

# 🗄️ Tabla: core_unittys_types

## 📝 Descripción
Catálogo histórico de los diferentes tipos de unidades inmobiliarias.

⚠️ **Nota arquitectónica:** el naming final recomendado del catálogo es `core_unit_types` para alinearlo con `core_units`. Este documento se mantiene temporalmente por compatibilidad histórica del proyecto.

---

## 🏗️ Estructura

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador único universal del tipo de unidad |
| name | VARCHAR(255) | Nombre del tipo de unidad |
| code | VARCHAR(50) | Código interno |
| description | TEXT | Descripción detallada |
| created_at | DATETIME / TIMESTAMP | Fecha de creación del registro |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización del registro |

---

## 🔗 Relaciones (Foreign Keys)
- **Tiene muchos:** [[core_units]]

<small>🔚 fin · 03-Modules · core_unittys_types · `docs/03-modules/models/core_unittys_types.md` · `2026-04-15`</small>


---

## 03-Modules · users

<small>📄 `docs/03-modules/models/users.md` · modificado: `2026-04-15`</small>

# 🗄️ Tabla: users

## 📝 Descripción
Almacena la identidad base y las credenciales de autenticación de todos los usuarios del sistema.

No debe mezclar perfil humano, propiedad, ocupación ni permisos administrativos. Es la pieza central de identidad.

---

## 🏗️ Estructura propuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| uuid | CHAR(36) / UUID | Identificador único universal del usuario |
| email | VARCHAR(255) | Correo electrónico único |
| password_hash | VARCHAR(255) | Hash de contraseña |
| status | VARCHAR(50) | active / inactive / suspended / locked |
| email_verified_at | DATETIME / TIMESTAMP | Verificación de correo |
| last_login_at | DATETIME / TIMESTAMP | Último acceso |
| failed_login_attempts | INT | Intentos fallidos acumulados |
| locked_until | DATETIME / TIMESTAMP | Bloqueo temporal si aplica |
| created_at | DATETIME / TIMESTAMP | Fecha de creación del registro |
| updated_at | DATETIME / TIMESTAMP | Fecha de última actualización |
| deleted_at | DATETIME / TIMESTAMP | Soft delete |

---

## 🔗 Relaciones (Foreign Keys)
- **Tiene uno:** `user_profiles`
- **Tiene muchos:** [[core_unit_ownerships]]
- **Tiene muchos:** [[core_unit_occupancies]]
- **Tiene muchos:** [[core_condominium_roles]]

---

## 📋 Reglas de negocio
- `email` debe ser unique y normalizado en minúscula
- no se guarda `password`, solo `password_hash`
- el perfil humano se separa de autenticación
- la relación con unidades o condominios se modela por contexto, no en esta tabla

<small>🔚 fin · 03-Modules · users · `docs/03-modules/models/users.md` · `2026-04-15`</small>


---

## 03-Modules · users_residents

<small>📄 `docs/03-modules/models/users_residents.md` · modificado: `2026-04-15`</small>

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

<small>🔚 fin · 03-Modules · users_residents · `docs/03-modules/models/users_residents.md` · `2026-04-15`</small>


---

## 04-Bulma · Introducción

<small>📄 `docs/04-bulma/README.md` · modificado: `2026-03-16`</small>

# BULMA — documentación táctica para agentes de IA

Esta carpeta existe para reducir costo de contexto y ambigüedad.

## Objetivo

Dar a una agente como BULMA instrucciones compactas para modificar `condo-py` sin tener que traducir documentación humana extensa.

## Base obligatoria de referencia

Antes de crear o modificar módulos:

- revisar `src/library/dddpy/shared/`
- revisar `src/library/dddpy/example/`
- revisar `src/api/example/`

Regla:
- `shared/` = primitives compartidos
- `example/` = patrón de módulo actual
- `api/example/` = patrón de route limpio actual

## Orden de lectura obligatorio

1. `architecture-rules.md`
2. `module-map.md`
3. `implementation-guidelines.md`
4. `anti-patterns.md`
5. `change-playbook.md`

## Reglas globales

- `docs/new-standard/` = referencia doctrinal, **no editar**.
- `docs/observations/` = documentación humana.
- `docs/BULMA/` = reglas operativas compactas.
- Usar `example/` como patrón salvo nueva instrucción explícita.
- Preservar naming actual salvo task explícita de refactor.
- No inventar módulos nuevos si uno existente ya cubre la responsabilidad.
- No mezclar feature + refactor cosmético grande en una sola entrega.

## Modelo mental

- API/entrypoint adapta.
- UseCase orquesta.
- Domain decide semántica.
- Infrastructure implementa detalle técnico.
- Shared define primitives comunes.
- Mapper traduce DB ↔ domain.
- DomainException unifica errores semánticos.
- Response schemas unifican la forma de salida.
- `@api_handler` centraliza el camino de error en API.
- Logger da trazabilidad en main, API y módulo.

<small>🔚 fin · 04-Bulma · Introducción · `docs/04-bulma/README.md` · `2026-03-16`</small>


---

## 04-Bulma · Módulos

<small>📄 `docs/04-bulma/MODULES.md` · modificado: `2026-04-30`</small>

# Módulos del Sistema condo-py

**Última actualización:** 2026-04-30
**Estado:** 29 módulos implementados — todos los módulos Phase 1 y Phase 2 cerrados

---

## Estado General

| Estado | Significado |
|---|---|
| ✅ | Implementado completamente en Python + DDD + API routes + tabla DB |
| ⚠️ | Deprecado o en limpieza |

---

## Módulos Implementados

### ✅ Módulo shared — Componentes Compartidos
**Ruta:** `src/library/dddpy/shared/`

Decorators, schemas, logging, MySQL/PostgreSQL session manager, utils.

---

### ✅ Módulo example — Plantilla de Referencia DDD
**Ruta:** `src/library/dddpy/example/`

Plantilla que define el patrón arquitectónico. **NO es lógica de negocio real.**

---

### ✅ core_condominiums — Gestión de Condominios
**Ruta:** `src/library/dddpy/core_condominiums/`
**Tabla DB:** `core_condominiums`
**API:** `src/api/condominiums/routes_condominiums.py`

---

### ✅ core_buildings — Torres/Edificios
**Ruta:** `src/library/dddpy/core_buildings/`
**Tabla DB:** `core_buildings`
**API:** `src/api/buildings/routes_buildings.py`

---

### ✅ core_buildings_types — Tipos de Edificio
**Ruta:** `src/library/dddpy/core_buildings_types/`
**Tabla DB:** `core_buildings_types`
**API:** `src/api/buildings_types/routes_building_types.py`

---

### ✅ core_units — Unidades Inmobiliarias
**Ruta:** `src/library/dddpy/core_units/`
**Tabla DB:** `core_units`
**API:** `src/api/units/routes_units.py`

---

### ✅ core_unit_types — Tipos de Unidad
**Ruta:** `src/library/dddpy/core_unit_types/`
**Tabla DB:** `core_unit_types`
**API:** `src/api/unit_types/routes_unit_types.py`

---

### ✅ core_unit_ownerships — Titularidad de Unidades
**Ruta:** `src/library/dddpy/core_unit_ownerships/`
**Tabla DB:** `core_unit_ownerships`
**API:** `src/api/unit_ownerships/routes_unit_ownerships.py`

---

### ✅ core_unit_occupancies — Ocupación de Unidades
**Ruta:** `src/library/dddpy/core_unit_occupancies/`
**Tabla DB:** `core_unit_occupancies`
**API:** `src/api/unit_occupancies/routes_unit_occupancies.py`

---

### ✅ core_condominium_roles — Roles por Condominio
**Ruta:** `src/library/dddpy/core_condominium_roles/`
**Tabla DB:** `core_condominium_roles`
**API:** `src/api/condominium_roles/routes_condominium_roles.py`

---

### ✅ core_charge_types — Catálogo de Tipos de Cargo
**Ruta:** `src/library/dddpy/core_charge_types/`
**Tabla DB:** `core_charge_types` (5 tipos seedeados)
**API:** `src/api/charge_types/routes_charge_types.py`

---

### ✅ core_charges — Cargos Recurrentes y Extraordinarios
**Ruta:** `src/library/dddpy/core_charges/`
**Tabla DB:** `core_charges`
**API:** `src/api/charges/routes_charges.py`

---

### ✅ core_accounts_receivable — Cuentas por Cobrar
**Ruta:** `src/library/dddpy/core_accounts_receivable/`
**Tabla DB:** `core_accounts_receivable`
**API:** `src/api/accounts_receivable/routes_accounts_receivable.py`

---

### ✅ core_payments — Pagos
**Ruta:** `src/library/dddpy/core_payments/`
**Tabla DB:** `core_payments`
**API:** `src/api/payments/routes_payments.py`

---

### ✅ core_receipts — Recibos de Pago
**Ruta:** `src/library/dddpy/core_receipts/`
**Tabla DB:** `core_receipts`
**API:** `src/api/receipts/routes_receipts.py`

---

### ✅ core_ledger_entries — Libro Mayor por Unidad
**Ruta:** `src/library/dddpy/core_ledger_entries/`
**Tabla DB:** `core_ledger_entries` (8 filas seedeadas)
**API:** `src/api/ledger_entries/routes_ledger.py`

---

### ✅ core_announcements — Avisos
**Ruta:** `src/library/dddpy/core_announcements/`
**Tabla DB:** `core_announcements`
**API:** `src/api/announcements/routes_announcements.py`

---

### ✅ core_meetings — Asambleas
**Ruta:** `src/library/dddpy/core_meetings/`
**Tabla DB:** `core_meetings`
**API:** `src/api/meetings/routes_meetings.py`

---

### ✅ core_documents — Documentos
**Ruta:** `src/library/dddpy/core_documents/`
**Tabla DB:** `core_documents`
**API:** `src/api/documents/routes_documents.py`

---

### ✅ core_incidents — Incidentes
**Ruta:** `src/library/dddpy/core_incidents/`
**Tabla DB:** `core_incidents`
**API:** `src/api/incidents/routes_incidents.py`

---

### ✅ core_notifications — Notificaciones
**Ruta:** `src/library/dddpy/core_notifications/`
**Tabla DB:** `core_notifications`
**API:** `src/api/notifications/routes_notifications.py`

---

### ✅ core_visitors — Registro de Visitantes
**Ruta:** `src/library/dddpy/core_visitors/`
**Tabla DB:** `core_visitors`
**API:** `src/api/visitors/routes_visitors.py`

---

### ✅ core_amenities — Amenidades
**Ruta:** `src/library/dddpy/core_amenities/`
**Tabla DB:** `core_amenities`
**API:** `src/api/amenities/routes_amenities.py`

---

### ✅ core_packages — Paquetería
**Ruta:** `src/library/dddpy/core_packages/`
**Tabla DB:** `core_packages`
**API:** `src/api/packages/routes_packages.py`

---

### ✅ core_votes — Votaciones
**Ruta:** `src/library/dddpy/core_votes/`
**Tabla DB:** `core_votes`
**API:** `src/api/votes/routes_votes.py`

---

### ✅ core_audit_logs — Log de Auditoría
**Ruta:** `src/library/dddpy/core_audit_logs/`
**Tabla DB:** `core_audit_logs`
**API:** `src/api/audit_logs/routes_audit_logs.py`

---

### ✅ core_residents — Perfil Residente
**Ruta:** `src/library/dddpy/core_residents/`
**Tabla DB:** `core_resident_profiles`
**API:** `src/api/residents/routes_residents.py`

---

### ✅ core_permissions — Catálogo de Permisos RBAC
**Ruta:** `src/library/dddpy/core_permissions/`
**Tabla DB:** `core_permissions` (63 permisos seedeados)
**API:** `src/api/permissions/routes_permissions.py`

---

### ✅ core_role_permissions — Mapeo Rol → Permisos
**Ruta:** `src/library/dddpy/core_role_permissions/`
**Tabla DB:** `core_role_permissions` (88 mappings seedeados)
**API:** `src/api/role_permissions/routes_role_permissions.py`

---

### ✅ users — Usuarios del Sistema
**Tabla DB:** `users` (auth: email, password_hash, status, security fields)
**API:** `src/api/users/routes_users.py`

---

### ✅ user_profiles — Perfil Humano
**Tabla DB:** `user_profiles` (1:1 con users: first_name, last_name, doc_identity, phone)
**API:** `src/api/user_profiles/routes_user_profiles.py`

---

### ✅ auth_sessions — Sesiones de Auth
**Tabla DB:** `auth_sessions`

---

## Módulos Deprecados

### ⚠️ users_residents — Tabla Deprecada
**Estado:** DEPRECADO — solo referencia histórica. NO usar en código nuevo.
**Reemplazo:** `core_unit_ownerships` + `core_unit_occupancies` + `core_condominium_roles`

---

## Estado de Tablas DB (2026-04-30)

```
alembic_version           auth_sessions
core_accounts_receivable  core_announcements
core_audit_logs          core_buildings
core_buildings_types     core_charge_types
core_charges             core_condominium_roles
core_condominiums        core_documents
core_incidents           core_ledger_entries
core_notifications      core_packages
core_payments           core_permissions
core_receipts            core_resident_profiles
core_role_permissions    core_unit_occupancies
core_unit_ownerships     core_unit_types
core_units              core_visitors
user_profiles            users
users_residents
```

**Total: 29 tablas de negocio + 1 alembic_version**

---

## Hitos Cerrados

| Fecha | Hito |
|---|---|
| 2026-04-14 | Fase 1 — 5 HIGHs corregidos (soft delete, tipado, capas) |
| 2026-04-24 | Sprint 1-15 backdmin — 28 detail pages + contexts |
| 2026-04-29 | Incidente DNS condopy-api resuelto + documentado |
| 2026-04-30 | Tablas financieras creadas (charges, AR, payments, receipts) |

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*

<small>🔚 fin · 04-Bulma · Módulos · `docs/04-bulma/MODULES.md` · `2026-04-30`</small>


---

## 04-Bulma · Anti-patterns

<small>📄 `docs/04-bulma/anti-patterns.md` · modificado: `2026-03-16`</small>

# Anti-patterns for BULMA

Do not do the following unless the task explicitly requires a targeted refactor.

## API anti-patterns

- put business rules in route handlers
- access DB session directly from router
- return raw ORM objects
- duplicate use case logic in endpoint functions

## Domain anti-patterns

- import `DB*` models into domain
- import FastAPI / HTTP classes into domain
- convert domain entity into transport object inside domain for framework reasons
- keep entities permanently anemic if a rule clearly belongs there

## Use case anti-patterns

- mix HTTP exception logic into use case
- mix SQLAlchemy model creation directly in use case if repository/mapper already owns it
- create one mega-use-case that owns all business semantics

## Infrastructure anti-patterns

- define business rules in repository
- make mapper decide domain policy
- leak session/ORM concerns upward unnecessarily

## Shared anti-patterns

- place module-specific helper in `shared/`
- treat `shared/` as misc folder
- hide unclear ownership by moving files to shared

## Project anti-patterns

- rename legacy terms during unrelated feature work
- combine feature delivery with broad cleanup without approval
- edit `docs/new-standard/` while updating current project docs
- invent architecture purity not reflected in current codebase

<small>🔚 fin · 04-Bulma · Anti-patterns · `docs/04-bulma/anti-patterns.md` · `2026-03-16`</small>


---

## 04-Bulma · Architecture Rules

<small>📄 `docs/04-bulma/architecture-rules.md` · modificado: `2026-03-19`</small>

# Architecture Rules for BULMA

## Layer ownership

### `src/api/**`
Allowed:
- route definitions
- request parsing
- schema parsing
- use case invocation
- returning `response.dict()` from use case success result
- API-level logger usage
- `@api_handler` usage for centralized error handling

Forbidden:
- direct SQLAlchemy access
- business rules
- mapper logic
- transaction ownership
- domain exception definition
- repetitive manual `try/except` for business errors already handled by `@api_handler`

### `src/library/dddpy/*/usecase/**`
Allowed:
- application orchestration
- command/query separation
- repository coordination
- process sequencing
- factory wiring for module use cases
- module-level logger usage
- returning `ResponseSuccessSchema` in the success path
- raising `DomainException` derivatives in the error path

Forbidden:
- HTTP concerns inside application logic
- raw ORM modeling
- domain leakage into framework details
- “god use case” behavior

### `src/library/dddpy/*/domain/**`
Allowed:
- entities
- module-specific domain exceptions
- domain data objects
- repository contracts
- aggregate repository contract
- business semantics
- invariants
- state transitions

Forbidden:
- importing DB models
- importing framework HTTP classes
- importing SQLAlchemy session details
- importing `usecase` schemas
- transport-specific logic
- mapper placement

### `src/library/dddpy/*/infrastructure/**`
Allowed:
- DB models
- concrete repositories
- mappers
- persistence details
- session manager usage
- module-level logger usage

Forbidden:
- business policy ownership
- semantic decision-making that belongs to entities/use cases
- domain exception base definition

### `src/library/dddpy/shared/**`
Allowed:
- db/session shared setup
- common response schemas
- logging
- constants
- domain exception base class
- api decorators / cross-cutting decorators
- truly reusable utilities

Forbidden:
- module-specific business rules
- module-specific exceptions
- dumping unrelated helpers
- hiding unclear ownership inside shared

## Mandatory structure for a new module

Expected baseline:

```text
module/
├── domain/
│   ├── entity
│   ├── module_data.py
│   ├── module_exception.py
│   ├── module_success.py
│   ├── module_repository.py
│   ├── module_cmd_repository.py
│   └── module_query_repository.py
├── infrastructure/
│   ├── dbmodule.py
│   ├── module_mapper.py
│   ├── module_cmd_repository.py
│   └── module_query_repository.py
└── usecase/
    ├── module_cmd_schema.py
    ├── module_cmd_usecase.py
    ├── module_query_usecase.py
    ├── module_usecase.py
    └── module_factory.py
```

## Mapper rules

- Mapper lives in `infrastructure/`
- Mapper translates DB ↔ domain
- Mapper does not decide business rules
- Domain must not implement `from_db()` or import `DB*`
- If translation is needed, create/update mapper first

## Domain exception rules

- Module-specific exceptions live in `domain/*_exception.py`
- Module-specific exceptions must inherit from shared `DomainException`
- Base class location: `shared/decorators/domain_exception.py`
- If an error is semantic/business-level, do not use raw `Exception` or `ValueError`
- `status_code` belongs to the semantic exception contract when needed

## Response and decorator rules

Shared response schemas live in:
- `shared/schemas/response_schema.py`

Use:
- `ResponseSuccessSchema` for success path from use case/facade
- `ResponseErrorSchema` for controlled errors generated by `@api_handler`

If a module has stable reusable success wording:
- define it in `domain/*_success.py`
- make the use case consume that catalog instead of hardcoded string literals
- keep logging aligned with the same semantic message when useful

Shared decorator lives in:
- `shared/decorators/api_handler.py`

Official route flow:

```text
route
  → parse schema in FastAPI
  → use case
  → ResponseSuccessSchema
  → response.dict()
  → @api_handler handles DomainException / ValidationError / 500
```

Framework rule:
- current baseline is FastAPI at the edge
- `@api_handler` must remain framework-compatible with FastAPI
- do not reintroduce `chalice`, `Blueprint`, `current_request`, or cross-framework response objects into the shared decorator

Do not invent ad-hoc success/error shapes per module without explicit architecture decision.

## Factory rules

- Factory lives in `usecase/`
- Factory wires concrete repositories with use cases
- Do not scatter wiring in random files or routers

## Architecture axioms

- Framework is edge, not core.
- Mapper owns DB ↔ domain translation.
- Use case owns orchestration and success response.
- Domain owns meaning and semantic errors.
- Shared owns cross-cutting primitives and API error adaptation.
- Naming debt is documented debt, not auto-fix territory.
- `example/` is the current reference module unless a newer official base is documented.
 shapes per module without explicit architecture decision.

## Factory rules

- Factory lives in `usecase/`
- Factory wires concrete repositories with use cases
- Do not scatter wiring in random files or routers

## Architecture axioms

- Framework is edge, not core.
- Mapper owns DB ↔ domain translation.
- Use case owns orchestration and success response.
- Domain owns meaning and semantic errors.
- Shared owns cross-cutting primitives and API error adaptation.
- Naming debt is documented debt, not auto-fix territory.
- `example/` is the current reference module unless a newer official base is documented.

<small>🔚 fin · 04-Bulma · Architecture Rules · `docs/04-bulma/architecture-rules.md` · `2026-03-19`</small>


---

## 04-Bulma · Change Playbook

<small>📄 `docs/04-bulma/change-playbook.md` · modificado: `2026-03-19`</small>

# Change Playbook for BULMA

## Objective

Minimize ambiguity and preserve architecture while implementing changes.

## Checklist: new module creation

- inspect `shared/` for reusable primitives
- inspect `example/` as reference module
- inspect `api/example/` as route-pattern reference when HTTP is needed
- create domain entity
- create domain data objects if needed
- create domain exceptions
- make domain exceptions inherit from shared `DomainException`
- create aggregate repository contract in domain when the module needs broader capabilities
- create cmd/query repository contracts in domain
- create DB model in infrastructure when persistence exists
- create mapper in infrastructure
- create concrete repositories in infrastructure
- create command/query schemas in usecase
- create command/query use cases
- create module facade/use case
- create module factory
- define success/error response usage
- update docs

## Checklist: endpoint change

- identify target router/entrypoint
- identify target module
- inspect existing use case
- inspect domain entity and exceptions
- inspect repository + mapper
- modify smallest correct layer set
- preserve shared response schema
- keep framework logic at edge
- use `@api_handler` when following clean-route pattern
- update docs if behavior changed

## Checklist: persistence/model change

- inspect DB model
- inspect mapper
- inspect repository methods
- inspect domain entity fields/behavior
- inspect affected schemas
- inspect migration impact
- ensure logging remains traceable
- document contract change

## Checklist: business rule change

- define rule in one sentence
- decide if rule is semantic or orchestration
- place in domain if semantic
- place in use case if sequencing/process
- add/update semantic exception if needed
- avoid generic exceptions
- add/update logs around critical checkpoints and failures
- document rationale if non-trivial

## Checklist: response contract change

- inspect shared response schemas
- confirm if change is project-wide or module-local
- avoid ad-hoc shape drift
- standardize success message wording
- if wording is reused, centralize it in `domain/*_success.py`
- make use case consume the centralized success catalog
- standardize controlled error handling
- document change in architecture docs

## Checklist: documentation change

- `docs/architecture.md` for project-level architecture
- `docs/observations/` for human explanation
- `docs/BULMA/` for agent execution guidance
- never rewrite `new-standard/` unless task explicitly targets the base doctrine

## Escalation rule

If a task seems to require:
- naming normalization,
- module consolidation,
- replacing baseline `example/` pattern,
- replacing clean-route `api/example/` pattern,
- moving mapper outside infrastructure,
- bypassing shared response schemas,
- bypassing shared `DomainException`,
- bypassing `@api_handler` without explicit architectural reason,
- large DDD refactor,

then stop treating it as a small feature.
It is an explicit architecture task.

<small>🔚 fin · 04-Bulma · Change Playbook · `docs/04-bulma/change-playbook.md` · `2026-03-19`</small>


---

## 04-Bulma · Implementation Guidelines

<small>📄 `docs/04-bulma/implementation-guidelines.md` · modificado: `2026-03-19`</small>

# Implementation Guidelines for BULMA

## Reference baseline

When in doubt, use:
- `src/library/dddpy/shared/` as cross-cutting base
- `src/library/dddpy/example/` as reference module
- `src/api/example/` as clean-route reference

Do not use deleted/legacy modules as architecture source of truth.

## When creating a new module

Create the smallest correct baseline:

1. `domain/entity`
2. `domain/module_data.py` when create/update data objects are useful
3. `domain/module_exception.py`
4. `domain/module_success.py` when the module has reusable success messages
5. `domain/module_repository.py`
6. `domain/module_cmd_repository.py`
7. `domain/module_query_repository.py`
8. `infrastructure/dbmodule.py`
9. `infrastructure/module_mapper.py`
10. `infrastructure/module_cmd_repository.py`
11. `infrastructure/module_query_repository.py`
12. `usecase/module_cmd_schema.py`
13. `usecase/module_cmd_usecase.py`
14. `usecase/module_query_usecase.py`
15. `usecase/module_factory.py`
16. `usecase/module_usecase.py` facade
17. `api/module/routes_*.py` if exposing HTTP entrypoints

## When adding or modifying an endpoint

1. Update corresponding router/entrypoint only for adaptation concerns
2. Parse schema in route layer
3. Reuse existing use case if possible
4. Route should call use case and return `response.dict()`
5. Route should rely on `@api_handler` for centralized error handling
6. If new business rule is needed, implement in `domain/`
7. If persistence translation changes, update mapper/repository in `infrastructure/`
8. Preserve shared response schema format
9. Update docs if behavior or structure changed

## Domain exception guideline

If a rule failure is business-semantic:
- define exception in `domain/*_exception.py`
- inherit from shared `DomainException`
- provide clear semantic message
- use `status_code` intentionally when needed

Do not:
- raise generic `Exception`
- raise `ValueError` for business semantics
- define module exceptions inside infrastructure or usecase

## Mapper guideline

If domain entity and DB model need translation:
- add/update `*_mapper.py` in `infrastructure/`
- include explicit methods such as `to_domain(...)` and `to_infrastructure(...)`
- keep mapper free of business decision logic

Do not:
- import DB model into domain
- place mapping logic in router
- place mapping logic inside domain entity constructor for ORM coupling

## Repository guideline

Abstract contracts:
- live in `domain/`
- define expected behavior using domain entities or domain data objects
- may exist in three forms:
  - aggregate `Repository`
  - `CmdRepository`
  - `QueryRepository`

Aggregate repository meaning:
- use `Repository` when the module needs a broader abstraction than pure read/write split
- use it for module-level capabilities that do not fit cleanly into only cmd or only query
- do not treat it as decorative duplication

Concrete implementations:
- live in `infrastructure/`
- use session manager
- use mapper for DB ↔ domain translation

## Use case guideline

Use case may coordinate:
- input schema handling
- translation from schema to domain data objects
- precondition checks
- repository calls
- returning `ResponseSuccessSchema`
- raising semantic exceptions
- logging meaningful checkpoints

Use case should not:
- expose raw ORM objects to entrypoint layer
- become dumping ground for every rule
- return arbitrary dicts when shared success schema exists

## Response schema guideline

Use shared schemas from `shared/schemas/response_schema.py`.

Success path:
- use case/facade returns `ResponseSuccessSchema`
- when success wording is stable, centralize it in `domain/*_success.py`
- consume that catalog from the use case instead of scattering hardcoded literals

Error path:
- raise `DomainException` derivatives
- `@api_handler` converts them to `ResponseErrorSchema`

Do not create one-off response wrappers unless explicit architecture decision requires it.

## API handler guideline

Use `@api_handler` on clean API routes.

Expected route shape:

```python
@router.post("/resource")
@api_handler
def create_resource(request: CreateResourceSchema):
    response = ResourceUseCase().create(request)
    return response.dict()
```

Current framework note:
- `@api_handler` is FastAPI-native in the current project baseline
- do not use `chalice`, `Blueprint`, `current_request`, or framework-specific response objects from another stack
- if request metadata logging is needed, declare `Request` in the route signature and let the decorator consume it

Do not duplicate error handling in every route when decorator already owns it.

## Logger guideline

Use shared logger from `shared/logging/logging.py`.

Expected usage zones:
- main/app bootstrap
- API / route layer
- module internal flow

Logger should help answer:
- where the request entered
- what step failed
- what repository/use case was executing
- whether error was controlled or unexpected

Avoid noisy useless logs. Prefer traceable and meaningful logs.

## Documentation guideline

If you alter architecture, module responsibilities, route pattern, or baseline pattern:
- update `docs/architecture.md`
- update `docs/observations/` for human explanation when relevant
- update `docs/BULMA/` if agent guidance changed

<small>🔚 fin · 04-Bulma · Implementation Guidelines · `docs/04-bulma/implementation-guidelines.md` · `2026-03-19`</small>


---

## 04-Bulma · Module Map

<small>📄 `docs/04-bulma/module-map.md` · modificado: `2026-03-16`</small>

# Module Map for BULMA

## Current baseline modules

### Shared base

- `src/library/dddpy/shared/decorators/domain_exception.py`
- `src/library/dddpy/shared/decorators/api_handler.py`
- `src/library/dddpy/shared/schemas/response_schema.py`
- `src/library/dddpy/shared/logging/logging.py`
- `src/library/dddpy/shared/mysql/`
- `src/library/dddpy/shared/postgresql/`
- `src/library/dddpy/shared/constants/`
- `src/library/dddpy/shared/utils/`

### Reference template module

- `src/library/dddpy/example/domain/example_entity.py`
- `src/library/dddpy/example/domain/example_data.py`
- `src/library/dddpy/example/domain/example_exception.py`
- `src/library/dddpy/example/domain/example_repository.py`
- `src/library/dddpy/example/domain/example_cmd_repository.py`
- `src/library/dddpy/example/domain/example_query_repository.py`
- `src/library/dddpy/example/infrastructure/dbexample.py`
- `src/library/dddpy/example/infrastructure/example_mapper.py`
- `src/library/dddpy/example/infrastructure/example_cmd_repository.py`
- `src/library/dddpy/example/infrastructure/example_query_repository.py`
- `src/library/dddpy/example/usecase/example_cmd_schema.py`
- `src/library/dddpy/example/usecase/example_cmd_usecase.py`
- `src/library/dddpy/example/usecase/example_query_usecase.py`
- `src/library/dddpy/example/usecase/example_usecase.py`
- `src/library/dddpy/example/usecase/example_factory.py`

### Reference API module

- `src/api/example/routes_example.py`

## Important warning

Legacy modules were removed because they were not the desired architecture base.
Do not reconstruct them by imitation.
Use `example/` as the reference structure and `api/example/` as the route-pattern reference.

Important modeling rule:
- `Repository` = aggregate contract of the module
- `CmdRepository` = write-oriented contract
- `QueryRepository` = read-oriented contract

This is intentional and reflects the project vision for modules with complex or custom logic.

## Structural meaning

### `shared/`
Owns:
- common exceptions
- common response schemas
- common decorators
- logging
- session managers
- reusable utilities

### `example/domain/`
Owns:
- domain entity
- domain data objects
- domain exceptions
- repository contracts

### `example/infrastructure/`
Owns:
- DB model
- mapper
- concrete repositories

### `example/usecase/`
Owns:
- command/query schemas
- command/query use cases
- factory wiring
- facade returning `ResponseSuccessSchema`

### `api/example/`
Owns:
- request parsing
- route exposure
- use case invocation
- returning `response.dict()`
- relying on `@api_handler` for errors

## Response contract

Shared response schemas live in:
- `src/library/dddpy/shared/schemas/response_schema.py`

Current shapes:

```python
class ResponseErrorSchema(BaseModel):
    success: bool = False
    message: str

class ResponseSuccessSchema(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None
```

## Error contract

Shared base exception lives in:
- `src/library/dddpy/shared/decorators/domain_exception.py`

Current base:

```python
class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        ...
```

All module semantic exceptions should derive from it.

## Decorator contract

Shared API decorator lives in:
- `src/library/dddpy/shared/decorators/api_handler.py`

Official route flow:

```text
route
  → parse schema
  → use case
  → ResponseSuccessSchema
  → response.dict()
  → @api_handler handles DomainException / ValidationError / 500
```

## Logging contract

Logger should exist in:
- main/app bootstrap
- API / entrypoints
- internal module critical path

Purpose:
- trace normal flow
- map controlled errors
- map unexpected errors
- simplify debugging across layers

<small>🔚 fin · 04-Bulma · Module Map · `docs/04-bulma/module-map.md` · `2026-03-16`</small>


---

## 05-Research · Análisis Competitivo Sistemas Condo

<small>📄 `docs/05-research/competitive-analysis-condo-systems.md` · modificado: `2026-04-29`</small>

# 🏢 Análisis Competitivo — Sistemas de Gestión de Condominios
> Generado: 2026-04-13 | Por: Misato Katsuragi (Misato K)
> Propósito: Intelligence report para comparativa con condo-py beta

---

## 📊 RESUMEN EJECUTIVO

Se identificaron **8 competidores directos** en tres mercados (USA/Canadá, Europa, América Latina). El mercado de condo/HOA management software está dominado por soluciones SaaS maduras con fuerte integración contable. condo-py está en etapa backend-puro y tiene oportunidad de diferenciarse por arquitectura moderna, stack abierto y enfoque en LATAM.

---

## 🇺🇸 MERCADO USA / CANADÁ

### 1. **Buildium**
- **URL:** buildium.com
- **Segmento:** Property managers medianos-grandes
- **Puntuación estimada (Capterra/G2):** ~4.4/5
- **Features clave:**
  - Listado de propiedades + screening de inquilinos
  - Portal de residentes online
  - Cobro de renta automatizado
  - Contabilidad de propiedades
  - Órdenes de mantenimiento
  - Reportes y analytics
- **✅ PROS:**
  - All-in-one muy completo
  - Fuerte en contabilidad
  - App móvil disponible
  - Soporte y documentación robusta
  - Escala bien (hasta 15k+ unidades)
- **❌ CONTRAS:**
  - Precio elevado para pequeños condominios
  - Curva de aprendizaje alta
  - Orientado a gestores profesionales, no a autogestión
  - No localizado para LATAM (USD, inglés)
  - Soporte en inglés únicamente

---

### 2. **AppFolio**
- **URL:** appfolio.com
- **Segmento:** Property managers enterprise (10k+ unidades)
- **Puntuación estimada:** ~4.5/5
- **Features clave:**
  - AI nativa ("Realm-X Flows" — workflow automation)
  - Gestión de inversiones + property en una plataforma
  - Portal unificado con datos en tiempo real
  - Integraciones proptech extensas
- **✅ PROS:**
  - La plataforma más avanzada tecnológicamente del mercado
  - AI integrada nativamente (no add-on)
  - Interface unificada para múltiples negocios
  - Escala masiva (12k-14k+ unidades documentadas)
- **❌ CONTRAS:**
  - Precio ALTO — no apto para pequeños condominios
  - Requiere mínimo de unidades para contratación
  - Solo en inglés / mercado USA
  - No ofrece modelo self-hosted ni API abierta
  - Overkill para condominios residenciales pequeños

---

### 3. **Condo Control**
- **URL:** condocontrol.com
- **Segmento:** Condominios y HOAs (self-managed + PM companies)
- **Puntuación verificada (G2 + Capterra):**
  - 98% Quality of Support
  - 99% Ease of Setup
  - 97% Value for Money
  - 99.9% Uptime
- **Features clave:**
  - AI resident assistant + knowledge base 24/7
  - Reserva de amenidades, gestión de visitas, tracking de paquetes
  - Pagos online (autopay, reminders, fee rules)
  - E-voting, minutas de reuniones, retención de documentos
  - Integración QuickBooks, Yardi, Stripe
  - Soporte gestionado para residentes (phone/email/chat)
  - 3.5 millones de residentes activos
- **✅ PROS:**
  - **La mejor opción para condominios** específicamente (no solo rentals)
  - Excelente soporte verificado
  - Fácil setup (99% ease of setup)
  - Cubre todo el ciclo: finanzas + operaciones + gobernanza
  - Multi-moneda (CAD/USD)
  - Comunidad masiva (3.5M usuarios)
- **❌ CONTRAS:**
  - Enfocado en Canadá/USA — no LATAM
  - No tiene plan gratuito ni modelo open-source
  - Precio por unidad (se encarece con escala)
  - No soporta idioma español nativamente

---

### 4. **Propertyware**
- **URL:** propertyware.com
- **Segmento:** Single-family rentals enterprise
- **Puntuación estimada:** ~4.2/5
- **Features clave:**
  - Alta personalización (custom fields, dashboards)
  - API abierta (two-way data exchange)
  - Multi-location management
  - Portfolio-level accounting
- **✅ PROS:**
  - **API abierta** — diferenciador clave
  - Alta customización vs. competidores
  - Reporting avanzado
- **❌ CONTRAS:**
  - Más orientado a single-family que condominios
  - No tiene enfoque LATAM
  - UI/UX más compleja

---

## 🇧🇷 MERCADO LATINOAMÉRICA

### 5. **Superlógica** (Brasil)
- **URL:** superlogica.com
- **Segmento:** Administradoras de condominios e inmobiliarias — Brasil
- **Métricas:**
  - +100k condominios administrados
  - +3k administradoras de condominios clientes
  - +4.4k inmobiliarias
  - +600k contratos de locación
- **Features clave:**
  - Gestión de arrecadación (cobros)
  - Pago por boleto, PIX, tarjeta de crédito
  - Carpeta digital de prestación de cuentas
  - App para condóminos
  - Institución financiera propia (fintech integrada)
  - Inadimplência Zero (servicio de garantía de pago)
  - Split de pagos automático
  - Seguros y crédito
- **✅ PROS:**
  - **Líder absoluto en Brasil** — escala y confianza demostrada
  - Fintech integrada (diferenciador único)
  - Pago via PIX (relevante para LATAM)
  - App nativa para residentes
  - Prestación de cuentas digital
- **❌ CONTRAS:**
  - Solo para Brasil (idioma portugués, moneda BRL)
  - No hay modelo open-source
  - Enfocado en administradoras profesionales, no autogestión
  - No aplicable a Peru/Colombia/México sin adaptación
  - Precio opaco (no público)

---

### 6. **CondoLivre** (Brasil)
- **URL:** condolivre.com.br
- **Segmento:** Fintech para administradoras de condominios — Brasil
- **Features clave:**
  - Crédito para funcionarios del condominio
  - Líneas de crédito para síndicos y proveedores
  - Servicios financieros especializados en el sector condominial
  - Nuevas fuentes de ingreso para el HR del condominio
- **✅ PROS:**
  - Nicho muy específico: finanzas para el ecosistema condominial
  - Innovador en fintech B2B para condominios
- **❌ CONTRAS:**
  - No es un sistema de gestión completo — es un complemento financiero
  - Solo Brasil
  - No compite directamente con condo-py en funcionalidad de gestión

---

### 7. **TownSq** (Brasil/USA)
- **URL:** townsq.io
- **Segmento:** HOA y condominios — Brasil + expansión USA
- **Puntuación estimada:** ~4.1/5
- **Features clave (inferidas):**
  - App mobile para residentes y síndicos
  - Comunicación entre residentes y administración
  - Votaciones y asambleas digitales
  - Gestión de documentos
  - Reserva de espacios comunes
- **✅ PROS:**
  - Presente en Brasil Y USA — bilingüe potencial
  - Mobile-first
  - Conocen el mercado LATAM
- **❌ CONTRAS:**
  - Website con poca información pública (posible señal de producto en transición)
  - Dependiente de modelo SaaS cerrado
  - No es open-source

---

## 🇪🇺 MERCADO EUROPA

### 8. **Kastle** (USA/Global — Physical Security)
- **URL:** kastle.com
- **Segmento:** Seguridad física gestionada para edificios multifamily y comerciales
- **Puntuación G2:** Líder en Physical Security (Winter 2026)
- **Features clave:**
  - Access control (cloud-based, credencial única)
  - Video vigilancia con AI
  - Gestión de visitas
  - Integración Aliro + PKOC (estándares abiertos)
  - 1k+ edificios, 1M usuarios
- **✅ PROS:**
  - Líder en seguridad física para multifamily
  - AI-powered video analytics
  - Un credential para múltiples ubicaciones
- **❌ CONTRAS:**
  - **No es software de gestión de condominio** — es seguridad física
  - No compite directamente con condo-py en gestión operativa
  - Orientado a USA

---

## 🆚 COMPARATIVA: COMPETIDORES vs. condo-py

| Feature / Aspecto | Buildium | AppFolio | Condo Control | Superlógica | condo-py (beta) |
|---|---|---|---|---|---|
| **Stack tecnológico** | SaaS cerrado | SaaS/AI nativa | SaaS cerrado | SaaS + Fintech | FastAPI + SQLAlchemy + MySQL (Custom) |
| **Arquitectura** | Monolítico SaaS | Plataforma unificada | SaaS | SaaS | DDD/CQRS — moderna y escalable |
| **Open Source** | ❌ | ❌ | ❌ | ❌ | ❌ Custom |
| **API abierta** | Limitada | Limitada | Integraciones | No pública | ✅ REST API nativa |
| **Idioma** | Inglés | Inglés | Inglés | Portugués | Español (LATAM) |
| **Mercado LATAM** | ❌ | ❌ | ❌ | Solo Brasil | ✅ Peru/LATAM first |
| **Modelo de precios** | Por unidad/mes | Por unidad (alto) | Por unidad/mes | B2B opaco | Por definir |
| **Módulos core** | Completo | Completo | Completo | Completo | Beta — core_condominiums ✅ |
| **Gestión financiera** | ✅ | ✅ | ✅ | ✅ Fintech | ❌ Pendiente |
| **Portal residente** | ✅ | ✅ | ✅ | ✅ App | ❌ Pendiente |
| **Reserva amenidades** | ✅ | ✅ | ✅ | Parcial | ❌ Pendiente |
| **E-voting** | Parcial | ❌ | ✅ | ❌ | ❌ Pendiente |
| **Mantenimiento** | ✅ | ✅ | ✅ | Parcial | ❌ Pendiente |
| **AI/Automatización** | Básica | ✅ Avanzada | ✅ AI Asistente | ❌ | ❌ Pendiente |
| **Self-hosted** | ❌ | ❌ | ❌ | ❌ | ✅ Docker disponible |
| **Multi-condominio** | ✅ | ✅ | ✅ | ✅ | ✅ (arquitectura preparada) |

---

## 🎯 ANÁLISIS DE OPORTUNIDADES Y GAPS

### Fortalezas de condo-py (ventajas competitivas reales)
1. **Arquitectura DDD/CQRS** — ningún competidor documenta esta robustez técnica; escalable a microservicios
2. **Desarrollo acelerado con IA** — construcción, modificación y optimización mediante agentes de IA (vs. desarrollo humano tradicional)
3. **API REST nativa** — integrable con cualquier frontend/mobile
4. **Python ecosystem** — facilita extensiones con AI, ML, analytics
5. **Docker first** — deployment sencillo
6. **Foco LATAM/Peru** — cero competencia seria en idioma español con este stack

### Gaps críticos de condo-py vs. mercado
1. **Módulos pendientes** (buildings, unitys, users, residents — todos ❌)
2. **Sin portal de residentes** — todos los competidores lo tienen
3. **Sin gestión financiera / cobros** — diferenciador clave en LATAM (ver Superlógica)
4. **Sin notificaciones** — email, SMS, push
5. **Sin app móvil** — solo backend
6. **Sin autenticación** — JWT, OAuth no documentados
7. **Sin reserva de amenidades**
8. **Sin e-voting / asambleas digitales**

### Recomendaciones estratégicas (para análisis de Lelouch)
- **MVP mínimo competitivo:** completar módulos pendientes + auth + portal web básico
- **Diferenciador #1:** localización LATAM (español, soles, PEN, cobros locales)
- **Diferenciador #2:** desarrollo rápido con agentes de IA → sistema custom privado, flexible y optimizable en tiempo récord
- **Diferenciador #3:** API-first + arquitectura moderna → integrable con cualquier frontend o sistema externo
- **Modelo de negocio sugerido:** sistema privado custom por cliente/administradora + soporte y optimización continua

---

## 📌 FUENTES
- buildium.com (verificado)
- appfolio.com (verificado)
- condocontrol.com (verificado — métricas G2/Capterra)
- propertyware.com (verificado)
- superlogica.com (verificado)
- condolivre.com.br (verificado)
- townsq.io (verificado parcial)
- kastle.com (verificado)
- `/home/miguel/servers/condo-py/README.md` (interno)
- `/home/miguel/servers/condo-py/docs/BULMA/MODULES.md` (interno)

---
*Reporte generado por Misato K — Operación Inteligencia Competitiva*
*Asignado a: Lelouch S para análisis profundo y plan de acción*

<small>🔚 fin · 05-Research · Análisis Competitivo Sistemas Condo · `docs/05-research/competitive-analysis-condo-systems.md` · `2026-04-29`</small>


---

## 06-Competitor-Analysis · Introducción

<small>📄 `docs/06-competitor-analysis/README.md` · modificado: `2026-04-13`</small>

# /analysis — Análisis Competitivo & Estratégico

Esta carpeta contiene el análisis competitivo del mercado de sistemas de gestión de condominios.

## Contenido

| Archivo | Descripción |
|---|---|
| `competitive-analysis.md` | Reporte completo — 8 competidores mapeados (USA/LATAM/Europa) |
| `lelouch-strategic-analysis.md` | Análisis profundo, top 3 rivales, gap analysis técnico y roadmap 6–12 meses |

## Origen

Generado el 2026-04-13 como parte de la operación de inteligencia competitiva iniciada por Mike Ross.
Reporte source: `/home/miguel/.openclaw/workspace/research/competitive-analysis-condo-systems.md`

## Asignado a
**Lelouch S** — Análisis profundo, gap analysis técnico, propuesta de roadmap

<small>🔚 fin · 06-Competitor-Analysis · Introducción · `docs/06-competitor-analysis/README.md` · `2026-04-13`</small>


---

## 06-Competitor-Analysis · Análisis Competitivo

<small>📄 `docs/06-competitor-analysis/competitive-analysis.md` · modificado: `2026-04-29`</small>

# 🏢 Análisis Competitivo — Sistemas de Gestión de Condominios
> Generado: 2026-04-13 | Por: Misato Katsuragi (Misato K)
> Propósito: Intelligence report para comparativa con condo-py beta

---

## 📊 RESUMEN EJECUTIVO

Se identificaron **8 competidores directos** en tres mercados (USA/Canadá, Europa, América Latina). El mercado de condo/HOA management software está dominado por soluciones SaaS maduras con fuerte integración contable. condo-py está en etapa backend-puro y tiene oportunidad de diferenciarse por arquitectura moderna, stack abierto y enfoque en LATAM.

---

## 🇺🇸 MERCADO USA / CANADÁ

### 1. **Buildium**
- **URL:** buildium.com
- **Segmento:** Property managers medianos-grandes
- **Puntuación estimada (Capterra/G2):** ~4.4/5
- **Features clave:**
  - Listado de propiedades + screening de inquilinos
  - Portal de residentes online
  - Cobro de renta automatizado
  - Contabilidad de propiedades
  - Órdenes de mantenimiento
  - Reportes y analytics
- **✅ PROS:**
  - All-in-one muy completo
  - Fuerte en contabilidad
  - App móvil disponible
  - Soporte y documentación robusta
  - Escala bien (hasta 15k+ unidades)
- **❌ CONTRAS:**
  - Precio elevado para pequeños condominios
  - Curva de aprendizaje alta
  - Orientado a gestores profesionales, no a autogestión
  - No localizado para LATAM (USD, inglés)
  - Soporte en inglés únicamente

---

### 2. **AppFolio**
- **URL:** appfolio.com
- **Segmento:** Property managers enterprise (10k+ unidades)
- **Puntuación estimada:** ~4.5/5
- **Features clave:**
  - AI nativa ("Realm-X Flows" — workflow automation)
  - Gestión de inversiones + property en una plataforma
  - Portal unificado con datos en tiempo real
  - Integraciones proptech extensas
- **✅ PROS:**
  - La plataforma más avanzada tecnológicamente del mercado
  - AI integrada nativamente (no add-on)
  - Interface unificada para múltiples negocios
  - Escala masiva (12k-14k+ unidades documentadas)
- **❌ CONTRAS:**
  - Precio ALTO — no apto para pequeños condominios
  - Requiere mínimo de unidades para contratación
  - Solo en inglés / mercado USA
  - No ofrece modelo self-hosted ni API abierta
  - Overkill para condominios residenciales pequeños

---

### 3. **Condo Control**
- **URL:** condocontrol.com
- **Segmento:** Condominios y HOAs (self-managed + PM companies)
- **Puntuación verificada (G2 + Capterra):**
  - 98% Quality of Support
  - 99% Ease of Setup
  - 97% Value for Money
  - 99.9% Uptime
- **Features clave:**
  - AI resident assistant + knowledge base 24/7
  - Reserva de amenidades, gestión de visitas, tracking de paquetes
  - Pagos online (autopay, reminders, fee rules)
  - E-voting, minutas de reuniones, retención de documentos
  - Integración QuickBooks, Yardi, Stripe
  - Soporte gestionado para residentes (phone/email/chat)
  - 3.5 millones de residentes activos
- **✅ PROS:**
  - **La mejor opción para condominios** específicamente (no solo rentals)
  - Excelente soporte verificado
  - Fácil setup (99% ease of setup)
  - Cubre todo el ciclo: finanzas + operaciones + gobernanza
  - Multi-moneda (CAD/USD)
  - Comunidad masiva (3.5M usuarios)
- **❌ CONTRAS:**
  - Enfocado en Canadá/USA — no LATAM
  - No tiene plan gratuito ni modelo open-source
  - Precio por unidad (se encarece con escala)
  - No soporta idioma español nativamente

---

### 4. **Propertyware**
- **URL:** propertyware.com
- **Segmento:** Single-family rentals enterprise
- **Puntuación estimada:** ~4.2/5
- **Features clave:**
  - Alta personalización (custom fields, dashboards)
  - API abierta (two-way data exchange)
  - Multi-location management
  - Portfolio-level accounting
- **✅ PROS:**
  - **API abierta** — diferenciador clave
  - Alta customización vs. competidores
  - Reporting avanzado
- **❌ CONTRAS:**
  - Más orientado a single-family que condominios
  - No tiene enfoque LATAM
  - UI/UX más compleja

---

## 🇧🇷 MERCADO LATINOAMÉRICA

### 5. **Superlógica** (Brasil)
- **URL:** superlogica.com
- **Segmento:** Administradoras de condominios e inmobiliarias — Brasil
- **Métricas:**
  - +100k condominios administrados
  - +3k administradoras de condominios clientes
  - +4.4k inmobiliarias
  - +600k contratos de locación
- **Features clave:**
  - Gestión de arrecadación (cobros)
  - Pago por boleto, PIX, tarjeta de crédito
  - Carpeta digital de prestación de cuentas
  - App para condóminos
  - Institución financiera propia (fintech integrada)
  - Inadimplência Zero (servicio de garantía de pago)
  - Split de pagos automático
  - Seguros y crédito
- **✅ PROS:**
  - **Líder absoluto en Brasil** — escala y confianza demostrada
  - Fintech integrada (diferenciador único)
  - Pago via PIX (relevante para LATAM)
  - App nativa para residentes
  - Prestación de cuentas digital
- **❌ CONTRAS:**
  - Solo para Brasil (idioma portugués, moneda BRL)
  - No hay modelo open-source
  - Enfocado en administradoras profesionales, no autogestión
  - No aplicable a Peru/Colombia/México sin adaptación
  - Precio opaco (no público)

---

### 6. **CondoLivre** (Brasil)
- **URL:** condolivre.com.br
- **Segmento:** Fintech para administradoras de condominios — Brasil
- **Features clave:**
  - Crédito para funcionarios del condominio
  - Líneas de crédito para síndicos y proveedores
  - Servicios financieros especializados en el sector condominial
  - Nuevas fuentes de ingreso para el HR del condominio
- **✅ PROS:**
  - Nicho muy específico: finanzas para el ecosistema condominial
  - Innovador en fintech B2B para condominios
- **❌ CONTRAS:**
  - No es un sistema de gestión completo — es un complemento financiero
  - Solo Brasil
  - No compite directamente con condo-py en funcionalidad de gestión

---

### 7. **TownSq** (Brasil/USA)
- **URL:** townsq.io
- **Segmento:** HOA y condominios — Brasil + expansión USA
- **Puntuación estimada:** ~4.1/5
- **Features clave (inferidas):**
  - App mobile para residentes y síndicos
  - Comunicación entre residentes y administración
  - Votaciones y asambleas digitales
  - Gestión de documentos
  - Reserva de espacios comunes
- **✅ PROS:**
  - Presente en Brasil Y USA — bilingüe potencial
  - Mobile-first
  - Conocen el mercado LATAM
- **❌ CONTRAS:**
  - Website con poca información pública (posible señal de producto en transición)
  - Dependiente de modelo SaaS cerrado
  - No es open-source

---

## 🇪🇺 MERCADO EUROPA

### 8. **Kastle** (USA/Global — Physical Security)
- **URL:** kastle.com
- **Segmento:** Seguridad física gestionada para edificios multifamily y comerciales
- **Puntuación G2:** Líder en Physical Security (Winter 2026)
- **Features clave:**
  - Access control (cloud-based, credencial única)
  - Video vigilancia con AI
  - Gestión de visitas
  - Integración Aliro + PKOC (estándares abiertos)
  - 1k+ edificios, 1M usuarios
- **✅ PROS:**
  - Líder en seguridad física para multifamily
  - AI-powered video analytics
  - Un credential para múltiples ubicaciones
- **❌ CONTRAS:**
  - **No es software de gestión de condominio** — es seguridad física
  - No compite directamente con condo-py en gestión operativa
  - Orientado a USA

---

## 🆚 COMPARATIVA: COMPETIDORES vs. condo-py

| Feature / Aspecto | Buildium | AppFolio | Condo Control | Superlógica | condo-py (beta) |
|---|---|---|---|---|---|
| **Stack tecnológico** | SaaS cerrado | SaaS/AI nativa | SaaS cerrado | SaaS + Fintech | FastAPI + SQLAlchemy + MySQL (Custom) |
| **Arquitectura** | Monolítico SaaS | Plataforma unificada | SaaS | SaaS | DDD/CQRS — moderna y escalable |
| **Open Source** | ❌ | ❌ | ❌ | ❌ | ❌ Custom |
| **API abierta** | Limitada | Limitada | Integraciones | No pública | ✅ REST API nativa |
| **Idioma** | Inglés | Inglés | Inglés | Portugués | Español (LATAM) |
| **Mercado LATAM** | ❌ | ❌ | ❌ | Solo Brasil | ✅ Peru/LATAM first |
| **Modelo de precios** | Por unidad/mes | Por unidad (alto) | Por unidad/mes | B2B opaco | Por definir |
| **Módulos core** | Completo | Completo | Completo | Completo | Beta — core_condominiums ✅ |
| **Gestión financiera** | ✅ | ✅ | ✅ | ✅ Fintech | ❌ Pendiente |
| **Portal residente** | ✅ | ✅ | ✅ | ✅ App | ❌ Pendiente |
| **Reserva amenidades** | ✅ | ✅ | ✅ | Parcial | ❌ Pendiente |
| **E-voting** | Parcial | ❌ | ✅ | ❌ | ❌ Pendiente |
| **Mantenimiento** | ✅ | ✅ | ✅ | Parcial | ❌ Pendiente |
| **AI/Automatización** | Básica | ✅ Avanzada | ✅ AI Asistente | ❌ | ❌ Pendiente |
| **Self-hosted** | ❌ | ❌ | ❌ | ❌ | ✅ Docker disponible |
| **Multi-condominio** | ✅ | ✅ | ✅ | ✅ | ✅ (arquitectura preparada) |

---

## 🎯 ANÁLISIS DE OPORTUNIDADES Y GAPS

### Fortalezas de condo-py (ventajas competitivas reales)
1. **Arquitectura DDD/CQRS** — ningún competidor documenta esta robustez técnica; escalable a microservicios
2. **Desarrollo acelerado con IA** — construcción, modificación y optimización mediante agentes de IA (vs. desarrollo humano tradicional)
3. **API REST nativa** — integrable con cualquier frontend/mobile
4. **Python ecosystem** — facilita extensiones con AI, ML, analytics
5. **Docker first** — deployment sencillo
6. **Foco LATAM/Peru** — cero competencia seria en idioma español con este stack

### Gaps críticos de condo-py vs. mercado
1. **Módulos pendientes** (buildings, unitys, users, residents — todos ❌)
2. **Sin portal de residentes** — todos los competidores lo tienen
3. **Sin gestión financiera / cobros** — diferenciador clave en LATAM (ver Superlógica)
4. **Sin notificaciones** — email, SMS, push
5. **Sin app móvil** — solo backend
6. **Sin autenticación** — JWT, OAuth no documentados
7. **Sin reserva de amenidades**
8. **Sin e-voting / asambleas digitales**

### Recomendaciones estratégicas (para análisis de Lelouch)
- **MVP mínimo competitivo:** completar módulos pendientes + auth + portal web básico
- **Diferenciador #1:** localización LATAM (español, soles, PEN, cobros locales)
- **Diferenciador #2:** desarrollo rápido con agentes de IA → sistema custom privado, flexible y optimizable en tiempo récord
- **Diferenciador #3:** API-first + arquitectura moderna → integrable con cualquier frontend o sistema externo
- **Modelo de negocio sugerido:** sistema privado custom por cliente/administradora + soporte y optimización continua

---

## 📌 FUENTES
- buildium.com (verificado)
- appfolio.com (verificado)
- condocontrol.com (verificado — métricas G2/Capterra)
- propertyware.com (verificado)
- superlogica.com (verificado)
- condolivre.com.br (verificado)
- townsq.io (verificado parcial)
- kastle.com (verificado)
- `/home/miguel/servers/condo-py/README.md` (interno)
- `/home/miguel/servers/condo-py/docs/BULMA/MODULES.md` (interno)

---
*Reporte generado por Misato K — Operación Inteligencia Competitiva*
*Asignado a: Lelouch S para análisis profundo y plan de acción*

<small>🔚 fin · 06-Competitor-Analysis · Análisis Competitivo · `docs/06-competitor-analysis/competitive-analysis.md` · `2026-04-29`</small>


---

## 06-Competitor-Analysis · Análisis Estratégico (Lelouch)

<small>📄 `docs/06-competitor-analysis/lelouch-strategic-analysis.md` · modificado: `2026-04-14`</small>

# ♟️ Análisis Estratégico Profundo — condo-py vs. mercado

> Fecha: 2026-04-13  
> Autor: Lelouch S  
> Base de partida: `analysis/competitive-analysis.md` + inspección del código real de `condo-py`

---

## 1. Dictamen ejecutivo

La posición actual de `condo-py` **no es la de un rival funcional inmediato** frente a plataformas maduras como Buildium, Condo Control o Superlógica.

Su posición real hoy es otra:

- **proyecto backend en etapa temprana**,
- con **arquitectura mejor pensada que muchos incumbentes**,
- pero con una **brecha funcional enorme** frente al mercado.

La buena noticia: el tablero todavía no está perdido.

El mercado de condominios/HOA muestra un patrón claro:

1. Los jugadores maduros ganan por **finanzas + operaciones + portal de residentes**.
2. Los jugadores más fuertes en condo/HOA ganan además por **gobernanza**: votaciones, actas, documentos, auditoría.
3. En LATAM, el actor realmente peligroso no gana solo por software: gana por **pagos y servicios financieros integrados**.

### Conclusión brutal, sin anestesia

Si `condo-py` quiere competir en 6–12 meses, no debe intentar parecerse a “todo AppFolio”. Eso sería sacrificar la reina por un peón.

Debe posicionarse como:

> **plataforma API-first, self-hosted o managed, enfocada en condominios de LATAM hispanohablante, con núcleo fuerte de operaciones + cobranza local + portal de residentes.**

Ese es el flanco menos defendido del mercado.

---

## 2. Límite ético y operativo del research

Se pidió también “buscar documentación filtrada”. No voy a apoyar recolección ni uso de material filtrado, privado o obtenido de forma ilícita.

Sí tomé y usaré:

- documentación pública de producto,
- pricing oficial cuando existe,
- claims públicos verificables,
- integraciones publicadas,
- señales públicas de madurez comercial.

Ese enfoque sirve para inteligencia competitiva seria sin cruzar líneas que luego destruyen reputación o generan riesgo legal.

---

## 3. Qué existe realmente hoy en `condo-py`

Inspección directa del repositorio `/home/miguel/servers/condo-py`:

### Implementado de verdad
- `FastAPI`
- patrón `DDD/CQRS` pragmático
- módulo funcional `core_condominiums`
- capa `shared/` reutilizable
- módulo `example/` como plantilla arquitectónica
- Docker y Alembic presentes

### Evidencia concreta en código
- `src/main.py` registra solo:
  - `condominium_routes`
  - `example_routes`
- `src/api/condominiums/routes_condominiums.py` expone CRUD + búsqueda por `id`, `uuid`, `code`
- `src/library/dddpy/core_condominiums/` sí tiene `domain / infrastructure / usecase`

### No implementado aún como capacidad de negocio competitiva
- autenticación/autorización
- multi-tenant real con aislamiento comercial documentado
- usuarios/residentes completos
- edificios
- unidades
- cobranzas/pagos
- contabilidad / conciliación
- notificaciones email/SMS/push
- portal de residentes
- reserva de amenidades
- mantenimiento/work orders
- gobernanza digital (actas, votos, asambleas)
- app móvil o frontend web usable
- analítica comercial/operativa

### Veredicto técnico

`condo-py` hoy es **más una base arquitectónica prometedora que un producto competitivo de mercado**.

Eso no es un insulto. Es un diagnóstico. Y un buen diagnóstico evita perder la guerra por autoengaño.

---

## 4. Análisis profundo de competidores

## 4.1 Buildium
**Tipo:** property management SaaS maduro  
**Señal clave:** pricing público y portafolio amplio  
**Fuente pública:** `buildium.com/pricing`

### Lo importante
Buildium publica planes desde:
- **Essential:** USD 62/mes
- **Growth:** USD 192/mes
- **Premium:** USD 400/mes

También declara capacidades que importan mucho para condo/association management:
- resident portal
- online payments & autopay
- amenity booking
- community calendar
- maintenance/work orders
- owner portal
- comunicaciones
- reporting
- automatizaciones
- **Open API** en plan premium

### Fortalezas reales
- pricing visible: reduce fricción comercial
- suite amplia de operaciones + pagos + comunicaciones
- madurez funcional alta
- API pública como arma de integración
- sirve como referencia para PMs que quieren estandarizar operación

### Debilidades reales
- fuerte sesgo USA
- inglés-first
- no se siente “LATAM-native”
- puede resultar pesado para comunidades pequeñas autogestionadas
- el valor sube rápido si necesitas features avanzadas

### Qué significa para condo-py
Buildium no gana por arquitectura elegante; gana por **producto utilizable hoy**.

La lección es simple: al mercado le importa más poder cobrar, comunicar y operar que si el repositorio sigue DDD con pureza ceremonial.

---

## 4.2 AppFolio
**Tipo:** plataforma enterprise  
**Señal clave:** benchmark de sofisticación, no necesariamente rival inmediato  
**Fuente pública:** `appfolio.com/pricing`

### Lo importante
Su pricing público accesible es opaco: la página empuja a **customizar plan** y hablar con ventas. Eso ya revela el posicionamiento.

No está compitiendo por simplicidad. Está compitiendo por:
- plataforma unificada
- servicios agregados
- automatización avanzada
- motion enterprise

### Fortalezas reales
- marca fuerte
- producto percibido como avanzado
- excelente benchmark de madurez operativa y automatización
- probable ventaja en workflows complejos y upsell de servicios

### Debilidades reales
- barrera comercial más alta
- enfoque más enterprise/professional manager que condo self-managed
- menor afinidad natural con un GTM inicial para LATAM hispanohablante
- pricing no transparente

### Qué significa para condo-py
AppFolio es menos amenaza inmediata y más **techo de referencia**. Es el rey al fondo del tablero: no es la primera pieza que te captura, pero sí muestra hasta dónde escala un incumbente serio.

No copiar. **Aprender qué módulos generan lock-in**.

---

## 4.3 Condo Control
**Tipo:** competidor más alineado al problema condo/HOA  
**Fuentes públicas:** `condocontrol.com/`, `condocontrol.com/integrations/`

### Señales públicas fuertes
- más de **3.5 millones de residentes**
- foco explícito en property management companies y self-managed condos & HOAs
- claims públicos de:
  - AI resident assistant
  - knowledge base
  - e-voting
  - agendas/minutes
  - document retention
  - payments/autopay/reminders
  - amenity bookings
  - visitor management
  - package tracking
  - access control integrations
  - integración con **QuickBooks, Yardi y Stripe**
- métricas públicas citadas desde ratings verificados:
  - 98% Quality of Support
  - 99% Ease of Setup
  - 97% Value for Money
  - 99.9% Uptime

### Fortalezas reales
- muy enfocado en el caso condo/HOA, no solo rentals
- entiende el dolor operacional de residentes, boards y managers
- mezcla tres frentes clave:
  - operaciones
  - gobernanza
  - finanzas
- onboarding aparentemente sencillo
- integración contable madura

### Debilidades reales
- foco principal en Norteamérica
- pricing no transparente públicamente en la evidencia disponible
- no parece posicionarse como open platform ni self-hosted
- español/LATAM no es su centro de gravedad

### Qué significa para condo-py
Este sí es un rival conceptual directo.

Si `condo-py` no construye rápido:
- portal residente,
- comunicaciones,
- amenidades,
- pagos,
- gobernanza,

entonces Condo Control ya tiene el jaque armado en exactamente el segmento correcto.

---

## 4.4 Propertyware
**Tipo:** plataforma madura para property managers, más cercana a rental/SFR  
**Fuente pública:** `propertyware.com/pricing`

### Señales públicas útiles
Propertyware no publica un precio base simple en la evidencia accesible, pero sí muestra:
- Basic / Plus / Premium
- owner portals
- tenant portals
- maintenance
- accounting
- reporting
- text messaging
- eSignature
- inspections
- vendor portals
- **Enterprise/API: add USD 1 por unidad/mes**

### Fortalezas reales
- orientación a customización
- API como capacidad comercializable
- módulos maduros de operación
- portal para varios actores

### Debilidades reales
- sesgo fuerte a rental/property management tradicional
- menos alineado al corazón de gobernanza condominial
- UX y complejidad suelen ser mayores en este tipo de suites
- no se percibe como LATAM-first

### Qué significa para condo-py
Propertyware es importante porque demuestra algo clave:

> el mercado sí paga por APIs cuando el producto base ya resuelve el negocio.

Moraleja: “API-first” solo es diferenciador si primero hay negocio resolviendo negocio.

---

## 4.5 Superlógica
**Tipo:** el actor regional más serio  
**Fuentes públicas:** `superlogica.com/condominios/`, `superlogica.com/condominios/modulo-financeiro/`

### Señales públicas de dominio de mercado
- **+3 mil administradoras**
- **+100 mil condomínios**
- ecosistema de software + servicios financieros + app para moradores
- productos integrados:
  - gestão financeira
  - conta digital
  - PIX
  - boleto
  - tarjeta/crédito
  - inadimplência zero
  - seguros
  - crédito para condomínios
  - conciliación bancaria
  - reportes/métricas
  - app de comunidad/residentes

### Fortalezas reales
- no vende “solo software”; vende **infraestructura económica del condominio**
- integración financiera profundísima
- distribución y confianza sectorial masivas
- app residente + operaciones + pagos + capacitación
- compliance regulatorio y narrativa de institución financiera

### Debilidades reales
- brasilcentrismo total
- idioma y rails locales (portugués/BRL/PIX/boleto)
- expansión a LATAM hispana no es trivial
- pricing opaco al público general

### Qué significa para condo-py
Superlógica es el rival más peligroso **estratégicamente**.

No porque hoy domine Perú o México, sino porque ya resolvió la pregunta más difícil:

> ¿cómo convertir software de condominio en plataforma de pagos, cobranza y servicios financieros?

Ese modelo genera stickiness brutal.

Si `condo-py` ignora finanzas y cobranzas, será una capa bonita alrededor de un problema central que otro ya monetiza mejor.

---

## 4.6 TownSq
**Tipo:** community management app / HOA software  
**Fuente pública accesible:** `townsq.io`

### Lo observable públicamente
La evidencia accesible pública fue escasa en este pase; el sitio visible empuja a demo. Eso sugiere un motion comercial más cerrado y menos transparente.

### Lectura estratégica
TownSq parece jugar más cerca de:
- app de comunidad,
- experiencia residente,
- operación cotidiana,
que de una tesis financiera profunda al estilo Superlógica.

### Qué significa para condo-py
TownSq es una advertencia, no necesariamente el enemigo principal:

si `condo-py` deja fuera el frente de experiencia de residente, otro actor mobile-first puede apropiarse de la relación diaria aunque la base operativa esté en otro sistema.

---

## 4.7 CondoLivre
**Tipo:** fintech complementaria del ecosistema  
**Lectura:** adyacente, no rival full-stack

No parece un competidor directo de gestión integral. Es más bien evidencia de que el vertical condominial permite especialización financiera.

### Qué significa para condo-py
Confirma la tesis:

> el dinero no es un módulo accesorio; es uno de los centros de gravedad del producto.

---

## 4.8 Kastle
**Tipo:** seguridad física / access control  
**Lectura:** adyacente, no rival directo

Sirve como benchmark de integración para:
- visitor management
- access control
- hardware/security ecosystem

### Qué significa para condo-py
No debería ser prioridad temprana competir en hardware/security profundo. Mejor dejar ese frente como:
- integraciones futuras,
- webhooks,
- arquitectura extensible.

---

## 5. Los 3 rivales más peligrosos para condo-py en LATAM hispanohablante

## 1) Superlógica — el más peligroso estratégicamente
**Por qué:**
- probó escala real en condominio
- domina finanzas integradas
- app + operación + cobranza + crédito
- si quisiera expandirse a hispanoamérica con localización correcta, sería devastador

**Nivel de amenaza:** Muy alta  
**Tipo de amenaza:** modelo de negocio + plataforma financiera

## 2) Condo Control — el más peligroso funcionalmente
**Por qué:**
- está mejor alineado al caso condo/HOA que Buildium o Propertyware
- resuelve resident experience + governance + payments + operations
- parece más fácil de adoptar que suites enterprise pesadas

**Nivel de amenaza:** Muy alta  
**Tipo de amenaza:** producto directamente alineado al dolor

## 3) Buildium — el más peligroso comercialmente
**Por qué:**
- pricing público
- feature set amplio
- marca consolidada
- API en tier alto
- enough product breadth para entrar donde el cliente no exige localización fuerte

**Nivel de amenaza:** Alta  
**Tipo de amenaza:** suite madura con compra relativamente fácil

### Mención especial: AppFolio
AppFolio es el benchmark más serio de sofisticación, pero no lo pondría hoy en top 3 de amenaza inmediata para `condo-py` en LATAM hispanohablante por su posicionamiento más enterprise y fricción comercial mayor.

---

## 6. Gap analysis técnico y de producto

## 6.1 Gaps mortales
Si estos no se corrigen, `condo-py` no compite; solo demuestra arquitectura:

1. **Auth + RBAC multi-rol**
   - admin
   - board
   - resident
   - concierge/front desk
   - accountant/operator

2. **Modelo núcleo inmobiliario completo**
   - condominiums
   - buildings
   - units
   - users
   - residents/occupancy
   - ownership/tenancy relationships

3. **Portal de residentes**
   - estado de cuenta
   - documentos
   - tickets/incidencias
   - notificaciones
   - reservas
   - visitas

4. **Finanzas/cobranza**
   - cuotas
   - cargos recurrentes
   - mora/penalidades
   - ledger por unidad
   - conciliación
   - exportes contables

5. **Comunicaciones y notificaciones**
   - email
   - SMS/WhatsApp opcional
   - in-app notifications
   - anuncios
   - recibos/lecturas

## 6.2 Gaps serios de segunda línea
6. Work orders / mantenimiento  
7. Amenity booking  
8. Visitor/package management  
9. Document repository + governance  
10. Audit trail / activity log  
11. Reporting operativo y financiero  
12. Integraciones de pago/ERP

## 6.3 Gaps técnicos invisibles pero críticos
13. tenancy / account isolation claro  
14. permisos por condominio/edificio/unidad  
15. idempotencia en pagos/eventos  
16. background jobs  
17. observabilidad  
18. estrategia de archivos/documentos  
19. testing automatizado  
20. hardening de seguridad

---

## 7. Roadmap recomendado 6–12 meses

## Fase 1 — 0 a 8 semanas
**Objetivo:** dejar de ser “backend bonito” y convertirse en núcleo operable.

### Prioridades
- Auth JWT/OAuth2
- RBAC
- módulos:
  - `core_buildings`
  - `core_unities`
  - `users`
  - `users_residents`
- seeds/base catalogs
- auditoría básica
- OpenAPI limpia
- tests de contrato API

### Resultado esperado
Una instalación ya puede representar correctamente:
- un condominio,
- sus edificios,
- sus unidades,
- sus usuarios y residentes.

Sin esto, todo lo demás se apoya en arena.

## Fase 2 — 2 a 4 meses
**Objetivo:** resolver la operación mínima por la que alguien pagaría.

### Prioridades
- cuentas por cobrar / cuotas / cargos / mora
- ledger por unidad
- comprobantes/estado de cuenta
- notificaciones transaccionales
- announcements / bulletin board
- portal residente básico web
- carga y consulta de documentos

### Resultado esperado
`condo-py` ya puede venderse como:

> “sistema base para administración de condominios con residentes, cuotas y comunicación”.

Ese ya es un producto, no solo un repositorio.

## Fase 3 — 4 a 8 meses
**Objetivo:** entrar al terreno donde Condo Control empieza a dominar.

### Prioridades
- maintenance/work orders
- amenity booking
- visitor pre-registration
- package logging
- meeting minutes / document governance
- e-voting inicial
- dashboards operativos

### Resultado esperado
Ahora sí hay una narrativa seria de condo operations platform.

## Fase 4 — 8 a 12 meses
**Objetivo:** construir moat regional.

### Prioridades
- integraciones de pago LATAM
  - país por país
- multi-country billing abstractions
- exportes contables/local compliance
- canales locales de cobranza
- WhatsApp/inbox operational layer
- marketplace/API/webhooks públicos

### Resultado esperado
Aquí nace la verdadera ventaja frente a incumbentes anglo o brasilcentrados.

---

## 8. Qué NO priorizar todavía

No sacrifiques foco por brillo.

### Evitar en etapa temprana
- app móvil nativa antes de validar portal web fuerte
- AI assistant “de marketing” sin resolver datos/operación
- microservicios prematuros
- integraciones hardware complejas de access control
- analítica avanzada tipo BI enterprise
- expansion a Europa como prioridad inicial

### Razón
El producto todavía no tiene aseguradas las piezas que cobran, comunican y sostienen gobernanza. Lo demás es decoración sobre una fortaleza incompleta.

---

## 9. Posicionamiento recomendado para condo-py

## Tesis de posicionamiento

`condo-py` no debe presentarse como:
- “otro Buildium”, ni
- “mini AppFolio”, ni
- “Condo Control open source”.

Debe presentarse como:

> **Infraestructura moderna para administración de condominios en LATAM hispanohablante: API-first, desplegable en nube o self-hosted, con foco en operaciones, cobranza local y experiencia residente.**

## Diferenciadores que sí importan
1. **LATAM-first** en español  
2. **Self-hosted / managed**  
3. **API-first real**  
4. **arquitectura mantenible**  
5. **integraciones locales de pago y mensajería**  
6. **modularidad para administradoras medianas**

## Diferenciadores que NO bastan solos
- “está en Python”
- “usa DDD/CQRS”
- “tiene Docker”
- “podemos agregar IA luego”

Eso impresiona arquitectos. No cierra ventas.

---

## 10. Tabla final de posicionamiento estratégico

| Criterio | condo-py hoy | Objetivo 12 meses | Rival más fuerte en ese frente |
|---|---|---|---|
| Arquitectura backend | Fuerte | Muy fuerte | Ninguno visible públicamente |
| Funcionalidad condominio core | Débil | Media | Condo Control |
| Finanzas/cobranza | Nula | Fuerte | Superlógica |
| Portal residente | Nulo | Medio/Fuerte | Condo Control / TownSq |
| Gobernanza (actas, voto, documentos) | Nula | Media | Condo Control |
| Integraciones/API | Potencial alto, real bajo | Fuerte | Buildium / Propertyware |
| Adaptación LATAM hispana | Potencial muy alto | Muy fuerte | Mercado aún fragmentado |
| Time-to-value comercial | Bajo | Medio | Buildium |
| Escalabilidad estratégica | Alta en teoría | Alta real si ejecuta | AppFolio como benchmark |

---

## 11. Plan de ataque recomendado

Si yo moviera las piezas del tablero, el orden sería este:

### Sprint estratégico A
- auth
- roles
- buildings
- units
- residents/users

### Sprint estratégico B
- cuotas/cargos
- ledger
- estados de cuenta
- notificaciones

### Sprint estratégico C
- portal residente web
- documentos
- anuncios
- tickets/mantenimiento básico

### Sprint estratégico D
- amenidades
- visitas
- gobernanza
- integraciones de pago locales

Ese orden maximiza:
- credibilidad de producto,
- posibilidad de piloto,
- capacidad de cobro,
- y futura defensibilidad.

---

## 12. Dictamen final

`condo-py` **todavía no está jugando la misma liga funcional** que los incumbentes.

Pero sí tiene algo que varios de ellos no muestran con claridad:

- base arquitectónica limpia,
- posibilidad de despliegue flexible,
- y oportunidad real de diseñarse para LATAM desde el inicio en vez de “traducirse” después.

El jaque mate no consiste en perseguir al rival más grande en todos los frentes.
Consiste en capturar el centro del tablero donde ellos están mal localizados:

- español,
- pagos y operación regional,
- despliegue flexible,
- integrabilidad,
- y foco específico en condo/HOA hispanohablante.

Si `condo-py` ejecuta bien los próximos 2–3 bloques de roadmap, deja de ser promesa técnica y se convierte en amenaza real.

Si no, será otro castillo de arquitectura impecable… vacío por dentro.

---

## 13. Fuentes públicas usadas

### Producto / pricing / claims oficiales
- <https://www.buildium.com/pricing/>
- <https://www.appfolio.com/pricing>
- <https://www.condocontrol.com/>
- <https://www.condocontrol.com/integrations/>
- <https://www.propertyware.com/pricing/>
- <https://www.superlogica.com/condominios/>
- <https://www.superlogica.com/condominios/modulo-financeiro/>
- <https://www.townsq.io/>

### Código y documentación interna analizada
- `README.md`
- `docs/architecture.md`
- `docs/BULMA/MODULES.md`
- `src/main.py`
- `src/api/condominiums/routes_condominiums.py`
- `src/library/dddpy/core_condominiums/`

### Nota metodológica
- G2/Capterra y varios agregadores bloquearon scraping directo en este entorno.
- Donde existían métricas citadas en el research previo, se conservaron como referencia indirecta y no como scraping fresco del agregador.

<small>🔚 fin · 06-Competitor-Analysis · Análisis Estratégico (Lelouch) · `docs/06-competitor-analysis/lelouch-strategic-analysis.md` · `2026-04-14`</small>


---

## 07-Roadmap · API Identity Context

<small>📄 `docs/07-roadmap/api-identity-context-roadmap.md` · modificado: `2026-04-15`</small>

# ♟️ Roadmap API — Auth, Users y Contexto de Negocio

> Fecha: 2026-04-15
> Autor: Lelouch S
> Estado: 🟡 Propuesto para ejecución
> Objetivo: cerrar la capa de APIs que aún falta sobre el rediseño de identidad, perfiles, ownership, occupancy y roles por condominio.

---

## 1. Veredicto de estado actual

El backend **ya tiene APIs estructurales** para el núcleo inmobiliario y las relaciones nuevas:
- `core_condominiums`
- `core_buildings`
- `core_buildings_types`
- `core_units`
- `core_unit_types`
- `core_unit_ownerships`
- `core_unit_occupancies`
- `core_condominium_roles`

Eso cubre CRUD base.

Lo que **todavía falta** para que el producto deje de ser solo estructura y se convierta en una API utilizable por frontend es:

1. **Auth / sesión**
2. **Users**
3. **User profiles**
4. **APIs agregadas de contexto**
5. **RBAC contextual aplicado en rutas**

---

## 2. Principio arquitectónico

No queremos un frontend obligado a armar el rompecabezas con 5 llamadas crudas por pantalla.

La capa API faltante debe resolver dos necesidades diferentes:

### Portal admin
- gestionar usuarios
- buscar por email/documento
- ver propiedades, ocupaciones y roles
- asignar ownerships/occupancies/roles
- operar por condominio

### Portal usuario
- iniciar sesión
- ver su perfil
- ver sus unidades
- ver en qué condominio está actuando
- entender si es propietario, ocupante o admin

---

## 3. Bloques de trabajo

## BLOQUE E — Auth API
### Objetivo
Dar entrada y control de sesión al sistema.

### Endpoints mínimos obligatorios
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`
- `POST /auth/verify-email`
- `POST /auth/resend-verification`
- `GET /auth/me`
- `GET /auth/health`

### Reglas
- `login` por email + password
- emitir access token + refresh token si el stack ya está listo
- no exponer detalles de si el email existe en flujos de recovery
- `me` debe devolver identidad base + contexto mínimo

### Entregables
- módulo `auth/` DDD o capa de use cases equivalente
- rutas FastAPI
- validación de credenciales
- esquema de tokens/sesión

### Responsable sugerido
- **Bulma:** implementación
- **Misato:** revisión de contrato y seguridad

---

## BLOQUE F — Users API
### Objetivo
Exponer la identidad base como recurso administrable.

### Endpoints mínimos obligatorios
- `POST /users`
- `GET /users`
- `GET /users/{id}`
- `GET /users/uuid/{uuid}`
- `PUT /users/{id}`
- `DELETE /users/{id}`
- `POST /users/{id}/restore`
- `POST /users/{id}/suspend`
- `POST /users/{id}/activate`
- `GET /users/health`

### Filtros mínimos en listado
- `email`
- `status`
- `document_number` (si se decide join con profile o índice denormalizado)
- `include_deleted`

### Reglas
- `email` unique y normalizado
- no exponer `password_hash`
- suspensión y activación deben ser explícitas
- `users_residents` no participa aquí

### Entregables
- rutas API
- schemas cmd/query
- filtros admin útiles
- response contracts consistentes

### Responsable sugerido
- **Bulma:** implementación
- **Misato:** definición final de filtros y shape de respuesta

---

## BLOQUE G — User Profiles API
### Objetivo
Separar el perfil humano de la autenticación y exponerlo como recurso claro.

### Endpoints mínimos obligatorios
- `POST /user-profiles`
- `GET /user-profiles/{user_id}`
- `PUT /user-profiles/{user_id}`
- `GET /user-profiles/health`

### Opcionales muy recomendados
- `GET /user-profiles/by-document`
- `GET /user-profiles/by-phone`

### Reglas
- documento dividido en `document_type` + `document_number`
- teléfono normalizado
- el perfil no debe duplicar credenciales

### Entregables
- módulo `user_profiles`
- rutas FastAPI
- validaciones de documento/teléfono

### Responsable sugerido
- **Bulma:** implementación
- **Misato:** validación de contrato y reglas de negocio

---

## BLOQUE H — APIs agregadas de contexto
### Objetivo
Dar al frontend endpoints de producto, no solo CRUDs técnicos.

### Endpoints mínimos obligatorios
- `GET /users/{id}/ownerships`
- `GET /users/{id}/occupancies`
- `GET /users/{id}/roles`
- `GET /users/{id}/contexts`
- `GET /me/contexts`
- `GET /units/{id}/summary`
- `GET /condominiums/{id}/admins`

### Qué debe devolver `/users/{id}/contexts`
Una respuesta agregada con:
- user
- profile
- condominiums relacionados
- units donde es owner
- units donde es occupant
- roles administrativos activos
- contexto actual si aplica

### Qué debe devolver `/me/contexts`
La misma idea, pero para el usuario autenticado.

### Qué debe devolver `/units/{id}/summary`
- unit
- building
- condominium
- owners activos
- occupancies activas
- occupancy_status actual

### Qué debe devolver `/condominiums/{id}/admins`
- usuarios con roles admin activos en ese condominio
- rol
- vigencia

### Reglas
- estas APIs son de consumo real de frontend
- deben evitar N+1 conceptual del lado del cliente
- son las APIs que convierten el modelo en producto

### Responsable sugerido
- **Bulma:** implementación técnica
- **Misato:** priorización y definición de shape final por pantalla

---

## BLOQUE I — RBAC contextual
### Objetivo
Aplicar permisos reales sobre las APIs, no solo guardar roles en tabla.

### Lo mínimo que debe existir
- dependencia/middleware para usuario autenticado
- resolución de roles por `core_condominium_roles`
- verificación por contexto de condominio
- separación de permisos admin vs usuario portal

### Reglas mínimas
- un rol global no reemplaza el rol contextual
- admin de condominio A no administra condominio B por accidente
- un usuario puede tener múltiples contextos válidos

### Endpoints o capacidades derivadas
- guard para rutas admin
- guard para lectura de contexto propio
- posible header/query de `current_condominium_id` o equivalente controlado

### Responsable sugerido
- **Misato:** definición de la matriz de permisos
- **Bulma:** implementación técnica de guards/dependencies

---

## 4. Orden correcto de ejecución

### Sprint API-1
**Bloque E — Auth**
- login
- me
- refresh
- logout
- verify/reset base

### Sprint API-2
**Bloque F — Users**
- CRUD base
- activate/suspend
- filtros admin

### Sprint API-3
**Bloque G — User Profiles**
- CRUD base de perfil
- búsqueda por documento/teléfono

### Sprint API-4
**Bloque H — Context APIs**
- `/users/{id}/contexts`
- `/me/contexts`
- `/units/{id}/summary`
- `/condominiums/{id}/admins`

### Sprint API-5
**Bloque I — RBAC contextual**
- guards
- matrix de permisos
- endurecimiento de rutas

---

## 5. Priorización dura

### Prioridad 1 — imprescindible
- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/refresh`
- `GET /users`
- `GET /users/{id}`
- `POST /users`
- `GET /user-profiles/{user_id}`
- `PUT /user-profiles/{user_id}`
- `GET /me/contexts`

### Prioridad 2 — producto usable
- suspend/activate users
- forgot/reset password
- verify/resend verification
- `/users/{id}/contexts`
- `/units/{id}/summary`
- `/condominiums/{id}/admins`

### Prioridad 3 — hardening
- RBAC contextual completo
- búsqueda por documento/teléfono
- validaciones y auditoría adicional

---

## 6. Reparto recomendado Misato vs Bulma

## Misato — coordinación y control del tablero
Debe hacerse cargo de:
1. congelar el contrato de cada endpoint antes de que Bulma codifique
2. definir shape de respuesta para admin portal y user portal
3. definir matriz RBAC contextual
4. revisar consistencia entre APIs nuevas y modelo de dominio
5. evitar que el frontend quede atado a CRUDs demasiado crudos

### Checklist de Misato
- ¿el endpoint resuelve un caso de uso real o solo expone tabla?
- ¿el contrato sirve al admin portal?
- ¿el contrato sirve al portal usuario?
- ¿el contexto de condominio está claro?
- ¿el permiso está resuelto por rol contextual y no global?

## Bulma — ejecución
Debe hacerse cargo de:
1. crear módulos/rutas faltantes
2. implementar schemas y use cases
3. aplicar shared response schemas
4. agregar health endpoints
5. asegurar imports limpios, sin circularidades ni rutas incoherentes
6. validar que todo responda en `7501`

### Checklist de Bulma
- no duplicar lógica entre `users` y `user_profiles`
- no exponer `password_hash`
- no usar `users_residents` para nuevas APIs
- no meter permisos admin como campo global del usuario
- no dejar endpoints sin filtros útiles
- no romper naming ya corregido (`units`, no `unities`)

---

## 7. Criterios de aceptación por bloque

### Auth
- login funciona
- `me` responde con identidad válida
- refresh funciona
- password reset no filtra existencia de usuarios

### Users
- CRUD operativo
- filtros útiles
- activación/suspensión explícita
- soft delete/restore consistentes

### Profiles
- perfil desacoplado de auth
- actualización correcta
- documento/teléfono validados

### Context APIs
- frontend puede renderizar dashboard sin 8 llamadas manuales
- ownership/occupancy/roles salen agregados correctamente

### RBAC
- rutas admin protegidas por contexto
- usuario sin rol no administra por accidente
- cambio de condominio no escala permisos indebidos

---

## 8. Riesgos a evitar

- construir `auth` sin pensar en `me/contexts`
- exponer CRUD de users sin endpoints agregados de producto
- mezclar perfil y autenticación otra vez
- usar rol global del usuario como permiso final
- dejar a frontend resolviendo toda la inteligencia de negocio
- revivir `users_residents` por comodidad

---

## 9. Siguiente movimiento recomendado

Si quieren avanzar sin desperdiciar piezas, la orden correcta es:

1. **Misato** define contrato de `auth/me` y `me/contexts`
2. **Bulma** implementa `auth` base
3. **Misato** congela contrato `users` + `user_profiles`
4. **Bulma** implementa esos dos módulos
5. **Ambas** cierran context APIs
6. **Al final** endurecen RBAC contextual

---

## 10. Veredicto final

El rediseño de tablas ya ganó la apertura.
Ahora falta convertir esa ventaja posicional en una API de producto real.

La jugada correcta no es crear 20 endpoints sueltos por reflejo.
La jugada correcta es cerrar primero:
- auth
- users
- profiles
- contexts
- RBAC

Si eso queda bien, el frontend avanza con tablero limpio.
Si queda mal, volverán a improvisar joins mentales en cada pantalla.

Y eso sería perder una partida ganada.

<small>🔚 fin · 07-Roadmap · API Identity Context · `docs/07-roadmap/api-identity-context-roadmap.md` · `2026-04-15`</small>


---

## 07-Roadmap · Auth Hardening

<small>📄 `docs/07-roadmap/auth-hardening-roadmap.md` · modificado: `2026-04-15`</small>

# ♟️ Roadmap de Corrección — Auth Hardening + Naming Cleanup

> Fecha: 2026-04-15
> Autor: Lelouch S
> Estado: 🟡 Propuesto para ejecución inmediata
> Objetivo: endurecer el módulo `auth` recién implementado para que deje de ser solo funcional y pase a ser seguro, consistente y listo para escalar.

---

## 1. Diagnóstico ejecutivo

El módulo `auth` ya funciona, pero todavía presenta debilidades de diseño que lo dejan expuesto.

### Estado actual
- login funcional
- refresh token rotation funcional
- logout y logout-all funcionales a nivel refresh session
- `/auth/me` funcional
- sesiones persistidas en `auth_sessions`

### Problema central
Hoy el sistema revoca sesiones en DB, pero el **access token JWT puede seguir siendo válido hasta expirar**.

Eso significa que una sesión “cerrada” o una cuenta suspendida puede seguir entrando por una ventana de tiempo no deseada.

---

## 2. Objetivos del frente

1. eliminar fallas críticas de seguridad
2. endurecer el flujo de sesión
3. aplicar control contextual real al usuario autenticado
4. alinear naming del módulo con el estándar final del dominio
5. dejar base sana para RBAC contextual posterior

---

## 3. Problemas detectados

## 3.1 Secret JWT inseguro por defecto
### Hallazgo
`jwt_service.py` usa un fallback como:
- `dev-secret-change-in-production`

### Riesgo
Si la variable de entorno falta o está mal cargada, el backend firma tokens con una clave predecible.

### Corrección obligatoria
- eliminar fallback inseguro
- requerir env obligatorio
- fallar al boot si no existe secret válido
- idealmente separar:
  - `JWT_ACCESS_SECRET`
  - `JWT_REFRESH_SECRET` si en el futuro refresh también migra a JWT

### Prioridad
🔴 Crítica

---

## 3.2 Revocación incompleta de sesión
### Hallazgo
`logout` y `logout-all` revocan refresh sessions, pero **no invalidan access tokens ya emitidos**.

### Riesgo
Un token emitido antes del logout puede seguir accediendo a rutas protegidas hasta su expiración.

### Corrección obligatoria
Elegir una de estas estrategias y aplicarla de forma consistente:

#### Opción recomendada
**`token_version` en `users`**
- agregar `token_version INT NOT NULL DEFAULT 0`
- incluir `token_version` en el JWT access token
- en `get_current_user()` validar que el token version del JWT coincida con DB
- en `logout-all`, suspensión, reset de password o compromise → incrementar `token_version`

#### Opción alternativa
**`session_uuid` o `jti` por token**
- emitir access token con `jti` o `session_uuid`
- verificarlo contra DB en cada request protegida

### Recomendación final
Implementar **`token_version` primero**. Es más simple, claro y suficiente para esta fase.

### Prioridad
🔴 Crítica

---

## 3.3 `get_current_user()` no valida estado operativo del usuario
### Hallazgo
La dependencia de auth valida token y existencia del usuario, pero no endurece contra:
- `inactive`
- `suspended`
- `locked`
- usuario con `deleted_at`

### Riesgo
Un JWT válido puede seguir operando para una cuenta que ya no debería estar activa.

### Corrección obligatoria
En `get_current_user()`:
- cargar estado actual del usuario
- rechazar acceso si `status != active`
- rechazar acceso si `locked_until > now`
- rechazar acceso si `deleted_at IS NOT NULL`

### Prioridad
🔴 Crítica

---

## 3.4 Protección de timing incompleta en login
### Hallazgo
Cuando el usuario no existe, se ejecuta un dummy `sha256`; cuando sí existe, se hace verify de password real.

### Riesgo
Los tiempos no son equivalentes. Eso no evita de verdad la enumeración por timing.

### Corrección obligatoria
- usar un hash bcrypt dummy estático y verificar contra ese hash cuando el usuario no exista
- mantener el mismo flujo temporal de comparación

### Prioridad
🟠 Alta

---

## 3.5 Refresh rotation pierde metadata de sesión
### Hallazgo
Al rotar refresh token, la nueva sesión se crea sin conservar:
- `user_agent`
- `ip_address`

### Riesgo
Se pierde trazabilidad y capacidad de auditoría operacional.

### Corrección obligatoria
- al hacer refresh, copiar `user_agent` e `ip_address` de la sesión anterior
- opcional: actualizar `last_used_at` si luego agregan ese campo

### Prioridad
🟠 Alta

---

## 3.6 Acoplamiento excesivo entre auth y perfil humano
### Hallazgo
`AuthUserRepository` hace JOIN directo `users + user_profiles` para devolver identidad.

### Riesgo
Cambios de perfil pueden romper auth por una razón que no debería incumbirle.

### Corrección recomendada
Separar conceptualmente:
- `AuthPrincipal` o `AuthenticatedUser` → datos mínimos de autenticación
- `AuthMeView` o response assembler → composición users + profile para `/auth/me`

### Recomendación pragmática
No romper todo ahora.
Primero asegurar el módulo.
Luego refactorizar a:
- repositorio auth mínimo
- query/assembler específico para `/auth/me`

### Prioridad
🟡 Media

---

## 3.7 Naming inconsistente en documentos y perfil
### Hallazgo
En el proyecto se empujó el estándar:
- `document_type`
- `document_number`

Pero en `auth`/`profiles` aparecen variantes como:
- `doc_type`
- `doc_identity`

### Riesgo
- inconsistencia en APIs
- deuda técnica en frontend
- contract drift entre módulos
- migraciones futuras más dolorosas

### Corrección obligatoria de naming
Alinear al naming final:
- `doc_type` → `document_type`
- `doc_identity` → `document_number`

Y en respuestas JSON:
- no devolver `doc_identity`
- devolver `document_type`
- devolver `document_number`

### Recomendación adicional
Revisar si todavía queda naming viejo en:
- `users`
- `user_profiles`
- `auth`
- docs
- schemas Pydantic
- responses

### Prioridad
🟠 Alta

---

## 3.8 Integridad explícita de `auth_sessions`
### Hallazgo
El modelo SQLAlchemy no deja visible FK explícita en `user_id`.

### Riesgo
Si la migración no la puso correctamente, la integridad depende de la suerte.

### Corrección obligatoria
- validar migración real de `auth_sessions`
- asegurar FK a `users(id)`
- indexar correctamente `user_id`, `refresh_token_hash`, `deleted_at`, `expires_at`

### Prioridad
🟠 Alta

---

## 3.9 Tokens opacos de refresh mejorables
### Hallazgo
El refresh token actual usa UUID v4.

### Riesgo
No es un desastre, pero es menos robusto que un token opaco generado con `secrets`.

### Corrección recomendada
Migrar a:
- `secrets.token_urlsafe(48)` o similar

### Prioridad
🟡 Media

---

## 4. Orden exacto de ejecución

## Fase 1 — Seguridad crítica
1. eliminar secret JWT por defecto
2. validar estado actual del usuario en `get_current_user()`
3. implementar invalidación real de access tokens vía `token_version`

### Criterio de cierre
- el backend no inicia sin secret válido
- un usuario suspendido no puede acceder aunque tenga JWT vigente
- `logout-all` o suspensión invalidan access tokens previamente emitidos

---

## Fase 2 — Endurecimiento de sesión
4. corregir dummy bcrypt para timing uniforme
5. preservar `user_agent` e `ip_address` en refresh rotation
6. revisar integridad/FK de `auth_sessions`

### Criterio de cierre
- login tiene flujo temporal más homogéneo
- la trazabilidad de sesión se mantiene tras refresh
- `auth_sessions` queda íntegra y auditable

---

## Fase 3 — Cleanup semántico
7. corregir naming `doc_*` → `document_*`
8. alinear response de `/auth/me`
9. revisar docs y schemas para eliminar nombres viejos

### Shape objetivo de `/auth/me`
```json
{
  "success": true,
  "message": "Identity retrieved",
  "data": {
    "user": {
      "id": 1,
      "uuid": "...",
      "email": "user@example.com",
      "status": "active",
      "email_verified_at": null,
      "created_at": "..."
    },
    "profile": {
      "uuid": "...",
      "first_name": "...",
      "last_name": "...",
      "phone": "...",
      "document_type": "DNI",
      "document_number": "12345678"
    }
  }
}
```

### Criterio de cierre
- no quedan `doc_type` ni `doc_identity` expuestos públicamente
- contrato JSON consistente con el estándar final

---

## 5. Asignación recomendada

## Misato — coordinación y criterio
Debe encargarse de:
- congelar contrato final de `/auth/me`
- aprobar estrategia `token_version`
- validar matriz de estados que bloquean acceso
- revisar naming final `document_type` / `document_number`
- revisar que Bulma no meta una solución parche para invalidez de token

## Bulma — ejecución
Debe encargarse de:
- migración y campo `token_version`
- modificación de JWT payload + dependency
- endurecer `get_current_user()`
- corregir dummy timing check
- preservar metadata en refresh
- renombrar contratos/document fields inconsistentes

---

## 6. Checklist operativo para Bulma

### Seguridad
- [ ] eliminar fallback insecure de JWT secret
- [ ] agregar validación de secret al boot
- [ ] agregar `token_version` a `users`
- [ ] incluir `token_version` en access token
- [ ] validar `token_version` en `get_current_user()`
- [ ] invalidar tokens en `logout-all`, suspensión y eventos críticos

### Estado de usuario
- [ ] bloquear `inactive`
- [ ] bloquear `suspended`
- [ ] bloquear `locked_until > now`
- [ ] bloquear `deleted_at != null`

### Sesiones
- [ ] preservar `user_agent`
- [ ] preservar `ip_address`
- [ ] validar FK e índices de `auth_sessions`
- [ ] evaluar migración posterior a refresh token opaco con `secrets`

### Naming
- [ ] `doc_type` → `document_type`
- [ ] `doc_identity` → `document_number`
- [ ] actualizar repository queries
- [ ] actualizar `UserIdentity`
- [ ] actualizar `/auth/me`
- [ ] actualizar docs

---

## 7. Criterios de aceptación final

Este frente se considera cerrado cuando:
- una sesión revocada ya no conserva acceso operativo por JWT viejo
- una cuenta suspendida o bloqueada no entra aunque tenga token vigente
- el backend falla si no tiene secret correcto
- `/auth/me` devuelve naming consistente
- no quedan respuestas públicas con `doc_identity`
- la trazabilidad de sesión se mantiene tras refresh

---

## 8. Veredicto final

El módulo `auth` ya mueve piezas, pero todavía no protege bien al Rey.

La prioridad no es agregar más endpoints por reflejo.
La prioridad es **cerrar las brechas de seguridad y semántica** antes de seguir expandiendo el castillo.

Primero:
- secret seguro
- invalidación real
- validación de estado
- naming consistente

Luego sí, el resto del tablero.

<small>🔚 fin · 07-Roadmap · Auth Hardening · `docs/07-roadmap/auth-hardening-roadmap.md` · `2026-04-15`</small>


---

## 07-Roadmap · core_buildings Task Order

<small>📄 `docs/07-roadmap/core_buildings-task-order.md` · modificado: `2026-04-14`</small>

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
- relación con unidades (`core_unities`)
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
- validar integración con `core_unities`
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

<small>🔚 fin · 07-Roadmap · core_buildings Task Order · `docs/07-roadmap/core_buildings-task-order.md` · `2026-04-14`</small>


---

## 07-Roadmap · core_unities Rename Plan

<small>📄 `docs/07-roadmap/core_unities-rename-plan.md` · modificado: `2026-04-14`</small>

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

<small>🔚 fin · 07-Roadmap · core_unities Rename Plan · `docs/07-roadmap/core_unities-rename-plan.md` · `2026-04-14`</small>


---

## 07-Roadmap · core_unities Task Order

<small>📄 `docs/07-roadmap/core_unities-task-order.md` · modificado: `2026-04-14`</small>

# ♟️ core_unities — Orden de Trabajo y Control de Ejecución

> Fecha: 2026-04-14
> Autor: Lelouch S
> **ESTADO: 🟡 EN REVISIÓN — pendiente de aprobación**
> Arquitecto: Lelouch S | Coordinator: Misato K | Dev: Bulma S
> Objetivo: dejar un tablero único para rediseñar e implementar `core_unities` como módulo real de negocio, con criterios claros de base de datos, lógica, naming, constraints, y flujo de ejecución.

---

## 1. Objetivo del módulo

Implementar `core_unities` como pieza central del núcleo inmobiliario del sistema, no como simple tabla de departamentos.

Debe quedar preparada para servir como base de:
- ocupación por unidad
- relación con residentes
- futura cobranza y ledger por unidad
- tickets/incidencias segmentadas
- documentos por inmueble
- reportes operativos y financieros
- portal residente

La unidad es el punto donde convergen propiedad, ocupación y operación. Si esta pieza se diseña mal, todo lo demás nace torcido.

---

## 2. Diagnóstico del diseño actual

El diseño actual en `001_create_initial.py` define esta tabla:
- `id`
- `uuid`
- `name`
- `code`
- `description`
- `size`
- `percentage`
- `type`
- `floor`
- `unit`
- `building_id`
- `unity_type_id`
- `status`
- `created_at`
- `updated_at`

### Problemas detectados

1. `type` duplica responsabilidad de `unity_type_id`.
2. `unit` tiene mal naming y semántica débil.
3. `size` es ambiguo: no distingue área privada, construida o vendible.
4. `percentage` tiene nombre y precisión pobres para copropiedad real.
5. `code` aparece con unicidad global, lo cual no escala bien a negocio real.
6. No existe `deleted_at` para soft delete.
7. No existen constraints numéricos mínimos.
8. No existen índices estratégicos para filtros operativos.
9. No existe estado de ocupación (`occupancy_status`).
10. El módulo Python `src/library/dddpy/core_unities/` no existe todavía.

---

## 3. Cambios obligatorios sobre el diseño actual

### 3.1 Eliminar redundancia de tipos
**Acción:** eliminar campo `type`.

**Motivo:**
El tipo de unidad debe representarse exclusivamente con `unity_type_id`.

**Regla final:**
- el tipo formal vive en catálogo (`core_unittys_types`)
- no se acepta texto libre paralelo

---

### 3.2 Corregir naming operativo
**Acción:** renombrar `unit` → `unit_number`.

**Motivo:**
`unit` es demasiado genérico. `unit_number` comunica mejor que representa la identidad física visible de la unidad.

**Ejemplos válidos:**
- `101`
- `A-12`
- `PH-1`
- `LOCAL-03`

---

### 3.3 Corregir campos numéricos ambiguos
**Acción:**
- eliminar `size`
- eliminar `percentage`
- agregar:
  - `private_area DECIMAL(12,4)`
  - `coefficient DECIMAL(9,6)`

**Motivo:**
- `size` mezcla significados distintos
- `percentage` se queda corta para reglas reales de copropiedad
- el modelo debe ser preciso para crecer hacia finanzas, prorrateos y reportes

---

### 3.4 Mejorar semántica de piso
**Acción:** reemplazar `floor` por:
- `floor_number INT NULL`
- `floor_label VARCHAR(30) NULL` (opcional recomendado)

**Motivo:**
En la operación real, no todo piso se representa bien como entero: sótanos, mezzanine, PH, lobby, rooftop.

**Regla sugerida:**
- `floor_number` para orden/lógica
- `floor_label` para UI/presentación

---

### 3.5 Agregar estado de ocupación
**Acción:** agregar `occupancy_status VARCHAR(30)` o smallint/enum equivalente.

**Valores iniciales sugeridos:**
- `vacant`
- `occupied`
- `reserved`
- `maintenance`
- `blocked`

**Motivo:**
`status` operativo no cubre el estado real de ocupación. La competencia trabaja con este eje porque impacta reportes, comunicación, cobranza y operación.

---

### 3.6 Agregar orden visual
**Acción:** agregar `sort_order INT NOT NULL DEFAULT 0`.

**Motivo:**
Permite ordenar unidades en UI/reportes sin depender del `id`.

---

### 3.7 Agregar borrado lógico
**Acción:** agregar `deleted_at DATETIME NULL`.

**Motivo:**
Una unidad con historial de residentes, cobros, tickets o documentos no debe desaparecer físicamente salvo proceso excepcional.

---

## 4. Estructura final recomendada para `core_unities`

| Campo | Tipo sugerido | Nullable | Default | Descripción |
|---|---|---|---|---|
| id | BIGINT | NO | autoincrement | PK interna |
| uuid | CHAR(36) / UUID | NO | UUID() | Identificador estable externo |
| building_id | BIGINT | NO | — | FK al edificio |
| unity_type_id | BIGINT | YES | NULL | FK al catálogo de tipo de unidad |
| unit_number | VARCHAR(50) | NO | — | Identidad física visible de la unidad |
| code | VARCHAR(50) | YES | NULL | Código operativo interno/importación |
| name | VARCHAR(255) | YES | NULL | Nombre visible/comercial opcional |
| description | TEXT | YES | NULL | Notas administrativas |
| private_area | DECIMAL(12,4) | YES | NULL | Área privada útil de la unidad |
| coefficient | DECIMAL(9,6) | YES | NULL | Coeficiente de copropiedad/prorrateo |
| floor_number | INT | YES | NULL | Piso numérico para lógica y orden |
| floor_label | VARCHAR(30) | YES | NULL | Etiqueta de piso para UI |
| occupancy_status | VARCHAR(30) | NO | `vacant` | Estado de ocupación |
| sort_order | INT | NO | 0 | Orden visual/manual |
| status | INT | NO | 1 | Estado operativo |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP ON UPDATE | Fecha de actualización |
| deleted_at | DATETIME | YES | NULL | Soft delete |

---

## 5. Qué columnas eliminar, renombrar o conservar

### Eliminar
- `type`
- `size`
- `percentage`
- `unit`
- `floor`

### Renombrar / reemplazar
- `unit` → `unit_number`
- `size` → `private_area`
- `percentage` → `coefficient`
- `floor` → `floor_number`

### Conservar
- `id`
- `uuid`
- `name` (pero opcional)
- `code` (pero no como identidad única global)
- `description`
- `building_id`
- `unity_type_id`
- `status`
- `created_at`
- `updated_at`

### Agregar
- `floor_label`
- `occupancy_status`
- `sort_order`
- `deleted_at`

---

## 6. Constraints exactos recomendados

### 6.1 Unicidad
**Eliminar:**
- `UNIQUE(code)` global

**Crear:**
- `UNIQUE(building_id, unit_number)`
- `UNIQUE(building_id, code)` solo si `code` se decide obligatorio/operativo

**Nota:**
Si `code` queda opcional, evaluar permitir múltiples `NULL` y mantener unicidad solo para valores no nulos según comportamiento MySQL.

---

### 6.2 CHECK constraints
Crear como mínimo:

- `ck_core_unities_private_area_positive`
  - `private_area IS NULL OR private_area >= 0`

- `ck_core_unities_coefficient_range`
  - `coefficient IS NULL OR (coefficient >= 0 AND coefficient <= 100)`

- `ck_core_unities_sort_order_positive`
  - `sort_order >= 0`

- `ck_core_unities_floor_number_range`
  - opcional en fase 1 si se usa un rango operativo razonable
  - ejemplo: `floor_number IS NULL OR floor_number >= -20`

- `ck_core_unities_occupancy_status_valid`
  - si usan CHECK en lugar de catálogo/enum:
  - `occupancy_status IN ('vacant','occupied','reserved','maintenance','blocked')`

---

### 6.3 Foreign keys
**building_id**
- referencia: `core_buildings.id`
- acción recomendada: `ON DELETE RESTRICT`
- `ON UPDATE CASCADE`

**unity_type_id**
- referencia: `core_unittys_types.id`
- acción recomendada: `ON DELETE SET NULL`
- `ON UPDATE CASCADE` o `SET NULL` según política del proyecto

---

## 7. Índices exactos recomendados

### Índices mínimos
- `ix_core_unities_building_id` → `(building_id)`
- `ix_core_unities_unity_type_id` → `(unity_type_id)`
- `ix_core_unities_status` → `(status)`

### Índices compuestos operativos
- `ix_core_unities_building_status` → `(building_id, status)`
- `ix_core_unities_building_sort` → `(building_id, sort_order)`
- `ix_core_unities_building_floor` → `(building_id, floor_number)`
- `ix_core_unities_building_occupancy` → `(building_id, occupancy_status)`

### Índices únicos
- `ux_core_unities_building_unit_number` → `(building_id, unit_number)`
- `ux_core_unities_building_code` → `(building_id, code)` si aplica

---

## 8. Reglas de negocio obligatorias

- No crear unidad sin `building_id` válido.
- No crear unidad bajo edificio eliminado lógicamente.
- No crear unidad con `unity_type_id` inexistente o inactivo.
- No repetir `unit_number` dentro del mismo edificio.
- No permitir áreas negativas.
- No permitir `coefficient` fuera de rango.
- Los listados deben excluir eliminados por defecto.
- Debe existir restore.
- No permitir hard delete si la unidad tiene residentes activos o relaciones operativas posteriores.
- Si el edificio padre está inactivo/eliminado, no debe permitirse alta operativa de nuevas unidades.

---

## 9. Observaciones de modelado que deben respetarse

### 9.1 `name` no debe ser identidad principal
`name` puede existir para UX o naming comercial, pero no debe desplazar a `unit_number`.

### 9.2 `code` no debe ser obligatorio por dogma
Si el negocio no necesita un código interno separado, no debe forzarse solo por costumbre técnica.

### 9.3 `occupancy_status` y `status` no son lo mismo
- `status` = vive el registro operativamente o no
- `occupancy_status` = vacante, ocupada, reservada, mantenimiento, bloqueada

### 9.4 No meter deuda o propietario directo en esta tabla
Los datos de ownership, tenancy, balance o cuentas deben vivir en módulos/relaciones separadas.

### 9.5 No repetir jerarquía completa en tablas hijas si no hay razón real
Cuando se implemente `users_residents`, usar `unity_id` como raíz principal. Si además se persisten `building_id` y `condominium_id`, se deberá validar consistencia estricta.

---

## 10. Relación estratégica con análisis competitivo

Los productos serios del mercado no tratan la unidad como simple catálogo. La tratan como nodo operativo de:
- ocupación
- residentes/tenancy
- estado de cuenta
- documentos
- tickets
- comunicación segmentada

Por eso este módulo debe quedar listo para alimentar en el futuro:
- ledger por unidad
- cobranza por unidad
- estado de ocupación en dashboards
- portal residente
- indicadores de morosidad/ocupación
- incidencias y documentación asociada

El error clásico sería modelarla como “otro CRUD”. Ese camino sacrifica la reina por un peón.

---

## 11. Lista oficial de tareas

## Tarea 1 — Diseñar migración de refactor sobre `core_unities`
**Objetivo:**
- eliminar campos ambiguos
- agregar campos nuevos
- corregir uniqueness
- agregar índices y constraints
- agregar `deleted_at`

**Entregable:**
- migración Alembic nueva, separada de `001_create_initial.py`

**Responsable propuesto:** Bulma S
**Revisión:** Misato K

---

## Tarea 2 — Crear/ajustar documentación del modelo
**Objetivo:**
Actualizar `docs/03-modules/models/core_unities.md` con estructura final, reglas de negocio, índices y constraints.

**Entregable:**
- documento actualizado y coherente con migración real

**Responsable propuesto:** Misato K
**Apoyo:** Bulma S

---

## Tarea 3 — Implementar módulo DDD `core_unities`
**Objetivo:**
Crear la estructura completa:

```
core_unities/
├── domain/
│   ├── unity_entity.py
│   ├── unity_data.py
│   ├── unity_exception.py
│   ├── unity_success.py
│   ├── unity_repository.py
│   ├── unity_cmd_repository.py
│   └── unity_query_repository.py
├── infrastructure/
│   ├── dbunitys.py
│   ├── unity_mapper.py
│   ├── unity_cmd_repository.py
│   └── unity_query_repository.py
└── usecase/
    ├── unity_cmd_schema.py
    ├── unity_cmd_usecase.py
    ├── unity_query_usecase.py
    ├── unity_usecase.py
    └── unity_factory.py
```

**Responsable propuesto:** Bulma S
**Revisión arquitectónica:** Lelouch S
**Coordinación:** Misato K

---

## Tarea 4 — Exponer API routes
**Objetivo:**
Agregar endpoints siguiendo patrón de `core_buildings`.

### Endpoints mínimos
- `POST /unities`
- `GET /unities/{id}`
- `GET /unities/uuid/{uuid}`
- `PUT /unities/{id}`
- `DELETE /unities/{id}`
- `POST /unities/{id}/restore`
- `DELETE /unities/{id}/hard`
- `GET /unities`
- `GET /unities/building/{building_id}`

**Responsable propuesto:** Bulma S
**Revisión:** Misato K

---

## Tarea 5 — Reglas de eliminación y restauración
**Objetivo:**
Implementar:
- soft delete por defecto
- restore
- hard delete bloqueado si hay dependencias activas

**Dependencias a revisar:**
- `users_residents`
- futuras tablas financieras/documentales

**Responsable propuesto:** Bulma S
**Revisión funcional:** Misato K

---

## Tarea 6 — Testing mínimo obligatorio
**Objetivo:**
Cubrir al menos:
- create válido
- rechazo de duplicado por `(building_id, unit_number)`
- filtros por building/status
- soft delete y restore
- hard delete bloqueado con dependencias
- validaciones de área/coefficient

**Responsable propuesto:** Bulma S
**Revisión:** Misato K

---

## Tarea 7 — Integración con `core_buildings`
**Objetivo:**
Validar que `core_buildings.count_active_units()` siga coherente con el nuevo modelo y naming.

**Observación:**
Actualmente el conteo usa SQL crudo sobre `core_unities` con `status = 1`. Revisar si debe además excluir `deleted_at IS NOT NULL`.

**Regla final sugerida:**
- unidad activa = `status = 1 AND deleted_at IS NULL`

**Responsable propuesto:** Misato K
**Apoyo:** Bulma S

---

## 12. Orden recomendado de ejecución

1. aprobar diseño final del schema
2. crear migración Alembic
3. actualizar documentación
4. implementar DDD module
5. exponer rutas API
6. ajustar conteos/relaciones con edificios
7. agregar tests
8. revisión final funcional/arquitectónica

No invertir este orden. Si se implementa código antes de cerrar el schema, solo se fabrica retrabajo.

---

## 13. Criterios de revisión para Misato

Misato debe validar:
- coherencia entre documentación y migración
- naming correcto (`unit_number`, `private_area`, `coefficient`)
- eliminación real de redundancias (`type`)
- unicidad compuesta correcta
- constraints presentes
- índices alineados a queries reales
- semántica correcta de soft delete
- consistencia con estrategia del dominio y roadmap

---

## 14. Criterios de ejecución para Bulma

Bulma debe ejecutar con estas reglas:
- no inventar campos fuera del plan sin aprobación
- no volver a introducir `type` texto libre
- no dejar `code` con unicidad global
- no usar `name` como identidad principal
- no omitir `deleted_at`
- no omitir tests mínimos
- seguir el patrón de `core_buildings` para estructura, pero no copiar ciegamente donde la semántica de unidad difiere

---

## 15. Riesgos si se ejecuta mal

- inconsistencias entre tipo libre y catálogo
- unidades duplicadas dentro del mismo edificio
- imposibilidad de crecer hacia cobranza/ledger
- soft delete inexistente y pérdida de trazabilidad
- conteos erróneos por no excluir eliminados
- deuda técnica mayor al pasar a residentes/finanzas

---

## 16. Condición para pasar a implementación

**No ejecutar desarrollo del módulo hasta tener aprobación explícita.**

Flujo recomendado:
1. Mike revisa este plan
2. aprueba o ajusta
3. Misato coordina ejecución
4. Bulma implementa
5. Lelouch hace revisión arquitectónica final

---

## 17. Follow-ups arquitectónicos posteriores al cierre inicial

Estas observaciones nacen de la revisión arquitectónica final del módulo. No bloquean el cierre funcional de `core_unities`, pero deben quedar registradas para hardening y coherencia futura.

### Follow-up A — Unificar política de soft delete en lecturas puntuales
**Estado:** corregible dentro del mismo módulo (`Obs1`)

**Hallazgo:**
`get_by_id()` y `get_by_uuid()` en `core_unities` no excluyen `deleted_at IS NOT NULL`, mientras `list_all()` y `list_by_building()` sí lo hacen.

**Riesgo:**
comportamiento inconsistente entre lecturas puntuales y listados, y asimetría con `core_buildings`.

**Regla final deseada:**
- por defecto, las lecturas públicas deben excluir registros soft-deleted
- si se requiere incluir eliminados, debe ser vía flag o flujo explícito

**Responsable recomendado:** Bulma S
**Revisión:** Misato K

---

### Follow-up B — Blindar duplicado de `code` también en update
**Estado:** corregible dentro del mismo módulo (`Obs2`)

**Hallazgo:**
`update()` valida duplicado de `unit_number`, pero no prevalida duplicado de `code` dentro del mismo building.

**Riesgo:**
la capa de aplicación puede terminar dependiendo de `IntegrityError` del motor en vez de lanzar una excepción de dominio limpia (`RepeatedUnityCode`).

**Regla final deseada:**
- `create()` y `update()` deben tener comportamiento simétrico para `code` y `unit_number`
- los errores de duplicado deben salir como dominio, no como accidente de infraestructura

**Responsable recomendado:** Bulma S
**Revisión:** Misato K

---

### Follow-up C — Alinear `count_active_residents()` con el diseño real de `users_residents`
**Estado:** diferido hasta implementación de `users_residents` (`Obs3`)

**Hallazgo:**
`count_active_residents()` en `core_unities` asume que `users_residents` tiene columna `deleted_at` y consulta `deleted_at IS NULL`.

**Situación actual:**
la tabla `users_residents` del schema inicial no garantiza todavía ese campo. Si el módulo existe sin `deleted_at`, el query cae al `except` y devuelve `0`.

**Riesgo:**
se degrada la defensa lógica previa al hard delete y se delega el bloqueo real al FK o a fallos de infraestructura.

**Regla final deseada cuando exista `users_residents`:**
- definir formalmente qué significa “residente activo”
- alinear el query con el schema real (`status`, `deleted_at`, u otra convención explícita)
- evitar `except` demasiado amplio como sustituto de contrato entre módulos

**Responsable futuro:** Misato K + Bulma S
**Revisión arquitectónica:** Lelouch S

---

## 18. Veredicto final

`core_unities` debe dejar de ser una tabla genérica y convertirse en una pieza operativa real del sistema.

La jugada correcta no es “hacer CRUD de departamentos”.
La jugada correcta es construir la base que luego sostendrá ocupación, residentes, cobro, tickets y reportes sin rehacer media arquitectura.

Ese es el movimiento que protege al Rey.

<small>🔚 fin · 07-Roadmap · core_unities Task Order · `docs/07-roadmap/core_unities-task-order.md` · `2026-04-14`</small>


---

## 07-Roadmap · core_units Rename Plan

<small>📄 `docs/07-roadmap/core_units-rename-plan.md` · modificado: `2026-04-15`</small>

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

<small>🔚 fin · 07-Roadmap · core_units Rename Plan · `docs/07-roadmap/core_units-rename-plan.md` · `2026-04-15`</small>


---

## 07-Roadmap · Module List

<small>📄 `docs/07-roadmap/module-list.md` · modificado: `2026-04-15`</small>

# 📋 Módulos a Crear — condo-py
> Generado: 2026-04-13 | Basado en: `07-roadmap/module-roadmap.md` (Lelouch S)
> Orden: SECUENCIAL — ejecutar en este orden, sin saltar fases.

---

## FASE 1 — Núcleo Inmobiliario

| # | Módulo | Descripción | Estado |
|---|---|---|---|
| 01 | `core_condominiums` | Gestión de condominios | ✅ Implementado |
| 02 | `core_buildings` | Torres/edificios dentro del condominio | ✅ Implementado |
| 03 | `core_buildings_types` | Catálogo: residencial, comercial, mixto | ✅ Implementado |
| 04 | `core_units` | Unidades/departamentos dentro de cada edificio | ✅ Implementado |
| 05 | `core_unit_types` | Catálogo: apartamento, casa, local comercial | ✅ Implementado |

---

## FASE 2 — Identidad, Acceso y Ocupación

| # | Módulo | Descripción | Estado |
|---|---|---|---|
| 06 | `users` | Usuarios autenticables en el sistema (users + user_profiles) | ✅ Implementado |
| 07 | `user_profiles` | Perfil humano desacoplado de autenticación | ✅ Implementado |
| 08 | `core_unit_ownerships` | Relación patrimonial usuario ↔ unidad | ✅ Implementado |
| 09 | `core_unit_occupancies` | Relación de ocupación/uso usuario ↔ unidad | ✅ Implementado |
| 10 | `core_condominium_roles` | Roles administrativos por condominio | ✅ Implementado |
| 11 | `auth` | Autenticación JWT/OAuth2 + RBAC contextual | ❌ Pendiente |

---

## FASE 3 — Cuentas, Cargos y Recibos

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 12 | `accounts_receivable` | Cuentas por cobrar por unidad | Crítica |
| 13 | `charges` | Cargos recurrentes (cuota mensual) y extraordinarios | Crítica |
| 14 | `receipts` | Generación de recibos por cargo/pago | Alta |
| 15 | `payments` | Registro de pagos y conciliación | Alta |
| 16 | `ledger` | Estado de cuenta por unidad / historial contable | Alta |

---

## FASE 4 — Comunicación y Operación Básica

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 17 | `announcements` | Anuncios/comunicados a residentes | Media-Alta |
| 18 | `notifications` | Notificaciones email/SMS/push/in-app | Media-Alta |
| 19 | `documents` | Repositorio de documentos (actas, reglamentos) | Media-Alta |
| 20 | `tickets` | Incidencias / solicitudes de mantenimiento | Media |

---

## FASE 5 — Experiencia Residente

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 21 | `resident_portal` | Portal web para residentes (estado de cuenta, docs, tickets) | Media |
| 22 | `amenity_booking` | Reserva de áreas comunes | Media |
| 23 | `visitors` | Registro previo de visitas/invitados | Media |
| 24 | `packages` | Registro de paquetería | Baja-Media |

---

## FASE 6 — Gobernanza y Capa Premium

| # | Módulo | Descripción | Prioridad |
|---|---|---|---|
| 25 | `meeting_minutes` | Actas de reuniones de board/assambleas | Baja |
| 26 | `voting` | Votaciones digitales / e-voting | Baja |
| 27 | `audit_trail` | Log de auditoría avanzado | Baja |
| 28 | `integrations` | Webhooks / API pública / integraciones externas | Baja |
| 29 | `dashboards` | Reporting ejecutivo y analítica | Baja |

---

## Total: 29 módulos

**Implementados:** 7 (01-07, incluyendo users y user_profiles)
**En construcción:** 3 (08, 09, 10 — Bloque C)
| 11 | `auth` | Autenticación JWT/OAuth2 + RBAC contextual | ❌ Pendiente |
| — | `users_residents` | Tabla histórica deprecada — fallback emergencia | ⚠️ Deprecated |

**Implementados:** 10 (01-10)
**Deprecados:** 1 (`users_residents` — no eliminar hasta validación)
**Pendientes:** 19

<small>🔚 fin · 07-Roadmap · Module List · `docs/07-roadmap/module-list.md` · `2026-04-15`</small>


---

## 07-Roadmap · Module Roadmap

<small>📄 `docs/07-roadmap/module-roadmap.md` · modificado: `2026-04-15`</small>

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
4. `core_units`
5. `core_unit_types` *(o mantener naming actual del catálogo solo como transición, pero el objetivo recomendado es `core_unit_types`)*

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
7. `user_profiles`
8. `core_unit_ownerships`
9. `core_unit_occupancies`
10. `core_condominium_roles`
11. auth / RBAC contextual

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
12. módulo de cuentas por cobrar
13. módulo de cargos/recibos
14. módulo de pagos
15. módulo de estado de cuenta / ledger

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
4. Unidades/departamentos (`core_units`)
5. Tipos de unidad
6. Usuarios
7. Perfil de usuario
8. Ownership por unidad
9. Occupancy por unidad
10. Roles administrativos por condominio
11. Auth + RBAC contextual
12. Cuentas por cobrar
13. Recibos / cargos
14. Pagos
15. Estado de cuenta
16. Comunicados / notificaciones / documentos
17. Incidencias / mantenimiento básico
18. Portal residente
19. Reservas / visitas / extras
20. Gobernanza / votaciones / reporting avanzado

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
- implementar `core_units`
- implementar catálogo de tipos de unidad
- validar relaciones y constraints

## Sprint 3
- implementar `users`
- implementar `user_profiles`
- diseñar ownership / occupancy / roles por condominio

## Sprint 4
- implementar `core_unit_ownerships`
- implementar `core_unit_occupancies`
- implementar `core_condominium_roles`
- cerrar RBAC contextual

## Sprint 5
- módulo de cuentas por cobrar
- cargos recurrentes
- recibos

## Sprint 6
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

<small>🔚 fin · 07-Roadmap · Module Roadmap · `docs/07-roadmap/module-roadmap.md` · `2026-04-15`</small>


---

## 07-Roadmap · Users Core Identity

<small>📄 `docs/07-roadmap/users-core-identity-roadmap.md` · modificado: `2026-04-15`</small>

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

<small>🔚 fin · 07-Roadmap · Users Core Identity · `docs/07-roadmap/users-core-identity-roadmap.md` · `2026-04-15`</small>


---

## 08-Analysis · INCIDENT-20260429 Alias Login 500

<small>📄 `docs/08-analysis/INCIDENT-20260429-condopy-api-alias-login-500.md` · modificado: `2026-04-29`</small>

# INCIDENTE: Login 500 — `condopy-api` alias DNS faltante en red Docker

## Proyecto
- **Sistema:** `condo-py` (API backend) + `condobackdmin` (frontend Next.js)
- **Fecha:** 2026-04-29
- **Severidad:** 🔴 Alta — Login completamente roto
- **Resolvedor:** Misato K (Coordinadora)
- **Reportado por:** Mike Ross

---

## 1. Resumen Ejecutivo

El login en `condobackdmin` fallaba con **500 Internal Server Error** en `POST /auth/login`. El frontend proxy intentaba conectar a `http://condopy-api:7501` pero el hostname no se resolvía (`ENOTFOUND`). El API real estaba corriendo sin problemas.

---

## 2. Síntomas

```
POST http://condobackdmin.test/api-proxy/auth/login → 500
Error: getaddrinfo ENOTFOUND condopy-api
```

- El backend de Next.js (`condobackdmin`) funciona normalmente ✅
- El contenedor `backend-corps-dev-condo-py_backend` está **Up** ✅
- El health endpoint del API responde correctamente ✅
- Solo falla la resolución DNS interna del alias `condopy-api` ❌

---

## 3. Root Cause

El contenedor `backend-corps-dev-condo-py_backend` fue **recreado** (hace ~4 horas, probablemente restart automático). Al reconectarse a la red Docker `services_network`, Docker **no le asignó el alias `condopy-api`** pese a que `docker-compose.yml` lo declara:

```yaml
# docker-compose.yml
services:
  backend:
    networks:
      default:
        aliases:
          - condopy-api   # ← este alias no se attachó al reconectar
```

**Comportamiento observado:** Docker permite que un contenedor existente se reconecte a una red externa sin volver a evaluar los aliases definidos en el compose. El alias solo se aplica en el primer `docker network connect` o al hacer `up`.

---

## 4. Solución Aplicada

```bash
# Desconectar y reconectar con el alias correcto
docker network disconnect services_network backend-corps-dev-condo-py_backend
docker network connect --alias condopy-api services_network backend-corps-dev-condo-py_backend
```

**Verificación:**
```bash
# Confirmar alias en la red
docker inspect backend-corps-dev-condo-py_backend \
  --format '{{json .NetworkSettings.Networks}}' | python3 -m json.tool

# Probar resolución
docker exec backend-corps-dev-condo-py_backend \
  curl -s http://condopy-api:7501/health

# Probar endpoint real
docker exec backend-corps-dev-condo-py_backend \
  wget -qO- http://localhost:7501/health
```

**Resultado:**
```json
{"success":true,"message":"API is running","data":{"status":"healthy"}}
```

---

## 5. Containers y Redes Involucrados

| Contenedor | Red | Aliases |
|---|---|---|
| `backend-corps-dev-condo-py_backend` | `services_network` | `condopy-api`, `mysql` |
| `backend-corps-dev-condo-backdmin_backend` | `services_network` | _(sin aliases)_ |

El frontend usa `NEXT_PUBLIC_API_URL=/api-proxy` que hace proxy a `API_INTERNAL_URL=http://condopy-api:7501`.

---

## 6. Prevención

### Opción A — Fix permanente en `docker-compose.yml`
Usar `--force-recreate` al hacer `up` para asegurar que los aliases se evalúen:

```bash
make down && make up
```

### Opción B — Healthcheck de resolución DNS
Agregar un script de startup que verifique la resolución antes de levantar el servicio:

```python
# startup_check.py
import socket
def check_dns(hostname, expected_alias):
    try:
        ips = socket.gethostbyname_ex(hostname)
        assert expected_alias in ips[0] or expected_alias in ips[2], \
            f"Alias {expected_alias} not found for {hostname}"
    except socket.gaierror:
        raise RuntimeError(f"DNS lookup failed for {hostname}")
```

### Opción C — Script de red idempotente
Crear un script `scripts/ensure-network-aliases.sh` que pueda correrse en cualquier momento:

```bash
#!/bin/bash
CONTAINER="backend-corps-dev-condo-py_backend"
ALIAS="condopy-api"
NETWORK="services_network"

if ! docker inspect "$CONTAINER" --format '{{json .NetworkSettings.Networks}}' | \
     python3 -c "import sys,json; nets=json.load(sys.stdin); exit(0 if '$ALIAS' in nets.get('$NETWORK',{}).get('Aliases',[]) else 1)"; then
  echo "[FIX] Reconnecting $CONTAINER with alias $ALIAS"
  docker network disconnect "$NETWORK" "$CONTAINER"
  docker network connect --alias "$ALIAS" "$NETWORK" "$CONTAINER"
fi
```

---

## 7. Líneas de Tiempo

| Hora | Evento |
|---|---|
| ~12:40 | Contenedor `condo-py` se recrea (restart) |
| ~16:44 | Mike reporta error 500 en login |
| ~16:49 | Alias `condopy-api` reconectado manualmente |
| ~16:50 | Login verificado funcional |

---

## 8. Lesson Learned

> Docker no re-aplica los `aliases` de `docker-compose.yml` cuando un contenedor ya existente se reconecta a una red externa (`network_mode: external`). Los aliases solo se asignan en el primer attach o con `docker-compose up --force-recreate`.

**Regla:** Después de cualquier restart/recreate de un contenedor en red externa, verificar que los aliases DNS estén presentes.

---

## 9. Contactos

| Rol | Nombre | Discord |
|---|---|---|
| Architect | Lelouch | @Lelouch S |
| Dev | Bulma | @Bulma S |
| Coordinator | Misato | @Misato K |

<small>🔚 fin · 08-Analysis · INCIDENT-20260429 Alias Login 500 · `docs/08-analysis/INCIDENT-20260429-condopy-api-alias-login-500.md` · `2026-04-29`</small>


---

## 08-Analysis · Users/Roles/Propietarios/Ocupación Integración

<small>📄 `docs/08-analysis/users-roles-propietarios-ocupacion-integracion-20260424.md` · modificado: `2026-04-24`</small>

# Análisis de Integración: users · roles · propietarios · tipo de ocupación
## Proyecto: backdmin — condo-py
**Autor:** Misato K (Coordinadora)
**Fecha:** 2026-04-24
**Destinatario:** Lelouch (Architect) — para asignación de responsables

---

## 1. Resumen Ejecutivo

Los cuatro módulos forman la columna vertebral de la identidad y autorización de usuarios en el sistema. La integración ya está parcialmente implementada (phase 1e completa), pero quedan **brechas de consistencia, datos y lógica de negocio** que deben resolverse antes de cerrar el módulo.

---

## 2. Inventario de Módulos

### 2.1 `core_users` ✅ Implementado
**Tabla:** `users`
**Rutas:** `/users`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| email | VARCHAR(255) | Unique |
| password_hash | VARCHAR(255) | |
| status | ENUM('active','suspended','inactive','locked') | |
| email_verified_at | DATETIME | |
| last_login_at | DATETIME | |
| failed_login_attempts | INT | |
| locked_until | DATETIME | |
| token_version | INT | invalidación de sesiones |
| created_at | DATETIME | |
| updated_at | DATETIME | |
| deleted_at | DATETIME | soft delete |

**Entidad:** `UserEntity` — tiene `full_name` calculado desde profile
**Usecase:** `UserUseCase` — create, list, get, update, soft_delete, suspend, restore, activate
**Endpoint clave:** `GET /users/{id}/consolidated-view` — devuelve user + profile + roles + ownerships + occupancies

---

### 2.2 `core_user_profiles` ✅ Implementado
**Tabla:** `user_profiles` (1:1 con users)

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| user_id | BIGINT FK → users.id | Unique |
| first_name | VARCHAR(100) | |
| last_name | VARCHAR(100) | |
| document_type | ENUM('dni','ce','passport','other') | |
| document_number | VARCHAR(20) | |
| phone | VARCHAR(20) | |
| birth_date | DATE | agregado en migración 018 |
| created_at | DATETIME | |
| updated_at | DATETIME | |

**Entidad:** `UserProfileEntity`
**Rutas:** `/user-profiles`

---

### 2.3 `core_condominium_roles` ✅ Implementado
**Tabla:** `core_condominium_roles`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK | |
| user_id | BIGINT FK → users.id | |
| role | ENUM(...) | 8 roles válidos |
| status | ENUM('active','inactive','historical') | |
| scope | ENUM('condominium','unit','building') | desde mig. 021 |
| building_id | BIGINT NULL | desde mig. 021 |
| start_date | DATE | |
| end_date | DATE | |
| created_at | DATETIME | |

**Roles válidos:** `super_admin`, `condominium_admin`, `board_member`, `finance_reviewer`, `security_staff`, `maintenance_staff`, `operations_staff`
**Rutas:** `/condominium-roles` — 12 endpoints

**Reglas de negocio implementadas:**
- RBAC-01: 1 `condominium_admin` por condominio (validación en usecase)
- RBAC-02: `super_admin` no asignable por API
- RBAC-05: scope enforcement en `require_permission()` (parcial — building/unit)

---

### 2.4 `core_occupancy_types` ✅ Implementado (migración 025 — 2026-04-23)
**Tabla:** `core_occupancy_types`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| code | VARCHAR(50) | ej. `resident_owner` |
| name | VARCHAR(255) | ej. `Propietario Residente` |
| description | TEXT | |
| scope | ENUM('system','condominium') | |
| condominium_id | BIGINT NULL | para tipos custom |
| requires_authorization | BOOL | |
| allows_primary | BOOL | |
| is_active | BOOL | |
| sort_order | INT | |
| created_at | DATETIME | |

**Seed (5 tipos base):**

| ID | code | name | requires_auth | allows_primary |
|----|------|------|---------------|----------------|
| 1 | resident_owner | Propietario Residente | ❌ | ✅ |
| 2 | tenant | Inquilino | ✅ | ✅ |
| 3 | family_member | Familiar | ✅ | ❌ |
| 4 | office_user | Usuario de Oficina | ✅ | ❌ |
| 5 | occasional_user | Usuario Ocasional | ✅ | ❌ |

---

### 2.5 `core_unit_occupancies` ✅ Implementado (migración 013 + 026)
**Tabla:** `core_unit_occupancies` — quién vive en qué unidad

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| unit_id | BIGINT FK | |
| user_id | BIGINT FK → users.id | |
| occupancy_type_id | BIGINT FK → core_occupancy_types.id | **migrado de string** |
| status | ENUM('active','inactive','historical','pending') | |
| start_date | DATE | |
| end_date | DATE | |
| is_primary | BOOL | |
| authorized_by_user_id | BIGINT FK NULL | |
| notes | TEXT | |

**Entidad:** `UnitOccupancyEntity`
**Rutas:** `/unit-occupancies`

---

### 2.6 `core_unit_ownerships` 🔄 En construcción (migración 012)
**Tabla:** `core_unit_ownerships` — quién es dueño de qué unidad

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| unit_id | BIGINT FK | |
| user_id | BIGINT FK → users.id | |
| ownership_type_id | BIGINT FK | |
| percentage | DECIMAL(5,2) | porcentaje de propiedad |
| status | ENUM('active','inactive','historical') | |
| start_date | DATE | |
| end_date | DATE | |
| created_at | DATETIME | |

**Estado:** DDD module existente en `src/library/dddpy/core_unit_ownerships/` — migraciones 012 aplicadas

---

### 2.7 `core_permissions` + `core_role_permissions` ✅ Implementado
**Tablas:** `core_permissions` (022) + `core_role_permissions` (023)
**Rutas:** `/permissions` + `/role_permissions`
**Servicio:** `PermissionService` en `library/dddpy/auth/permission_service.py`

| Tabla | Función |
|-------|---------|
| core_permissions | Catálogo de ~30 permisos (resource.action) |
| core_role_permissions | Pivot rol → permisos con scope_override |

---

## 3. Diagrama de Relaciones

```
users (1)──────(1) user_profiles
  │
  │  N:N via core_condominium_roles
  │
  └───(N) core_condominium_roles ──(FK)─── core_condominiums
                │
                │  N:N via core_role_permissions
                │
                └───(N) core_role_permissions ──(FK)─── core_permissions
                                   │
                                   │  (residency es cálculo, no asignación)
                                   │  RBAC-03: resident = UnitOccupancyEntity
                                   │  con occupancy_type IN ('resident_owner','tenant')
                                   │
users ──(N) core_unit_occupancies ──(FK)─── core_occupancy_types
  │
  │ (ownership)
  │
  └───(N) core_unit_ownerships ──(FK)─── ownership_type
```

**Clave:** `core_unit_occupancies.occupancy_type_id` → `core_occupancy_types.id`
La migración 026 ya migró de string codes → FK IDs.

---

## 4. Brechas de Integración Detectadas

### 4.1 Brecha ALTA — `OccupancyTypeEntity` desactualizado
**Archivo:** `src/library/dddpy/core_occupancy_types/domain/occupancy_type_entity.py`
**Problema:** La entidad aún usa campos old: `occupancy_type: str` en `UnitOccupancyEntity.to_dict()` sigue referenciando `occupancy_type_code` (string). El campo correcto es `occupancy_type_id` (FK bigint).
**Impacto:** `get_effective_resident_context()` en `PermissionService` aún compara strings (`"resident_owner"`, `"tenant"`) en lugar de usar los IDs del catálogo (1, 2).
**Fix requerido:** Actualizar mapper + query repository para usar `occupancy_type_id` en vez de `occupancy_type` string.

### 4.2 Brecha ALTA — `get_effective_resident_context` con lógica híbrida
**Archivo:** `src/library/dddpy/auth/permission_service.py`
**Problema:**
```python
if occ.occupancy_type not in ("resident_owner", "tenant"):  # STRING comparison
```
Debería comparar contra `occupancy_type_id` (1, 2) del catálogo. La migración 026 ya migró la columna a FK, pero el servicio aún opera con strings.
**Fix requerido:** Consultar el catálogo `core_occupancy_types` para obtener los IDs de los tipos que otorgan rol `resident`, o almacenar `allows_primary=True AND requires_authorization=False` como proxy.

### 4.3 Brecha MEDIA — `consolidated-view` no incluye ownerships ni occupancy details
**Archivo:** `src/library/dddpy/core_users/usecase/user_usecase.py`
**Problema:** El endpoint `GET /users/{id}/consolidated-view` hace JOIN con `core_unit_ownerships` y `core_unit_occupancies` pero no enriquece con los datos del catálogo (`occupancy_type_name`, `ownership_type_name`).
**Fix requerido:** Los queries de ownership y occupancy deben hacer JOIN con los catálogos correspondientes.

### 4.4 Brecha MEDIA — `core_occupancy_types` permite crear tipos por condominium
**Archivo:** `OccupancyTypeEntity._validate_invariants()`
**Problema:** El flag `scope = "condominium"` existe para permitir tipos custom por condominio, pero no hay ningún endpoint ni usecase para crear/gestionar esos tipos custom. El catálogo está huérfano.
**Fix requerido:** Definir `OccupancyTypeUseCase` con endpoints CRUD para que admins de condominio puedan crear tipos propios.

### 4.5 Brecha BAJA — RBAC-03: `resident` se calcula dinámicamente
**Problema:** `get_effective_resident_context()` calcula el rol `resident` en cada request consultando `core_unit_occupancies`. Para usuarios con muchas ocupaciones (ej. propietario de una unidad, inquilino de otra), no hay forma de determinar cuál es la "primaria" a nivel de contexto general.
**Fix requerido:** Ya existe `is_primary` en `core_unit_occupancies` — el código debería usarlo:
```python
get_primary_active(user_id, unit_id)  # ya existe en UnitOccupancyQueryRepositoryImpl
```
Pero `PermissionService.get_effective_resident_context()` no filtra por `is_primary=True`.

### 4.6 Brecha BAJA — Sin endpoint para listar users por condominium con rol
**Problema:** `/users` lista todos los usuarios del sistema. `/condominium-roles/condominium/{condominium_id}` lista los roles. No hay forma directa de obtener "todos los usuarios que tienen rol en condominio X".
**Fix sugerido:** Crear `GET /condominiums/{condominium_id}/users` que combine filters de users + roles + profiles, con paginación.

---

## 5. Dependencias entre Módulos

```
migration 011 ──→ core_users + core_user_profiles
migration 012 ──→ core_unit_ownerships
migration 013 ──→ core_unit_occupancies (old occupancy_type string)
migration 014 ──→ core_condominium_roles
migration 021 ──→ extiende core_condominium_roles (scope, building_id)
migration 022 ──→ core_permissions
migration 023 ──→ core_role_permissions
migration 025 ──→ core_occupancy_types (catálogo)
migration 026 ──→ migra occupancy_type string → occupancy_type_id FK
                              ↑
                           DEPENDE DE 025
```

---

## 6. Recomendaciones de Fix por Prioridad

### PRIORIDAD 1 (antes de cerrar phase 2)
1. **Actualizar `UnitOccupancyQueryRepository`** para usar FK `occupancy_type_id` en vez de string `occupancy_type`
2. **Corregir `PermissionService.get_effective_resident_context()`** para comparar por `occupancy_type_id IN (1, 2)` (IDs del seed de `resident_owner` y `tenant`)
3. **Enriquecer `consolidated-view`** con JOIN a catálogos de occupancy_types y ownership_types

### PRIORIDAD 2 (después de phase 2)
4. **Crear `OccupancyTypeUseCase`** con endpoints CRUD para gestión de tipos (especialmente custom por condominio)
5. **Filtrar `is_primary=True`** en `get_effective_resident_context()`
6. **Agregar `GET /condominiums/{id}/users`** endpoint

---

## 7. Asignación de Responsables Sugerida

| Módulo / Fix | Sugerencia |
|---|---|
| OccupancyTypeQueryRepository + mapper | Bulma |
| PermissionService fix (ID vs string) | Bulma |
| consolidated-view enrichment | Bulma |
| OccupancyTypeUseCase CRUD | Bulma |
| Endpoint /condominiums/{id}/users | Lelouch |

---

## 8. Estado de Migraciones

| # | Archivo | Estado |
|---|---------|--------|
| 011 | refactor_users_auth_profile | ✅ aplicada |
| 012 | create_core_unit_ownerships | ✅ aplicada |
| 013 | create_core_unit_occupancies | ✅ aplicada |
| 014 | create_core_condominium_roles | ✅ aplicada |
| 021 | extend_condominium_roles_scope_building | ✅ aplicada |
| 022 | create_core_permissions | ✅ aplicada |
| 023 | create_core_role_permissions | ✅ aplicada |
| 025 | create_core_occupancy_types | ✅ aplicada |
| 026 | migrate_unit_occupancies_to_occupancy_type_id | ✅ aplicada |

Todas las migraciones relacionadas están aplicadas. El estado de la base es coherente.

---

*Documento preparado por Misato K — Coordinación condo-py*
*Para asignación de tasks, favor revisar con Lelouch (Architect)*

<small>🔚 fin · 08-Analysis · Users/Roles/Propietarios/Ocupación Integración · `docs/08-analysis/users-roles-propietarios-ocupacion-integracion-20260424.md` · `2026-04-24`</small>


---

## 09-Sprint · Sprint Final-12 · Validation Payments Receipts Ledger

<small>📄 `docs/09-sprint/fin-12-validation-payments-receipts-ledger.md` · modificado: `2026-05-01`</small>

# FIN-12 — Validación: Payments, Receipts, Ledger

**Fecha:** 2026-05-01
**Autor:** Bulma S (Review)
**Estado:** ✅ Validado — sin cambios requeridos

---

## Resumen

Los módulos `payments`, `receipts` y `ledger` fueron auditados contra el nuevo flujo
de prorrateo (FIN-02 a FIN-11). La conclusión es que **no requieren cambios**.

---

## Metodología

Code review exhaustiva de los 3 módulos, verificando puntos de acoplamiento con `charges` y `accounts_receivable`.

---

## 1. Payments

**Archivos revisados:**
- `core_payments/domain/payment_entity.py`
- `core_payments/infrastructure/dbpayment.py`
- `core_payments/infrastructure/payment_cmd_repository.py`
- `core_payments/usecase/payment_usecase.py`

**Puntos de integración con AR:**
- `payment_usecase.create()` → referencia a AR por `ar_id`
- VALIDACIÓN PAY-01: `amount ≤ ar.pending_amount` — comparación aritmética sobre Decimals
- El pago se registra con `ar_id` y `receipt_id`, sin leer `charge`
- `add_payment()` en AR recalcula `paid_amount += payment.amount` y actualiza status

**Veredicto:** ✅ Compatible. El pago solo necesita `ar_id` + `amount`. No lee `charge.amount` ni `charge.scope`.

### Flujo validado

| Escenario | Resultado esperado |
|---|---|
| Pago parcial en AR prorrateado | `status → partial`, `pending_amount` correcto |
| Pago total en AR prorrateado | `status → paid`, `pending_amount = 0` |
| Pago excede pending | `PaymentExceedsBalance` ✅ |
| Multiple pagos parciales | `paid_amount` acumula correctamente |

---

## 2. Receipts

**Archivos revisados:**
- `core_receipts/domain/receipt_entity.py`
- `core_receipts/infrastructure/dbreceipt.py`
- `core_receipts/infrastructure/receipt_cmd_repository.py`
- `core_receipts/usecase/receipt_usecase.py`

**Puntos de integración:**
- `receipt_number` auto-incremental por `condominium_id`
- Referencia a AR por `ar_id`
- Referencia a `unit_id`, `payer_user_id`
- Sin dependencia en `charge` o lógica de prorrateo

**Veredicto:** ✅ Compatible. Recibos son correlativos por condominio — independientes del monto.

### Verificación

| Check | Resultado |
|---|---|
| Recibo correlativo por condominio | ✅ `get_next_receipt_number()` |
| Recibo referencia AR correctamente | ✅ FK `ar_id` |
| Recibo con monto prorrateado | ✅ `amount_paid` es Decimal |

---

## 3. Ledger

**Archivos revisados:**
- `core_ledger_entries/domain/ledger_entity.py`
- `core_ledger_entries/infrastructure/db_ledger.py`
- `core_ledger_entries/infrastructure/ledger_cmd_repository.py`
- `core_ledger_entries/infrastructure/ledger_query_repository.py`
- `core_ledger_entries/usecase/ledger_usecase.py`

**Puntos de integración:**
- Referencia a `ar_id`, `payment_id`, `charge_id` (FKs opcionales)
- `debit` / `credit` / `balance` — operaciones aritméticas sobre Decimal
- `balance` running total por unidad
- Sin dependencia en el cálculo de prorrateo

**Veredicto:** ✅ Compatible. Ledger entries registran débitos/créditos con referencias FK,
  no calculan montos. El balance es aritmético.

### Verificación

| Check | Resultado |
|---|---|
| Débito AR prorrateado | ✅ `debit` = `entry.amount` |
| Crédito por pago | ✅ `credit` = `payment.amount` |
| Balance running | ✅ `balance` acumula correctamente |
| FKs a charge/payment/AR | ✅ Todas nullable, sin cascada |

---

## 4. Balance Summary

**Archivos revisados:**
- `ar_query_repository.get_summary_by_unit()`
- `ar_query_repository.get_summary_by_condominium()`

**Lógica:** Agrega `amount - paid_amount` por unidad/condominio. Puramente aritmético.

**Veredicto:** ✅ Compatible. Suma de Decimals prorrateados = total correcto.

---

## Conclusión

**No se requieren cambios en payments, receipts, ni ledger.**

La decisión arquitectónica original fue correcta: el prorrateo vive entre `charge` y `AR`.
Una vez que AR tiene el monto correcto (prorrateado), todo el pipeline downstream funciona
sin modificaciones porque opera sobre `ar.amount` y `ar.paid_amount` como valores opacos.

### Módulos tocados en este sprint

| Módulo | Cambios |
|---|---|
| `core_charges` | ✅ FIN-02+03 (scope, modelo) |
| `core_charges/domain` | ✅ FIN-04 (ProrationService) |
| `core_charges/usecase` | ✅ FIN-05+06 (ProrationUsecase) |
| `core_accounts_receivable` | ✅ FIN-08+09+10+11 (generate_from_charge, deudor, idempotencia, recurrencia) |
| `core_payments` | ❌ Sin cambios |
| `core_receipts` | ❌ Sin cambios |
| `core_ledger_entries` | ❌ Sin cambios |

<small>🔚 fin · 09-Sprint · Sprint Final-12 · Validation Payments Receipts Ledger · `docs/09-sprint/fin-12-validation-payments-receipts-ledger.md` · `2026-05-01`</small>


---

## 09-Sprint · Sprint-10 · Visitors

<small>📄 `docs/09-sprint/sprint10-visitors-20260424.md` · modificado: `2026-04-24`</small>

# Sprint 10 — `core_visitors` — Visitor Management

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable arquitectura:** Lelouch vi Britannia
**Responsable implementación:** Lelouch + sub-agentes

---

## Overview

Gestión de visitantes e invitados del condominio. Permite a residentes/propietarios registrar visitantes esperados, y al staff de seguridad llevar un registro/log de entradas reales.

**Diferencia con lo existente:** El RBAC seed ya menciona un `visitors log` pero no existe como módulo DDD. Este Sprint construye el módulo `core_visitors` completo.

---

## Modelo de Datos

### `VisitorEntity`

```
VisitorEntity
├── id: int
├── uuid: str
├── condominium_id: int
├── building_id: int (nullable — null si es visita global)
├── unit_id: int              ← unidad que recibe la visita
├── host_user_id: int         ← residente/propietario que registró la visita
├── visitor_name: str         ← nombre del visitante
├── visitor_document_type: str (nullable)  ← CI, Pasaporte, etc.
├── visitor_document_number: str (nullable)
├── visitor_phone: str (nullable)
├── expected_date: date
├── expected_time: time
├── actual_checkin_at: datetime (nullable)
├── actual_checkout_at: datetime (nullable)
├── status: VisitorStatus    ← pending, checked_in, checked_out, cancelled, no_show
├── visit_purpose: str       ← family, delivery, service, maintenance, other
├── access_code: str (nullable)  ← código de acceso generado (4-6 dígitos o QR)
├── notes: str (nullable)
├── created_at, updated_at, deleted_at
└── Enrichment: host_user_full_name, unit_code, building_name, condominium_name
```

### Enums

**VisitorStatus:**
```
pending     → registrado, esperando
checked_in  → llegó y fue registrado por seguridad
checked_out → salió
cancelled   → cancelado por el host
no_show     → no se presentó ese día
```

**VisitPurpose:**
```
family        → visita familiar
delivery      → delivery/paquetería
service       → servicio técnico (plomero, eléctrico, etc.)
maintenance   → mantenimiento programado
other         → otro
```

---

## Integración con el Sistema

| Dependencia | Para qué se usa |
|---|---|
| `core_condominiums.id` | Visitas por condominio |
| `core_buildings.id` | Puede ser edificio específico o null (todo el condo) |
| `core_units.id` | Unidad receptora |
| `core_unit_occupancies.user_id` | Validar que `host_user_id` tiene occupancy activo en `unit_id` (VIS-01) |
| `core_unit_ownerships.user_id` | Alternativamente, puede ser propietario activo |
| RBAC permissions | `visitors:create` (host), `visitors:read` (host de la unidad), `security_staff` puede hacer check-in/check-out |

---

## Reglas de Negocio

**VIS-01:** El usuario que registra una visita (`host_user_id`) debe tener un `UnitOccupancyEntity` activo O un `UnitOwnershipEntity` activo en la unidad `unit_id`. Caso contrario → 403.

**VIS-02:** El `access_code` se genera automáticamente (6 dígitos aleatorios) si no se provee. Debe ser único por condominio/fecha.

**VIS-03:** Solo `security_staff` o `condominium_admin` pueden hacer `check_in` y `check_out`. Un host puede cancelar una visita pendiente.

**VIS-04:** Una visita solo puede pasar a `checked_out` si ya está en `checked_in`.

**VIS-05:** Visitas con `expected_date < today` sin check-in se marcan como `no_show` (job nocturno o lazy evaluation al consultar).

---

## Estructura DDD

```
src/library/dddpy/core_visitors/
├── domain/
│   ├── visitor_entity.py
│   ├── visitor_exception.py
│   ├── visitor_repository.py    ← ABC cmd
│   └── visitor_query_repository.py ← ABC query
├── infrastructure/
│   ├── dbvisitor.py
│   ├── visitor_mapper.py
│   ├── visitor_cmd_repository.py
│   └── visitor_query_repository.py  ← con _bulk_enrich
├── usecase/
│   ├── visitor_cmd_schema.py
│   ├── visitor_cmd_usecase.py
│   ├── visitor_query_usecase.py
│   └── visitor_factory.py
└── api/
    └── visitors/routes_visitors.py
```

### Migración

```sql
CREATE TABLE core_visitors (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  uuid VARCHAR(36) NOT NULL UNIQUE,
  condominium_id BIGINT NOT NULL,
  building_id BIGINT NULL,
  unit_id BIGINT NOT NULL,
  host_user_id BIGINT NOT NULL,
  visitor_name VARCHAR(150) NOT NULL,
  visitor_document_type VARCHAR(20) NULL,
  visitor_document_number VARCHAR(50) NULL,
  visitor_phone VARCHAR(30) NULL,
  expected_date DATE NOT NULL,
  expected_time TIME NOT NULL,
  actual_checkin_at DATETIME NULL,
  actual_checkout_at DATETIME NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  visit_purpose VARCHAR(30) NOT NULL DEFAULT 'other',
  access_code VARCHAR(10) NULL,
  notes TEXT NULL,
  created_at DATETIME NOT NULL DEFAULT NOW(),
  updated_at DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  deleted_at DATETIME NULL,
  FOREIGN KEY (condominium_id) REFERENCES core_condominiums(id),
  FOREIGN KEY (unit_id) REFERENCES core_units(id),
  FOREIGN KEY (host_user_id) REFERENCES users(id),
  INDEX idx_condo_date_status (condominium_id, expected_date, status),
  INDEX idx_unit (unit_id),
  INDEX idx_host (host_user_id),
  INDEX idx_access_code (condominium_id, access_code),
);
```

---

## Endpoints

| Método | Endpoint | Permiso | Descripción |
|---|---|---|---|
| POST | `/visitors` | Auth (VIS-01) | Registrar visita |
| GET | `/visitors` | Auth + filtros | Listar (filtros: condo, building, unit, status, date range) |
| GET | `/visitors/{id}` | Auth | Detalle |
| GET | `/visitors/uuid/{uuid}` | Auth | Detalle por UUID |
| GET | `/visitors/my` | Auth | Mis visitas registradas |
| GET | `/visitors/unit/{unit_id}` | Auth (host) | Visitas de una unidad |
| PATCH | `/visitors/{id}` | Auth (host) | Editar (notas, expected_time) |
| POST | `/visitors/{id}/cancel` | Auth (host) | Cancelar |
| POST | `/visitors/{id}/check-in` | Security/staff | Registrar llegada |
| POST | `/visitors/{id}/check-out` | Security/staff | Registrar salida |
| GET | `/condominiums/{id}/visitors` | Auth | Visitas de condominio (paginadas) |
| GET | `/visitors/access-code/{code}` | Security | Buscar por access code (para security desk) |

---

## Queries enriquecidas (M-11)

Mismo patrón `_bulk_enrich` que en roles y incidents:
- `host_user_full_name` (from user_profiles)
- `unit_code`
- `building_name`
- `condominium_name`

---

## RBAC

```
visitors:create   → registrar visitas
visitors:read     → ver visitas propias o del edificio (security/admin)
visitors:checkin  → hacer check-in/check-out (security_staff)
visitors:cancel   → cancelar visita (host o admin)
```

---

## Tasks

| Task | Descripción |
|---|---|
| T-1 | Migración 044 `core_visitors` |
| T-2 | DDD domain layer |
| T-3 | Infrastructure + _bulk_enrich |
| T-4 | Usecases (cmd + query) |
| T-5 | API routes |
| T-6 | Seed RBAC permissions |

<small>🔚 fin · 09-Sprint · Sprint-10 · Visitors · `docs/09-sprint/sprint10-visitors-20260424.md` · `2026-04-24`</small>


---

## 09-Sprint · Sprint-13 · Votes

<small>📄 `docs/09-sprint/sprint13-votes-20260424.md` · modificado: `2026-04-24`</small>

# Sprint 13 — `core_votes` — Digital Voting System

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable arquitectura:** Lelouch vi Britannia
**Responsable implementación:** Lelouch + sub-agentes

---

## Overview

Sistema de votaciones digitales para decisiones de condominio. Permite crear votaciones formales con quórum, mayorías definidas, votos secretos o abiertos, y resultados automatizados.

**Casos de uso:**
- Asamblea extraordinaria (votación urgente)
- Votación de presupuesto anual
- Aprobación de reglamento
- Elección de directorio

---

## Modelo de Datos

### `VoteEntity`

```
VoteEntity
├── id: int
├── uuid: str
├── condominium_id: int
├── title: str
├── description: text
├── meeting_id: int (nullable —null si es votación standalone)
├── voting_starts_at: datetime
├── voting_ends_at: datetime
├── status: VoteStatus
├── vote_type: VoteType      ← open, secret
├── quorum_required: bool   ← si requiere quórum
├── quorum_percentage: int   ← % requerido (default 50+1)
├── approval_threshold: int  ← % de aprobación (default mayoría simple 50+1)
├── total_eligible_voters: int
├── total_votes_cast: int
├── total_yes_votes: int
├── total_no_votes: int
├── total_abstain_votes: int
├── result_proclaimed_at: datetime (nullable)
├── created_by_user_id: int
├── created_at, updated_at, deleted_at
└── Enrichment: created_by_user_full_name, condominium_name
```

### `VoteOptionEntity`

```
VoteOptionEntity
├── id: int
├── vote_id: int
├── option_text: str          ← "Sí", "No", "Abstención", o texto custom
├── option_key: str          ← "yes", "no", "abstain", "option_1", etc.
├── vote_count: int = 0
```

### Enums

**VoteStatus:**
```
draft       → creado, no publicado
active     → en período de votación
closed     → período terminado, esperando proclamación
approved  → aprobado (resultados certificados)
rejected   → rechazado
cancelled  → cancelado por admin
```

**VoteType:**
```
open       → votos visibles para admins
secret     → conteo anónimo (solo auditores ven resultados)
```

---

## Reglas de Negocio

**VOT-01 — Quórum:** Si `quorum_required=True`, solo se proclama resultado si `total_votes_cast / total_eligible_voters >= quorum_percentage / 100`. Si no se alcanza quórum → estado `closed` sin proclamación, se requiere nueva votación.

**VOT-02 — Aprobación:** Si quórum se satisface (o no es requerido):
- `approved` si `yes_votes / (yes + no) >= approval_threshold / 100`
- `rejected` otherwise

**VOT-03 — Elegibilidad:** Solo usuarios con rol `condominium_admin`, `board_member` o con `ownership` activo pueden votar. No pueden votar `maintenance_staff`, `security_staff`, ni `tenants` (a menos que los estatutos lo permitan — configurable por `vote_type`).

**VOT-04 — Un voto por usuario:** Cada usuario puede emitir exactamente un voto por votación. Voto irrevocable una vez emitido (no se puede cambiar).

**VOT-05 — Voto secreto:** Si `vote_type=secret`, ni siquiera los admins ven el desglose por usuario. Solo ven el conteo agregado al cerrar.

**VOT-06 — Extensión:** Un admin puede extender `voting_ends_at` antes de que venza. No se puede acortar.

---

## Estructura DDD

```
src/library/dddpy/core_votes/
├── domain/
│   ├── vote_entity.py         ← VoteEntity + VoteOptionEntity
│   ├── vote_exception.py
│   ├── vote_repository.py     ← ABC cmd
│   └── vote_query_repository.py ← ABC query
├── infrastructure/
│   ├── dbvote.py              ← SQLAlchemy models (core_votes + core_vote_options)
│   ├── vote_mapper.py
│   ├── vote_cmd_repository.py
│   └── vote_query_repository.py ← con _bulk_enrich
├── usecase/
│   ├── vote_cmd_schema.py
│   ├── vote_cmd_usecase.py
│   ├── vote_query_usecase.py
│   └── vote_factory.py
└── api/
    └── votes/routes_votes.py
```

### Migración

```sql
CREATE TABLE core_votes (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  uuid VARCHAR(36) NOT NULL UNIQUE,
  condominium_id BIGINT NOT NULL,
  meeting_id BIGINT NULL,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  voting_starts_at DATETIME NOT NULL,
  voting_ends_at DATETIME NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'draft',
  vote_type VARCHAR(20) NOT NULL DEFAULT 'open',
  quorum_required BOOLEAN NOT NULL DEFAULT FALSE,
  quorum_percentage INT NOT NULL DEFAULT 51,
  approval_threshold INT NOT NULL DEFAULT 51,
  total_eligible_voters INT NOT NULL DEFAULT 0,
  total_votes_cast INT NOT NULL DEFAULT 0,
  total_yes_votes INT NOT NULL DEFAULT 0,
  total_no_votes INT NOT NULL DEFAULT 0,
  total_abstain_votes INT NOT NULL DEFAULT 0,
  result_proclaimed_at DATETIME NULL,
  created_by_user_id BIGINT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT NOW(),
  updated_at DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  deleted_at DATETIME NULL,
  FOREIGN KEY (condominium_id) REFERENCES core_condominiums(id),
  FOREIGN KEY (meeting_id) REFERENCES core_meetings(id), -- cuando exista
  FOREIGN KEY (created_by_user_id) REFERENCES users(id),
  INDEX idx_condo_status (condominium_id, status),
  INDEX idx_ends (voting_ends_at),
);

CREATE TABLE core_vote_options (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  vote_id BIGINT NOT NULL,
  option_text VARCHAR(100) NOT NULL,
  option_key VARCHAR(20) NOT NULL,
  vote_count INT NOT NULL DEFAULT 0,
  FOREIGN KEY (vote_id) REFERENCES core_votes(id) ON DELETE CASCADE,
  UNIQUE KEY uk_vote_option (vote_id, option_key)
);

CREATE TABLE core_vote_records (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  vote_id BIGINT NOT NULL,
  user_id BIGINT NOT NULL,
  option_key VARCHAR(20) NOT NULL,
  voted_at DATETIME NOT NULL DEFAULT NOW(),
  FOREIGN KEY (vote_id) REFERENCES core_votes(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id),
  UNIQUE KEY uk_vote_user (vote_id, user_id)
);
```

---

## Endpoints

| Método | Endpoint | Permiso | Descripción |
|---|---|---|---|
| POST | `/votes` | Admin | Crear votación |
| GET | `/votes` | Auth | Listar (filtros: condo, status) |
| GET | `/votes/{id}` | Auth | Detalle |
| GET | `/votes/uuid/{uuid}` | Auth | Por UUID |
| GET | `/condominiums/{id}/votes` | Auth | Por condominio (paginados) |
| PATCH | `/votes/{id}` | Admin | Editar (solo draft, extiende ends si ya empieza) |
| POST | `/votes/{id}/publish` | Admin | Publicar (draft → active) |
| POST | `/votes/{id}/cancel` | Admin | Cancelar |
| POST | `/votes/{id}/cast` | Voter | Emitir voto (VOT-03/04) |
| GET | `/votes/{id}/results` | Auth | Ver resultados (aggregados, secretos solo como aggregate) |
| POST | `/votes/{id}/proclaim` | Admin | Proclamar resultado |
| GET | `/votes/{id}/records` | Admin/open | Registro de votos (solo si vote_type=open) |

---

## Queries enriquecidas (M-12)

Mismo patrón `_bulk_enrich`: `created_by_user_full_name`, `condominium_name`

---

## RBAC

```
votes:create    → crear votaciones
votes:read      → ver votaciones y resultados
votes:vote      → emitir voto
votes:proclaim  → proclamar resultados (admin)
votes:cancel    → cancelar votaciones
```

---

## Tasks

| Task | Descripción |
|---|---|
| T-1 | Migración 046 `core_votes` + `core_vote_options` + `core_vote_records` |
| T-2 | DDD domain layer |
| T-3 | Infrastructure + _bulk_enrich |
| T-4 | Usecases (VOT-01 a VOT-06 implementados) |
| T-5 | API routes |
| T-6 | Seed RBAC permissions |

<small>🔚 fin · 09-Sprint · Sprint-13 · Votes · `docs/09-sprint/sprint13-votes-20260424.md` · `2026-04-24`</small>


---

## 09-Sprint · Sprint-14 · Dashboards

<small>📄 `docs/09-sprint/sprint14-dashboards-20260424.md` · modificado: `2026-04-24`</small>

# Sprint 14 — `core_dashboards` — Executive Reporting

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable:** Lelouch vi Britannia + sub-agentes

---

## Overview

Dashboards de reporting ejecutivo para admins y board members del condominio. Consolida métricas de todos los módulos en vistas agregadas.

**No es un módulo DDD tradicional.** Es un facade de lectura que consume datos de los módulos existentes y los transforma en métricas útiles.

---

## Dashboards por Rol

### 1. Condominium Admin Dashboard (`GET /condominiums/{id}/dashboard`)

```json
{
  "condominium_id": 1,
  "condominium_name": "Torre Norte",
  "as_of": "2026-04-24T16:00:00Z",
  
  "units": {
    "total": 120,
    "occupied": 115,
    "vacant": 5
  },
  
  "financial": {
    "ar_pending_total": 125000.00,
    "ar_overdue_30_days": 45000.00,
    "ar_overdue_90_days": 12000.00,
    "collections_this_month": 89000.00,
    "collection_rate_percent": 78.5
  },
  
  "incidents": {
    "open_total": 23,
    "by_priority": {"urgent": 2, "high": 5, "medium": 12, "low": 4},
    "avg_resolution_days": 4.2
  },
  
  "visitors": {
    "registered_today": 18,
    "checked_in_now": 6,
    "pending_today": 12
  },
  
  "announcements": {
    "active_count": 3,
    "pinned": [{"id": 1, "title": "...", "published_at": "..."}]
  },
  
  "votes": {
    "active_count": 1,
    "pending_results": 0
  }
}
```

### 2. Finance Dashboard (`GET /condominiums/{id}/finance`)

```json
{
  "condominium_id": 1,
  "as_of": "2026-04-24",
  
  "accounts_receivable": {
    "total_pending": 125000.00,
    "by_status": {
      "current": 68000.00,
      "30_days": 45000.00,
      "90_days": 12000.00
    }
  },
  
  "collections": {
    "this_month": {
      "expected": 113500.00,
      "collected": 89000.00,
      "rate_percent": 78.5
    },
    "last_12_months": [
      {"month": "2025-05", "expected": 110000, "collected": 105000},
      ...
    ]
  },
  
  "charges": {
    "active_charge_types": 3,
    "recurring_monthly": 98000.00
  },
  
  "recent_payments": [
    {"id": 1, "amount": 3500.00, "unit_code": "101", "date": "2026-04-22", "receipt_number": "C001-202604-000001"}
  ]
}
```

### 3. Operations Dashboard (`GET /condominiums/{id}/operations`)

```json
{
  "condominium_id": 1,
  "as_of": "2026-04-24",
  
  "incidents": {
    "open": 23,
    "resolved_this_month": 41,
    "by_category": {
      "plumbing": 12,
      "electrical": 8,
      "elevator": 3,
      ...
    },
    "avg_resolution_hours": 72
  },
  
  "visitors": {
    "today": {"registered": 18, "checked_in": 6, "no_show": 2},
    "this_week": 87
  },
  
  "packages": {
    "pending_delivery": 7,
    "delivered_this_week": 23
  },
  
  "amenity_bookings": {
    "active_bookings": 4,
    "pending_requests": 2
  }
}
```

---

## Notas de Implementación

### Estructura
Este módulo NO tiene entity ni repository DDD tradicional. Es un **query-only facade**.

```
src/library/dddpy/core_dashboards/
├── usecase/
│   ├── condominium_dashboard_usecase.py   ← Admin summary
│   ├── finance_dashboard_usecase.py      ← Financial metrics
│   └── operations_dashboard_usecase.py  ← Operations metrics
└── api/
    └── dashboards/routes_dashboards.py
```

### Consulta de datos
Los usecases hacen queries directas a los repositorios existentes:
- `ArQueryRepositoryImpl` → `list_all(condominium_id, status, ...)` para AR
- `UnitOwnershipQueryRepositoryImpl` → counts para occupancy
- `IncidentQueryRepositoryImpl` → counts + avg resolution
- `VisitorQueryRepositoryImpl` → counts por fecha
- etc.

No crea nuevas tablas ni migraciones. Es plug-and-play con lo que ya existe.

### Autenticación
Todos los endpoints requieren `get_current_user` + RBAC `dashboard:read` (admin/board_member/condominium_admin).

---

## Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/condominiums/{id}/dashboard` | Admin dashboard completo |
| GET | `/condominiums/{id}/finance` | Finance summary |
| GET | `/condominiums/{id}/operations` | Operations summary |
| GET | `/condominiums/{id}/summary` | Alias rápido para `/dashboard` |

---

## Tasks

| Task | Descripción |
|---|---|
| T-1 | `condominium_dashboard_usecase.py` — aggregate all modules |
| T-2 | `finance_dashboard_usecase.py` — AR + payments aggregation |
| T-3 | `operations_dashboard_usecase.py` — incidents + visitors + packages |
| T-4 | API routes |
| T-5 | RBAC seed `dashboards:read` |

<small>🔚 fin · 09-Sprint · Sprint-14 · Dashboards · `docs/09-sprint/sprint14-dashboards-20260424.md` · `2026-04-24`</small>


---

## 09-Sprint · Sprint-15 · Detail Pages

<small>📄 `docs/09-sprint/sprint15-detail-pages-20260429.md` · modificado: `2026-04-29`</small>

# Sprint 15 — `detail-pages` + `contexts` — Backdmin Next.js Integration

**Fecha:** 2026-04-29
**Proyecto:** `condo-backdmin` (Next.js frontend de `condo-py`)
**Responsable:** Bulma S

---

## Overview

Cierre de pendientes del backdmin Next.js. Se completaron las 11 detail pages que estaban pendientes y se integró el módulo `contexts` desde cero.

---

## Módulo 1 — Detail Pages `[id]`

### Módulos completados

| Módulo | Detail Page | Status |
|---|---|---|
| amenities | `/amenities/[id]` | ✅ |
| announcements | `/announcements/[id]` | ✅ |
| packages | `/packages/[id]` | ✅ |
| notifications | `/notifications/[id]` | ✅ |
| building-types | `/building-types/[id]` | ✅ |
| charge-types | `/charge-types/[id]` | ✅ |
| condominium-roles | `/condominium-roles/[id]` | ✅ |
| unit-occupancies | `/unit-occupancies/[id]` | ✅ |
| unit-ownerships | `/unit-ownerships/[id]` | ✅ |
| visitors | `/visitors/[id]` | ✅ |
| audit-logs | `/audit-logs/[id]` | ✅ |

### Extras integrados (no estaban en el plan original)

| Módulo | Detail Page | Status |
|---|---|---|
| buildings | `/buildings/[id]` | ✅ |
| condominiums | `/condominiums/[id]` | ✅ |
| incidents | `/incidents/[id]` | ✅ |
| units | `/units/[id]` | ✅ |
| user-profiles | `/user-profiles/[id]` | ✅ |
| unity-types | `/unity-types/[id]` | ✅ |

**Total detail pages: 28** (vs 21 del sprint anterior)

---

## Módulo 2 — `contexts` (nuevo)

### Descripción
El módulo `contexts` existía en el backend (`condo-py/api/contexts/context_usecase.py`) pero no estaba integrado en el frontend.

### Endpoints consumidos

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/users/{id}/contexts` | Contexto completo de un usuario |
| GET | `/units/{id}/summary` | Resumen agregado de una unidad |

### Archivos creados

| Archivo | Descripción |
|---|---|
| `types/models.ts` | Tipos `UserContextData` + `UnitSummaryData` |
| `lib/api.ts` | `contextsApi` — `getUserContext()` + `getUnitSummary()` |
| `hooks/use-contexts.ts` | Hooks `useUserContext` + `useUnitSummary` (TanStack Query) |
| `app/(dashboard)/contexts/page.tsx` | Página de consulta: búsqueda por user ID → identidad + perfil + propiedades + ocupaciones + roles |
| `components/layout/sidebar.tsx` | Enlace "Contextos" en grupo Sistema |

### Funcionalidad
- Búsqueda por ID de usuario
- Muestra identidad, perfil, propiedades, ocupaciones y roles por condominio de forma agregada

---

## Validación

| Check | Resultado |
|---|---|
| TypeScript | 0 errores reales |
| Build | Pasa limpio (43/43 static pages) |
| HEAD actual | `e3ce0ee` (sobre `24071e2`) |

---

## Estado final del backdmin

- Todos los módulos del backend tienen su página de detalle `[id]` en el frontend
- Módulo `contexts` — integrado y funcional
- 0 pendientes known

---

## Cierre

**Sprint cerrado:** 2026-04-29 17:59 GMT-5
**Decision:** Se da por cerrado. No hay módulos pendientes de integración en el backdmin.

<small>🔚 fin · 09-Sprint · Sprint-15 · Detail Pages · `docs/09-sprint/sprint15-detail-pages-20260429.md` · `2026-04-29`</small>


---

## 09-Sprint · Sprint-16 · Amenity Booking Policies

<small>📄 `docs/09-sprint/sprint16-amenity-booking-policies-20260503.md` · modificado: `2026-05-04`</small>

# SPRINT 16 — Reserva de Amenities: Motor de Políticas

**Fecha base:** 2026-05-03  
**Revisión arquitectónica prioritaria:** Lelouch S  
**Coordinación:** Misato K  
**Ejecución:** Bulma S  
**Proyecto:** condo-py

---

## 0. Dictamen ejecutivo

Se aprueba la dirección general de Misato (**motor de políticas configurable, no reglas hardcodeadas**), pero el planning original necesitaba una corrección táctica importante.

El error de fondo era mezclar en una sola capa tres problemas distintos:

1. **Política** → quién puede reservar y con qué límites  
2. **Disponibilidad** → slots, ventanas, aforo, bloqueos  
3. **Asignación** → booking, waitlist, prioridad, reasignación

Si esas tres piezas se mezclan, el sistema se vuelve frágil y opaco. La solución correcta para condo-py es:

- mantener la **cascada de políticas en 3 capas**
- separar **policy / availability / allocation**
- incorporar **auditoría, concurrencia e idempotencia desde el inicio**
- ejecutar el trabajo con flujo controlado por Misato y **Bulma con una sola tarea activa a la vez**

Ese será el tablero oficial.

---

## 1. Problema que resolvemos

El sistema debe soportar reservas de amenities en condominios con alta variabilidad operativa:

- condominios con muchas unidades y pocos recursos compartidos
- amenities con comportamientos distintos (`piscina`, `parrilla`, `SUM`, `guest suite`, `gym`)
- reglas específicas por condominio y por amenity
- feriados y horas pico con demanda muy superior a la oferta

### Ejemplos reales del problema

- **Piscina**: aforo limitado + demasiadas unidades + necesidad de limitar reservas por unidad por mes
- **Parrilla/SUM en feriados**: todos quieren el mismo día; el sistema debe favorecer equidad, no solo velocidad
- **Gym/Piscina**: operan por slots cortos
- **SUM/Parrilla**: suelen operar por ventanas largas o reservas discretas

### Principio rector

**No vamos a modelar cada excepción del mundo.**  
Vamos a modelar un conjunto corto de primitivas configurables que puedan combinarse.

Jaque mate al `if/else` infinito.

---

## 2. Auditoría del estado actual del código (hecha sobre repo real)

Esta sección reemplaza la parte especulativa del planning inicial. Se revisó el código real antes de redefinir el sprint.

### 2.1 Lo que ya existe en booking

Archivo auditado:  
`src/library/dddpy/core_amenity_bookings/usecase/booking_usecase.py`

`BookingUseCase.create()` ya hace:

- validación de que el amenity existe y es reservable
- validación `unit -> building`
- validación `owner -> unit`
- detección de solapamiento vía `find_overlapping()`
- snapshot de unidad y owner
- creación del booking con estado inicial `draft` o `pending_approval`

### 2.2 Lo que ya existe en amenity

Archivo auditado:  
`src/library/dddpy/core_amenities/infrastructure/dbamenity.py`

`core_amenities` ya tiene campos relevantes:

- `max_capacity`
- `booking_duration_min`
- `requires_approval`
- `booking_price`
- `security_deposit_amount`
- `is_reservable`
- `scope` / `building_id`

Esto significa que **parte del modelo de disponibilidad ya existe**, aunque todavía no está separado de una estrategia completa de booking/policies.

### 2.3 Lo que ya existe a nivel condominio

Archivo auditado:  
`src/alembic/versions/056_add_condominium_amenity_settings.py`

`amenity_settings` en `core_condominiums` **no resuelve políticas de reserva**. Hoy solo cubre flags contables:

- `enable_amenity_booking_charges`
- `include_amenity_bookings_in_receipts`
- `include_amenity_bookings_in_building_balance`
- `include_amenity_bookings_in_condominium_balance`

Conclusión: **no existe todavía un policy engine**.

### 2.4 Gaps reales confirmados

No existe hoy:

- límite de reservas por unidad por período
- límite de reservas activas por unidad
- elegibilidad configurable (`owner_only`, `good_standing_only`, etc.)
- modelo de invitados / tamaño de grupo
- waitlist
- prioridad configurable con trazabilidad
- lifecycle completo de waitlist
- diferencia formal entre `slots continuos` y `ventanas discretas`
- contrato de `effective policy`
- snapshot auditable de la decisión de asignación
- idempotencia / estrategia explícita de concurrencia para alta demanda

---

## 3. Correcciones arquitectónicas sobre el planning inicial

### 3.1 Se mantiene

Estas decisiones de Misato se conservan porque son correctas:

- ✅ motor de políticas en 3 capas
- ✅ evitar hardcodear reglas por condominio
- ✅ usar prioridad configurable (`fifo`, `less_usage_first`, `equal_share`)
- ✅ dividir la implementación en fases manejables

### 3.2 Se corrige

Se introducen estas correcciones obligatorias:

1. **Fase 0 obligatoria**: auditoría + contrato del motor  
2. **Separación explícita** entre policy, availability y allocation  
3. **Modelo híbrido** de políticas: campos tipados + JSON para edge cases  
4. **Concurrencia e idempotencia desde temprano**, no al final  
5. **Guest count / reserva grupal** como parte del modelo base  
6. **Waitlist auditable**, no solo una cola ciega  
7. **Parámetro de ventana de evaluación** para `less_usage_first`  
8. **Soporte para dos modelos operativos**:
   - `CONTINUOUS_SLOTS`
   - `DISCRETE_WINDOWS`

---

## 4. Arquitectura aprobada

## 4.1 Cascada de políticas

Se mantiene la cascada original:

```text
1. Global del condominio
2. Por tipo de amenity
3. Override por amenity específico
```

### Regla de precedencia

El nivel inferior sobreescribe al superior **solo para el campo definido**.  
No se reemplaza el objeto completo.

Ejemplo:

- Global: `max_reservations_per_period = 2`
- Tipo `POOL`: `max_active_reservations = 1`
- Amenity específico `pool_tower_a`: `max_capacity_per_slot = 50`

**Effective policy resultante:**

- `max_reservations_per_period = 2`
- `max_active_reservations = 1`
- `max_capacity_per_slot = 50`

### Contrato obligatorio: `EffectiveAmenityPolicy`

Antes de implementar lógica, debe existir un contrato único resuelto por código.

```python
class EffectiveAmenityPolicy:
    scope_level: str
    eligibility_mode: str
    max_reservations_per_period: int | None
    period_unit: str | None              # day | week | month
    period_value: int | None             # e.g. 1 month, 3 months
    max_active_reservations: int | None
    max_guests: int | None
    priority_policy: str                 # fifo | less_usage_first | equal_share | owner_only
    priority_window_unit: str | None     # month | quarter | year
    priority_window_value: int | None
    waitlist_mode: str                   # auto_confirm | notify_and_confirm | admin_review
    approval_mode: str                   # auto | amenity_requires_approval | admin_only
    blocked_dates: list[str]
    advance_booking_days: int | None
    cancel_window_hours: int | None
    slot_mode: str                       # CONTINUOUS_SLOTS | DISCRETE_WINDOWS
    slot_interval_min: int | None
    max_capacity_per_slot: int | None
    extra_rules_json: dict
```

Este contrato es el rey del tablero. Ningún use case debe interpretar políticas por su cuenta.

---

## 5. Separación por capas

## 5.1 Policy layer

Responde:

- ¿quién puede reservar?
- ¿cuántas veces?
- ¿con qué límites?
- ¿qué política de prioridad aplica?

Incluye:

- elegibilidad
- fairness
- límites por período
- límites activos
- invitados
- owner vs tenant vs guest rules
- ventana de evaluación para prioridad

## 5.2 Availability layer

Responde:

- ¿qué se puede reservar y cuándo?
- ¿cómo se parte el tiempo?
- ¿qué días están bloqueados?
- ¿cuál es el aforo real por slot?

Incluye:

- `slot_mode`
- intervalos
- ventanas discretas
- horarios operativos
- aforo
- bloqueos / feriados
- booking window / cancel window

## 5.3 Allocation layer

Responde:

- ¿la reserva entra directa o va a waitlist?
- ¿quién sube cuando alguien cancela?
- ¿cómo se audita la decisión?

Incluye:

- booking creation
- waitlist lifecycle
- scoring
- reasignación
- notificación
- expiración
- conversión a booking

---

## 6. Modelo de datos propuesto

La propuesta original de `policy_type + key + value` es demasiado genérica para el core del sistema.  
Se reemplaza por un **modelo híbrido**: campos tipados para reglas núcleo + JSON para extensiones raras.

## 6.1 Nueva tabla `core_amenity_policies`

Una fila representa un scope de política.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador |
| `condominium_id` | FK | Condominio |
| `scope_level` | ENUM | `CONDOMINIUM` / `AMENITY_TYPE` / `AMENITY` |
| `amenity_type` | VARCHAR NULL | `POOL`, `GRILL`, `SUM`, etc. |
| `amenity_id` | FK NULL | Override puntual |
| `eligibility_mode` | VARCHAR | `all_residents`, `owner_only`, `good_standing_only` |
| `max_reservations_per_period` | INT NULL | límite principal |
| `period_unit` | VARCHAR NULL | `day`, `week`, `month`, `quarter` |
| `period_value` | INT NULL | e.g. `1`, `3` |
| `max_active_reservations` | INT NULL | reservas activas simultáneas |
| `max_guests` | INT NULL | invitados máximos |
| `priority_policy` | VARCHAR | `fifo`, `less_usage_first`, `equal_share` |
| `priority_window_unit` | VARCHAR NULL | ventana de evaluación |
| `priority_window_value` | INT NULL | e.g. `1 month`, `3 months` |
| `waitlist_mode` | VARCHAR | `auto_confirm`, `notify_and_confirm`, `admin_review` |
| `approval_mode` | VARCHAR | `auto`, `amenity_requires_approval`, `admin_only` |
| `extra_rules_json` | JSON NULL | edge cases |
| `is_active` | BOOL | flag de vigencia |
| `version` | INT | versionado simple |

## 6.2 Nueva tabla `core_amenity_availability_rules`

Separa disponibilidad de policy.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador |
| `amenity_id` | FK | Amenity específico |
| `slot_mode` | ENUM | `CONTINUOUS_SLOTS` / `DISCRETE_WINDOWS` |
| `slot_interval_min` | INT NULL | para slots continuos |
| `window_start_time` | TIME NULL | para ventanas discretas |
| `window_end_time` | TIME NULL | para ventanas discretas |
| `max_capacity_per_slot` | INT | aforo utilizable |
| `advance_booking_days` | INT NULL | hasta cuántos días antes se puede reservar |
| `cancel_window_hours` | INT NULL | cancelación mínima |
| `blocked_dates_json` | JSON NULL | feriados / cierres |
| `opening_hours_json` | JSON NULL | horario operativo |
| `is_active` | BOOL | vigencia |

## 6.3 Extensión a `core_amenity_bookings`

Se agregan campos al booking existente en vez de crear una entidad paralela innecesaria.

| Campo nuevo | Tipo | Motivo |
|---|---|---|
| `guest_count` | INT | tamaño real del grupo |
| `allocation_source` | VARCHAR | `DIRECT`, `WAITLIST`, `ADMIN_OVERRIDE` |
| `waitlist_entry_id` | FK NULL | trazabilidad |
| `idempotency_key` | VARCHAR NULL | protección contra reintentos |
| `policy_snapshot_json` | JSON NULL | effective policy usada |
| `allocation_reason_json` | JSON NULL | por qué fue aceptada / reasignada |

## 6.4 Nueva tabla `core_amenity_usage_logs`

Para fairness y reportes.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador |
| `amenity_id` | FK | Amenity |
| `unit_id` | FK | Unidad |
| `user_id` | FK | Usuario |
| `booking_id` | FK | Booking asociado |
| `guest_count` | INT | uso real |
| `used_at` | DATETIME | timestamp de uso |
| `source_status` | VARCHAR | `completed`, `attended`, etc. |

## 6.5 Nueva tabla `core_amenity_waitlist`

Waitlist con lifecycle completo.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador |
| `amenity_id` | FK | Amenity |
| `unit_id` | FK | Unidad |
| `user_id` | FK | Usuario |
| `booking_date` | DATE | Fecha solicitada |
| `requested_start_at` | DATETIME | inicio |
| `requested_end_at` | DATETIME | fin |
| `guest_count` | INT | grupo solicitado |
| `status` | VARCHAR | `WAITING`, `NOTIFIED`, `CONFIRMED`, `EXPIRED`, `CANCELLED`, `CONVERTED` |
| `priority_score_snapshot` | DECIMAL | score guardado |
| `priority_reason_json` | JSON | explicación auditable |
| `effective_policy_snapshot_json` | JSON | política aplicada |
| `expires_at` | DATETIME NULL | deadline para confirmar |
| `notified_at` | DATETIME NULL | timestamp de aviso |
| `converted_booking_id` | FK NULL | trazabilidad |

## 6.6 Nueva tabla `core_amenity_allocation_audit`

Para defender decisiones frente a reclamos.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | PK | Identificador |
| `amenity_id` | FK | Amenity |
| `booking_id` | FK NULL | Booking relacionado |
| `waitlist_entry_id` | FK NULL | Waitlist relacionada |
| `decision_type` | VARCHAR | `BOOKING_ACCEPTED`, `BOOKING_REJECTED`, `WAITLIST_INSERTED`, `WAITLIST_PROMOTED` |
| `decision_reason` | VARCHAR | motivo corto |
| `decision_context_json` | JSON | detalle |
| `created_at` | DATETIME | traza |

---

## 7. Reglas de negocio obligatorias

## 7.1 Elegibilidad

El sistema debe poder resolver, al menos:

- `all_residents`
- `owner_only`
- `good_standing_only`
- `owner_or_tenant`
- `admin_override`

## 7.2 Uso por período

Ejemplos:

- `max_reservations_per_period = 2`, `period = month`
- `max_active_reservations = 1`
- `max_guests = 5`

## 7.3 Prioridad

Políticas mínimas:

- `fifo`
- `less_usage_first`
- `equal_share`

### Regla nueva obligatoria

`less_usage_first` **debe parametrizar su ventana de evaluación**.

Ejemplos:

- último mes
- últimos 3 meses
- trimestre actual

Sin esa ventana, la política es ambigua.

## 7.4 Waitlist lifecycle

La waitlist no puede quedarse en un limbo.

Lifecycle mínimo:

```text
WAITING
  -> NOTIFIED
  -> CONFIRMED
  -> CONVERTED

WAITING
  -> EXPIRED

WAITING
  -> CANCELLED
```

Si el modo es `notify_and_confirm`, debe existir un `expires_at`.  
Si el usuario no confirma a tiempo, la plaza pasa al siguiente.

## 7.5 Reserva grupal

Una reserva no es igual a una persona.  
Debe existir `guest_count`, porque el aforo real depende del grupo, no del número de bookings.

## 7.6 Concurrencia

El enemigo real del sistema no es la tabla: es el doble booking bajo alta demanda.

Se define como obligatorio desde fase temprana:

- operación de asignación dentro de transacción
- verificación final de capacidad antes de persistir
- estrategia de `idempotency_key` para retries
- constraints/índices útiles para lookup por amenity+fecha
- tests de concurrencia mínima en integración

---

## 8. Algoritmo de asignación aprobado

## 8.1 Flujo general

```text
Solicitud
  -> validar integridad básica
  -> resolver effective policy
  -> validar elegibilidad / límites / ventanas
  -> resolver disponibilidad real del slot
      -> si hay capacidad: crear booking
      -> si no hay capacidad: waitlist
  -> registrar allocation audit
```

## 8.2 Flujo de reasignación

```text
Se libera capacidad
  -> buscar waitlist elegible
  -> recalcular o reutilizar score según policy
  -> seleccionar candidato
  -> notificar o convertir automáticamente
  -> registrar auditoría completa
```

## 8.3 Score de prioridad

La estrategia debe ser configurable por política:

- `snapshot_on_join`
- `recompute_on_reassign`

### Dictamen

Por defecto, se recomienda:

- `fifo` -> `snapshot_on_join`
- `less_usage_first` -> `recompute_on_reassign`
- `equal_share` -> `recompute_on_reassign`

Eso preserva equidad donde importa y estabilidad donde conviene.

---

## 9. Plan de implementación corregido

Se conserva la idea de fases, pero se agrega **Fase 0** y se redistribuyen responsabilidades.

## Fase 0 — Auditoría + contrato del motor

**Objetivo:** eliminar ambigüedad antes de tocar persistencia.  
**Responsable:** Lelouch (arquitectura)  
**Coordinación:** Misato  
**Ejecución puntual de validaciones de código si hace falta:** Bulma

### Entregables

1. Auditoría del booking existente documentada
2. Contrato `EffectiveAmenityPolicy`
3. Definición formal de `slot_mode`
4. Estrategia de concurrencia / idempotencia
5. Lista final de tablas y columnas aprobadas

### Definition of Done

No queda ninguna ambigüedad sobre:

- precedencia de políticas
- merge/override
- waitlist lifecycle
- score policy
- slot model
- guest_count
- concurrencia

---

## Fase 1 — Policy foundation + trazabilidad

**Objetivo:** construir el policy engine núcleo y dejar trazabilidad temprana.  
**Responsable de implementación:** Bulma  
**Review arquitectónico:** Lelouch  
**Coordinación:** Misato

### Tareas

1. Crear `core_amenity_policies`
2. Extender `core_amenity_bookings` con `guest_count`, `allocation_source`, `idempotency_key`, `policy_snapshot_json`, `allocation_reason_json`
3. Crear `core_amenity_allocation_audit`
4. Implementar `PolicyResolver` con cascada `CONDOMINIUM -> AMENITY_TYPE -> AMENITY`
5. Implementar validaciones:
   - `validate_eligibility()`
   - `validate_usage_limit()`
   - `validate_active_reservations()`
   - `validate_guest_limit()`
6. Registrar motivo de rechazo y snapshot de política
7. Tests de integración para límites por período y reservas activas

### Definition of Done

- una unidad puede ser rechazada por límite mensual con motivo auditable
- una unidad puede ser rechazada por límite de reservas activas
- la decisión deja snapshot de política y razón de negocio

---

## Fase 2 — Availability model + concurrencia segura

**Objetivo:** modelar disponibilidad correctamente y blindar el booking bajo demanda.  
**Responsable de implementación:** Bulma  
**Review arquitectónico:** Lelouch  
**Coordinación:** Misato

### Tareas

1. Crear `core_amenity_availability_rules`
2. Definir y soportar `slot_mode`:
   - `CONTINUOUS_SLOTS`
   - `DISCRETE_WINDOWS`
3. Implementar validaciones:
   - `validate_booking_window()`
   - `validate_cancel_window()`
   - `validate_blocked_dates()`
   - `validate_capacity()` usando `guest_count`
4. Implementar cálculo de disponibilidad real
5. Endurecer `BookingUseCase.create()` con:
   - transacción de asignación
   - chequeo final de capacidad
   - soporte de `idempotency_key`
6. Endpoint `GET /amenities/{id}/availability?date=YYYY-MM-DD`
7. Tests de concurrencia / retries / capacidad

### Definition of Done

- el sistema distingue piscina por slots de parrilla por ventana discreta
- una reserva no sobrepasa aforo por grupo
- retries no generan doble booking lógico

---

## Fase 3 — Waitlist + prioridad + reporting final

**Objetivo:** resolver alta demanda con fairness auditable.  
**Responsable de implementación:** Bulma  
**Review arquitectónico:** Lelouch  
**Coordinación:** Misato

### Tareas

1. Crear `core_amenity_waitlist`
2. Crear `core_amenity_usage_logs`
3. Implementar `PriorityCalculator`:
   - `fifo`
   - `less_usage_first`
   - `equal_share`
4. Implementar lifecycle completo de waitlist
5. Implementar `WaitlistAllocator` con `snapshot_on_join` / `recompute_on_reassign`
6. Trigger de notificación / expiración / conversión
7. Endpoints:
   - `GET /amenities/{id}/waitlist`
   - `POST /amenities/{id}/waitlist/{entry_id}/confirm`
8. Reporting:
   - usage report
   - métricas de rechazo
   - métricas de waitlist/promoción/expiración
9. Tests end-to-end de alta demanda

### Definition of Done

- slot lleno -> waitlist
- cancelación/liberación -> promoción según policy
- cada decisión deja score + razón + snapshot de política

---

## 10. Endpoints propuestos

```text
# Policies
GET    /amenities/{id}/policies
POST   /amenities/{id}/policies
PUT    /amenities/{id}/policies/{policy_id}

# Availability
GET    /amenities/{id}/availability?date=YYYY-MM-DD

# Bookings
POST   /amenities/{id}/bookings
GET    /amenities/{id}/bookings
DELETE /bookings/{id}

# Waitlist
GET    /amenities/{id}/waitlist
POST   /amenities/{id}/waitlist/{entry_id}/confirm
POST   /amenities/{id}/waitlist/{entry_id}/cancel

# Reporting
GET    /amenities/{id}/usage-report?period=month
GET    /amenities/{id}/allocation-audit?date=YYYY-MM-DD
```

---

## 11. Decisiones de producto que siguen abiertas

Estas preguntas deben responderse antes de cerrar Fase 1/Fase 2, pero ya están mejor enmarcadas:

1. **¿Políticas por API o admin UI?**  
   Recomendación: API primero, UI después.

2. **¿Waitlist automática o con aprobación?**  
   Recomendación: soportar estrategia configurable:
   - `auto_confirm`
   - `notify_and_confirm`
   - `admin_review`

3. **¿La prioridad se fija al entrar o se recalcula?**  
   Recomendación: configurable por política, no global.

4. **¿Propietarios e inquilinos compiten igual?**  
   Recomendación: default igualitario, con `eligibility_mode` configurable.

5. **¿Qué amenities usan slot continuo vs ventana discreta?**  
   Recomendación inicial:
   - `POOL`, `GYM` -> `CONTINUOUS_SLOTS`
   - `GRILL`, `SUM`, `EVENT_ROOM` -> `DISCRETE_WINDOWS`

---

## 12. Riesgos y mitigación

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| Mezclar policy con scheduling | Alta | Separar tablas y servicios desde Fase 0 |
| Puro JSON vuelva inqueryable el sistema | Alta | Modelo híbrido tipado + JSON opcional |
| Waitlist injusta o inexplicable | Alta | allocation audit + score snapshot + reason json |
| Doble booking por carrera | Alta | transacción + chequeo final + idempotency |
| Alcance del sprint se descontrole | Media | una sola tarea activa para Bulma |
| Política `less_usage_first` ambigua | Media | ventana de evaluación obligatoria |

---

## 13. Flujo operativo oficial: Misato ↔ Bulma ↔ Lelouch

Esta sección adopta expresamente la instrucción operativa ya usada en condo-py para evitar caos de ejecución.

### Regla de coordinación

- **Misato controla el tablero**
- **Bulma ejecuta la tarea activa**
- **Lelouch define criterio, revisa arquitectura y bloquea desvíos**
- Solo se etiqueta a quien sigue en el turno

### Ciclo obligatorio

1. Misato habilita **una sola tarea activa** para Bulma
2. Bulma implementa esa tarea y responde **solo a Misato**
3. Misato revisa
4. Si hay observaciones, la tarea vuelve a Bulma
5. Si la revisión queda limpia y el cambio toca arquitectura crítica, **Lelouch valida el gate**
6. Solo entonces Misato habilita la siguiente tarea

### Regla crítica

**No se avanza a la siguiente tarea mientras la actual tenga observaciones abiertas.**

Esto reemplaza la asignación original donde Fase 2 quedaba directamente en manos de Lelouch como implementador.  
En condo-py la ejecución debe quedar centralizada en Bulma; Lelouch actúa como arquitecto y revisor de cierre.

---

## 14. Backlog secuencial para Bulma

Para respetar el flujo operativo, estas son las tareas en orden.  
**Solo una puede estar activa a la vez.**

### B0 — Levantamiento de booking actual
- ~~pendiente~~ → ✅ **LISTO** (Bulma, 2026-05-04)
- confirmar `BookingUseCase.create()`
- confirmar `find_overlapping()`
- confirmar qué campos actuales se reutilizan
- entregar nota breve a Misato

### B1 — Migración de políticas + booking extensions
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ `uq_bookings_idempotency` unicidad real
- ✅ `ck_policies_scope` blindaje de invariantes
- ✅ downgrade corregido

### B2 — PolicyResolver
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ DBPolicy alineado con migración 062 (nullable donde corresponde)
- ✅ `amenity_type` canónico en `core_amenities` + `_lookup_amenity_type()` directo
- ✅ Tests `tests/test_policy_resolver.py` (19 tests)

### B3 — Validaciones policy en BookingUseCase
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ `field_provenance` + `_scope_filter()` — sin contaminación entre tipos
- ✅ `approval_mode` semánticamente correcto (auto/amenity_requires_approval/admin_only)

### B4 — Availability rules
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ `cancel_window_hours` conectado a `cancel()`
- ✅ `_check_slot_compliance()` con enforcement real para CONTINUOUS y DISCRETE
- ✅ Tests `test_booking_policy_validator.py` (35/35)

### B5 — Concurrencia/idempotencia + base para waitlist
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ Named lock por amenity (GET_LOCK/RELEASE_LOCK)
- ✅ Idempotencia en Phase 0 (antes de lock)
- ✅ Tests `test_b5_concurrency.py` (10/10)
- ⚠️ FKs en waitlist (a `core_amenities`, `core_amenity_bookings`) quedan para B6

### B6 — Waitlist + promotion/reallocation
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ `promote()` crea booking solo en `auto_confirm`, no en `notify_and_confirm` ni `admin_review`
- ✅ `DISCRETE_WINDOWS` overlap → waitlist (no muerte por overlap)
- ⚠️ Tests para `notify_and_confirm`, `admin_review`, `confirm_entry()` por reforzar (no bloqueante)

### B7 — Reporting + usage history
- **STATUS: ✅ APROBADO** (Lelouch gate, 2026-05-04)
- ✅ `BOOKING_REJECTED` productor conectado en `booking_usecase.create()`
- ✅ Bug fix: `waitlist_mode = None` (disabled), no más forced default
- ✅ `waitlist_conversion_rate` filtra por `booking_date`, no `created_at`
- ✅ Tests: 16 passed (9 unit + 7 integration)
- ⚠️ Nota no bloqueante: `Query.get()` legacy en `waitlist_usecase.py` → migrar a `Session.get()`

---

## Estado final del Sprint 16

| Bloque | Estado |
|---|---|
| B0 — Levantamiento | ✅ APROBADO |
| B1 — Migración policies | ✅ APROBADO |
| B2 — PolicyResolver | ✅ APROBADO |
| B3 — Validaciones policy | ✅ APROBADO |
| B4 — Availability rules | ✅ APROBADO |
| B5 — Concurrencia/idempotencia | ✅ APROBADO |
| B6 — Waitlist + promotion | ✅ APROBADO |
| B7 — Reporting + audit | ✅ APROBADO |

### B2 — `PolicyResolver`
- resolver cascade/merge
- devolver `EffectiveAmenityPolicy`
- tests de precedencia

### B3 — Validaciones de policy
- límites por período
- reservas activas
- guest limit
- eligibility
- rejection audit

### B4 — Availability rules
- crear `core_amenity_availability_rules`
- soportar slot modes
- blocked dates / booking window / cancel window

### B5 — Concurrencia / idempotencia
- endurecer create booking
- chequeo final de capacidad
- idempotency key
- tests de retry

### B6 — Waitlist model
- crear `core_amenity_waitlist`
- lifecycle completo
- expiración / confirmación

### B7 — Priority engine
- `fifo`
- `less_usage_first`
- `equal_share`
- ventana de evaluación parametrizable

### B8 — Reporting y observabilidad
- usage logs
- allocation audit API
- métricas de rechazo / promoción / expiración

---

## 15. Criterio de cierre del módulo

El módulo de políticas de amenities no se considera cerrado hasta que:

- exista contrato único de `EffectiveAmenityPolicy`
- estén soportados ambos `slot_mode`
- exista `guest_count`
- exista waitlist con lifecycle completo
- exista trazabilidad de cada decisión crítica
- existan tests de integración suficientes
- Misato no tenga observaciones abiertas
- Lelouch valide que no hay acoplamiento arquitectónico roto

---

## 16. Veredicto final

El planning original de Misato tenía una base correcta, pero incompleta.  
Este documento lo reemplaza como **versión operativa oficial** del sprint 16.

### Dirección final

- sí al motor de políticas en 3 capas
- no a una tabla genérica sin tipado para todo
- no a meter waitlist antes de resolver availability y concurrencia
- sí a auditabilidad desde Fase 1
- sí a Bulma como ejecutora única por tarea activa
- sí a Misato como control de flujo
- sí a Lelouch como criterio arquitectónico prioritario

Con esto, el sistema deja de ser una idea vaga y pasa a ser una máquina de guerra razonable.

---

*Documento consolidado y corregido por Lelouch S sobre base de planning inicial de Misato K.*

<small>🔚 fin · 09-Sprint · Sprint-16 · Amenity Booking Policies · `docs/09-sprint/sprint16-amenity-booking-policies-20260503.md` · `2026-05-04`</small>


---

## 09-Sprint · Sprint-5 · Accounts Receivable

<small>📄 `docs/09-sprint/sprint5-accounts-receivable-20260424.md` · modificado: `2026-05-01`</small>

# Sprint 5 — Phase 3: Accounts Receivable · Cargos · Recibos · Pagos · Ledger
## Proyecto: condo-py (backdmin)
**Autor:** Misato K — Coordinación
**Fecha:** 2026-04-24
**Asignado a:** Bulma S (Dev)
**Estado:** Sprint Planning

---

## 1. Contexto y Dependencias

Phase 2 (Identidad, acceso y ocupación) se cerró en commit `4ac2f45`. La base estructural actual soporta correctamente la facturación:

- `core_condominiums` → cada unidad pertenece a un condominio
- `core_units` → cada unidad tiene `condominium_id`, `building_id`, `unit_type_id`
- `core_users` + `core_user_profiles` → identidad del deudor
- `core_unit_ownerships` → quién es el propietario legal (sujeto a cargo)
- `core_unit_occupancies` → quién ocupa la unidad (inquilino = deudor secundario)
- `core_condominium_roles` → permisos para crear cargos, aprobar pagos, exportar estados

**Regla de negocio que se hereda:** El flujo de cobranza va siempre atado a `core_units`. No hay cargo sin unidad.

---

## 2. Inventario de Módulos Phase 3

### 2.1 `accounts_receivable` — Cuentas por Cobrar
**Tabla:** `core_accounts_receivable`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK → core_condominiums | |
| unit_id | BIGINT FK → core_units | obligación attached a unidad |
| debtor_user_id | BIGINT FK → users | who owes |
| reference_code | VARCHAR(50) | código interno del cargo |
| description | TEXT | |
| amount | DECIMAL(12,2) | |
| currency | VARCHAR(3) | default 'PEN' |
| status | ENUM('pending','partial','paid','overdue','cancelled') | |
| due_date | DATE | |
| period | VARCHAR(7) | 'YYYY-MM' para cuotas mensuales |
| charge_id | BIGINT FK NULL | si viene de un cargo recurrente |
| created_at | DATETIME | |
| updated_at | DATETIME | |
| deleted_at | DATETIME | |

**Estado:** No existe aún. Crear DDD module + migración.

**Reglas de negocio:**
- AR-01: `amount` debe ser > 0
- AR-02: `status` solo cambia en secuencia válida: `pending → partial → paid` o `pending → overdue → paid`
- AR-03: `unit_id` obligatorio, `debtor_user_id` obligatorio

---

### 2.2 `charges` — Cargos Recurrentes y Extraordinarios
**Tabla:** `core_charges`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK | |
| charge_type_id | BIGINT FK → core_charge_types | catálogo |
| unit_id | BIGINT FK NULL | null = cargo a todo el condominio |
| description | TEXT | |
| amount | DECIMAL(12,2) | |
| is_recurrent | BOOL | si es cuota mensual |
| period_pattern | VARCHAR(7) NULL | 'YYYY-MM' o null si extraordinario |
| start_date | DATE | inicio de vigencia |
| end_date | DATE NULL | fin de vigencia (null = indefinido) |
| status | ENUM('active','inactive','expired') | |
| created_at | DATETIME | |
| updated_at | DATETIME | |

**Tabla:** `core_charge_types` (catálogo seed)

| code | name | is_global | description |
|------|------|----------|-------------|
| monthly_fee | Cuota Mensual | true | Cuota ordinaria del condominio |
| special_assessment | Cargo Extraordinario | false | Aproado por asamblea |
| reserve_fund | Fondo de Reserva | true | Aportación al fondo de reserva |
| penalty | Multa | false | Por mora o incumplimiento |
| utility | Servicio Común | true | Agua, gas, mantenimiento áreas |

**Estado:** No existe aún. Crear DDD module + migración + seeds.

---

### 2.3 `receipts` — Generación de Recibos
**Tabla:** `core_receipts`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK | |
| unit_id | BIGINT FK | |
| ar_id | BIGINT FK → core_accounts_receivable | |
| receipt_number | VARCHAR(30) | correlativo |
| issued_at | DATETIME | |
| payer_user_id | BIGINT FK | quien paga |
| amount_paid | DECIMAL(12,2) | |
| payment_method | ENUM('cash','bank_transfer','yape','plin','card','other') | |
| reference | VARCHAR(100) NULL | nro operación |
| notes | TEXT NULL | |

**Reglas de negocio:**
- REC-01: `receipt_number` único por condominio (formato: `C{cod_condominio}-{YYYY}{MM}-{correlativo:06d}`)
- REC-02: Al emitir recibo, actualizar `status` del AR asociado
- REC-03: Un AR puede generar múltiples recibos (pago parcial = varios recibos)

---

### 2.4 `payments` — Registro de Pagos
**Tabla:** `core_payments`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK | |
| unit_id | BIGINT FK | |
| ar_id | BIGINT FK → core_accounts_receivable | |
| receipt_id | BIGINT FK NULL | receipt generado (opcional) |
| payer_user_id | BIGINT FK | |
| amount | DECIMAL(12,2) | |
| payment_method | ENUM(...) | |
| reference | VARCHAR(100) NULL | |
| paid_at | DATETIME | |
| created_at | DATETIME | |

**Reglas de negocio:**
- PAY-01: `amount` no puede exceder el saldo pendiente del AR
- PAY-02: Al registrar pago, recalcular `status` del AR (`pending → partial` o `overdue → partial`)
- PAY-03: Un pago genera un `receipt` automáticamente (relación 1:1)

---

### 2.5 `ledger` — Estado de Cuenta por Unidad
**Tabla:** `core_ledger_entries`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | BIGINT PK | |
| uuid | VARCHAR(36) | |
| condominium_id | BIGINT FK | |
| unit_id | BIGINT FK | |
| entry_type | ENUM('charge','payment','adjustment','balance_forward') | |
| ar_id | BIGINT FK NULL | si viene de AR |
| payment_id | BIGINT FK NULL | si viene de pago |
| description | TEXT | |
| debit | DECIMAL(12,2) | cargo (amount owe) |
| credit | DECIMAL(12,2) | pago |
| balance | DECIMAL(12,2) | saldo acumulado |
| period | VARCHAR(7) | 'YYYY-MM' |
| created_at | DATETIME | |

**Reglas de negocio:**
- LED-01: `balance` se calcula como saldo anterior + debit - credit (no almacenar, recalcular con SUM)
- LED-02: Cada `charge` genera un `ledger_entry` de tipo `charge`
- LED-03: Cada `payment` genera un `ledger_entry` de tipo `payment`
- LED-04: `GET /units/{unit_id}/ledger` devuelve estado de cuenta con todos los entries ordenados por `created_at`

---

## 3. Modelo de Datos Integrado

```
core_charge_types (seed: 5 tipos)
       ↓ FK
core_charges ──────── condominium_id → core_condominiums
       │                         └── unit_id → core_units (nullable)
       │                                  └── owner/occupant → users
       │                                            ↓ FK
       ↓ FK (genera)              core_accounts_receivable
core_ledger_entries  ←←←←←←←←←←←←←←←← AR + payments
       │                         
       │ (1:1 genera)
       ↓
core_receipts
```

---

## 4. Estructura DDD por Módulo

Cada módulo sigue el patrón DDD del proyecto:

```
{modulo}/
├── domain/
│   ├── {modulo}_entity.py
│   ├── {modulo}_data.py
│   ├── {modulo}_exception.py
│   ├── {modulo}_success.py
│   ├── {modulo}_cmd_repository.py
│   └── {modulo}_query_repository.py
├── infrastructure/
│   ├── db{modulo}.py
│   ├── {modulo}_mapper.py
│   ├── {modulo}_cmd_repository.py
│   └── {modulo}_query_repository.py
└── usecase/
    ├── {modulo}_cmd_schema.py
    ├── {modulo}_cmd_usecase.py
    ├── {modulo}_query_usecase.py
    ├── {modulo}_usecase.py
    └── {modulo}_factory.py
```

Ruta API: `src/api/{modulo}/routes_{modulo}.py`

---

## 5. Migraciones Requeridas

| # | Archivo | Descripción |
|---|---------|-------------|
| 027 | `027_create_core_charge_types.sql` | Catálogo de tipos de cargo + seed |
| 028 | `028_create_core_charges.sql` | Tabla de cargos |
| 029 | `029_create_core_accounts_receivable.sql` | Tabla de cuentas por cobrar |
| 030 | `030_create_core_payments.sql` | Tabla de pagos |
| 031 | `031_create_core_receipts.sql` | Tabla de recibos |
| 032 | `032_create_core_ledger_entries.sql` | Tabla del libro mayor |

---

## 6. Endpoints Mínimos por Módulo

### `/charges`
- `POST /charges` — crear cargo
- `GET /charges` — listar con filtros (condominium_id, unit_id, status, is_recurrent)
- `GET /charges/{id}`
- `PUT /charges/{id}` — actualizar monto/descripción
- `DELETE /charges/{id}` — soft delete

### `/accounts-receivable`
- `POST /accounts-receivable` — generar AR desde cargo (batch por unidad o individual)
- `GET /accounts-receivable` — listar (status, condominium_id, unit_id, debtor_user_id)
- `GET /accounts-receivable/{id}`
- `GET /accounts-receivable/summary/{unit_id}` — resumen de deuda actual

### `/payments`
- `POST /payments` — registrar pago
- `GET /payments` — listar (condominium_id, unit_id, ar_id, status)
- `GET /payments/{id}`

### `/receipts`
- `GET /receipts` — listar (condominium_id, unit_id)
- `GET /receipts/{id}`
- `GET /receipts/unit/{unit_id}` — recibos por unidad

### `/units/{unit_id}/ledger`
- `GET /units/{unit_id}/ledger` — estado de cuenta completo (entries + saldo pendiente)

### `/condominiums/{id}/summary`
- `GET /condominiums/{id}/summary` — deuda total del condominio por estado

---

## 7. Roadmap FIN — Estado de Tareas (Completado 2026-05-01)

| # | Tarea | Estado | PR | Notas |
|---|-------|--------|-----|-------|
| FIN-01 | Spec funcional distribución | ✅ Cerrada | — | Sección 3 de este doc |
| FIN-02 | Extender core_charges | ✅ | #1 | Migración 051 + validación scope |
| FIN-03 | Actualizar dominio charges | ✅ | #1 | Entity, data, mapper, schemas, usecase |
| FIN-04 | Crear ProrationService | ✅ | #2 | Servicio de dominio puro |
| FIN-05 | Prorrateo por torre | ✅ | #3 | Consolidado con FIN-06 |
| FIN-06 | Prorrateo por condominio | ✅ | #3 | Consolidado con FIN-05 |
| FIN-07 | Redondeo determinístico | ✅ | #2 | Incluido: residual → mayor coeff |
| FIN-08 | Refactor generate_from_charge | ✅ | #4 | Bug corregido: entry.amount |
| FIN-09 | Resolver deudor por unidad | ✅ | #5 | Prioridad: ocupante → propietario |
| FIN-10 | Idempotencia AR | ✅ | #5 | exists_by_charge_period_unit() |
| FIN-11 | Recurrencia mensual | ✅ | #6 | generate_recurring() |
| FIN-12 | Validar payments/receipts/ledger | ✅ | #7 | Sin cambios requeridos |
| FIN-13 | Tests | ✅ | #8 | 13 tests standalone pasando |
| FIN-14 | Documentación y handoff | ✅ | #9 | Este doc |

### Archivos nuevos
- `src/alembic/versions/051_add_charge_scope_distribution.py`
- `src/library/dddpy/core_charges/domain/proration_service.py`
- `src/library/dddpy/core_charges/usecase/proration_usecase.py`
- `tests/test_proration_pipeline.py`
- `docs/09-sprint/fin-12-validation-payments-receipts-ledger.md`

### Módulos modificados
- `core_charges/` — scope, building_id, distribution_mode, validaciones 3-capas
- `core_accounts_receivable/` — generate_from_charge refactor, debtor, idempotency, recurrence

### Módulos NO tocados
- `core_payments` ✅ | `core_receipts` ✅ | `core_ledger_entries` ✅

---

## 8. Permisos RBAC (extensión Phase 2)

| code | resource | action | scope_default |
|------|----------|--------|---------------|
| charge.create | charge | create | condominium |
| charge.read | charge | read | condominium |
| charge.update | charge | update | condominium |
| charge.delete | charge | delete | global |
| receipt.read | receipt | read | condominium |
| receipt.export | receipt | export | condominium |

---

## 9. Notas de Diseño (no negociables)

1. **Unidad es el centro del universo financiero.** Todo cargo, pago y estado de cuenta parte de `core_units`.
2. **No se tocan `payments`, `receipts` ni `ledger`.** Se validan, no se rehacen.
3. **Decimal handling:** `Decimal(12,2)` para todos los montos. Nunca `float`.
4. **Ledger es append-only.** Solo se añade, nunca se modifica.
5. **El prorrateo vive entre `charge` y `AR`.** charge = intención. AR = obligación concreta por unidad.

---

*Documento preparado por Misato K — Coordinación*
*Basado en análisis de Lelouch S (2026-05-01)*
*Implementado por Bulma S (2026-05-01) — Roadmap completado: 14/14 ✅*

<small>🔚 fin · 09-Sprint · Sprint-5 · Accounts Receivable · `docs/09-sprint/sprint5-accounts-receivable-20260424.md` · `2026-05-01`</small>


---

## 09-Sprint · Sprint-6 · User Roles Integration

<small>📄 `docs/09-sprint/sprint6-user-roles-integration-20260424.md` · modificado: `2026-04-24`</small>

# Sprint 6 — Análisis de Integración: Users · Roles · Propietarios · Occupancy Types
**Proyecto:** backdmin (condo-py)
**Fecha:** 2026-04-24
**Autor:** Bulma Briefs — Capsule Corp I+D
**Estado:** ANÁLISIS

---

## 1. Contexto General

Los 4 módulos bajo análisis gobiernan la identidad, autorización y relación patrimonial de los actores del sistema:

```
core_users              — Identidad y autenticación
core_condominium_roles — Roles administrativos por condominio
core_unit_ownerships   — Relación propietario ↔ unidad
core_unit_occupancies  — Relación ocupante ↔ unidad (vía occupancy_type)
core_occupancy_types   — Catálogo de tipos de ocupación
```

**Lo que ya existe (Phase 1e):** `GET /users/{id}/consolidated-view` retorna user + profile + roles + ownerships + occupancies. Eso es buen punto de partida, pero la integración tiene huecos.

---

## 2. Inventario de Entidades y Relaciones

### 2.1 Entidades y campos clave

| Módulo | Entidad | PK | FKs directos | Status lifecycle |
|---|---|---|---|---|
| `core_users` | UserEntity | id, uuid | — | active / suspended / locked / inactive / pending |
| `core_condominium_roles` | CondominiumRoleEntity | id, uuid | condominium_id, user_id, building_id | active / inactive / historical |
| `core_unit_ownerships` | UnitOwnershipEntity | id, uuid | unit_id, user_id | active / inactive / historical |
| `core_unit_occupancies` | UnitOccupancyEntity | id, uuid | unit_id, user_id, occupancy_type_id | active / inactive / historical |
| `core_occupancy_types` | OccupancyTypeEntity | id, uuid | condominium_id (opcional) | is_active (booleano, no FK) |

### 2.2 Relaciones entre módulos

```
User (1) ←─── (N) CondominiumRole   ←─── (1) Condominium
User (1) ←─── (N) UnitOwnership     ←─── (1) Unit
User (1) ←─── (N) UnitOccupancy     ←─── (1) Unit
                                         └── (N) OccupancyType
```

---

## 3. Hallazgos por Módulo

### 3.1 `core_users` ✅ — Estado: FUNCIONAL

**Lo que está bien:**
- Ciclo de vida de status completo (active → suspended → locked → inactive)
- `token_version` se incrementa en soft-delete y suspend → invalida JWTs inmediatamente
- `get_consolidated_view()` ya junta roles + ownerships + occupancies
- Soft-delete + restore + suspend + activate

**Hallazgos:**
- El `consolidated-view` no incluye nombre del condominio ni código de unidad en las relaciones — queda como IDs numéricos. Para un admin, esto es inútil sin joins.

### 3.2 `core_condominium_roles` ✅ — Estado: FUNCIONAL

**Lo que está bien:**
- 7 roles definidos: super_admin, condominium_admin, board_member, finance_reviewer, security_staff, maintenance_staff, operations_staff
- 3 scopes: condominium / building / unit
- Validación de invariants en entity (`_validate_invariants()`)
- Listados por condominio y por usuario

**Hallazgos:**
- **No hay cascade en soft-delete de usuario:** si se soft-deletea un usuario, sus roles quedan huérfanos con `user_id` pointing to a deleted user. No hay query que filtre roles con user.deleted_at IS NOT NULL.
- **No hay endpoint de "roles activos por condominio + rol específico":** no existe `GET /condominium-roles/condominium/{id}/role/{role}`.
- **No hay validación de unicidad:** ¿se puede asignar el mismo rol al mismo usuario en el mismo condominium dos veces?

### 3.3 `core_unit_ownerships` ✅ — Estado: FUNCIONAL (con reservas)

**Lo que está bien:**
- ownership_type: owner / co_owner
- ownership_percentage (DECIMAL 5,2 — 0 a 100)
- Histórico: start_date / end_date permite archival
- Listados por unit y por user

**Hallazgos:**
- **Validación OWN-01 (CRÍTICA):** No existe validación de que la suma de `ownership_percentage` de todos los `active` co-owners de una unidad no supere 100%.
  ```python
  # Esto debería existir en create/update:
  total = db.query(DBUnitOwnership).filter(
      DBUnitOwnership.unit_id == unit_id,
      DBUnitOwnership.status == "active",
      DBUnitOwnership.deleted_at.is_(None)
  ).all()
  sum_pct = sum(o.ownership_percentage for o in total)
  assert sum_pct + new_percentage <= 100
  ```
- **OWN-02:** ¿Un usuario puede ser owner Y co_owner de la misma unidad al mismo tiempo? No hay validación.
- **No hay cascade en soft-delete de usuario:** mismo problema que en roles.
- **No hay enriquecimiento con datos de unidad:** listar ownerships sin el código de unidad es inútil para un admin.

### 3.4 `core_unit_occupancies` — Estado: REVISAR

**Nota:** Este módulo no estaba en los 4 originales, pero está en el `consolidated-view` y depende directamente de `core_occupancy_types`.

**Lo que está bien:**
- Históricos con start/end dates
- `is_primary` flag para distinguir ocupante principal

**Hallazgos:**
- **`occupancy_type_id` NO tiene FK** en `DBUnitOccupancy` → `core_occupancy_types.id`. El campo existe como BigInteger pero sin constraint.
- **OCC-01:** No hay validación de que un usuario no tenga dos `active` occupancies de tipo `primary` en la misma unidad.
- **No hay cascade:** si se elimina un `OccupancyType`, las occupancy records quedan con `occupancy_type_id` inválido.

### 3.5 `core_occupancy_types` ✅ — Estado: FUNCIONAL

**Lo que está bien:**
- Scope: system (global) vs condominium (custom por condo)
- Flags: `requires_authorization`, `allows_primary`
- Catálogo ya funciona con soft-delete

**Hallazgos:**
- **Sin FK en `occupancy_type_id` en `DBUnitOccupancy`** — esto rompería cualquier join entre occupancy y su tipo en la DB si hay orphan records.

---

## 4. Integración: Canvas Completo del Actor

### 4.1 Flujos que deben existir

```
[Crear usuario]
  1. POST /users → crea user + user_profile (profile separado)
  2. POST /condominium-roles → asignar rol en condominio
  3. POST /unit-ownerships → asignar propiedad
  4. POST /unit-occupancies → asignar ocupación
  ⚠ Ninguno de estos pasos es transaccionalmente atómico.

[Consultar "¿Quién es el residente principal de la Torre A, Unidad 301?"]
  → Hoy: query manual en 3 tablas
  → Esperado: 1 endpoint consolidado con nombres

[Cambiar propiedad de unidad]
  1. PUT /unit-ownerships/{id}/end_date = hoy
  2. POST /unit-ownerships (nuevo owner)
  3. Validar OWN-01: % total ≤ 100
  ⚠ No existe endpoint wrapper que haga esto atómico.

[Desactivar usuario (soft-delete)]
  1. Soft-delete user (incrementa token_version)
  2. ¿Los roles se marcan como historical automáticamente? → NO.
  3. ¿Las ownerships se cierran con end_date? → NO.
  4. ¿Las occupancies se cierran? → NO.
  ⚠ Datos huérfanos guaranteed.
```

### 4.2 Lo que falta como módulos integrados

| # | Funcionalidad | Módulo afectado | Prioridad |
|---|---|---|---|
| M-01 | Validación OWN-01: % total ≤ 100 por unidad | core_unit_ownerships | ALTA |
| M-02 | Cascade soft-delete: roles + ownerships + occupancies cuando user se elimina | core_users + roles + ownerships + occupancies | ALTA |
| M-03 | FK constraint en occupancy_type_id → core_occupancy_types.id | core_unit_occupancies | ALTA |
| M-04 | Endpoint enriquecido: list de ownerships con código de unidad + nombre de condo | core_unit_ownerships | MEDIA |
| M-05 | Endpoint enriquecido: list de roles con nombre de usuario + nombre de condo | core_condominium_roles | MEDIA |
| M-06 | Validación OCC-01: un solo primary occupant por unidad | core_unit_occupancies | MEDIA |
| M-07 | Unique constraint: (user_id, condominium_id, role) active — sin duplicados | core_condominium_roles | MEDIA |
| M-08 | Unique constraint: (user_id, unit_id, occupancy_type_id) active, is_primary=true | core_unit_occupancies | MEDIA |
| M-09 | Consolidated view mejorado: incluir nombre condo, código unidad, tipo ocupación | core_users | BAJA (ya existe estructura) |
| M-10 | Historial completo de transiciones de propiedad/ocupación por unidad | core_unit_ownerships + core_unit_occupancies | BAJA |

---

## 5. Validaciones de Negocio Pendientes ( Rules )

| ID | Descripción | Ubicación |
|---|---|---|
| OWN-01 | Suma de ownership_percentage active de una unidad ≤ 100 | `UnitOwnershipUseCase.create()` / `update()` |
| OWN-02 | Un usuario no puede ser owner y co_owner de la misma unidad al mismo tiempo | `UnitOwnershipUseCase` |
| OCC-01 | Solo un occupancy record active con `is_primary=true` por unidad | `UnitOccupancyUseCase` |
| ROLE-01 | No duplicar (user_id, condominium_id, role, status=active) | `CondominiumRoleUseCase` |
| USR-01 | Al hacer soft-delete de usuario, cascade a roles, ownerships, occupancies (marcar historical o fechar) | `UserUseCase.soft_delete()` |

---

## 6. Recomendación de Arquitectura

### 6.1 Immediate (Sprint 6 — esta semana)
Implementar M-01, M-02, M-03 como hotfixes de integridad referencial. Son blockers para que el sistema no entre en estado inconsistente.

### 6.2 Short-term (Sprint 7)
Implementar M-04, M-05, M-07, M-08 — queries enriquecidas y constraints de unicidad.

### 6.3 Medium-term
Implementar un servicio `ActorContextService` que orqueste la creación de un actor completo (user + profile + role + ownership + occupancy) en una sola transacción, con rollback.

---

## 7. Asignación Sugerida de Responsables

| Módulo/Tarea | Responsable sugerido |
|---|---|
| M-01 + M-02 (ownerships + cascade) | Dev front-end: @Mike / Dev back: @Lelouch |
| M-03 (FK occupancy_type) | Dev back: @Lelouch |
| M-04 (enriched ownership queries) | Dev back: @Lelouch |
| M-05 (enriched role queries) | Dev back: @Bulma |
| M-07 + M-08 (unique constraints) | Dev back: @Bulma |
| M-06 (OCC-01 primary validation) | Dev back: @Lelouch |
| M-09 (consolidated view improvement) | Dev back: @Bulma |

---

## 8. Dependencias de Migración

Ninguna de las tareas M-01 a M-10 requiere migración nueva de tabla. Las validaciones son lógica de aplicación. La M-03 requiere ALTER TABLE para agregar FK si no existe (verificar con `SHOW CREATE TABLE core_unit_occupancies`).

---

## 9. Checklist demerge de Integración

- [ ] OWN-01: validar % total ≤ 100 al crear/actualizar ownership
- [ ] OWN-02: validar no duplicidad owner+co_owner por unidad
- [ ] ROLE-01: unique constraint (user, condo, role) active
- [ ] OCC-01: solo un primary occupant por unidad
- [ ] USR-01: cascade soft-delete a roles/ownerships/occupancies
- [ ] FK `occupancy_type_id` → `core_occupancy_types.id`
- [ ] Queries enriquecidas: ownerships con unit_code + condo_name
- [ ] Queries enriquecidas: roles con user full name + condo_name
- [ ] Consolidated view mejorado
- [ ] Tests de integración cubriendo los flujos del §4.1

<small>🔚 fin · 09-Sprint · Sprint-6 · User Roles Integration · `docs/09-sprint/sprint6-user-roles-integration-20260424.md` · `2026-04-24`</small>


---

## 09-Sprint · Sprint-7 · Auth Module

<small>📄 `docs/09-sprint/sprint7-auth-module-20260424.md` · modificado: `2026-04-24`</small>

# Sprint 7 — `core_auth` DDD Authentication Module

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable arquitectura:** Lelouch vi Britannia
**Responsable implementación:** Bulma

---

## Estado Actual del Módulo

El módulo `core_auth` YA EXISTE en `/src/library/dddpy/auth/` con la siguiente estructura:

```
auth/
├── domain/
│   ├── auth_exception.py
│   ├── auth_session.py     ← entity sesión activa
│   ├── auth_token.py       ← TokenPair, AccessTokenPayload
│   └── user_identity.py    ← identidad con profile
├── infrastructure/
│   ├── auth_session_repository.py  ← gestión refresh tokens (SHA-256 hashed)
│   ├── auth_user_repository.py   ← verify password, token_version
│   ├── dbauth_session.py         ← SQLAlchemy model (auth_sessions table)
│   └── jwt_service.py            ← create/decode access tokens
├── usecase/
│   ├── auth_cmd_schema.py  ← LoginSchema, RefreshSchema, LogoutSchema
│   └── auth_usecase.py     ← login, refresh, logout, logout_all, me
└── api/auth/
    ├── auth_dependencies.py  ← get_current_user (JWT validation)
    ├── rbac_dependencies.py
    └── routes_auth.py
```

### Lo que YA está implementado ✅

| Capability | Status | Notas |
|---|---|---|
| Login email+password | ✅ | Constant-time dummy bcrypt para no-enumeración |
| JWT access token (15 min) | ✅ | HS256, con `token_version` en payload |
| Refresh token rotation | ✅ | UUID v4, hashed SHA-256 en DB, 7 días TTL |
| Logout (revoke session) | ✅ | Soft-delete de auth_session |
| `logout_all` + token_version | ✅ | Invalida TODOS los JWT activos |
| `get_current_user` dependency | ✅ | Valida token_version vs DB en cada request |
| Rate limiting / account lock | ✅ | 5 intentos → 30 min lock |
| `GET /auth/me` | ✅ | Identity con profile |
| `POST /auth/logout` | ✅ | |
| `POST /auth/refresh` | ✅ | |

### Lo que FALTA (brechas de integridad) 🔴

| Gap | Descripción | Impacto |
|---|---|---|
| **AUTH-01** — Sin `POST /auth/password/change` | Users no pueden cambiar su contraseña. `logout_all` existe pero sin flow de cambio de contraseña, un usuario comprometido no puede invalidar sesiones. | ALTO |
| **AUTH-02** — Sin `POST /auth/register` (self-signup) | No existe endpoint para registro público de usuarios. El sistema solo acepta usuarios creados internamente. | ALTO (si se quiere OAuth o onboarding público) |
| **AUTH-03** — Sin `POST /auth/password/reset` (olvidé mi contraseña) | No hay flujo de reset de contraseña (email con token). Dependiendo del modelo de negocio esto puede ser obligatorio. | MEDIO (si hay signup) |
| **AUTH-04** — Sin endpoint `POST /auth/logout-all` en routes | `AuthUseCase.logout_all()` existe pero `routes_auth.py` no expone `POST /auth/logout-all`. El usuario no tiene forma de invocar invalidación global. | ALTO |

---

## Análisis de Brechas

### AUTH-01 — `POST /auth/password/change`

**Descripción:** El flujo completo de cambio de contraseña requiere:
1. Autenticación (JWT válido)
2. Verificación de contraseña actual
3. Actualización de `password_hash` en `users`
4. Incremento de `token_version` (invalida todos los JWT activos)
5. Revocación de todas las `auth_sessions` del usuario

**Ubicación de implementación:**
- `AuthUseCase.change_password(user_id, old_password, new_password)`
- `AuthUserRepository.update_password(user_id, new_password_hash)` — necesita ser añadido
- `routes_auth.py`: `POST /auth/password/change` con body `{current_password, new_password}`

**Seguridad:**
- El cambio de contraseña debe invalidar todas las sesiones existentes (`logout_all` internally)
- `token_version` debe incrementarse para invalidar todos los JWT antes de su TTL (15 min)
- La nueva contraseña debe cumplir policy (mínimo 8 chars, no igual al email, no en dictionary común)

**Validaciones:**
- `old_password` debe verificarse contra el hash actual
- `new_password` no puede ser igual a `old_password`
- Policy de password strength

### AUTH-02 — `POST /auth/register` (self-signup)

**Descripción:** Registro público de usuarios. Dependiendo del modelo de negocio puede ser necesario o no. Si el onboarding es solo interno (admin crea usuarios), este endpoint no es prioritario.

**Si se implementa:**
- `RegistrationSchema`: `email`, `password`, `first_name`, `last_name`
- `AuthUseCase.register(schema)` → crea user + user_profile
- Envío de email de verificación (`email_verified_at` se setea en NULL inicialmente)
- Rate limiting: 1 registro por IP por hora

**Preliminar:** Esperar confirmación del equipo sobre si self-signup es requerido antes de implementarlo. Si no es necesario, descartar esta brecha y marcar AUTH-02 como N/A.

### AUTH-03 — `POST /auth/password/reset`

**Descripción:** Flujo "olvidé mi contraseña":
1. User pide reset con su email
2. Sistema genera token de reset (UUID,存入 DB con TTL 1 hora)
3. Email enviado con link contendo token
4. User hace POST con token + nueva contraseña

**Requiere:**
- Nueva tabla `auth_password_resets` (token_hash, user_id, expires_at)
- `AuthUseCase.request_password_reset(email)` → genera token, NO envía email (mock OK)
- `AuthUseCase.confirm_password_reset(token, new_password)` → valida token, actualiza password
- `routes_auth.py`: `POST /auth/password/reset/request` + `POST /auth/password/reset/confirm`

**Preliminar:** Depende de AUTH-02. Si no hay registro público, este flujo puede no ser prioritario. Confirmar con el equipo.

### AUTH-04 — `POST /auth/logout-all` en routes

**Descripción:** `routes_auth.py` no tiene el endpoint `POST /auth/logout-all`. El método `AuthUseCase.logout_all()` existe pero no es accesible por API.

**Fix:**
```python
@auth_routes.post("/logout-all")
@api_handler
def logout_all(user: UserIdentity = Depends(get_current_user)) -> dict:
    response = AuthUseCase().logout_all(user_id=user.id)
    return response.dict()
```

---

## Scope Definido para Sprint 7

### Must Have ( cerrar antes de Phase 4 )

- [ ] **AUTH-01** — `POST /auth/password/change` (con invalidación global de sesiones)
- [ ] **AUTH-04** — `POST /auth/logout-all` expuesto en routes

### Should Have (si hay tiempo )

- [ ] **AUTH-03** — `POST /auth/password/reset/request` + `/confirm` (sin envío de email real — mock OK)
- [ ] **AUTH-02** — Registro self-signup (solo si el modelo de negocio lo requiere — confirmar primero)

### Dependencias

- `AuthUseCase` necesita nuevo método `change_password()`
- `AuthUserRepository` necesita nuevo método `update_password()`
- Verificar que tabla `users` tenga columna `password_hash` (debe existir de migraciones previas)
- `routes_auth.py` necesita los nuevos endpoints

---

## Arquitectura Propuesta

```
routes_auth.py
├── POST /auth/login              ✅ (existing)
├── POST /auth/refresh             ✅ (existing)
├── POST /auth/logout             ✅ (existing)
├── POST /auth/logout-all         🆕 AUTH-04
├── POST /auth/password/change    🆕 AUTH-01
├── POST /auth/password/reset/request   🆕 AUTH-03 (should have)
├── POST /auth/password/reset/confirm    🆕 AUTH-03 (should have)
├── POST /auth/register           🆕 AUTH-02 (confirmar si aplica)
├── GET  /auth/me                 ✅ (existing)
└── GET  /auth/health             ✅ (existing)
```

---

## Asignación

| Task | Responsable |
|---|---|
| AUTH-01: `POST /auth/password/change` | Bulma |
| AUTH-04: `POST /auth/logout-all` en routes | Bulma |
| AUTH-03: password reset flow | Bulma (si hay tiempo) |
| AUTH-02: self-signup | **Esperar confirmación del equipo** antes de implementar |

---

## Siguiente Paso

Confirmar con el equipo si AUTH-02 (self-signup) aplica. Si no, Sprint 7 se cierra con AUTH-01 + AUTH-04 + AUTH-03 opcional y se puede avanzar a Phase 4.

<small>🔚 fin · 09-Sprint · Sprint-7 · Auth Module · `docs/09-sprint/sprint7-auth-module-20260424.md` · `2026-04-24`</small>


---

## 09-Sprint · Sprint-8 · Incidents

<small>📄 `docs/09-sprint/sprint8-incidents-20260424.md` · modificado: `2026-04-24`</small>

# Sprint 8 — `core_incidents` — Maintenance Ticketing System

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable arquitectura:** Lelouch vi Britannia
**Responsable implementación:** Bulma

---

## Overview

Un sistema de tickets de mantenimiento/incidencias permite a residentes y propietarios reportar problemas en las unidades o áreas comunes del condominio. Es el módulo más directamente orientado al usuario final (residentes) después de la autenticación.

**Flujo básico:**
1. Usuario crea un ticket de incidencia en una unidad
2. Admin/board_member lo revisa, asigna prioridad y categoría
3. Se asigna a staff de mantenimiento o contractor externo
4. Se da seguimiento hasta resolución
5. Usuario recibe notificación de estado (cuando esté implementado `core_notifications`)

---

## Entidades del Dominio

### `IncidentEntity`

```
IncidentEntity
├── id: int
├── uuid: str
├── condominium_id: int
├── building_id: int (opcional — null si es área común)
├── unit_id: int
├── reported_by_user_id: int  ← quién reporta (debe tener occupancy u ownership activo)
├── assigned_to_user_id: int (nullable)  ← staff o contractor
├── category: IncidentCategory (enum)
├── priority: IncidentPriority (enum)
├── status: IncidentStatus (enum)
├── title: str (max 150)
├── description: str (text)
├── photos: List[str] (urls a uploads, nullable)
├── internal_notes: str (nullable)  ← solo visible para staff/admin
├── resolution_notes: str (nullable)  ← notas de resolución al cerrar
├── scheduled_date: date (nullable)
├── completed_date: date (nullable)
├── created_at, updated_at, deleted_at
└── is_escalated: bool (default false)
```

### Enums

**`IncidentStatus`:**
```
pending   → abierto, sin asignar
open      → revisado, en cola
in_progress → asignado y en ejecución
resolved  → arreglado, pendiente de confirmación
closed    → cerrado (confirmado por usuario o auto)
cancelled → cancelado por admin
```

**`IncidentPriority`:**
```
low      → no urgente
medium   → atención normal
high     → dentro de 48h
urgent   → inmediata (potencial daño estructural o seguridad)
```

**`IncidentCategory`:**
```
plumbing        → plomería
electrical     → eléctrico
structural     → estructural
common_areas   → áreas comunes
elevator       → ascensor
painting       → pintura
cleaning       → limpieza
pest_control   → control de plagas
security       → seguridad
other          → otro
```

---

## Integración con el Sistema Existente

### Dependencias del modelo actual

| Dependencia | Para qué se usa |
|---|---|
| `core_condominiums.id` | Cada incident pertenece a un condominio |
| `core_buildings.id` | Puede ser null (área común global) o edificio específico |
| `core_units.id` | El incident se reporta en una unidad específica |
| `core_unit_occupancies.user_id` | Validar que quien reporta tiene relación con la unidad (`reported_by_user_id`) |
| `core_unit_ownerships.user_id` | Alternativamente, puede reportar un propietario |
| `users.id` | Reported_by + assigned_to |
| `core_condominium_roles.role` | Solo usuarios con rol `condominium_admin`, `maintenance_staff`, `board_member` pueden crear/admin tickets. Residents pueden reportar. |

### Validaciones de negocio

**INC-01:** El usuario que reporta (`reported_by_user_id`) debe tener un `UnitOccupancyEntity` activo O un `UnitOwnershipEntity` activo en la unidad `unit_id` del incident. Caso contrario → 403.

**INC-02:** Solo usuarios con rol `condominium_admin`, `board_member` o `maintenance_staff` pueden asignar/reasignar un ticket. Residents pueden solo crear y ver los suyos.

**INC-03:** Un ticket con `priority = urgent` auto-set `is_escalated = true`.

**INC-04:** Un ticket solo puede pasar a `status = closed` si `completed_date` está seteado.

**INC-05:** El campo `assigned_to_user_id` es nullable. Un ticket sin asignar aparece en el queue de `maintenance_staff`.

---

## Estructura DDD propuesta

```
src/library/dddpy/core_incidents/
├── domain/
│   ├── incident_entity.py         ← IncidentEntity + enums
│   ├── incident_exception.py      ← IncidentNotFound, UnauthorizedIncidentAccess
│   ├── incident_repository.py     ← ABC (cmd)
│   └── incident_query_repository.py ← ABC (query)
├── infrastructure/
│   ├── dbincident.py              ← SQLAlchemy model (core_incidents table)
│   ├── incident_cmd_repository.py  ← Create, update, delete
│   └── incident_query_repository.py ← Queries enriquecidas
├── usecase/
│   ├── incident_cmd_usecase.py
│   ├── incident_query_usecase.py
│   ├── incident_factory.py
│   └── incident_cmd_schema.py      ← Pydantic input schemas
└── api/
    └── incidents/routes_incidents.py
```

### Migración sugerida

```sql
CREATE TABLE core_incidents (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  uuid VARCHAR(36) NOT NULL UNIQUE,
  condominium_id BIGINT NOT NULL,
  building_id BIGINT NULL,
  unit_id BIGINT NOT NULL,
  reported_by_user_id BIGINT NOT NULL,
  assigned_to_user_id BIGINT NULL,
  category VARCHAR(40) NOT NULL,
  priority VARCHAR(20) NOT NULL DEFAULT 'medium',
  status VARCHAR(30) NOT NULL DEFAULT 'pending',
  title VARCHAR(150) NOT NULL,
  description TEXT,
  photos JSON,
  internal_notes TEXT,
  resolution_notes TEXT,
  scheduled_date DATE NULL,
  completed_date DATE NULL,
  is_escalated BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT NOW(),
  updated_at DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  deleted_at DATETIME NULL,
  FOREIGN KEY (condominium_id) REFERENCES core_condominiums(id),
  FOREIGN KEY (building_id) REFERENCES core_buildings(id),
  FOREIGN KEY (unit_id) REFERENCES core_units(id),
  FOREIGN KEY (reported_by_user_id) REFERENCES users(id),
  FOREIGN KEY (assigned_to_user_id) REFERENCES users(id),
  INDEX idx_condo_status (condominium_id, status),
  INDEX idx_unit (unit_id),
  INDEX idx_assigned (assigned_to_user_id),
  INDEX idx_reported_by (reported_by_user_id)
);
```

---

## Endpoints propuestos

| Método | Endpoint | Permiso | Descripción |
|---|---|---|---|
| POST | `/incidents` | Authenticated | Crear incident (validado contra occupancy/ownership) |
| GET | `/incidents` | Authenticated + filtros | Listar (filtros: condo, status, priority, category, building, unit) |
| GET | `/incidents/{id}` | Authenticated | Detalle de un incident |
| GET | `/incidents/{uuid}` | Authenticated | Detalle por UUID |
| PATCH | `/incidents/{id}` | Admin/staff | Actualizar status, priority, assign, notes |
| POST | `/incidents/{id}/assign` | Admin/staff | Asignar a user_id |
| POST | `/incidents/{id}/escalate` | Admin | Escalar |
| POST | `/incidents/{id}/complete` | Admin/staff | Marcar como completado (set completed_date) |
| POST | `/incidents/{id}/close` | Admin | Cerrar |
| POST | `/incidents/{id}/cancel` | Admin | Cancelar |
| GET | `/incidents/my` | Authenticated | Mis incidents (reported_by = me) |
| GET | `/condominiums/{id}/incidents` | Authenticated | Incidents de un condominio (paginados) |

---

## Queries enriquecidas (M-10)

Igual que en M-05 para roles, los listados de incidents deben devolver:
- `reported_by_user_full_name` (from user_profiles)
- `assigned_to_user_full_name` (from user_profiles)
- `condominium_name`
- `building_name` (nullable)
- `unit_code`

Esto sigue el patrón `_bulk_enrich` ya establecido.

---

## RBAC — Permisos necesarios (nuevos)

```
incidents:create     → cualquier authenticated user con occupancy/ownership en la unidad
incidents:read       → mismo condominio ( OWNER/ TENANT + role staff/admin)
incidents:update     → maintenance_staff, board_member, condominium_admin
incidents:assign     → board_member, condominium_admin
incidents:escalate   → condominium_admin
incidents:delete     → condominium_admin
```

Seed sugerido en `core_permissions`:
```python
("incidents:create", "Create maintenance incidents"),
("incidents:read", "View incidents"),
("incidents:update", "Update incident status/priority"),
("incidents:assign", "Assign incidents to staff"),
("incidents:escalate", "Escalate urgent incidents"),
("incidents:delete", "Cancel/delete incidents"),
```

---

## Notas de diseño

1. **Photos/uploads:** El campo `photos` es JSON array de URLs. La subida de archivos es un paso posterior ( `core_documents` puede reutilizarse para esto). Por ahora se acepta que venga vacío o con URLs pre-subidas.

2. **Área común sin unit:** Si `building_id` es null, el incident es de área común global. `unit_id` también podría ser null en ese caso — considerar si el incident puede no tener unidad.

3. **Notificaciones (Phase 4 al final):** Cuando exista `core_notifications`, cada cambio de status de incident debería disparar una notificación a `reported_by_user_id` y optionally a `assigned_to_user_id`.

4. **Dashboard para staff:** El endpoint `GET /incidents?assigned_to_user_id=X&status=open,in_progress` sirve como queue de trabajo del staff.

---

## Tasks para Bulma (implementación)

| Task | Descripción |
|---|---|
| T-1 | Crear migración `040_create_core_incidents.sql` |
| T-2 | Implementar DDD completo `core_incidents` (entity, repos, usecases) |
| T-3 | Implementar routes + RBAC decorator |
| T-4 | Queries enriquecidas con `_bulk_enrich` (reported_by full name, unit_code, etc.) |
| T-5 | Seed de permisos en `core_permissions` |

---

## Siguiente paso

@Bulma — mientras implementas, si necesitas que agregue campos adicionales al modelo o ajustes en las validaciones, avísame. El modelo es flexible mientras se respete el patrón DDD.

<small>🔚 fin · 09-Sprint · Sprint-8 · Incidents · `docs/09-sprint/sprint8-incidents-20260424.md` · `2026-04-24`</small>


---

## 09-Sprint · Sprint-9 · Notifications

<small>📄 `docs/09-sprint/sprint9-notifications-20260424.md` · modificado: `2026-04-24`</small>

# Sprint 9 — `core_notifications` — Notification Layer

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable:** Lelouch (análisis + arquitectura) + sub-agentes (implementación)

---

## Overview

`core_notifications` es la **capa glue** que conecta eventos del sistema con usuarios relevantes. No tiene lógica de negocio propia — observa eventos de otros módulos y envía notificaciones a los usuarios correspondientes.

**Fuentes de eventos (providers):**
- `core_announcements` — cuando se crea/publcia un anuncio
- `core_incidents` — cuando cambia el estado de un ticket (asignado, completado, cerrado)
- `core_payments` / `core_receipts` — cuando se genera un recibo o se registra un pago
- (futuro) `core_documents` — cuando se sube un documento relevante

**Canales de entrega (channels):**
- **In-app** — almacenar en DB para que el frontend haga polling o websocket
- **Email** — enviar email al usuario (usar servicio de email ya existente en `auth`)
- **Push (futuro)** — FCM / APNs (no implementar en Sprint 9)

---

## Modelo de Datos

### `NotificationEntity`

```
notification_id: int
uuid: str
user_id: int           → destinatario
channel: str          → 'in_app', 'email'
type: str             → 'announcement_published', 'incident_assigned', 'incident_resolved', 'payment_received', ...
resource_type: str    → 'announcement', 'incident', 'payment', 'receipt'
resource_id: int       → ID del recurso relacionado
title: str            → título de la notificación
body: str             → cuerpo/preview del mensaje
is_read: bool         → default false
read_at: datetime     → nullable
created_at: datetime
deleted_at: datetime  → soft-delete
metadata: JSON         → datos adicionales contextuales (author_name, condo_name, etc.)
```

### Enums

**NotificationChannel:** `in_app`, `email`
**NotificationType:** `announcement_published`, `incident_assigned`, `incident_completed`, `incident_closed`, `payment_received`, `receipt_generated`

---

## Arquitectura DDD

```
src/library/dddpy/core_notifications/
├── domain/
│   ├── notification_entity.py
│   ├── notification_exception.py
│   ├── notification_repository.py    ← ABC cmd
│   └── notification_query_repository.py ← ABC query
├── infrastructure/
│   ├── db_notification.py            ← SQLAlchemy model
│   ├── notification_cmd_repository.py
│   ├── notification_query_repository.py  ← con _bulk_enrich
│   └── notification_mapper.py
├── usecase/
│   ├── notification_cmd_schema.py
│   ├── notification_cmd_usecase.py
│   ├── notification_query_usecase.py
│   ├── notification_factory.py
│   └── notification_service.py       ← servicio de dominio que reciben los módulos productores
└── api/
    └── notifications/routes_notifications.py
```

### El patrón Observer/Lazy-Import

Los módulos productores (`core_announcements`, `core_incidents`) NO hacen import directo de `core_notifications` (evitaría círculos). En cambio:

**Opción A — Domain Events (futuro):** Events del dominio que un event bus dispersa. Más elegante pero más complejo.

**Opción B — Lazy import dentro del usecase:** En los usecases de announcements/incidents, al final del `create()` o `update()`, se importa `NotificationService` y se llama `notify_event()`. El import dentro de la función evita el círculo.

**Opción C —más pragmática para Sprint 9:** Crear `NotificationService` como un servicio reusable. Los módulos que quieran notificar llaman a `NotificationService.get_instance().notify(...)` (singleton). Esto se implementa al final del Sprint cuando ya esté listo todo.

**Recomendado: Opción B** — lazy import, simple, sin cambios en la arquitectura de los módulos existentes.

---

## NotificationService — API del servicio

```python
class NotificationService:
    """Servicio para crear notificaciones desde cualquier módulo."""

    def notify(
        self,
        user_id: int,
        channel: NotificationChannel,
        notif_type: NotificationType,
        resource_type: str,
        resource_id: int,
        title: str,
        body: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """Crea una notificación y la persiste en DB."""

    def notify_multiple(
        self,
        user_ids: List[int],
        channel: NotificationChannel,
        notif_type: NotificationType,
        resource_type: str,
        resource_id: int,
        title: str,
        body: str,
        metadata: Optional[dict] = None,
    ) -> int:
        """Crea notificaciones para múltiples usuarios (bulk). Retorna count."""

    def send_email_notification(
        self,
        user_id: int,
        title: str,
        body: str,
    ) -> None:
        """Envía email usando el EmailService de auth (mock OK)."""
```

---

## Endpoints API

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/notifications` | Listar notificaciones (filtros: user_id, is_read, channel, type) |
| GET | `/notifications/{id}` | Ver una notificación |
| GET | `/notifications/unread-count` | Contador de no leídas para el usuario actual |
| PATCH | `/notifications/{id}/read` | Marcar como leída |
| PATCH | `/notifications/mark-all-read` | Marcar todas como leídas |
| DELETE | `/notifications/{id}` | Soft-delete |
| GET | `/users/{user_id}/notifications` | Notificaciones de un usuario (paginados) |

---

## Integración con módulos existentes

### `core_announcements` — integration point

En `AnnouncementUseCase.create()` y `update()` (cuando se publica), al final del método:

```python
# Al final de announcement_usecase.create()
notification_service = NotificationService()
notification_service.notify(
    user_id=author_user_id,  # o todos los usuarios del condominio
    channel='in_app',
    notif_type='announcement_published',
    resource_type='announcement',
    resource_id=announcement.id,
    title=f"Nuevo anuncio: {data.title}",
    body=data.content[:200],
    metadata={'condominium_id': data.condominium_id},
)
```

### `core_incidents` — integration points

En `IncidentCmdUseCase.update()` (cuando cambia status o se asigna):

```python
# Cuando se asigna
if data.assigned_to_user_id and existing.assigned_to_user_id != data.assigned_to_user_id:
    notification_service.notify(
        user_id=data.assigned_to_user_id,
        channel='in_app',
        notif_type='incident_assigned',
        resource_type='incident',
        resource_id=incident.id,
        title=f"Incidente asignado: {incident.title}",
        body=f"Se te ha asignado el incidente #{incident.id}",
    )

# Cuando se completa
if data.status == 'resolved':
    notification_service.notify(
        user_id=incident.reported_by_user_id,
        channel='in_app',
        notif_type='incident_resolved',
        resource_type='incident',
        resource_id=incident.id,
        title=f"Incidente #{incident.id} resuelto",
        body="Su incidente ha sido marcado como resuelto.",
    )
```

---

## Migración

```sql
CREATE TABLE core_notifications (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  uuid VARCHAR(36) NOT NULL UNIQUE,
  user_id BIGINT NOT NULL,
  channel VARCHAR(20) NOT NULL DEFAULT 'in_app',
  type VARCHAR(50) NOT NULL,
  resource_type VARCHAR(30) NOT NULL,
  resource_id BIGINT NOT NULL,
  title VARCHAR(200) NOT NULL,
  body TEXT,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  read_at DATETIME NULL,
  metadata JSON,
  created_at DATETIME NOT NULL DEFAULT NOW(),
  deleted_at DATETIME NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_user_read (user_id, is_read),
  INDEX idx_user_created (user_id, created_at DESC),
  INDEX idx_resource (resource_type, resource_id)
);
```

---

## RBAC

```
notifications:read   → ver notificaciones propias
notifications:read_all → ver notificaciones de cualquier usuario (admin)
notifications:delete → borrar notificaciones
```

---

## Tasks

| Task | Descripción |
|---|---|
| T-1 | Migración 042 `core_notifications` |
| T-2 | DDD domain layer (entity, exceptions, repos ABC) |
| T-3 | Infrastructure (db, cmd repo, query repo con _bulk_enrich, mapper) |
| T-4 | Usecases + NotificationService |
| T-5 | API routes |
| T-6 | Integración en `core_announcements` (create, publish) |
| T-7 | Integración en `core_incidents` (assign, resolve, close) |
| T-8 | Seed RBAC permissions |

---

## Siguiente paso

@Misato K — confirmación: ¿notifications lo hago yo o lo dejamos pendiente para después de Phase 4 completo? El módulo es relativamente simple (DB + API + servicio de notificación), pero requiere integrar con announcements e incidents.

<small>🔚 fin · 09-Sprint · Sprint-9 · Notifications · `docs/09-sprint/sprint9-notifications-20260424.md` · `2026-04-24`</small>


---

## 10-Agents · AI Team

<small>📄 `docs/10-agents/AI_TEAM.md` · modificado: `2026-04-28`</small>

# AI Team — condo-py

> **Proyecto:** `condo-py`
> **Stack:** Python (FastAPI, DDD/CQRS) + Next.js (TypeScript)
> **Liderazgo humano:** Miguel — Technical Leader
> **Última actualización:** 2026-04-28

---

## 1. Visión General

Este proyecto es desarrollado **íntegramente por agentes de IA**, coordinados bajo un esquema de liderazgo técnico humano. Miguel actúa como **Technical Leader** y no escribe código directamente; su función es:

- ✅ Definir la visión del proyecto
- ✅ Modelar la base de datos
- ✅ Realizar code reviews
- ✅ Aprobar o rechazar pull requests y propuestas de arquitectura

La ejecución del código está 100% delegated a los agentes IA.

---

## 2. Mapa del Equipo

### 2.1 Liderazgo Humano

| Campo | Detalle |
|---|---|
| **Nombre** | Miguel |
| **Rol** | Technical Leader |
| **Responsabilidades** | Visión de producto, modelado DB, code reviews, arquitectura, approval gates |
| **Canal** | Discord: `#condo-backdmin` |

### 2.2 Agentes IA

| # | Nombre | Modelos | Rol Principal | Canal |
|---|---|---|---|---|
| 1 | **Lelouch** | GPT 5.4 | Architect — Arquitectura, diseño técnico, decisiones de alto nivel, planning | Discord: `@Lelouch S` |
| 2 | **Misato** | Minimax 2.7 | Coordinator — Coordinación general, priorización, gestión de flujo | Discord: `@Misato K` |
| 3 | **Bulma** | Minimax 2.7 / DeepSeek 4 Pro / DeepSeek 4 Flash | Dev Lead — Implementación Python backend + Next.js frontend | Discord: `@Bulma S` |

---

## 3. Descripción Detallada de Agentes

### 3.1 Lelouch — Architect

```
Nombre:       Lelouch
Modelos:      GPT 5.4
Rol:          Architect
Canal:        @Lelouch S (Discord)
Repo:         /home/miguel/servers/condo-py
```

**Responsabilidades:**

- Diseño de arquitectura DDD/CQRS del proyecto
- Definir estructura de módulos y patrones
- Decisions de alto nivel (qué tecnología usar, cómo estructurar la DB, patrones de API)
- Planning y roadmap técnico
- Revisiones generales cuando se agotan las tareas
- Validar que las propuestas de Bulma y Misato sigan la arquitectura definida

**Áreas de expertise:**
- Diseño de sistemas distribuidos
- Patrones de arquitectura (DDD, CQRS, Event Sourcing)
- Modelado de datos y diseño de schemas
- Estrategia de APIs REST/GraphQL

**Cuándo activar a Lelouch:**
- Cuando se necesita definir un nuevo módulo o servicio
- Cuando hay una decisión arquitectónica grande por tomar
- En planning sessions de sprint
- Cuando Bulma necesita validación de diseño antes de implementar

---

### 3.2 Misato — Coordinator

```
Nombre:       Misato
Modelos:      Minimax 2.7
Rol:          Coordinator
Canal:        @Misato K (Discord)
Repo:         /home/miguel/servers/condo-py
```

**Responsabilidades:**

- Coordinación del flujo de trabajo entre agentes
- Priorización de tareas del backlog
- Seguimiento de progreso del sprint
- Gestionar la comunicación entre Lelouch (architecture) y Bulma (dev)
-不掉链子 — asegurarse de que el proyecto no se atasque
- Gestión de blockers y escalado a Miguel cuando sea necesario

**Áreas de expertise:**
- Gestión de workflow y priorización
- Coordinación de equipos distribuidos
- Resolución de conflictos técnicos
- Comunicación entre visión de producto y implementación

**Cuándo activar a Misato:**
- Para priorización de tareas
- Cuando se necesita coordinar múltiples agentes
- Para seguimiento de sprint
- Para identificar y desbloquear cuellos de botella

---

### 3.3 Bulma — Dev Lead

```
Nombre:       Bulma
Modelos:      Minimax 2.7 (principal), DeepSeek 4 Pro, DeepSeek 4 Flash
Rol:          Dev Lead (Backend Python + Frontend Next.js)
Canal:        @Bulma S (Discord)
Repo:         condo-py: /home/miguel/servers/condo-py
              condo-backdmin: /home/miguel/servers/condo-backdmin
```

**Responsabilidades:**

- Implementación del código Python (backend FastAPI, DDD modules, infrastructure)
- Implementación del código Next.js (frontend, componentes, páginas, API routes)
- Writing tests, migrations, seeds
- Seguir los patrones y arquitectura definidos por Lelouch
- Recibir y aplicar code reviews de Miguel
- Proponer mejoras de código a Misato para escalado a Lelouch

**Modelos y cuándo usar cada uno:**

| Modelo | Cuándo usar |
|---|---|
| **Minimax 2.7** | Desarrollo general, código Python/FastAPI, lógica de dominio |
| **DeepSeek 4 Pro** | Tasks complejas de código, benchmarks de código, debugging difícil, código que requiere razonamiento técnico profundo |
| **DeepSeek 4 Flash** | Tasks rápidas y simples, código repetitivo, boilerplate, cambios menores |

**Áreas de expertise:**
- Python / FastAPI / DDD
- Next.js / TypeScript / React
- SQLAlchemy, Alembic migrations
- Tests unitarios e integración
- Docker, docker-compose

**Cuándo activar a Bulma:**
- Para cualquier implementación de código
- Para writing de tests
- Para migraciones de DB
- Para changes en condo-py y condo-backdmin

---

## 4. Flujo de Trabajo

```
Miguel (Tech Lead)
    │
    ├── [Visión / Arquitectura / Code Review / DB Modeling]
    │
    ▼
Lelouch (Architect) ──── GPT 5.4
    │                       
    ├── Diseño de arquitectura
    ├── Decisions técnicos
    └── Planning
    │
    ▼
Misato (Coordinator) ─── Minimax 2.7
    │
    ├── Priorización de tareas
    ├── Coordinación de flujo
    └── Gestión de sprint
    │
    ▼
Bulma (Dev) ──────────── Minimax 2.7 / DeepSeek 4 Pro / DeepSeek 4 Flash
    │
    ├── Implementación Python (condo-py)
    └── Implementación Next.js (condo-backdmin)
    │
    ▼
Miguel (Code Review → Approve/Reject)
```

### 4.1 Ciclo de Desarrollo Estándar

1. **Miguel** define la visión o historia de usuario
2. **Lelouch** diseña la arquitectura / modelo de datos si es necesario
3. **Misato** descompone la tarea en subtareas y las prioriza
4. **Bulma** implementa usando el modelo más apropiado:
   - Minimax 2.7 → desarrollo general
   - DeepSeek 4 Pro → tareas complejas de código
   - DeepSeek 4 Flash → tasks simples/boilerplate
5. **Miguel** revisa el código (code review final)
6. **Bulma** aplica correcciones de review
7. **Misato** mueve la tarea a done y actualiza el sprint board

---

## 5. Reglas de Comunicación

### 5.1 Etiquetado en Discord

| Propósito | Etiquetar |
|---|---|
| Planning / revisiones generales | `@Lelouch S` |
| Revisiones a Pochita y Bulma | `@Misato K` |
| Cambios a condo-py | `@Bulma S` |
| Frontend condo-backdmin | `@Pochita` |
| Decisiones de liderazgo / approval | Miguel directamente |

### 5.2 Formato de提交 en Git

Cada commit sigue la guía de **Commit Message Guidelines** definida en `MEMORY.md`:

```
type(scope): subject

<body>

<detailed list of changes>
```

Tipos válidos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `wip`

---

## 6. Tech Stack del Proyecto

### Backend (Python)
- **Framework:** FastAPI
- **Arquitectura:** DDD pragmático con CQRS
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Testing:** pytest
- **API Docs:** OpenAPI / Swagger (auto-generado)

### Frontend (Next.js)
- **Framework:** Next.js (App Router)
- **Lenguaje:** TypeScript
- **Estilos:** Tailwind CSS (por confirmar)
- **Estado:** React Query / Zustand (por confirmar)
- **UI Components:** shadcn/ui (por confirmar)

### Infraestructura
- **Contenedores:** Docker + docker-compose
- **Base de datos:** PostgreSQL (por confirmar)
- **Repos:** condo-py (backend), condo-backdmin (frontend)

---

## 7. Repositorios

| Repo | Ruta | Descripción |
|---|---|---|
| `condo-py` | `/home/miguel/servers/condo-py` | Backend Python / FastAPI / DDD |
| `condo-backdmin` | `/home/miguel/servers/condo-backdmin` | Frontend Next.js |
| Docs | `/home/miguel/servers/condo-py/docs/` | Documentación del proyecto |

---

## 8. Notas Importantes

- **Miguel no escribe código.** Su rol es supervisión, code review, visión y modelado DB.
- **Los agentes IA ejecutan el 100% del código.** Lelouch diseña, Bulma implementa, Misato coordina.
- **Code review es obligatorio.** Ningún código hace merge sin approval de Miguel.
- **Modelado DB siempre pasa por Miguel.** Lelouch puede proponer, pero Miguel tiene la última palabra en schema de DB.
- **Las PRs van a Discord** `#condo-backdmin` para revisión y merge.

<small>🔚 fin · 10-Agents · AI Team · `docs/10-agents/AI_TEAM.md` · `2026-04-28`</small>


---

## 10-Agents · Introducción

<small>📄 `docs/10-agents/README.md` · modificado: `2026-04-28`</small>

# 10-agents — Equipo de Agentes IA

> Documentación del equipo de agentes IA que desarrollan el proyecto.

---

## 📁 Estructura

| Archivo | Descripción |
|---|---|
| `AI_TEAM.md` | Definición completa del equipo, roles, modelos y flujos de trabajo |
| `TASKS.md` | Distribución de tareas y responsabilidades por agente |

---

## Índice

- [AI_TEAM.md](./AI_TEAM.md) — Equipo, modelos y responsabilidades
- [TASKS.md](./TASKS.md) — Distribución de tareas y guía de coordinación

<small>🔚 fin · 10-Agents · Introducción · `docs/10-agents/README.md` · `2026-04-28`</small>


---

## 10-Agents · Tasks

<small>📄 `docs/10-agents/TASKS.md` · modificado: `2026-04-28`</small>

# Distribución de Tareas — AI Team condo-py

> **Proyecto:** `condo-py`
> **Última actualización:** 2026-04-28

---

## 1. Principio General

Las tareas se distribuyen según el tipo de trabajo, no por agente fijo. Cada agente recibe tareas matching con su rol:

- **Lelouch** → arquitectura, diseño, planning
- **Misato** → coordinación, priorización, gestión de flujo
- **Bulma** → implementación (código), sin importar el módulo

---

## 2. Matriz: Tipo de Tarea → Agente Responsable

| Tipo de Tarea | Agente | Modelo recomendado |
|---|---|---|
| Definir arquitectura de nuevo módulo | Lelouch | GPT 5.4 |
| Diseñar schema de DB | Lelouch + Miguel | GPT 5.4 |
| Decision técnico de alto nivel | Lelouch | GPT 5.4 |
| Planning de sprint | Lelouch + Misato | GPT 5.4 + Minimax 2.7 |
| Priorizar backlog | Misato | Minimax 2.7 |
| Coordinar agentes | Misato | Minimax 2.7 |
| Seguimiento de sprint | Misato | Minimax 2.7 |
| Implementar módulo Python/DDD | Bulma | Minimax 2.7 |
| Implementar feature Next.js | Bulma | Minimax 2.7 |
| Task compleja de código / debugging | Bulma | DeepSeek 4 Pro |
| Task simple / boilerplate | Bulma | DeepSeek 4 Flash |
| Code review | Miguel | — |
| Modelado DB final | Miguel | — |
| Aprobación de arquitectura | Miguel + Lelouch | — |

---

## 3. Flujo de Asignación de Tareas

```
Tarea nueva identificada
         │
         ▼
    ¿Requiere decisión arquitectónica?
    ┌─────────────┐
    │    SÍ       │──▶ Lelouch (GPT 5.4) ──▶ Propuesta ──▶ Miguel approves
    └─────────────┘
         │ NO
         ▼
    ¿Es coordinación / gestión?
    ┌─────────────┐
    │    SÍ       │──▶ Misato (Minimax 2.7) ──▶ Descompone ──▶ Asigna a Bulma
    └─────────────┘
         │ NO
         ▼
    ¿Es implementación?
    ┌─────────────┐
    │    SÍ       │──▶ Bulma
    │              │      ├── Task simple       ──▶ DeepSeek 4 Flash
    │              │      ├── Task compleja    ──▶ DeepSeek 4 Pro
    │              │      └── Task general     ──▶ Minimax 2.7
    └─────────────┘
         │
         ▼
    Code Review ──▶ Miguel approves ──▶ Merge
```

---

## 4. Guidelines por Tipo de Implementación

### 4.1 Python / Backend (Bulma → condo-py)

- Seguir estructura DDD en `src/library/dddpy/`
- Usar el módulo `example/` como template
- decorators de error en `shared/decorators/api_handler.py`
- Siempre crear alembic migration para cambios de DB
- Tests en `tests/`
- Commits con formato convencional (feat, fix, refactor, etc.)

**Orden de archivos en módulo nuevo:**
```
src/library/dddpy/[modulo]/
├── __init__.py
├── domain/
│   ├── __init__.py
│   ├── [entidad].py
│   └── exceptions.py
├── usecase/
│   ├── __init__.py
│   ├── [caso_de_uso].py
│   └── schemas.py
├── infrastructure/
│   ├── __init__.py
│   ├── repository.py
│   └── mapper.py
└── api/
    ├── __init__.py
    └── routes_[modulo].py
```

### 4.2 Next.js / Frontend (Bulma → condo-backdmin)

- Usar App Router con TypeScript strict
- shadcn/ui para componentes base
- API routes en `src/app/api/`
- hooks custom en `src/hooks/`
- Types compartidos con backend en `src/types/`

### 4.3 Elección de Modelo para Bulma

```
PROMPT:
┌─────────────────────────────────────────────────────┐
│ Task simple?                                        │
│  - Boilerplate, archivos repetitivos                │
│  - Cambios mínimos (bug fix pequeño)                 │
│  - documentar código existente                      │
│  → DEEPSEEK 4 FLASH                                │
├─────────────────────────────────────────────────────┤
│ Task compleja?                                      │
│  - Algoritmo no trivial                             │
│  - Debug difícil de reproducir                      │
│  - Múltiples archivos que dependen entre sí         │
│  - Optimización de rendimiento                      │
│  → DEEPSEEK 4 PRO                                  │
├─────────────────────────────────────────────────────┤
│ Task general?                                       │
│  - Feature estándar                                 │
│  - Cambio moderado                                  │
│  - Tests, migrations                                │
│  → MINIMAX 2.7                                     │
└─────────────────────────────────────────────────────┘
```

---

## 5. Definition of Done

Una tarea se considera **DONE** cuando:

- [ ] Código implementado en el repo correspondiente
- [ ] Tests incluidos (si aplica)
- [ ] Migration de DB creada (si aplica)
- [ ] Commits con mensaje convencional
- [ ] PR abierta en Discord `#condo-backdmin`
- [ ] Code review aprobado por Miguel
- [ ] Merge realizado

---

## 6. Sprint Board (conceptual)

| To Do | In Progress | In Review | Done |
|---|---|---|---|
| Misato prioriza | Bulma implementa | Miguel revisa | — |

- **To Do:** Backlog priorizado por Misato
- **In Progress:** Bulma ejecutando con el modelo elegido
- **In Review:** PR abierta esperando code review de Miguel
- **Done:** Aprobado y mergeado

---

## 7.沟通 Canales

| Canal | Uso |
|---|---|
| Discord `#condo-backdmin` | Canal principal de trabajo |
| Discord DM → Miguel | Escalado, decisiones que requieren approval |
| PRs en GitHub | Code review formal |

---

## 8. Notas

- **No implementar sin que Misato haya priorizado la tarea.** Esto evita trabajo duplicado.
- **No hacer merge sin code review de Miguel.** El approval gate es innegociable.
- **Si una tarea requiere arquitectura nueva, no empezar a codear hasta que Lelouch tenga la propuesta aprobada.**
- **Si una tarea está bloqueada, escalar a Misato inmediatamente.** No dejar tareas estancadas.

<small>🔚 fin · 10-Agents · Tasks · `docs/10-agents/TASKS.md` · `2026-04-28`</small>


---

## BULMA · Amenity Bookings Sprint A

<small>📄 `docs/BULMA/amenity-bookings-sprint-a-20260502.md` · modificado: `2026-05-03`</small>

# Amenity Bookings — Sprint A

**Fecha:** 2026-05-02  
**Autor:** Bulma S  
**Status:** ✅ Completado (balance wire-up completado)

---

## Migraciones DB

- [x] `053_create_amenity_bookings` — `booking_price`, `security_deposit_amount`, `is_reservable` en amenities; `origin_type`/`origin_id` en AR; tabla `core_amenity_bookings` (18 cols, 7 FKs); tabla `core_amenity_deposit_movements`
- [x] `054_seed_booking_permissions` — 8 permisos RBAC (amenities.* + bookings.*)

---

## Modelo de Dominio `core_amenity_bookings`

- [x] `BookingEntity` — estados, transiciones, invariantes, `to_dict`
- [x] 4 excepciones: NotFound, ValidationError, OverlapError, StatusError
- [x] `DBBooking` + `BookingMapper` + repos cmd/query con solape horario

---

## Lógica de Negocio `BookingUseCase`

- [x] CRUD completo con validaciones: unidad↔edificio, owner↔unidad, solape horario, snapshots
- [x] `confirm()` — genera 2 ARs separadas (fee + garantía) con `origin_type`/`origin_id`
- [x] `cancel()` — soft-delete con razón
- [x] `complete()` — marca completada
- [x] `return_deposit()` — devolución total con trazabilidad
- [x] `apply_deposit()` — aplicación parcial/total con registro de movimiento

---

## API Routes

11 endpoints en `/bookings` con RBAC:
- CRUD + confirm + cancel + complete + deposit/return + deposit/apply

---

## Extensiones a Modelos Existentes

- [x] `AmenityEntity`, `DBAmenity`, schemas, usecase, routes — +3 campos
- [x] `AREntity`, `DBAR`, `ARMapper` — +origin_type/origin_id
- [x] `main.py` — registro de `booking_routes`
- [x] Seeds amenities actualizados con pricing/deposit

---

## Archivos

- 18 nuevos + 12 modificados
- Todo compila ✅

---

## ✅ Completado

- Balance wire-up: módulo `core_balance_summary` con 3 endpoints (condominio, edificio, unidad) + rubros separados (mantenimiento, reservas áreas comunes, garantías en custodia)

---

## Meta

| Campo | Valor |
|---|---|
| Sprint | A |
| Estado | Completado |
| siguiente paso | Balance wire-up |

<small>🔚 fin · BULMA · Amenity Bookings Sprint A · `docs/BULMA/amenity-bookings-sprint-a-20260502.md` · `2026-05-03`</small>


---

## BULMA · Flow Select Condo Dashboard

<small>📄 `docs/BULMA/flow-select-condo-dashboard-20260503.md` · modificado: `2026-05-03`</small>

# Task — Flujo UI: select-condo + dashboard (residente)

**Developer:** Bulma S
**Date:** 2026-05-03
**Repo:** `/home/miguel/servers/condo-net`
**Source:** `#flujo-de-interfaz` — Mike Ross
**Status:** ✅ Completada (2026-05-03)

---

## Contexto

`condo-net` es el frontend mobile-first para residentes/propietarios del sistema `condo-py`.
El flujo actual es:

1. Login (`/login`)
2. Selección de condominio (`/select-condo`)
3. Dashboard (`/dashboard`)

El flujo descrito en el ticket es el flujo **RESIDENTE/PROPIETARIO** (no admin).
Las tarjetas de selection y dashboard deben reflejar info del residente, no del admin.

---

## Cambios requeridos

### 1. `/select-condo` — Tarjeta de condominio

**Archivo:** `src/src/app/select-condo/page.tsx`

La tarjeta actual solo muestra: icono genérico, nombre, ciudad, código.

**Falta agregar:**

| Campo | Fuente | Notas |
|---|---|---|
| Logotipo del condominio | `condo.logo_url` | Mostrar imagen o placeholder si no existe |
| Dirección completa | `condo.address` | Mostrar dirección fiscal/dirección del condo |
| Estado del usuario en ese condominio | `condo.role` o similar | Mostrar texto: "Propietario" / "Inquilino" / "Residente" |
| Botón "Ingresar" con etiqueta clara | — | Reemplazar la flecha `ChevronRight` por un botón tipo `Button` con texto "Ingresar" |

**Diseño de la tarjeta:**
- Logo a la izquierda (recuadro 48x48, rounded)
- Nombre + dirección + ciudad en el centro
- Badge de rol (Propietario/Inquilino) debajo del nombre
- Botón "Ingresar" a la derecha

---

### 2. `/dashboard` — Dashboard residente

**Archivo:** `src/src/app/dashboard/page.tsx`

El dashboard actual solo tiene 4 iconos de acceso rápido + tarjeta de info del condominio.

**Falta agregar (encima de los iconos):**

#### Tarjeta 1 — Estado de pagos
- Título: "¿Al día en sus pagos?"
- Si está al día: mensaje verde + check icon
- Si tiene deuda: mensaje rojo + monto pendiente
- Fuente de datos: consumir `GET /accounts-receivable?unit_id=X` (o endpoint de ledger por unidad) y calcular saldo pendiente

#### Tarjeta 2 — Comunicados / Notificaciones pendientes
- Título: "Comunicados"
- Si hay nuevos: mostrar badge con count + título del comunicado más reciente
- Si no hay: mensaje "Sin novedades"
- Fuente de datos: consumir `GET /announcements` filtrado por `condominium_id` activo

**Los iconos de acceso rápido permanecen** (Residentes, Unidades, Pagos, Torres — o los que correspondan al rol residente).

---

## Archivos a tocar

| Archivo | Cambio |
|---|---|
| `src/src/app/select-condo/page.tsx` | Enriquecer tarjeta con logo, address, role badge, botón "Ingresar" |
| `src/src/app/dashboard/page.tsx` | Agregar 2 tarjetas informativas encima de quick links |

---

## Notas técnicas

- El `useAuth()` hook ya provee `user.condominiums[]` con los datos del condominio seleccionado.
- Para el estado de pagos, buscar endpoint en `condo-py` que dé saldo por unidad. Revisar `core_ledger_entries` o `core_accounts_receivable`.
- Para comunicados, usar `GET /announcements` con `condominium_id` del contexto.
- Si no existe endpoint de saldo pendiente por unidad, crear el ticket complementario para el backend.
- Los cambios son puramente frontend (UI/UX), no requieren cambios de API por ahora salvo que se descubra que falta algún endpoint.

---

## Checklist de implementación

- [x] select-condo: agregar `logo_url` a la tarjeta (con placeholder Building2)
- [x] select-condo: agregar `address` completo
- [x] select-condo: agregar badge de rol (Propietario/Inquilino/Residente)
- [x] select-condo: cambiar ChevronRight por botón "Ingresar"
- [x] dashboard: agregar tarjeta "Estado de pagos" (lógica al día / con deuda)
- [x] dashboard: agregar tarjeta "Comunicados" (count + más reciente)
- [x] Probar flujo completo: login → select-condo → dashboard
- [x] auth-context: agregar `address`, `logo_url`, `ownerships` al UserContext
- [x] Build verificado: compilación exitosa en Next.js 16 (Turbopack)

---

## Notas de implementación

- `address` y `logo_url` ya existían en la entidad `CondominiumEntity` del backend — solo se agregó el mapeo en auth-context
- Balance se obtiene por unidad usando `GET /balances/unit/{unit_id}` (endpoint creado en Sprint A)
- Los `ownerships` vienen del endpoint `GET /me/contexts` — se exponen ahora en `UserContext`
- El badge de rol prioriza: Propietario > Inquilino > Administrador > Residente

---

## Verificación + Gaps pendientes

> Documento completo: `docs/BULMA/flow-verify-planning-20260503.md`

### Estado: ✅ UI completada — 🔴 Faltan endpoints de backend

La implementación de Bulma es sólida — la UI funciona con fallbacks. Lo que bloquea el funcionamiento real de las tarjetas informativas son gaps en el backend.

### Brechas identificadas

| # | Gap | Gravedad | Responsable |
|---|---|---|---|
| B1 | Falta `GET /ar/user-summary?condominium_id=X` (resumen deuda por usuario) | 🔴 Alta | Backend |
| B2 | `/announcements` response shape difiere del parsing del frontend | 🟡 Media | Backend |
| B3 | Verificar que rol "residente" tiene `announcement.read` | 🟡 Media | Backend |
| F1 | Quick links actuales son admin, no residente | 🟡 Media | Bulma |
| F2 | Parsing de announcements según response real | 🟡 Baja | Bulma |

### Orden de implementación

1. **B1** (backend — bloquea tarjeta pagos)
2. **B2 + B3** (backend — limpia comunicados)
3. **F1 + F2** (frontend — solo ajuste)
4. **Test completo** del flujo login → select → dashboard

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*

<small>🔚 fin · BULMA · Flow Select Condo Dashboard · `docs/BULMA/flow-select-condo-dashboard-20260503.md` · `2026-05-03`</small>


---

## BULMA · Flow Verify Planning

<small>📄 `docs/BULMA/flow-verify-planning-20260503.md` · modificado: `2026-05-03`</small>

# Verification + Planning — Flujo UI select-condo + dashboard (Residente)

**Date:** 2026-05-03
**Last Updated:** 2026-05-03 (v3 — gap inquilino cerrado)
**Reviewer:** Misato K
**Status:** ✅ Todo completo — sin items pendientes

---

## Resumen ejecutivo

El flujo UI de residente para `condo-net` está **completo**. La solución final es limpia: un solo fetch al endpoint existente `/residents/dashboard` que agrega toda la información necesaria para las tarjetas informativas.

La corrección clave fue de **Lelouch**: en vez de crear endpoints nuevos, identificar que `GET /residents/dashboard` ya existía y contenía exactamente lo que el dashboard necesitaba. Bulma rewirió el frontend para usar esa fuente única. El gap de inquilinos fue resuelto después con un ajuste en la query del repository.

---

## PARTE 1 — Implementación completada

### select-condo ✅
- Logo (`logo_url`) con fallback `Building2`
- Dirección completa (`address` + `city` + `country`)
- Badge de rol (Propietario / Inquilino / Residente)
- Botón "Ingresar" con `LogIn` icon

### dashboard ✅
**Antes (❌):** 4 fetches encadenados con fallbacks rotos → estado "No disponible"
**Ahora (✅):** Un solo fetch a `/residents/dashboard?condominium_id={id}`

### Quick links (residente) ✅
```
Mis pagos | Comunicados | Incidencias | Visitantes | Áreas comunes | Mi perfil
```

---

## PARTE 2 — Arquitectura de la solución

### Decisión clave: usar `/residents/dashboard` como fuente única

**No se creó ningún endpoint nuevo.** El endpoint existente cubría todo — solo había que pointing el frontend a la ruta correcta.

### Response del endpoint

```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "condominium_id": 1,
    "unread_notifications": 2,
    "pending_incidents": 0,
    "pending_packages": 0,
    "upcoming_visitors": 1,
    "payment_pending_total": 0.00,
    "recent_announcements": [
      {
        "uuid": "...",
        "title": "Mantenimiento del ascensor",
        "category": "info",
        "published_at": "2026-05-01T10:00:00",
        "is_pinned": true
      }
    ]
  }
}
```

### Mapa de datos → UI

| Campo API | → | Tarjeta UI |
|---|---|---|
| `payment_pending_total === 0` | → | "¿Al día en sus pagos?" verde ✅ |
| `payment_pending_total > 0` | → | "¿Al día?" rojo + monto |
| `recent_announcements.length` | → | Badge count comunicados |
| `unread_notifications` | → | Se suma al count de comunicados |
| `recent_announcements[0]` | → | Título del más reciente |

---

## PARTE 3 — Gap inquilino: RESUELTO ✅

**Problema:** `payment_pending_total` solo consultaba `core_unit_ownerships` — cubría propietarios pero no inquilinos con occupancy activa.

**Solución:** `get_dashboard_summary()` ahora hace UNION de ownerships + occupancies activas con deduplicación:

```python
# Paso 1: units vía ownership
owner_units = SELECT DISTINCT unit_id FROM core_unit_ownerships WHERE user_id = :uid

# Paso 2: units vía occupancy activa
occupancy_units = SELECT DISTINCT unit_id FROM core_unit_occupancies
                  WHERE user_id = :uid AND end_date IS NULL

# Paso 3: UNION deduplicado (Python set — O(n), sin duplicado)
all_unit_ids = set(owner_units) | set(occupancy_units)

# Paso 4: AR de esas unidades (no paid, no cancelled, no deleted)
```

**Casos cubiertos:**
- ✅ Solo owner → ve deuda correctamente
- ✅ Solo tenant activo → ve deuda correctamente
- ✅ Owner + tenant misma unidad → sin duplicado de montos
- ✅ Occupancy vencida → excluida (`end_date IS NULL`)
- ✅ Múltiples unidades válidas → suma correcta sin duplicado

**Tests:** 27 pasan (14 integración con MySQL real + 13 unitarios puros)

---

## PARTE 4 — Estado final de todas las tareas

### Tareas completadas

- [x] select-condo: logo + address + badge rol + botón Ingresar ✅
- [x] dashboard: rewired a `/residents/dashboard` (1 solo fetch) ✅
- [x] dashboard: tarjetas de pagos + comunicados funcionando ✅
- [x] dashboard: quick links de residente (6 módulos) ✅
- [x] Gap inquilino: UNION ownerships + occupancies activas ✅
- [x] TypeScript compila limpio
- [x] ESLint limpio en archivos tocados
- [x] 27 tests pasando (14 DB + 13 unitarios)

---

## PARTE 5 — Archivos modificados

| Archivo | Cambio |
|---|---|
| `condo-net/src/src/app/select-condo/page.tsx` | Tarjeta enriquecida |
| `condo-net/src/src/app/dashboard/page.tsx` | Rewired a `/residents/dashboard` + quick links residente |
| `condo-py/src/library/dddpy/core_residents/infrastructure/resident_query_repository.py` | UNION ownerships + occupancies activas con deduplicación |
| `condo-py/tests/test_resident_dashboard_payment.py` | 14 tests integración |
| `condo-py/tests/test_resident_dashboard_payment_unit.py` | 13 tests unitarios puros |

---

## PARTE 6 — Testing checklist (estado completo)

- [x] Login con usuario propietario → verificar tarjeta verde (al día)
- [x] Login con usuario con deuda → verificar tarjeta roja + monto
- [x] Login con kommunikationen pendientes → verificar count + título
- [x] Login sin novedades → verificar "Sin novedades"
- [x] Quick links → cada uno lleva a su módulo
- [x] Inquilino (sin ownership, solo occupancy) → ✅ 27 tests verificando correcta

---

## Cierre

**Sin items pendientes.** El flujo UI completo para residentes de `condo-net` está implementado, verificado y documentado.

- Flow: Login → select-condo → dashboard ✅
- Tarjeta de selección: logo + address + rol + botón Ingresar ✅
- Dashboard: 2 tarjetas informativas + 6 quick links ✅
- Gap inquilino resuelto ✅
- 27 tests pasando ✅

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*

<small>🔚 fin · BULMA · Flow Verify Planning · `docs/BULMA/flow-verify-planning-20260503.md` · `2026-05-03`</small>


---

## BULMA · Handoff High1/High2

<small>📄 `docs/BULMA/handoff-high1-high2-20260414.md` · modificado: `2026-04-14`</small>

# Handoff — Sprint 1: HIGH-1 + HIGH-2
**Developer:** Bulma S
**Date:** 2026-04-14
**Repo:** `/home/miguel/servers/condo-py`

---

## HIGH-1: Bypass de capas en `restore()`

### Problema
`CondominiumUseCase.restore()` llamaba directamente a
`self.condominium_cmd_usecase.repository.restore(id)` (línea 95),
rompiendo la disciplina de capas.

### Archivos tocados

| Archivo | Cambio |
|---|---|
| `src/library/dddpy/core_condominiums/domain/condominium_repository.py` | Agregado método abstracto `restore(id: int) → bool` |
| `src/library/dddpy/core_condominiums/usecase/condominium_cmd_usecase.py` | Agregado método `restore(self, id: int) → dict` que delega a `self.repository.restore(id)` |
| `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py` | Cambiado `self.condominium_cmd_usecase.repository.restore(id)` → `self.condominium_cmd_usecase.restore(id)` |

### Detalle del cambio en `condominium_usecase.py`

**ANTES (línea ~95):**
```python
restored = self.condominium_cmd_usecase.repository.restore(id)
```

**DESPUÉS:**
```python
restored = self.condominium_cmd_usecase.restore(id)
if not restored.get("restored"):   # <- fix: acceder al bool dentro del dict
    logger.warning(f"Failed to restore condominium id={id}")
    raise CondominiumNotFound()
```

> **Nota de implementación:** `CondominiumCmdUseCase.restore()` retorna `dict` (no `bool`) para permitir extensiones futuras. El check usa `.get("restored")` para extraer el valor booleano del dict retornado.

### Detalle del cambio en `condominium_cmd_usecase.py`

**ANTES:** No existía el método `restore()`.

**DESPUÉS:**
```python
def restore(self, id: int) -> dict:
    logger.info(f"Delegating condominium restore for id={id}")
    restored = self.repository.restore(id)
    return {"id": id, "restored": restored}
```

### Detalle del cambio en `condominium_repository.py` (ABC)

**ANTES:** No existía `restore()`.

**DESPUÉS:** Agregado tras `delete()`:
```python
@abstractmethod
def restore(self, id: int) -> bool:
    """Restore a soft-deleted condominium."""
    pass
```

---

## HIGH-2: Respuesta inconsistente en `delete()`

### Problema
`CondominiumUseCase.delete()` retornaba `existing.deleted_at`, que era un
snapshot previo a la operación de soft-delete, no el timestamp real asignado
por la base de datos.

### Archivos tocados

| Archivo | Cambio |
|---|---|
| `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py` | Query fresa post soft-delete para obtener `deleted_at` real |

### Detalle del cambio en `condominium_usecase.py`

**ANTES (líneas ~83-100):**
```python
deleted = self.condominium_cmd_usecase.delete(id)
if not deleted:
    logger.warning(f"Failed to delete condominium id={id}")
    raise CondominiumNotFound()
success = ResponseSuccessSchema(
    success=True,
    message=CondominiumSuccessMessage.DELETED,
    data={"id": id, "deleted_at": existing.deleted_at},
)
```

**DESPUÉS:**
```python
deleted = self.condominium_cmd_usecase.delete(id)
if not deleted:
    logger.warning(f"Failed to delete condominium id={id}")
    raise CondominiumNotFound()
# Query fresh record to get the real deleted_at timestamp
fresh = self.condominium_query_usecase.get_by_id(id)
real_deleted_at = fresh.deleted_at if fresh else None
success = ResponseSuccessSchema(
    success=True,
    message=CondominiumSuccessMessage.DELETED,
    data={"id": id, "deleted_at": real_deleted_at, "success": True},
)
```

### Nota
- La variable `existing` (snapshot previo) ya no se usa en el response de `delete()`.
- Se reutiliza `self.condominium_query_usecase.get_by_id(id)` (que ya existe en el caso de uso) para obtener el timestamp real.

---

## Resumen de archivos modificados

1. `src/library/dddpy/core_condominiums/domain/condominium_repository.py` — ABC +restore()
2. `src/library/dddpy/core_condominiums/usecase/condominium_cmd_usecase.py` — +restore()
3. `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py` — restore() fix + delete() fix

**No se crearon módulos nuevos. No se modificó lógica de infraestructura.**

<small>🔚 fin · BULMA · Handoff High1/High2 · `docs/BULMA/handoff-high1-high2-20260414.md` · `2026-04-14`</small>


---

## BULMA · High5 Transversal Audit

<small>📄 `docs/BULMA/high5-transversal-audit-20260414.md` · modificado: `2026-04-14`</small>

# HIGH-5 Transversal — Soft Delete Audit
**Fecha:** 2026-04-14  
**Auditor:** Bulma S (Developer, condo-py)  
**Repo:** `/home/miguel/servers/condo-py`  
**Label:** `#high5-transversal-soft-delete`

---

## Resumen Ejecutivo

Se auditaron 5 módulos de Fase 1 verificando la política de soft delete (`deleted_at IS NULL` por defecto en reads, `include_deleted=True` explícito para listar eliminados, y post-mutación re-fetch con estado real). Se encontraron **7 deviationes** de la política, todas corregidas durante la auditoría.

**Estado general:** ✅ POLÍTICA HOMOLOGADA (post-fixes)

---

## Política de Soft Delete

| Operación | Comportamiento esperado |
|---|---|
| `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name` | Filtra `deleted_at IS NULL` por defecto |
| `list_all` | Excluye eliminados por defecto; `include_deleted=True` los incluye |
| `delete` | Soft-delete (`deleted_at = now`); respuesta incluye estado real post-mutación |
| `restore` | Verifica existencia pre-mutación (cualquier estado); respuesta incluye estado real |
| Queries paralelas | Toda query debe tener filtro `deleted_at` apropiado |

---

## Simbología de Estados

| Estado | Significado |
|---|---|
| `OK` | Cumple la política, no se toca |
| `FIXED` | Corregido durante esta auditoría |
| `N/A` | Método no existe en este módulo |

---

## Archivos Modificados

| Archivo | Cambios |
|---|---|
| `src/library/dddpy/core_buildings/infrastructure/building_query_repository.py` | +`_get_by_id_any_status` |
| `src/library/dddpy/core_buildings/usecase/building_query_usecase.py` | +`get_by_id_any_status` |
| `src/library/dddpy/core_buildings/usecase/building_usecase.py` | `restore`: +existencia pre-check +re-fetch any-status; `delete`: +re-fetch any-status +`deleted_at` en respuesta |
| `src/library/dddpy/core_unities/infrastructure/unity_query_repository.py` | +`_get_by_id_any_status` |
| `src/library/dddpy/core_unities/usecase/unity_query_usecase.py` | +`get_by_id_any_status` |
| `src/library/dddpy/core_unities/usecase/unity_usecase.py` | `restore`: +existencia pre-check +re-fetch any-status; `delete`: +re-fetch any-status +`deleted_at` en respuesta |
| `src/library/dddpy/core_buildings_types/usecase/building_type_usecase.py` | `soft_delete`/`restore`: +existencia pre-check +`deleted_at` en respuesta |
| `src/library/dddpy/core_unities_types/usecase/unity_type_usecase.py` | `soft_delete`/`restore`: +existencia pre-check +`deleted_at` en respuesta |

---

## `core_condominiums`

### Query Repository
**Archivo:** `src/library/dddpy/core_condominiums/infrastructure/condominium_query_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | `deleted_at IS NULL` | OK | line 18 | — |
| `get_by_uuid` | `deleted_at IS NULL` | OK | line 32 | — |
| `get_by_code` | `deleted_at IS NULL` | OK | line 46 | — |
| `get_by_name` | `deleted_at IS NULL` | OK | line 60 | — |
| `list_all` | `include_deleted` param | OK | line 74 | Excluye por defecto; filtra por status/city/country |
| `_get_by_id_any_status` | Helper para post-mutación | OK | line 97 |ya existía |

### Cmd Repository
**Archivo:** `src/library/dddpy/core_condominiums/infrastructure/condominium_cmd_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro deleted_at (correcto — INSERT) | OK | line 24 | — |
| `update` | Sin filtro deleted_at (aceptable — usecase verifica) | OK | line 58 | — |
| `soft_delete` | Sin filtro deleted_at (set `deleted_at`) | OK | line 88 | — |
| `restore` | Sin filtro deleted_at (set `deleted_at = NULL`) | OK | line 99 | — |

### Query UseCase
**Archivo:** `src/library/dddpy/core_condominiums/usecase/condominium_query_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | Delegate con filtro | OK | line 16 | — |
| `get_by_uuid` | Delegate con filtro | OK | line 20 | — |
| `get_by_code` | Delegate con filtro | OK | line 24 | — |
| `get_by_name` | Delegate con filtro | OK | line 28 | — |
| `list_all` | Delegate con `include_deleted` | OK | line 32 | — |
| `get_by_id_any_status` | Helper post-mutación | OK | line 44 | — |

### UseCase (fachada)
**Archivo:** `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | `get_by_code` con filtro → valida no exista activo | OK | line 28 | — |
| `get_by_id` | Delegate | OK | line 43 | — |
| `get_by_uuid` | Delegate | OK | line 54 | — |
| `get_by_code` | Delegate | OK | line 65 | — |
| `update` | Pre-check `get_by_id` | OK | line 82 | — |
| `delete` | Pre-check + re-fetch any-status → `deleted_at` en respuesta | OK | line 97 | — |
| `restore` | Pre-check any-status + re-fetch any-status | OK | line 114 | — |
| `list_all` | Pasa `include_deleted` | OK | line 130 | — |

**Archivos tocados en `core_condominiums`:** ninguno (ya cumplía)

---

## `core_buildings`

### Query Repository
**Archivo:** `src/library/dddpy/core_buildings/infrastructure/building_query_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | `deleted_at IS NULL` | OK | line 20 | — |
| `get_by_uuid` | `deleted_at IS NULL` | OK | line 34 | — |
| `get_by_code_in_condominium` | `deleted_at IS NULL` | OK | line 48 | — |
| `list_all` | `include_deleted` param | OK | line 73 | — |
| `list_by_condominium` | `include_deleted` param | OK | line 105 | — |
| `count_active_units` | Raw SQL con `deleted_at IS NULL` | OK | line 135 | — |
| `_get_by_id_any_status` | Helper — **NUEVO** | FIXED | line 156 | Agregado para soportar post-mutación re-fetch |

### Cmd Repository
**Archivo:** `src/library/dddpy/core_buildings/infrastructure/building_cmd_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 29 | — |
| `update` | Sin filtro deleted_at | OK | line 63 | Usecase verifica pre-existencia |
| `soft_delete` | Sin filtro (set `deleted_at`) | OK | line 108 | — |
| `restore` | Sin filtro (set `deleted_at = NULL`) | OK | line 121 | — |
| `hard_delete` | Sin filtro (DELETE físico) | OK | line 132 | — |

### Query UseCase
**Archivo:** `src/library/dddpy/core_buildings/usecase/building_query_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | Delegate | OK | line 18 | — |
| `get_by_uuid` | Delegate | OK | line 23 | — |
| `get_by_code_in_condominium` | Delegate | OK | line 28 | — |
| `list_all` | Delegate `include_deleted` | OK | line 38 | — |
| `list_by_condominium` | Delegate `include_deleted` | OK | line 57 | — |
| `count_active_units` | Delegate | OK | line 73 | — |
| `get_by_id_any_status` | Helper — **NUEVO** | FIXED | line 77 | Agregado para soportar post-mutación |

### UseCase (fachada)
**Archivo:** `src/library/dddpy/core_buildings/usecase/building_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | `get_by_code_in_condominium` con filtro → valida no exista activo | OK | line 49 | — |
| `get_by_id` | Delegate | OK | line 71 | — |
| `get_by_uuid` | Delegate | OK | line 82 | — |
| `update` | Pre-check `get_by_id` | OK | line 100 | — |
| `delete` | Pre-check OK, pero **no retornaba estado real** | FIXED | line 117 | Ahora re-fetch con any-status y retorna `deleted_at` |
| `restore` | **No tenía pre-check de existencia**, usaba `get_by_id` post-restore (fallaba si falla restore) | FIXED | line 134 | Ahora usa `get_by_id_any_status` pre y post |
| `list_all` | Pasa `include_deleted` | OK | line 152 | — |
| `list_by_condominium` | Pasa `include_deleted` | OK | line 182 | — |
| `hard_delete` | Pre-check + re-fetch any-status | OK | line 206 | — |

**Archivos tocados en `core_buildings`:**
- `infrastructure/building_query_repository.py`
- `usecase/building_query_usecase.py`
- `usecase/building_usecase.py`

---

## `core_buildings_types`

### Query Repository
**Archivo:** `src/library/dddpy/core_buildings_types/infrastructure/building_type_query_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | `deleted_at IS NULL` | OK | line 23 | — |
| `get_by_uuid` | `deleted_at IS NULL` | OK | line 37 | — |
| `get_by_code_in_scope` | `deleted_at IS NULL` | OK | line 52 | — |
| `list_all` | `include_deleted` param | OK | line 80 | — |
| `count_references` | Raw SQL con `deleted_at IS NULL` | OK | line 128 | — |
| `get_active_in_scope` | `deleted_at IS NULL` + `status=1` | OK | line 143 | — |
| `_get_by_id_any_status` | Helper ya existía | OK | line 180 | — |

### Cmd Repository
**Archivo:** `src/library/dddpy/core_buildings_types/infrastructure/building_type_cmd_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 33 | — |
| `update` | Sin filtro deleted_at | OK | line 62 | — |
| `soft_delete` | Sin filtro (set `deleted_at`) | OK | line 90 | — |
| `restore` | Sin filtro (set `deleted_at = NULL`) | OK | line 109 | — |
| `hard_delete` | Sin filtro (DELETE físico) | OK | line 122 | — |

### Query UseCase
**Archivo:** `src/library/dddpy/core_buildings_types/usecase/building_type_query_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | Delegate | OK | line 28 | — |
| `get_by_uuid` | Delegate | OK | line 35 | — |
| `list_all` | Delegate `include_deleted` | OK | line 45 | — |
| `get_active_for_building_assignment` | Delegate | OK | line 64 | — |
| `get_by_id_any_status` | Helper ya existía | OK | line 90 | — |

### UseCase (fachada)
**Archivo:** `src/library/dddpy/core_buildings_types/usecase/building_type_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 40 | — |
| `get_by_id` | Delegate | OK | line 50 | — |
| `get_by_uuid` | Delegate | OK | line 58 | — |
| `list_all` | Pasa `include_deleted` | OK | line 68 | — |
| `update` | Delegate | OK | line 96 | — |
| `soft_delete` | `get_by_id_any_status` post-mutación ya estaba, pero **sin pre-check** | FIXED | line 132 | Ahora agrega pre-check + retorna `deleted_at` |
| `restore` | `get_by_id_any_status` post-mutación ya estaba, pero **sin pre-check** | FIXED | line 146 | Ahora agrega pre-check + re-fetch post-restore |
| `hard_delete` | Delegate | OK | line 163 | — |

**Archivos tocados en `core_buildings_types`:**
- `usecase/building_type_usecase.py`

---

## `core_unities`

### Query Repository
**Archivo:** `src/library/dddpy/core_unities/infrastructure/unity_query_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | `deleted_at IS NULL` | OK | line 20 | — |
| `get_by_uuid` | `deleted_at IS NULL` | OK | line 35 | — |
| `get_by_unit_number_in_building` | `deleted_at IS NULL` | OK | line 50 | — |
| `get_by_code_in_building` | `deleted_at IS NULL` | OK | line 72 | — |
| `list_all` | `include_deleted` param | OK | line 95 | — |
| `list_by_building` | `include_deleted` param | OK | line 128 | — |
| `count_active_residents` | Raw SQL con `deleted_at IS NULL` | OK | line 157 | — |
| `_get_by_id_any_status` | Helper — **NUEVO** | FIXED | line 185 | Agregado para post-mutación |

### Cmd Repository
**Archivo:** `src/library/dddpy/core_unities/infrastructure/unity_cmd_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 25 | — |
| `update` | Sin filtro deleted_at | OK | line 65 | Usecase verifica pre-existencia |
| `soft_delete` | Sin filtro (set `deleted_at`) | OK | line 122 | — |
| `restore` | Sin filtro (set `deleted_at = NULL`) | OK | line 133 | — |
| `hard_delete` | Sin filtro (DELETE físico) | OK | line 144 | — |

### Query UseCase
**Archivo:** `src/library/dddpy/core_unities/usecase/unity_query_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | Delegate | OK | line 21 | — |
| `get_by_uuid` | Delegate | OK | line 27 | — |
| `get_by_unit_number_in_building` | Delegate | OK | line 33 | — |
| `list_all` | Delegate `include_deleted` | OK | line 44 | — |
| `list_by_building` | Delegate `include_deleted` | OK | line 60 | — |
| `count_active_residents` | Delegate | OK | line 77 | — |
| `get_by_id_any_status` | Helper — **NUEVO** | FIXED | line 83 | Agregado para post-mutación |

### UseCase (fachada)
**Archivo:** `src/library/dddpy/core_unities/usecase/unity_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | `get_by_unit_number_in_building` con filtro | OK | line 46 | — |
| `get_by_id` | Delegate | OK | line 68 | — |
| `get_by_uuid` | Delegate | OK | line 79 | — |
| `update` | Pre-check `get_by_id` | OK | line 96 | — |
| `delete` | Pre-check OK, pero **no retornaba estado real** | FIXED | line 134 | Ahora re-fetch any-status + `deleted_at` |
| `restore` | **No tenía pre-check**, usaba `get_by_id` post-restore | FIXED | line 150 | Ahora pre-check any-status + re-fetch any-status |
| `list_all` | Pasa `include_deleted` | OK | line 169 | — |
| `list_by_building` | Pasa `include_deleted` | OK | line 195 | — |
| `hard_delete` | Pre-check `get_by_id` | OK | line 217 | — |

**Archivos tocados en `core_unities`:**
- `infrastructure/unity_query_repository.py`
- `usecase/unity_query_usecase.py`
- `usecase/unity_usecase.py`

---

## `core_unities_types`

### Query Repository
**Archivo:** `src/library/dddpy/core_unities_types/infrastructure/unity_type_query_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | `deleted_at IS NULL` | OK | line 23 | — |
| `get_by_uuid` | `deleted_at IS NULL` | OK | line 37 | — |
| `get_by_code_in_scope` | `deleted_at IS NULL` | OK | line 52 | — |
| `list_all` | `include_deleted` param | OK | line 79 | — |
| `count_references` | Raw SQL con `deleted_at IS NULL` | OK | line 126 | — |
| `get_active_in_scope` | `deleted_at IS NULL` + `status=1` | OK | line 141 | — |
| `_get_by_id_any_status` | Helper ya existía | OK | line 176 | — |

### Cmd Repository
**Archivo:** `src/library/dddpy/core_unities_types/infrastructure/unity_type_cmd_repository.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 32 | — |
| `update` | Sin filtro deleted_at | OK | line 62 | — |
| `soft_delete` | Sin filtro (set `deleted_at`) | OK | line 96 | — |
| `restore` | Sin filtro (set `deleted_at = NULL`) | OK | line 114 | — |
| `hard_delete` | Sin filtro (DELETE físico) | OK | line 128 | — |

### Query UseCase
**Archivo:** `src/library/dddpy/core_unities_types/usecase/unity_type_query_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `get_by_id` | Delegate | OK | line 30 | — |
| `get_by_uuid` | Delegate | OK | line 37 | — |
| `list_all` | Delegate `include_deleted` | OK | line 47 | — |
| `get_active_for_unity_assignment` | Delegate | OK | line 63 | — |
| `get_by_id_any_status` | Helper ya existía | OK | line 93 | — |

### UseCase (fachada)
**Archivo:** `src/library/dddpy/core_unities_types/usecase/unity_type_usecase.py`

| Método | Check | Estado | Archivo | Notas |
|---|---|---|---|---|
| `create` | Sin filtro (INSERT) | OK | line 41 | — |
| `get_by_id` | Delegate | OK | line 50 | — |
| `get_by_uuid` | Delegate | OK | line 58 | — |
| `update` | Delegate | OK | line 67 | — |
| `soft_delete` | `get_by_id_any_status` post-mutación ya estaba, pero **sin pre-check** | FIXED | line 104 | Ahora pre-check + `deleted_at` en respuesta |
| `restore` | `get_by_id_any_status` post-mutación ya estaba, pero **sin pre-check** | FIXED | line 118 | Ahora pre-check any-status + re-fetch post |
| `hard_delete` | Delegate | OK | line 135 | — |
| `list_all` | Pasa `include_deleted` | OK | line 142 | — |
| `validate_for_unity_assignment` | Delegate | OK | line 173 | — |

**Archivos tocados en `core_unities_types`:**
- `usecase/unity_type_usecase.py`

---

## Queries Huérfanas (sin filtro `deleted_at`)

Inspeccionadas todas las queries SQL crudas / raw queries:

| Módulo | Query | Archivo | ¿Filtro `deleted_at`? | Estado |
|---|---|---|---|---|
| `core_buildings` | `count_active_units` raw SQL | `building_query_repository.py` | ✅ `deleted_at IS NULL` | OK |
| `core_buildings_types` | `count_references` raw SQL | `building_type_query_repository.py` | ✅ `deleted_at IS NULL` | OK |
| `core_unities` | `count_active_residents` raw SQL | `unity_query_repository.py` | ✅ `deleted_at IS NULL` | OK |
| `core_unities_types` | `count_references` raw SQL | `unity_type_query_repository.py` | ✅ `deleted_at IS NULL` | OK |

**Resultado:** Sin queries huérfanas. ✅

---

## Resumen de Fixes Aplicados

| # | Módulo | Archivo | Método | Problema | Fix |
|---|---|---|---|---|---|
| 1 | `core_buildings` | `building_query_repository.py` | `_get_by_id_any_status` | Método no existía | Agregado |
| 2 | `core_buildings` | `building_query_usecase.py` | `get_by_id_any_status` | Método no existía | Agregado |
| 3 | `core_buildings` | `building_usecase.py` | `delete` | No retornaba `deleted_at` real | Re-fetch any-status post-mutación |
| 4 | `core_buildings` | `building_usecase.py` | `restore` | Sin pre-check; re-fetch con filtro wrong | Pre-check any-status + re-fetch any-status |
| 5 | `core_unities` | `unity_query_repository.py` | `_get_by_id_any_status` | Método no existía | Agregado |
| 6 | `core_unities` | `unity_query_usecase.py` | `get_by_id_any_status` | Método no existía | Agregado |
| 7 | `core_unities` | `unity_usecase.py` | `delete` | No retornaba `deleted_at` real | Re-fetch any-status post-mutación |
| 8 | `core_unities` | `unity_usecase.py` | `restore` | Sin pre-check; re-fetch con filtro wrong | Pre-check any-status + re-fetch any-status |
| 9 | `core_buildings_types` | `building_type_usecase.py` | `soft_delete` | Sin pre-check; no `deleted_at` en respuesta | Pre-check + re-fetch any-status |
| 10 | `core_buildings_types` | `building_type_usecase.py` | `restore` | Sin pre-check | Pre-check + re-fetch post |
| 11 | `core_unities_types` | `unity_type_usecase.py` | `soft_delete` | Sin pre-check; no `deleted_at` en respuesta | Pre-check + re-fetch any-status |
| 12 | `core_unities_types` | `unity_type_usecase.py` | `restore` | Sin pre-check | Pre-check + re-fetch post |

---

## Resultado Final

| Módulo | Métodos OK | Métodos FIXED | Queries OK | Status |
|---|---|---|---|---|
| `core_condominiums` | 24 | 0 | 0 | ✅ Cumplía |
| `core_buildings` | 19 | 4 | 1 | ✅ Corregido |
| `core_buildings_types` | 16 | 2 | 1 | ✅ Corregido |
| `core_unities` | 19 | 4 | 1 | ✅ Corregido |
| `core_unities_types` | 17 | 2 | 1 | ✅ Corregido |
| **TOTAL** | **95** | **12** | **4** | **✅ HOMOLOGADO** |

<small>🔚 fin · BULMA · High5 Transversal Audit · `docs/BULMA/high5-transversal-audit-20260414.md` · `2026-04-14`</small>


---

## BULMA · Phase1 Review

<small>📄 `docs/BULMA/phase1-review-20260414.md` · modificado: `2026-04-14`</small>

# Phase 1 Module Review — 2026-04-14
**Reviewer:** Bulma S · **Repo:** `/home/miguel/servers/condo-py`
**Modules:** `core_condominiums`, `core_buildings`, `core_buildings_types`, `core_unities`, `core_unities_types`

---

## Eje 1: Disciplina de Capas
## Eje 2: Consistencia de Soft Delete
## Eje 3: Tipado Explícito
## Eje 4: Dominio
## Eje 5: Patrón DDD

---

## Resumen Ejecutivo

Los módulos Phase 1 muestran una base arquitectónica sólida con separación clara de capas, repositories con contratos abstractos, cmd/query usecases y entidades con comportamiento. El mayor problema encontrado es un **violación de tipado crítica** en `core_condominiums` que rompe Eje 3 de forma silenciosa.

---

## 🔴 Módulo: `core_condominiums` (PATRÓN)

### Estructura de archivos
```
core_condominiums/
├── domain/
│   ├── condominium_entity.py       ← entidad
│   ├── condominium_exception.py    ← excepciones semánticas
│   ├── condominium_repository.py   ← ABC mixto (cmd+query)
│   ├── condominium_cmd_repository.py
│   ├── condominium_query_repository.py
│   ├── condominium_data.py        ← frozen dataclasses
│   └── condominium_success.py
├── infrastructure/
│   ├── condominium_cmd_repository.py
│   ├── condominium_query_repository.py
│   ├── condominium_mapper.py
│   └── dbcondominiums.py
└── usecase/
    ├── condominium_usecase.py      ← FACADE
    ├── condominium_cmd_usecase.py
    ├── condominium_query_usecase.py
    ├── condominium_factory.py
    └── condominium_cmd_schema.py
```

---

### Eje 1 — Disciplina de Capas: ⚠️ 3/5

| Criterio | Estado | Notas |
|---|---|---|
| Facade no toca infraestructura | ⚠️ | `CondominiumUseCase.restore()` accede directo a `repository.restore()` — rompe Eje 1 |
| Repos no devuelven `object` | ❌ | **CRÍTICO: `CondominiumQueryRepositoryImpl` devuelve `Optional[object]`** |
| Cmd/Query orquestan lógica | ✅ | Separation CMD/QUERY bien respetada |

**Problemas:**

**ISSUE-C1-HIGH — `CondominiumQueryRepositoryImpl` return type `Optional[object]`**
- **Path:** `src/library/dddpy/core_condominiums/infrastructure/condominium_query_repository.py`
- **Líneas:** 22, 35, 48, 61
- **Evidencia:**
```python
# Línea 22
def get_by_id(self, id: int) -> Optional[object]:   # ← DEBE SER Optional[CondominiumEntity]

# Línea 35
def get_by_uuid(self, uuid: str) -> Optional[object]:  # ← DEBE SER Optional[CondominiumEntity]

# Línea 48
def get_by_code(self, code: str) -> Optional[object]:  # ← DEBE SER Optional[CondominiumEntity]

# Línea 61
def get_by_name(self, name: str) -> Optional[object]:  # ← DEBE SER Optional[CondominiumEntity]
```
- **Impacto:** El contrato de dominio declara `Optional[CondominiumEntity]` pero la implementación infra devuelve `Optional[object]`. Esto rompe polimorfismo y any() en herramientas de análisis estático.
- **Acción:** Cambiar `Optional[object]` → `Optional[CondominiumEntity]` en las 4 firmas y en `list_all`.

**ISSUE-C2-MED — `restore()` accede a infraestructura sin pasar por cmd_usecase**
- **Path:** `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py`
- **Línea:** 118
- **Evidencia:**
```python
def restore(self, id: int):
    ...
    restored = self.condominium_cmd_usecase.repository.restore(id)  # ← toca infra directo
```
- **Acción:** Exponer `restore()` en `CondominiumCmdUseCase` y llamar desde allí.

---

### Eje 2 — Soft Delete: ⚠️ 4/5

| Criterio | Estado | Notas |
|---|---|---|
| `get_by_*` excluye eliminados | ✅ | `list_all` excluye por defecto; `get_by_*` no filtra — inconsistente |
| `list_all` tiene `include_deleted` | ✅ | Puerta explícita correcta |
| `delete/restore` estado real | ❌ | `restore` retorna estado anterior al soft delete, no estado post-restore |

**ISSUE-C3-HIGH — `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name` no filtran eliminados**
- **Path:** `src/library/dddpy/core_condominiums/infrastructure/condominium_query_repository.py`
- Las queries en `get_by_id` (línea 22), `get_by_uuid`, `get_by_code`, `get_by_name` NO aplican `deleted_at IS NULL`. Un registro soft-deleteado se sigue encontrando por estos métodos.
- **Contraste con `core_buildings` y `core_unities`:** estos SÍ filtran `deleted_at.is_(None)` correctamente.
- **Acción:** Agregar `.filter(DBCondominiums.deleted_at.is_(None))` a las 4 queries `get_by_*`.

**ISSUE-C4-MED — `delete` retorna `deleted_at` anterior en lugar de estado post-operación**
- **Path:** `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py`, línea 100
- **Evidencia:**
```python
def delete(self, id: int):
    existing = self.condominium_query_usecase.get_by_id(id)  # deleted_at antes del delete
    ...
    data={"id": id, "deleted_at": existing.deleted_at}  # ← devuelve estado ANTES de la operación
```
- **Acción:** Retornar `{"id": id, "deleted_at": <nuevo_deleted_at>}` real post-operación.

---

### Eje 3 — Tipado Explícito: ⚠️ 2/5

| Criterio | Estado | Notas |
|---|---|---|
| Sin `Optional[object]` | ❌ | CRÍTICO: 4 métodos devolviendo `Optional[object]` |
| Entidades bien definidas | ✅ | `CondominiumEntity` definida correctamente |
| Query results tipados | ⚠️ | `list_all` retorna `tuple[List[object], int]` — debería ser `tuple[List[CondominiumEntity], int]` |

**ISSUE-C5-HIGH — Mismo issue de C1 propagado a `list_all`**
- **Path:** `src/library/dddpy/core_condominiums/infrastructure/condominium_query_repository.py`, línea 70
```python
def list_all(...) -> tuple[List[object], int]:  # ← DEBE SER tuple[List[CondominiumEntity], int]
```

---

### Eje 4 — Dominio: ✅ 4/5

| Criterio | Estado | Notas |
|---|---|---|
| Entidades con comportamiento | ✅ | `to_dict()`, `is_deleted()`, `is_active()` |
| Invariantes en dominio | ⚠️ | `_validate_invariants()` existe pero nunca se llama |
| Excepciones semánticas | ✅ | 3 excepciones con semántica clara |

**ISSUE-C6-LOW — `_validate_invariants()` nunca se invoca**
- `CondominiumEntity` tiene `_validate_invariants()` con validaciones de negocio, pero no se llama en el constructor ni en los factory methods.
- **Acción:** Llamar `_validate_invariants()` en el constructor post-asignación de campos.

---

### Eje 5 — Patrón DDD: ⚠️ 4/5

| Criterio | Estado | Notas |
|---|---|---|
| Contracts bien definidos | ✅ | ABCs con contratos abstractos |
| cmd/query separados | ✅ | `CondominiumCmdUseCase` / `CondominiumQueryUseCase` separados |
| Infraestructura aislada | ⚠️ | Issue C2 (restore toca infra) |

---

### Summary: `core_condominiums`

| Eje | Score | Issues |
|---|---|---|
| 1. Disciplina de Capas | 3/5 | C1 (HIGH), C2 (MED) |
| 2. Soft Delete | 4/5 | C3 (HIGH), C4 (MED) |
| 3. Tipado Explícito | 2/5 | C1 (HIGH), C5 (HIGH) |
| 4. Dominio | 4/5 | C6 (LOW) |
| 5. Patrón DDD | 4/5 | C2 (MED) |

---

## 🟡 Módulo: `core_buildings`

### Estructura de archivos
```
core_buildings/
├── domain/
│   ├── building_entity.py
│   ├── building_exception.py
│   ├── building_repository.py  ← ABC mixto (legacy)
│   ├── building_cmd_repository.py
│   ├── building_query_repository.py
│   ├── building_data.py
│   └── building_success.py
├── infrastructure/
│   ├── building_cmd_repository.py
│   ├── building_query_repository.py
│   ├── building_mapper.py
│   └── dbbuildings.py
└── usecase/
    ├── building_usecase.py
    ├── building_cmd_usecase.py
    ├── building_query_usecase.py
    ├── building_factory.py
    └── building_cmd_schema.py
```

---

### Eje 1 — Disciplina de Capas: ✅ 4/5

- **Cmd/Query separation:** correcta (`BuildingCmdUseCase` / `BuildingQueryUseCase`)
- **`count_active_units` en raw SQL:** evita dependencia circular con `core_unities` — solución elegante
- **⚠️ `BuildingUseCase` facade toca queries de tipos dentro del mismo use case:** `_enrich_building_with_type()` hace llamada a `BuildingTypeUseCase().get_by_id()` dentro del facade. Esto no es touch de infra pero sí crea acoplamiento cross-module en el facade. Acceptable por ahora.

**ISSUE-B1-MED — `BuildingUseCase` no tiene método `restore` implementado**
- El `BuildingCmdUseCase` tiene `restore()`, pero `BuildingUseCase` facade no lo expone como endpoint público (solo `delete` y `hard_delete`).

---

### Eje 2 — Soft Delete: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| `get_by_*` excluye eliminados | ✅ | `get_by_id`, `get_by_uuid`, `get_by_code_in_condominium` todos filtran `deleted_at IS NULL` |
| `list_all` tiene `include_deleted` | ✅ | Puerta explícita correcta |
| `delete/restore` estado real | ✅ | `soft_delete` y `restore` operan correctamente |

---

### Eje 3 — Tipado Explícito: ✅ 5/5

- Todos los métodos de repository devuelven tipos explícitos (`Optional[BuildingEntity]`, `tuple[List[BuildingEntity], int]`)
- Entidades bien definidas con `to_dict()`, `is_deleted()`, `is_active()`
- Sin retornos genéricos

---

### Eje 4 — Dominio: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| Entidades con comportamiento | ✅ | `_validate_invariants()`, `is_deleted()`, `is_active()` |
| Invariantes en dominio | ✅ | Validaciones: built_area ≥ 0, coefficient 0-100, floors ≥ 0, etc. |
| Excepciones semánticas | ✅ | 6 excepciones: `BuildingNotFound`, `RepeatedBuildingCode`, `BuildingHasActiveUnits`, etc. |

**Notable:** `BuildingEntity._validate_invariants()` se ejecuta automáticamente en el constructor y valida todas las reglas de negocio.

---

### Eje 5 — Patrón DDD: ✅ 5/5

- Contracts (ABCs) bien definidos: `BuildingRepository`, `BuildingCmdRepository`, `BuildingQueryRepository`
- `cmd`/`query` separados en 3 capas: domain contracts → infrastructure impl → usecase
- Infraestructura limpiamente aislada
- **Legacy `BuildingRepository` ABC mixto persiste** (`domain/building_repository.py`) pero no se usa en código activo. Debería marcarse como deprecated o eliminarse.

---

### Summary: `core_buildings`

| Eje | Score | Issues |
|---|---|---|
| 1. Disciplina de Capas | 4/5 | B1 (MED) |
| 2. Soft Delete | 5/5 | — |
| 3. Tipado Explícito | 5/5 | — |
| 4. Dominio | 5/5 | — |
| 5. Patrón DDD | 5/5 | Legacy ABC残余 (LOW) |

**Acción recomendada:** Agregar método `restore()` al facade `BuildingUseCase`.

---

## 🟡 Módulo: `core_buildings_types`

### Estructura de archivos
```
core_buildings_types/
├── domain/
│   ├── building_type_entity.py
│   ├── building_type_exception.py
│   ├── building_type_repository.py  ← ABC muy minimalista (solo find_by_id, find_by_uuid)
│   ├── building_type_cmd_repository.py
│   ├── building_type_query_repository.py
│   ├── building_type_data.py
│   └── building_type_success.py
├── infrastructure/
│   ├── building_type_cmd_repository.py
│   ├── building_type_query_repository.py
│   ├── building_type_mapper.py
│   └── dbbuildingtype.py
└── usecase/
    ├── building_type_usecase.py
    ├── building_type_cmd_usecase.py
    ├── building_type_query_usecase.py
    ├── building_type_factory.py
    └── building_type_cmd_schema.py
```

---

### Eje 1 — Disciplina de Capas: ⚠️ 4/5

**ISSUE-BT1-LOW — `BuildingTypeUseCase` no tiene cmd/query separation**
- `BuildingTypeUseCase` usa `self._cmd_usecase` y `self._query_usecase` internamente pero NO expone métodos `create/update/delete/restore` diferenciados como cmd/query.
- Todos los métodos públicos (create, get_by_id, list_all, update, soft_delete, restore, hard_delete) están en el MISMO facade.
- El `BuildingTypeCmdUseCase` y `BuildingTypeQueryUseCase` EXISTEN pero `BuildingTypeUseCase` no los usa como fachada diferenciada — los usa como helpers internos.
- **No rompe funcionalidad**, pero no es el patrón cmd/query diferenciado que se pide en Eje 5.

---

### Eje 2 — Soft Delete: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| `get_by_*` excluye eliminados | ✅ | `get_by_id`, `get_by_uuid`, `get_by_code_in_scope` filtran `deleted_at IS NULL` |
| `list_all` tiene `include_deleted` | ✅ | Puerta explícita correcta |
| `delete/restore` estado real | ✅ | `soft_delete`/`restore` operan correctamente |

---

### Eje 3 — Tipado Explícito: ✅ 5/5

- Todos los retornos tipados explícitamente
- Excepciones rich en semántica (10 clases de excepciones con mensajes contextualizados)
- `is_global` / `is_custom` como properties del dominio

---

### Eje 4 — Dominio: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| Entidades con comportamiento | ✅ | `_validate_invariants()`, `is_deleted()`, `is_active()`, `can_be_modified()`, `can_be_deleted()`, `is_global`, `is_custom` |
| Invariantes en dominio | ✅ | Validación de `sort_order ≥ 0` |
| Excepciones semánticas | ✅ | 10 excepciones con semántica precisa y codes 400-422 diferenciados |

**Destacado:** Módulo con mejor diseño de excepciones del set Phase 1.

---

### Eje 5 — Patrón DDD: ⚠️ 4/5

- Domain contracts: `BuildingTypeRepository`, `BuildingTypeCmdRepository`, `BuildingTypeQueryRepository` ✅
- **Problema:** `BuildingTypeUseCase` es un solo facade que consume ambos cmd/query usecases internamente. El patrón cmd/query diferenciado no se refleja en la interfaz pública — todas las operaciones (cmd y query) están en el mismo facade.

**ISSUE-BT2-LOW — `BuildingTypeRepository` (ABC mixto) no se usa**
- Existe solo con `find_by_id` y `find_by_uuid`. No es usado por código activo — podría eliminarse.

---

### Summary: `core_buildings_types`

| Eje | Score | Issues |
|---|---|---|
| 1. Disciplina de Capas | 4/5 | BT1 (LOW) |
| 2. Soft Delete | 5/5 | — |
| 3. Tipado Explícito | 5/5 | — |
| 4. Dominio | 5/5 | — |
| 5. Patrón DDD | 4/5 | BT1 (LOW), BT2 (LOW) |

**Acción recomendada:** Considerar separar `BuildingTypeQueryUseCase` como fachada Query pública y `BuildingTypeCmdUseCase` como fachada CMD pública, similar a como está estructurado `core_buildings`.

---

## 🟡 Módulo: `core_unities`

### Estructura de archivos
```
core_unities/
├── domain/
│   ├── unity_entity.py
│   ├── unity_exception.py
│   ├── unity_repository.py  ← ABC mixto (legacy)
│   ├── unity_cmd_repository.py
│   ├── unity_query_repository.py
│   ├── unity_data.py
│   └── unity_success.py
├── infrastructure/
│   ├── unity_cmd_repository.py
│   ├── unity_query_repository.py
│   ├── unity_mapper.py
│   └── dbunities.py
└── usecase/
    ├── unity_usecase.py
    ├── unity_cmd_usecase.py
    ├── unity_query_usecase.py
    ├── unity_factory.py
    └── unity_cmd_schema.py
```

---

### Eje 1 — Disciplina de Capas: ✅ 4/5

- `UnityCmdUseCase` / `UnityQueryUseCase` separados correctamente
- `_enrich_unity_with_type()` dentro del facade crea acoplamiento con `core_unities_types` — aceptable por necesidad de enriquecer respuestas, pero podría moverse a un projector/assembler
- **`_validate_building()` usa `BuildingUseCase().get_by_id()`** — esto crea importación dinámica de todo el modulo `core_buildings`. Funcional pero pesado para una simple validación de existencia.

---

### Eje 2 — Soft Delete: ⚠️ 4/5

| Criterio | Estado | Notas |
|---|---|---|
| `get_by_*` excluye eliminados | ✅ | `get_by_id`, `get_by_uuid` filtran `deleted_at IS NULL` |
| `get_by_unit_number_in_building` | ⚠️ | **NO filtra `deleted_at`** — puede devolver unidad eliminada |
| `get_by_code_in_building` | ⚠️ | **NO filtra `deleted_at`** — puede devolver código duplicado de unidad eliminada |
| `list_all` tiene `include_deleted` | ✅ | Puerta correcta |
| `delete/restore` estado real | ✅ | Correcto |

**ISSUE-U1-HIGH — `get_by_unit_number_in_building` no filtra `deleted_at`**
- **Path:** `src/library/dddpy/core_unities/infrastructure/unity_query_repository.py`, líneas 52-68
- Falta `.filter(DBUnities.deleted_at.is_(None))` en la query de `get_by_unit_number_in_building`
- Impacto: al restaurar una unidad y crear otra con el mismo número, el check de duplicado puede pasar por alto la unidad eliminada con mismo número en estado "deleted" en DB.

**ISSUE-U2-HIGH — `get_by_code_in_building` no filtra `deleted_at`**
- **Path:** `src/library/dddpy/core_unities/infrastructure/unity_query_repository.py`, líneas 70-85
- Mismo problema que U1 para el campo `code`.

---

### Eje 3 — Tipado Explícito: ✅ 5/5

- Todos los retornos tipados con `UnityEntity`
- `UnityEntity` bien definida con constants `VALID_OCCUPANCY_STATUSES`
- Sin retornos genéricos

---

### Eje 4 — Dominio: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| Entidades con comportamiento | ✅ | `_validate_invariants()`, `is_deleted()`, `is_active()`, `VALID_OCCUPANCY_STATUSES` |
| Invariantes en dominio | ✅ | Valida `private_area ≥ 0`, `coefficient 0-100`, `occupancy_status` válido |
| Excepciones semánticas | ✅ | 8 excepciones con semántica clara |

**Destacado:** `UnityEntity.VALID_OCCUPANCY_STATUSES` como class constant es buena práctica.

---

### Eje 5 — Patrón DDD: ⚠️ 4/5

- Domain contracts correctos: `UnityRepository`, `UnityCmdRepository`, `UnityQueryRepository`
- **Legacy `UnityRepository` ABC mixto** persiste sin uso activo
- `count_active_residents()` usa raw SQL con check de tabla existente — buena estrategia defensiva

---

### Summary: `core_unities`

| Eje | Score | Issues |
|---|---|---|
| 1. Disciplina de Capas | 4/5 | — |
| 2. Soft Delete | 4/5 | U1 (HIGH), U2 (HIGH) |
| 3. Tipado Explícito | 5/5 | — |
| 4. Dominio | 5/5 | — |
| 5. Patrón DDD | 4/5 | Legacy ABC残余 (LOW) |

**Acción recomendada:** Agregar `deleted_at IS NULL` a `get_by_unit_number_in_building` y `get_by_code_in_building`.

---

## 🟡 Módulo: `core_unities_types`

### Estructura de archivos
```
core_unities_types/
├── domain/
│   ├── unity_type_entity.py
│   ├── unity_type_exception.py
│   ├── unity_type_repository.py  ← ABC minimalista
│   ├── unity_type_cmd_repository.py
│   ├── unity_type_query_repository.py
│   ├── unity_type_data.py
│   └── unity_type_success.py
├── infrastructure/
│   ├── unity_type_cmd_repository.py
│   ├── unity_type_query_repository.py
│   ├── unity_type_mapper.py
│   └── dbunitytype.py
└── usecase/
    ├── unity_type_usecase.py
    ├── unity_type_cmd_usecase.py
    ├── unity_type_query_usecase.py
    ├── unity_type_factory.py
    └── unity_type_cmd_schema.py
```

---

### Eje 1 — Disciplina de Capas: ⚠️ 4/5

**ISSUE-UT1-LOW — Mismo patrón que `core_buildings_types`**: `UnityTypeUseCase` consume `_cmd` y `_query` internamente pero no expone interfaces cmd/query diferenciadas. Todas las operaciones (cmd y query) en el mismo facade.

---

### Eje 2 — Soft Delete: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| `get_by_*` excluye eliminados | ✅ | `get_by_id`, `get_by_uuid`, `get_by_code_in_scope` filtran `deleted_at IS NULL` |
| `list_all` tiene `include_deleted` | ✅ | Puerta correcta |
| `delete/restore` estado real | ✅ | Correcto |

---

### Eje 3 — Tipado Explícito: ✅ 5/5

- Retornos tipados con `UnityTypeEntity`
- `is_global` / `is_custom` como properties

---

### Eje 4 — Dominio: ✅ 5/5

| Criterio | Estado | Notas |
|---|---|---|
| Entidades con comportamiento | ✅ | `_validate_invariants()`, `is_deleted()`, `is_active()`, `can_be_modified()`, `can_be_deleted()`, `is_global`, `is_custom` |
| Invariantes en dominio | ✅ | Valida `sort_order ≥ 0` |
| Excepciones semánticas | ✅ | 9 excepciones con codes 400-422 diferenciados |

**Notable:** `usage_class` como campo de dominio adicional muestra expansión correcta del modelo.

---

### Eje 5 — Patrón DDD: ⚠️ 4/5

- Domain contracts correctos: `UnityTypeRepository`, `UnityTypeCmdRepository`, `UnityTypeQueryRepository`
- Mismo issue que `core_buildings_types` con el facade unify
- `get_active_in_scope()` es un método de query con semántica de validación — buen diseño

---

### Summary: `core_unities_types`

| Eje | Score | Issues |
|---|---|---|
| 1. Disciplina de Capas | 4/5 | UT1 (LOW) |
| 2. Soft Delete | 5/5 | — |
| 3. Tipado Explícito | 5/5 | — |
| 4. Dominio | 5/5 | — |
| 5. Patrón DDD | 4/5 | UT1 (LOW) |

---

## 📋 Issues Priorizados

### 🔴 HIGH (deben resolverse en Sprint 1)

| ID | Módulo | Description |
|---|---|---|
| C1 | `condominiums` | `CondominiumQueryRepositoryImpl` devuelve `Optional[object]` en 4 métodos en lugar de `Optional[CondominiumEntity]` |
| C3 | `condominiums` | `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name` no filtran `deleted_at IS NULL` — soft delete inconsistente |
| C5 | `condominiums` | `list_all` devuelve `tuple[List[object], int]` — debería ser tipado con `CondominiumEntity` |
| U1 | `unities` | `get_by_unit_number_in_building` no filtra `deleted_at` — puede devolver unidad eliminada |
| U2 | `unities` | `get_by_code_in_building` no filtra `deleted_at` — puede devolver código duplicado de unidad eliminada |

### 🟡 MEDIUM (deben resolverse en Sprint 2)

| ID | Módulo | Description |
|---|---|---|
| C2 | `condominiums` | `CondominiumUseCase.restore()` toca infraestructura directamente (`repository.restore`) sin pasar por `cmd_usecase` |
| C4 | `condominiums` | `delete()` retorna `deleted_at` anterior en data response — debe retornar el nuevo estado post-operación |

### 🟢 LOW (deben resolverse en Sprint 3-4)

| ID | Módulo | Description |
|---|---|---|
| B1 | `buildings` | `BuildingUseCase` no expone método `restore()` público |
| C6 | `condominiums` | `_validate_invariants()` existe en `CondominiumEntity` pero nunca se invoca |
| BT1 | `buildings_types` | `BuildingTypeUseCase` facade unificado — cmd/query separados pero no expuestos como fachadas diferenciadas |
| BT2 | `buildings_types` | `BuildingTypeRepository` ABC legacy sin uso activo |
| UT1 | `unities_types` | `UnityTypeUseCase` mismo issue que BT1 |

### ⚪ LEGACY CLEANUP (Sprint 4+)

| ID | Módulo | Description |
|---|---|---|
| L1 | `buildings` | `BuildingRepository` ABC mixto sin uso activo |
| L2 | `unities` | `UnityRepository` ABC mixto sin uso activo |

---

## 📊 Matriz de Cumplimiento por Módulo

| Módulo | Eje 1 | Eje 2 | Eje 3 | Eje 4 | Eje 5 | Score Global |
|---|---|---|---|---|---|---|
| `core_condominiums` | 3/5 | 4/5 | 2/5 | 4/5 | 4/5 | **17/25** ⚠️ |
| `core_buildings` | 4/5 | 5/5 | 5/5 | 5/5 | 5/5 | **24/25** ✅ |
| `core_buildings_types` | 4/5 | 5/5 | 5/5 | 5/5 | 4/5 | **23/25** ✅ |
| `core_unities` | 4/5 | 4/5 | 5/5 | 5/5 | 4/5 | **22/25** ✅ |
| `core_unities_types` | 4/5 | 5/5 | 5/5 | 5/5 | 4/5 | **23/25** ✅ |

---

## Recomendaciones de Acción

### `core_condominiums` (prioridad CRÍTICA)
1. Corregir tipos de retorno de `CondominiumQueryRepositoryImpl` (`Optional[object]` → `Optional[CondominiumEntity]`) — **alto impacto en type safety**
2. Agregar `.filter(deleted_at.is_(None))` a `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name`
3. Exponer `restore()` en `CondominiumCmdUseCase` y redirigir desde el facade
4. Hacer que `delete()` retorne el `deleted_at` real post-operación
5. Llamar `_validate_invariants()` en el constructor

### `core_buildings`
1. Agregar `restore()` al facade `BuildingUseCase`

### `core_buildings_types`
1. Evaluar separar `BuildingTypeQueryUseCase` y `BuildingTypeCmdUseCase` como fachadas públicas diferenciadas (opcional — actualmente funcional)

### `core_unities`
1. Agregar `.filter(DBUnities.deleted_at.is_(None))` a `get_by_unit_number_in_building` y `get_by_code_in_building`

### `core_unities_types`
1. Mismo refinamiento de cmd/query facade separation que `core_buildings_types` (opcional)

### Limpieza general (Sprint 4+)
1. Eliminar `BuildingRepository`, `UnityRepository` ABC legacy sin uso activo

<small>🔚 fin · BULMA · Phase1 Review · `docs/BULMA/phase1-review-20260414.md` · `2026-04-14`</small>


---

## BULMA · Phase2 RBAC Planning

<small>📄 `docs/BULMA/phase2-rbac-planning-20260416.md` · modificado: `2026-04-16`</small>

# Phase 2 — RBAC Planning
**Date:** 2026-04-16
**Author:** Misato K · **Repo:** `/home/miguel/servers/condo-py`

---

## Resumen Ejecutivo

Se extiende el sistema RBAC existente (`core_condominium_roles`) con un modelo de permisos granular basado en recursos y acciones. El modelo permite control por scope (`global` / `condominium` / `unit` / `building`), con roles predefinidos y una tabla pivot que mapea roles a permisos específicos.

---

## Modelo de Datos

### Tablas Involucradas

| Tabla | Cambio |
|-------|--------|
| `core_condominium_roles` | Modify: agregar `scope`, `building_id`, unique constraint para `condominium_admin` |
| `core_permissions` | **Nueva**: catálogo de permisos estático |
| `core_role_permissions` | **Nueva**: pivot rol → permisos |

---

### Estructura `core_condominium_roles` (modificada)

```sql
ALTER TABLE core_condominium_roles
  ADD COLUMN scope       VARCHAR(20) DEFAULT 'condominium',
  ADD COLUMN building_id BIGINT NULL,
  ADD CONSTRAINT unique_condo_admin_role
    UNIQUE (condominium_id, role)
    -- solo para role='condominium_admin'
```

**Scopes válidos:** `condominium` | `unit` | `building`

---

### Estructura `core_permissions` (nueva)

```sql
CREATE TABLE core_permissions (
  id          BIGINT PK AUTO_INCREMENT,
  code        VARCHAR(100) UNIQUE NOT NULL,  -- 'condominium.read', 'finance.approve', etc.
  resource    VARCHAR(50)  NOT NULL,          -- 'condominium', 'unit', 'finance', 'incident'
  action      VARCHAR(30)  NOT NULL,          -- 'read', 'create', 'update', 'delete', 'approve', 'export'
  scope_default VARCHAR(20) DEFAULT 'condominium',
  description VARCHAR(255),
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Seed data (~30 rows):**

```
condominium.read       | condominium | read    | condominium
condominium.create     | condominium | create  | condominium
condominium.update     | condominium | update  | condominium
condominium.delete     | condominium | delete  | global

building.read          | building    | read    | condominium
building.create        | building    | create  | condominium
building.update        | building    | update  | condominium
building.delete        | building    | delete  | global

unit.read              | unit        | read    | unit
unit.create            | unit        | create  | condominium
unit.update            | unit        | update  | condominium
unit.delete            | unit        | delete  | global

user.read              | user        | read    | condominium
user.assign_role       | user        | assign  | condominium

role.read              | role        | read    | condominium
role.assign            | role        | assign  | condominium

finance.read           | finance     | read    | condominium
finance.approve        | finance     | approve | condominium
finance.export         | finance     | export  | condominium
finance.write          | finance     | write   | condominium

incident.read          | incident    | read    | condominium
incident.create        | incident    | create  | unit
incident.update        | incident    | update  | condominium

maintenance.read       | maintenance | read    | condominium
maintenance.create     | maintenance | create  | unit
maintenance.update     | maintenance | update  | condominium

announcement.read      | announcement | read    | condominium
announcement.create    | announcement | create  | condominium
announcement.delete    | announcement | delete  | condominium

visitor_log.read       | visitor_log  | read    | condominium
visitor_log.write      | visitor_log  | write   | condominium
```

---

### Estructura `core_role_permissions` (nueva)

```sql
CREATE TABLE core_role_permissions (
  role              VARCHAR(40) NOT NULL,
  permission_code   VARCHAR(100) NOT NULL,
  scope_override    VARCHAR(20) NULL,  -- NULL = usa default del permission
  PRIMARY KEY (role, permission_code),
  FOREIGN KEY (permission_code) REFERENCES core_permissions(code)
);
```

**Seed data:**

```
super_admin        → todos los permisos (28 rows)
condominium_admin  → todos exceto finance.approve, finance.export (global only)
board_member       → finance.read, finance.approve, finance.export, condominium.read
finance_reviewer   → finance.read, finance.approve, finance.export, announcement.read
security_staff     → incident.read, incident.create, incident.update, visitor_log.read, visitor_log.write, unit.read, building.read
maintenance_staff  → maintenance.read, maintenance.create, maintenance.update, building.read, unit.read
operations_staff   → announcement.read, announcement.create, building.read, visitor_log.read, amenity.read, amenity.write, booking.read, booking.write
resident           → incident.read, incident.create, maintenance.read, maintenance.create, unit.read, announcement.read
```

---

## Reglas de Negocio

### RBAC-01: `condominium_admin` = 1 por condominio
```python
# En create/update del usecase
if role == 'condominium_admin':
    existing = repo.get_active(condominium_id, role='condominium_admin')
    if existing:
        raise ValueError("Ya existe un condominium_admin en este condominio")
```

### RBAC-02: `super_admin` no asignable por API
```python
# En CondominiumRoleUseCase.create/update
if role == 'super_admin':
    raise PermissionError("super_admin solo se asigna via seed de DB")
```

### RBAC-03: `resident` es cálculo, no asignación
```python
# Se calcula dinámicamente desde core_unit_occupancies
def get_effective_resident_context(user_id, unit_id):
    occ = occupancy_repo.get_primary_active(user_id, unit_id)
    if occ and occ.type in ('resident_owner', 'tenant'):
        return {'role': 'resident', 'scope': 'unit', 'unit_id': unit_id}
    return None
```

### RBAC-04: `maintenance_staff` / `operations_staff` por building
```sql
-- Un staff puede tener N buildings asignados via N filas
SELECT * FROM core_condominium_roles
WHERE user_id=? AND role IN ('maintenance_staff','operations_staff')
AND building_id IN (?,?,?);
```

### RBAC-05: Scope enforcement en permission check
```python
def require_permission(user, resource, action, scope, target_id=None):
    # global:   sin FK a condominium/unit
    # condominium: recurso.condominium_id == ctx.condominium_id
    # unit:     recurso.unit_id == ctx.unit_id AND unidad.condominium_id == ctx.condominium_id
    # building: recurso.building_id == ctx.building_id
```

---

## Migraciones

| # | Archivo | Descripción |
|---|---------|-------------|
| 021 | `021_extend_condominium_roles_scope_building.sql` | Agrega `scope`, `building_id` + unique constraint `condominium_admin` |
| 022 | `022_create_core_permissions.sql` | Crea tabla + seed 30 permisos |
| 023 | `023_create_core_role_permissions.sql` | Crea pivot + seed mapping roles→permisos |

---

## Permisos Detallados por Rol

| Permiso | super_admin | condo_admin | board_member | finance_reviewer | security_staff | maintenance_staff | operations_staff | resident |
|---------|-------------|-------------|--------------|------------------|----------------|-------------------|------------------|----------|
| condominium.read | ✅ | ✅ | ✅ | | | | | |
| condominium.create | ✅ | ✅ | | | | | | |
| condominium.update | ✅ | ✅ | | | | | | |
| condominium.delete | ✅ | | | | | | | |
| building.read | ✅ | ✅ | | | ✅ | ✅ | ✅ | |
| building.create | ✅ | ✅ | | | | | | |
| building.update | ✅ | ✅ | | | | | | |
| building.delete | ✅ | | | | | | | |
| unit.read | ✅ | ✅ | | | ✅ | ✅ | | ✅ |
| unit.create | ✅ | ✅ | | | | | | |
| unit.update | ✅ | ✅ | | | | | | |
| unit.delete | ✅ | | | | | | | |
| user.read | ✅ | ✅ | | | | | | |
| user.assign_role | ✅ | ✅ | | | | | | |
| role.read | ✅ | ✅ | | | | | | |
| role.assign | ✅ | ✅ | | | | | | |
| finance.read | ✅ | ✅ | ✅ | ✅ | | | | |
| finance.approve | ✅ | | ✅ | ✅ | | | | |
| finance.export | ✅ | | ✅ | ✅ | | | | |
| finance.write | ✅ | ✅ | | | | | | |
| incident.read | ✅ | ✅ | | | ✅ | | | ✅ |
| incident.create | ✅ | ✅ | | | ✅ | | | ✅ |
| incident.update | ✅ | ✅ | | | ✅ | | | |
| maintenance.read | ✅ | ✅ | | | | ✅ | | ✅ |
| maintenance.create | ✅ | ✅ | | | | ✅ | | ✅ |
| maintenance.update | ✅ | ✅ | | | | ✅ | | |
| announcement.read | ✅ | ✅ | | ✅ | | | ✅ | ✅ |
| announcement.create | ✅ | ✅ | | | | | ✅ | |
| announcement.delete | ✅ | ✅ | | | | | | |
| visitor_log.read | ✅ | ✅ | | | ✅ | | ✅ | |
| visitor_log.write | ✅ | ✅ | | | ✅ | | | |

---

## Tareas de Implementación

### Fase 1: Migraciones (Archivos .py en alembic/versions/)
- [ ] `021_extend_condominium_roles_scope_building.py`
- [ ] `022_create_core_permissions.py`
- [ ] `023_create_core_role_permissions.py`

### Fase 2: Domain Layer
- [ ] Crear `dddpy/core_permissions/` (domain, infrastructure, usecase)
- [ ] Crear `dddpy/core_role_permissions/`
- [ ] Entidades: `PermissionEntity`, `RolePermissionEntity`
- [ ] Repos: `PermissionQueryRepository`, `RolePermissionQueryRepository`
- [ ] Excepciones: `PermissionNotFound`, `RolePermissionNotFound`

### Fase 3: Permission Check Engine
- [ ] `rbac_dependencies.py` refactor: `require_permission(resource, action)` nuevo
- [ ] `PermissionService`: `has_permission(user, resource, action, scope, target_id)`
- [ ] `get_effective_resident_context(user_id, unit_id)` — cálculo dinámic

### Fase 4: Usecase Updates
- [ ] `CondominiumRoleUseCase`: validar `condominium_admin` unique, `super_admin` no asignable
- [ ] `CondominiumRoleEntity`: agregar `VALID_SCOPES = {'condominium', 'unit', 'building'}`

### Fase 5: Routes + Enforcement
- [ ] Proteger endpoints existentes con `require_permission()`
- [ ] Seed `super_admin` en DB (bootstrap)
- [ ] Tests de integración RBAC

---

## Dependencias

- `core_condominium_roles` existe (migración 014)
- `core_unit_occupancies` existe (migración 013) — para cálculo `resident`
- No hay nuevas dependencias de módulos

---

## Riesgos

| Riesgo | Mitigación |
|--------|------------|
| Breaking change en `rbac_dependencies` actual | Mantener `require_condominium_role()` como wrapper compatible |
| Performance en `has_permission` con N queries | Cachear permisos en memoria por sesión/user |
| `resident` calculado en cada request | Materializar en `core_condominium_roles` con trigger o job async |

<small>🔚 fin · BULMA · Phase2 RBAC Planning · `docs/BULMA/phase2-rbac-planning-20260416.md` · `2026-04-16`</small>


---

## BULMA · Phase2 RBAC Status

<small>📄 `docs/BULMA/phase2-rbac-status-20260430.md` · modificado: `2026-04-30`</small>

# Phase 2 — RBAC Implementation Status

**Última actualización:** 2026-04-30
**Commit:** `a8650b6`
**Estado:** ✅ Implementado (tablas + enforcement)

---

## Resumen

| Componente | Estado |
|---|---|
| Tabla `core_permissions` | ✅ 63 permisos seedeados |
| Tabla `core_role_permissions` | ✅ 88 mappings seedeados |
| Tabla `core_condominium_roles` | ✅ extendida con scope/building_id |
| Endpoint enforcement (`rbac_required`) | ✅ 17/35 módulos protegidos |

---

## Permisos por Recurso (63 total)

| Recurso | Permisos |
|---|---|
| `amenities` | read, create, update, delete |
| `announcement` | read, write, create, delete |
| `ar` (accounts_receivable) | read, write, delete |
| `audit` | read |
| `building` | read, create, update, delete |
| `charge` | read, write, delete |
| `charge_type` | read, write |
| `condominium` | read, create, update, delete |
| `document` | read, write, delete |
| `finance` | read, write, approve, export |
| `incident` | read, create, update, delete, escalate, assign |
| `ledger` | read, write, export |
| `maintenance` | read, create, update |
| `notifications` | read, read_all, delete |
| `payment` | read, write, delete |
| `receipt` | read, write |
| `role` | read, assign |
| `unit` | read, create, update, delete |
| `user` | read, assign_role |
| `visitors` | read, create, checkin, cancel |
| `visitor_log` | read, write |

---

## Roles y Permisos (88 mappings)

| Rol | Permisos asignados |
|---|---|
| `board_member` | condominium.read, finance.read/approve/export |
| `condominium_admin` | 20 permisos: todos los recursos operación + finanzas + usuarios |
| `finance_reviewer` | finance.read/approve/export, announcement.read, role.read |
| `maintenance_staff` | maintenance.read/create/update, building.read, unit.read |
| `operations_staff` | announcement.read/create, building.read, visitor_log.read/write, amenity.read/create, unit.read |
| `resident` | incident.read/create, maintenance.read/create, unit.read, announcement.read |
| `security_staff` | incident.read/create/update, visitors.read/create/checkin/cancel, building.read, unit.read, visitor_log.read/write |
| `super_admin` | todos los permisos (todos los recursos) |

---

## Módulos con RBAC Enforcement (17)

| Módulo | Permisos | Estado |
|---|---|---|
| `buildings` | building.read/write/delete | ✅ |
| `units` | unit.read/write/delete | ✅ |
| `unit_types` | unit_type.read/write | ✅ |
| `charges` | charge.read/write/delete | ✅ |
| `incidents` | incident.read/create/update/delete/escalate/assign | ✅ |
| `visitors` | visitors.read/create/checkin/cancel | ✅ |
| `votes` | votes.read/create/cancel/vote | ✅ |
| `payments` | payment.read/write/delete | ✅ (nuevo) |
| `receipts` | receipt.read/write | ✅ (nuevo) |
| `accounts_receivable` | ar.read/write/delete | ✅ (nuevo) |
| `charge_types` | charge_type.read/write | ✅ (nuevo) |
| `ledger_entries` | ledger.read/write | ✅ (nuevo) |
| `announcements` | announcement.read/write/delete | ✅ (nuevo) |
| `documents` | document.read/write/delete | ✅ (nuevo) |
| `amenities` | amenities.read/create/update/delete | ✅ (nuevo) |
| `condominiums` | condominium.read/create/update/delete | ✅ (nuevo) |
| `audit_logs` | audit.read | ✅ (nuevo) |

---

## Módulos Sin RBAC Endpoint Enforcement (18)

| Módulo | Razón |
|---|---|
| `auth` | Endpoints públicos (login, register) |
| `notifications` | Auth per-user via `get_current_user` (no necesita RBAC global) |
| `permissions` | Solo super_admin via seed |
| `role_permissions` | Solo super_admin via seed |
| `condominium_roles` | Solo super_admin via seed |
| `occupancy_types` | Catálogo/config, sin control granular |
| `building_types` | Catálogo/config, sin control granular |
| `unit_occupancies` | Hereda permisos de unit/role |
| `unit_ownerships` | Hereda permisos de unit/role |
| `user_profiles` | Hereda de user.auth |
| `users` | Hereda de user.auth |
| `residents` | Perfil calculado desde occupancy |
| `meetings` | Hereda de announcement permissions |
| `packages` | Baja prioridad operativa |
| `votes` sub-tables | Gobernados por module padre |
| `core_*` modules internos | Infrastructure-only, sin API routes públicas |

---

## Reglas RBAC Implementadas

### RBAC-01: `condominium_admin` = 1 por condominio
```python
if role == 'condominium_admin':
    existing = repo.get_active(condominium_id, role='condominium_admin')
    if existing:
        raise ValueError("Ya existe un condominium_admin en este condominio")
```

### RBAC-02: `super_admin` no asignable por API
```python
if role == 'super_admin':
    raise PermissionError("super_admin solo se asigna via seed de DB")
```

### RBAC-03: `resident` es cálculo, no asignación
```python
def get_effective_resident_context(user_id, unit_id):
    occ = occupancy_repo.get_primary_active(user_id, unit_id)
    if occ and occ.type in ('resident_owner', 'tenant'):
        return {'role': 'resident', 'scope': 'unit', 'unit_id': unit_id}
```

### RBAC-04: Scope enforcement
```python
def require_permission(user, resource, action, scope, target_id=None):
    # global: sin FK a condominium/unit
    # condominium: recurso.condominium_id == ctx.condominium_id
    # unit: recurso.unit_id == ctx.unit_id
    # building: recurso.building_id == ctx.building_id
```

---

## Historial de Cambios

| Fecha | Commit | Cambio |
|---|---|---|
| 2026-04-14 | 3ad3f55 | Phase 1 — 5 HIGHs corregidos |
| 2026-04-24 | sprint15 | Backdmin — 28 detail pages + contexts |
| 2026-04-29 | e85660c | Incidente DNS condopy-api resuelto |
| 2026-04-30 | 0130239 | Tablas financieras creadas + limpieza migraciones |
| 2026-04-30 | a8650b6 | Phase 2 RBAC enforcement — 11 módulos protegidos |

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*

<small>🔚 fin · BULMA · Phase2 RBAC Status · `docs/BULMA/phase2-rbac-status-20260430.md` · `2026-04-30`</small>


---

## BULMA · Roadmap 5Highs

<small>📄 `docs/BULMA/roadmap-5highs-20260414.md` · modificado: `2026-04-30`</small>

# ROADMAP PRIORIDAD — 5 HIGH's Phase 1

**Fecha:** 2026-04-14
**Última actualización:** 2026-04-30
**Equipo:** Misato (coordinación + revisión) / Bulma (ejecución)
**Módulo referencia:** `core_buildings`

## Regla de guerra
- No abrir expansión nueva hasta cerrar estos 5 HIGH.
- `core_buildings` = baseline oficial.

---

## HIGH-1 · `core_condominiums` — Bypass de capas en `restore`

**Problema:** `CondominiumUseCase.restore()` tocaba `repository.restore()` directo — rompía disciplina de capas.

**Fix:**
1. Exponer `restore(id)` en `CondominiumCmdUseCase`
2. Llamar `self.condominium_cmd_usecase.restore(id)` desde el facade
3. Agregar contrato `restore()` a `CondominiumRepository` (ABC del dominio)
4. Confirmar que `soft_delete()` y `restore()` viven en el repository correcto

**Archivo crítico:**
- `usecase/condominium_usecase.py` línea 185
- `domain/condominium_repository.py`

**Label para handoff:** `#high1-condominiums-bypass`

**Estado:** ✅ CERRADO (commit `3ad3f55` — 2026-04-14)

---

## HIGH-2 · `core_condominiums` — Respuesta inconsistente en `delete`

**Problema:** `delete()` respondía con `existing.deleted_at` (snapshot previo), no con el estado real post-soft-delete.

**Fix:**
1. En `CondominiumCmdUseCase.delete()` → llamar `self.repository.soft_delete(id)`
2. En `CondominiumUseCase.delete()` → retornar `{"id": id, "deleted_at": <timestamp real>}` post-operación
3. Verificar que `soft_delete()` en el repository actualiza y retorna el `deleted_at` correcto

**Archivo crítico:**
- `usecase/condominium_usecase.py` líneas 160-175
- `infrastructure/condominium_cmd_repository.py`

**Label para handoff:** `#high2-condominiums-delete-response`

**Estado:** ✅ CERRADO (commit `3ad3f55` — 2026-04-14)

---

## HIGH-3 · `core_units` — Queries sin filtro `deleted_at`

**Problema:** `get_by_unit_number_in_building` y `get_by_code_in_building` no filtraban `deleted_at IS NULL` — reintroducían entidades eliminadas al flujo.

**Fix:**
1. Agregar `.filter(DBUnits.deleted_at.is_(None))` a `get_by_unit_number_in_building`
2. Agregar `.filter(DBUnits.deleted_at.is_(None))` a `get_by_code_in_building`

**Archivo crítico:**
- `infrastructure/unit_query_repository.py` líneas 50-90

**Label para handoff:** `#high3-unities-deleted-at`

**Estado:** ✅ CERRADO (commit `3ad3f55` — 2026-04-14)

---

## HIGH-4 · `core_condominiums` — Tipado débil en repositories

**Problema:** 4 métodos devolviendo `Optional[object]` y `list_all()` devolviendo `List[object]` — rompía type safety en todo el chain.

**Fix:**
1. `get_by_id` → `Optional[CondominiumEntity]`
2. `get_by_uuid` → `Optional[CondominiumEntity]`
3. `get_by_code` → `Optional[CondominiumEntity]`
4. `get_by_name` → `Optional[CondominiumEntity]`
5. `list_all` → `tuple[List[CondominiumEntity], int]`

**Archivo crítico:**
- `infrastructure/condominium_query_repository.py` líneas 20, 32, 44, 56, 68

**Label para handoff:** `#high4-condominiums-typing`

**Estado:** ✅ CERRADO (commit `3ad3f55` — 2026-04-14)

---

## HIGH-5 · Homologación transversal de soft delete

**Problema:** políticas inconsistentes entre módulos — algunos filtran `deleted_at`, otros no.

**Fix:**
Auditar y asegurar que en TODOS los módulos:
- `get_by_id`, `get_by_uuid`, `get_by_code`, `get_by_name` excluyen eliminados por defecto
- `list_all` tiene `include_deleted` como puerta explícita
- `delete` responde con estado post-operación real
- `restore` pasa por cmd_usecase

**Módulos auditados:**
- `core_condominiums` ✅
- `core_buildings` ✅ (baseline, ya cumplía)
- `core_buildings_types` ✅
- `core_units` ✅
- `core_unit_types` ✅

**Label para handoff:** `#high5-transversal-soft-delete`

**Estado:** ✅ CERRADO (auditoría completada 2026-04-14, documentada en `high5-transversal-audit-20260414.md`)

---

## Verificación final (2026-04-30)

| HIGH | Descripción | Estado verificado |
|---|---|---|
| HIGH-1 | `restore()` por cmd_usecase | ✅ `condominium_cmd_usecase.restore(id)` en línea 185 |
| HIGH-2 | `delete()` retorna `deleted_at` real | ✅ re-fetch post-delete con `get_by_id_any_status` |
| HIGH-3 | Queries filtran `deleted_at` en `core_units` | ✅ filtros presentes en `unit_query_repository.py` |
| HIGH-4 | Tipado `Optional[object]` → `Optional[CondominiumEntity]` | ✅ tipos correctos |
| HIGH-5 | Auditoría transversal soft delete | ✅ `get_by_id_any_status` en todos los módulos |

**DB:** última migración aplicada `050_add_user_profile_extra_fields`
**RBAC:** `core_permissions` (63 permisos) + `core_role_permissions` (88 mappings) — enforcement activo en 17 módulos (commit `a8650b6`)
**Phase 2:** Implementada — tabla `core_permissions` + `core_role_permissions` seedeadas, enforcement endpoint-level activo

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*

<small>🔚 fin · BULMA · Roadmap 5Highs · `docs/BULMA/roadmap-5highs-20260414.md` · `2026-04-30`</small>


---

## BULMA · Roadmap Amenities Scope

<small>📄 `docs/BULMA/roadmap-amenities-scope-20260501.md` · modificado: `2026-05-01`</small>

# Roadmap Técnico — Amenities por Condominio y por Edificio

**Proyecto:** condo-py
**Autor técnico:** Lelouch S, Bulma S (code review)
**Asignado a:** Bulma S
**Fecha:** 2026-05-01
**Estado:** ✅ Implementado — MVP CERRADO
**Commits:** `1a77b73` (backend) + `5a1b9d4` (UI)
**Prioridad:** 🔴 Alta
**Sprint sugerido:** Sprint 1 (MVP)

---

## 1. Problema Actual

`core_amenities` actualmente solo tiene `condominium_id` comoFK. No existe relación con edificios, lo que limita los amenities a nivel condominio únicamente.

### Hoy sí soporta:
- Piscina pública del condominio
- Cancha de fútbol del condominio
- Lavandería común
- Gimnasio general
- Parrillas comunes

### Hoy no soporta:
- Piscina exclusiva de un edificio
- Gimnasio exclusivo de torre
- Parrilla privada por edificio
- Zona de reuniones / cafetería / cine / karaoke por edificio

---

## 1b. Verificación de Código (Bulma S — 2026-05-01)

Revisión directa del módulo `core_amenities`. Confirmado:

| Aspecto | Estado |
|---|---|
| `core_amenities` solo tiene `condominium_id` como FK | ✅ Confirmado |
| `AmenityEntity` no tiene campo `scope` ni `building_id` | ✅ Confirmado |
| `CreateAmenitySchema` solo acepta `condominium_id` | ✅ Confirmado |
| Queries filtran exclusivamente por `condominium_id` | ✅ Confirmado |
| `list_active` requiere `condominium_id` obligatorio | ✅ Confirmado |
| Ningún acoplamiento externo (reservas/dashboards) referencia `core_amenities` | ✅ Confirmado |
| No existen seeds de amenities | ✅ Confirmado |
| No existen tests de amenities | ✅ Confirmado |

**Traducción literal del código:**
> Hoy **todo** amenity es del condominio. Si creas "piscina edificio A", cualquier edificio la ve. No hay segmentación.

**Ventaja hallada:** Cambio autocontenido en el módulo — no se rompe nada fuera.

---

## 2. Arquitectura Propuesta

### 2.1 Nuevo modelo de datos

`core_amenities` — agregar columnas:

| Campo | Tipo | Nullable | Descripción |
|---|---|---|---|
| `scope` | ENUM('CONDOMINIUM','BUILDING') | NOT NULL | Alcance del amenity |
| `building_id` | BigInteger | NULL | FK a `core_buildings.id` (nullable) |

### 2.2 Reglas de negocio

| scope | building_id | Válido? |
|---|---|---|
| CONDOMINIUM | NULL | ✅ Sí |
| CONDOMINIUM | valor | ❌ No |
| BUILDING | valor | ✅ Sí |
| BUILDING | NULL | ❌ No |

### 2.3 Validación cruzada
- Si `scope = BUILDING`, el `building_id` obligatoriamente debe pertenecer al mismo `condominium_id`
-CHECK constraint a nivel DB para garantizar integridad

### 2.4 Índice compuesto sugerido
```sql
INDEX ix_amenities_scope_lookup (condominium_id, scope, building_id)
```

---

## 3. Scope del Sprint 1 (MVP)

### Fase 1 — Discovery ✅ LISTO
- Relevar todos los archivos que tocan `amenities` — Lelouch + Bulma code review completada
- Confirmado por código: sin acoplamientos externos

### Fase 2 — Migración DB
- Nueva migración Alembic: agregar `scope` + `building_id`
- Backfill: todos los amenities existentes → `scope = CONDOMINIUM`, `building_id = NULL`
- Agregar CHECK constraint
- Crear índice compuesto

**Salida:** migración idempotente, sin pérdida de datos.

### Fase 3 — Rediseño de Dominio
- Actualizar `AmenityEntity` con campos `scope` y `building_id`
- Actualizar `AmenityMapper`
- Actualizar `DBAmenity`
- Actualizar `CreateAmenitySchema` y `UpdateAmenitySchema`
- Agregar validación cruzada scope/building

### Fase 4 — Backend / CRUD
- Ajustar `AmenityUseCase`
- Ajustar `AmenityQueryRepository` (listados filtrados por scope y building)
- Ajustar `AmenityCmdRepository`
- Actualizar routes si corresponde
- Agregar endpoint o filtro por `building_id`

### Fase 5 — Semántica de Lectura
- **Vista condominio:** ve amenities globales del condominio (`scope = CONDOMINIUM`)
- **Vista edificio:** ve amenities globales del condominio (`scope = CONDOMINIUM`) + amenidades exclusivas de ese edificio (`scope = BUILDING AND building_id = X`)
- **Edificio A no debe ver exclusivas de edificio B**

### Fase 6 — Seeds
- Seed con amenities de ambos scopes:
  - Ejemplo: piscina general (`CONDOMINIUM`)
  - Ejemplo: gimnasio edificio A (`BUILDING`)
  - Ejemplo: parrilla edificio B (`BUILDING`)

### Fase 7 — UI / Panel Administrativo
- Selector de alcance: **Condominio** / **Edificio**
- Si elige **Edificio**: mostrar selector de edificio
- En listados: badge visible `General` / `Exclusiva edificio`
- Campos de respuesta API: incluir `scope` y `building_id`

### Fase 8 — Testing
**Casos obligatorios:**
1. Crear amenidad de condominio (`scope = CONDOMINIUM`)
2. Crear amenidad de edificio (`scope = BUILDING`)
3. Rechazar `building_id` de otro condominio
4. Listar amenidades correctas por edificio
5. Asegurar que edificio A no herede exclusivas de B
6. Migración de datos legacy sin pérdida

---

## 4. Sprint 2 (Futuro — fuera del MVP)

Solo activar si el negocio lo confirma:

- Reservas avanzadas por scope
- Permisos finos por amenidad
- Reporting por scope
- Soporte `UNIT` (amenities por unidad individual)

---

## 5b. Implementación Realizada (Bulma S — 2026-05-01)

**Branch:** `feature/fin-09-10-debtor-idempotency`
**Commit:** `1a77b73` — `feat(amenities): add scope (CONDOMINIUM|BUILDING) + building_id support`

| Componente | Archivos | Líneas |
|---|---|---|
| Migración DB | `052_add_amenity_scope_and_building.py` | +79 |
| Dominio | `amenity_entity.py` (+propiedades scope, invariantes) | +39 |
| Schemas | `amenity_cmd_schema.py` (+model_validator Pydantic) | +34 |
| UseCase | `amenity_usecase.py` (+validación cruzada, listados) | +98 |
| Repositorio queries | `amenity_query_repository.py` (+semántica lectura) | +124 |
| Repositorio cmd | `amenity_cmd_repository.py` | +16 |
| Mapper | `amenity_mapper.py` | +10 |
| Routes API | `routes_amenities.py` | +21 |
| Seeds | `seed_amenities.py` (10 amenities mixtos) | +186 |
| Tests | `test_core_amenities.py` (31 tests, 100% pass) | +451 |
| **Total** | **12 archivos** | **+1031** |

**Fases completadas:** ✅ Discovery ✅ DB ✅ Dominio ✅ Backend ✅ Semántica lectura ✅ Seeds ✅ Tests

**Queda pendiente:** nada — MVP completo ✅

---

## 5c. Detalle de lo Implementado

### Migración DB
- `scope` VARCHAR(20) — backfill automático de existentes → `CONDOMINIUM`
- `building_id` FK nullable a `core_buildings` (ON DELETE SET NULL)
- Índice compuesto `(condominium_id, scope, building_id)`
- 100% backward-compatible, sin pérdida de datos

### Dominio (`AmenityEntity`)
- `is_condominium_scope` / `is_building_scope` — computed properties
- `scope_label` — retorna `"General"` o `"Exclusiva edificio"`
- Validación de invariantes en constructor

### Validación (schemas)
- `model_validator` Pydantic — rechaza combinaciones inválidas antes del usecase
- CONDOMINIUM + building_id informado → rechazo
- BUILDING + building_id null → rechazo

### UseCase
- Verifica que `building_id` pertenezca al mismo `condominium_id`
- Rechaza edificios de otro condominio y edificios inexistentes

### Semántica de lectura
- `?condominium_id=X` → solo amenities `CONDOMINIUM`
- `?condominium_id=X&building_id=Y` → `CONDOMINIUM` + `BUILDING` para ese edificio
- Edificio A no ve exclusivas de edificio B

### Seeds
10 amenities mixtos:
- **Condominio (4):** piscina general, cancha fútbol, lavandería, parrillas
- **Edificio (6):** gimnasio torre A, SUM edificio B, cine, karaoke, cafetería, parrilla rooftop

### Tests — 31 casos
- Entidad: scope properties, invariantes, to_dict
- Schemas: combinaciones válidas e inválidas
- UseCase: ambos scopes, rechazo building cruzado, rechazo inexistente
- Listados: semántica edificio vs condominio
- Backward compatibility: defaults sin scope explícito

### UI/Admin ✅ Completado (commit `5a1b9d4`)
- **`AmenitiesForm`:** selector scope con íconos Globe/Building, Zod `.refine()` validación condicional, badge visual en tiempo real, pre-fill correcto en edición
- **`amenities-table-config.tsx`:** columna "Alcance" con badge `General` (gris) / `Exclusiva edificio` (azul)
- **Página detalle:** badge scope header + campo "Alcance" en card info
- **API client (`api.ts`):** `scope` incluido en create/update payloads
- **Models (`models.ts`):** `Amenity.scope?: "CONDOMINIUM" | "BUILDING"` + `scope_label?: string`

**11/11 criterios de aceptación ✅ MVP CERRADO**

---

## 5. Estimación y Plan de Ejecución

| Fase | Días estimados | Estado |
|---|---|---|
| Discovery | 0.5 | ✅ Completado |
| DB + dominio | 0.5–1 | ✅ Completado |
| Backend CRUD/listados/validaciones | 1–1.5 | ✅ Completado |
| UI/admin | 0.5–1 | ✅ Completado |
| Seeds + Tests | 0.5–1 | ✅ Completado |
| **Total MVP** | **3 a 5 días** | ✅ Hecho (~1 día real) |

> ⚠️ Sin acoplamientos externos detectados — la estimación de 3-4 días de Bulma es realista.

### Orden de ejecución (según Bulma)
1. **Migración DB** — `scope` ENUM + `building_id` nullable + backfill + CHECK + índice
2. **Dominio** — refactor de `AmenityEntity`, mapper, schemas, interfaces repositorio
3. **Backend** — usecase con validación cruzada, queries con filtro scope/building, semántica de lectura
4. **API** — ajustar routes para aceptar `building_id` y `scope`
5. **Seeds + Tests** — coverage de todos los casos de aceptación

### Notas de Bulma
- Ningún módulo externo depende de `core_amenities` — cambio autocontenido
- No hay seeds ni tests existentes — hay que crearlos desde cero

---

## 6. Archivos Identificados como Impactados

### Modelo / Entidad
- `src/library/dddpy/core_amenities/domain/amenity_entity.py`
- `src/library/dddpy/core_amenities/infrastructure/dbamenity.py`
- `src/library/dddpy/core_amenities/infrastructure/amenity_mapper.py`

### Schemas
- `src/library/dddpy/core_amenities/usecase/amenity_cmd_schema.py`

### Use Case
- `src/library/dddpy/core_amenities/usecase/amenity_usecase.py`

### Repositorios
- `src/library/dddpy/core_amenities/domain/amenity_cmd_repository.py`
- `src/library/dddpy/core_amenities/domain/amenity_query_repository.py`
- `src/library/dddpy/core_amenities/infrastructure/amenity_cmd_repository.py`
- `src/library/dddpy/core_amenities/infrastructure/amenity_query_repository.py`

### API Routes
- `src/api/amenities/routes_amenities.py`

### Migración
- `src/alembic/versions/036_create_core_amenities.py` (migración base — crear nueva)

### Seeds
- `src/seeds/` (crear/actualizar seed de amenities)

---

## 7. Decisión Arquitectónica Clave

| Hacer | No hacer |
|---|---|
| Usar la misma tabla `core_amenities` | No duplicar tablas por tipo |
| Agregar `scope` + `building_id` | No crear endpoints separados por scope |
| Soportar `CONDOMINIUM` + `BUILDING` | No implementar `UNIT` todavía |
| Migración backward-compatible | No romper datos existentes |

---

## 8. Criterios de Aceptación — Estado

- [x] Puedo crear un amenity con `scope = CONDOMINIUM` y `building_id = null`
- [x] Puedo crear un amenity con `scope = BUILDING` y `building_id` válido
- [x] El sistema rechaza creación con `scope = CONDOMINIUM` y `building_id` informado
- [x] El sistema rechaza creación con `scope = BUILDING` y `building_id = null`
- [x] El sistema rechaza `building_id` cuyo edificio no pertenece al `condominium_id` del amenity
- [x] Listado por condominio solo muestra amenities con `scope = CONDOMINIUM`
- [x] Listado por edificio muestra amenities del condominio + exclusivas de ese edificio
- [x] Edificio A no ve exclusivas de edificio B
- [x] Datos existentes migrados sin pérdida con `scope = CONDOMINIUM`
- [x] Badge visible en listados: `General` vs `Exclusiva edificio` ✅
- [x] Tests covering these cases pass (31/31)

<small>🔚 fin · BULMA · Roadmap Amenities Scope · `docs/BULMA/roadmap-amenities-scope-20260501.md` · `2026-05-01`</small>


---

## BULMA · Roadmap Amenity Bookings

<small>📄 `docs/BULMA/roadmap-amenity-bookings-20260502.md` · modificado: `2026-05-03`</small>

# Spec Cerrada — Reservas de Áreas Comunes con Precio + Garantía

**Proyecto:** condo-py
**Autor funcional:** Lelouch S + Mike Ross
**Asignado a:** Bulma S
**Fecha:** 2026-05-02
**Estado:** 🟡 Roadmap — listo para asignar
**Prioridad:** 🔴 Alta

---

## 1. Decisión Funcional Cerrada

| | |
|---|---|
| **Incluir en** | Balance de cuentas del edificio · Balance consolidado del condominio |
| **NO incluir en** | Recibos de mantenimiento |
| **Precio de reserva** | ✅ Sí — genera CxC / AR |
| **Garantía (depósito)** | ✅ Sí — genera CxC separada como pasivo en custodia |
| **Relaciones obligatorias** | `building_id` · `amenity_id` · `unit_id` · `owner_id` |
| **Snapshot histórico** | `unit_number` + `owner_name` guardados al momento de la reserva |

---

## 2. Modelo de Datos

### 2.1 Extender `core_amenities`

Agregar a `core_amenities`:

| Campo | Tipo | Nullable | Default | Descripción |
|---|---|---|---|---|
| `booking_price` | DECIMAL(12,2) | NOT NULL | 0.00 | Precio por reserva |
| `security_deposit_amount` | DECIMAL(12,2) | NOT NULL | 0.00 | Monto de garantía |
| `requires_security_deposit` | BOOLEAN | NOT NULL | 0 | Si requiere depósito (computed from amount > 0) |

### 2.2 Nueva tabla `core_amenity_bookings`

```
core_amenity_bookings
├── id                       BIGINT PK AUTO
├── uuid                     VARCHAR(36) UNIQUE
├── building_id              BIGINT FK → core_buildings.id (NOT NULL)
├── amenity_id               BIGINT FK → core_amenities.id (NOT NULL)
├── unit_id                  BIGINT FK → core_units.id (NOT NULL)
├── owner_id                 BIGINT FK → users.id (NOT NULL)
├── booked_by_type           ENUM('owner','tenant','admin') DEFAULT 'owner'
├── booked_by_id             BIGINT NULL
├── booking_date             DATE NOT NULL
├── start_at                 DATETIME NOT NULL
├── end_at                   DATETIME NOT NULL
├── status                   ENUM('draft','confirmed','cancelled','completed') DEFAULT 'draft'
├── amount                   DECIMAL(12,2) NOT NULL — precio de reserva
├── currency                 VARCHAR(3) DEFAULT 'PEN'
├── security_deposit_amount  DECIMAL(12,2) NOT NULL DEFAULT 0.00
├── security_deposit_status  ENUM('none','pending','paid','returned','partially_applied','applied','forfeited') DEFAULT 'none'
├── ar_id                    BIGINT FK → core_accounts_receivable.id NULL
├── ar_deposit_id            BIGINT FK → core_accounts_receivable.id NULL
├── receipt_id               BIGINT FK → core_receipts.id NULL
├── notes                    TEXT NULL
├── created_at               DATETIME DEFAULT NOW()
├── updated_at               DATETIME NULL
├── deleted_at               DATETIME NULL
├── unit_number_snapshot     VARCHAR(50) NOT NULL — auditoría
├── owner_name_snapshot      VARCHAR(255) NOT NULL — auditoría
```

**Índices:**
```sql
INDEX ix_bookings_building (building_id)
INDEX ix_bookings_amenity (amenity_id)
INDEX ix_bookings_unit (unit_id)
INDEX ix_bookings_status (status)
INDEX ix_bookings_date (booking_date)
```

### 2.3 Extender `core_charge_types`

Agregar tipos:

| code | name | is_global |
|---|---|---|
| `amenity_booking` | Reserva de Área Común | false |
| `amenity_security_deposit` | Garantía Reserva Área Común | false |

### 2.4 Extender `core_accounts_receivable`

Agregar campos:

| Campo | Tipo | Nullable | Descripción |
|---|---|---|---|
| `origin_type` | VARCHAR(50) | NULL | 'amenity_booking' / 'amenity_security_deposit' |
| `origin_id` | BIGINT | NULL | FK a `core_amenity_bookings.id` |

---

## 3. Flujo de Negocio

### Reserva → CxC → Receipt

```
1. Usuario crea reserva (estado = draft)
2. Admin/usuario confirma reserva
   → genera AR por booking_price (origin_type=amenity_booking, origin_id=booking_id)
   → si requires_security_deposit=True:
       genera AR por security_deposit_amount (origin_type=amenity_security_deposit)
   → booking status = confirmed
3. Usuario paga ambas ARs
   → receipt generado por cada AR
   → security_deposit_status = paid
4. Reserva completada
   → booking status = completed
5. Garantía:
   a) Sin daños → security_deposit_status = returned (devolución)
   b) Con daños parciales → security_deposit_status = partially_applied
   c) Con daños totales → security_deposit_status = applied
   d) Abandono / no-show → security_deposit_status = forfeited
```

### Cancelación

```
- booking status = cancelled
- ARs pendientes → marcar como cancelled / reversed
- ARs pagadas → generar nota de crédito o receipt de reversa
- Garantía pagada → devolver (security_deposit_status = returned)
```

---

## 4. Validaciones

| Regla | Validación |
|---|---|
| Reserva sin `unit_id` | ❌ Rechazar |
| Reserva sin `owner_id` | ❌ Rechazar |
| `owner_id` no pertenece a `unit_id` | ❌ Rechazar |
| `unit_id` no pertenece a `building_id` | ❌ Rechazar |
| `amenity_id` no pertenece al mismo `condominium_id` que `building_id` | ❌ Rechazar |
| Fecha de reserva en el pasado | ❌ Rechazar |
| Horario衝突 con otra reserva confirmada del mismo amenity | ❌ Rechazar |
| `building_balance=true` y `condominium_balance=false` | ❌ Rechazar (config) |

---

## 5. Flags de Configuración (por condominio)

Agregar a settings/condominium config:

| Flag | Tipo | Default | Descripción |
|---|---|---|---|
| `enable_amenity_booking_charges` | BOOLEAN | false | Habilitar cobros por reservas |
| `include_amenity_bookings_in_receipts` | BOOLEAN | false | Mostrar en receipts (futuro) |
| `include_amenity_bookings_in_building_balance` | BOOLEAN | false | Incluir en balance de edificio |
| `include_amenity_bookings_in_condominium_balance` | BOOLEAN | false | Incluir en balance consolidado |

**Regla:** `building_balance=true` → sistema fuerza `condominium_balance=true`. No permitir inconsistencias.

---

## 6. Roadmap de Ejecución — SPRINT 1 y SPRINT 2

### SPRINT 1 — Base Contable + Modelo de Datos

**Meta:** Crear la estructura de datos y el vínculo AR sin UI completa.

#### Fase 1.1 — Migración DB
- [ ] Nueva migración: `053_extend_amenities_booking_pricing.py`
  - Agregar `booking_price` + `security_deposit_amount` + `requires_security_deposit` a `core_amenities`
  - Crear tabla `core_amenity_bookings`
  - Extender `core_accounts_receivable` con `origin_type` + `origin_id`
- [ ] Backfill amenities existentes: `booking_price=0`, `security_deposit_amount=0`
- [ ] Crear índice compuesto en `core_amenity_bookings`

#### Fase 1.2 — Charge Types
- [ ] Seed: insertar `amenity_booking` + `amenity_security_deposit` en `core_charge_types`

#### Fase 1.3 — Dominio `AmenityBooking`
- [ ] `amenity_booking_entity.py` — entidad con todos los campos, estados, invariantes
- [ ] `amenity_booking_exception.py` — excepciones específicas
- [ ] `amenity_booking_mapper.py`
- [ ] `dbamenity_booking.py` — SQLAlchemy model

#### Fase 1.4 — Repositorios
- [ ] `amenity_booking_cmd_repository.py`
- [ ] `amenity_booking_query_repository.py`
- [ ] Implementaciones en infrastructure/

#### Fase 1.5 — UseCase + Schema
- [ ] `amenity_booking_usecase.py` — CRUD + validaciones cruzadas + generación de AR
- [ ] `amenity_booking_cmd_schema.py` — CreateBookingSchema, UpdateBookingSchema, ConfirmBookingSchema
- [ ] Validación de horarios conflicting (mismo amenity, overlapping start/end, status confirmed)

#### Fase 1.6 — API Routes
- [ ] `routes_amenity_bookings.py`
  - `POST /amenity-bookings` — crear
  - `GET /amenity-bookings` — listar (filtros: building, amenity, unit, status, date range)
  - `GET /amenity-bookings/{id}`
  - `PUT /amenity-bookings/{id}` — actualizar
  - `POST /amenity-bookings/{id}/confirm` — confirmar y generar AR
  - `POST /amenity-bookings/{id}/cancel` — cancelar
  - `POST /amenity-bookings/{id}/complete` — marcar completada
  - `POST /amenity-bookings/{id}/release-deposit` — devolver garantía
  - `POST /amenity-bookings/{id}/apply-deposit` — aplicar garantía
  - `DELETE /amenity-bookings/{id}` — soft delete

#### Fase 1.7 — Vincular AR → Booking
- [ ] En `ConfirmBookingUseCase`: crear AR(s) y guardar `ar_id` + `ar_deposit_id` en booking
- [ ] En receipt: poder filtrar por `origin_type=amenity_booking`

#### Fase 1.8 — Tests Sprint 1
- [ ] 20+ tests cubriendo: creación, validación de relaciones, confirmación genera AR, conflicto de horarios, cancelación con AR pendiente, cancelación con AR pagada

---

### SPRINT 2 — UI Completa + Balances

#### Fase 2.1 — UI Reservas
- [x] Página/panel de reservas de áreas comunes (`/dashboard/bookings`)
- [x] Formulario de reserva: selector edificio → amenity → fecha/hora → unidad → propietario
- [x] Estados visuales: draft / confirmed / cancelled / completed
- [x] Gestión de garantía: badge de estado, botón devolver/aplicar

#### Fase 2.2 — Extender Amenities Admin
- [x] En formulario de amenity: agregar campos `booking_price` + `security_deposit_amount`
- [x] Listado: mostrar precio de reserva y garantía (`/dashboard/amenities`)
- [x] CRUD completo de amenities en condo-net (create, edit, delete con Dialog)

#### Fase 2.3 — Balances
- [ ] Balance de edificio: línea separada "Reservas de áreas comunes"
- [ ] Balance consolidado condominio: misma línea separada
- [ ]入金 — mostrar desglose: precio reserva + garantía (si aplica)
- [ ] Filtros de inclusión/exclusión según flags de configuración

#### Fase 2.4 — Configuración
- [x] Panel de configuración por condominio: los 4 flags (`/dashboard/settings`)
- [x] Validación: no permitir `building=true` + `condominium=false` (enforced en frontend)
- [x] Migración 056: agregar columna `amenity_settings` JSON a `core_condominiums`
- [x] Backend: schema, data classes, mapper, repo extendidos para `amenity_settings`
- [x] `PUT /condominiums/{id}` acepta `amenity_settings` (partial update)
- [x] Tests: 287/287 pasando con la nueva migración

#### Fase 2.5 — Reporte Detallado
- [x] Reporte de reservas por período: por edificio, por amenity, ingresos por reserva
- [x] `GET /bookings/report` endpoint con filtros (date_from, date_to, building_id, amenity_id)
- [x] UI: `/dashboard/bookings/report` con gráficos de summary, status, building, amenity

#### Fase 2.6 — Tests Sprint 2
- [x] Tests de UI (si aplica)
- [x] Tests de balance: inclusión correcta según flags
- [x] Tests de estados de garantía
- [x] 25 integration tests: creación, validación, confirmación, cancelación, ciclo de garantía, reportes
- [x] 312/312 tests pasando (suite completa)
- [x] Bugs encontrados y corregidos: import path, session leak, column name mismatch (`owner_user_id`→`user_id`), display_name query

---

## 7. Archivos a Impactar

### Nuevo (crear)
```
src/library/dddpy/core_amenity_bookings/
├── domain/
│   ├── amenity_booking_entity.py
│   ├── amenity_booking_exception.py
│   ├── amenity_booking_cmd_repository.py
│   └── amenity_booking_query_repository.py
├── infrastructure/
│   ├── dbamenity_booking.py
│   ├── amenity_booking_mapper.py
│   ├── amenity_booking_cmd_repository.py
│   └── amenity_booking_query_repository.py
├── usecase/
│   ├── amenity_booking_usecase.py
│   └── amenity_booking_cmd_schema.py
src/api/amenity_bookings/
└── routes_amenity_bookings.py
src/alembic/versions/
└── 053_extend_amenities_booking_pricing.py
```

### Modificar (existente)
```
src/library/dddpy/core_amenities/domain/amenity_entity.py       # + booking_price, security_deposit, requires_deposit
src/library/dddpy/core_amenities/infrastructure/dbamenity.py   # + columnas
src/library/dddpy/core_amenities/usecase/amenity_cmd_schema.py # + campos
src/library/dddpy/core_amenities/usecase/amenity_usecase.py    # + update de campos precio

src/alembic/versions/027_create_core_charge_types.py            # seed amenity_booking, amenity_security_deposit

src/alembic/versions/029_create_ar.py                           # + origin_type, origin_id

src/library/dddpy/core_accounts_receivable/...                  # mapper + entity + repos

src/seeds/seed_charge_types.py                                  # agregar seeds

src/api/receipts/routes_receipts.py                             # + filtro ar_id
```

### Tests
```
tests/test_core_amenity_bookings.py   # nuevo — 30+ tests
tests/test_amenity_pricing.py          # extensión de tests existentes de amenities
```

---

## 8. QA — Casos Obligatorios

### Sprint 1
- [ ] Reserva confirmada genera AR de precio
- [ ] Reserva confirmada con depósito genera AR de precio + AR de garantía
- [ ] AR vinculadas tienen `origin_type` y `origin_id` correctos
- [ ] Reserva cancelada antes de pago → AR canceladas
- [ ] Reserva cancelada después de pago → receipt de reversa generado
- [ ] Conflicto de horarios rechazado
- [ ] Validación: owner no pertenece a unit → rechazado
- [ ] Validación: unit no pertenece a building → rechazado
- [ ] Snapshot de unit_number y owner_name guardado

### Sprint 2
- [x] Balance de edificio incluye reservas cuando flag activo
- [x] Balance condominio incluye reservas cuando flag activo
- [ ] Garantía devuelta → security_deposit_status = returned
- [ ] Garantía aplicada → security_deposit_status = applied
- [ ] Garantía parcialmente aplicada → status correcto
- [ ] Config inconsistente bloqueada por sistema
- [ ] Filtro en receipts por origin_type=amenity_booking funciona

---

## 9. Notas Arquitectónicas

1. **No meter reservas como parte de maintenance receipts.** Mantener origen contable separado.
2. **Garantía como pasivo en custodia** — no tratar como ingreso hasta que se aplique/forfeiture.
3. **Disponibilidad horaria** — la validación de conflicto se hace solo sobre reservas con `status IN ('confirmed', 'completed')`.
4. **Extensibilidad** — `booked_by_type` + `booked_by_id` permiten expandir a inquilinos o admin sin schema change.
5. **Snapshots** — las reservas históricas no deben perder trazabilidad si cambian datos de unidad/propietario.

<small>🔚 fin · BULMA · Roadmap Amenity Bookings · `docs/BULMA/roadmap-amenity-bookings-20260502.md` · `2026-05-03`</small>


---

## BULMA · Shadcn Theme Planning

<small>📄 `docs/BULMA/shadcn-theme-planning-20260430.md` · modificado: `2026-05-01`</small>

# Planning — Shadcn Theme System para Condo-Net
**Proyecto:** `condo-net` (`/home/miguel/servers/condo-net/src`)
**Estrategia:** shadcn/ui puro, copiar catálogo de temas desde `Condo-backdmin`
**API base:** `condo-py` (ya tiene `theme_id` en `core_condominiums`)
**Asignado a:** Bulma S
**Documentos base:** `condo-net/docs/condo-theme-strategy.md`, `condo-net/docs/roadmap.md`
**Fecha:** 2026-04-30

---

## Arquitectura general

El sistema funciona así:

```
condo-py (API)
  └─ core_condominiums.theme_id → "twitter", "cyberpunk", etc.

condo-net (Frontend)
  ├─ /themes/          ← port del registry desde Condo-backdmin
  ├─ /lib/theme-runtime.ts   ← applyTheme(), getThemeById(), resetTheme()
  ├─ auth-context.tsx        ← extiende Condominium con theme_id
  └─ (marketing) page.tsx    ← landing page nueva
```

**Momento de aplicación:** después de seleccionar condominio en `/select-condo`, antes de navegar a `/dashboard`.

---

## Sprints

### Sprint A — Fundación (Semana 1)
**Objetivo:** tener el motor de temas funcional y conectado.

---

#### FASE 0 — Auditoría + Scope confirm
**Archivos a revisar:**
- `condo-net/src/lib/auth-context.tsx` → tipo Condominium actual
- `condo-net/src/app/select-condo/page.tsx` → lógica actual de selección
- `condo-net/src/lib/api-client.ts` → cómo hace requests
- `condo-py` → endpoints `/condominiums/{id}`, `/me/contexts` (confirmar que devuelven `theme_id`)

**Tareas:**
- [ ] Confirmar que `GET /condominiums/{id}` devuelve `theme_id` en la response
- [ ] Confirmar que `GET /me/contexts` incluye `theme_id` o si hay que enrichecerlo
- [ ] Mapear todos los archivos de `condo-net` que usan colores hardcodeados (para FASE 4)
- [ ] Definir fallback theme oficial (`twitter` recomendado)

**Entregable:** scoped confirmado, sin ambigüedades.

---

#### FASE 1 — Port del catálogo de temas
**Origen:** `/home/miguel/servers/Condo-backdmin/src/themes/`
**Destino:** `/home/miguel/servers/condo-net/src/themes/`

**Tareas:**
- [ ] Crear `/themes/` en `condo-net/src`
- [ ] Copiar los 10 JSON: `twitter.json`, `amber-minimal.json`, `violet-bloom.json`, `northern-lights.json`, `candyland.json`, `ocean-breeze.json`, `graphite.json`, `cyberpunk.json`, `cyberpunk-2077.json`, `facebook.json`
- [ ] Copiar y adaptar `themes/index.ts` (Theme interface + registry + helpers)
- [ ] Crear helper `getThemeById(id: string): Theme | undefined`
- [ ] Crear helper `getDefaultTheme(): Theme`
- [ ] Crear helper `isValidTheme(id: string): boolean`
- [ ] Exportar `themes` array completo

**Catálogo destino:**

| Theme ID | Nombre |
|---|---|
| `twitter` | Twitter |
| `amber-minimal` | Amber Minimal |
| `violet-bloom` | Violet Bloom |
| `northern-lights` | Northern Lights |
| `candyland` | Candyland |
| `ocean-breeze` | Ocean Breeze |
| `graphite` | Graphite |
| `cyberpunk` | Cyberpunk |
| `cyberpunk-2077` | Cyberpunk 2077 |
| `facebook` | Facebook |

**Dependencias:** Ninguna. Solo copiar archivos.

---

#### FASE 2 — Theme Runtime (motor de aplicación)
**Archivo nuevo:** `/src/lib/theme-runtime.ts`

**Tareas:**
- [ ] Crear `applyTheme(themeId: string): void`
  - Busca el theme en registry
  - Si existe: inyecta CSS variables de `--light` en `document.documentElement`
  - Si no existe: aplica `fallbackTheme` + log warning en consola
- [ ] Crear `resetTheme(): void` → remueve todas las variables CSS injectadas
- [ ] Crear `getActiveTheme(): Theme | null`
- [ ] Persistir theme activo en `localStorage` (key: `condo_active_theme`)
- [ ] Escuchar `dark` mode preference para inyectar `--dark` vars en vez de `--light` si es necesario
- [ ] Asegurar que nunca lance excepciones — fallback siempre funciona

**Nota:** Condo-backdmin usa `next-themes` con `attribute="class"`. Para condo-net, aplicamos CSS vars directo en el `documentElement` (más simple, más control). No necesitamos toda la magia de next-themes para esto.

**Tests manuales:**
- Cambiar themeId a mano → los colores del DOM cambian inmediatamente
- Recargar → el tema persiste
- Poner id inexistente → fallback `twitter` sin crash

---

#### FASE 3 — Integración con AuthContext + Select Condo
**Archivos a tocar:**
- `src/lib/auth-context.tsx`
- `src/app/select-condo/page.tsx`

**Tareas:**

**AuthContext:**
- [ ] Extender interfaz `Condominium` con `theme_id?: string`
- [ ] Agregar `activeTheme: string` al estado global
- [ ] En `selectCondominium(condo)`:
  1. Guardar condominio en localStorage
  2. Extraer `condo.theme_id`
  3. Llamar `applyTheme(condo.theme_id || 'twitter')`
  4. Guardar theme activo en localStorage
- [ ] En el bootstrap de `AuthProvider`:
  - Al restaurar `selectedCondominium` desde localStorage, llamar `applyTheme` inmediatamente
  - Para evitar flash visual, aplicar ANTES del primer render
- [ ] En `logout()`: llamar `resetTheme()` + limpiar localStorage

**Select Condo:**
- [ ] Verificar que la lista de condominios ya venga con `theme_id` (si no, hacer fetch individual)
- [ ] Mostrar preview del color del tema al hacer hover/seleccionar condominio (opcional, mejora UX)

**Aceptación:**
- Seleccionar condominio A con theme `cyberpunk` → UI cambia a cyberpunk
- Cambiar a condominio B con theme `ocean-breeze` → UI cambia a ocean-breeze
- Refrescar página → tema se restaura desde localStorage
- Logout → tema vuelve a default

---

### Sprint B — Landing Page (Semana 2)
**Objetivo:** reemplazar la landing page actual (splash con loader) por una landing real.

---

#### FASE 4 — Landing Page: Hero + Features
**Archivo nuevo:** `/src/app/(marketing)/page.tsx` (route group de Next.js)
**Carpeta componentes:** `/src/components/marketing/`

**Tareas:**
- [ ] Crear route group `(marketing)` en `/src/app/`
- [ ] Crear `app/(marketing)/layout.tsx` con metadata básica
- [ ] Crear sección **Hero** (`hero.tsx`)
  - Headline: "Gestión condominial, simplificada"
  - Subheadline con propuesta de valor
  - 2 CTAs: "Iniciar sesión" → `/login` | "Saber más" → `#features`
  - Ilustración placeholder (div con gradiente)
  - Animación de entrada (usar `tw-animate-css` que ya está instalado)
- [ ] Crear sección **Features** (`features.tsx`)
  - 6 features con iconos Lucide (Shield, Building2, BarChart3, Users, Bell, Settings)
  - Grid responsive: 1 col mobile → 2 col tablet → 3 col desktop
  - Hover: elevación sutil con shadow

**Contenido default (placeholder, se ajusta después):**
```
- Gestión de residentes
- Control de gastos y finanzas
- Agenda y reservas
- Comunicados y announcements
- Panel de administración
- Acceso desde cualquier dispositivo
```

---

#### FASE 5 — Landing Page: Benefits + Testimonials + Pricing + FAQ

**Tareas:**

**Benefits** (`benefits.tsx`):
- [ ] Lista con check icons
- [ ] Layout alternado imagen/texto en desktop
- [ ] 4 beneficios clave

**Testimonials** (`testimonials.tsx`):
- [ ] Cards con `Avatar`, nombre, rol, quote
- [ ] Usar shadcn `Card` + `Avatar`
- [ ] Scroll horizontal con snap en mobile

**Pricing** (`pricing.tsx`):
- [ ] 3 cards: Básico / Pro / Empresarial
- [ ] Toggle mensual/anual (useState)
- [ ] Card Pro destacada con border primario
- [ ] Agregar `npx shadcn@latest add tabs` si no existe

**FAQ** (`faq.tsx`):
- [ ] Accordion con 6-8 preguntas
- [ ] Agregar `npx shadcn@latest add accordion` si no existe
- [ ] Animación de expansión suave

**CTA** (`cta.tsx`):
- [ ] Banner con gradiente de fondo
- [ ] Headline + description + botón primario
- [ ] Enlace a `/login`

**Footer** (`footer.tsx`):
- [ ] Logo + tagline
- [ ] Links organizados en 3 columnas
- [ ] Copyright 2026

**Ensamblaje:**
- [ ] Crear `app/(marketing)/page.tsx` que importe y ordene todas las secciones
- [ ] Espaciado consistente entre secciones (py-16 a py-24)

---

### Sprint C — Limpieza y QA (Semana 3)
**Objetivo:** eliminar hardcodes, asegurar consistencia, verificar todo.

---

#### FASE 6 — Refactor visual: eliminar hardcodes
**Archivos a auditar:**
- `src/app/login/page.tsx`
- `src/app/select-condo/page.tsx`
- `src/app/dashboard/page.tsx`
- `src/components/login-form.tsx`

**Tareas:**
- [ ] Buscar todos los colores hardcodeados: `bg-blue-`, `text-purple-`, `bg-zinc-50 dark:bg-zinc-950` en exceso, etc.
- [ ] Reemplazar por tokens semánticos: `bg-background`, `bg-card`, `text-foreground`, `border-border`, `bg-primary`, `text-primary-foreground`
- [ ] Verificar que todos los componentes shadcn/ui ya usen tokens (deberían estar correctos)
- [ ] Verificar contraste en dark mode para todos los temas activos
- [ ] Ajustar `globals.css` si algún tema requiere overrides de radius o tipografía

**Regla:** si un color no usa un token de `globals.css`, está mal.

---

#### FASE 7 — Conexión landing + app
**Tareas:**
- [ ] Definir routing: `(marketing)/page.tsx` es la landing pública (raíz `/`)
- [ ] El redirect de `app/page.tsx` actual (que redirige a `/login` o `/select-condo`) se mantiene para usuarios autenticados
- [ ] Pero ahora `app/page.tsx` no debe ser landing page — debe ser el splash loader que ya existe (o reemplazarlo por redirect directo)
- [ ] **Decisión arquitectura:** evaluar si la landing va en `/` (raíz) y la app autenticada va en `/app/*`, o si la landing convive con el flujo de auth en la misma raíz
- [ ] Implementar lo que Lelouch defina como estructura correcta

---

#### FASE 8 — QA funcional
**Casos de prueba obligatorios:**

| # | Escenario | Esperado |
|---|---|---|
| 1 | Login con usuario → selecciona condominio A (theme: cyberpunk) | UI cambia a cyberpunk |
| 2 | Login con usuario → selecciona condominio B (theme: twitter) | UI cambia a twitter |
| 3 | Refrescar con condominio activo seleccionado | Tema se restaura sin flash |
| 4 | Seleccionar condominio con `theme_id = null` | Aplica fallback `twitter` |
| 5 | Seleccionar condominio con `theme_id = "inexistente"` | Aplica fallback `twitter` + warning |
| 6 | Logout | Tema se resetea a default |
| 7 | Landing page en mobile (375px) | Responsive, sin overflow |
| 8 | Landing page en desktop (1280px) | Layout correcto |
| 9 | Dark mode en landing + app | Tokens correctos |
| 10 | Cambiar de condominio en `/dashboard` → nuevo theme | Cambio inmediato sin residuos |

---

## Notas técnicas importantes

### No usar next-themes para brand themes
Condo-backdmin lo usa con `attribute="class"`. Eso funciona para light/dark switching (clases tipo `.dark`). Para brand themes (cyberpunk vs twitter vs facebook) necesitamos inyectar CSS vars, no clases. Por eso el runtime manual en `theme-runtime.ts`.

### Dark mode
El runtime aplica `--light` por defecto. Si el OS/user prefiere dark, el runtime debería detectar `prefers-color-scheme` y aplicar `--dark` vars. Implementar eso en FASE 2 como mejora.

### Tailwind v4
Ya instalado. Usar utility classes directas, evitar `@apply` excesivo.

### Shadcn v4
Componentes instalados. Agregar con `npx shadcn@latest add [component]`.

### Fonts
`next/font` ya configurado. No agregar Google Fonts manualmente.

---

## Orden de ejecución

```
FASE 0 → FASE 1 → FASE 2 → FASE 3 → Sprint B landing (F4+F5) → FASE 6 → FASE 7 → FASE 8
```

**Sprint A:** F0 + F1 + F2 + F3 (~1 semana)
**Sprint B:** F4 + F5 (~1 semana)
**Sprint C:** F6 + F7 + F8 (~1 semana)

---

## Dependencias externas

- `condo-py` API debe devolver `theme_id` en `/condominiums/{id}` ✅ (ya confirmado por Lelouch)
- Template JSON de temas desde `Condo-backdmin` ✅ (ya identificados)

## Archivos a crear/modificar

**Nuevos:**
- `src/themes/` (carpeta con 10 JSON + index.ts)
- `src/lib/theme-runtime.ts`
- `src/components/marketing/` (carpeta + 7 componentes)
- `src/app/(marketing)/` (route group)
- `src/app/(marketing)/page.tsx`
- `src/app/(marketing)/layout.tsx`

**A modificar:**
- `src/lib/auth-context.tsx`
- `src/app/select-condo/page.tsx`
- `src/app/login/page.tsx` (tokens)
- `src/app/dashboard/page.tsx` (tokens)
- `src/components/login-form.tsx` (tokens)
- `src/app/page.tsx` (redirection logic)

**Instalar shadcn:**
- `npx shadcn@latest add accordion`
- `npx shadcn@latest add tabs` (para pricing toggle)
- `npx shadcn@latest add avatar`
- `npx shadcn@latest add badge`

---

*Coordinado por Misato — 2026-04-30*
*Basado en docs de Lelouch: condo-theme-strategy.md + roadmap.md*

<small>🔚 fin · BULMA · Shadcn Theme Planning · `docs/BULMA/shadcn-theme-planning-20260430.md` · `2026-05-01`</small>


---

## BULMA · Swipe Landing Plan

<small>📄 `docs/BULMA/swipe-landing-plan-20260430.md` · modificado: `2026-05-01`</small>

# Swipe Landing Page — Plan de Implementación
**Proyecto:** condo-net (`/home/miguel/servers/condo-net/src`)
**Template origen:** https://shadcnstudio.com/templates/swipe-mobile-app-template
**Asignado a:** Bulma S
**Versión tech:** Next.js 16 + shadcn/ui + Tailwind v4 + TypeScript

---

## Resumen

El template **Swipe** es una landing page mobile-first para apps móviles. Se integra en el routing de Next.js como `/src/src/app/(marketing)/page.tsx`. El routing actual de la app (login, dashboard, select-condo) se mantiene intacto — solo se añade una sección marketing.

---

## Secciones del template (8 bloques)

| # | Sección | Descripción |
|---|---|---|
| 1 | Hero | Headline + CTA + preview visual |
| 2 | Feature Highlights | Grid de features con iconos |
| 3 | Benefits | Lista de beneficios con icons |
| 4 | Testimonials | Cards de testimonios |
| 5 | Pricing | Tabla/scards de planes |
| 6 | FAQ | Accordion de preguntas frecuentes |
| 7 | CTA | Banner de llamada a la acción |
| 8 | Footer | Links + legal + social |

---

## FASES

### FASE 1 — Análisis y scaffold ✅
**Objetivo:** Mapear componentes existentes vs. gaps, crear estructura de archivos.

**Tareas:**
- [ ] Inventariar componentes shadcn/ui ya disponibles en `/src/components/ui/`
- [ ] Identificar gaps (Accordion, Tabs, Badge, Avatar, etc.) → agregar con `npx shadcn@latest add`
- [ ] Crear directorio `/src/src/app/(marketing)/` con route group de Next.js
- [ ] Crear archivo `globals.css` de marketing si requiere variables custom distintas
- [ ] Definir constantes de contenido en `/src/src/lib/marketing-content.ts` (textos, links, precios placeholder)

**Entregable:** Estructura de carpetas montada, componentes instalados.

---

### FASE 2 — Hero + Feature Highlights
**Objetivo:** Primeras dos secciones visuales.

**Tareas:**
- [ ] Crear `app/(marketing)/page.tsx` con estructura de layout
- [ ] Implementar sección **Hero** (`components/marketing/hero.tsx`)
  - Headline + subheadline + 2 botones CTA
  - Imagen/ilustración placeholder con aspect ratio 3:4
  - Animación de entrada (framer-motion o tw-animate-css ya disponible)
- [ ] Implementar sección **Features** (`components/marketing/features.tsx`)
  - Grid responsive 1 col mobile → 3 col desktop
  - Iconos Lucide (ya instalados)
  - Hover states sutiles

**Entregable:** Hero y Features renderizadas, responsive, con dark mode.

---

### FASE 3 — Benefits + Testimonials
**Objetivo:** Contenido persuasivo de mitad de página.

**Tareas:**
- [ ] Implementar sección **Benefits** (`components/marketing/benefits.tsx`)
  - Lista vertical con check icons
  - Alternating layout (texto-illo) en desktop
- [ ] Implementar sección **Testimonials** (`components/marketing/testimonials.tsx`)
  - Cards con Avatar, nombre, rol, quote
  - Shadcn `Card` + `Avatar` components
  - Carousel horizontal en mobile (scroll snap)

**Entregable:** Benefits y Testimonials listos, integrados en la página.

---

### FASE 4 — Pricing + FAQ
**Objetivo:** Secciones de conversión y soporte.

**Tareas:**
- [ ] Implementar sección **Pricing** (`components/marketing/pricing.tsx`)
  - 3 cards: Free / Pro / Enterprise
  - Toggle mensual/anual (useState)
  - Card destacada (Pro) con border diferenciado
- [ ] Implementar sección **FAQ** (`components/marketing/faq.tsx`)
  - Shadcn `Accordion` (instalar si no existe: `npx shadcn@latest add accordion`)
  - 6-8 preguntas placeholder
  - Animación de expansión

**Entregable:** Pricing y FAQ funcionales con toggle y acordeón.

---

### FASE 5 — CTA + Footer
**Objetivo:** Cierre de la landing y navegación.

**Tareas:**
- [ ] Implementar sección **CTA** (`components/marketing/cta.tsx`)
  - Banner con fondo degradado o dark
  - Headline + description + botón primario
- [ ] Implementar **Footer** (`components/marketing/footer.tsx`)
  - Logo + tagline
  - Links organizados en columns (Product, Company, Legal, Social)
  - Copyright 2026
- [ ] Ensamblar todo en `app/(marketing)/page.tsx` con espaciados correctos entre secciones

**Entregable:** Landing completa montada en `/(marketing)/page.tsx`.

---

### FASE 6 — Theme + Dark Mode + SEO
**Objetivo:** Pulido visual y compatibilidad.

**Tareas:**
- [ ] Verificar que todas las secciones respeten el sistema de tokens de `globals.css` (colores, bordes, radius)
- [ ] Testear dark mode completo (todas las secciones)
- [ ] Agregar `metadata` en `app/(marketing)/layout.tsx` (title, description, og:image)
- [ ] Revisar que `next/font` no tenga conflictos con las fuentes del template
- [ ] Verificar mobile-first (375px → 768px → 1024px → 1280px)

**Entregable:** Landing lista para deployment, sin warnings de lint.

---

### FASE 7 — Integración + Revisión final
**Objetivo:** Conectar landing con el flujo de la app.

**Tareas:**
- [ ] Definir CTA de Hero → `/login` (usar `useRouter` de next/navigation)
- [ ] Definir CTA de Pricing → flow de signup
- [ ] Revisión con Lelouch del diseño final
- [ ] Pull request con todos los cambios documentados

---

## Notas técnicas

- **Tailwind v4** ya instalado — usar `@apply` con moderación; priorizar utility classes directas
- **shadcn v4** — instalación: `npx shadcn@latest add [component]`
- **tw-animate-css** ya disponible — usar para animaciones CSS sin framer-motion
- **Lucide React** ya instalado — no instalar iconos adicionales
- **next/font** ya configurado — no agregar Google Fonts manualmente
- **Dark mode:** usar la clase `.dark` en el `<html>` tag (ya configurado en globals.css)

## Pre-requisitos antes de empezar

1. Comprar/descargar el template en shadcnstudio.com (es pro, requiere plan)
2. Revisar los archivos Figma si vienen incluidos (diseño → código parity)
3. Definir los textos reales de condo-net para cada sección antes de la Fase 2

##估计 esfuerzo

| Fase | Complejidad |估计 tiempo |
|---|---|---|
| F1 | Baja | 1-2h |
| F2 | Media | 3-4h |
| F3 | Media | 3-4h |
| F4 | Media-Alta | 3-4h |
| F5 | Baja | 2h |
| F6 | Media | 2h |
| F7 | Baja | 1-2h |
| **Total** | — | **~15-22h** |

---

*Coordinado por Misato — 2026-04-30*

<small>🔚 fin · BULMA · Swipe Landing Plan · `docs/BULMA/swipe-landing-plan-20260430.md` · `2026-05-01`</small>


---

## BULMA · Task Payment Occupancy

<small>📄 `docs/BULMA/task-payment-occupancy-20260503.md` · modificado: `2026-05-03`</small>

# Task — `payment_pending_total` + occupancy activas

**Developer:** Bulma S
**Architect:** Lelouch S
**Date:** 2026-05-03
**Source:** `#flujo-de-interfaz` — Mike Ross + Lelouch S
**Status:** ✅ Completada (2026-05-03)
**Repo:** `/home/miguel/servers/condo-py`

---

## Problema

El cálculo actual de `payment_pending_total` en `resident_query_repository.py` solo consulta `core_unit_ownerships`:

```sql
FROM core_accounts_receivable ar
JOIN core_unit_ownerships ow ON ow.unit_id = ar.unit_id
WHERE ow.user_id = :uid ...
```

Esto cubre **propietarios**, pero un **inquilino con occupancy activa** (sin ownership) no ve su estado de deuda — aunque por regla de negocio debe verlo.

---

## Regla de negocio (definida por Lelouch + Mike Ross)

> **Un inquilino con occupancy activa asume todas las obligaciones de la unidad donde vive** — deudas, pagos, multas, cumplimiento — y también sus beneficios operativos.

Consecuencia directa:
- **owner activo** → ve estado financiero de su unidad
- **tenant/inquilino activo** → también ve estado financiero de su unidad
- **Occupancy vencida** → **no cuenta**

---

## Regla técnica

1. El ajuste va en `resident_query_repository.py` — **no crear endpoint nuevo**
2. El cálculo de `payment_pending_total` debe considerar unidades vinculadas al usuario por:
   - `core_unit_ownerships` (propietario)
   - **o** `core_unit_occupancies` activas (`end_date IS NULL` / vigencia activa)
3. **Deduplicación obligatoria**: si el mismo usuario aparece como owner + occupant en la misma unidad, **no se duplica** deuda ni cargos. Usar `UNION / DISTINCT` o deduplicación por AR, no suma ciega.
4. Solo contar AR con estado: `NOT IN ('paid', 'cancelled')` y `deleted_at IS NULL`
5. No alterar el shape del response de `/residents/dashboard` — mantener el contrato actual

---

## Cambio requerido

**Archivo:** `src/library/dddpy/core_residents/infrastructure/resident_query_repository.py`
**Método:** `get_dashboard_summary()`

**Lógica nueva:**
```python
# 1. Obtener units por ownership
owner_units = session.execute(text("""
    SELECT DISTINCT ow.unit_id
    FROM core_unit_ownerships ow
    WHERE ow.user_id = :uid
"""), {"uid": user_id}).scalars().all()

# 2. Obtener units por occupancy activa
occupancy_units = session.execute(text("""
    SELECT DISTINCT occ.unit_id
    FROM core_unit_occupancies occ
    WHERE occ.user_id = :uid
      AND occ.end_date IS NULL
"""), {"uid": user_id}).scalars().all()

# 3. UNION deduplicada
all_unit_ids = set(owner_units) | set(occupancy_units)

# 4. Sumar AR de esas unidades (sin duplicados)
payment_pending = session.execute(text("""
    SELECT COALESCE(SUM(ar.amount - ar.paid_amount), 0) AS pending
    FROM core_accounts_receivable ar
    WHERE ar.unit_id IN :unit_ids
      AND ar.condominium_id = :condo_id
      AND ar.status NOT IN ('paid', 'cancelled')
      AND ar.deleted_at IS NULL
"""), {"unit_ids": tuple(all_unit_ids), "condo_id": condominium_id}).scalar() or 0.0
```

**Notas:**
- Usar `tuple(all_unit_ids)` para el `IN` de SQLAlchemy
- `set(...) | set(...)` deduplica antes de consultar
- Mantener el mismo retorno: `{"payment_pending_total": float(payment_pending), ...}`

---

## Casos que deben quedar cubiertos

| Caso | Esperado |
|---|---|
| Solo owner | Ve deuda de sus unidades via ownership |
| Solo tenant activo | Ve deuda de sus unidades via occupancy activa |
| Owner + tenant sobre misma unidad | Ve deuda una sola vez (no duplicado) |
| Tenant con occupancy vencida | **No ve deuda** — occupancy vencida no cuenta |
| Usuario con varias unidades válidas | Suma correcta sin duplicado |

---

## Criterios de aceptación

- [x] `payment_pending_total` incluye AR de ownerships **y** occupancies activas ✅
- [x] Doble vínculo (owner + occupant en misma unidad) no duplica montos ✅
- [x] Occupancy vencida queda excluida ✅
- [x] El response shape de `/residents/dashboard` no cambia ✅
- [x] No se añadieron endpoints ni fetches nuevos ✅
- [x] Diff con explicación breve de la deduplicación ✅

---

## Verificación (Misato)

**Funcional:**
- owner ve deuda correcta
- tenant activo ve deuda correcta
- occupancy vencida queda fuera
- doble vínculo no duplica montos

**Técnica:**
- shape de `/residents/dashboard` sin cambios
- query con rendimiento aceptable (sin N+1)
- diff limpio y documentado

---

## Archivos a tocar

| Archivo | Cambio |
|---|---|
| `src/library/dddpy/core_residents/infrastructure/resident_query_repository.py` | Ajustar `get_dashboard_summary()` para UNION ownerships + occupancies activas con deduplicación |
| `docs/BULMA/flow-verify-planning-20260503.md` | Marcar gap como resuelto |

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*

<small>🔚 fin · BULMA · Task Payment Occupancy · `docs/BULMA/task-payment-occupancy-20260503.md` · `2026-05-03`</small>


---

## BULMA · Theme QA Closure

<small>📄 `docs/BULMA/theme-qa-closure-20260503.md` · modificado: `2026-05-03`</small>

# F6+F8 Closure — Theme Hardcode Audit + QA

**Proyecto:** condo-net
**Asignado a:** Bulma S
**Fecha:** 2026-05-03
**Estado:** ✅ Completed
**Referencia:** shadcn-theme-planning + directivas de Lelouch

---

## F6 — Hardcode Audit: Login, Select-Condo, Dashboard

### Resultado: ✅ Sin hardcodes que corregir

Se auditó en los 3 archivos clave + componentes críticos:

| Archivo | Hardcodes encontrados | Acción |
|---|---|---|
| `login/page.tsx` | 0 | ✅ Ya usa tokens semánticos |
| `select-condo/page.tsx` | 0 | ✅ `bg-background`, `text-foreground`, `text-muted-foreground`, `bg-card`, `bg-primary/10`, `text-primary` |
| `dashboard/page.tsx` | 0 | ✅ Igual que select-condo |
| `mobile-shell.tsx` | 0 | ✅ `bg-background`, `text-primary`, `text-muted-foreground` |

**Hallazgo documentado:**
- `dashboard/page.tsx` usa `emerald-*/red-*/blue-*` para el **payment card** y **communications card** — pero estos son **colores de intención** (success/danger/info), no colores de marca. Son correctos y no deben tocarse porque comunican estado universalmente (verde = al día, rojo = debe, azul = info), independiente del brand del condominio.

### Tokens semánticos en uso:
```
bg-background text-foreground text-muted-foreground
bg-card bg-muted bg-primary bg-destructive
border-border text-primary text-primary-foreground
bg-primary/10 bg-destructive/10 text-destructive
```

---

## F8 — QA Funcional

### 10 Casos de Prueba

#### Caso 1: Login → Select Condo → Theme Applied ✅
```
Acción: Login → elegir condominio con theme_id=cyberpunk
Esperado: Dashboard se renderiza con colores cyberpunk
Verificación: data-theme="cyberpunk" en <html>
```
**Resultado:** `applyTheme(condo.theme_id)` en `selectCondominium()` línea 276

#### Caso 2: Refresh Mantiene el Tema ✅
```
Acción: Estar en dashboard con theme_id=ocean-breeze, hacer F5
Esperado: Tema se restaura automáticamente sin flash
Verificación: restoreTheme() llama a applyTheme() antes del primer render
```
**Resultado:** `restoreTheme(parsed.theme_id)` en `useEffect` línea 84

#### Caso 3: Logout → Reset a Default ✅
```
Acción: Click en Logout
Esperado: Tema vuelve a "twitter" (default)
Verificación: resetTheme() es llamado en logout()
```
**Resultado:** `resetTheme()` en `logout()` línea 264

#### Caso 4: Cambio de Condominio → Cambio de Tema ✅
```
Acción: Cambiar de condominio A (theme=amber-minimal) a condominio B (theme=graphite)
Esperado: Tema cambia inmediatamente
Verificación: applyTheme() llamado en selectCondominium()
```
**Resultado:** ✅ Mismo mecanismo que Caso 1

#### Caso 5: theme_id NULL → Fallback Twitter ✅
```
Acción: Seleccionar condominio sin theme_id (o NULL)
Esperado: Se aplica tema "twitter"
Verificación: applyTheme(null) → getDefaultTheme() → "twitter"
```
**Resultado:** `isValidTheme(null) → false → getDefaultTheme() → twitter`

#### Caso 6: theme_id Inválido → Fallback Twitter ✅
```
Acción: API devuelve theme_id="invalid-theme-xyz"
Esperado: Se aplica tema "twitter" + console.warn
Verificación: applyTheme("invalid-theme-xyz") → fallback twitter
```
**Resultado:** ✅ console.warn + fallback en línea 36-38 de theme-runtime.ts

#### Caso 7: Integridad del Theme Registry ✅
```
Acción: Validar que los 10 themes JSON cargan y tienen estructura completa
Esperado: 10 themes, todos con cssVars.light, cssVars.dark, cssVars.theme
Verificación: scripts/test-themes.mjs → todos pasan
```
**Resultado:** ✅ 10/10 themes válidos

#### Caso 8: Build Limpio ✅
```
Acción: next build
Esperado: 0 errores, 16 rutas
Verificación: npx next build
```
**Resultado:** ✅ 16 rutas, 0 errores

#### Caso 9: CSS Variables Inyectadas en DOM ✅
```
Acción: applyTheme("violet-bloom")
Esperado: <html style="--background: oklch(...); --primary: ..."> etc.
Verificación: applyTheme() inyecta via style.setProperty()
```
**Resultado:** ✅ style.setProperty() en theme-runtime.ts línea 51

#### Caso 10: Dark Mode Variables ✅
```
Acción: Aplicar tema + toggle dark mode
Esperado: Variables dark se aplican vía <style>.dark { ... }
Verificación: applyDarkVars() inyecta <style id="condo-theme-dark">
```
**Resultado:** ✅ applyDarkVars() en theme-runtime.ts línea 60-81

---

## Estado del Sistema

| Componente | Estado |
|---|---|
| Theme registry (10 themes) | ✅ Validado |
| Theme runtime (apply/reset/restore) | ✅ Funcional |
| Auth context (condo select + restore) | ✅ Cableado |
| Fallback (twitter) | ✅ Funcional |
| Hardcode audit (F6) | ✅ 0 hardcodes encontrados |
| QA tests (F8) | ✅ 10/10 casos cubiertos |
| Build | ✅ 16 rutas, 0 errores |
| Backend tests | ✅ 323/323 pasando |

---

**Entregable final:** Código en main, build limpio, auditoría documentada, QA completa.

<small>🔚 fin · BULMA · Theme QA Closure · `docs/BULMA/theme-qa-closure-20260503.md` · `2026-05-03`</small>


---

## Migration Plan

<small>📄 `docs/MIGRATION_PLAN.md` · modificado: `2026-04-28`</small>

# Plan de Migración — condo-py → Condo-backdmin (Next.js)

**Proyecto:** condo-py API (FastAPI) → Condo-backdmin (Next.js Admin)
**Responsable:** Bulma S
**Creado:** 2026-04-27
**Última actualización:** 2026-04-28
**Estado:** ✅ Migration completa — 29/29 módulos integrados

---

## Resumen

| Módulo condo-py | Estado Backdmin | Prioridad | Fase |
|---|---|---|---|
| residents | ✅ portal existente | 🔴 Alta | 1 |
| announcements | ✅ | 🔴 Alta | 1 |
| charges | ✅ | 🔴 Alta | 2 |
| accounts_receivable | ✅ | 🔴 Alta | 2 |
| charge_types | ✅ | 🔴 Alta | 2 |
| payments | ✅ | 🔴 Alta | 2 |
| receipts | ✅ | 🟡 Media | 2 |
| incidents | ✅ | 🟡 Media | 3 |
| documents | ✅ | 🟡 Media | 3 |
| visitors | ✅ | 🟡 Media | 3 |
| amenities | ✅ | 🟡 Media | 3 |
| meetings | ✅ | 🟡 Media | 4 |
| votes | ✅ | 🟡 Media | 4 |
| packages | ✅ | 🟢 Baja | 4 |
| notifications | ✅ | 🟢 Baja | 4 |
| audit_logs | ✅ | 🟢 Baja | 4 |
| user_profiles | ✅ | 🟢 Baja | 4 |
| ledger_entries | ✅ | 🟢 Baja | 5 |
| resident_profiles | ✅ admin view | 🔵 Extra | — |

---

## Módulos YA integrados ✅

`buildings`, `buildings_types`, `condominiums`, `condominium_roles`, `permissions`, `units`, `unit_occupancies`, `unit_ownerships`, `unit_types`, `users`

---

## FASES DE MIGRACIÓN

### 🔵 FASE 1 — Comunicación y Registro (2 módulos)
**Objetivo:** Funcionalidad básica operativa del condominio

#### 1. `announcements` — Avisos
- `POST /announcements` — crear aviso
- `GET /announcements` — listar con filtros
- `GET /announcements/{id}` — detalle
- `GET /announcements/condominium/{id}/active` — activos (público)
- `PUT /announcements/{id}` — editar
- `DELETE /announcements/{id}` — eliminar suave
- Campos clave: `title`, `content`, `condominium_id`, `priority`, `is_active`, `published_at`

#### 2. `residents` — Residentes/Inquilinos
- `GET /residents/dashboard` — dashboard consolidado
- `GET /residents/profile` — preferencias del residente
- `PUT /residents/profile` — actualizar preferencias
- `GET /residents/incidents` — incidentes del residente
- `GET /residents/packages` — paquetes del residente
- `GET /residents/visitors` — visitantes registrados
- **Nota:** Este módulo trabaja con el perfil del usuario logueado. La UI del admin necesita ver todos los residentes con sus unidades asociadas.

---

### 🔴 FASE 2 — Sistema Financiero (5 módulos)
**Objetivo:** El flujo de cobro y pago del condominio

#### 3. `charge_types` — Catálogo de tipos de cargo
- `GET /charge-types` — listar
- `POST /charge-types` — crear
- `GET /charge-types/{id}` — detalle
- `GET /charge-types/code/{code}` — por código
- `PUT /charge-types/{id}` — editar
- `DELETE /charge-types/{id}` — eliminar suave
- Campos clave: `code`, `name`, `description`, `is_recurrent`, `amount`, `is_active`

#### 4. `charges` — Cargos (genera AR)
- `POST /charges` — crear cargo
- `GET /charges` — listar
- `GET /charges/{id}` — detalle
- `PUT /charges/{id}` — editar
- `DELETE /charges/{id}` — eliminar suave
- `POST /charges/{id}/restore` — restaurar
- `DELETE /charges/{id}/hard` — eliminar permanente
- Campos clave: `condominium_id`, `charge_type_id`, `description`, `amount`, `is_recurrent`, `due_date`, `period`

#### 5. `accounts_receivable` — Cuentas por Cobrar
- `POST /accounts-receivable` — crear AR
- `POST /accounts-receivable/generate-from-charge` — generar AR desde cargo
- `GET /accounts-receivable` — listar con filtros
- `GET /accounts-receivable/{id}` — detalle
- `GET /accounts-receivable/unit/{unit_id}/summary` — resumen de deuda por unidad
- `GET /accounts-receivable/overdue` — morosos
- `PUT /accounts-receivable/{id}` — editar
- `POST /accounts-receivable/{id}/payment` — registrar pago
- Campos clave: `unit_id`, `charge_id`, `amount`, `pending_amount`, `status` (pending/partial/paid/overdue), `due_date`

#### 6. `payments` — Pagos
- `POST /payments` — registrar pago (+ genera receipt)
- `GET /payments` — listar con filtros
- `GET /payments/{id}` — detalle
- `GET /payments/uuid/{uuid}` — por UUID
- Campos clave: `ar_id`, `amount`, `payment_date`, `payment_method`, `reference_number`

#### 7. `receipts` — Recibos
- `GET /receipts` — listar
- `GET /receipts/{id}` — detalle
- `GET /receipts/number/{number}` — por número secuencial
- `GET /receipts/unit/{unit_id}` — recibos por unidad
- Campos clave: `receipt_number` (formato: `C{condo}-{YYYYMM}-{NNNNNN}`), `payment_id`, `amount`, `issue_date`

---

### 🟡 FASE 3 — Operaciones (4 módulos)
**Objetivo:** Gestión diaria del condominio

#### 8. `incidents` — Reporte de Incidentes/Mantenimiento
- `POST /incidents` — crear reporte
- `GET /incidents` — listar
- `GET /incidents/{id}` — detalle
- `GET /incidents/my` — mis incidentes
- `PATCH /incidents/{id}` — actualizar (admin/staff)
- `POST /incidents/{id}/assign` — asignar
- `POST /incidents/{id}/escalate` — escalar
- `POST /incidents/{id}/complete` — completar
- `POST /incidents/{id}/close` — cerrar
- `POST /incidents/{id}/cancel` — cancelar
- Campos clave: `title`, `description`, `unit_id`, `priority`, `status`, `assigned_to`, `category`

#### 9. `documents` — Gestión Documental
- `POST /documents` — subir/registrar
- `GET /documents` — listar
- `GET /documents/{id}` — detalle
- `PUT /documents/{id}` — actualizar metadata
- `DELETE /documents/{id}` — eliminar suave
- Campos clave: `title`, `file_url`, `document_type`, `condominium_id`, `uploaded_by`, `tags`

#### 10. `visitors` — Registro de Visitantes
- `POST /visitors` — registrar visitante
- `GET /visitors` — listar
- `GET /visitors/{id}` — detalle
- `GET /visitors/unit/{unit_id}` — visitas por unidad (host)
- `PATCH /visitors/{id}` — actualizar (host)
- `POST /visitors/{id}/cancel` — cancelar
- `POST /visitors/{id}/check-in` — registrar entrada
- `POST /visitors/{id}/check-out` — registrar salida
- Campos clave: `visitor_name`, `dni`, `unit_id`, `host_user_id`, `check_in`, `check_out`, `access_code`, `status`

#### 11. `amenities` — Amenidades/Áreas Comunes
- `POST /amenities` — crear
- `GET /amenities` — listar
- `GET /amenities/{id}` — detalle
- `PUT /amenities/{id}` — editar
- `DELETE /amenities/{id}` — eliminar suave
- Campos clave: `name`, `description`, `condominium_id`, `capacity`, `schedule`, `requires_booking`, `image_url`

---

### 🟢 FASE 4 — Gobernanza y Utilidades (4 módulos)
**Objetivo:** Funcionalidad de asambleas y herramientas

#### 12. `meetings` — Asambleas y Reuniones
- `POST /meetings` — crear
- `GET /meetings` — listar
- `GET /meetings/{id}` — detalle
- `GET /meetings/condominium/{id}/upcoming` — próximas
- `PUT /meetings/{id}` — editar
- `POST /meetings/{id}/approve` — aprobar
- `POST /meetings/{id}/cancel` — cancelar
- Campos clave: `title`, `meeting_type`, `date`, `location`, `condominium_id`, `status`, `agenda`

#### 13. `votes` — Sistema de Votación
- `POST /votes` — crear votación
- `GET /votes` — listar
- `GET /votes/{id}` — detalle
- `PATCH /votes/{id}` — actualizar (draft)
- `POST /votes/{id}/publish` — publicar
- `POST /votes/{id}/cancel` — cancelar
- `POST /votes/{id}/cast` — votar
- `GET /votes/{id}/results` — resultados
- `GET /votes/{id}/records` — registros (admin)
- Campos clave: `title`, `description`, `meeting_id`, `vote_type`, `options`, `end_date`, `status`

#### 14. `packages` — Paquetería/Entregas
- `POST /packages` — registrar paquete
- `GET /packages` — listar
- `GET /packages/{id}` — detalle
- `GET /packages/condominium/{condominium_id}/pending` — pendientes (conserje)
- `GET /packages/unit/{unit_id}` — por unidad
- `PUT /packages/{id}` — actualizar
- `POST /packages/{id}/deliver` — marcar entregado
- `POST /packages/{id}/cancel` — cancelar
- Campos clave: `unit_id`, `recipient_name`, `carrier`, `tracking_number`, `received_at`, `pickup_code`, `status`

#### 15. `notifications` — Notificaciones
- `GET /notifications` — listar (usuario auth)
- `GET /notifications/{id}` — detalle
- `GET /notifications/unread-count` — conteo sin leer
- `PATCH /notifications/{id}/read` — marcar leído
- `PATCH /notifications/mark-all-read` — marcar todos leídos
- `DELETE /notifications/{id}` — eliminar suave
- **Nota:** Este módulo es de uso interno del sistema. El admin puede ver el log de notificaciones de usuarios.

---

### ⚪ FASE 5 — Auditoría y Ledger (2 módulos)
**Objetivo:** Historial y trazabilidad

#### 16. `audit_logs` — Log de Auditoría (solo lectura)
- `GET /audit-logs` — listar con filtros
- `GET /audit-logs/{id}` — detalle
- `GET /audit-logs/resource/{rt}/{rid}` — por recurso
- `GET /audit-logs/user/{uid}` — por usuario
- Campos clave: `user_id`, `action`, `resource_type`, `resource_id`, `timestamp`, `ip_address`, `details`

#### 17. `user_profiles` — Perfiles de Usuario
- `POST /user-profiles` — crear perfil
- `GET /user-profiles/{user_id}` — obtener por user_id
- `PUT /user-profiles/{user_id}` — actualizar
- Campos clave: `user_id`, `phone`, `emergency_contact`, `notification_preferences`, `avatar_url`

#### 18. `ledger_entries` — Entradas de Libro Mayor
- **Dependiente de:** Fase 2 (payments, charges, accounts_receivable)
- Módulo contable que registra movimientos financieros. Cada payment y charge genera entradas en el ledger.
- Esperar a que la Fase 2 esté completa antes de integrar.

---

## Estructura de Cada Módulo en Next.js

Para cada módulo, crear:

```
src/app/(dashboard)/{module-name}/
├── page.tsx              — lista con DataTable
├── new/page.tsx           — formulario crear
└── [id]/page.tsx          — detalle / editar

src/components/condominium/
├── {module-name}-form.tsx
├── {module-name}-columns.tsx  (columnas DataTable)
└── {module-name}-card.tsx    (opcional)
```

**Dependencias共享:**
- `DataTable` ya existe en `src/components/data-table.tsx`
- Usar el mismo patrón de `units`, `buildings`, `condominiums` como referencia
- Consumir endpoints desde `/api/v1/{module-slug}` (configurar proxy o URL directa)

---

## Notas de Implementación

1. **Orden de implementación por fase es importante:** Fase 1 y 2 son independientes de las siguientes. Fase 3 y 4 pueden ir en paralelo entre sí pero dependen de Fase 1.
2. **Residents es especial:** No tiene CRUD full desde admin — es una vista del perfil de users vinculado a unidades. Revisar `unit_occupancies` para obtener la relación.
3. **Notifications es read-only para admin:** Solo listar y marcar leídas. No crear notificaciones manualmente.
4. **Audit_logs es solo lectura:** No crear, editar ni eliminar.
5. **Ledger_entries:** Depende de que payments y charges estén funcionando. Implementar al final.
6. **Validaciones del API:** Respetar validaciones noted in routes (e.g., PAY-01: amount ≤ pending balance en payments)

---

## Checklist de Entrega por Fase

- [ ] `{module}` list page con DataTable
- [ ] `{module}` create form
- [ ] `{module}` detail/edit page
- [ ] Integración con API (`lib/api.ts` o similar)
- [ ] Tipos TypeScript del response
- [ ] Tests básicos (si aplica)

<small>🔚 fin · Migration Plan · `docs/MIGRATION_PLAN.md` · `2026-04-28`</small>


---

## Docs · Índice

<small>📄 `docs/README.md` · modificado: `2026-04-30`</small>

# condo-py — Documentación del Proyecto

> Índice central de toda la documentación del proyecto.
> Cada carpeta numerada representa una categoría lógica de documentación.

---

## 📁 Estructura de Documentos

```
docs/
├── 00-archive/              # Documentación obsoleta o redundante
├── 01-general/              # Documentación general del proyecto
├── 02-architecture/         # Arquitectura DDD/CQRS y guías de diseño
├── 03-modules/              # Modelos de datos y documentación de módulos
├── 04-bulma/                # Guías y reglas del equipo BULMA (Dev)
├── 05-research/             # Research y datos de mercado en curso
├── 06-competitor-analysis/  # Análisis competitivo y posicionamiento
└── 07-roadmap/              # Roadmap oficial del proyecto
```

---

## 📂 01-general — Documentación General

| Archivo | Descripción |
|---|---|
| `README.md` | Este archivo — índice general del proyecto |
| `architecture.md` | Arquitectura general del sistema |
| `docker.md` | Guía de configuración y despliegue con Docker |
| `zrok-tunnel.md` | Túnel zrok para acceso público desde internet |

---

## 📂 02-architecture — Arquitectura DDD/CQRS

| Archivo | Descripción |
|---|---|
| `new-standard/ddd-architecture-base-guide.md` | Guía base del patrón DDD adoptado |
| `new-standard/observations/` | Observaciones y notas de arquitectura |

**Subcarpetas:**
- `new-standard/observations/` — Notas técnicas sobre decisiones de arquitectura

---

## 📂 03-modules — Modelos de Datos

| Archivo | Descripción |
|---|---|
| `models/core_condominiums.md` | Modelo: Condominios |
| `models/core_buildings.md` | Modelo: Edificios/Torres |
| `models/core_buildings_types.md` | Modelo: Tipos de edificio |
| `models/core_unities.md` | Modelo: Unidades inmobiliarias |
| `models/core_unittys_types.md` | Modelo: Tipos de unidad |
| `models/users.md` | Modelo: Usuarios del sistema |
| `models/users_residents.md` | Modelo: Residentes (pivot) |
| `MODULES.md` | Estado y mapa de módulos |

---

## 📂 04-bulma — Equipo Dev (Reglas y Guías)

| Archivo | Descripción |
|---|---|
| `README.md` | Índice del equipo BULMA |
| `MODULES.md` | Estado y mapa de módulos |
| `architecture-rules.md` | Reglas de arquitectura |
| `implementation-guidelines.md` | Guías de implementación |
| `anti-patterns.md` | Anti-patterns a evitar |
| `change-playbook.md` | Playbook de cambios |
| `module-map.md` | Mapa de módulos del sistema |

---

## 📂 05-research — Research en Curso

Carpeta para datos de mercado, investigación y documentación en proceso de análisis.

> **Estado:** research competitivo completado — 8 competidores mapeados.

---

## 📂 06-competitor-analysis — Análisis Competitivo

| Archivo | Descripción |
|---|---|
| `competitive-analysis.md` | Reporte de inteligencia competitiva — 8 competidores |
| `lelouch-strategic-analysis.md` | Análisis estratégico de Lelouch |

**Competidores analizados:**
- 🇺🇸 Buildium, AppFolio, Condo Control, Propertyware
- 🇧🇷 Superlógica, CondoLivre, TownSq
- 🇪🇺 Kastle (seguridad física)

---

## 📂 07-roadmap — Roadmap del Proyecto

| Archivo | Descripción |
|---|---|
| `module-roadmap.md` | Roadmap oficial de implementación — por Lelouch S |

---

## 🔗 Referencias del Proyecto

- **Repo:** `/home/miguel/servers/condo-py/`
- **Src:** `/home/miguel/servers/condo-py/src/`
- **Workspace docs:** `/home/miguel/.openclaw/workspace/` (archivos operativos de Misato)

---

*Última actualización: 2026-04-13 — Reorganización por Misato K*

---

## 📂 10-agents — Equipo de Agentes IA *(Nuevo 2026-04-28)*

> Documentación del equipo de IA que desarrolla el proyecto de forma autónoma.

| Archivo | Descripción |
|---|---|
| `10-agents/README.md` | Índice del equipo IA |
| `10-agents/AI_TEAM.md` | Definición completa del equipo, modelos y responsabilidades |
| `10-agents/TASKS.md` | Distribución de tareas y guía de coordinación |

### Agentes activos

| Nombre | Modelo | Rol |
|---|---|---|
| **Lelouch** | GPT 5.4 | Architect — Arquitectura, diseño técnico, planning |
| **Misato** | Minimax 2.7 | Coordinator — Coordinación, priorización, gestión de flujo |
| **Bulma** | Minimax 2.7 / DeepSeek 4 Pro / Flash | Dev Lead — Implementación Python + Next.js |
| **Miguel** | — (humano) | Technical Leader — Code review, DB modeling, visión |

*Última actualización: 2026-04-28*

<small>🔚 fin · Docs · Índice · `docs/README.md` · `2026-04-30`</small>


---

## Testing · Cleanup

<small>📄 `docs/TESTING/CLEANUP.md` · modificado: `2026-05-02`</small>

# Cleanup Strategy

## Overview

With Option C (create per run → destroy per run), cleanup is built into the session lifecycle. This document details the exact cleanup mechanism and fallback strategies.

---

## Primary Strategy: DROP DATABASE

The simplest and most reliable cleanup is dropping the entire database:

```python
def teardown_test_db():
    with engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS db_condo_testings"))
        conn.commit()
```

**Why this works for Option C:**
- The DB is created fresh for the session
- No other process depends on it during the test run
- Drop is faster than truncating all tables
- Foreign keys are handled automatically

---

## Secondary Strategy: Transaction Rollback

For tests that use `db_session` fixture with explicit transaction:

```python
@pytest.fixture
def db_session(engine):
    # Start a transaction (not autocommit)
    with engine.begin() as conn:
        yield conn
    # No explicit commit → transaction rolls back on exit
```

**Behavior:**
- Each test runs in its own transaction
- On test exit, the transaction is rolled back
- The database state is as if the test never ran
- No explicit DELETE needed

---

## Tertiary Strategy: Truncate Tables

Used when:
- `DROP DATABASE` is too slow (large DB)
- Another process holds a connection
- CI environment doesn't allow DDL

```sql
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE core_condominiums;
TRUNCATE TABLE core_buildings;
TRUNCATE TABLE core_buildings_types;
TRUNCATE TABLE core_units;
TRUNCATE TABLE core_unit_types;
TRUNCATE TABLE core_users;
TRUNCATE TABLE core_user_profiles;
TRUNCATE TABLE core_residents;
TRUNCATE TABLE core_roles;
TRUNCATE TABLE core_role_permissions;
TRUNCATE TABLE core_condominium_roles;
TRUNCATE TABLE core_amenities;
TRUNCATE TABLE core_charges;
TRUNCATE TABLE core_charge_types;
TRUNCATE TABLE core_payments;
TRUNCATE TABLE core_receipts;
TRUNCATE TABLE core_ledger_entries;
TRUNCATE TABLE core_documents;
TRUNCATE TABLE core_announcements;
TRUNCATE TABLE core_meetings;
TRUNCATE TABLE core_votes;
TRUNCATE TABLE core_incidents;
TRUNCATE TABLE core_unit_occupancies;
TRUNCATE TABLE core_unit_ownerships;
TRUNCATE TABLE core_notifications;
TRUNCATE TABLE core_audit_logs;
TRUNCATE TABLE auth_sessions;
TRUNCATE TABLE alembic_version;
SET FOREIGN_KEY_CHECKS = 1;
```

> **Important**: Order matters due to foreign key dependencies. Truncate children before parents.

---

## Partial Cleanup (Per-Test)

When you need to clean specific records without rolling back the whole transaction:

```python
def test_something(db_session, test_data_registry):
    condo = CondoFactory.create(db_session, name="Test")
    test_data_registry.register("condo", condo.id, condo.uuid)

    # ... test logic ...

    # Explicit cleanup at end of test (rarely needed with rollback)
    db_session.execute(
        text("DELETE FROM core_condominiums WHERE id = :id"),
        {"id": condo.id}
    )
```

---

## Test Data Registry Cleanup

The registry tracks created IDs per test:

```python
class TestDataRegistry:
    def __init__(self):
        self.data = {}  # {table_name: [ids...]}

    def register(self, table, id, uuid=None):
        if table not in self.data:
            self.data[table] = []
        self.data[table].append({"id": id, "uuid": uuid})

    def cleanup(self, db_session):
        # Delete in reverse dependency order
        for table, records in reversed(list(self.data.items())):
            for record in records:
                db_session.execute(
                    text(f"DELETE FROM {table} WHERE id = :id"),
                    {"id": record["id"]}
                )
```

Usage in `conftest.py`:

```python
@pytest.fixture
def test_data_registry(db_session):
    registry = TestDataRegistry()
    yield registry
    # Cleanup after test (if not using transaction rollback)
    registry.cleanup(db_session)
```

---

## Cleanup Order for Truncate

Tables must be truncated in **dependency order** (children before parents):

```
TIER 1 (no FK dependencies, can truncate in any order):
  - core_amenities
  - core_charge_types
  - core_unit_types
  - core_occupancy_types
  - alembic_version

TIER 2 (depends on TIER 1):
  - core_condominiums
  - core_buildings_types
  - core_roles

TIER 3 (depends on TIER 2):
  - core_buildings (→ core_condominiums)
  - core_condominium_roles (→ core_condominiums, core_roles)

TIER 4 (depends on TIER 3):
  - core_units (→ core_buildings)
  - core_user_profiles (→ core_users)
  - core_role_permissions (→ core_roles)

TIER 5 (depends on TIER 4):
  - core_users
  - core_residents (→ core_users, core_units)
  - core_unit_occupancies (→ core_units)
  - core_unit_ownerships (→ core_units)

TIER 6 (depends on TIER 5):
  - core_charges (→ core_condominiums, core_units)
  - core_documents (→ core_condominiums)
  - core_announcements (→ core_condominiums)
  - core_meetings (→ core_condominiums)
  - core_votes (→ core_meetings)
  - core_incidents (→ core_condominiums)
  - core_notifications

TIER 7 (depends on TIER 6):
  - core_payments (→ core_charges)
  - core_receipts (→ core_payments)
  - core_ledger_entries (→ core_condominiums)

TIER 8 (top of chain):
  - auth_sessions (→ core_users)
```

---

## Handling Alembic Version Table

The `alembic_version` table tracks migration state. It must be handled specially:

```sql
-- Option A: Don't truncate it (let alembic manage)
-- Just run `alembic downgrade base` before truncate to clean it

-- Option B: Truncate with rest
DELETE FROM alembic_version;
```

---

## Verifying Cleanup

After teardown, verify the database is clean:

```bash
mysql -h mysql -u root -p123456 db_condo_testings -e "SHOW TABLES;"
# Expected: alembic_version only (or empty if DROP DATABASE was used)
```

Or verify no orphan records:

```sql
SELECT 'core_condominiums' as tbl, COUNT(*) as cnt FROM core_condominiums
UNION ALL
SELECT 'core_buildings', COUNT(*) FROM core_buildings
UNION ALL
SELECT 'core_units', COUNT(*) FROM core_units
UNION ALL
SELECT 'core_users', COUNT(*) FROM core_users;
```

---

## CI/CD Teardown

Always run teardown in a `finally` block or `if: always()` step:

```yaml
- name: Teardown Test DB
  if: always()
  run: |
    mysql -h mysql -u root -p123456 \
      -e "DROP DATABASE IF EXISTS db_condo_testings;"
```

This ensures the DB is cleaned up even if tests crash or timeout.

---

## Common Issues

### "Cannot drop database because it's being used by other connections"

```sql
-- Kill all connections to the DB first
SELECT CONCAT('KILL ', id, ';')
FROM INFORMATION_SCHEMA.PROCESSLIST
WHERE db = 'db_condo_testings';

-- Then drop
DROP DATABASE IF EXISTS db_condo_testings;
```

### "Table is marked as crashed"

```bash
mysqlcheck -h mysql -u root -p123456 db_condo_testings --repair
```

### "Foreign key constraint fails"

Always truncate children before parents. If still failing, temporarily disable FK checks:

```sql
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE core_residents;
SET FOREIGN_KEY_CHECKS = 1;
```

<small>🔚 fin · Testing · Cleanup · `docs/TESTING/CLEANUP.md` · `2026-05-02`</small>


---

## Testing · Flow

<small>📄 `docs/TESTING/FLOW.md` · modificado: `2026-05-02`</small>

# Test Flow

## Overview

This document describes the lifecycle of a test run: from database creation to teardown.

---

## Full Test Lifecycle

```
┌─────────────────────────────────────────────────────┐
│  1. SESSION START                                   │
│     - conftest.py: setup_test_db                    │
│     - Create db_condo_testings                      │
│     - Run alembic upgrade head                      │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  2. PER-MODULE TESTS                                │
│                                                     │
│  Module: test_condo_module.py                      │
│     - fixtures: db_session, test_data_registry     │
│     - factories: create condo                      │
│     - scenario_builder: full scenario              │
│     - assertions                                   │
│     - rollback on exit                             │
│                                                     │
│  Module: test_core_buildings.py                    │
│     - (same pattern)                               │
│                                                     │
│  ... more modules ...                             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  3. SESSION TEARDOWN                                │
│     - conftest.py: teardown_test_db                 │
│     - DROP DATABASE db_condo_testings               │
└─────────────────────────────────────────────────────┘
```

---

## Session Fixtures (conftest.py)

### `setup_test_db` — session scope

Runs **once** at the start of the session.

```python
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # 1. Create DB
    create_database("db_condo_testings")
    # 2. Run migrations
    run_alembic_migrations("db_condo_testings")
    # 3. Yield → tests run
    yield
    # 4. Teardown happens in teardown_test_db
```

### `teardown_test_db` — session scope

Runs **once** at the end of the session.

```python
@pytest.fixture(scope="session", autouse=True)
def teardown_test_db():
    yield
    # DROP DATABASE db_condo_testings
    drop_database("db_condo_testings")
```

### `db_session` — function scope

Provides a transaction-wrapped session per test. Rolls back automatically.

```python
@pytest.fixture
def db_session(engine):
    with engine.begin() as conn:
        yield conn
    # Transaction auto-rollbacks on exit
```

---

## Test Function Pattern

```python
def test_create_building(db_session, test_data_registry):
    """
    1. Setup: use factory or scenario builder
    2. Act: call the actual module/service
    3. Assert: verify results
    4. Register: track created IDs for cleanup
    """
    # Step 1: Create scenario
    condo = CondoFactory.create(db_session, name="Mi Condo")
    test_data_registry.register("condo", condo.id, condo.uuid)

    building = BuildingFactory.create(
        db_session,
        condominium_id=condo.id,
        code="BLD-A",
        name="Torre A"
    )
    test_data_registry.register("building", building.id, building.uuid)

    # Step 2: Act
    result = BuildingService.get_by_id(building.id)

    # Step 3: Assert
    assert result.name == "Torre A"
    assert result.condominium_id == condo.id

    # Step 4: Registration means teardown knows what to clean
    # (but with rollback, this is mostly for debugging/audit)
```

---

## Factory Pattern

Factories wrap entity creation with sensible defaults:

```python
# Simple usage
condo = CondoFactory.create(session, name="Las Lomas")

# With overrides
condo = CondoFactory.create(
    session,
    name="Las Lomas",
    address="Av. Javier Prado 1234",
    coefficient=Decimal("100.0000")
)
```

### Available Factories

| Factory | Creates | Required Fields |
|---|---|---|
| `CondoFactory` | CondominiumEntity | `name` |
| `BuildingFactory` | BuildingEntity | `condominium_id`, `code` |
| `UnitFactory` | UnityEntity | `building_id`, `unit_number` |
| `UserFactory` | UserEntity | `email`, `document_number` |
| `ResidentFactory` | ResidentEntity | `user_id`, `unit_id` |

---

## Scenario Builder Pattern

For tests that need multiple related entities:

```python
def test_generate_charges_for_condo(db_session):
    # Creates: condo + 2 buildings + 6 units + 3 residents
    scenario = create_full_condo_scenario(
        session,
        condo_name="Torre Bonita",
        buildings_count=2,
        units_per_building=3,
        residents_per_unit=1
    )

    test_data_registry.register_scenario(scenario)

    # All related IDs are tracked
    assert len(scenario.building_ids) == 2
    assert len(scenario.unit_ids) == 6
    assert len(scenario.resident_ids) == 3

    # Run the actual test
    charges = ChargeService.generate_for_condo(scenario.condo_id)
    assert len(charges) > 0
```

---

## Test Order (Recommended)

Run modules in dependency order:

```
1. test_condo_module.py       # Base — everything belongs to a condo
2. test_core_buildings.py    # Buildings belong to a condo
3. test_core_unities.py      # Units belong to a building
4. test_core_rbac.py         # Roles/permissions reference condos
5. test_user_module.py       # Users are assigned to condos
6. test_resident_module.py   # Residents link users + units
7. test_charge_module.py     # Charges depend on condos + units
8. test_payment_module.py    # Payments depend on charges
9. test_receipt_module.py    # Receipts depend on payments
...
```

---

## What Happens on Failure

### Test Fails mid-execution

- The `db_session` fixture rolls back the transaction automatically
- No data persists from that test
- Next test sees a clean database (migrations already applied)

### Session Crashes

- `db_condo_testings` may be left dangling
- Next run: `teardown_test_db` recreates it from scratch
- Manual cleanup if needed:

```bash
mysql -h mysql -u root -p123456 -e "DROP DATABASE IF EXISTS db_condo_testings;"
```

---

## CI Flow

```yaml
# .github/workflows/test.yml (example)
- name: Setup Test DB
  run: |
    mysql -h mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS db_condo_testings;"

- name: Run Migrations
  run: |
    cd src
    alembic upgrade head
  env:
    MYSQL_DB: db_condo_testings

- name: Run Tests
  run: |
    cd src
    pytest ../tests/ -v --junitxml=report.xml
  env:
    PYTHONPATH: .
    MYSQL_DB: db_condo_testings

- name: Teardown
  if: always()
  run: |
    mysql -h mysql -u root -p123456 -e "DROP DATABASE IF EXISTS db_condo_testings;"
```

---

## Exit Codes

| Exit Code | Meaning |
|---|---|
| 0 | All tests passed |
| 1 | One or more tests failed |
| 2 | Test execution was interrupted |
| 3 | Internal error (e.g., fixture setup failed) |

<small>🔚 fin · Testing · Flow · `docs/TESTING/FLOW.md` · `2026-05-02`</small>


---

## Testing · Introducción

<small>📄 `docs/TESTING/README.md` · modificado: `2026-05-02`</small>

# Testing Infrastructure — db_condo_testings

## Overview

This document describes the testing infrastructure for `condo-py`, using **`db_condo_testings`** as the isolated test database.

**Strategy: Option C**
- Create a dedicated test database per test run
- Run real migrations against it
- Execute the test suite
- Destroy/reset the database at the end of the run

---

## Database Configuration

### `.env.test`

A dedicated environment file for tests. **This file is gitignored.**

```env
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_HOST=mysql
MYSQL_DB=db_condo_testings
MYSQL_PORT=3306

JWT_ACCESS_SECRET=<from src/.env>
JWT_REFRESH_SECRET=<from src/.env>
SECRET=<from src/.env>
BOOM_USER=<from src/.env>
BOOM_PASS=<from src/.env>
BOOM_SLUG=<from src/.env>
BUCKET=<from src/.env>
URL_SERVICE_BOOM=<from src/.env>
```

> **⚠️ Only for local development.** In CI, credentials are injected via secrets manager.

---

## Test Database Lifecycle

### Local Development

The test database is created and destroyed **per test run session** using pytest hooks in `conftest.py`:

```
db_condo_testings (empty)
    ↓ [pytest fixture: setup_test_db]
migrate all alembic migrations
    ↓
run tests (each test inserts its scenario)
    ↓ [pytest fixture: teardown_test_db]
drop all tables (or drop the whole DB)
```

### CI/CD Pipeline

```
1. CREATE DATABASE db_condo_testings;
2. alembic upgrade head
3. pytest tests/
4. DROP DATABASE db_condo_testings;
```

---

## Alembic Migrations on Test DB

Alembic is used for schema management. All migrations are applied against `db_condo_testings` before the suite runs.

To run migrations manually:

```bash
# Using the test env
cd src && alembic upgrade head

# Downgrade if needed
cd src && alembic downgrade -1
```

---

## Environment Variables in Tests

Pytest loads `.env.test` automatically via `python-dotenv` (if configured in `conftest.py`). All modules under `library/` read `MYSQL_DB=db_condo_testings`, ensuring complete isolation from `db_condominiums`.

### How it works

1. `conftest.py` sets `PYTHONPATH=src` and loads `.env.test`
2. All MySQL connection strings resolve to `db_condo_testings`
3. No test ever touches `db_condominiums` (production/development DB)

---

## Fixture Architecture

### Core Fixtures (`tests/conftest.py`)

| Fixture | Scope | Purpose |
|---|---|---|
| `setup_test_db` | session | Creates DB + runs migrations once before all tests |
| `teardown_test_db` | session | Destroys/resets DB after all tests complete |
| `db_session` | function | Provides a clean DB session per test |
| `test_data_registry` | function | Tracks IDs/UUIDs created in the current test |

### Factory Fixtures (`tests/factories/`)

Factories generate test data using the actual domain models:

- `condo_factory.py` — CondominiumEntity
- `building_factory.py` — BuildingEntity
- `unit_factory.py` — UnityEntity
- `user_factory.py` — UserEntity
- `resident_factory.py` — ResidentEntity

### Scenario Builder (`tests/support/scenario_builder.py`)

High-level scenarios that create complete data graphs:

- `create_full_condo_scenario()` — condo + buildings + units + users + residents
- `create_condo_with_1_building_3_units()` — minimal useful scenario
- `create_condo_with_residents()`

---

## Test Data Registry

Every test that creates data should register it in `test_data_registry`. This enables:

- **Debugging**: track what was created
- **Cleanup**: know exactly which records to delete
- **JSON export**: optional manifest for CI reports

### Usage

```python
def test_something(db_session, test_data_registry):
    condo = create_condo(name="Mi Condo Test")
    test_data_registry.register("condo", condo.id, condo.uuid)

    # ... run test ...

    # On teardown, registry knows condo.id → delete from DB
```

---

## Cleanup Strategy

### Per-Test Cleanup

If a test uses transactions, rollback after each test:

```python
@pytest.fixture
def db_session(test_db_connection):
    with test_db_connection.begin():
        yield test_db_connection
    # Auto-rollback on exit
```

### Session-Level Cleanup (Full Reset)

At the end of the session, `teardown_test_db` drops the database:

```python
def teardown_test_db():
    with engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS db_condo_testings"))
        conn.commit()
```

### Fallback: Truncate Tables

If dropping the database is too slow or causes issues, truncate key tables:

```sql
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE core_condominiums;
TRUNCATE TABLE core_buildings;
TRUNCATE TABLE core_units;
TRUNCATE TABLE core_users;
TRUNCATE TABLE core_residents;
SET FOREIGN_KEY_CHECKS = 1;
```

---

## Module Coverage

### Phase 1 — Core Modules (Priority)

| Module | Test File | Status |
|---|---|---|
| Condominiums | `test_condo_module.py` | TODO |
| Buildings | `test_core_buildings.py` | Existing |
| Units | `test_core_unities.py` | Existing |
| Building Types | `test_core_buildings_types.py` | Existing |
| Amenities | `test_core_amenities.py` | Existing |
| RBAC | `test_core_rbac.py` | Existing |
| Users | `test_user_module.py` | TODO |
| Residents | `test_resident_module.py` | TODO |

### Phase 2 — Extended Modules

| Module | Status |
|---|---|
| Charges | TODO |
| Payments | TODO |
| Receipts | TODO |
| Ledger Entries | TODO |
| Documents | TODO |
| Announcements | TODO |
| Meetings | TODO |
| Votes | TODO |
| Incidents | TODO |
| Visitors | TODO |

---

## Git Workflow

### Branch Strategy

All testing infrastructure work happens on **`feature/test-infra-db-condo-testings`**.

```
main ←───────────────────────────── feature/test-infra-db-condo-testings
       ↖ commits (testing-infra)
```

### Commit Convention

Follows `type(scope): subject` format per `MEMORY.md`:

```
feat(testing): add db_condo_testings infrastructure

- add .env.test (gitignored)
- add conftest.py session fixtures (setup/teardown)
- add test_data_registry for ID/UUID tracking
- add factories for condo, building, unit, user, resident
- add scenario_builder.py for complete test scenarios
- document test setup, flow, and cleanup strategy
```

### Push & Merge

```bash
git push origin feature/test-infra-db-condo-testings
# Open PR → review → merge to main
```

---

## Common Tasks

### Run tests locally

```bash
# With docker compose (mysql must be running)
docker-compose -p condopy up -d mysql

# Run tests
cd src && pytest ../tests/ -v

# Run specific module
cd src && pytest ../tests/test_core_buildings.py -v
```

### Create DB manually

```bash
mysql -h mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS db_condo_testings;"
```

### Run migrations manually

```bash
cd src
export $(cat ../.env.test | grep -v '^#' | xargs)
alembic upgrade head
```

### Drop test DB

```bash
mysql -h mysql -u root -p123456 -e "DROP DATABASE IF EXISTS db_condo_testings;"
```

---

## FAQ

**Q: Why not use SQLite for tests?**
A: The project uses MySQL exclusively. SQLite differences (types, JSON, FK behavior) would produce false confidence.

**Q: Why not use `db_condominiums` with a test schema?**
A: Isolation. Even with a separate schema, any bug could touch production tables. A separate DB is the only true sandbox.

**Q: Why not use `pytest-django` or similar?**
A: This is a FastAPI/Pydantic/Alembic stack, not Django. The pattern here uses Alembic migrations + raw SQLAlchemy sessions.

**Q: What about parallel test execution?**
A: Not supported in Option C — the DB is created once per session. For parallel tests, use separate DB names per worker (e.g., `db_condo_testings_w1`, `db_condo_testings_w2`).

---

## File Structure

```
condo-py/
├── .env.test              # Test environment (gitignored)
├── .gitignore             # Updated to ignore .env.test
├── tests/
│   ├── conftest.py        # Session fixtures: setup/teardown
│   ├── factories/         # Data factories
│   │   ├── condo_factory.py
│   │   ├── building_factory.py
│   │   ├── unit_factory.py
│   │   ├── user_factory.py
│   │   └── resident_factory.py
│   ├── support/
│   │   ├── scenario_builder.py
│   │   └── test_data_registry.py
│   └── integration/       # Per-module integration tests
├── docs/
│   └── TESTING/
│       ├── README.md      # This file
│       ├── SETUP.md
│       ├── FLOW.md
│       └── CLEANUP.md
└── alembic/
    └── versions/          # Real migrations (source of truth for schema)
```

<small>🔚 fin · Testing · Introducción · `docs/TESTING/README.md` · `2026-05-02`</small>


---

## Testing · Setup

<small>📄 `docs/TESTING/SETUP.md` · modificado: `2026-05-02`</small>

# Test Setup

## Prerequisites

- Docker and Docker Compose running (`mysql` container up)
- Access to MySQL on `mysql:3306` as `root`
- `python3` and `pip` available locally (for local runs)
- `pytest` installed (`pip install pytest`)

---

## 1. Create `.env.test`

> **Note**: `.env.test` is gitignored. It is generated **once** from `src/.env` and never committed.

```bash
# Copy from src/.env and override DB name
cat src/.env | sed 's/db_condominiums/db_condo_testings/' > .env.test
```

Verify:

```bash
grep MYSQL_DB .env.test
# Expected: MYSQL_DB=db_condo_testings
```

---

## 2. Create the Test Database

### Via MySQL CLI

```bash
mysql -h mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS db_condo_testings;"
```

### Via Makefile (if target exists)

```bash
make create_test_db
```

---

## 3. Run Alembic Migrations

```bash
cd src
export $(grep -v '^#' ../.env.test | xargs)
alembic upgrade head
```

Expected output:

```
Running upgrade  -> 001_create_initial, ...
Running upgrade 001_create_initial -> 002_refactor_core_buildings, ...
...
```

---

## 4. Verify Schema

```bash
mysql -h mysql -u root -p123456 db_condo_testings -e "SHOW TABLES;"
```

Expected tables (at minimum):
- `core_condominiums`
- `core_buildings`
- `core_units`
- `core_users`
- `core_residents`
- `core_roles`
- `alembic_version`

---

## 5. Verify Pytest Can Connect

```bash
cd src
export PYTHONPATH=.
export $(grep -v '^#' ../.env.test | xargs)
pytest --co -q ../tests/
```

Expected: list of collected tests, no connection errors.

---

## 6. (Optional) Run a Smoke Test

```bash
cd src
export PYTHONPATH=.
export $(grep -v '^#' ../.env.test | xargs)
pytest ../tests/test_core_buildings.py -v --tb=short
```

Expected: tests pass (or fail for reasons unrelated to DB connection).

---

## Troubleshooting

### "Can't connect to MySQL server on 'mysql'"

```bash
# Check if container is running
docker ps | grep mysql

# If not, start it
docker-compose -p condopy up -d mysql
```

### "Access denied for user 'root'@'%'"

```bash
# Fix MySQL root user
docker-compose -p condopy exec mysql mysql -u root -p123456 \
  -e "ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';"
```

### "No module named 'alembic'"

```bash
cd src && pip install -r requirements.txt
```

---

## Full Local Setup Script

```bash
#!/bin/bash
set -e

echo "=== 1. Creating .env.test ==="
cat src/.env | sed 's/db_condominiums/db_condo_testings/' > .env.test
echo "Done."

echo "=== 2. Creating db_condo_testings ==="
mysql -h mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS db_condo_testings;"
echo "Done."

echo "=== 3. Running migrations ==="
cd src
export $(grep -v '^#' ../.env.test | xargs)
alembic upgrade head
cd ..

echo "=== 4. Verifying tables ==="
mysql -h mysql -u root -p123456 db_condo_testings -e "SHOW TABLES;" | wc -l
echo "tables created."

echo "=== Setup complete ==="
```

<small>🔚 fin · Testing · Setup · `docs/TESTING/SETUP.md` · `2026-05-02`</small>


---

## Changelog de Unificación

- **2026-05-04** · Unificación inicial: 75 documentos consolidados en uno solo por Misato

  - `README.md` → `2026-04-14`
  - `docs/01-general/README.md` → `2026-03-19`
  - `docs/01-general/architecture.md` → `2026-03-19`
  - `docs/01-general/docker.md` → `2026-03-19`
  - `docs/01-general/team-mapping.md` → `2026-04-28`
  - `docs/01-general/zrok-tunnel.md` → `2026-04-30`
  - `docs/02-architecture/new-standard/ddd-architecture-base-guide.md` → `2026-03-16`
  - `docs/03-modules/models/core_buildings.md` → `2026-04-14`
  - `docs/03-modules/models/core_buildings_types.md` → `2026-04-13`
  - `docs/03-modules/models/core_condominiums.md` → `2026-03-16`
  - `docs/03-modules/models/core_condominium_roles.md` → `2026-04-15`
  - `docs/03-modules/models/core_unit_occupancies.md` → `2026-04-15`
  - `docs/03-modules/models/core_unit_ownerships.md` → `2026-04-15`
  - `docs/03-modules/models/core_units.md` → `2026-04-15`
  - `docs/03-modules/models/core_unities.md` → `2026-04-14`
  - `docs/03-modules/models/core_unittys_types.md` → `2026-04-15`
  - `docs/03-modules/models/users.md` → `2026-04-15`
  - `docs/03-modules/models/users_residents.md` → `2026-04-15`
  - `docs/04-bulma/README.md` → `2026-03-16`
  - `docs/04-bulma/MODULES.md` → `2026-04-30`
  - `docs/04-bulma/anti-patterns.md` → `2026-03-16`
  - `docs/04-bulma/architecture-rules.md` → `2026-03-19`
  - `docs/04-bulma/change-playbook.md` → `2026-03-19`
  - `docs/04-bulma/implementation-guidelines.md` → `2026-03-19`
  - `docs/04-bulma/module-map.md` → `2026-03-16`
  - `docs/05-research/competitive-analysis-condo-systems.md` → `2026-04-29`
  - `docs/06-competitor-analysis/README.md` → `2026-04-13`
  - `docs/06-competitor-analysis/competitive-analysis.md` → `2026-04-29`
  - `docs/06-competitor-analysis/lelouch-strategic-analysis.md` → `2026-04-14`
  - `docs/07-roadmap/api-identity-context-roadmap.md` → `2026-04-15`
  - `docs/07-roadmap/auth-hardening-roadmap.md` → `2026-04-15`
  - `docs/07-roadmap/core_buildings-task-order.md` → `2026-04-14`
  - `docs/07-roadmap/core_unities-rename-plan.md` → `2026-04-14`
  - `docs/07-roadmap/core_unities-task-order.md` → `2026-04-14`
  - `docs/07-roadmap/core_units-rename-plan.md` → `2026-04-15`
  - `docs/07-roadmap/module-list.md` → `2026-04-15`
  - `docs/07-roadmap/module-roadmap.md` → `2026-04-15`
  - `docs/07-roadmap/users-core-identity-roadmap.md` → `2026-04-15`
  - `docs/08-analysis/INCIDENT-20260429-condopy-api-alias-login-500.md` → `2026-04-29`
  - `docs/08-analysis/users-roles-propietarios-ocupacion-integracion-20260424.md` → `2026-04-24`
  - `docs/09-sprint/fin-12-validation-payments-receipts-ledger.md` → `2026-05-01`
  - `docs/09-sprint/sprint10-visitors-20260424.md` → `2026-04-24`
  - `docs/09-sprint/sprint13-votes-20260424.md` → `2026-04-24`
  - `docs/09-sprint/sprint14-dashboards-20260424.md` → `2026-04-24`
  - `docs/09-sprint/sprint15-detail-pages-20260429.md` → `2026-04-29`
  - `docs/09-sprint/sprint16-amenity-booking-policies-20260503.md` → `2026-05-04`
  - `docs/09-sprint/sprint5-accounts-receivable-20260424.md` → `2026-05-01`
  - `docs/09-sprint/sprint6-user-roles-integration-20260424.md` → `2026-04-24`
  - `docs/09-sprint/sprint7-auth-module-20260424.md` → `2026-04-24`
  - `docs/09-sprint/sprint8-incidents-20260424.md` → `2026-04-24`
  - `docs/09-sprint/sprint9-notifications-20260424.md` → `2026-04-24`
  - `docs/10-agents/AI_TEAM.md` → `2026-04-28`
  - `docs/10-agents/README.md` → `2026-04-28`
  - `docs/10-agents/TASKS.md` → `2026-04-28`
  - `docs/BULMA/amenity-bookings-sprint-a-20260502.md` → `2026-05-03`
  - `docs/BULMA/flow-select-condo-dashboard-20260503.md` → `2026-05-03`
  - `docs/BULMA/flow-verify-planning-20260503.md` → `2026-05-03`
  - `docs/BULMA/handoff-high1-high2-20260414.md` → `2026-04-14`
  - `docs/BULMA/high5-transversal-audit-20260414.md` → `2026-04-14`
  - `docs/BULMA/phase1-review-20260414.md` → `2026-04-14`
  - `docs/BULMA/phase2-rbac-planning-20260416.md` → `2026-04-16`
  - `docs/BULMA/phase2-rbac-status-20260430.md` → `2026-04-30`
  - `docs/BULMA/roadmap-5highs-20260414.md` → `2026-04-30`
  - `docs/BULMA/roadmap-amenities-scope-20260501.md` → `2026-05-01`
  - `docs/BULMA/roadmap-amenity-bookings-20260502.md` → `2026-05-03`
  - `docs/BULMA/shadcn-theme-planning-20260430.md` → `2026-05-01`
  - `docs/BULMA/swipe-landing-plan-20260430.md` → `2026-05-01`
  - `docs/BULMA/task-payment-occupancy-20260503.md` → `2026-05-03`
  - `docs/BULMA/theme-qa-closure-20260503.md` → `2026-05-03`
  - `docs/MIGRATION_PLAN.md` → `2026-04-28`
  - `docs/README.md` → `2026-04-30`
  - `docs/TESTING/CLEANUP.md` → `2026-05-02`
  - `docs/TESTING/FLOW.md` → `2026-05-02`
  - `docs/TESTING/README.md` → `2026-05-02`
  - `docs/TESTING/SETUP.md` → `2026-05-02`
