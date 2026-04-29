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
