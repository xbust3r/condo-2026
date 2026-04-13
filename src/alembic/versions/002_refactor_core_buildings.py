"""refactor core_buildings schema

Revision ID: 002_refactor_core_buildings
Revises: 001_create_initial
Create Date: 2026-04-13

Changes:
- Drop: type, size, percentage
- Add: short_name, built_area, common_area, coefficient,
       floors_count, basements_count, units_planned, sort_order
- Add: deleted_at (soft delete)
- Replace global UNIQUE(code) with UNIQUE(condominium_id, code)
- Add CHECK constraints for numeric fields
- Add strategic indexes

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_refactor_core_buildings'
down_revision: Union[str, None] = '001_create_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # === STEP 1: Safely drop old global UNIQUE constraint on code ===
    # MySQL/SQLAlchemy auto-generates constraint and index names.
    # The UNIQUE constraint on column 'code' creates a MySQL index named 'code'.
    # Alembic's drop_constraint('core_buildings.code', ...) FAILS because the
    # actual constraint name is not 'core_buildings.code' — it's auto-generated.
    #
    # Solution: Query information_schema to find the actual constraint name,
    # then drop it dynamically. Also try DROP INDEX IF EXISTS for the index.
    # This is fully idempotent — safe on clean install AND upgraded envs.
    #
    # MySQL 8.0.29+ supports DROP INDEX IF EXISTS.
    result = op.get_bind().execute(
        sa.text("""
            SELECT c.CONSTRAINT_NAME
            FROM information_schema.TABLE_CONSTRAINTS c
            JOIN information_schema.KEY_COLUMN_USAGE k
              ON c.CONSTRAINT_NAME = k.CONSTRAINT_NAME
              AND c.TABLE_SCHEMA = k.TABLE_SCHEMA
              AND c.TABLE_NAME = k.TABLE_NAME
            WHERE c.TABLE_SCHEMA = DATABASE()
              AND c.TABLE_NAME = 'core_buildings'
              AND c.CONSTRAINT_TYPE = 'UNIQUE'
              AND k.COLUMN_NAME = 'code'
            LIMIT 1
        """)
    )
    row = result.fetchone()
    if row:
        fk_constraint_name = row[0]
        op.execute(f"ALTER TABLE core_buildings DROP INDEX `{fk_constraint_name}`")

    # Also try DROP INDEX IF EXISTS for the auto-named index (MySQL 8.0.29+)
    # This handles the case where the index exists but constraint query returned nothing
    op.execute("""
        ALTER TABLE core_buildings
        DROP INDEX IF EXISTS `code`,
        DROP INDEX IF EXISTS ix_core_buildings_code,
        DROP INDEX IF EXISTS uq_core_buildings_code,
        DROP INDEX IF EXISTS core_buildings_code_uq
    """)

    # === STEP 2: Drop deprecated columns ===
    op.drop_column('core_buildings', 'type')
    op.drop_column('core_buildings', 'size')
    op.drop_column('core_buildings', 'percentage')

    # === STEP 3: Add new columns ===
    op.add_column(
        'core_buildings',
        sa.Column('short_name', sa.String(50), nullable=True)
    )
    op.add_column(
        'core_buildings',
        sa.Column('built_area', sa.DECIMAL(12, 4), nullable=True)
    )
    op.add_column(
        'core_buildings',
        sa.Column('common_area', sa.DECIMAL(12, 4), nullable=True)
    )
    op.add_column(
        'core_buildings',
        sa.Column('coefficient', sa.DECIMAL(9, 6), nullable=True)
    )
    op.add_column(
        'core_buildings',
        sa.Column('floors_count', sa.Integer(), nullable=False, server_default='0')
    )
    op.add_column(
        'core_buildings',
        sa.Column('basements_count', sa.Integer(), nullable=False, server_default='0')
    )
    op.add_column(
        'core_buildings',
        sa.Column('units_planned', sa.Integer(), nullable=False, server_default='0')
    )
    op.add_column(
        'core_buildings',
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0')
    )
    op.add_column(
        'core_buildings',
        sa.Column(
            'deleted_at',
            sa.DateTime(),
            nullable=True
        )
    )

    # === STEP 4: Add composite unique constraint (condominium_id, code) ===
    op.create_index(
        'ix_core_buildings_condominium_code',
        'core_buildings',
        ['condominium_id', 'code'],
        unique=True
    )

    # === STEP 5: Add strategic indexes ===
    # Single-column indexes for FK lookups
    op.create_index(
        'ix_core_buildings_condominium_id',
        'core_buildings',
        ['condominium_id']
    )
    op.create_index(
        'ix_core_buildings_building_type_id',
        'core_buildings',
        ['building_type_id']
    )
    op.create_index(
        'ix_core_buildings_status',
        'core_buildings',
        ['status']
    )
    # Composite index for filtered listings
    op.create_index(
        'ix_core_buildings_condominium_status',
        'core_buildings',
        ['condominium_id', 'status']
    )
    # Index for sorted queries (visual order)
    op.create_index(
        'ix_core_buildings_condominium_sort',
        'core_buildings',
        ['condominium_id', 'sort_order']
    )

    # === STEP 6: Add CHECK constraints ===
    op.create_check_constraint(
        'ck_core_buildings_built_area_positive',
        'core_buildings',
        'built_area IS NULL OR built_area >= 0'
    )
    op.create_check_constraint(
        'ck_core_buildings_common_area_positive',
        'core_buildings',
        'common_area IS NULL OR common_area >= 0'
    )
    op.create_check_constraint(
        'ck_core_buildings_coefficient_range',
        'core_buildings',
        'coefficient IS NULL OR (coefficient >= 0 AND coefficient <= 100)'
    )
    op.create_check_constraint(
        'ck_core_buildings_floors_count_positive',
        'core_buildings',
        'floors_count >= 0'
    )
    op.create_check_constraint(
        'ck_core_buildings_basements_count_positive',
        'core_buildings',
        'basements_count >= 0'
    )
    op.create_check_constraint(
        'ck_core_buildings_units_planned_positive',
        'core_buildings',
        'units_planned >= 0'
    )
    op.create_check_constraint(
        'ck_core_buildings_sort_order_positive',
        'core_buildings',
        'sort_order >= 0'
    )


def downgrade() -> None:
    # === DROP CHECK constraints ===
    op.drop_constraint(
        'ck_core_buildings_sort_order_positive',
        'core_buildings',
        type_='check'
    )
    op.drop_constraint(
        'ck_core_buildings_units_planned_positive',
        'core_buildings',
        type_='check'
    )
    op.drop_constraint(
        'ck_core_buildings_basements_count_positive',
        'core_buildings',
        type_='check'
    )
    op.drop_constraint(
        'ck_core_buildings_floors_count_positive',
        'core_buildings',
        type_='check'
    )
    op.drop_constraint(
        'ck_core_buildings_coefficient_range',
        'core_buildings',
        type_='check'
    )
    op.drop_constraint(
        'ck_core_buildings_common_area_positive',
        'core_buildings',
        type_='check'
    )
    op.drop_constraint(
        'ck_core_buildings_built_area_positive',
        'core_buildings',
        type_='check'
    )

    # === DROP indexes ===
    op.drop_index('ix_core_buildings_condominium_sort', 'core_buildings')
    op.drop_index('ix_core_buildings_condominium_status', 'core_buildings')
    op.drop_index('ix_core_buildings_status', 'core_buildings')
    op.drop_index('ix_core_buildings_building_type_id', 'core_buildings')
    op.drop_index('ix_core_buildings_condominium_id', 'core_buildings')
    op.drop_index('ix_core_buildings_condominium_code', 'core_buildings')

    # === DROP new columns ===
    op.drop_column('core_buildings', 'deleted_at')
    op.drop_column('core_buildings', 'sort_order')
    op.drop_column('core_buildings', 'units_planned')
    op.drop_column('core_buildings', 'basements_count')
    op.drop_column('core_buildings', 'floors_count')
    op.drop_column('core_buildings', 'coefficient')
    op.drop_column('core_buildings', 'common_area')
    op.drop_column('core_buildings', 'built_area')
    op.drop_column('core_buildings', 'short_name')

    # === ADD back deprecated columns ===
    op.add_column(
        'core_buildings',
        sa.Column('percentage', sa.DECIMAL(5, 2), nullable=True)
    )
    op.add_column(
        'core_buildings',
        sa.Column('size', sa.DECIMAL(10, 2), nullable=True)
    )
    op.add_column(
        'core_buildings',
        sa.Column('type', sa.String(100), nullable=True)
    )

    # === RESTORE global unique constraint ===
    # Cannot use op.create_unique_constraint('core_buildings.code', ...) because
    # MySQL generates the constraint name, not Alembic. Use raw SQL instead.
    op.execute(
        "ALTER TABLE core_buildings ADD UNIQUE(`code`)"
    )