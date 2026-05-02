"""
Add CHECK constraint for amenity scope/building_id consistency.

Rules:
- scope=CONDOMINIUM → building_id MUST be NULL
- scope=BUILDING → building_id MUST NOT be NULL

Revision ID: 053_add_amenity_scope_check
Revises: 052_add_amenity_scope_and_building
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '053_add_amenity_scope_check'
down_revision: Union[str, None] = '052_add_amenity_scope_and_building'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        'ck_amenities_scope_building_consistency',
        'core_amenities',
        (
            "(scope = 'CONDOMINIUM' AND building_id IS NULL) "
            "OR (scope = 'BUILDING' AND building_id IS NOT NULL)"
        ),
    )


def downgrade() -> None:
    op.drop_constraint(
        'ck_amenities_scope_building_consistency',
        'core_amenities',
        type_='check',
    )
