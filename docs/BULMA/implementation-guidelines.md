# Implementation Guidelines for BULMA

## Reference baseline

When in doubt, use:
- `src/library/dddpy/shared/` as cross-cutting base
- `src/library/dddpy/example/` as reference module
- `src/api/campaigns/` as clean-route reference

Do not use deleted/legacy modules as architecture source of truth.

## When creating a new module

Create the smallest correct baseline:

1. `domain/entity`
2. `domain/module_data.py` when create/update data objects are useful
3. `domain/module_exception.py`
4. `domain/module_repository.py`
5. `domain/module_cmd_repository.py`
6. `domain/module_query_repository.py`
7. `infrastructure/dbmodule.py`
8. `infrastructure/module_mapper.py`
9. `infrastructure/module_cmd_repository.py`
10. `infrastructure/module_query_repository.py`
11. `usecase/module_cmd_schema.py`
12. `usecase/module_cmd_usecase.py`
13. `usecase/module_query_usecase.py`
14. `usecase/module_factory.py`
15. `usecase/module_usecase.py` facade
16. `api/module/routes_*.py` if exposing HTTP entrypoints

## When adding or modifying an endpoint

1. Update corresponding router/entrypoint only for adaptation concerns
2. Parse schema in route layer
3. Reuse existing use case if possible
4. Route should call use case and return `response.dict()`
5. Route should rely on `@api_handler` for centralized error handling
6. If new business rule is needed, implement in `domain/`
7. If persistence translation changes, update mapper/repository in `infrastructure/`
8. Preserve shared response schema format
9. Update docs if behavior or structure changed

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
- define expected behavior using domain entities or domain data objects

Concrete implementations:
- live in `infrastructure/`
- use session manager
- use mapper for DB ↔ domain translation

## Use case guideline

Use case may coordinate:
- input schema handling
- translation from schema to domain data objects
- precondition checks
- repository calls
- returning `ResponseSuccessSchema`
- raising semantic exceptions
- logging meaningful checkpoints

Use case should not:
- expose raw ORM objects to entrypoint layer
- become dumping ground for every rule
- return arbitrary dicts when shared success schema exists

## Response schema guideline

Use shared schemas from `shared/schemas/response_schema.py`.

Success path:
- use case/facade returns `ResponseSuccessSchema`

Error path:
- raise `DomainException` derivatives
- `@api_handler` converts them to `ResponseErrorSchema`

Do not create one-off response wrappers unless explicit architecture decision requires it.

## API handler guideline

Use `@api_handler` on clean API routes.

Expected route shape:

```python
@blueprint.route("/resource", methods=["POST"], cors=True)
@api_handler
def create_resource():
    request = blueprint.current_request
    data = CreateResourceSchema.parse_obj(request.json_body)
    response = ResourceUseCase().create(data)
    return response.dict()
```

Do not duplicate error handling in every route when decorator already owns it.

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

If you alter architecture, module responsibilities, route pattern, or baseline pattern:
- update `docs/architecture.md`
- update `docs/observations/` for human explanation when relevant
- update `docs/BULMA/` if agent guidance changed
