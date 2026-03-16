# Change Playbook for BULMA

## Objective

Minimize ambiguity and preserve architecture while implementing changes.

## Checklist: endpoint change

- identify target router
- identify target module
- inspect existing use case
- inspect domain entity and exceptions
- inspect repository + mapper
- modify smallest correct layer set
- preserve response schema
- update docs if behavior changed

## Checklist: persistence/model change

- inspect ORM model
- inspect mapper
- inspect repository methods
- inspect domain entity fields/behavior
- inspect affected schemas
- inspect migration impact
- document contract change

## Checklist: business rule change

- define rule in one sentence
- decide if rule is semantic or orchestration
- place in domain if semantic
- place in use case if sequencing/process
- add/update tests when available
- document rationale if non-trivial

## Checklist: documentation change

- `docs/architecture.md` for project-level architecture
- `docs/observations/` for human explanation
- `docs/BULMA/` for agent execution guidance
- never rewrite `new-standard/` unless task explicitly targets the base doctrine

## Escalation rule

If a task seems to require:
- naming normalization,
- module consolidation,
- replacing `users` with `core_users`,
- replacing `usecase` with `application`,
- large DDD refactor,

then stop treating it as a small feature.
It is an explicit architecture task.
