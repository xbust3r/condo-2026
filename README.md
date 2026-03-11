# condo-py — Sistema de Gestión para Condominios

> **Estado del proyecto:** backend Python funcional en evolución
>
> **Arquitectura actual:** Chalice + SQLAlchemy + Pydantic + estructura DDD/CQRS modular
>
> **Objetivo de este README:** servir como mapa técnico para que **BULMA** desarrolle nuevos módulos siguiendo el patrón real del proyecto, no referencias heredadas.

---

## 1. Visión general

`condo-py` es un backend para gestión de condominios. Actualmente expone endpoints HTTP mediante **AWS Chalice**, usa **SQLAlchemy** para persistencia y organiza el código de negocio bajo `src/chalicelib/dddpy/` con una convención repetible por módulo.

El proyecto ya tiene una base modular consistente y tests automatizados. Sin embargo, la implementación actual debe entenderse como:

- **DDD/CQRS en transición**, no una implementación purista
- **modular CRUD bien estructurado**, con espacio claro de mejora hacia dominio rico
- una base válida para construir nuevos módulos si se respeta un estándar técnico común

---

## 2. Stack tecnológico actual

### Backend
- **Python**
- **AWS Chalice** como framework HTTP/API
- **SQLAlchemy** como ORM
- **Pydantic** para validación de entrada/salida
- **Pytest** para pruebas
- **Alembic** para migraciones
- **Docker / docker-compose** para entorno local

### Estructura del proyecto
- `src/app.py` → entry point de Chalice
- `src/chalicelib/api/` → rutas HTTP por módulo
- `src/chalicelib/dddpy/` → módulos de dominio/aplicación/infrastructura
- `src/tests/` → pruebas por módulo
- `documentation/` → notas y guías técnicas complementarias

---

## 3. Estructura real del proyecto

```text
condo-py/
├── README.md
├── Makefile
├── docker-compose.yml
├── docker/
├── documentation/
├── dbs/
└── src/
    ├── app.py
    ├── alembic/
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

## 4. Módulos actuales en `dddpy`

Estos son los módulos reales detectados en el código fuente.

| Módulo | Propósito actual | API expuesta | Estado |
|---|---|---|---|
| `core_condominiums` | Gestión base del condominio | Sí | Activo |
| `core_buildings` | Gestión de edificios/bloques | Sí | Activo |
| `core_buildings_types` | Catálogo de tipos de edificio | Sí | Activo |
| `core_unitys` | Gestión de unidades | Sí | Activo |
| `core_unittys_types` | Catálogo de tipos de unidad | Sí | Activo |
| `users` | Gestión de usuarios | Sí | Activo |
| `users_residents` | Relación / gestión de residentes | Sí | Activo |
| `shared` | utilidades transversales | No aplica | Activo |

### Observaciones de arquitectura
- Los módulos siguen una **plantilla consistente**, útil para replicar nuevos desarrollos.
- La separación actual es principalmente por **entidad/tablas**, no todavía por bounded context maduro.
- Existe convención de **comandos y queries separados**, aunque el CQRS todavía es liviano.

---

## 5. Patrón de módulo que BULMA debe seguir

Cada módulo en `src/chalicelib/dddpy/{modulo}` sigue esta estructura:

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
    ├── {modulo}_cmd_usecase.py
    ├── {modulo}_factory.py
    ├── {modulo}_query_schema.py
    ├── {modulo}_query_usecase.py
    └── {modulo}_usecase.py
```

Y normalmente existe una ruta HTTP asociada en:

```text
src/chalicelib/api/{ruta_modulo}/routes_{ruta_modulo}.py
```

---

## 6. Responsabilidad de cada capa

### `api/`
Responsable de:
- declarar rutas Chalice
- recibir request HTTP
- validar payload con schemas
- invocar casos de uso
- transformar respuesta a `Response`

No debería contener:
- reglas de negocio complejas
- acceso directo a base de datos
- lógica transaccional relevante

### `domain/`
Responsable de:
- entidades del negocio
- contratos de repositorio
- excepciones de dominio
- mensajes semánticos de éxito

**Importante:**
Aunque hoy algunos módulos mezclan dominio con infraestructura, **los nuevos módulos no deben repetir ese error**. El dominio debe ser independiente del ORM y de Chalice.

### `infrastructure/`
Responsable de:
- modelos SQLAlchemy
- implementación de repositorios
- persistencia
- mapeo entre DB y dominio

### `usecase/`
Responsable de:
- orquestar casos de uso
- coordinar repositorios
- separar comandos y consultas
- devolver respuestas consistentes a la capa API

### `shared/`
Responsable de piezas transversales como:
- logging
- manejo de sesiones DB
- decorators
- schemas de respuesta
- utilidades comunes

---

## 7. Flujo actual por request

El flujo operativo típico es este:

```text
HTTP Request
  → api/routes_*.py
  → schema Pydantic
  → *UseCase
  → repository interface
  → repository implementation
  → SQLAlchemy model / DB
  → respuesta serializada
```

Ejemplo real simplificado:

```text
GET /users
  → chalicelib/api/users/routes_users.py
  → UsersUseCase().get_all()
  → UsersQueryUseCase
  → UsersQueryRepositoryImpl
  → DBUsers
  → Users
  → Response
```

---

## 8. Diagnóstico arquitectónico actual

La arquitectura es útil, pero debe entenderse con precisión para no propagar defectos.

### Fortalezas
- estructura modular consistente
- separación básica entre API / use case / repository / ORM
- convención repetible entre módulos
- tests ya existentes por módulo
- buena base para estandarizar desarrollo futuro

### Debilidades actuales
- algunas entidades de `domain/` importan modelos de `infrastructure/`
- el dominio es todavía **anémico**: tiene pocos comportamientos de negocio
- hay `Exception(...)` genéricas en repositorios
- hay `session.commit()` duplicado dentro de repositorios y `session_scope()`
- la separación CQRS existe a nivel de archivos, pero aún no como lectura/escritura verdaderamente especializadas
- hay detalles operativos por endurecer en seguridad y middleware

### Conclusión práctica
Para BULMA, la consigna es clara:

> **replicar la convención estructural actual, pero corrigiendo las malas prácticas detectadas.**

No copiar defectos. Copiar el patrón útil.

---

## 9. Reglas para desarrollar nuevos módulos

### Regla 1 — Mantener el mismo esqueleto
Todo nuevo módulo debe crear:
- `domain/`
- `infrastructure/`
- `usecase/`
- su ruta correspondiente en `api/`
- su suite de tests en `src/tests/`

### Regla 2 — El dominio no depende de infraestructura
No hacer esto en nuevos módulos:
- importar modelos SQLAlchemy dentro de `domain/`
- usar clases DB como tipo del dominio

Preferir:
- entidades puras
- mappers en infraestructura
- repositorios que traduzcan DB ↔ dominio

### Regla 3 — Excepciones específicas
No usar:
- `raise Exception("...")`

Usar:
- excepciones semánticas del módulo
- con mensaje claro y `status_code` coherente

### Regla 4 — Un solo control transaccional
Evitar commits duplicados.
La estrategia recomendada es:
- `session_scope()` maneja commit/rollback
- repositorios solo modifican entidades y hacen `flush/refresh` si hace falta

### Regla 5 — Validación en schemas, reglas en dominio
- Pydantic valida formato y shape del request
- el dominio protege invariantes de negocio

### Regla 6 — Queries y Commands separados cuando aporten valor
Mantener separación:
- `*_cmd_usecase.py`
- `*_query_usecase.py`
- `*_cmd_repository.py`
- `*_query_repository.py`

Pero sin sobrediseñar. Si no hay complejidad real, no inventar CQRS teatral.

### Regla 7 — Tests obligatorios por módulo
Cada nuevo módulo debe incluir mínimo:
- tests de entidad
- tests de excepciones
- tests de serialización / `to_dict()`
- tests de casos de uso clave

---

## 10. Contrato mínimo para un nuevo módulo

Cuando BULMA cree un módulo nuevo, debe entregar como mínimo:

### Dominio
- entidad principal
- excepciones del módulo
- interfaz de repositorio
- mensajes de éxito

### Aplicación / casos de uso
- schema de creación
- schema de actualización o query si aplica
- command use case
- query use case
- fachada unificada del módulo
- factory de dependencias

### Infraestructura
- modelo SQLAlchemy
- repositorio de escritura
- repositorio de lectura
- mapper si el dominio es puro

### API
- ruta health del módulo
- CRUD o endpoints definidos
- responses homogéneas

### Testing
- carpeta del módulo en `src/tests/`
- pruebas mínimas del comportamiento principal

---

## 11. Módulo de referencia práctica: `users`

El módulo `users` sirve hoy como referencia estructural porque contiene el patrón completo:

- `domain/users.py`
- `domain/users_repository.py`
- `domain/users_exception.py`
- `domain/users_success.py`
- `infrastructure/users.py`
- `infrastructure/users_cmd_repository.py`
- `infrastructure/users_query_repository.py`
- `usecase/users_cmd_schema.py`
- `usecase/users_cmd_usecase.py`
- `usecase/users_query_usecase.py`
- `usecase/users_factory.py`
- `usecase/users_usecase.py`
- `api/users/routes_users.py`
- `tests/users/test_users.py`

### Qué copiar de `users`
- convención de nombres
- separación de archivos
- factory + usecase unificado
- esquema de pruebas

### Qué no copiar de `users`
- dependencia del dominio respecto a infraestructura
- errores genéricos en repositorios
- diseño de dominio demasiado anémico

---

## 12. Guía rápida para BULMA al crear un módulo nuevo

Secuencia recomendada:

1. definir nombre del módulo y lenguaje ubicuo
2. crear entidad y excepciones de dominio
3. definir contratos de repositorio
4. modelar SQLAlchemy en infraestructura
5. implementar repositorios cmd/query
6. crear schemas Pydantic
7. construir use cases
8. exponer rutas Chalice
9. agregar tests
10. validar consistencia con módulos existentes

---

## 13. Módulos candidatos futuros

Posibles siguientes capacidades del sistema:
- finanzas
- pagos
- áreas comunes
- reservas
- visitantes
- vehículos
- anuncios/comunicaciones
- seguridad / control de acceso

Recomendación arquitectónica:
antes de seguir multiplicando módulos por tabla, conviene evolucionar hacia grupos de negocio más claros, por ejemplo:
- `identity`
- `property_structure`
- `residency`
- `billing`
- `communications`
- `security`

---

## 14. Calidad actual del proyecto

Estado observado durante la revisión:
- estructura modular consistente: **sí**
- tests pasando: **sí**
- patrón reutilizable para nuevos módulos: **sí**
- DDD puro: **no todavía**
- base apta para refactor progresivo: **sí**

Resumen brutalmente honesto:

> `condo-py` ya tiene tablero, piezas y aperturas.
> Ahora toca dejar de modelar solo tablas y empezar a modelar negocio.

---

## 15. Criterio rector para futuros cambios

Toda nueva contribución debe respetar esta prioridad:

1. **claridad del dominio**
2. **consistencia estructural**
3. **bajo acoplamiento**
4. **pruebas mínimas obligatorias**
5. **sin referencias heredadas de stacks anteriores**

Este proyecto ya no debe documentarse ni diseñarse como migración desde otra plataforma. La fuente de verdad es el código Python actual.

---

## 16. Referencias internas útiles

- `src/app.py`
- `src/chalicelib/api/`
- `src/chalicelib/dddpy/`
- `src/tests/`
- `documentation/architecture.md`
- `documentation/docker.md`

---

**README actualizado para el estado real de `condo-py`, enfocado en desarrollo modular con la arquitectura vigente.**
