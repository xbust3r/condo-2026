"""
Idempotent safety-net migration: ensure composite UNIQUE exists on (condominium_id, code)

Purpose: On a clean upgrade chain (001->002->003->004), 002 already creates
ix_core_buildings_condominium_code. This migration is a no-op in that case.

On environments where 002 didn't create the index (partial/failed upgrade), 004
creates it as fallback. This makes 004 always safe to run — never fails due to
duplicate index, never fails due to missing index on downgrade.

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
    # Only create composite index if it doesn't already exist.
    # 002 already creates ix_core_buildings_condominium_code, so on a clean
    # upgrade chain (001->002->003->004) this is a no-op.
    # This migration serves as safety net for environments where 002
    # didn't run cleanly and the composite index is missing.
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'core_buildings'
              AND INDEX_NAME = 'ix_core_buildings_condominium_code'
        """)
    )
    if result.scalar() == 0:
        op.create_index(
            'ix_core_buildings_condominium_code',
            'core_buildings',
            ['condominium_id', 'code'],
            unique=True
        )


def downgrade() -> None:
    # Idempotent: only drop if index exists
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'core_buildings'
              AND INDEX_NAME = 'ix_core_buildings_condominium_code'
        """)
    )
    if result.scalar() > 0:
        op.drop_index('ix_core_buildings_condominium_code', 'core_buildings')

    # Restore global unique constraint (MySQL will auto-generate index name)
    op.create_unique_constraint(
        'core_buildings.code', 'core_buildings', ['code']
    )