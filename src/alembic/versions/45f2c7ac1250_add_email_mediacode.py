"""add email mediacode

Revision ID: 45f2c7ac1250
Revises:
Create Date: 2025-10-27 20:33:50.945424

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "45f2c7ac1250"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "catalog_media_codes_emails",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("mediacode_id", sa.BigInteger(), nullable=False),
        sa.Column("description", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        # Remover la foreign key por ahora ya que la tabla catalog_media_codes no existe
        # sa.ForeignKeyConstraint(["mediacode_id"], ["catalog_media_codes.id"], ondelete="CASCADE")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("catalog_media_codes_emails")
