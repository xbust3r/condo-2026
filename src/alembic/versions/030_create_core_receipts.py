"""
Create core_receipts — Generación de recibos por pagos de AR.

Un receipt:
  - Es generado automáticamente al registrar un pago
  - receipt_number = correlativo por condominio (formato: C{cod}-{YYYY}{MM}-{correlativo:06d})
  - Un AR puede tener múltiples receipts (pago parcial = varios receipts)

Revision ID: 030_create_core_receipts
Revises: 029_create_core_accounts_receivable
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '030_create_core_receipts'
down_revision: Union[str, None] = '029_create_core_accounts_receivable'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'core_receipts',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('unit_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('ar_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('receipt_number', sa.String(30), nullable=False),
        sa.Column('issued_at', sa.DateTime(), nullable=False),
        sa.Column('payer_user_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('amount_paid', sa.Numeric(12, 2), nullable=False),
        sa.Column('payment_method', sa.String(30), nullable=False),
        sa.Column('reference', sa.String(100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )
    # Foreign keys
    op.create_foreign_key(
        'fk_receipts_condominium', 'core_receipts', 'core_condominiums',
        ['condominium_id'], ['id']
    )
    op.create_foreign_key(
        'fk_receipts_unit', 'core_receipts', 'core_units',
        ['unit_id'], ['id']
    )
    op.create_foreign_key(
        'fk_receipts_ar', 'core_receipts', 'core_accounts_receivable',
        ['ar_id'], ['id']
    )
    op.create_foreign_key(
        'fk_receipts_payer', 'core_receipts', 'users',
        ['payer_user_id'], ['id']
    )
    # Unique receipt number per condominium
    op.create_index('ix_receipts_condominium_receipt_number',
                    'core_receipts', ['condominium_id', 'receipt_number'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_receipts_condominium_receipt_number', table_name='core_receipts')
    op.drop_constraint('fk_receipts_payer', 'core_receipts', type_='foreignkey')
    op.drop_constraint('fk_receipts_ar', 'core_receipts', type_='foreignkey')
    op.drop_constraint('fk_receipts_unit', 'core_receipts', type_='foreignkey')
    op.drop_constraint('fk_receipts_condominium', 'core_receipts', type_='foreignkey')
    op.drop_table('core_receipts')
