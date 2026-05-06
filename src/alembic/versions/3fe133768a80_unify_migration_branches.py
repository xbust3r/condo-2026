"""unify_migration_branches

Revision ID: 3fe133768a80
Revises: 036_create_core_amenities, 047_seed_vote_permissions, 048_create_core_meetings, 053_add_amenity_scope_check, 073_add_auth_sessions_indexes
Create Date: 2026-05-06 12:58:05.120646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fe133768a80'
down_revision: Union[str, None] = ('036_create_core_amenities', '047_seed_vote_permissions', '048_create_core_meetings', '053_add_amenity_scope_check', '073_add_auth_sessions_indexes')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
