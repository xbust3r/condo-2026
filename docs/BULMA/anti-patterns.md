# Anti-patterns for BULMA

Do not do the following unless the task explicitly requires a targeted refactor.

## API anti-patterns

- put business rules in route handlers
- access DB session directly from router
- return raw ORM objects
- duplicate use case logic in endpoint functions

## Domain anti-patterns

- import `DB*` models into domain
- import FastAPI / HTTP classes into domain
- convert domain entity into transport object inside domain for framework reasons
- keep entities permanently anemic if a rule clearly belongs there

## Use case anti-patterns

- mix HTTP exception logic into use case
- mix SQLAlchemy model creation directly in use case if repository/mapper already owns it
- create one mega-use-case that owns all business semantics

## Infrastructure anti-patterns

- define business rules in repository
- make mapper decide domain policy
- leak session/ORM concerns upward unnecessarily

## Shared anti-patterns

- place module-specific helper in `shared/`
- treat `shared/` as misc folder
- hide unclear ownership by moving files to shared

## Project anti-patterns

- rename legacy terms during unrelated feature work
- combine feature delivery with broad cleanup without approval
- edit `docs/new-standard/` while updating current project docs
- invent architecture purity not reflected in current codebase
