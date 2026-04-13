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
