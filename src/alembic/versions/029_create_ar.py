"""
Create core_accounts_receivable — Cuentas por Cobrar del condominio.

Una AR se genera desde un charge (1 charge → N AR, una por unidad).
Cada AR tiene status que transita: pending → partial → paid / pending → overdue → paid

Revision ID: 029_create_ar
Revises: 028_create_core_charges
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '029_create_ar'
down_revision: Union[str, None] = '028_create_core_charges'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'core_accounts_receivable',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('unit_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('debtor_user_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('reference_code', sa.String(50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('paid_amount', sa.Numeric(12, 2), nullable=False, server_default='0.00'),
        sa.Column('currency', sa.String(3), nullable=False, server_default='PEN'),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending', index=True),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('period', sa.String(7), nullable=True),  # 'YYYY-MM'
        sa.Column('charge_id', sa.BigInteger(), nullable=True, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    # Foreign keys
    op.create_foreign_key(
        'fk_ar_condominium', 'core_accounts_receivable', 'core_condominiums',
        ['condominium_id'], ['id']
    )
    op.create_foreign_key(
        'fk_ar_unit', 'core_accounts_receivable', 'core_units',
        ['unit_id'], ['id']
    )
    op.create_foreign_key(
        'fk_ar_debtor_user', 'core_accounts_receivable', 'users',
        ['debtor_user_id'], ['id']
    )
    op.create_foreign_key(
        'fk_ar_charge', 'core_accounts_receivable', 'core_charges',
        ['charge_id'], ['id']
    )
    # Indexes for common queries
    op.create_index('ix_ar_condominium_status', 'core_accounts_receivable',
                    ['condominium_id', 'status'])
    op.create_index('ix_ar_unit_status', 'core_accounts_receivable',
                    ['unit_id', 'status'])


def downgrade() -> None:
    op.drop_index('ix_ar_unit_status', table_name='core_accounts_receivable')
    op.drop_index('ix_ar_condominium_status', table_name='core_accounts_receivable')
    op.drop_constraint('fk_ar_charge', 'core_accounts_receivable', type_='foreignkey')
    op.drop_constraint('fk_ar_debtor_user', 'core_accounts_receivable', type_='foreignkey')
    op.drop_constraint('fk_ar_unit', 'core_accounts_receivable', type_='foreignkey')
    op.drop_constraint('fk_ar_condominium', 'core_accounts_receivable', type_='foreignkey')
    op.drop_table('core_accounts_receivable')
