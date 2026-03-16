# Architecture Rules for BULMA

## Layer ownership

### `src/api/**`
Allowed:
- route definitions
- request parsing
- response shaping
- HTTP exception translation
- use case invocation

Forbidden:
- direct SQLAlchemy access
- business rules
- mapper logic
- transaction ownership

### `src/library/dddpy/*/usecase/**`
Allowed:
- application orchestration
- command/query separation
- repository coordination
- process sequencing

Forbidden:
- HTTP concerns
- raw ORM modeling
- domain leakage into framework details
- “god use case” behavior

### `src/library/dddpy/*/domain/**`
Allowed:
- entities
- domain exceptions
- repository contracts
- business semantics
- invariants
- state transitions

Forbidden:
- importing DB models
- importing FastAPI classes
- importing SQLAlchemy session details
- transport-specific logic

### `src/library/dddpy/*/infrastructure/**`
Allowed:
- DB models
- concrete repositories
- mappers
- persistence details

Forbidden:
- business policy ownership
- semantic decision-making that belongs to entities/use cases

### `src/library/dddpy/shared/**`
Allowed:
- db/session shared setup
- common response schemas
- logging
- constants
- truly reusable utilities

Forbidden:
- dumping unrelated helpers
- module-specific logic disguised as shared

## Architecture axioms

- Framework is edge, not core.
- Mapper owns DB ↔ domain translation.
- Use case owns orchestration.
- Domain owns meaning.
- Naming debt is documented debt, not auto-fix territory.
