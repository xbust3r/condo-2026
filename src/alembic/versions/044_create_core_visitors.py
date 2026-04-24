"""create core_visitors

Revision ID: 044_create_core_visitors
Revises: 043_seed_notification_permissions
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '044_create_core_visitors'
down_revision: Union[str, None] = '043_seed_notification_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE core_visitors (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            uuid VARCHAR(36) NOT NULL UNIQUE,
            condominium_id BIGINT NOT NULL,
            building_id BIGINT NULL,
            unit_id BIGINT NOT NULL,
            host_user_id BIGINT NOT NULL,
            visitor_name VARCHAR(150) NOT NULL,
            visitor_document_type VARCHAR(20) NULL,
            visitor_document_number VARCHAR(50) NULL,
            visitor_phone VARCHAR(30) NULL,
            expected_date DATE NOT NULL,
            expected_time TIME NOT NULL,
            actual_checkin_at DATETIME NULL,
            actual_checkout_at DATETIME NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            visit_purpose VARCHAR(30) NOT NULL DEFAULT 'other',
            access_code VARCHAR(10) NULL,
            notes TEXT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NULL,
            deleted_at DATETIME NULL,
            INDEX idx_condo_date_status (condominium_id, expected_date, status),
            INDEX idx_unit (unit_id),
            INDEX idx_host (host_user_id),
            INDEX idx_access_code (condominium_id, access_code)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS core_visitors")