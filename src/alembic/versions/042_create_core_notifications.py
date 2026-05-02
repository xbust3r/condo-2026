"""create core_notifications

Revision ID: 042
Revises: 041_seed_incident_permissions
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '042'
down_revision: Union[str, None] = '041_seed_incident_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'core_notifications',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('channel', sa.String(20), nullable=False, server_default='in_app'),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('resource_type', sa.String(30), nullable=False),
        sa.Column('resource_id', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )
    op.create_index('idx_user_read', 'core_notifications', ['user_id', 'is_read'])
    op.create_index('idx_user_created', 'core_notifications', ['user_id', 'created_at'])
    op.create_index('idx_resource', 'core_notifications', ['resource_type', 'resource_id'])


def downgrade() -> None:
    op.drop_index('idx_resource', 'core_notifications')
    op.drop_index('idx_user_created', 'core_notifications')
    op.drop_index('idx_user_read', 'core_notifications')
    op.drop_table('core_notifications')