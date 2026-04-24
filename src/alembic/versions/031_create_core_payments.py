"""
Create core_payments — Registro de pagos de cuentas por cobrar.

Un pago:
  - Se registra contra un AR (accounts_receivable)
  - Genera automáticamente un receipt (1:1)
  - Actualiza el status del AR (pending→partial, overdue→partial, partial→paid)

Revision ID: 031_create_core_payments
Revises: 030_create_core_receipts
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '031_create_core_payments'
down_revision: Union[str, None] = '030_create_core_receipts'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'core_payments',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('unit_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('ar_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('receipt_id', sa.BigInteger(), nullable=True, index=True),
        sa.Column('payer_user_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('payment_method', sa.String(30), nullable=False),
        sa.Column('reference', sa.String(100), nullable=True),
        sa.Column('paid_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    # Foreign keys
    op.create_foreign_key(
        'fk_payments_condominium', 'core_payments', 'core_condominiums',
        ['condominium_id'], ['id']
    )
    op.create_foreign_key(
        'fk_payments_unit', 'core_payments', 'core_units',
        ['unit_id'], ['id']
    )
    op.create_foreign_key(
        'fk_payments_ar', 'core_payments', 'core_accounts_receivable',
        ['ar_id'], ['id']
    )
    op.create_foreign_key(
        'fk_payments_payer', 'core_payments', 'users',
        ['payer_user_id'], ['id']
    )
    op.create_foreign_key(
        'fk_payments_receipt', 'core_payments', 'core_receipts',
        ['receipt_id'], ['id']
    )
    # Indexes
    op.create_index('ix_payments_ar_id', 'core_payments', ['ar_id'])
    op.create_index('ix_payments_condominium_paid_at', 'core_payments',
                    ['condominium_id', 'paid_at'])


def downgrade() -> None:
    op.drop_index('ix_payments_condominium_paid_at', table_name='core_payments')
    op.drop_index('ix_payments_ar_id', table_name='core_payments')
    op.drop_constraint('fk_payments_receipt', 'core_payments', type_='foreignkey')
    op.drop_constraint('fk_payments_payer', 'core_payments', type_='foreignkey')
    op.drop_constraint('fk_payments_ar', 'core_payments', type_='foreignkey')
    op.drop_constraint('fk_payments_unit', 'core_payments', type_='foreignkey')
    op.drop_constraint('fk_payments_condominium', 'core_payments', type_='foreignkey')
    op.drop_table('core_payments')
