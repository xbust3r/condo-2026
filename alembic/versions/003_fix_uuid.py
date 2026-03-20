"""fix uuid not null and add index

Revision ID: 003_fix_uuid
Revises: 002_add_uuid
Create Date: 2026-03-16

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '003_fix_uuid'
down_revision: Union[str, None] = '002_add_uuid'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    tables = ['core_condominiums', 'core_buildings', 'core_buildings_types', 
              'core_unitys', 'core_unittys_types', 'users', 'users_residents']
    
    for table in tables:
        # Fill null UUIDs
        op.execute(f"UPDATE {table} SET uuid = UUID() WHERE uuid IS NULL")
        # Make not nullable
        op.alter_column(table, 'uuid', nullable=False, type_=sa.String(36))
        # Create index
        index_name = f'ix_{table}_uuid'
        if table == 'users_residents':
            index_name = 'ix_residents_uuid'
        op.create_index(index_name, table, ['uuid'], unique=True)


def downgrade() -> None:
    pass
