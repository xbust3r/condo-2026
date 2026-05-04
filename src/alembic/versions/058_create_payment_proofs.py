"""Create payment_proofs table.

Revision ID: 058_create_payment_proofs
Revises: 057_seed_resident_financial_permissions
Create Date: 2026-05-03
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '058_create_payment_proofs'
down_revision: Union[str, None] = '057_seed_resident_financial_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'payment_proofs',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False),
        sa.Column('unit_id', sa.BigInteger(), nullable=False),
        sa.Column('ar_id', sa.BigInteger(), nullable=False),
        sa.Column('submitted_by', sa.BigInteger(), nullable=False),
        sa.Column('file_url', sa.String(500), nullable=False),
        sa.Column('original_filename', sa.String(255), nullable=False),
        sa.Column('file_size_bytes', sa.BigInteger(), nullable=False),
        sa.Column('mime_type', sa.String(100), nullable=False),
        sa.Column('bank_name', sa.String(100), nullable=True),
        sa.Column('transaction_code', sa.String(100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(30), nullable=False, server_default='pending_review'),
        sa.Column('reviewed_by', sa.BigInteger(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('rejection_reason', sa.String(500), nullable=True),
        sa.Column('payment_id', sa.BigInteger(), nullable=True),
        sa.Column('receipt_id', sa.BigInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid'),
        sa.ForeignKeyConstraint(
            ['condominium_id'], ['core_condominiums.id'],
            name='fk_payment_proofs_condominium',
        ),
        sa.ForeignKeyConstraint(
            ['unit_id'], ['core_units.id'],
            name='fk_payment_proofs_unit',
        ),
        sa.ForeignKeyConstraint(
            ['ar_id'], ['core_accounts_receivable.id'],
            name='fk_payment_proofs_ar',
        ),
        sa.ForeignKeyConstraint(
            ['submitted_by'], ['users.id'],
            name='fk_payment_proofs_submitted_by',
        ),
        sa.ForeignKeyConstraint(
            ['reviewed_by'], ['users.id'],
            name='fk_payment_proofs_reviewed_by',
        ),
        sa.ForeignKeyConstraint(
            ['payment_id'], ['core_payments.id'],
            name='fk_payment_proofs_payment',
        ),
        sa.ForeignKeyConstraint(
            ['receipt_id'], ['core_receipts.id'],
            name='fk_payment_proofs_receipt',
        ),
    )
    op.create_index('idx_payment_proofs_condominium', 'payment_proofs', ['condominium_id'])
    op.create_index('idx_payment_proofs_unit', 'payment_proofs', ['unit_id'])
    op.create_index('idx_payment_proofs_ar', 'payment_proofs', ['ar_id'])
    op.create_index('idx_payment_proofs_status', 'payment_proofs', ['status'])
    op.create_index('idx_payment_proofs_submitted_by', 'payment_proofs', ['submitted_by'])


def downgrade() -> None:
    op.drop_table('payment_proofs')
