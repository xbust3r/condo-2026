# condo-py — Documentación Unificada

> **Proyecto:** Sistema de Gestión de Condominios para LATAM
> **Estado:** Backend operativo (FastAPI + DDD/CQRS) — Frontend en desarrollo (Next.js)
> **Liderazgo:** Miguel (Technical Leader — humano)
> **Desarrollo:** 100% agentes de IA (Lelouch, Misato, Bulma)
> **Última actualización:** 2026-04-29

---

## Tabla de Contenidos

1. [Visión General del Proyecto](#1-visión-general-del-proyecto)
2. [Arquitectura DDD/CQRS](#2-arquitectura-dddcqrs)
3. [Stack Tecnológico](#3-stack-tecnológico)
4. [Módulos del Sistema](#4-módulos-del-sistema)
5. [Análisis Competitivo](#5-análisis-competitivo)
6. [Roadmap de Implementación](#6-roadmap-de-implementación)
7. [Reglas de Arquitectura para el Equipo Dev](#7-reglas-de-arquitectura-para-el-equipo-dev)
8. [Equipo de Agentes IA](#8-equipo-de-agentes-ia)
9. [Anti-Patterns](#9-anti-patterns)

---

## 1. Visión General del Proyecto

### 1.1 Qué es condo-py

`condo-py` es un sistema de gestión de condominios Backend desarrollado en Python con arquitectura DDD/CQRS, pensado para el mercado LATAM hispanohablante.

### 1.2 Diferenciadores Clave

| # | Diferenciador | Descripción |
|---|---|---|
| 1 | **LATAM-first** | Español, soles (PEN), cobros locales,sin competencia seria en idioma español con este stack |
| 2 | **Desarrollo rápido con IA** | Sistema custom privado, flexible y optimizable en tiempo récord mediante agentes de IA |
| 3 | **API-first + arquitectura moderna** | REST API nativa, integrable con cualquier frontend o sistema externo |
| 4 | **Arquitectura DDD/CQRS** | Ningún competidor documenta esta robustez técnica; escalable a microservicios |
| 5 | **Docker first** | Deployment sencillo y reproducible |

### 1.3 Modelo de Negocio

**Sistema privado custom por cliente/administradora + soporte y optimización continua.**

No es open source. No es SaaS público. Es desarrollo privado adaptado a cada administradora de condominios.

---

## 2. Arquitectura DDD/CQRS

### 2.1 Tesis Arquitectónica

> **El dominio expresa significado, el use case coordina y produce la respuesta de éxito, la infraestructura implementa, y shared define contratos transversales para logging y manejo de errores.**

### 2.2 Capas y Responsabilidades

| Capa | Ubicación | Responsabilidad |
|---|---|---|
| **API** | `src/api/` | Parsear input, invocar use case, devolver `response.dict()`, delegar errores a `@api_handler` |
| **Domain** | `src/library/dddpy/*/domain/` | Entidades, excepciones, contratos abstractos, invariantes de negocio |
| **Use Case** | `src/library/dddpy/*/usecase/` | Orquestación, coordinación de repositorios, devuelve `ResponseSuccessSchema` |
| **Infrastructure** | `src/library/dddpy/*/infrastructure/` | Modelos SQLAlchemy, repositorios concretos, mappers, persistencia |
| **Shared** | `src/library/dddpy/shared/` | Decoradores transversales, schemas compartidos, logging, sesión DB |

### 2.3 Flujo Oficial de una Ruta

```
route (FastAPI)
  → parse schema de entrada
  → invoke use case
  → ResponseSuccessSchema (en camino de éxito)
  → response.dict()
  → @api_handler captura DomainException / ValidationError / 500
```

### 2.4 Estructura de un Módulo DDD

```
{modulo}/
├── domain/
│   ├── {modulo}_entity.py          # Entidad de dominio
│   ├── {modulo}_data.py            # Data objects (opcional)
│   ├── {modulo}_exception.py       # Excepciones del módulo
│   ├── {modulo}_success.py         # Catálogo de mensajes de éxito
│   ├── {modulo}_repository.py      # Contrato agregado (opcional)
│   ├── {modulo}_cmd_repository.py  # Contrato de escritura
│   └── {modulo}_query_repository.py # Contrato de lectura
├── infrastructure/
│   ├── db{modulo}.py               # Modelo SQLAlchemy
│   ├── {modulo}_mapper.py          # Mapper DB ↔ Dominio
│   ├── {modulo}_cmd_repository.py  # Repositorio concreto de escritura
│   └── {modulo}_query_repository.py # Repositorio concreto de lectura
└── usecase/
    ├── {modulo}_cmd_schema.py      # Schemas Pydantic de entrada
    ├── {modulo}_cmd_usecase.py     # Caso de uso de escritura
    ├── {modulo}_query_usecase.py   # Caso de uso de lectura
    ├── {modulo}_usecase.py         # Fachada (devuelve ResponseSuccessSchema)
    └── {modulo}_factory.py         # Ensamblaje de dependencias
```

**Módulo de referencia:** `src/library/dddpy/example/`

### 2.5 Reglas del Mapper

- El mapper **vive en infraestructura**
- Traduce DB ↔ dominio
- **No decide reglas de negocio**
- El dominio **no** debe implementar `from_db()` ni importar modelos DB

### 2.6 Response Schemas Compartidos

```python
class ResponseSuccessSchema(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None

class ResponseErrorSchema(BaseModel):
    success: bool = False
    message: str
```

### 2.7 Excepciones de Dominio

```python
# Base: shared/decorators/domain_exception.py
class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        ...

# Las excepciones del módulo heredan de DomainException
# y viven en domain/{modulo}_exception.py
```

### 2.8 Decorador @api_handler

Maneja errores transversalmente:
- `DomainException` → convierte a `ResponseErrorSchema` con el `status_code` de la excepción
- `ValidationError` → convierte a 400
- Errores inesperados → convierte a 500

**Implementación vigente:** FastAPI-native. No debe mezclarse con lógica de Chalice u otros frameworks.

---

## 3. Stack Tecnológico

### Backend (Python)
- **Python** 3.14
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Validación:** Pydantic
- **Base de datos:** MySQL (AWS RDS)
- **Contenedores:** Docker + docker-compose

### Frontend (Next.js)
- **Framework:** Next.js (App Router)
- **Lenguaje:** TypeScript
- **Estilos:** Tailwind CSS
- **Estado:** React Query / Zustand
- **UI Components:** shadcn/ui

### Repositorios

| Repo | Ruta | Descripción |
|---|---|---|
| `condo-py` | `/home/miguel/servers/condo-py` | Backend Python / FastAPI / DDD |
| `condo-backdmin` | `/home/miguel/servers/condo-backdmin` | Frontend Next.js |

---

## 4. Módulos del Sistema

### 4.1 Estado General

| Estado | Significado |
|--------|-------------|
| ✅ | Implementado completamente en Python |
| ❌ | Pendiente — sin código Python |
| 🔄 | En construcción |
| ⚠️ | Deprecado — no usar en código nuevo |

### 4.2 Módulos Implementados

| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `shared/` | Componentes transversales (decorators, schemas, logging, mysql) | ✅ |
| `example/` | Plantilla de referencia DDD (NO lógica de negocio) | ✅ |
| `core_condominiums/` | Gestión de condominios | ✅ |
| `core_buildings/` | Torres/edificios dentro del condominio | ✅ |
| `core_buildings_types/` | Catálogo: residencial, comercial, mixto | ✅ |
| `core_units/` | Unidades/departamentos dentro de cada edificio | ✅ |
| `core_unit_types/` | Catálogo: apartamento, casa, local comercial | ✅ |
| `users/` | Usuarios autenticables (email, password_hash, status) | ✅ |
| `user_profiles/` | Perfil humano desacoplado de autenticación | ✅ |
| `core_unit_ownerships/` | Relación patrimonial usuario ↔ unidad | 🔄 |
| `core_unit_occupancies/` | Relación de ocupación/uso usuario ↔ unidad | 🔄 |
| `core_condominium_roles/` | Roles administrativos por condominio | 🔄 |

### 4.3 Módulos Pendientes

| Módulo | Descripción | Prioridad |
|--------|-------------|-----------|
| `auth` | Autenticación JWT/OAuth2 + RBAC contextual | Crítica |
| `accounts_receivable` | Cuentas por cobrar por unidad | Crítica |
| `charges` | Cargos recurrentes y extraordinarios | Crítica |
| `receipts` | Generación de recibos | Alta |
| `payments` | Registro de pagos y conciliación | Alta |
| `ledger` | Estado de cuenta por unidad | Alta |
| `announcements` | Anuncios/comunicados | Media-Alta |
| `notifications` | Email/SMS/push/in-app | Media-Alta |
| `documents` | Repositorio de documentos | Media-Alta |
| `tickets` | Incidencias / solicitudes | Media |
| `resident_portal` | Portal web para residentes | Media |
| `amenity_booking` | Reserva de áreas comunes | Media |
| `visitors` | Registro de visitas/invitados | Media |
| `packages` | Registro de paquetería | Baja-Media |
| `meeting_minutes` | Actas de reuniones | Baja |
| `voting` | Votaciones digitales | Baja |
| `audit_trail` | Log de auditoría | Baja |
| `integrations` | Webhooks / API pública | Baja |
| `dashboards` | Reporting ejecutivo | Baja |

### 4.4 Tablas Deprecadas

| Tabla | Motivo |
|-------|--------|
| `users_residents` | Mezclaba identidad, propiedad, ocupación y contexto físico. Reemplazada por `core_unit_ownerships` + `core_unit_occupancies` + `core_condominium_roles`. Solo fallback de emergencia. |

---

## 5. Análisis Competitivo

### 5.1 Competidores Mapeados

| Competidor | Mercado | Diferenciador clave |
|---|---|---|
| **Buildium** | USA/Canadá | All-in-one, contabilidad fuerte |
| **AppFolio** | USA/Enterprise | AI nativa (Realm-X Flows), escala masiva |
| **Condo Control** | USA/Canadá | Mejor para condominios específicos, AI assistant |
| **Propertyware** | USA | API abierta, alta customización |
| **Superlógica** | Brasil | Fintech integrada, PIX, líder en Brasil |
| **CondoLivre** | Brasil | Fintech complementaria (crédito condominial) |
| **TownSq** | Brasil/USA | Mobile-first, bilingual |
| **Kastle** | Global | Seguridad física, no es gestión condominial |

### 5.2 Comparativa: condo-py vs. Competidores

| Feature | Buildium | AppFolio | Condo Control | Superlógica | condo-py |
|---|---|---|---|---|---|
| **Stack** | SaaS cerrado | SaaS/AI nativa | SaaS cerrado | SaaS + Fintech | FastAPI + SQLAlchemy (Custom) |
| **Arquitectura** | Monolítico SaaS | Plataforma unificada | SaaS | SaaS | DDD/CQRS moderna |
| **Open Source** | ❌ | ❌ | ❌ | ❌ | ❌ Custom |
| **API abierta** | Limitada | Limitada | Integraciones | No pública | ✅ REST nativa |
| **Idioma** | Inglés | Inglés | Inglés | Portugués | **Español LATAM** |
| **Mercado LATAM** | ❌ | ❌ | ❌ | Solo Brasil | ✅ Peru/LATAM first |
| **Gestión financiera** | ✅ | ✅ | ✅ | ✅ Fintech | ❌ Pendiente |
| **Portal residente** | ✅ | ✅ | ✅ | ✅ App | ❌ Pendiente |
| **AI/Automatización** | Básica | ✅ Avanzada | ✅ AI Asistente | ❌ | ❌ Pendiente |
| **Self-hosted** | ❌ | ❌ | ❌ | ❌ | ✅ Docker |
| **Multi-condominio** | ✅ | ✅ | ✅ | ✅ | ✅ Preparada |

### 5.3 Fortalezas de condo-py

1. **Arquitectura DDD/CQRS** — ningún competidor documenta esta robustez técnica
2. **Desarrollo acelerado con IA** — construcción, modificación y optimización mediante agentes de IA (vs. desarrollo humano tradicional)
3. **API REST nativa** — integrable con cualquier frontend/mobile
4. **Python ecosystem** — facilita extensiones con AI, ML, analytics
5. **Docker first** — deployment sencillo
6. **Foco LATAM/Peru** — cero competencia seria en idioma español

### 5.4 Gaps Críticos

1. Sin portal de residentes
2. Sin gestión financiera / cobros
3. Sin notificaciones (email, SMS, push)
4. Sin app móvil
5. Sin autenticación JWT/OAuth
6. Sin reserva de amenidades
7. Sin e-voting / asambleas digitales

---

## 6. Roadmap de Implementación

### Fase 1 — Núcleo Inmobiliario ✅
1. `core_condominiums`
2. `core_buildings`
3. `core_buildings_types`
4. `core_units`
5. `core_unit_types`

### Fase 2 — Identidad, Acceso y Ocupación 🔄
6. `users`
7. `user_profiles`
8. `core_unit_ownerships`
9. `core_unit_occupancies`
10. `core_condominium_roles`
11. `auth` (JWT/OAuth2 + RBAC)

### Fase 3 — Cuentas, Cargos y Recibos ❌
12. `accounts_receivable`
13. `charges`
14. `receipts`
15. `payments`
16. `ledger`

### Fase 4 — Comunicación y Operación Básica ❌
17. `announcements`
18. `notifications`
19. `documents`
20. `tickets`

### Fase 5 — Experiencia Residente ❌
21. `resident_portal`
22. `amenity_booking`
23. `visitors`
24. `packages`

### Fase 6 — Gobernanza y Capa Premium ❌
25. `meeting_minutes`
26. `voting`
27. `audit_trail`
28. `integrations`
29. `dashboards`

---

## 7. Reglas de Arquitectura para el Equipo Dev

### 7.1 Reglas por Capa

**`src/api/**`**
- ✅ Allowed: route definitions, request parsing, schema parsing, use case invocation, `response.dict()`, `@api_handler`
- ❌ Forbidden: direct SQLAlchemy access, business rules, mapper logic, transaction ownership

**`src/library/dddpy/*/domain/**`**
- ✅ Allowed: entities, domain exceptions, data objects, repository contracts, invariants
- ❌ Forbidden: importing DB models, HTTP classes, SQLAlchemy sessions, usecase schemas

**`src/library/dddpy/*/usecase/**`**
- ✅ Allowed: orchestration, command/query separation, repository coordination, `ResponseSuccessSchema`, raising `DomainException`
- ❌ Forbidden: HTTP concerns, raw ORM modeling, domain leakage

**`src/library/dddpy/*/infrastructure/**`**
- ✅ Allowed: DB models, concrete repositories, mappers, persistence details
- ❌ Forbidden: business policy ownership, semantic decisions that belong to domain

**`src/library/dddpy/shared/**`**
- ✅ Allowed: db/session setup, response schemas, logging, decorators, domain exception base
- ❌ Forbidden: module-specific business rules, module-specific exceptions, misc dumping

### 7.2 Reglas del Decorador `@api_handler`

El decorador es **FastAPI-native**. Implementación vigente no debe depender de `chalice`, `Blueprint`, `current_request` ni respuestas de otro framework.

```
route → parse schema → use case → ResponseSuccessSchema → response.dict()
                                                    ↓
                              @api_handler captura DomainException / ValidationError
```

### 7.3 Reglas de Factory

- La factory vive en `usecase/`
- Ensambla repositorios concretos con use cases
- **No** esparcir wiring en archivos random o routers

### 7.4 Axiomas de Arquitectura

- Framework es borde, no núcleo
- Mapper owns DB ↔ domain translation
- Use case owns orchestration y success response
- Domain owns meaning y semantic errors
- Shared owns cross-cutting primitives
- `example/` es el módulo de referencia actual

---

## 8. Equipo de Agentes IA

### 8.1 Estructura del Equipo

| Rol | Nombre | Modelo | Canal Discord |
|---|---|---|---|
| Technical Leader (humano) | **Miguel** | — | `#condo-backdmin` |
| Architect | **Lelouch** | GPT 5.4 | `@Lelouch S` |
| Coordinator | **Misato** | Minimax 2.7 | `@Misato K` |
| Dev Lead | **Bulma** | Minimax 2.7 / DeepSeek 4 Pro / Flash | `@Bulma S` |

### 8.2 Responsabilidades por Agente

**Lelouch (Architect)**
- Diseño de arquitectura DDD/CQRS
- Decisiones de alto nivel
- Definición de estructura de módulos y patrones
- Planning y roadmap técnico

**Misato (Coordinator)**
- Coordinación del flujo de trabajo
- Priorización de tareas
- Seguimiento de progreso del sprint
- Gestión de blockers y escalado a Miguel

**Bulma (Dev Lead)**
- Implementación Python (FastAPI, DDD modules, infrastructure)
- Implementación Next.js (frontend)
- Writing tests, migrations, seeds
- Seguir patrones y arquitectura definidos

### 8.3 Cuándo Usar Cada Modelo (Bulma)

| Modelo | Uso |
|---|---|
| **Minimax 2.7** | Desarrollo general, código Python/FastAPI, lógica de dominio |
| **DeepSeek 4 Pro** | Tasks complejas, debugging difícil, código que requiere razonamiento técnico profundo |
| **DeepSeek 4 Flash** | Tasks rápidas y simples, boilerplate, cambios menores |

### 8.4 Reglas de Etiquetado en Discord

| Propósito | Etiquetar |
|---|---|
| Planning / revisiones generales | `@Lelouch S` |
| Revisiones a Bulma | `@Misato K` |
| Cambios a condo-py | `@Bulma S` |
| Frontend condo-backdmin | `@Pochita` |
| Decisiones de liderazgo | Miguel directamente |

### 8.5 Formato de Commits

```
type(scope): subject

<body>

<detailed list of changes>
```

Tipos válidos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `wip`

---

## 9. Anti-Patterns

### API Anti-Patterns
- Poner reglas de negocio en route handlers
- Acceder DB session directamente desde router
- Retornar objetos ORM crudos
- Duplicar lógica de use case en funciones de endpoint

### Domain Anti-Patterns
- Importar modelos `DB*` en domain
- Importar clases FastAPI/HTTP en domain
- Convertir entidad de dominio en objeto de transporte dentro de domain
- Mantener entidades permanentemente anémicas si una regla pertenece claramente al dominio

### Use Case Anti-Patterns
- Mezclar lógica de excepciones HTTP en use case
- Mezclar creación de modelos SQLAlchemy directamente en use case si el mapper ya lo maneja
- Crear un mega-use-case que owning toda la semántica de negocio

### Infrastructure Anti-Patterns
- Definir reglas de negocio en repository
- Hacer que el mapper decida política de dominio
- Filtrar concerns de sesión/ORM hacia arriba innecesariamente

### Shared Anti-Patterns
- Colocar helpers específicos de módulo en `shared/`
- Tratar `shared/` como carpeta misc
- Ocultar ownership poco claro escondiendo archivos en shared

### Project Anti-Patterns
- Renombrar términos legacy durante trabajo de features no relacionadas
- Combinar entrega de features con cleanup general sin approval
- Editar `docs/new-standard/` mientras se actualizan docs del proyecto actual
- Inventar pureza arquitectónica no reflejada en el codebase actual

---

## Repositorios

| Repo | Ruta | Descripción |
|---|---|---|
| `condo-py` | `/home/miguel/servers/condo-py` | Backend Python / FastAPI / DDD |
| `condo-backdmin` | `/home/miguel/servers/condo-backdmin` | Frontend Next.js |

---

*Documentación unificada por Misato K — 2026-04-29*
