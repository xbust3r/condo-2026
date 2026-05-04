"""create core_amenity_usage_logs — operational usage tracking for amenity bookings

Tracks real-world usage events (check-in, check-out, no-show, etc.)
separately from allocation decisions to maintain clean audit boundaries.

Revision ID: 068
Revises: 067_widen_priority_score
Create Date: 2026-05-04

"""
from alembic import op
import sqlalchemy as sa


revision = '068_create_amenity_usage_logs'
down_revision = '067_widen_priority_score'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'core_amenity_usage_logs',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True, server_default=sa.text('uuid()')),
        sa.Column('booking_id', sa.BigInteger(), nullable=False),
        sa.Column('amenity_id', sa.BigInteger(), nullable=False),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False),
        sa.Column('unit_id', sa.BigInteger(), nullable=True),
        sa.Column('owner_id', sa.BigInteger(), nullable=True),
        sa.Column('event_type', sa.String(20), nullable=False),
        sa.Column('event_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('recorded_by', sa.BigInteger(), nullable=True),
        sa.Column('source', sa.String(20), nullable=False, server_default='system'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('event_context_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Foreign keys
    op.create_foreign_key(
        'fk_usage_logs_booking',
        'core_amenity_usage_logs', 'core_amenity_bookings',
        ['booking_id'], ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'fk_usage_logs_amenity',
        'core_amenity_usage_logs', 'core_amenities',
        ['amenity_id'], ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'fk_usage_logs_condominium',
        'core_amenity_usage_logs', 'core_condominiums',
        ['condominium_id'], ['id'],
        ondelete='CASCADE',
    )

    # Indexes
    op.create_index('ix_usage_logs_amenity_event', 'core_amenity_usage_logs', ['amenity_id', 'event_at'])
    op.create_index('ix_usage_logs_booking_type', 'core_amenity_usage_logs', ['booking_id', 'event_type'])
    op.create_index('ix_usage_logs_condo_event', 'core_amenity_usage_logs', ['condominium_id', 'event_at'])

    # Check constraint for valid event types
    op.create_check_constraint(
        'ck_usage_logs_event_type',
        'core_amenity_usage_logs',
        "event_type IN ('CHECK_IN', 'CHECK_OUT', 'NO_SHOW', 'AUTO_RELEASE', 'MANUAL_CLOSE')",
    )


def downgrade():
    op.drop_constraint('ck_usage_logs_event_type', 'core_amenity_usage_logs', type_='check')
    op.drop_index('ix_usage_logs_condo_event', table_name='core_amenity_usage_logs')
    op.drop_index('ix_usage_logs_booking_type', table_name='core_amenity_usage_logs')
    op.drop_index('ix_usage_logs_amenity_event', table_name='core_amenity_usage_logs')
    op.drop_constraint('fk_usage_logs_condominium', 'core_amenity_usage_logs', type_='foreignkey')
    op.drop_constraint('fk_usage_logs_amenity', 'core_amenity_usage_logs', type_='foreignkey')
    op.drop_constraint('fk_usage_logs_booking', 'core_amenity_usage_logs', type_='foreignkey')
    op.drop_table('core_amenity_usage_logs')
