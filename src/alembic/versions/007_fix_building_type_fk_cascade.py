"""
Corrective migration: change ON UPDATE action on core_buildings.building_type_id
from SET NULL to CASCADE.

Tarea 9: The FK on core_buildings.building_type_id must have:
  - ON DELETE SET NULL  (already correct from migration 005)
  - ON UPDATE CASCADE   (change from SET NULL)

Rationale: when a building_type PK changes, all buildings referencing it
should automatically point to the new PK. ON DELETE SET NULL protects
buildings when a type is removed.

Revision ID: 007_fix_building_type_fk_cascade
Revises: 006_add_building_types_scope
Create Date: 2026-04-13
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '007_fix_building_type_fk_cascade'
down_revision: Union[str, None] = '006_add_building_types_scope'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # Find current FK constraint name for building_type_id
    result = conn.execute(
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
    row = result.fetchone()
    if not row:
        # FK may not exist yet (e.g. fresh DB that hasn't run migrations)
        return

    fk_name = row[0]

    # Verify it currently has SET NULL on update (from migration 005)
    # If FK already has CASCADE, this is already applied — idempotent guard
    check = conn.execute(
        sa.text("""
            SELECT UPDATE_RULE
            FROM information_schema.REFERENTIAL_CONSTRAINTS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'core_buildings'
              AND CONSTRAINT_NAME = :fk_name
            LIMIT 1
        """),
        {"fk_name": fk_name},
    )
    rule_row = check.fetchone()
    if rule_row and rule_row[0] == 'CASCADE':
        return  # Already CASCADE, nothing to do

    # Drop and recreate with CASCADE on UPDATE
    conn.execute(f"ALTER TABLE core_buildings DROP FOREIGN KEY `{fk_name}`")
    conn.execute("""
        ALTER TABLE core_buildings
        ADD CONSTRAINT fk_buildings_type
        FOREIGN KEY (building_type_id)
        REFERENCES core_buildings_types(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
    """)


def downgrade() -> None:
    conn = op.get_bind()

    result = conn.execute(
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
    row = result.fetchone()
    if not row:
        return

    fk_name = row[0]

    conn.execute(f"ALTER TABLE core_buildings DROP FOREIGN KEY `{fk_name}`")
    conn.execute("""
        ALTER TABLE core_buildings
        ADD CONSTRAINT fk_buildings_type
        FOREIGN KEY (building_type_id)
        REFERENCES core_buildings_types(id)
        ON DELETE SET NULL
        ON UPDATE SET NULL
    """)
