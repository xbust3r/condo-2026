"""seed vote permissions

Revision ID: 047_seed_vote_permissions
Revises: 046_create_core_votes
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op


revision: str = '047_seed_vote_permissions'
down_revision: Union[str, None] = '046_create_core_votes'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


VOTE_PERMISSIONS_SEED = [
    # votes:create — create a new vote (admin)
    ("votes:create", "votes", "create", "condominium", "Create a new digital vote"),
    # votes:read — view votes and results (authenticated)
    ("votes:read", "votes", "read", "condominium", "View votes and results"),
    # votes:vote — cast a vote (voter)
    ("votes:vote", "votes", "vote", "condominium", "Cast a vote in an active voting"),
    # votes:proclaim — proclaim results (admin)
    ("votes:proclaim", "votes", "proclaim", "condominium", "Proclaim voting results"),
    # votes:cancel — cancel a vote (admin)
    ("votes:cancel", "votes", "cancel", "condominium", "Cancel an active or draft vote"),
]


def upgrade() -> None:
    for code, resource, action, scope_default, description in VOTE_PERMISSIONS_SEED:
        op.execute(
            f"""
            INSERT INTO core_permissions (code, resource, action, scope_default, description)
            VALUES ('{code}', '{resource}', '{action}', '{scope_default}', '{description}')
            ON DUPLICATE KEY UPDATE description = VALUES(description)
            """
        )


def downgrade() -> None:
    for code, _, _, _, _ in VOTE_PERMISSIONS_SEED:
        op.execute(f"DELETE FROM core_permissions WHERE code = '{code}'")
