"""
Add indexes on auth_sessions(user_id, expires_at) for session lookup
and cleanup queries.

Revision ID: 073_add_auth_sessions_indexes
Revises: 072_create_core_voting_rules
Create Date: 2026-05-05
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '073_add_auth_sessions_indexes'
down_revision: Union[str, None] = '072_create_core_voting_rules'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _index_exists(idx_name: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
              AND INDEX_NAME = :idx_name
        """),
        {"idx_name": idx_name},
    )
    return result.scalar() > 0


def upgrade() -> None:
    if not _index_exists('ix_auth_sessions_user_id'):
        op.create_index(
            'ix_auth_sessions_user_id',
            'auth_sessions',
            ['user_id'],
            unique=False,
        )

    if not _index_exists('ix_auth_sessions_expires_at'):
        op.create_index(
            'ix_auth_sessions_expires_at',
            'auth_sessions',
            ['expires_at'],
            unique=False,
        )


def downgrade() -> None:
    op.drop_index('ix_auth_sessions_expires_at', table_name='auth_sessions')
    op.drop_index('ix_auth_sessions_user_id', table_name='auth_sessions')