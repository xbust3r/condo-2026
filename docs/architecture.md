# Arquitectura de `condo-py`

> **Proyecto:** `condo-py`
>
> **Tipo de sistema:** backend CRUD modular para gestión de condominios
>
> **Entrypoint principal:** FastAPI
>
> **Persistencia:** SQLAlchemy + MySQL
>
> **Validación:** Pydantic
>
> **Migraciones:** Alembic

---

## 1. Propósito del sistema

`condo-py` es un backend orientado a gestionar recursos del dominio inmobiliario/condominial, principalmente:

- condominios,
- edificios,
- tipos de edificio,
- unidades,
- tipos de unidad,
- usuarios,
- relaciones de residentes.

No debe pensarse como “un FastAPI con tablas”.
Debe pensarse como un sistema modular donde la API es solo la puerta de entrada y la semántica debe vivir en capas internas.

---

## 2. Tesis arquitectónica

La tesis correcta del proyecto es esta:

> **FastAPI entra y sale; el dominio y los casos de uso deben conservar el control semántico.**

En términos prácticos:

- `api/` recibe y adapta requests.
- `usecase/` coordina casos de uso.
- `domain/` representa entidades y reglas de negocio.
- `infrastructure/` contiene ORM, repositorios concretos y mappers.
- `shared/` concentra piezas transversales realmente compartidas.

Si el framework empieza a gobernar el modelo, el tablero se rompe.

---

## 3. Estructura real del proyecto

```text
condo-py/
├── docs/
├── src/
│   ├── app.py
│   ├── main.py
│   ├── api/
│   │   ├── condominiums/
│   │   ├── buildings/
│   │   ├── buildings_types/
│   │   ├── unitys/
│   │   ├── unittys_types/
│   │   ├── users/
│   │   └── residents/
│   ├── library/
│   │   └── dddpy/
│   │       ├── shared/
│   │       ├── core_condominiums/
│   │       ├── core_buildings/
│   │       ├── core_buildings_types/
│   │       ├── core_unitys/
│   │       ├── core_unittys_types/
│   │       ├── core_users/
│   │       ├── core_users_residents/
│   │       ├── users/
│   │       └── users_residents/
│   ├── alembic/
│   ├── requirements.txt
│   └── .env
└── docker-compose.yml
```

### Observación importante

La estructura muestra una intención DDD, pero también evidencia deuda:

- naming inconsistente (`unitys`, `unittys`, `users` vs `core_users`),
- coexistencia de módulos aparentemente duplicados,
- mezcla de naming histórico con naming más reciente.

La documentación debe reconocer esto.
No conviene fingir una pureza que el código aún no tiene.

---

## 4. Capas y responsabilidades

## 4.1 `api/` — entrypoints HTTP

Responsable de:

- declarar rutas FastAPI,
- recibir payloads,
- invocar casos de uso,
- traducir excepciones a respuestas HTTP,
- envolver resultados en `ResponseSchema`.

No debe:

- implementar reglas de negocio,
- consultar SQLAlchemy directamente,
- decidir semántica del dominio,
- duplicar lógica de validación semántica que debería vivir más adentro.

Ejemplo real: `src/api/condominiums/routes.py` crea el use case, llama métodos como `create`, `get_all`, `update`, y adapta errores a `HTTPException`.

---

## 4.2 `usecase/` — application layer

Responsable de:

- coordinar pasos,
- separar operaciones de command/query cuando aporta claridad,
- trabajar contra contratos de repositorio,
- definir la secuencia del caso de uso.

En el proyecto existe un **CQRS liviano** en varios módulos:

- `..._cmd_usecase.py`
- `..._query_usecase.py`
- `..._usecase.py` como fachada combinada

Eso es válido siempre que siga siendo pragmático y no ceremonial.

No debe:

- absorber toda la semántica del negocio,
- convertirse en un “god service”,
- mezclar detalles HTTP o SQLAlchemy crudos.

---

## 4.3 `domain/` — modelo de negocio

Responsable de:

- representar entidades,
- expresar estados válidos,
- contener comportamiento semántico,
- definir excepciones de dominio,
- exponer contratos de repositorio.

Ejemplo: `Condominium` ya tiene comportamiento básico como `activate`, `deactivate` y `update`.
Eso es una señal correcta: la entidad no debería ser solo un saco de atributos.

Aun así, el dominio actual sigue siendo relativamente delgado.
Todavía hay espacio para fortalecer:

- invariantes,
- value objects,
- reglas de transición,
- validaciones semánticas.

No debe conocer:

- clases `DB*`,
- sesiones SQLAlchemy,
- detalles de FastAPI,
- detalles de transporte externo.

---

## 4.4 `infrastructure/` — persistencia y detalles técnicos

Responsable de:

- modelos ORM,
- repositorios concretos,
- mappers DB ↔ dominio,
- detalles de sesión/persistencia.

Ejemplo correcto: `condominiums_mapper.py` traduce entre `DBCondominiums` y `Condominium`.
Esa es la frontera sana: infraestructura conoce al dominio; el dominio no debe obedecer al ORM.

No debe:

- gobernar reglas de negocio,
- decidir transiciones semánticas,
- filtrar acoplamientos técnicos hacia `domain/`.

---

## 4.5 `shared/` — cross-cutting disciplinado

Responsable de:

- base de datos compartida,
- esquemas comunes como `ResponseSchema`,
- logging,
- constantes,
- utilidades realmente transversales.

No debe convertirse en:

- basurero genérico,
- carpeta “misc”,
- punto donde se deposita cualquier cosa que no encaja.

`shared/` debe ser pequeño y austero.
Cuando crece sin control, el reino cae por el flanco interno.

---

## 5. Flujo principal de una request

El flujo sano de una operación HTTP es:

```text
HTTP Request
  → FastAPI Router (`api/`)
  → Pydantic schema de entrada
  → UseCase (`usecase/`)
  → Repository contract (`domain/`)
  → Repository implementation (`infrastructure/`)
  → SQLAlchemy model / mapper
  → MySQL
  → Domain entity / response wrapper
  → HTTP Response
```

### Lectura táctica del flujo

- **Router** adapta.
- **UseCase** coordina.
- **Domain** decide significado.
- **Infrastructure** ejecuta detalle técnico.

Si una sola capa intenta hacer las cuatro cosas, ya sacrificaste demasiadas piezas en una sola jugada.

---

## 6. Módulos funcionales actuales

Los módulos principales documentados y visibles en el proyecto son:

- `core_condominiums`
- `core_buildings`
- `core_buildings_types`
- `core_unitys`
- `core_unittys_types`
- `users`
- `users_residents`

También aparecen:

- `core_users`
- `core_users_residents`

Esto debe interpretarse como una **inconsistencia estructural pendiente de aclaración o consolidación**. La documentación no debe ocultarlo y los cambios futuros deben manejarlo con cuidado.

---

## 7. Contratos y respuestas

El proyecto usa un wrapper común de respuesta:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": {},
  "errors": null
}
```

Ese contrato ayuda a estandarizar la salida HTTP.
Sin embargo, la estandarización de forma no reemplaza la semántica del dominio.

Pydantic valida estructura.
El negocio debe validarse en `domain/` y `usecase/`.

---

## 8. Decisiones arquitectónicas vigentes

### 8.1 FastAPI es borde, no núcleo
El framework organiza rutas y middlewares, pero no debe gobernar la lógica central.

### 8.2 `usecase/` representa la capa de aplicación
Aunque el naming histórico use `usecase` en lugar de `application`, la responsabilidad es la misma: coordinar casos de uso.

### 8.3 Los mappers deben absorber la traducción DB ↔ dominio
Las entidades no deben importar el ORM.

### 8.4 CQRS solo si aporta claridad
Separar command/query está bien cuando ayuda a comprender o aislar operaciones. Si solo duplica archivos, se vuelve teatro enterprise.

### 8.5 La deuda de naming es real
No debe corregirse accidentalmente durante una feature. Si se quiere refactor serio de nombres, debe hacerse como iniciativa explícita.

---

## 9. Deuda y contradicciones actuales

La arquitectura tiene buenas intenciones, pero todavía presenta frentes en rojo:

### 9.1 Naming inconsistente
- `unitys`
- `unittys_types`
- `users` vs `core_users`
- `residents` expuesto por API pero `users_residents` en módulos

Esto impacta:

- legibilidad,
- onboarding,
- predicción de imports,
- diseño futuro.

### 9.2 Dominio aún delgado
Las entidades tienen comportamiento básico, pero todavía no gobiernan suficientes invariantes del negocio.

### 9.3 Riesgo de duplicidad conceptual
La convivencia de módulos `core_*` y módulos no `core_*` exige una decisión futura: consolidar, documentar mejor, o eliminar duplicidad real.

### 9.4 DDD declarado vs DDD efectivo
El proyecto ya tiene separación por capas, pero todavía debe fortalecerse para que DDD no sea solo estructura de carpetas.

---

## 10. Dirección recomendada de evolución

El camino sano para `condo-py` es:

1. **preservar fronteras**,
2. **hacer explícitas las responsabilidades**,
3. **enriquecer el dominio gradualmente**,
4. **evitar refactors cosméticos mezclados con features**,
5. **usar documentación humana y documentación para IA en paralelo**.

La evolución correcta no es “mover archivos para que se vea bonito”.
Es lograr que el sistema siga teniendo sentido aunque cambie el borde técnico.

---

## 11. Resumen ejecutivo

`condo-py` ya tiene una base modular respetable.
La jugada correcta ahora no es reinventarlo todo, sino:

- clarificar la arquitectura real,
- blindar las fronteras,
- no esconder la deuda,
- y dar instrucciones precisas para humanos y agentes.

> **Una arquitectura madura no es la que presume DDD. Es la que permite extender el sistema sin romper la semántica ni convertir cada feature en una guerra civil.**
