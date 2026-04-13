"""
Corrective migration: replace global UNIQUE(code) with composite UNIQUE(condominium_id, code)

Problem: Migration 002 tried to drop an index with auto-generated name that may not exist.
This migration uses a safer, idempotent approach.

Revision ID: 004_fix_buildings_unique_constraint
Revises: 003_seed_core_buildings_types
Create Date: 2026-04-13
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '004_fix_buildings_unique_constraint'
down_revision: Union[str, None] = '003_seed_core_buildings_types'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Safe approach: check if old constraint/index exists, then replace
    # MySQL creates an index for UNIQUE constraints. The auto-generated name
    # is NOT predictable across MySQL versions. We use raw SQL to safely drop
    # any existing unique index on the 'code' column for core_buildings.

    # Step 1: Try to drop the old unique constraint using raw SQL (idempotent)
    # This handles cases where the constraint name differs from what 002 assumed
    op.execute("""
        ALTER TABLE core_buildings
        DROP INDEX IF EXISTS code,
        DROP INDEX IF EXISTS ix_core_buildings_code,
        DROP INDEX IF EXISTS uq_core_buildings_code
    """)

    # Step 2: Also try the Alembic-native approach for constraint drop
    # using the constraint name that SQLAlchemy typically generates
    try:
        op.drop_constraint(
            'core_buildings.code', 'core_buildings', type_='unique'
        )
    except Exception:
        # If Alembic approach fails (constraint not found), ignore
        # The raw SQL above already handled it
        pass

    # Step 3: Add the composite unique constraint (condominium_id, code)
    op.create_index(
        'ix_core_buildings_condominium_code',
        'core_buildings',
        ['condominium_id', 'code'],
        unique=True
    )


def downgrade() -> None:
    # Remove composite unique
    op.drop_index('ix_core_buildings_condominium_code', 'core_buildings')

    # Restore old global unique constraint on 'code'
    try:
        op.drop_constraint(
            'core_buildings.code', 'core_buildings', type_='unique'
        )
    except Exception:
        pass

    op.create_unique_constraint(
        'core_buildings.code', 'core_buildings', ['code']
    )