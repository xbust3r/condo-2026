"""add FKs to core_amenity_waitlist

Revision ID: 066
Revises: 065_create_waitlist_table
Create Date: 2026-05-04

"""
from alembic import op
import sqlalchemy as sa

revision = '066_add_waitlist_foreign_keys'
down_revision = '065_create_waitlist_table'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        'fk_waitlist_amenity',
        'core_amenity_waitlist',
        'core_amenities',
        ['amenity_id'],
        ['id'],
    )
    op.create_foreign_key(
        'fk_waitlist_booking',
        'core_amenity_waitlist',
        'core_amenity_bookings',
        ['converted_booking_id'],
        ['id'],
    )


def downgrade():
    op.drop_constraint('fk_waitlist_booking', 'core_amenity_waitlist', type_='foreignkey')
    op.drop_constraint('fk_waitlist_amenity', 'core_amenity_waitlist', type_='foreignkey')
