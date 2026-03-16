# Module Map for BULMA

## Current baseline modules

### Shared base

- `src/library/dddpy/shared/decorators/domain_exception.py`
- `src/library/dddpy/shared/decorators/api_handler.py`
- `src/library/dddpy/shared/schemas/response_schema.py`
- `src/library/dddpy/shared/logging/`
- `src/library/dddpy/shared/mysql/`
- `src/library/dddpy/shared/postgresql/`
- `src/library/dddpy/shared/constants/`
- `src/library/dddpy/shared/utils/`

### Reference business module

- `src/library/dddpy/campaigns/domain/campaigns.py`
- `src/library/dddpy/campaigns/domain/campaigns_exception.py`
- `src/library/dddpy/campaigns/domain/campaigns_repository.py`
- `src/library/dddpy/campaigns/domain/campaigns_cmd_repository.py`
- `src/library/dddpy/campaigns/domain/campaigns_query_repository.py`
- `src/library/dddpy/campaigns/infrastructure/dbcampaigns.py`
- `src/library/dddpy/campaigns/infrastructure/campaign_mapper.py`
- `src/library/dddpy/campaigns/infrastructure/campaigns_cmd_repository.py`
- `src/library/dddpy/campaigns/infrastructure/campaigns_query_repository.py`
- `src/library/dddpy/campaigns/usecase/campaigns_cmd_schema.py`
- `src/library/dddpy/campaigns/usecase/campaigns_cmd_usecase.py`
- `src/library/dddpy/campaigns/usecase/campaigns_query_usecase.py`
- `src/library/dddpy/campaigns/usecase/campaigns_usecase.py`
- `src/library/dddpy/campaigns/usecase/campaigns_factory.py`

## Important warning

Legacy modules were removed because they were not the desired architecture base.
Do not reconstruct them by imitation.
Use `campaigns/` as the reference structure.

## Structural meaning

### `shared/`
Owns:
- common exceptions
- common response schemas
- common decorators
- logging
- session managers
- reusable utilities

### `campaigns/domain/`
Owns:
- domain entity
- domain exceptions
- repository contracts

### `campaigns/infrastructure/`
Owns:
- DB model
- mapper
- concrete repositories

### `campaigns/usecase/`
Owns:
- command/query schemas
- command/query use cases
- factory wiring
- optional facade

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
