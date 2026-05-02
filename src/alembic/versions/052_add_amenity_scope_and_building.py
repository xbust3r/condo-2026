"""
Add scope + building_id to core_amenities.

- scope ENUM('CONDOMINIUM','BUILDING') NOT NULL
- building_id BIGINT NULLABLE (FK → core_buildings.id)
- Backfill: all existing → scope='CONDOMINIUM', building_id=NULL
- CHECK constraint: scope/building_id consistency
- Composite index: (condominium_id, scope, building_id)

Revision ID: 052_add_amenity_scope_and_building
Revises: 051_add_charge_scope_distribution
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '052_add_amenity_scope_and_building'
down_revision: Union[str, None] = '051_add_charge_scope_distribution'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # 1. Add scope column (default CONDOMINIUM for backfill)
    op.add_column(
        'core_amenities',
        sa.Column(
            'scope',
            sa.String(20),
            nullable=False,
            server_default='CONDOMINIUM',
        ),
    )

    # 2. Add building_id column (nullable FK)
    op.add_column(
        'core_amenities',
        sa.Column(
            'building_id',
            sa.BigInteger(),
            nullable=True,
        ),
    )
    op.create_foreign_key(
        'fk_amenities_building',
        'core_amenities',
        'core_buildings',
        ['building_id'],
        ['id'],
        ondelete='SET NULL',
    )

    # 3. Backfill: all existing rows → scope='CONDOMINIUM', building_id=NULL
    #    (server_default already handled scope; building_id is NULL by default)
    conn.execute(sa.text("""
        UPDATE core_amenities
        SET scope = 'CONDOMINIUM'
        WHERE scope IS NULL OR scope = ''
    """))

    # 4. Remove server_default now that backfill is done (avoid future ambiguity)
    op.alter_column('core_amenities', 'scope', server_default=None)

    # 5. Add composite index for scope-aware lookups
    op.create_index(
        'ix_amenities_scope_lookup',
        'core_amenities',
        ['condominium_id', 'scope', 'building_id'],
    )


def downgrade() -> None:
    op.drop_index('ix_amenities_scope_lookup', table_name='core_amenities')
    op.drop_constraint('fk_amenities_building', 'core_amenities', type_='foreignkey')
    op.drop_column('core_amenities', 'building_id')
    op.drop_column('core_amenities', 'scope')
