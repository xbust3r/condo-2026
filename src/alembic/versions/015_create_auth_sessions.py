"""
Create auth_sessions — gestión de sesiones de autenticación JWT.

Almacena hashes de refresh tokens para poder invalidar sesiones
(logout, rotación de tokens). Sin Redis — escala a Redis después.

access_token: JWT corto (15 min), contiene user_id + metadata
refresh_token: UUID v4, almacenado hash en DB, válido 7 días

Revision ID: 015_create_auth_sessions
Revises: 014_create_roles
Create Date: 2026-04-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '015_create_auth_sessions'
down_revision: Union[str, None] = '014_create_roles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(table: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
        """),
        {"table": table},
    )
    return result.scalar() > 0


def upgrade() -> None:
    if not _table_exists('auth_sessions'):
        op.create_table(
            'auth_sessions',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
            sa.Column('user_id', sa.BigInteger(), nullable=False),
            sa.Column('refresh_token_hash', sa.String(255), nullable=False),
            sa.Column('user_agent', sa.String(500), nullable=True),
            sa.Column('ip_address', sa.String(45), nullable=True),
            sa.Column('expires_at', sa.DateTime(), nullable=False),
            sa.Column(
                'created_at',
                sa.DateTime(),
                nullable=False,
                server_default=sa.text('CURRENT_TIMESTAMP'),
            ),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('uuid'),
            sa.ForeignKeyConstraint(
                ['user_id'],
                ['users.id'],
                name='fk_auth_sessions_user',
                ondelete='CASCADE',
            ),

            sa.Index('ix_auth_sessions_refresh_hash', 'refresh_token_hash'),
        )


def downgrade() -> None:
    op.drop_table('auth_sessions')
