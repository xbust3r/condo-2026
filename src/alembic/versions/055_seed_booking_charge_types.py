"""
Seed amenity booking charge types for financial classification.

Revision ID: 055_seed_booking_charge_types
Revises: 054_seed_booking_permissions
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '055_seed_booking_charge_types'
down_revision: Union[str, None] = '054_seed_booking_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CHARGE_TYPES_SEED = [
    {
        "code": "amenity_booking",
        "name": "Reserva de Área Común",
        "description": "Cobro por reserva de amenidad/área común",
        "is_global": 0,
        "sort_order": 100,
    },
    {
        "code": "amenity_security_deposit",
        "name": "Garantía Reserva Área Común",
        "description": "Depósito en garantía por reserva de amenidad",
        "is_global": 0,
        "sort_order": 101,
    },
]


def upgrade() -> None:
    for ct in CHARGE_TYPES_SEED:
        op.execute(
            sa.text("""
                INSERT IGNORE INTO core_charge_types (code, name, description, is_global, sort_order)
                VALUES (:code, :name, :description, :is_global, :sort_order)
            """),
            ct,
        )


def downgrade() -> None:
    for ct in CHARGE_TYPES_SEED:
        op.execute(
            sa.text("DELETE FROM core_charge_types WHERE code = :code"),
            {"code": ct["code"]},
        )
