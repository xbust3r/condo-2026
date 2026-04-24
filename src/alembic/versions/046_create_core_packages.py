"""create core_packages

Revision ID: 046_create_core_packages
Revises: 045_seed_visitor_permissions
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '046_create_core_packages'
down_revision: Union[str, None] = '045_seed_visitor_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE core_packages (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            uuid VARCHAR(36) NOT NULL UNIQUE,
            condominium_id BIGINT NOT NULL,
            unit_id BIGINT NOT NULL,
            recipient_user_id BIGINT NOT NULL,
            carrier VARCHAR(100) NULL,
            tracking_number VARCHAR(100) NULL,
            description TEXT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            received_at DATETIME NULL,
            delivered_at DATETIME NULL,
            pickup_code VARCHAR(4) NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NULL,
            deleted_at DATETIME NULL,
            INDEX ix_packages_condo_status (condominium_id, status),
            INDEX ix_packages_unit_status (unit_id, status),
            INDEX ix_packages_recipient (recipient_user_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS core_packages")
