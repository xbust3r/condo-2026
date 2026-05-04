"""create core_amenity_waitlist table

Revision ID: 065
Revises: 064_create_availability_rules
Create Date: 2026-05-04

Waitlist lifecycle: WAITING → NOTIFIED → CONFIRMED/CONVERTED/EXPIRED/CANCELLED
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = '065_create_waitlist_table'
down_revision = '064_create_availability_rules'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'core_amenity_waitlist',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('amenity_id', sa.BigInteger(), nullable=False),
        sa.Column('unit_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('booking_date', sa.Date(), nullable=False),
        sa.Column('requested_start_at', sa.DateTime(), nullable=False),
        sa.Column('requested_end_at', sa.DateTime(), nullable=False),
        sa.Column('guest_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.String(32), nullable=False, server_default='WAITING'),
        sa.Column('priority_score_snapshot', sa.Numeric(10, 4), nullable=True),
        sa.Column('priority_reason_json', mysql.JSON(), nullable=True),
        sa.Column('effective_policy_snapshot_json', mysql.JSON(), nullable=True),
        sa.Column('idempotency_key', sa.String(255), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('notified_at', sa.DateTime(), nullable=True),
        sa.Column('converted_booking_id', sa.BigInteger(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True),

        # Indexes for operational lookups
        sa.Index('idx_waitlist_amenity_status', 'amenity_id', 'status'),
        sa.Index('idx_waitlist_unit', 'unit_id'),
        sa.Index('idx_waitlist_user', 'user_id'),
        sa.Index('idx_waitlist_booking_date', 'amenity_id', 'booking_date'),
        # Idempotency per condominium (via amenity→condominium implicitly)
        # But waitlist doesn't have condominium_id directly; amenity serves that role
    )


def downgrade():
    op.drop_table('core_amenity_waitlist')
