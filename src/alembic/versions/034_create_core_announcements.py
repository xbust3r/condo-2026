"""
Create core_announcements — tabla de anuncios/comunicados del administrador.

Revision ID: 034_create_core_announcements
Revises: 033_seed_financial_permissions
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '034_create_core_announcements'
down_revision: Union[str, None] = '033_seed_financial_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


ANNOUNCEMENT_CATEGORIES = ['info', 'warning', 'urgent', 'event']
VISIBILITY_SCOPES = ['public', 'owners_only', 'residents_only']


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
    if not _table_exists('core_announcements'):
        op.create_table(
            'core_announcements',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, unique=True),
            sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column('author_user_id', sa.BigInteger(), nullable=False),
            sa.Column('title', sa.String(200), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('category', sa.String(20), nullable=False, server_default='info'),
            sa.Column('visibility', sa.String(20), nullable=False, server_default='public'),
            sa.Column('is_pinned', sa.Boolean(), nullable=False, server_default='0'),
            sa.Column('published_at', sa.DateTime(), nullable=True),
            sa.Column('expires_at', sa.DateTime(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('updated_at', sa.DateTime(), nullable=True, onupdate=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id']),
            sa.ForeignKeyConstraint(['author_user_id'], ['users.id']),
            sa.Index('ix_announcements_condo_published', 'condominium_id', 'published_at'),
            sa.Index('ix_announcements_category', 'category'),
        )


def downgrade() -> None:
    op.drop_table('core_announcements')
