# Guía de Arquitectura de `condo-py`

> **Proyecto:** `condo-py`
>
> **Framework HTTP:** AWS Chalice
>
> **Persistencia:** SQLAlchemy + MySQL
>
> **Validación:** Pydantic
>
> **Testing:** Pytest
>
> **Objetivo del documento:** definir la arquitectura vigente del proyecto y establecer el estándar que debe seguir **BULMA** al crear o ampliar módulos.

---

## 1. Principio rector

La fuente de verdad de esta arquitectura es el **código Python actual** del proyecto.

Este documento no describe una migración, ni una arquitectura heredada, ni referencias externas. Describe el tablero real de `condo-py` hoy:

- backend en Python
- endpoints en Chalice
- persistencia con SQLAlchemy
- módulos en `src/chalicelib/dddpy/`
- separación por capas con convención DDD/CQRS modular

---

## 2. Visión general de la arquitectura

La arquitectura actual puede resumirse así:

```text
HTTP / Chalice
  → API routes
  → Schemas Pydantic
  → Use cases
  → Repositories
  → SQLAlchemy
  → Base de datos
```

Y a nivel organizacional:

```text
src/
├── app.py
├── chalicelib/
│   ├── api/
│   └── dddpy/
└── tests/
```

### Patrones presentes

| Patrón | Uso actual |
|---|---|
| DDD | estructura por módulos de dominio |
| CQRS | separación básica entre command/query |
| Repository Pattern | abstracción de acceso a datos |
| Factory Pattern | construcción de use cases |
| Layered Architecture | separación API / usecase / domain / infrastructure |

### Lectura honesta
La implementación actual es **DDD/CQRS en evolución**. La estructura ya existe, pero el dominio aún no está completamente desacoplado ni enriquecido.

---

## 3. Estructura real del proyecto

```text
condo-py/
├── README.md
├── Makefile
├── docker-compose.yml
├── docker/
├── documentation/
│   ├── architecture.md
│   └── docker.md
├── dbs/
└── src/
    ├── .chalice/
    ├── alembic/
    ├── app.py
    ├── requirements.txt
    ├── chalicelib/
    │   ├── api/
    │   │   ├── buildings/
    │   │   ├── buildings_types/
    │   │   ├── condominiums/
    │   │   ├── residents/
    │   │   ├── unittys_types/
    │   │   ├── unitys/
    │   │   └── users/
    │   └── dddpy/
    │       ├── core_buildings/
    │       ├── core_buildings_types/
    │       ├── core_condominiums/
    │       ├── core_unittys_types/
    │       ├── core_unitys/
    │       ├── users/
    │       ├── users_residents/
    │       └── shared/
    └── tests/
        ├── core_buildings/
        ├── core_buildings_types/
        ├── core_condominiums/
        ├── core_unittys_types/
        ├── core_unitys/
        ├── users/
        └── users_residents/
```

---

## 4. Módulos vigentes en `dddpy`

| Módulo | Responsabilidad actual |
|---|---|
| `core_condominiums` | gestión base de condominios |
| `core_buildings` | gestión de edificios/bloques |
| `core_buildings_types` | catálogo de tipos de edificio |
| `core_unitys` | gestión de unidades |
| `core_unittys_types` | catálogo de tipos de unidad |
| `users` | gestión de usuarios |
| `users_residents` | relación y gestión de residentes |
| `shared` | piezas transversales reutilizables |

### Observación importante
La modularidad actual sigue más una lógica de **entidades persistidas** que de bounded contexts maduros. Eso es aceptable por ahora, pero debe considerarse una etapa intermedia.

---

## 5. Estructura estándar de un módulo

Todo módulo funcional en `src/chalicelib/dddpy/{modulo}` debe seguir esta plantilla:

```text
{modulo}/
├── domain/
│   ├── {modulo}.py
│   ├── {modulo}_exception.py
│   ├── {modulo}_repository.py
│   └── {modulo}_success.py
├── infrastructure/
│   ├── {modulo}.py
│   ├── {modulo}_cmd_repository.py
│   └── {modulo}_query_repository.py
└── usecase/
    ├── {modulo}_cmd_schema.py
    ├── {modulo}_query_schema.py
    ├── {modulo}_cmd_usecase.py
    ├── {modulo}_query_usecase.py
    ├── {modulo}_factory.py
    └── {modulo}_usecase.py
```

Además, debe existir una capa HTTP asociada en:

```text
src/chalicelib/api/{ruta_modulo}/routes_{ruta_modulo}.py
```

Y su suite de pruebas en:

```text
src/tests/{modulo}/
```

---

## 6. Responsabilidad por capa

## 6.1 `api/`
Responsabilidades:
- exponer endpoints Chalice
- tomar `current_request`
- validar body/query params con Pydantic
- invocar casos de uso
- construir `Response`

No debe contener:
- lógica de negocio compleja
- acceso directo a ORM
- reglas transaccionales de negocio

### Ejemplo real
`src/chalicelib/api/users/routes_users.py`

Patrón observado:
- health check
- CRUD HTTP
- uso de `@api_handler`
- parseo con `CreateUserSchema` y `UpdateUserSchema`
- delegación a `UsersUseCase`

---

## 6.2 `domain/`
Responsabilidades:
- entidades del negocio
- contratos de repositorio
- excepciones semánticas
- mensajes de éxito

Debe tender a contener:
- invariantes
- comportamiento del dominio
- reglas del negocio

### Estado actual
Hoy algunas entidades del dominio todavía dependen de infraestructura, por ejemplo importando modelos ORM para `from_db(...)`.

Eso debe considerarse **deuda técnica existente**, no estándar de diseño para módulos nuevos.

### Regla futura obligatoria
Los nuevos módulos deben tener un dominio **independiente del ORM**.

---

## 6.3 `infrastructure/`
Responsabilidades:
- modelos SQLAlchemy
- repositorios concretos
- persistencia
- consultas a DB
- mapeo DB ↔ dominio

Aquí vive el detalle técnico de almacenamiento. La base de datos no debe imponer la forma del dominio; solo persistirlo.

---

## 6.4 `usecase/`
Responsabilidades:
- orquestación de aplicación
- separación command/query
- coordinación de repositorios
- respuestas consistentes para API

En la práctica actual, `usecase/` funciona como capa de **aplicación**.

### Patrón habitual
- `*_cmd_usecase.py` → escritura
- `*_query_usecase.py` → lectura
- `*_factory.py` → inyección de dependencias
- `*_usecase.py` → fachada unificada del módulo

---

## 6.5 `shared/`
Contiene componentes reutilizables para todos los módulos.

Estructura detectada:

```text
src/chalicelib/dddpy/shared/
├── decorators/
├── logging/
├── mysql/
├── postgresql/
├── schemas/
├── utils/
└── timezone.py
```

Responsabilidades actuales:
- decorators de API y excepciones
- logger personalizado
- manejo de sesiones MySQL/PostgreSQL
- schemas de respuesta
- helpers de utilería

---

## 7. Flujo completo de una solicitud

Flujo típico real del sistema:

```text
Request HTTP
  → route de Chalice
  → @api_handler
  → schema Pydantic
  → UseCase unificado
  → Command o Query UseCase
  → Repository interface
  → Repository implementation
  → SQLAlchemy model
  → DB
  → entidad / response schema
  → Response HTTP
```

### Ejemplo real simplificado: `users`

```text
GET /users
  → api/users/routes_users.py
  → UsersUseCase.get_all()
  → UsersQueryUseCase
  → UsersQueryRepositoryImpl
  → DBUsers
  → Users
  → Response(status_code=200, body=...)
```

---

## 8. Ejemplo práctico: módulo `users`

El módulo `users` hoy es la mejor referencia estructural porque contiene el ciclo completo.

### Archivos clave

```text
users/
├── domain/
│   ├── users.py
│   ├── users_exception.py
│   ├── users_repository.py
│   └── users_success.py
├── infrastructure/
│   ├── users.py
│   ├── users_cmd_repository.py
│   └── users_query_repository.py
└── usecase/
    ├── users_cmd_schema.py
    ├── users_cmd_usecase.py
    ├── users_factory.py
    ├── users_query_usecase.py
    └── users_usecase.py
```

### Qué muestra bien este módulo
- naming consistente
- separación de capas
- uso de factories
- repositorios command/query
- schema Pydantic para create/update
- use case fachada

### Qué no debe copiarse ciegamente
- `domain/users.py` importando `DBUsers`
- `raise Exception("User not found")` en repositorios
- commits redundantes dentro del contexto transaccional
- entidad demasiado anémica

El módulo `users` es el peón de referencia para la forma. No necesariamente para la pureza arquitectónica.

---

## 9. Estado real del DDD en el proyecto

## 9.1 Lo que sí existe
- módulos por dominio/entidad
- capa API separada
- capa de aplicación (`usecase`) separada
- contratos de repositorio
- implementaciones de infraestructura
- excepciones de dominio por módulo
- tests por módulo

## 9.2 Lo que aún falta para DDD más sólido
- dominio rico con comportamiento
- value objects
- aggregates bien definidos
- mappers fuera del dominio
- bounded contexts más claros
- mejor separación entre application y domain

## 9.3 Diagnóstico breve
Esto es hoy:

> **estructura DDD/CQRS funcional, pero aún con dominio anémico y acoplamiento residual a infraestructura.**

---

## 10. CQRS: cómo entenderlo aquí

El proyecto usa CQRS de manera práctica, no doctrinaria.

### Lo que sí significa aquí
- separar escritura y lectura en clases distintas
- usar repositorios distintos para comandos y consultas
- mantener intención semántica clara

### Lo que no significa todavía
- read models especializados por proyección
- stores separados
- event sourcing
- pipelines complejos de sincronización

### Regla para BULMA
Mantener la separación command/query cuando aporte claridad, pero sin crear complejidad ceremonial.

---

## 11. Shared: componentes importantes

## 11.1 `api_handler`
Ubicación:
- `src/chalicelib/dddpy/shared/decorators/api_handler.py`

Responsabilidad:
- envolver rutas
- capturar `DomainException`
- capturar `ValidationError`
- devolver errores HTTP homogéneos
- registrar trazas y contexto del request

Es la primera línea defensiva del borde HTTP.

---

## 11.2 `DomainException`
Ubicación:
- `src/chalicelib/dddpy/shared/decorators/domain_exception.py`

Contrato actual:
```python
class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
```

Regla:
- toda excepción semántica del negocio debe heredar de esta clase

---

## 11.3 `session_scope()`
Ubicación:
- `src/chalicelib/dddpy/shared/mysql/session_manager.py`

Función:
- abrir sesión
- hacer commit al finalizar
- hacer rollback ante error
- cerrar sesión siempre

### Recomendación arquitectónica
Si `session_scope()` ya controla commit/rollback, los repositorios no deberían duplicar `session.commit()` salvo necesidad muy justificada.

---

## 11.4 `ResponseSuccessSchema` y `ResponseErrorSchema`
Ubicación:
- `src/chalicelib/dddpy/shared/schemas/response_schema.py`

Se usan para homogenizar respuestas desde los casos de uso y la capa API.

---

## 12. Normas obligatorias para nuevos módulos

## 12.1 Estructura mínima
Todo módulo nuevo debe incluir:
- carpeta en `dddpy/`
- carpeta API correspondiente
- carpeta de tests correspondiente
- contratos de repositorio
- schemas Pydantic
- excepciones del módulo
- use cases de command/query

## 12.2 Independencia del dominio
No hacer en módulos nuevos:
- importar modelos SQLAlchemy en `domain/`
- usar entidades ORM como tipo del dominio

Sí hacer:
- entidades puras
- mappers o adapters en infraestructura
- traducción explícita DB ↔ dominio

## 12.3 Excepciones específicas
No usar:
```python
raise Exception("...")
```

Sí usar:
- `MiModuloNotFoundException`
- `MiModuloValidationException`
- `MiModuloAlreadyExistsException`

## 12.4 Control transaccional consistente
Preferencia del proyecto a futuro:
- `session_scope()` gobierna la transacción
- repositorios hacen `add`, `flush`, `refresh` cuando aplique
- evitar commits duplicados

## 12.5 Validación por capas
- Pydantic valida estructura/formato
- dominio valida reglas e invariantes
- repositorio persiste

## 12.6 Testing mínimo obligatorio
Cada módulo nuevo debe tener al menos:
- test de entidad
- test de excepciones
- test de `to_dict()` o serialización
- test de caso de uso principal

---

## 13. Contrato de desarrollo para BULMA

Cuando BULMA cree un módulo, debe entregar como mínimo:

### Dominio
- entidad principal
- excepciones
- mensajes de éxito
- contratos de repositorio

### Aplicación
- command schema
- query schema si aplica
- command use case
- query use case
- factory
- use case fachada

### Infraestructura
- modelo SQLAlchemy
- repositorio de escritura
- repositorio de lectura
- mapper si se usa dominio puro

### API
- blueprint
- health endpoint
- endpoints del módulo
- responses homogéneas

### Testing
- suite mínima del módulo
- pruebas ejecutables con Pytest

---

## 14. Plantilla recomendada para un módulo nuevo

```text
src/chalicelib/dddpy/mi_modulo/
├── domain/
│   ├── mi_modulo.py
│   ├── mi_modulo_exception.py
│   ├── mi_modulo_repository.py
│   └── mi_modulo_success.py
├── infrastructure/
│   ├── mi_modulo.py
│   ├── mi_modulo_cmd_repository.py
│   ├── mi_modulo_query_repository.py
│   └── mappers.py
└── usecase/
    ├── mi_modulo_cmd_schema.py
    ├── mi_modulo_query_schema.py
    ├── mi_modulo_cmd_usecase.py
    ├── mi_modulo_query_usecase.py
    ├── mi_modulo_factory.py
    └── mi_modulo_usecase.py
```

Y su capa HTTP:

```text
src/chalicelib/api/mi_modulo/routes_mi_modulo.py
```

Y sus pruebas:

```text
src/tests/mi_modulo/
```

---

## 15. Ejemplo de secuencia para crear un módulo

1. definir el lenguaje ubicuo del módulo
2. modelar la entidad principal
3. crear excepciones semánticas
4. definir interfaces de repositorio
5. crear modelo SQLAlchemy
6. implementar repositorios cmd/query
7. crear schemas Pydantic
8. implementar casos de uso
9. exponer rutas Chalice
10. escribir tests
11. validar consistencia con módulos existentes

---

## 16. Deuda técnica conocida

Estas son piezas reales a mejorar en refactors futuros:

- dominio acoplado a infraestructura en varios módulos
- entidades anémicas
- `Exception(...)` genérica en repositorios
- commits duplicados
- middleware HTTP con puntos a endurecer
- naming mejorable en algunos módulos (`unitys`, `unittys`)
- bounded contexts todavía inmaduros

Esta deuda debe reconocerse, no copiarse.

---

## 17. Dirección arquitectónica recomendada

A mediano plazo, la evolución correcta sería:

- pasar de módulos por tabla a módulos por capacidad de negocio
- enriquecer el dominio con comportamiento
- introducir value objects
- definir aggregate roots
- separar más claramente application/domain/infrastructure
- usar mappers explícitos

Ejemplos de bounded contexts futuros más sanos:
- `identity`
- `property_structure`
- `residency`
- `billing`
- `communications`
- `security`

---

## 18. Resumen ejecutivo

`condo-py` ya tiene una base modular coherente y reutilizable.

La regla maestra para futuros desarrollos es esta:

> **copiar la convención estructural actual, pero no heredar sus defectos.**

O dicho con crudeza imperial:

> el tablero ya existe; ahora toca dejar de obedecer a la base de datos y hacer que el dominio gobierne el reino.
