"""seed core_buildings_types base catalog (idempotent upsert)

Revision ID: 003_seed_core_buildings_types
Revises: 002_refactor_core_buildings
Create Date: 2026-04-13

Seed data for core_buildings_types (base system types):
  - RESIDENTIAL (residencial)
  - COMMERCIAL (comercial)
  - MIXED (mixto)
  - SERVICES (servicios)

This seed is idempotent — uses INSERT ... ON DUPLICATE KEY UPDATE.
Safe to re-run; does NOT depend on COUNT(*) > 0.

The global UNIQUE(code) constraint exists at this point in the chain,
so the upsert is safe.  Migration 006 later adds scope columns and
re-upserts with is_system=1.
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '003_seed_core_buildings_types'
down_revision: Union[str, None] = '002_refactor_core_buildings'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


BASE_TYPES = [
    {
        "code": "RESIDENTIAL",
        "name": "Residencial",
        "description": (
            "Edificio de uso predominantemente residencial. "
            "Viviendas individuales o departamentos."
        ),
    },
    {
        "code": "COMMERCIAL",
        "name": "Comercial",
        "description": (
            "Edificio de uso comercial. "
            "Oficinas, locales o espacios de negocio."
        ),
    },
    {
        "code": "MIXED",
        "name": "Mixto",
        "description": (
            "Edificio con combinación de usos residenciales "
            "y comerciales en la misma estructura."
        ),
    },
    {
        "code": "SERVICES",
        "name": "Servicios",
        "description": (
            "Edificio destinado a prestación de servicios. "
            "Clínicas, universidades, centros de datos, etc."
        ),
    },
]


def upgrade() -> None:
    for bt in BASE_TYPES:
        op.execute(
            f"""
            INSERT INTO core_buildings_types
              (uuid, code, name, description, status, created_at, updated_at)
            VALUES
              (UUID(), :code, :name, :description, 1, NOW(), NOW())
            ON DUPLICATE KEY UPDATE
              name        = VALUES(name),
              description = VALUES(description),
              updated_at  = NOW()
            """,
            {"code": bt["code"], "name": bt["name"], "description": bt["description"]},
        )


def downgrade() -> None:
    # Only reference columns that exist at this migration's level.
    # Columns added by 006 (is_system, condominium_id, etc.) don't exist yet.
    op.execute(
        "DELETE FROM core_buildings_types "
        "WHERE code IN ('RESIDENTIAL','COMMERCIAL','MIXED','SERVICES')"
    )
