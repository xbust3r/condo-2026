"""
Migration: add theme_id to core_condominiums

Adds optional theme_id column for frontend theme association.
"""
from alembic import op
import sqlalchemy as sa


revision = "024_add_theme_id_to_condominiums"
down_revision = "023_create_core_role_permissions"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "core_condominiums",
        sa.Column("theme_id", sa.String(100), nullable=True)
    )


def downgrade():
    op.drop_column("core_condominiums", "theme_id")
