# Sprint 13 — `core_votes` — Digital Voting System

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable arquitectura:** Lelouch vi Britannia
**Responsable implementación:** Lelouch + sub-agentes

---

## Overview

Sistema de votaciones digitales para decisiones de condominio. Permite crear votaciones formales con quórum, mayorías definidas, votos secretos o abiertos, y resultados automatizados.

**Casos de uso:**
- Asamblea extraordinaria (votación urgente)
- Votación de presupuesto anual
- Aprobación de reglamento
- Elección de directorio

---

## Modelo de Datos

### `VoteEntity`

```
VoteEntity
├── id: int
├── uuid: str
├── condominium_id: int
├── title: str
├── description: text
├── meeting_id: int (nullable —null si es votación standalone)
├── voting_starts_at: datetime
├── voting_ends_at: datetime
├── status: VoteStatus
├── vote_type: VoteType      ← open, secret
├── quorum_required: bool   ← si requiere quórum
├── quorum_percentage: int   ← % requerido (default 50+1)
├── approval_threshold: int  ← % de aprobación (default mayoría simple 50+1)
├── total_eligible_voters: int
├── total_votes_cast: int
├── total_yes_votes: int
├── total_no_votes: int
├── total_abstain_votes: int
├── result_proclaimed_at: datetime (nullable)
├── created_by_user_id: int
├── created_at, updated_at, deleted_at
└── Enrichment: created_by_user_full_name, condominium_name
```

### `VoteOptionEntity`

```
VoteOptionEntity
├── id: int
├── vote_id: int
├── option_text: str          ← "Sí", "No", "Abstención", o texto custom
├── option_key: str          ← "yes", "no", "abstain", "option_1", etc.
├── vote_count: int = 0
```

### Enums

**VoteStatus:**
```
draft       → creado, no publicado
active     → en período de votación
closed     → período terminado, esperando proclamación
approved  → aprobado (resultados certificados)
rejected   → rechazado
cancelled  → cancelado por admin
```

**VoteType:**
```
open       → votos visibles para admins
secret     → conteo anónimo (solo auditores ven resultados)
```

---

## Reglas de Negocio

**VOT-01 — Quórum:** Si `quorum_required=True`, solo se proclama resultado si `total_votes_cast / total_eligible_voters >= quorum_percentage / 100`. Si no se alcanza quórum → estado `closed` sin proclamación, se requiere nueva votación.

**VOT-02 — Aprobación:** Si quórum se satisface (o no es requerido):
- `approved` si `yes_votes / (yes + no) >= approval_threshold / 100`
- `rejected` otherwise

**VOT-03 — Elegibilidad:** Solo usuarios con rol `condominium_admin`, `board_member` o con `ownership` activo pueden votar. No pueden votar `maintenance_staff`, `security_staff`, ni `tenants` (a menos que los estatutos lo permitan — configurable por `vote_type`).

**VOT-04 — Un voto por usuario:** Cada usuario puede emitir exactamente un voto por votación. Voto irrevocable una vez emitido (no se puede cambiar).

**VOT-05 — Voto secreto:** Si `vote_type=secret`, ni siquiera los admins ven el desglose por usuario. Solo ven el conteo agregado al cerrar.

**VOT-06 — Extensión:** Un admin puede extender `voting_ends_at` antes de que venza. No se puede acortar.

---

## Estructura DDD

```
src/library/dddpy/core_votes/
├── domain/
│   ├── vote_entity.py         ← VoteEntity + VoteOptionEntity
│   ├── vote_exception.py
│   ├── vote_repository.py     ← ABC cmd
│   └── vote_query_repository.py ← ABC query
├── infrastructure/
│   ├── dbvote.py              ← SQLAlchemy models (core_votes + core_vote_options)
│   ├── vote_mapper.py
│   ├── vote_cmd_repository.py
│   └── vote_query_repository.py ← con _bulk_enrich
├── usecase/
│   ├── vote_cmd_schema.py
│   ├── vote_cmd_usecase.py
│   ├── vote_query_usecase.py
│   └── vote_factory.py
└── api/
    └── votes/routes_votes.py
```

### Migración

```sql
CREATE TABLE core_votes (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  uuid VARCHAR(36) NOT NULL UNIQUE,
  condominium_id BIGINT NOT NULL,
  meeting_id BIGINT NULL,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  voting_starts_at DATETIME NOT NULL,
  voting_ends_at DATETIME NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'draft',
  vote_type VARCHAR(20) NOT NULL DEFAULT 'open',
  quorum_required BOOLEAN NOT NULL DEFAULT FALSE,
  quorum_percentage INT NOT NULL DEFAULT 51,
  approval_threshold INT NOT NULL DEFAULT 51,
  total_eligible_voters INT NOT NULL DEFAULT 0,
  total_votes_cast INT NOT NULL DEFAULT 0,
  total_yes_votes INT NOT NULL DEFAULT 0,
  total_no_votes INT NOT NULL DEFAULT 0,
  total_abstain_votes INT NOT NULL DEFAULT 0,
  result_proclaimed_at DATETIME NULL,
  created_by_user_id BIGINT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT NOW(),
  updated_at DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  deleted_at DATETIME NULL,
  FOREIGN KEY (condominium_id) REFERENCES core_condominiums(id),
  FOREIGN KEY (meeting_id) REFERENCES core_meetings(id), -- cuando exista
  FOREIGN KEY (created_by_user_id) REFERENCES users(id),
  INDEX idx_condo_status (condominium_id, status),
  INDEX idx_ends (voting_ends_at),
);

CREATE TABLE core_vote_options (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  vote_id BIGINT NOT NULL,
  option_text VARCHAR(100) NOT NULL,
  option_key VARCHAR(20) NOT NULL,
  vote_count INT NOT NULL DEFAULT 0,
  FOREIGN KEY (vote_id) REFERENCES core_votes(id) ON DELETE CASCADE,
  UNIQUE KEY uk_vote_option (vote_id, option_key)
);

CREATE TABLE core_vote_records (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  vote_id BIGINT NOT NULL,
  user_id BIGINT NOT NULL,
  option_key VARCHAR(20) NOT NULL,
  voted_at DATETIME NOT NULL DEFAULT NOW(),
  FOREIGN KEY (vote_id) REFERENCES core_votes(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id),
  UNIQUE KEY uk_vote_user (vote_id, user_id)
);
```

---

## Endpoints

| Método | Endpoint | Permiso | Descripción |
|---|---|---|---|
| POST | `/votes` | Admin | Crear votación |
| GET | `/votes` | Auth | Listar (filtros: condo, status) |
| GET | `/votes/{id}` | Auth | Detalle |
| GET | `/votes/uuid/{uuid}` | Auth | Por UUID |
| GET | `/condominiums/{id}/votes` | Auth | Por condominio (paginados) |
| PATCH | `/votes/{id}` | Admin | Editar (solo draft, extiende ends si ya empieza) |
| POST | `/votes/{id}/publish` | Admin | Publicar (draft → active) |
| POST | `/votes/{id}/cancel` | Admin | Cancelar |
| POST | `/votes/{id}/cast` | Voter | Emitir voto (VOT-03/04) |
| GET | `/votes/{id}/results` | Auth | Ver resultados (aggregados, secretos solo como aggregate) |
| POST | `/votes/{id}/proclaim` | Admin | Proclamar resultado |
| GET | `/votes/{id}/records` | Admin/open | Registro de votos (solo si vote_type=open) |

---

## Queries enriquecidas (M-12)

Mismo patrón `_bulk_enrich`: `created_by_user_full_name`, `condominium_name`

---

## RBAC

```
votes:create    → crear votaciones
votes:read      → ver votaciones y resultados
votes:vote      → emitir voto
votes:proclaim  → proclamar resultados (admin)
votes:cancel    → cancelar votaciones
```

---

## Tasks

| Task | Descripción |
|---|---|
| T-1 | Migración 046 `core_votes` + `core_vote_options` + `core_vote_records` |
| T-2 | DDD domain layer |
| T-3 | Infrastructure + _bulk_enrich |
| T-4 | Usecases (VOT-01 a VOT-06 implementados) |
| T-5 | API routes |
| T-6 | Seed RBAC permissions |
