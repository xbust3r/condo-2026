"""
Add amenity_settings JSON column to core_condominiums.

Stores amenity booking configuration flags per condominium:
- enable_amenity_booking_charges: bool (default false)
- include_amenity_bookings_in_receipts: bool (default false)
- include_amenity_bookings_in_building_balance: bool (default false)
- include_amenity_bookings_in_condominium_balance: bool (default false)

Revision ID: 056
Revises: 055_seed_booking_charge_types
"""
from typing import Sequence, Union
from alembic import op


revision: str = '056_add_condominium_amenity_settings'
down_revision: Union[str, None] = '055_seed_booking_charge_types'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE core_condominiums
        ADD COLUMN amenity_settings JSON NULL
        COMMENT 'Amenity booking configuration flags (JSON)'
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE core_condominiums
        DROP COLUMN amenity_settings
    """)
