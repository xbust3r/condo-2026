# Module Map for BULMA

## Entry points

- `src/app.py` → FastAPI application setup
- `src/api/condominiums/routes.py`
- `src/api/buildings/routes.py`
- `src/api/buildings_types/routes.py`
- `src/api/unitys/routes.py`
- `src/api/unittys_types/routes.py`
- `src/api/users/routes.py`
- `src/api/residents/routes.py`

## Main DDD modules in active documentation

- `core_condominiums`
- `core_buildings`
- `core_buildings_types`
- `core_unitys`
- `core_unittys_types`
- `users`
- `users_residents`

## Additional modules detected in source tree

- `core_users`
- `core_users_residents`

## Important warning

Source tree contains naming duplication / inconsistency.
Do not normalize names opportunistically.
If task does not explicitly request naming refactor:
- preserve current import paths,
- preserve public route names,
- document inconsistency instead of renaming.

## Typical module internal structure

```text
module/
├── domain/
├── infrastructure/
└── usecase/
```

Possible split under `usecase/`:
- `cmd/`
- `query/`
- facade `*_usecase.py`
- factory `*_factory.py`

## Response contract

Common response wrapper lives in:
- `src/library/dddpy/shared/schemas/response_schema.py`

Expected shape:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": {},
  "errors": null
}
```
