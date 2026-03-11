"""Create users_residents table

Revision ID: a4b5c6d7e8f9
Revises: f3a4b5c6d7e8
Create Date: 2025-10-29 14:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a4b5c6d7e8f9"
down_revision: Union[str, Sequence[str], None] = "f3a4b5c6d7e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users_residents",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("condominium_id", sa.BigInteger(), nullable=True),
        sa.Column("building_id", sa.BigInteger(), nullable=True),
        sa.Column("unity_id", sa.BigInteger(), nullable=True),
        sa.Column("type", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["condominium_id"], ["core_condominiums.id"], ),
        sa.ForeignKeyConstraint(["building_id"], ["core_buildings.id"], ),
        sa.ForeignKeyConstraint(["unity_id"], ["core_unitys.id"], ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users_residents")
