# Module Map for BULMA

## Current baseline modules

### Shared base

- `src/library/dddpy/shared/decorators/domain_exception.py`
- `src/library/dddpy/shared/decorators/api_handler.py`
- `src/library/dddpy/shared/schemas/response_schema.py`
- `src/library/dddpy/shared/logging/logging.py`
- `src/library/dddpy/shared/mysql/`
- `src/library/dddpy/shared/postgresql/`
- `src/library/dddpy/shared/constants/`
- `src/library/dddpy/shared/utils/`

### Reference template module

- `src/library/dddpy/example/domain/example_entity.py`
- `src/library/dddpy/example/domain/example_data.py`
- `src/library/dddpy/example/domain/example_exception.py`
- `src/library/dddpy/example/domain/example_repository.py`
- `src/library/dddpy/example/domain/example_cmd_repository.py`
- `src/library/dddpy/example/domain/example_query_repository.py`
- `src/library/dddpy/example/infrastructure/dbexample.py`
- `src/library/dddpy/example/infrastructure/example_mapper.py`
- `src/library/dddpy/example/infrastructure/example_cmd_repository.py`
- `src/library/dddpy/example/infrastructure/example_query_repository.py`
- `src/library/dddpy/example/usecase/example_cmd_schema.py`
- `src/library/dddpy/example/usecase/example_cmd_usecase.py`
- `src/library/dddpy/example/usecase/example_query_usecase.py`
- `src/library/dddpy/example/usecase/example_usecase.py`
- `src/library/dddpy/example/usecase/example_factory.py`

### Reference API module

- `src/api/example/routes_example.py`

## Important warning

Legacy modules were removed because they were not the desired architecture base.
Do not reconstruct them by imitation.
Use `example/` as the reference structure and `api/example/` as the route-pattern reference.

Important modeling rule:
- `Repository` = aggregate contract of the module
- `CmdRepository` = write-oriented contract
- `QueryRepository` = read-oriented contract

This is intentional and reflects the project vision for modules with complex or custom logic.

## Structural meaning

### `shared/`
Owns:
- common exceptions
- common response schemas
- common decorators
- logging
- session managers
- reusable utilities

### `example/domain/`
Owns:
- domain entity
- domain data objects
- domain exceptions
- repository contracts

### `example/infrastructure/`
Owns:
- DB model
- mapper
- concrete repositories

### `example/usecase/`
Owns:
- command/query schemas
- command/query use cases
- factory wiring
- facade returning `ResponseSuccessSchema`

### `api/example/`
Owns:
- request parsing
- route exposure
- use case invocation
- returning `response.dict()`
- relying on `@api_handler` for errors

## Response contract

Shared response schemas live in:
- `src/library/dddpy/shared/schemas/response_schema.py`

Current shapes:

```python
class ResponseErrorSchema(BaseModel):
    success: bool = False
    message: str

class ResponseSuccessSchema(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None
```

## Error contract

Shared base exception lives in:
- `src/library/dddpy/shared/decorators/domain_exception.py`

Current base:

```python
class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        ...
```

All module semantic exceptions should derive from it.

## Decorator contract

Shared API decorator lives in:
- `src/library/dddpy/shared/decorators/api_handler.py`

Official route flow:

```text
route
  → parse schema
  → use case
  → ResponseSuccessSchema
  → response.dict()
  → @api_handler handles DomainException / ValidationError / 500
```

## Logging contract

Logger should exist in:
- main/app bootstrap
- API / entrypoints
- internal module critical path

Purpose:
- trace normal flow
- map controlled errors
- map unexpected errors
- simplify debugging across layers
