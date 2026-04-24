"""
Create core_resident_profiles — preferences and settings per user per condominium.

Revision ID: 047_create_core_resident_profiles
Revises: 046_create_core_packages
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '047_create_core_resident_profiles'
down_revision: Union[str, None] = '046_create_core_packages'
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
    if not _table_exists('core_resident_profiles'):
        op.create_table(
            'core_resident_profiles',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(36), nullable=False, unique=True),
            sa.Column('user_id', sa.BigInteger(), nullable=False),
            sa.Column('condominium_id', sa.BigInteger(), nullable=False),
            # Notification preferences (JSON for flexibility)
            sa.Column('notify_announcements', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('notify_incidents', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('notify_packages', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('notify_visitors', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('notify_payments', sa.Boolean(), nullable=False, server_default='1'),
            # App preferences
            sa.Column('language', sa.String(10), nullable=False, server_default='es'),
            sa.Column('theme', sa.String(20), nullable=False, server_default='light'),
            sa.Column('default_building_id', sa.BigInteger(), nullable=True),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('updated_at', sa.DateTime(), nullable=True, onupdate=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.UniqueConstraint('user_id', 'condominium_id', name='uq_resident_profile_user_condo'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id']),
            sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id']),
            sa.ForeignKeyConstraint(['default_building_id'], ['core_buildings.id']),
            sa.Index('ix_resident_profiles_user_condo', 'user_id', 'condominium_id'),
        )


def downgrade() -> None:
    op.drop_table('core_resident_profiles')
