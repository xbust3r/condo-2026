"""
Create core_meetings — tabla de reuniones/asambleas del condominio.

Revision ID: 048_create_core_meetings
Revises: 047_create_core_resident_profiles
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '048_create_core_meetings'
down_revision: Union[str, None] = '047_create_core_resident_profiles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


MEETING_TYPES = ['assembly', 'board', 'committee']
STATUSES = ['scheduled', 'confirmed', 'held', 'cancelled']


def _table_exists(table: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*) FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :table
        """),
        {"table": table},
    )
    return result.scalar() > 0


def upgrade() -> None:
    if not _table_exists('core_meetings'):
        op.create_table(
            'core_meetings',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, unique=True),
            sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column('meeting_type', sa.String(20), nullable=False, server_default='assembly'),
            sa.Column('title', sa.String(200), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('meeting_date', sa.DateTime(), nullable=False),
            sa.Column('location', sa.String(300), nullable=True),
            sa.Column('status', sa.String(20), nullable=False, server_default='scheduled'),
            sa.Column('approved_at', sa.DateTime(), nullable=True),
            sa.Column('created_by_user_id', sa.BigInteger(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('updated_at', sa.DateTime(), nullable=True, onupdate=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id']),
            sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id']),
            sa.Index('ix_meetings_condo_date', 'condominium_id', 'meeting_date'),
            sa.Index('ix_meetings_status', 'status'),
        )


def downgrade() -> None:
    op.drop_table('core_meetings')
