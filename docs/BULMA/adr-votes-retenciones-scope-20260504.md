# ADR — Votaciones: Retenciones, Tipos de Conteo y Scope por Edificio

**Fecha:** 2026-05-04
**Estado:** Propuesto
**Arquitecto:** Misato Katsuragi
**Implementación:** Bulma (Dev), Lelouch (Architect)

---

## Contexto

El módulo `core_votes` está implementado con las reglas VOT-01 a VOT-06 básicas:

- Quórum configurable
- Aprobación por umbral
- Un voto por usuario
- Voto abierto/secreto
- Extensión de plazos

**Lo que falta y el negocio necesita:**

1. **Regla de retenciones:** Solo propietarios que no excedan N meses de deuda pueden votar. El umbral es configurable por votación/condominio.
2. **Tipos de conteo:**
   - `BY_UNIT`: 1 voto por unidad/departamento (cada ownership activo = 1 voto)
   - `BY_COEFFICIENT`: voto ponderado por coeficiente de participación (opcional incluir estacionamiento y anexas)
3. **Scope de votación:**
   - `CONDOMINIUM`: votan todos los propietarios del condominio
   - `BUILDING`: votan solo propietarios de un edificio específico

---

## Decisiones

### DECISIÓN 1 — Nombre del módulo de deuda

**Opción A:** `core_arrears` (éxitos/cuotas vencidas)
**Opción B:** `core_retenciones` (retenciones/deuda)
**Opción C:** `core_withholdings`

**Resolución: Opción A — `core_arrears`**

"Razones" no es un nombre de dominio de negocio en español para contextos multilingual. "Arrears" es el término técnico estándar en sistemas de propiedad horizontal (AppFolio, Buildium). Mantiene coherencia con naming en inglés del codebase.

---

### DECISIÓN 2 — Fuente de datos de deuda

La deuda de un propietario puede venir de:
- Módulo `core_accounts_receivable` existente (cuentas por cobrar)
- Tabla resumen nueva `core_unit_arrears_summary`
- Integración con sistema AR/ERP externo

**Resolución: Interface `ArrearsReader` + implementación desde `core_accounts_receivable`**

```
core_votes/domain/
  └── voter_eligibility_policy.py   ← interface abstracta

core_votes/infrastructure/
  └── debt_based_eligibility_provider.py  ← implementación concreta
       consulta core_accounts_receivable para meses de deuda

core_arrears/                        ← módulo nuevo (si se necesita tabla resumen)
  └── ...
```

El `VoteCmdUseCase` recibe inyectada la policy de elegibilidad. No se acopla `core_votes` a `core_arrears`.

---

### DECISIÓN 3 — Tabla de configuración de reglas de votación

Se crea `core_voting_rules`:

```sql
CREATE TABLE core_voting_rules (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    uuid VARCHAR(36) NOT NULL UNIQUE,
    condominium_id BIGINT NOT NULL,
    building_id BIGINT NULL,              -- null = aplica a todo el condominio
    name VARCHAR(100) NOT NULL,
    -- Eligibility
    owners_only BOOLEAN NOT NULL DEFAULT TRUE,  -- TRUE = solo propietarios
    max_debt_months INT NOT NULL DEFAULT 2,      -- 0 = sin límite
    allow_tenants BOOLEAN NOT NULL DEFAULT FALSE,
    -- Vote calculation
    vote_calculation_type VARCHAR(20) NOT NULL DEFAULT 'BY_UNIT',
    -- BY_COEFFICIENT options
    include_parking BOOLEAN NOT NULL DEFAULT FALSE,
    include_annexes BOOLEAN NOT NULL DEFAULT FALSE,
    -- Scope
    scope_type VARCHAR(20) NOT NULL DEFAULT 'CONDOMINIUM',
    -- Audits
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by_user_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    deleted_at DATETIME NULL,
    INDEX idx_condo_building (condominium_id, building_id),
    INDEX idx_active (condominium_id, is_active)
);
```

**Nota:** Esta tabla se asocia a la votación en el momento de creación — es un **snapshot**. Si las reglas cambian después, las votaciones activas no mutan.

---

### DECISIÓN 4 — Tipo de cálculo de voto

```python
class VoteCalculationType(str, Enum):
    BY_UNIT = "by_unit"           # 1 voto por unit_ownership activo
    BY_COEFFICIENT = "by_coefficient"  # voto ponderado por coeficiente
```

**BY_UNIT:**
- Cada `unit_ownership` activo con estado "active" = 1 voto
- Si un propietario tiene 3 departamentos, tiene 3 votos
- Se persiste `vote_record` por `unit_ownership_id` (no solo por `user_id`)

**BY_COEFFICIENT:**
- Cada propietario emite UNA acción de voto
- El peso de su voto = suma de coeficientes de sus unidades
- Opcional: incluir coeficientes de estacionamientos (`include_parking`) y anexos (`include_annexes`)
- El coeficiente se consulta de `core_units.coefficient` o `core_buildings.coefficient` según configuración

---

### DECISIÓN 5 — Scope de votación

```python
class VoteScopeType(str, Enum):
    CONDOMINIUM = "condominium"   # todos los propietarios del condominio
    BUILDING = "building"         # solo propietarios de un edificio
```

- En `CreateVoteSchema` se agrega `scope_type` y `building_id` (nullable)
- Si `scope_type = BUILDING`, `building_id` es obligatorio
- El universo electoral se filtra por scope al momento de definir elegibles

---

### DECISIÓN 6 — Clave única para evitar doble voto

En `core_vote_records`, cambiar constraint de:

```
UNIQUE KEY uk_vote_user (vote_id, user_id)
```

a:

```
UNIQUE KEY uk_vote_unit_ownership (vote_id, unit_ownership_id)
```

Esto permite que en modo BY_UNIT, un mismo usuario con múltiples units emita múltiples votos (uno por unit).

---

### DECISIÓN 7 — Migración del schema existente

Se requieren migraciones nuevas:

- `048_create_core_voting_rules` — tabla de configuración
- `049_create_core_arrears` — módulo de deuda (si no se integra con AR existente)
- `050_alter_core_vote_records` — agregar `unit_ownership_id` nullable
- `051_extend_core_votes` — agregar `scope_type`, `vote_calculation_type`, `voting_rule_id` (snapshot)

---

### DECISIÓN 8 — Elección de voting_rule al crear votación

- Si el condominio tiene una `voting_rule` activa para el scope elegido, se usa esa
- Si no existe, se usa un **default inline** (los valores actuales de `CreateVoteSchema` se mantienen como fallback)
- El snapshot se almacena en `core_votes.voting_rule_snapshot` como JSON

---

## Arquitectura propuesta

```
src/library/dddpy/
├── core_votes/
│   ├── domain/
│   │   ├── vote_entity.py           ← VoteEntity, VoteOptionEntity
│   │   ├── vote_enums.py            ← VoteStatus, VoteType, VoteCalculationType, VoteScopeType
│   │   ├── voter_eligibility_policy.py  ← ABC: is_eligible(user, vote) -> (bool, reason)
│   │   └── ...
│   ├── infrastructure/
│   │   ├── dbvote.py                ← DBVote, DBVoteOption, DBVoteRecord
│   │   ├── dbvotingrule.py          ← DBVotingRule
│   │   ├── debt_based_eligibility_provider.py  ← VoterEligibilityPolicy implementation
│   │   └── vote_cmd_repository.py   ← actualizado
│   └── usecase/
│       ├── vote_cmd_schema.py       ← CreateVoteSchema actualizado
│       └── vote_cmd_usecase.py      ← con eligibility policy inyectada

src/library/dddpy/core_arrears/           ← NUEVO
├── domain/
│   ├── arrears_entity.py
│   ├── arrears_reader.py             ← ABC interface
│   └── arrears_exception.py
├── infrastructure/
│   ├── arrears_sql_repository.py      ← implementación desde core_accounts_receivable
│   └── db_arrears_summary.py
└── usecase/
    └── arrears_query_usecase.py

src/library/dddpy/core_voting_rules/     ← NUEVO (o integrado en core_votes)
├── domain/
│   ├── voting_rule_entity.py
│   └── voting_rule_repository.py
├── infrastructure/
│   └── ...
└── usecase/
    └── ...
```

---

## Reglas de negocio resumidas

| Regla | Descripción | Implementación |
|---|---|---|
| `owners_only` | Solo propietarios votan | `DebtBasedEligibilityProvider` + ownership check |
| `max_debt_months` | Límite de deuda para votar | `ArrearsReader.get_months_debt(ownership_id)` ≤ `max_debt_months` |
| `allow_tenants` | Inquilinos pueden votar (si/no) | check en eligibility policy |
| `vote_calculation_type=BY_UNIT` | 1 voto por unit_ownership | persistir por `unit_ownership_id` |
| `vote_calculation_type=BY_COEFFICIENT` | Voto ponderado por coeficiente | peso = `sum(units.coefficient)` |
| `include_parking` | Incluir estacionamiento en coeficiente | boolean en weight calculation |
| `scope_type=CONDOMINIUM` | Votan todos los del condominio | filter por `condominium_id` |
| `scope_type=BUILDING` | Votan solo los del edificio | filter por `building_id` |

---

## Casos de prueba mínimos

| # | Escenario | Resultado esperado |
|---|---|---|
| 1 | Propietario con 0 meses deuda, ownership activo | Elegible |
| 2 | Propietario con 2 meses deuda, `max_debt_months=2` | Elegible |
| 3 | Propietario con 3 meses deuda, `max_debt_months=2` | No elegible (deuda_excede) |
| 4 | Inquilino, `allow_tenants=False` | No elegible (no_es_propietario) |
| 5 | Inquilino, `allow_tenants=True` | Elegible (sujeto a deuda) |
| 6 | Propietario multi-unidad, `BY_UNIT` | 2 votos (uno por cada ownership) |
| 7 | Propietario multi-unidad, `BY_COEFFICIENT` | 1 voto, peso = suma de coeficientes |
| 8 | Votación scope=CONDOMINIUM, usuario de edificio A | Puede votar |
| 9 | Votación scope=BUILDING, usuario de edificio B | No elegible (fuera_de_scope) |
| 10 | Ya votó (unit_ownership_id duplicado) | `AlreadyVoted` |

---

## Orden de ejecución

1. **Migraciones** — `048`, `049`, `050`, `051`
2. **Domain** — `VoteCalculationType`, `VoteScopeType`, `VoterEligibilityPolicy` ABC
3. **`core_arrears`** — Entity + `ArrearsReader` + implementación desde AR
4. **`core_voting_rules`** — Entity + repositorio + seed data
5. **Eligibility provider** — `DebtBasedEligibilityProvider`
6. **Update `VoteEntity`** — agregar campos de scope y snapshot
7. **Update `VoteCmdUseCase`** — inyectar policy, implementar nuevas reglas
8. **Update API** — `CreateVoteSchema` con nuevos campos
9. **Tests**
10. **Docs**

---

## Effort estimate

| Phase | Task | Hours |
|---|---|---|
| Migrations | 048-051 | 1h |
| Domain | Enums + policy ABC | 30min |
| core_arrears | Entity + reader | 2h |
| core_voting_rules | Entity + repo | 1.5h |
| Eligibility provider | Implementation | 1h |
| VoteEntity + UseCase | Actualización | 2h |
| API + routes | Actualización | 1.5h |
| Tests | Casos de prueba | 3h |
| **Total** | | **~12.5h** |

---

## Notas

- El snapshot de reglas en `core_votes` evita que cambios en las reglas muten votaciones activas
- La interface `VoterEligibilityPolicy` permite cambiar la fuente de deuda sin tocar `core_votes`
- El campo `unit_ownership_id` en `core_vote_records` es backward-compatible: es nullable (votos viejos no lo tienen) y el código actual sigue funcionando
- `include_parking` y `include_annexes` aplican solo a `BY_COEFFICIENT`

---

*Misato coordina, Bulma ejecuta, Lelouch valida al cierre.*