# Implementation Guidelines for BULMA

## When adding or modifying an endpoint

1. Update corresponding router in `src/api/**/routes.py`
2. Reuse existing schema/use case if possible
3. If new application behavior is needed, implement in module `usecase/`
4. If new business rule is needed, evaluate if it belongs in `domain/`
5. If persistence translation changes, update mapper/repository in `infrastructure/`
6. Preserve response wrapper format
7. Update docs if behavior or structure changed

## When adding a new business rule

Decision order:
1. If semantic invariant/state rule → `domain/`
2. If process sequencing/orchestration → `usecase/`
3. If storage/query/mapping detail → `infrastructure/`
4. If request/response adaptation only → `api/`

## When creating new files

Prefer extending an existing module if the responsibility already exists.
Create a new module only if there is a clearly new business capability.

## Naming behavior

- Preserve existing naming unless explicit refactor task exists
- Do not silently rename `unitys` / `unittys_types` / `users_residents`
- Do not collapse `users` and `core_users` without explicit design task

## Mapper rule

If a domain entity needs data from ORM:
- add/update mapper in infrastructure
- do not import DB model into domain

## Use case rule

Use case may coordinate:
- load entity
- validate preconditions
- call repository
- return entity/result

Use case should not:
- embed HTTP logic
- expose raw ORM objects to API layer
- become a dumping ground for every rule

## Documentation rule

If you alter architecture, module responsibilities, or change patterns:
- update `docs/architecture.md`
- update `docs/observations/` when useful for humans
- update `docs/BULMA/` if agent guidance changed
