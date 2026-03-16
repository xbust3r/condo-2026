# Arquitectura de `condo-py`

> **Proyecto:** `condo-py`
>
> **Base actual de referencia:** `src/library/dddpy/shared/` + `src/library/dddpy/campaigns/`
>
> **Estilo arquitectónico:** DDD pragmático con separación `domain / infrastructure / usecase / shared`
>
> **Objetivo:** que cada módulo nuevo siga un patrón estable, explícito y repetible

---

## 1. Propósito de esta documentación

Esta documentación ya no parte de los módulos viejos que fueron descartados.
Parte de la **nueva base deseada** del proyecto:

- `shared/` como núcleo transversal,
- `campaigns/` como módulo patrón,
- y una separación estricta entre semántica, orquestación y persistencia.

La idea central es simple:

> **un módulo nuevo no debe inventar su estructura; debe seguir el patrón base oficial.**

---

## 2. Tesis arquitectónica

La tesis correcta del proyecto es esta:

> **el dominio expresa significado, el use case coordina, la infraestructura implementa y shared define las piezas comunes del reino.**

En términos prácticos:

- `domain/` contiene entidades, contratos y excepciones de negocio.
- `usecase/` contiene schemas, orquestación y factories.
- `infrastructure/` contiene DB models, mappers y repositorios concretos.
- `shared/` contiene respuesta estándar, excepciones base, logging y session managers.

Si una capa invade a otra, el diseño se degrada aunque el código “funcione”.

---

## 3. Base estructural actual

La base que hoy debe tomarse como referencia es:

```text
src/library/dddpy/
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
└── campaigns/
    ├── domain/
    ├── infrastructure/
    └── usecase/
```

## 3.1 Qué significa esto

- `shared/` define las piezas comunes que todos los módulos pueden reutilizar.
- `example/` representa la **plantilla arquitectónica actual** para crear futuros módulos.
- Los módulos viejos no deben usarse como patrón de diseño si contradicen esta base.

---

## 4. Estructura oficial esperada de un módulo

Todo módulo nuevo debería aproximarse a esta forma:

```text
module/
├── domain/
│   ├── entity.py
│   ├── module_exception.py
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
    ├── module_usecase.py        # opcional si existe fachada combinada
    └── module_factory.py
```

### Regla táctica

Si un módulo no deja claro:

- qué es entidad,
- qué es excepción,
- qué es contrato,
- qué es mapper,
- qué es repositorio concreto,
- y qué es orquestación,

entonces aún no está bien modelado.

---

## 5. Responsabilidad por capa

## 5.1 `domain/`

Responsable de:

- entidades de dominio,
- semántica de negocio,
- contratos abstractos de repositorio,
- excepciones de dominio.

Ejemplo real:

- `campaigns.py`
- `campaigns_exception.py`
- `campaigns_repository.py`
- `campaigns_cmd_repository.py`
- `campaigns_query_repository.py`

### Regla de pureza

El dominio **no** debe importar:

- modelos DB,
- sesiones SQLAlchemy,
- detalles HTTP,
- decorators del framework,
- respuestas técnicas.

### Excepciones de dominio

Las excepciones concretas del módulo deben vivir en `domain/*_exception.py`.

Ejemplo actual:

- `CampaignNotFound`
- `RepeatedCampaignMediaCode`

Y deben heredar de la base compartida:

- `shared/decorators/domain_exception.py`

Eso permite un contrato común de error semántico:

```python
class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        ...
```

### Qué aporta esto

- errores de negocio consistentes,
- status code controlado,
- mejor traducción en el borde,
- menos uso de excepciones genéricas.

---

## 5.2 `usecase/`

Responsable de:

- orquestar casos de uso,
- recibir schemas de entrada,
- coordinar repositorios,
- separar command/query cuando aporte claridad,
- exponer factories para ensamblar dependencias.

Ejemplos reales en `campaigns/`:

- `campaigns_cmd_schema.py`
- `campaigns_cmd_usecase.py`
- `campaigns_query_usecase.py`
- `campaigns_factory.py`

### Regla de diseño

Use case:
- coordina,
- no modela persistencia,
- no debe absorber toda la semántica del negocio,
- no debe contaminarse con detalles HTTP.

### Factories

Las factories viven en `usecase/` y sirven para ensamblar el caso de uso con su implementación concreta.

Ejemplo:

- `campaign_cmd_usecase_factory()`
- `campaign_query_usecase_factory()`

Eso deja explícito el wiring y evita dispersarlo en cualquier parte del sistema.

---

## 5.3 `infrastructure/`

Responsable de:

- modelos ORM,
- repositorios concretos,
- mappers,
- interacción con base de datos,
- detalles técnicos de persistencia.

Ejemplos reales en `campaigns/`:

- `dbcampaigns.py`
- `campaign_mapper.py`
- `campaigns_cmd_repository.py`
- `campaigns_query_repository.py`

### Regla del mapper

El mapper vive en infraestructura y es la frontera oficial entre DB y dominio.

Ejemplo actual:

- `CampaignMapper.to_domain(db_campaign)`
- `CampaignMapper.to_infrastructure(campaign)`

### Qué significa esto

- el dominio no hace `from_db()`;
- el ORM no gobierna a la entidad;
- la traducción de representación queda encapsulada.

### Regla de oro del mapper

El mapper:
- **traduce**,
- **no decide negocio**,
- **no inventa validaciones semánticas**,
- **no reemplaza al dominio**.

---

## 5.4 `shared/`

Responsable de:

- excepciones base,
- response schemas comunes,
- logging,
- session managers,
- constantes y utilidades realmente transversales.

Piezas clave actuales:

- `shared/decorators/domain_exception.py`
- `shared/decorators/api_handler.py`
- `shared/schemas/response_schema.py`
- `shared/logging/`
- `shared/mysql/`
- `shared/postgresql/`

### Regla disciplinaria

`shared/` no debe ser un basurero.
Solo deben entrar piezas que tengan sentido transversal para múltiples módulos.

---

## 6. Contrato de respuestas

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

- `ResponseSuccessSchema` = respuesta estandarizada de éxito.
- `ResponseErrorSchema` = respuesta estandarizada de error controlado.

## 6.2 Regla de uso

Las respuestas del sistema no deben reinventar estructura en cada módulo.
La forma debe mantenerse consistente.

## 6.3 Success messages

Los mensajes de éxito deben ser:

- claros,
- estables,
- semánticos,
- y consistentes entre módulos.

Ejemplos sanos:

- `Campaign created successfully`
- `Campaign updated successfully`
- `Campaign deleted successfully`

Lo importante no es el texto exacto, sino evitar:

- mensajes arbitrarios distintos para la misma operación,
- mensajes vacíos,
- mensajes técnicos innecesarios,
- mezcla de éxito de negocio con detalle interno.

---

## 7. Flujo arquitectónico recomendado

El flujo correcto de una operación es:

```text
Request
  → schema de entrada
  → use case
  → contrato de repositorio en domain
  → implementación concreta en infrastructure
  → mapper DB ↔ domain
  → entidad de dominio
  → response schema compartido
```

### Lectura táctica

- `schema` valida forma,
- `use case` coordina,
- `domain` expresa significado,
- `repository impl` ejecuta,
- `mapper` traduce,
- `shared` estandariza respuesta y manejo transversal.

---

## 8. Módulo patrón: `campaigns`

Hoy `campaigns/` debe considerarse la referencia práctica de cómo construir módulos nuevos.

### Lo que demuestra correctamente

- entidad de dominio separada,
- excepciones del módulo,
- contratos abstractos de repositorio,
- repositorios concretos separados por intención,
- mapper explícito,
- schemas de entrada,
- use cases command/query,
- factory de ensamblaje.

### Lo que todavía debe cuidarse

Aunque `example/` es la base patrón, no significa que esté libre de evolución futura.
Se documenta como patrón porque hoy expresa mejor la estructura deseada que los módulos descartados.

---

## 9. Decisiones arquitectónicas vigentes

### 9.1 El mapper siempre vive en infraestructura
Nunca en domain. Nunca mezclado con el DB model. Nunca en el router.

### 9.2 Las excepciones de negocio heredan de `DomainException`
Si una falla expresa semántica del negocio, debe representarse con una excepción semántica propia.

### 9.3 Los repositorios abstractos viven en domain
La implementación concreta vive en infrastructure.

### 9.4 Las factories viven en usecase
El wiring no debe quedar repartido de forma accidental.

### 9.5 Los response schemas compartidos viven en `shared`
No se redefine la estructura de éxito/error por capricho en cada módulo.

### 9.6 `shared/` define piezas comunes, no reglas de negocio específicas
Si algo solo le sirve a un módulo, probablemente no pertenece a `shared/`.

---

## 10. Dirección recomendada de evolución

El camino sano para `condo-py` es:

1. **usar `campaigns/` como patrón base real**,
2. **crear módulos nuevos respetando la jerarquía domain/usecase/infrastructure/shared**,
3. **mantener mapper, exceptions y response schemas como contratos explícitos**,
4. **evitar refactors cosméticos mezclados con construcción funcional**,
5. **documentar para humanos y para BULMA al mismo tiempo**.

---

## 11. Resumen ejecutivo

La nueva arquitectura de `condo-py` debe entenderse así:

- `shared/` define las piezas comunes del reino,
- `campaigns/` marca el patrón base,
- el mapper traduce,
- `DomainException` unifica errores semánticos,
- los response schemas unifican la forma de salida,
- y cada módulo nuevo debe entrar al tablero siguiendo ese orden.

> **La arquitectura correcta no es la que acumula carpetas. Es la que deja claro quién manda, quién traduce, quién persiste y quién responde.**
la que deja claro quién manda, quién traduce, quién persiste y quién responde.**
o la jerarquía domain/usecase/infrastructure/shared**,
3. **mantener mapper, exceptions y response schemas como contratos explícitos**,
4. **evitar refactors cosméticos mezclados con construcción funcional**,
5. **documentar para humanos y para BULMA al mismo tiempo**.

---

## 11. Resumen ejecutivo

La nueva arquitectura de `condo-py` debe entenderse así:

- `shared/` define las piezas comunes del reino,
- `campaigns/` marca el patrón base,
- el mapper traduce,
- `DomainException` unifica errores semánticos,
- los response schemas unifican la forma de salida,
- y cada módulo nuevo debe entrar al tablero siguiendo ese orden.

> **La arquitectura correcta no es la que acumula carpetas. Es la que deja claro quién manda, quién traduce, quién persiste y quién responde.**
