"""widen priority_score_snapshot to Numeric(16,4)

Revision ID: 067
Revises: 066_add_waitlist_foreign_keys
Create Date: 2026-05-04

"""
from alembic import op
import sqlalchemy as sa


revision = '067_widen_priority_score'
down_revision = '066_add_waitlist_foreign_keys'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'core_amenity_waitlist',
        'priority_score_snapshot',
        existing_type=sa.Numeric(10, 4),
        type_=sa.Numeric(16, 4),
        existing_nullable=True,
    )


def downgrade():
    op.alter_column(
        'core_amenity_waitlist',
        'priority_score_snapshot',
        existing_type=sa.Numeric(16, 4),
        type_=sa.Numeric(10, 4),
        existing_nullable=True,
    )
