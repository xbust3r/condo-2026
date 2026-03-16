# Architecture Rules for BULMA

## Layer ownership

### `src/api/**`
Allowed:
- route definitions
- request parsing
- response shaping
- HTTP/framework adaptation
- use case invocation

Forbidden:
- direct SQLAlchemy access
- business rules
- mapper logic
- transaction ownership
- domain exception definition

### `src/library/dddpy/*/usecase/**`
Allowed:
- application orchestration
- command/query separation
- repository coordination
- process sequencing
- factory wiring for module use cases

Forbidden:
- HTTP concerns inside application logic
- raw ORM modeling
- domain leakage into framework details
- “god use case” behavior

### `src/library/dddpy/*/domain/**`
Allowed:
- entities
- module-specific domain exceptions
- repository contracts
- business semantics
- invariants
- state transitions

Forbidden:
- importing DB models
- importing framework HTTP classes
- importing SQLAlchemy session details
- transport-specific logic
- mapper placement

### `src/library/dddpy/*/infrastructure/**`
Allowed:
- DB models
- concrete repositories
- mappers
- persistence details
- session manager usage
- module-level logger usage

Forbidden:
- business policy ownership
- semantic decision-making that belongs to entities/use cases
- domain exception base definition

### `src/library/dddpy/shared/**`
Allowed:
- db/session shared setup
- common response schemas
- logging
- constants
- domain exception base class
- api decorators / cross-cutting decorators
- truly reusable utilities

Forbidden:
- module-specific business rules
- module-specific exceptions
- dumping unrelated helpers
- hiding unclear ownership inside shared

## Mandatory structure for a new module

Expected baseline:

```text
module/
├── domain/
│   ├── entity
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
    ├── module_usecase.py      # optional facade
    └── module_factory.py
```

## Mapper rules

- Mapper lives in `infrastructure/`
- Mapper translates DB ↔ domain
- Mapper does not decide business rules
- Domain must not implement `from_db()` or import `DB*`
- If translation is needed, create/update mapper first

## Domain exception rules

- Module-specific exceptions live in `domain/*_exception.py`
- Module-specific exceptions must inherit from shared `DomainException`
- Base class location: `shared/decorators/domain_exception.py`
- If an error is semantic/business-level, do not use raw `Exception` or `ValueError`
- `status_code` belongs to the semantic exception contract when needed

## Response schema rules

Shared response schemas live in:
- `shared/schemas/response_schema.py`

Use:
- `ResponseSuccessSchema` for success
- `ResponseErrorSchema` for controlled errors

Do not invent ad-hoc response shapes per module without explicit architecture decision.

## Factory rules

- Factory lives in `usecase/`
- Factory wires concrete repositories with use cases
- Do not scatter wiring in random files or routers

## Architecture axioms

- Framework is edge, not core.
- Mapper owns DB ↔ domain translation.
- Use case owns orchestration.
- Domain owns meaning.
- Shared owns cross-cutting primitives.
- Naming debt is documented debt, not auto-fix territory.
- `example/` is the current reference module unless a newer official base is documented.
sitories with use cases
- Do not scatter wiring in random files or routers

## Architecture axioms

- Framework is edge, not core.
- Mapper owns DB ↔ domain translation.
- Use case owns orchestration.
- Domain owns meaning.
- Shared owns cross-cutting primitives.
- Naming debt is documented debt, not auto-fix territory.
- `example/` is the current reference module unless a newer official base is documented.
