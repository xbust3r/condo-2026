"""
Create amenity bookings + extend amenities and AR for booking support.

Changes:
1. Add booking_price + security_deposit_amount to core_amenities
2. Add origin_type + origin_id to core_accounts_receivable (nullable, additive)
3. Create core_amenity_bookings table
4. Create core_amenity_deposit_movements table

Revision ID: 053_create_amenity_bookings
Revises: 052_add_amenity_scope_and_building
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '053_create_amenity_bookings'
down_revision: Union[str, None] = '052_add_amenity_scope_and_building'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. Extend core_amenities ──────────────────────────────────────
    op.add_column('core_amenities', sa.Column(
        'booking_price',
        sa.Numeric(12, 2),
        nullable=False,
        server_default='0.00',
        comment='Precio de reserva (0 = gratuito)',
    ))
    op.add_column('core_amenities', sa.Column(
        'security_deposit_amount',
        sa.Numeric(12, 2),
        nullable=False,
        server_default='0.00',
        comment='Monto de garantía (0 = sin garantía)',
    ))
    op.add_column('core_amenities', sa.Column(
        'is_reservable',
        sa.Boolean(),
        nullable=False,
        server_default='0',
        comment='Si la amenidad acepta reservas',
    ))

    # ── 2. Extend core_accounts_receivable ────────────────────────────
    op.add_column('core_accounts_receivable', sa.Column(
        'origin_type',
        sa.String(50),
        nullable=True,
        comment='Tipo de origen: amenity_booking_fee | amenity_security_deposit | NULL=charge-based',
    ))
    op.add_column('core_accounts_receivable', sa.Column(
        'origin_id',
        sa.BigInteger(),
        nullable=True,
        comment='ID del registro origen (booking_id cuando origin_type es amenity_*)',
    ))
    op.create_index(
        'ix_ar_origin',
        'core_accounts_receivable',
        ['origin_type', 'origin_id'],
    )

    # ── 3. Create core_amenity_bookings ───────────────────────────────
    op.create_table(
        'core_amenity_bookings',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('building_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('amenity_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('unit_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('owner_id', sa.BigInteger(), nullable=False, index=True),

        # Snapshots (for audit trail if unit/owner change later)
        sa.Column('unit_number_snapshot', sa.String(50), nullable=True),
        sa.Column('owner_name_snapshot', sa.String(200), nullable=True),

        # Booking timeframe
        sa.Column('booking_date', sa.Date(), nullable=False),
        sa.Column('start_at', sa.DateTime(), nullable=False),
        sa.Column('end_at', sa.DateTime(), nullable=False),

        # Status
        sa.Column('status', sa.String(20), nullable=False, server_default='draft',
                  comment='draft | pending_approval | confirmed | cancelled | completed'),

        # Financial
        sa.Column('booking_fee_amount', sa.Numeric(12, 2), nullable=False, server_default='0.00'),
        sa.Column('security_deposit_amount', sa.Numeric(12, 2), nullable=False, server_default='0.00'),
        sa.Column('currency', sa.String(3), nullable=False, server_default='PEN'),

        # Linked ARs
        sa.Column('booking_fee_ar_id', sa.BigInteger(), nullable=True),
        sa.Column('security_deposit_ar_id', sa.BigInteger(), nullable=True),

        # Deposit lifecycle
        sa.Column('deposit_status', sa.String(20), nullable=False, server_default='not_required',
                  comment='not_required | pending | paid | returned | partially_applied | applied | forfeited'),

        # Metadata
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_by', sa.BigInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),

        # Foreign keys
        sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id'], name='fk_booking_condominium'),
        sa.ForeignKeyConstraint(['building_id'], ['core_buildings.id'], name='fk_booking_building'),
        sa.ForeignKeyConstraint(['amenity_id'], ['core_amenities.id'], name='fk_booking_amenity'),
        sa.ForeignKeyConstraint(['unit_id'], ['core_units.id'], name='fk_booking_unit'),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name='fk_booking_owner'),
        sa.ForeignKeyConstraint(['booking_fee_ar_id'], ['core_accounts_receivable.id'], name='fk_booking_fee_ar'),
        sa.ForeignKeyConstraint(['security_deposit_ar_id'], ['core_accounts_receivable.id'], name='fk_booking_deposit_ar'),
    )

    # Composite indexes for common queries
    op.create_index('ix_bookings_status', 'core_amenity_bookings', ['condominium_id', 'status'])
    op.create_index('ix_bookings_amenity_dates', 'core_amenity_bookings', ['amenity_id', 'start_at', 'end_at'])
    op.create_index('ix_bookings_unit', 'core_amenity_bookings', ['unit_id', 'status'])
    op.create_index('ix_bookings_owner', 'core_amenity_bookings', ['owner_id', 'status'])

    # ── 4. Create core_amenity_deposit_movements ──────────────────────
    op.create_table(
        'core_amenity_deposit_movements',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('booking_id', sa.BigInteger(), nullable=False, index=True),
        sa.Column('movement_type', sa.String(20), nullable=False,
                  comment='charge | return | partial_apply | full_apply'),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False, server_default='PEN'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_by', sa.BigInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),

        # Foreign key
        sa.ForeignKeyConstraint(['booking_id'], ['core_amenity_bookings.id'], name='fk_deposit_movement_booking'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], name='fk_deposit_movement_creator'),
    )

    op.create_index('ix_deposit_movements_booking', 'core_amenity_deposit_movements', ['booking_id', 'created_at'])


def downgrade() -> None:
    # 4. Drop deposit movements
    op.drop_index('ix_deposit_movements_booking', table_name='core_amenity_deposit_movements')
    op.drop_table('core_amenity_deposit_movements')

    # 3. Drop bookings
    op.drop_index('ix_bookings_owner', table_name='core_amenity_bookings')
    op.drop_index('ix_bookings_unit', table_name='core_amenity_bookings')
    op.drop_index('ix_bookings_amenity_dates', table_name='core_amenity_bookings')
    op.drop_index('ix_bookings_status', table_name='core_amenity_bookings')
    op.drop_table('core_amenity_bookings')

    # 2. Revert AR extension
    op.drop_index('ix_ar_origin', table_name='core_accounts_receivable')
    op.drop_column('core_accounts_receivable', 'origin_id')
    op.drop_column('core_accounts_receivable', 'origin_type')

    # 1. Revert amenities extension
    op.drop_column('core_amenities', 'is_reservable')
    op.drop_column('core_amenities', 'security_deposit_amount')
    op.drop_column('core_amenities', 'booking_price')
