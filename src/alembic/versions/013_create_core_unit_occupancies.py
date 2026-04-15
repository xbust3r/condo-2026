"""
Create core_unit_occupancies — relación de ocupación / uso usuario ↔ unidad.

¿Qué responde?: ¿Quién ocupa, usa o tiene autorización sobre una unidad y bajo qué condición?
¿Qué NO responde?: Propiedad (para eso existe core_unit_ownerships).

Tipos de ocupación:
  resident_owner  — propietario que vive en la unidad
  tenant          — inquilino (arrendatario)
  family_member   — familiar del propietario/inquilino
  office_user     — usuario de oficina comercial
  occasional_user — usuario ocasional (airbnb, prestado, etc.)

Revision ID: 013_create_core_unit_occupancies
Revises: 012_create_core_unit_ownerships
Create Date: 2026-04-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision: str = '013_create_core_unit_occupancies'
down_revision: Union[str, None] = '012_create_core_unit_ownerships'
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
    if not _table_exists('core_unit_occupancies'):
        op.create_table(
            'core_unit_occupancies',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
            sa.Column('unit_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column('user_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column(
                'occupancy_type',
                sa.String(40),
                nullable=False,
                server_default='tenant',
            ),
            sa.Column(
                'status',
                sa.String(30),
                nullable=False,
                server_default='active',
            ),
            sa.Column('start_date', sa.Date(), nullable=True),
            sa.Column('end_date', sa.Date(), nullable=True),
            sa.Column(
                'is_primary',
                sa.Boolean(),
                nullable=False,
                server_default='0',
            ),
            sa.Column('authorized_by_user_id', sa.BigInteger(), nullable=True),
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
                name='fk_unit_occupancies_unit',
                ondelete='CASCADE',
            ),
            sa.ForeignKeyConstraint(
                ['user_id'],
                ['users.id'],
                name='fk_unit_occupancies_user',
                ondelete='CASCADE',
            ),
            sa.ForeignKeyConstraint(
                ['authorized_by_user_id'],
                ['users.id'],
                name='fk_unit_occupancies_authorizer',
                ondelete='SET NULL',
            ),
            sa.Index('ix_unit_occupancies_unit_user', 'unit_id', 'user_id'),
            sa.Index('ix_unit_occupancies_status', 'status'),
            sa.Index('ix_unit_occupancies_occupancy_type', 'occupancy_type'),
        )


def downgrade() -> None:
    op.drop_table('core_unit_occupancies')