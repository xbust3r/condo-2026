"""
Corrective migration: set explicit FK actions on core_buildings

Problem: FK actions for core_buildings referencing core_condominiums and core_buildings_types
were documented but not guaranteed in the original migration.

Required FK actions (from documentation):
  - condominium_id -> RESTRICT (no cascade delete)
  - building_type_id -> SET NULL (allow NULL if type deleted)

Revision ID: 005_fix_buildings_fk_actions
Revises: 004_fix_buildings_unique_constraint
Create Date: 2026-04-13
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '005_fix_buildings_fk_actions'
down_revision: Union[str, None] = '004_fix_buildings_unique_constraint'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop existing FK constraints and recreate with explicit ON DELETE/UPDATE actions
    # The original FKs had no explicit actions (MySQL defaults to NO ACTION)

    # FK: core_buildings.condominium_id -> core_condominiums.id
    # Required: RESTRICT (can't delete condom if buildings exist)
    op.drop_constraint(
        'core_buildings_condominium_id_fk',  # auto-generated name may vary
        'core_buildings',
        type_='foreignkey'
    )
    op.create_foreign_key(
        'core_buildings_condominium_id_fk',
        'core_buildings', 'core_condominiums',
        ['condominium_id'], ['id'],
        ondelete='RESTRICT',
        onupdate='CASCADE'
    )

    # FK: core_buildings.building_type_id -> core_buildings_types.id
    # Required: SET NULL (if type is deleted, building remains without type)
    op.drop_constraint(
        'core_buildings_building_type_id_fk',  # auto-generated name may vary
        'core_buildings',
        type_='foreignkey'
    )
    op.create_foreign_key(
        'core_buildings_building_type_id_fk',
        'core_buildings', 'core_buildings_types',
        ['building_type_id'], ['id'],
        ondelete='SET NULL',
        onupdate='SET NULL'
    )


def downgrade() -> None:
    # Restore FKs without explicit actions (MySQL defaults)
    op.drop_constraint('core_buildings_condominium_id_fk', 'core_buildings', type_='foreignkey')
    op.drop_constraint('core_buildings_building_type_id_fk', 'core_buildings', type_='foreignkey')

    op.create_foreign_key(
        'core_buildings_condominium_id_fk',
        'core_buildings', 'core_condominiums',
        ['condominium_id'], ['id']
    )
    op.create_foreign_key(
        'core_buildings_building_type_id_fk',
        'core_buildings', 'core_buildings_types',
        ['building_type_id'], ['id']
    )