# BULMA — documentación táctica para agentes de IA

Esta carpeta existe para reducir costo de contexto y ambigüedad.

## Objetivo

Dar a una agente como BULMA instrucciones compactas para modificar `condo-py` sin tener que traducir documentación humana extensa.

## Orden de lectura obligatorio

1. `architecture-rules.md`
2. `module-map.md`
3. `implementation-guidelines.md`
4. `anti-patterns.md`
5. `change-playbook.md`

## Reglas globales

- `docs/new-standard/` = referencia doctrinal, **no editar**.
- `docs/observations/` = documentación humana.
- `docs/BULMA/` = reglas operativas compactas.
- Preservar naming actual salvo task explícita de refactor.
- No inventar módulos nuevos si uno existente ya cubre la responsabilidad.
- No mezclar feature + refactor cosmético grande en una sola entrega.

## Modelo mental

- API adapta.
- UseCase orquesta.
- Domain decide semántica.
- Infrastructure implementa detalle técnico.
- Shared solo para cross-cutting real.
