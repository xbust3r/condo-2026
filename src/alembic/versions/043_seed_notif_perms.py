"""seed notification permissions

Revision ID: 043_seed_notif_perms
Revises: 042_create_core_notifications
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '043_seed_notif_perms'
down_revision: Union[str, None] = '042'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NOTIFICATION_PERMISSIONS_SEED = [
    # notifications:read — view own notifications
    ("notifications:read", "notifications", "read", "user", "View own notifications"),
    # notifications:read_all — view all notifications (admin)
    ("notifications:read_all", "notifications", "read_all", "condominium", "View all notifications"),
    # notifications:delete — delete own notifications
    ("notifications:delete", "notifications", "delete", "user", "Delete own notifications"),
]


def upgrade() -> None:
    for code, resource, action, scope_default, description in NOTIFICATION_PERMISSIONS_SEED:
        op.execute(
            f"""
            INSERT INTO core_permissions (code, resource, action, scope_default, description)
            VALUES ('{code}', '{resource}', '{action}', '{scope_default}', '{description}')
            ON DUPLICATE KEY UPDATE description = VALUES(description)
            """
        )


def downgrade() -> None:
    for code, _, _, _, _ in NOTIFICATION_PERMISSIONS_SEED:
        op.execute(f"DELETE FROM core_permissions WHERE code = '{code}'")