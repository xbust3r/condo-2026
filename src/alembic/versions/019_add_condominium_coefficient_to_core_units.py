"""
Add condominium_coefficient to core_units.

Required for maintenance fee calculations. The coefficient represents
the unit's percentage participation in the condominium's total (0-100).

Revision ID: 019_add_condominium_coefficient_to_core_units
Revises: 018_add_birth_date_to_user_profiles
Create Date: 2026-04-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '019_add_condominium_coefficient_to_core_units'
down_revision: Union[str, None] = '018_add_birth_date_to_user_profiles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table: str, column: str) -> bool:
    result = op.get_bind().execute(
        sa.text("""
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME = :column
        """),
        {"table": table, "column": column},
    )
    return result.scalar() > 0


def upgrade() -> None:
    if not _column_exists('core_units', 'condominium_coefficient'):
        op.add_column(
            'core_units',
            sa.Column('condominium_coefficient', sa.DECIMAL(9, 6), nullable=True),
        )


def downgrade() -> None:
    if _column_exists('core_units', 'condominium_coefficient'):
        op.drop_column('core_units', 'condominium_coefficient')