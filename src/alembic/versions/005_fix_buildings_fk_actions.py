"""
Corrective migration: set explicit FK actions on core_buildings using raw SQL.

Problem: FK actions for core_buildings referencing core_condominiums and core_buildings_types
were documented but not guaranteed in the original migration.

Required FK actions:
  - condominium_id -> core_condominiums.id : ON DELETE RESTRICT
  - building_type_id -> core_buildings_types.id : ON DELETE SET NULL

Uses raw SQL to look up and modify FK constraints since MySQL auto-generates
constraint names that Alembic's drop_constraint cannot reliably predict.

Revision ID: 005_fix_buildings_fk_actions
Revises: 004_fix_buildings_unique_constraint
Create Date: 2026-04-13
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '005_fix_buildings_fk_actions'
down_revision: Union[str, None] = '004_fix_buildings_unique_constraint'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # === Step 1: Fix condominium_id FK -> RESTRICT ===

    # Find the current FK constraint name for condominium_id
    result = op.get_bind().execute(
        sa.text("""
            SELECT CONSTRAINT_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'core_buildings'
            AND COLUMN_NAME = 'condominium_id'
            AND REFERENCED_TABLE_NAME = 'core_condominiums'
            LIMIT 1
        """)
    )
    row = result.fetchone()
    if row:
        fk_name = row[0]
        op.execute(f"ALTER TABLE core_buildings DROP FOREIGN KEY `{fk_name}`")

    op.execute("""
        ALTER TABLE core_buildings
        ADD CONSTRAINT fk_buildings_condominium
        FOREIGN KEY (condominium_id)
        REFERENCES core_condominiums(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
    """)

    # === Step 2: Fix building_type_id FK -> SET NULL ===

    result2 = op.get_bind().execute(
        sa.text("""
            SELECT CONSTRAINT_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'core_buildings'
            AND COLUMN_NAME = 'building_type_id'
            AND REFERENCED_TABLE_NAME = 'core_buildings_types'
            LIMIT 1
        """)
    )
    row2 = result2.fetchone()
    if row2:
        fk_name2 = row2[0]
        op.execute(f"ALTER TABLE core_buildings DROP FOREIGN KEY `{fk_name2}`")

    op.execute("""
        ALTER TABLE core_buildings
        ADD CONSTRAINT fk_buildings_type
        FOREIGN KEY (building_type_id)
        REFERENCES core_buildings_types(id)
        ON DELETE SET NULL
        ON UPDATE SET NULL
    """)


def downgrade() -> None:
    # Drop named FKs
    op.execute("""
        ALTER TABLE core_buildings
        DROP FOREIGN KEY IF EXISTS fk_buildings_condominium,
        DROP FOREIGN KEY IF EXISTS fk_buildings_type
    """)

    # Recreate with MySQL defaults (no explicit actions)
    op.execute("""
        ALTER TABLE core_buildings
        ADD CONSTRAINT fk_buildings_condominium
        FOREIGN KEY (condominium_id)
        REFERENCES core_condominiums(id)
    """)
    op.execute("""
        ALTER TABLE core_buildings
        ADD CONSTRAINT fk_buildings_type
        FOREIGN KEY (building_type_id)
        REFERENCES core_buildings_types(id)
    """)