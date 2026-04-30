"""
Clean invalid UUIDs from database tables.

UUIDs should follow format: 8-4-4-4-12 hex chars.
Some seed/fixture inserts used arbitrary strings like '2', 'test-condo-1-uuid'.

Revision ID: 020_clean_invalid_uuids
Revises: 019_condo_coefficient
Create Date: 2026-04-16
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '020_clean_invalid_uuids'
down_revision: Union[str, None] = '019_condo_coefficient'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Regenerate invalid UUIDs in core_condominiums
    op.execute("""
        UPDATE core_condominiums
        SET uuid = UUID()
        WHERE uuid NOT REGEXP '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    """)
    # Regenerate invalid UUIDs in core_buildings
    op.execute("""
        UPDATE core_buildings
        SET uuid = UUID()
        WHERE uuid NOT REGEXP '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    """)
    # Regenerate invalid UUIDs in core_condominium_roles
    op.execute("""
        UPDATE core_condominium_roles
        SET uuid = UUID()
        WHERE uuid NOT REGEXP '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    """)


def downgrade() -> None:
    pass