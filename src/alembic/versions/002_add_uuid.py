"""add uuid to all tables

Revision ID: 002_add_uuid
Revises: 001_create_initial
Create Date: 2026-03-16

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_add_uuid'
down_revision: Union[str, None] = '001_create_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # core_condominiums
    op.add_column('core_condominiums', sa.Column('uuid', sa.String(36), nullable=True))
    op.execute("UPDATE core_condominiums SET uuid = UUID()")
    op.alter_column('core_condominiums', 'uuid', nullable=False, type_=sa.String(36))
    op.create_index('ix_condominiums_uuid', 'core_condominiums', ['uuid'], unique=True)
    
    # core_buildings
    op.add_column('core_buildings', sa.Column('uuid', sa.String(36), nullable=True))
    op.execute("UPDATE core_buildings SET uuid = UUID()")
    op.alter_column('core_buildings', 'uuid', nullable=False, type_=sa.String(36))
    op.create_index('ix_buildings_uuid', 'core_buildings', ['uuid'], unique=True)
    
    # core_buildings_types
    op.add_column('core_buildings_types', sa.Column('uuid', sa.String(36), nullable=True))
    op.execute("UPDATE core_buildings_types SET uuid = UUID()")
    op.alter_column('core_buildings_types', 'uuid', nullable=False, type_=sa.String(36))
    op.create_index('ix_buildings_types_uuid', 'core_buildings_types', ['uuid'], unique=True)
    
    # core_unitys
    op.add_column('core_unitys', sa.Column('uuid', sa.String(36), nullable=True))
    op.execute("UPDATE core_unitys SET uuid = UUID()")
    op.alter_column('core_unitys', 'uuid', nullable=False, type_=sa.String(36))
    op.create_index('ix_unitys_uuid', 'core_unitys', ['uuid'], unique=True)
    
    # core_unittys_types
    op.add_column('core_unittys_types', sa.Column('uuid', sa.String(36), nullable=True))
    op.execute("UPDATE core_unittys_types SET uuid = UUID()")
    op.alter_column('core_unittys_types', 'uuid', nullable=False, type_=sa.String(36))
    op.create_index('ix_unittys_types_uuid', 'core_unittys_types', ['uuid'], unique=True)
    
    # users
    op.add_column('users', sa.Column('uuid', sa.String(36), nullable=True))
    op.execute("UPDATE users SET uuid = UUID()")
    op.alter_column('users', 'uuid', nullable=False, type_=sa.String(36))
    op.create_index('ix_users_uuid', 'users', ['uuid'], unique=True)
    
    # users_residents
    op.add_column('users_residents', sa.Column('uuid', sa.String(36), nullable=True))
    op.execute("UPDATE users_residents SET uuid = UUID()")
    op.alter_column('users_residents', 'uuid', nullable=False, type_=sa.String(36))
    op.create_index('ix_residents_uuid', 'users_residents', ['uuid'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_residents_uuid', table_name='users_residents')
    op.drop_column('users_residents', 'uuid')
    op.drop_index('ix_users_uuid', table_name='users')
    op.drop_column('users', 'uuid')
    op.drop_index('ix_unittys_types_uuid', table_name='core_unittys_types')
    op.drop_column('core_unittys_types', 'uuid')
    op.drop_index('ix_unitys_uuid', table_name='core_unitys')
    op.drop_column('core_unitys', 'uuid')
    op.drop_index('ix_buildings_types_uuid', table_name='core_buildings_types')
    op.drop_column('core_buildings_types', 'uuid')
    op.drop_index('ix_buildings_uuid', table_name='core_buildings')
    op.drop_column('core_buildings', 'uuid')
    op.drop_index('ix_condominiums_uuid', table_name='core_condominiums')
    op.drop_column('core_condominiums', 'uuid')
