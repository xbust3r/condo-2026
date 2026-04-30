"""
Rename core_unities → core_units and core_unities_types → core_unit_types

Also renames:
  - unity_type_id → unit_type_id on core_units
  - Indexes prefixed with core_unities_* → core_units_*

Revision ID: 010_rename_core_units
Revises: 008_refactor_core_unities
Create Date: 2026-04-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '010_rename_core_units'
down_revision: Union[str, None] = '009_rename_core_unities'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _index_exists(index_name: str, table: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND INDEX_NAME = :index_name
        """),
        {"table": table, "index_name": index_name},
    )
    return result.scalar() > 0


def _table_exists(table: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
        """),
        {"table": table},
    )
    return result.scalar() > 0


def _column_exists(table: str, column: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME = :column
        """),
        {"table": table, "column": column},
    )
    return result.scalar() > 0


def _fk_exists_for_column(table: str, column: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME = :column
              AND REFERENCED_TABLE_NAME IS NOT NULL
        """),
        {"table": table, "column": column},
    )
    return result.scalar() > 0


# ---------------------------------------------------------------------------
# UPGRADE
# ---------------------------------------------------------------------------

def upgrade() -> None:
    conn = op.get_bind()

    # ------------------------------------------------------------------
    # 1. Rename core_unities → core_units
    # ------------------------------------------------------------------
    if _table_exists('core_unities') and not _table_exists('core_units'):
        op.execute("RENAME TABLE `core_unities` TO `core_units`")

    # ------------------------------------------------------------------
    # 2. Rename core_unities_types → core_unit_types
    # ------------------------------------------------------------------
    if _table_exists('core_unities_types') and not _table_exists('core_unit_types'):
        op.execute("RENAME TABLE `core_unities_types` TO `core_unit_types`")

    # ------------------------------------------------------------------
    # 3. Rename unity_type_id → unit_type_id in core_units
    # ------------------------------------------------------------------
    if _table_exists('core_units') and _column_exists('core_units', 'unity_type_id'):
        op.execute("ALTER TABLE `core_units` CHANGE COLUMN `unity_type_id` `unit_type_id` BIGINT NULL")

    # ------------------------------------------------------------------
    # 4. Rename indexes — core_unities → core_units
    # ------------------------------------------------------------------
    index_renames = [
        ('ux_core_unities_building_unit_number', 'ux_core_units_building_unit_number'),
        ('ux_core_unities_building_code', 'ux_core_units_building_code'),
        ('ix_core_unities_building_status', 'ix_core_units_building_status'),
        ('ix_core_unities_building_sort', 'ix_core_units_building_sort'),
        ('ix_core_unities_building_floor', 'ix_core_units_building_floor'),
        ('ix_core_unities_building_occupancy', 'ix_core_units_building_occupancy'),
        ('ix_core_unities_status', 'ix_core_units_status'),
    ]

    for old_idx, new_idx in index_renames:
        if _index_exists(old_idx, 'core_units') and not _index_exists(new_idx, 'core_units'):
            op.execute(f"ALTER TABLE `core_units` RENAME INDEX `{old_idx}` TO `{new_idx}`")

    # ------------------------------------------------------------------
    # 5. Rename indexes — core_unities_types → core_unit_types
    #    (FK indexes on unity_type_id in core_units)
    # ------------------------------------------------------------------
    # The FK index name depends on MySQL; rename by finding any index on unit_type_id
    # referencing the old table. We just rename the table name in the FK constraint.
    # MySQL auto-names FK indexes; check and rename if needed.
    # Note: FK constraints from core_units → core_unities_types need to be updated.
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 6. Update FK constraint on core_units referencing core_unities_types
    # ------------------------------------------------------------------
    # Check if FK still references old table name
    if _table_exists('core_units'):
        result = conn.execute(
            sa.text("""
                SELECT CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'core_units'
                  AND REFERENCED_TABLE_NAME = 'core_unities_types'
            """)
        )
        fk_rows = result.fetchall()
        for row in fk_rows:
            constraint_name = row[0]
            column_name = row[1]
            # Drop old FK and recreate with new table name
            op.execute(
                f"ALTER TABLE `core_units` DROP FOREIGN KEY `{constraint_name}`"
            )
            op.execute(
                f"ALTER TABLE `core_units` ADD CONSTRAINT `{constraint_name}` "
                f"FOREIGN KEY (`{column_name}`) REFERENCES `core_unit_types`(`id`)"
            )

    # ------------------------------------------------------------------
    # 7. Update FK in users_residents referencing core_unities → core_units
    # ------------------------------------------------------------------
    if _table_exists('users_residents'):
        result = conn.execute(
            sa.text("""
                SELECT CONSTRAINT_NAME, COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'users_residents'
                  AND REFERENCED_TABLE_NAME = 'core_unities'
            """)
        )
        fk_rows = result.fetchall()
        for row in fk_rows:
            constraint_name = row[0]
            column_name = row[1]
            op.execute(
                f"ALTER TABLE `users_residents` DROP FOREIGN KEY `{constraint_name}`"
            )
            op.execute(
                f"ALTER TABLE `users_residents` ADD CONSTRAINT `{constraint_name}` "
                f"FOREIGN KEY (`{column_name}`) REFERENCES `core_units`(`id`)"
            )


# ---------------------------------------------------------------------------
# DOWNGRADE
# ---------------------------------------------------------------------------

def downgrade() -> None:
    conn = op.get_bind()

    # ------------------------------------------------------------------
    # 1. Revert FK on core_units → core_unit_types back to old name
    # ------------------------------------------------------------------
    if _table_exists('core_units'):
        result = conn.execute(
            sa.text("""
                SELECT CONSTRAINT_NAME, COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'core_units'
                  AND REFERENCED_TABLE_NAME = 'core_unit_types'
            """)
        )
        fk_rows = result.fetchall()
        for row in fk_rows:
            constraint_name = row[0]
            column_name = row[1]
            op.execute(
                f"ALTER TABLE `core_units` DROP FOREIGN KEY `{constraint_name}`"
            )
            op.execute(
                f"ALTER TABLE `core_units` ADD CONSTRAINT `{constraint_name}` "
                f"FOREIGN KEY (`{column_name}`) REFERENCES `core_unities_types`(`id`)"
            )

    # ------------------------------------------------------------------
    # 2. Revert FK in users_residents back to core_unities
    # ------------------------------------------------------------------
    if _table_exists('users_residents'):
        result = conn.execute(
            sa.text("""
                SELECT CONSTRAINT_NAME, COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'users_residents'
                  AND REFERENCED_TABLE_NAME = 'core_units'
            """)
        )
        fk_rows = result.fetchall()
        for row in fk_rows:
            constraint_name = row[0]
            column_name = row[1]
            op.execute(
                f"ALTER TABLE `users_residents` DROP FOREIGN KEY `{constraint_name}`"
            )
            op.execute(
                f"ALTER TABLE `users_residents` ADD CONSTRAINT `{constraint_name}` "
                f"FOREIGN KEY (`{column_name}`) REFERENCES `core_unities`(`id`)"
            )

    # ------------------------------------------------------------------
    # 3. Rename unit_type_id → unity_type_id
    # ------------------------------------------------------------------
    if _table_exists('core_units') and _column_exists('core_units', 'unit_type_id'):
        op.execute("ALTER TABLE `core_units` CHANGE COLUMN `unit_type_id` `unity_type_id` BIGINT NULL")

    # ------------------------------------------------------------------
    # 4. Rename indexes back
    # ------------------------------------------------------------------
    index_renames = [
        ('ux_core_units_building_unit_number', 'ux_core_unities_building_unit_number'),
        ('ux_core_units_building_code', 'ux_core_unities_building_code'),
        ('ix_core_units_building_status', 'ix_core_unities_building_status'),
        ('ix_core_units_building_sort', 'ix_core_unities_building_sort'),
        ('ix_core_units_building_floor', 'ix_core_unities_building_floor'),
        ('ix_core_units_building_occupancy', 'ix_core_unities_building_occupancy'),
        ('ix_core_units_status', 'ix_core_unities_status'),
    ]

    for old_idx, new_idx in index_renames:
        if _index_exists(old_idx, 'core_units') and not _index_exists(new_idx, 'core_units'):
            op.execute(f"ALTER TABLE `core_units` RENAME INDEX `{old_idx}` TO `{new_idx}`")

    # ------------------------------------------------------------------
    # 5. Rename tables back
    # ------------------------------------------------------------------
    if _table_exists('core_unit_types') and not _table_exists('core_unities_types'):
        op.execute("RENAME TABLE `core_unit_types` TO `core_unities_types`")

    if _table_exists('core_units') and not _table_exists('core_unities'):
        op.execute("RENAME TABLE `core_units` TO `core_unities`")