"""
Create core_ledger_entries — Libro mayor por unidad.

Cada operación financiera (cargo o pago) genera una entrada en el ledger.
El ledger es append-only: nunca se modifica ni borra.

Revision ID: 032_create_core_ledger_entries
Revises: 031_create_core_payments
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '032_create_core_ledger_entries'
down_revision: Union[str, None] = '031_create_core_payments'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'core_ledger_entries',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('unit_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('entry_type', sa.String(20), nullable=False),  # charge/payment/adjustment/balance_forward
        sa.Column('ar_id', sa.BigInteger(), nullable=True, index=True),
        sa.Column('payment_id', sa.BigInteger(), nullable=True, index=True),
        sa.Column('charge_id', sa.BigInteger(), nullable=True, index=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('debit', sa.Numeric(12, 2), nullable=False, server_default='0.00'),
        sa.Column('credit', sa.Numeric(12, 2), nullable=False, server_default='0.00'),
        sa.Column('balance', sa.Numeric(12, 2), nullable=False, server_default='0.00'),
        sa.Column('period', sa.String(7), nullable=True),  # 'YYYY-MM'
        sa.Column('reference', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )
    # Foreign keys
    op.create_foreign_key(
        'fk_ledger_condominium', 'core_ledger_entries', 'core_condominiums',
        ['condominium_id'], ['id']
    )
    op.create_foreign_key(
        'fk_ledger_unit', 'core_ledger_entries', 'core_units',
        ['unit_id'], ['id']
    )
    op.create_foreign_key(
        'fk_ledger_ar', 'core_ledger_entries', 'core_accounts_receivable',
        ['ar_id'], ['id']
    )
    op.create_foreign_key(
        'fk_ledger_payment', 'core_ledger_entries', 'core_payments',
        ['payment_id'], ['id']
    )
    op.create_foreign_key(
        'fk_ledger_charge', 'core_ledger_entries', 'core_charges',
        ['charge_id'], ['id']
    )
    # Indexes for unit ledger queries
    op.create_index('ix_ledger_unit_created', 'core_ledger_entries',
                    ['unit_id', 'created_at'])
    op.create_index('ix_ledger_unit_period', 'core_ledger_entries',
                    ['unit_id', 'period'])


def downgrade() -> None:
    op.drop_index('ix_ledger_unit_period', table_name='core_ledger_entries')
    op.drop_index('ix_ledger_unit_created', table_name='core_ledger_entries')
    op.drop_constraint('fk_ledger_charge', 'core_ledger_entries', type_='foreignkey')
    op.drop_constraint('fk_ledger_payment', 'core_ledger_entries', type_='foreignkey')
    op.drop_constraint('fk_ledger_ar', 'core_ledger_entries', type_='foreignkey')
    op.drop_constraint('fk_ledger_unit', 'core_ledger_entries', type_='foreignkey')
    op.drop_constraint('fk_ledger_condominium', 'core_ledger_entries', type_='foreignkey')
    op.drop_table('core_ledger_entries')
