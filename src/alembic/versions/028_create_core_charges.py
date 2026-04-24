"""
Create core_charges — tabla de cargos recurrentes y extraordinarios.

Un cargo puede ser:
  - Global (is_global=True): aplica a todas las unidades del condominio
  - Unit-specific (unit_id): aplica solo a una unidad

Un cargo recurrente (is_recurrent=True) genera AR automáticamente para
cada unidad activa del condominio en cada período.

Revision ID: 028_create_core_charges
Revises: 027_create_core_charge_types
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '028_create_core_charges'
down_revision: Union[str, None] = '027_create_core_charge_types'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'core_charges',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('charge_type_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('unit_id', sa.BigInteger(), nullable=True, index=True),  # null = global
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False, server_default='PEN'),
        sa.Column('is_recurrent', sa.SmallInteger(), nullable=False, server_default='0'),
        sa.Column('period_pattern', sa.String(7), nullable=True),  # 'YYYY-MM'
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    # Foreign keys
    op.create_foreign_key(
        'fk_charges_condominium',
        'core_charges', 'core_condominiums',
        ['condominium_id'], ['id']
    )
    op.create_foreign_key(
        'fk_charges_charge_type',
        'core_charges', 'core_charge_types',
        ['charge_type_id'], ['id']
    )
    op.create_foreign_key(
        'fk_charges_unit',
        'core_charges', 'core_units',
        ['unit_id'], ['id']
    )
    # Index for listing by status
    op.create_index('ix_charges_condominium_status', 'core_charges',
                    ['condominium_id', 'status'])


def downgrade() -> None:
    op.drop_index('ix_charges_condominium_status', table_name='core_charges')
    op.drop_constraint('fk_charges_unit', 'core_charges', type_='foreignkey')
    op.drop_constraint('fk_charges_charge_type', 'core_charges', type_='foreignkey')
    op.drop_constraint('fk_charges_condominium', 'core_charges', type_='foreignkey')
    op.drop_table('core_charges')
