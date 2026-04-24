"""
Seed incident permissions into core_permissions.

Revision ID: 041_seed_incident_permissions
Revises: 040_create_core_incidents
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '041_seed_incident_permissions'
down_revision: Union[str, None] = '040_create_core_incidents'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


INCIDENT_PERMISSIONS_SEED = [
    # incidents:create — any authenticated user with occupancy/ownership in the unit
    ("incidents:create", "incidents", "create", "unit",        "Report maintenance incidents"),
    # incidents:read — same condominium (owner/tenant + role staff/admin)
    ("incidents:read",   "incidents", "read",   "condominium", "View incidents"),
    # incidents:update — maintenance_staff, board_member, condominium_admin
    ("incidents:update", "incidents", "update", "condominium", "Update incident status/priority"),
    # incidents:assign — board_member, condominium_admin
    ("incidents:assign", "incidents", "assign", "condominium", "Assign incidents to staff"),
    # incidents:escalate — condominium_admin
    ("incidents:escalate", "incidents", "escalate", "condominium", "Escalate urgent incidents"),
    # incidents:delete — condominium_admin
    ("incidents:delete", "incidents", "delete", "condominium", "Cancel/delete incidents"),
]


def upgrade() -> None:
    for code, resource, action, scope_default, description in INCIDENT_PERMISSIONS_SEED:
        op.execute(
            f"""
            INSERT INTO core_permissions (code, resource, action, scope_default, description)
            VALUES ('{code}', '{resource}', '{action}', '{scope_default}', '{description}')
            ON DUPLICATE KEY UPDATE description = VALUES(description)
            """
        )


def downgrade() -> None:
    for code, _, _, _, _ in INCIDENT_PERMISSIONS_SEED:
        op.execute(f"DELETE FROM core_permissions WHERE code = '{code}'")
