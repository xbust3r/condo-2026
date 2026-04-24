"""
Create core_amenities — tabla de amenidades/áreas comunes del condominio.

Revision ID: 036_create_core_amenities
Revises: 045_seed_visitor_permissions
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '036_create_core_amenities'
down_revision: Union[str, None] = '045_seed_visitor_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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
    if not _table_exists('core_amenities'):
        op.create_table(
            'core_amenities',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, unique=True),
            sa.Column('condominium_id', sa.BigInteger(), nullable=False, index=True),
            sa.Column('name', sa.String(200), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('location', sa.String(255), nullable=True),
            sa.Column('max_capacity', sa.BigInteger(), nullable=False, server_default='1'),
            sa.Column('booking_duration_min', sa.BigInteger(), nullable=False, server_default='60'),
            sa.Column('requires_approval', sa.Boolean(), nullable=False, server_default='0'),
            sa.Column('status', sa.String(20), nullable=False, server_default='active'),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id']),
            sa.Index('ix_amenities_condo_status', 'condominium_id', 'status'),
        )


def downgrade() -> None:
    op.drop_table('core_amenities')
