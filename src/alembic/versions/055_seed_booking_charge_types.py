"""
Seed amenity booking charge types for financial classification.

Revision ID: 055_seed_booking_charge_types
Revises: 054_seed_booking_permissions
"""
from typing import Sequence, Union
from alembic import op


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
            f"""
            INSERT INTO core_charge_types (uuid, code, name, description, is_global, sort_order)
            SELECT UUID(), '{ct["code"]}', '{ct["name"]}',
                   '{ct["description"]}', {ct["is_global"]}, {ct["sort_order"]}
            WHERE NOT EXISTS (
                SELECT 1 FROM core_charge_types WHERE code = '{ct["code"]}'
            )
            """
        )


def downgrade() -> None:
    for ct in CHARGE_TYPES_SEED:
        op.execute(
            f"DELETE FROM core_charge_types WHERE code = '{ct['code']}'"
        )
