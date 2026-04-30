"""
Add birth_date column to user_profiles.

Revision ID: 018_birth_date
Revises: 017_rename_doc
Create Date: 2026-04-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '018_birth_date'
down_revision: Union[str, None] = '017_rename_doc'
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
    if not _column_exists('user_profiles', 'birth_date'):
        op.add_column(
            'user_profiles',
            sa.Column('birth_date', sa.Date(), nullable=True),
        )


def downgrade() -> None:
    if _column_exists('user_profiles', 'birth_date'):
        op.drop_column('user_profiles', 'birth_date')
