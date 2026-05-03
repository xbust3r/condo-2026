"""
Seed financial permissions for resident role.

Residents need read access to their own receipts, payments, charges, and ledger.
These permissions were defined in 033_seed_financial_permissions but never
assigned to the resident role in 023_create_core_role_permissions.

Revision ID: 057_seed_resident_financial_permissions
Revises: 056_add_condominium_amenity_settings
Create Date: 2026-05-03
"""
from typing import Sequence, Union
from alembic import op


revision: str = '057_seed_resident_financial_permissions'
down_revision: Union[str, None] = '056_add_condominium_amenity_settings'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "INSERT IGNORE INTO core_role_permissions (role, permission_code) VALUES "
        "('resident', 'receipt.read'),"
        "('resident', 'payment.read'),"
        "('resident', 'charge.read'),"
        "('resident', 'ledger.read')"
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM core_role_permissions WHERE role = 'resident' AND "
        "permission_code IN ('receipt.read', 'payment.read', 'charge.read', 'ledger.read')"
    )
