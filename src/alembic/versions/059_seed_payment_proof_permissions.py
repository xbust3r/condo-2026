"""Seed payment_proof permissions.

Revision ID: 059_seed_payment_proof_permissions
Revises: 058_create_payment_proofs
Create Date: 2026-05-03
"""
from typing import Sequence, Union
from alembic import op


revision: str = '059_seed_payment_proof_permissions'
down_revision: Union[str, None] = '058_create_payment_proofs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insert permissions into core_permissions
    op.execute(
        "INSERT IGNORE INTO core_permissions (code, description, scope_default) VALUES "
        "('payment_proof.write', 'Subir comprobantes de pago', 'condominium'),"
        "('payment_proof.read', 'Ver comprobantes de pago', 'condominium'),"
        "('payment_proof.review', 'Revisar y aprobar/rechazar comprobantes', 'condominium')"
    )

    # Assign to roles:
    # - resident: write + read (own proofs)
    # - admin: write + read + review
    # - accountant: write + read + review
    # - super_admin: write + read + review
    op.execute(
        "INSERT IGNORE INTO core_role_permissions (role, permission_code) VALUES "
        "('resident', 'payment_proof.write'),"
        "('resident', 'payment_proof.read'),"
        "('admin', 'payment_proof.write'),"
        "('admin', 'payment_proof.read'),"
        "('admin', 'payment_proof.review'),"
        "('accountant', 'payment_proof.write'),"
        "('accountant', 'payment_proof.read'),"
        "('accountant', 'payment_proof.review'),"
        "('super_admin', 'payment_proof.write'),"
        "('super_admin', 'payment_proof.read'),"
        "('super_admin', 'payment_proof.review')"
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM core_role_permissions WHERE permission_code LIKE 'payment_proof.%'"
    )
    op.execute(
        "DELETE FROM core_permissions WHERE code LIKE 'payment_proof.%'"
    )
