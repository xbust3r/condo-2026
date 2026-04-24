"""seed visitor permissions

Revision ID: 045_seed_visitor_permissions
Revises: 044_create_core_visitors
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op


revision: str = '045_seed_visitor_permissions'
down_revision: Union[str, None] = '044_create_core_visitors'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


VISITOR_PERMISSIONS_SEED = [
    # visitors:create — register visitor (host)
    ("visitors:create", "visitors", "create", "condominium", "Register visitor for a unit"),
    # visitors:read — view visitors (host, security, admin)
    ("visitors:read", "visitors", "read", "condominium", "View visitor records"),
    # visitors:checkin — check-in / check-out visitors (security_staff)
    ("visitors:checkin", "visitors", "checkin", "condominium", "Check-in or check-out visitors"),
    # visitors:cancel — cancel visitor registration (host or admin)
    ("visitors:cancel", "visitors", "cancel", "condominium", "Cancel a visitor registration"),
]


def upgrade() -> None:
    for code, resource, action, scope_default, description in VISITOR_PERMISSIONS_SEED:
        op.execute(
            f"""
            INSERT INTO core_permissions (code, resource, action, scope_default, description)
            VALUES ('{code}', '{resource}', '{action}', '{scope_default}', '{description}')
            ON DUPLICATE KEY UPDATE description = VALUES(description)
            """
        )


def downgrade() -> None:
    for code, _, _, _, _ in VISITOR_PERMISSIONS_SEED:
        op.execute(f"DELETE FROM core_permissions WHERE code = '{code}'")