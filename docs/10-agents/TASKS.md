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
