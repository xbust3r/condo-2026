"""
Add token_version to users for access token invalidation.

When a user is suspended, locked, or logs out from all devices,
we increment token_version. Any JWT with an old token_version
is immediately rejected — even if the token hasn't expired yet.

Revision ID: 016_add_token_version_to_users
Revises: 015_create_auth_sessions
Create Date: 2026-04-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '016_add_token_version_to_users'
down_revision: Union[str, None] = '015_create_auth_sessions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table: str, column: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME = :column
        """),
        {"table": table, "column": column},
    )
    return result.scalar() > 0


def upgrade() -> None:
    if not _column_exists('users', 'token_version'):
        op.add_column(
            'users',
            sa.Column('token_version', sa.Integer(), nullable=False, server_default='0'),
        )
        op.execute("UPDATE users SET token_version = 0 WHERE token_version IS NULL")
        op.alter_column('users', 'token_version',
                        existing_type=sa.Integer(),
                        nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'token_version')
