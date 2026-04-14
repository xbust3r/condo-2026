"""create initial tables

Revision ID: 001_create_initial
Revises: 
Create Date: 2026-03-16

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# --- ESTAS VARIABLES SON CRÍTICAS ---
# Alembic las usa para rastrear la migración. 
# El valor de 'revision' debe coincidir con el prefijo del nombre del archivo si es posible.
revision = '001_create_initial'
down_revision = None
branch_labels = None
depends_on = None
# ------------------------------------

def upgrade() -> None:
    # Create core_condominiums with UPDATED schema (2026-04-13)
    op.create_table(
        'core_condominiums',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('legal_name', sa.String(255), nullable=True),
        sa.Column('document_number', sa.String(50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('land_area', sa.DECIMAL(12, 4), nullable=True),
        sa.Column('built_area', sa.DECIMAL(12, 4), nullable=True),
        sa.Column('area_unit', sa.String(20), server_default='m2', nullable=True),
        sa.Column('address', sa.String(500), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('contact_email', sa.String(255), nullable=True),
        sa.Column('contact_phone', sa.String(50), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.UniqueConstraint('uuid')
    )

    # Create core_buildings_types
    op.create_table(
        'core_buildings_types',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.UniqueConstraint('uuid')
    )

    # Create core_buildings
    op.create_table(
        'core_buildings',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('size', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('percentage', sa.DECIMAL(5, 2), nullable=True),
        sa.Column('type', sa.String(100), nullable=True),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False),
        sa.Column('building_type_id', sa.BigInteger(), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.UniqueConstraint('uuid'),
        sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id']),
        sa.ForeignKeyConstraint(['building_type_id'], ['core_buildings_types.id'])
    )

    # Create core_unittys_types
    op.create_table(
        'core_unittys_types',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.UniqueConstraint('uuid')
    )

    # Create core_unities
    op.create_table(
        'core_unities',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('size', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('percentage', sa.DECIMAL(5, 2), nullable=True),
        sa.Column('type', sa.String(100), nullable=True),
        sa.Column('floor', sa.Integer(), nullable=True),
        sa.Column('unit', sa.String(50), nullable=True),
        sa.Column('building_id', sa.BigInteger(), nullable=False),
        sa.Column('unity_type_id', sa.BigInteger(), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.UniqueConstraint('uuid'),
        sa.ForeignKeyConstraint(['building_id'], ['core_buildings.id']),
        sa.ForeignKeyConstraint(['unity_type_id'], ['core_unittys_types.id'])
    )

    # Create users
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=True),
        sa.Column('doc_identity', sa.String(50), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('uuid')
    )

    # Create users_residents
    op.create_table(
        'users_residents',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False, server_default=sa.text('(UUID())')),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False),
        sa.Column('building_id', sa.BigInteger(), nullable=False),
        sa.Column('unity_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('type', sa.String(100), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid'),
        sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id']),
        sa.ForeignKeyConstraint(['building_id'], ['core_buildings.id']),
        sa.ForeignKeyConstraint(['unity_id'], ['core_unities.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )

def downgrade() -> None:
    op.drop_table('users_residents')
    op.drop_table('users')
    op.drop_table('core_unities')
    op.drop_table('core_unittys_types')
    op.drop_table('core_buildings')
    op.drop_table('core_buildings_types')
    op.drop_table('core_condominiums')
