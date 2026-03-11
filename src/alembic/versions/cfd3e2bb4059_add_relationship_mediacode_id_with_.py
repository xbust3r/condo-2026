""" add relationship mediacode_id with mediacode table

Revision ID: cfd3e2bb4059
Revises: 45f2c7ac1250
Create Date: 2025-10-28 20:13:35.301048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfd3e2bb4059'
down_revision: Union[str, Sequence[str], None] = '45f2c7ac1250'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:

    op.create_foreign_key(
        'fk_catalog_media_codes_emails_mediacode_id',
        'catalog_media_codes_emails',
        'catalog_media_codes',
        ['mediacode_id'],
        ['id'],
        ondelete='CASCADE'
    )

def downgrade() -> None:
    op.drop_constraint(
        'fk_catalog_media_codes_emails_mediacode_id',
        'catalog_media_codes_emails',
        type_='foreignkey'
    )
