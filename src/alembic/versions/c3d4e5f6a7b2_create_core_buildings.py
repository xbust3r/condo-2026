"""Create core_buildings table

Revision ID: c3d4e5f6a7b2
Revises: b2c3d4e5f6a1
Create Date: 2025-10-29 10:10:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3d4e5f6a7b2"
down_revision: Union[str, Sequence[str], None] = "b2c3d4e5f6a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "core_buildings",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("size", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("percentage", sa.DECIMAL(5, 2), nullable=True),
        sa.Column("type", sa.String(length=100), nullable=True),
        sa.Column("condominium_id", sa.BigInteger(), nullable=True),
        sa.Column("building_type_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.ForeignKeyConstraint(["condominium_id"], ["core_condominiums.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["building_type_id"], ["core_buildings_types.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("core_buildings")
