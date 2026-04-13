"""
Idempotent fix: replace global UNIQUE(code) with composite UNIQUE(condominium_id, code)

Problem: 002_refactor_core_buildings.py has a known issue where MySQL's
auto-generated constraint/index names don't match what Alembic's drop_* expects.
This migration fixes that using raw SQL with IF EXISTS.

Note: This migration does NOT modify FK actions. FK actions are handled by 005.

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
    # Use raw SQL to safely remove any existing global unique index on 'code'.
    # IF EXISTS prevents errors on clean environments where the index doesn't exist.
    # We try multiple common index name patterns since MySQL auto-generates names.
    op.execute("""
        ALTER TABLE core_buildings
        DROP INDEX IF EXISTS `code`,
        DROP INDEX IF EXISTS ix_core_buildings_code,
        DROP INDEX IF EXISTS uq_core_buildings_code,
        DROP INDEX IF EXISTS core_buildings_code_uq
    """)

    # Add the composite unique constraint
    op.create_index(
        'ix_core_buildings_condominium_code',
        'core_buildings',
        ['condominium_id', 'code'],
        unique=True
    )


def downgrade() -> None:
    op.drop_index('ix_core_buildings_condominium_code', 'core_buildings')
    # Restore global unique constraint (MySQL will auto-generate index name)
    op.create_unique_constraint(
        'core_buildings.code', 'core_buildings', ['code']
    )