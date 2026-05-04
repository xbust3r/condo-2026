"""
Create core_amenity_availability_rules — per-amenity slot/date configuration.

Separates availability from policy:
- slot_mode: CONTINUOUS_SLOTS vs DISCRETE_WINDOWS
- slot_interval_min / window times
- max_capacity_per_slot
- advance_booking_days / cancel_window_hours
- blocked_dates / opening_hours (JSON)

Revision ID: 064_create_availability_rules
Revises: 063_add_amenity_type_column
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '064_create_availability_rules'
down_revision: Union[str, None] = '063_add_amenity_type_column'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'core_amenity_availability_rules',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('amenity_id', sa.BigInteger(), nullable=False),

        # Slot model
        sa.Column(
            'slot_mode',
            sa.String(20),
            nullable=False,
            server_default='CONTINUOUS_SLOTS',
            comment='CONTINUOUS_SLOTS | DISCRETE_WINDOWS',
        ),
        sa.Column('slot_interval_min', sa.Integer(), nullable=True, comment='Duration of each slot in minutes'),
        sa.Column('window_start_time', sa.Time(), nullable=True, comment='Earliest booking start per window'),
        sa.Column('window_end_time', sa.Time(), nullable=True, comment='Latest booking end per window'),

        # Capacity
        sa.Column('max_capacity_per_slot', sa.Integer(), nullable=False, server_default='1',
                  comment='Max people/groups per slot'),

        # Booking window
        sa.Column('advance_booking_days', sa.Integer(), nullable=True,
                  comment='How many days into the future bookings are allowed'),
        sa.Column('cancel_window_hours', sa.Integer(), nullable=True,
                  comment='Minimum hours before start to cancel without penalty'),

        # Date config
        sa.Column('blocked_dates_json', sa.JSON(), nullable=True,
                  comment='["2026-12-25","2027-01-01"] — dates where booking is blocked'),
        sa.Column('opening_hours_json', sa.JSON(), nullable=True,
                  comment='{"monday":{"open":"08:00","close":"22:00"},...}'),

        # Metadata
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True),

        # Constraints
        sa.ForeignKeyConstraint(
            ['amenity_id'], ['core_amenities.id'],
            name='fk_availability_amenity',
        ),
        sa.UniqueConstraint('amenity_id', name='uq_availability_amenity'),
    )

    op.create_index(
        'ix_availability_active',
        'core_amenity_availability_rules',
        ['amenity_id', 'is_active'],
    )


def downgrade() -> None:
    op.drop_index('ix_availability_active', table_name='core_amenity_availability_rules')
    op.drop_table('core_amenity_availability_rules')
