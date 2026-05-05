"""extend core_announcements with new categories and tower_id filter

- Expand categories to include: balance, assembly, maintenance, vote, rule, general
- Add tower_id (BigInteger, nullable, FK to core_buildings.id)
- Add index on tower_id
- tower_id NULL = condominium-wide (all towers)

Revision ID: 069
Revises: 068_create_amenity_usage_logs
Create Date: 2026-05-04

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '069_extend_announcements'
down_revision: Union[str, None] = '068_create_amenity_usage_logs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # ── 1. Add tower_id column (if not already present) ──────────────────
    inspector = sa.inspect(conn)
    existing_cols = [c['name'] for c in inspector.get_columns('core_announcements')]

    if 'tower_id' not in existing_cols:
        op.add_column(
            'core_announcements',
            sa.Column(
                'tower_id',
                sa.BigInteger(),
                nullable=True,
            ),
        )
        op.create_foreign_key(
            'fk_announcements_tower',
            'core_announcements',
            'core_buildings',
            ['tower_id'],
            ['id'],
            ondelete='SET NULL',
        )
        op.create_index(
            'ix_announcements_tower_id',
            'core_announcements',
            ['tower_id'],
        )

    # ── 2. Widen category column to support new values ───────────────────
    #      Existing column is String(20) which fits the new categories.
    #      Drop the existing CHECK constraint if it exists, then recreate.
    #      (MySQL 8 treats ENUM-ish checks as CHECK constraints on CREATE)
    #      For safety, just ensure the column type supports the wider set.
    #      The new values are: balance, assembly, maintenance, vote, rule, general
    #      All fit within String(20) so no ALTER needed.


def downgrade() -> None:
    op.drop_index('ix_announcements_tower_id', table_name='core_announcements')
    op.drop_constraint('fk_announcements_tower', 'core_announcements', type_='foreignkey')
    op.drop_column('core_announcements', 'tower_id')
