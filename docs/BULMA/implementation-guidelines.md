# Implementation Guidelines for BULMA

## Reference baseline

When in doubt, use:
- `src/library/dddpy/shared/` as cross-cutting base
- `src/library/dddpy/example/` as reference module

Do not use deleted/legacy modules as architecture source of truth.

## When creating a new module

Create the smallest correct baseline:

1. `domain/entity`
2. `domain/module_exception.py`
3. `domain/module_repository.py`
4. `domain/module_cmd_repository.py`
5. `domain/module_query_repository.py`
6. `infrastructure/dbmodule.py`
7. `infrastructure/module_mapper.py`
8. `infrastructure/module_cmd_repository.py`
9. `infrastructure/module_query_repository.py`
10. `usecase/module_cmd_schema.py`
11. `usecase/module_cmd_usecase.py`
12. `usecase/module_query_usecase.py`
13. `usecase/module_factory.py`
14. optional `usecase/module_usecase.py` facade

## When adding or modifying an endpoint

1. Update corresponding router/entrypoint only for adaptation concerns
2. Reuse existing schema/use case if possible
3. If new application behavior is needed, implement in module `usecase/`
4. If new business rule is needed, implement in `domain/`
5. If persistence translation changes, update mapper/repository in `infrastructure/`
6. Preserve shared response schema format
7. Update docs if behavior or structure changed

## Domain exception guideline

If a rule failure is business-semantic:
- define exception in `domain/*_exception.py`
- inherit from shared `DomainException`
- provide clear semantic message
- use `status_code` intentionally when needed

Do not:
- raise generic `Exception`
- raise `ValueError` for business semantics
- define module exceptions inside infrastructure or usecase

## Mapper guideline

If domain entity and DB model need translation:
- add/update `*_mapper.py` in `infrastructure/`
- include explicit methods such as `to_domain(...)` and `to_infrastructure(...)`
- keep mapper free of business decision logic

Do not:
- import DB model into domain
- place mapping logic in router
- place mapping logic inside domain entity constructor for ORM coupling

## Repository guideline

Abstract contracts:
- live in `domain/`
- define expected behavior

Concrete implementations:
- live in `infrastructure/`
- use session manager
- use mapper for DB ↔ domain translation

## Use case guideline

Use case may coordinate:
- input schema handling
- precondition checks
- repository calls
- returning domain entity/result
- selecting success path

Use case should not:
- embed HTTP response shape logic when shared contract already exists
- expose raw ORM objects to entrypoint layer
- become dumping ground for every rule

## Success message guideline

Success responses should use stable semantic messages.
Preferred pattern:
- `<Entity> created successfully`
- `<Entity> updated successfully`
- `<Entity> deleted successfully`
- `<Entity> fetched successfully` when useful

Goal:
- consistency
- low ambiguity
- predictable API behavior

## Response schema guideline

Use shared schemas from `shared/schemas/response_schema.py`.
Do not create one-off response wrappers unless explicit architecture decision requires it.

## Logger guideline

Use shared logger from `shared/logging/logging.py`.

Expected usage zones:
- main/app bootstrap
- API / route layer
- module internal flow

Logger should help answer:
- where the request entered
- what step failed
- what repository/use case was executing
- whether error was controlled or unexpected

Avoid noisy useless logs. Prefer traceable and meaningful logs.

## Documentation guideline

If you alter architecture, module responsibilities, or baseline pattern:
- update `docs/architecture.md`
- update `docs/observations/` for human explanation when relevant
- update `docs/BULMA/` if agent guidance changed
