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

