"""Add emergency_contact, notification_preferences, avatar_url to user_profiles.

Revision ID: 050_add_user_profile_extra_fields
Revises: 049_create_core_audit_logs
Create Date: 2026-04-28
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = "050_add_user_profile_extra_fields"
down_revision: str = "049_create_core_audit_logs"
branch_labels: list = []
depends_on: list = []


def upgrade() -> None:
    # emergency_contact — JSON string (name + phone del contacto de emergencia)
    op.add_column(
        "user_profiles",
        sa.Column("emergency_contact", sa.JSON(), nullable=True),
    )
    # notification_preferences — JSON object con prefs de notificación
    op.add_column(
        "user_profiles",
        sa.Column("notification_preferences", sa.JSON(), nullable=True),
    )
    # avatar_url — URL pública del avatar
    op.add_column(
        "user_profiles",
        sa.Column("avatar_url", sa.String(500), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("user_profiles", "avatar_url")
    op.drop_column("user_profiles", "notification_preferences")
    op.drop_column("user_profiles", "emergency_contact")
