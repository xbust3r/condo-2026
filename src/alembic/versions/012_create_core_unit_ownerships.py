"""
Create core_unit_ownerships — relación patrimonial usuario ↔ unidad.

¿Qué responde?: ¿Quién es dueño de qué unidad y desde cuándo?
¿Qué NO responde?: Ocupación, permisos, roles.

Tabla pivote: un usuario puede tener N propiedades;
una unidad puede tener 1 o N propietarios (copropiedad).

Revision ID: 012_create_core_unit_ownerships
Revises: 011_refactor_users_auth_profile
Create Date: 2026-04-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '012_create_core_unit_ownerships'
down_revision: Union[str, None] = '011_refactor_users_auth_profile'
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
    if not _table_exists('core_unit_ownerships'):
        op.create_table(
            'core_unit_ownerships',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
            sa.Column('unit_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column('user_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column(
                'ownership_type',
                sa.String(30),
                nullable=False,
                server_default='owner',
            ),
            sa.Column(
                'ownership_percentage',
                sa.Numeric(5, 2),
                nullable=False,
                server_default='100.00',
            ),
            sa.Column(
                'status',
                sa.String(30),
                nullable=False,
                server_default='active',
            ),
            sa.Column('start_date', sa.Date(), nullable=True),
            sa.Column('end_date', sa.Date(), nullable=True),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column(
                'created_at',
                sa.DateTime(),
                nullable=False,
                server_default=sa.text('CURRENT_TIMESTAMP'),
            ),
            sa.Column(
                'updated_at',
                sa.DateTime(),
                nullable=False,
                server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
            ),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('uuid'),
            sa.ForeignKeyConstraint(
                ['unit_id'],
                ['core_units.id'],
                name='fk_unit_ownerships_unit',
                ondelete='CASCADE',
            ),
            sa.ForeignKeyConstraint(
                ['user_id'],
                ['users.id'],
                name='fk_unit_ownerships_user',
                ondelete='CASCADE',
            ),
            sa.Index('ix_unit_ownerships_unit_user', 'unit_id', 'user_id'),
            sa.Index('ix_unit_ownerships_status', 'status'),
        )


def downgrade() -> None:
    op.drop_table('core_unit_ownerships')