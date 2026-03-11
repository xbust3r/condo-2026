"""Create core_unitys table

Revision ID: e2f3a4b5c6d7
Revises: d1e2f3a4b5c6
Create Date: 2025-10-29 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e2f3a4b5c6d7"
down_revision: Union[str, Sequence[str], None] = "d1e2f3a4b5c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "core_unitys",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("size", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("percentage", sa.DECIMAL(5, 2), nullable=True),
        sa.Column("type", sa.String(length=100), nullable=True),
        sa.Column("floor", sa.Integer(), nullable=True),
        sa.Column("unit", sa.String(length=50), nullable=True),
        sa.Column("building_id", sa.BigInteger(), nullable=True),
        sa.Column("unity_type_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.ForeignKeyConstraint(["building_id"], ["core_buildings.id"], ),
        sa.ForeignKeyConstraint(["unity_type_id"], ["core_unittys_types.id"], ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("core_unitys")
