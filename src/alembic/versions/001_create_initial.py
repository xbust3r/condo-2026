"""create initial tables

Revision ID: 001_create_initial
Revises: 
Create Date: 2026-03-16

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001_create_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create core_condominiums
    op.create_table(
        'core_condominiums',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('size', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('percentage', sa.DECIMAL(5, 2), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Create core_buildings_types
    op.create_table(
        'core_buildings_types',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Create core_buildings
    op.create_table(
        'core_buildings',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
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
        sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id']),
        sa.ForeignKeyConstraint(['building_type_id'], ['core_buildings_types.id'])
    )

    # Create core_unittys_types
    op.create_table(
        'core_unittys_types',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Create core_unitys
    op.create_table(
        'core_unitys',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
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
        sa.ForeignKeyConstraint(['building_id'], ['core_buildings.id']),
        sa.ForeignKeyConstraint(['unity_type_id'], ['core_unittys_types.id'])
    )

    # Create users
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
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
        sa.UniqueConstraint('email')
    )

    # Create users_residents
    op.create_table(
        'users_residents',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('condominium_id', sa.BigInteger(), nullable=False),
        sa.Column('building_id', sa.BigInteger(), nullable=False),
        sa.Column('unity_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('type', sa.String(100), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['condominium_id'], ['core_condominiums.id']),
        sa.ForeignKeyConstraint(['building_id'], ['core_buildings.id']),
        sa.ForeignKeyConstraint(['unity_id'], ['core_unitys.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )


def downgrade() -> None:
    op.drop_table('users_residents')
    op.drop_table('users')
    op.drop_table('core_unitys')
    op.drop_table('core_unittys_types')
    op.drop_table('core_buildings')
    op.drop_table('core_buildings_types')
    op.drop_table('core_condominiums')
