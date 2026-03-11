"""Create core_buildings_types table

Revision ID: b2c3d4e5f6a1
Revises: a1b2c3d4e5f0
Create Date: 2025-10-29 10:05:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a1"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "core_buildings_types",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("core_buildings_types")
