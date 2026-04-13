# Change Playbook for BULMA

## Objective

Minimize ambiguity and preserve architecture while implementing changes.

## Checklist: new module creation

- inspect `shared/` for reusable primitives
- inspect `example/` as reference module
- inspect `api/example/` as route-pattern reference when HTTP is needed
- create domain entity
- create domain data objects if needed
- create domain exceptions
- make domain exceptions inherit from shared `DomainException`
- create aggregate repository contract in domain when the module needs broader capabilities
- create cmd/query repository contracts in domain
- create DB model in infrastructure when persistence exists
- create mapper in infrastructure
- create concrete repositories in infrastructure
- create command/query schemas in usecase
- create command/query use cases
- create module facade/use case
- create module factory
- define success/error response usage
- update docs

## Checklist: endpoint change

- identify target router/entrypoint
- identify target module
- inspect existing use case
- inspect domain entity and exceptions
- inspect repository + mapper
- modify smallest correct layer set
- preserve shared response schema
- keep framework logic at edge
- use `@api_handler` when following clean-route pattern
- update docs if behavior changed

## Checklist: persistence/model change

- inspect DB model
- inspect mapper
- inspect repository methods
- inspect domain entity fields/behavior
- inspect affected schemas
- inspect migration impact
- ensure logging remains traceable
- document contract change

## Checklist: business rule change

- define rule in one sentence
- decide if rule is semantic or orchestration
- place in domain if semantic
- place in use case if sequencing/process
- add/update semantic exception if needed
- avoid generic exceptions
- add/update logs around critical checkpoints and failures
- document rationale if non-trivial

## Checklist: response contract change

- inspect shared response schemas
- confirm if change is project-wide or module-local
- avoid ad-hoc shape drift
- standardize success message wording
- if wording is reused, centralize it in `domain/*_success.py`
- make use case consume the centralized success catalog
- standardize controlled error handling
- document change in architecture docs

## Checklist: documentation change

- `docs/architecture.md` for project-level architecture
- `docs/observations/` for human explanation
- `docs/BULMA/` for agent execution guidance
- never rewrite `new-standard/` unless task explicitly targets the base doctrine

## Escalation rule

If a task seems to require:
- naming normalization,
- module consolidation,
- replacing baseline `example/` pattern,
- replacing clean-route `api/example/` pattern,
- moving mapper outside infrastructure,
- bypassing shared response schemas,
- bypassing shared `DomainException`,
- bypassing `@api_handler` without explicit architectural reason,
- large DDD refactor,

then stop treating it as a small feature.
It is an explicit architecture task.
