"""
Add scope, building_id, and distribution_mode to core_charges.

Extends the charges table to support three distribution scopes:
  - unit:        fixed charge for one specific unit
  - building:    charge prorated across units within a tower
  - condominium: charge prorated across all units in the condominium

Backward compatibility:
  - Existing charges with unit_id set get scope='unit', distribution_mode='fixed_unit_amount'
  - Existing charges with unit_id null get scope='condominium', distribution_mode='fixed_unit_amount'
    (preserving the old "global" behavior as condominium-scoped with flat replication)

Revision ID: 051_add_charge_scope_distribution
Revises: 050_add_user_profile_extra_fields
Create Date: 2026-05-01
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '051_add_charge_scope_distribution'
down_revision: Union[str, None] = '050_add_user_profile_extra_fields'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add new columns (nullable initially for safe migration)
    op.add_column(
        'core_charges',
        sa.Column('scope', sa.String(20), nullable=True,
                  comment='unit | building | condominium')
    )
    op.add_column(
        'core_charges',
        sa.Column('building_id', sa.BigInteger(), nullable=True,
                  comment='FK to core_buildings; required when scope=building')
    )
    op.add_column(
        'core_charges',
        sa.Column('distribution_mode', sa.String(40), nullable=True,
                  server_default='fixed_unit_amount',
                  comment='fixed_unit_amount | prorated_by_building_coefficient | prorated_by_condominium_coefficient')
    )

    # 2. Backfill existing rows so columns can be made NOT NULL safely
    #    Existing charges with unit_id → scope='unit'
    #    Existing charges without unit_id → scope='condominium' (old "global")
    op.execute(
        sa.text(
            "UPDATE core_charges SET scope = 'unit' WHERE unit_id IS NOT NULL AND scope IS NULL"
        )
    )
    op.execute(
        sa.text(
            "UPDATE core_charges SET scope = 'condominium' WHERE unit_id IS NULL AND scope IS NULL"
        )
    )
    # Ensure distribution_mode has a value for all rows
    op.execute(
        sa.text(
            "UPDATE core_charges SET distribution_mode = 'fixed_unit_amount' WHERE distribution_mode IS NULL"
        )
    )

    # 3. Make scope and distribution_mode NOT NULL now that data is backfilled
    op.alter_column('core_charges', 'scope',
                    existing_type=sa.String(20), nullable=False)
    op.alter_column('core_charges', 'distribution_mode',
                    existing_type=sa.String(40), nullable=False,
                    server_default='fixed_unit_amount')

    # 4. Indexes
    op.create_index('ix_charges_scope', 'core_charges', ['scope'])
    op.create_index('ix_charges_building_id', 'core_charges', ['building_id'])

    # 5. FK for building_id
    op.create_foreign_key(
        'fk_charges_building',
        'core_charges', 'core_buildings',
        ['building_id'], ['id']
    )


def downgrade() -> None:
    op.drop_constraint('fk_charges_building', 'core_charges', type_='foreignkey')
    op.drop_index('ix_charges_building_id', table_name='core_charges')
    op.drop_index('ix_charges_scope', table_name='core_charges')
    op.drop_column('core_charges', 'distribution_mode')
    op.drop_column('core_charges', 'building_id')
    op.drop_column('core_charges', 'scope')
