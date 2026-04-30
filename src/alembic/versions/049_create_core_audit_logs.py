"""create core_audit_logs

Revision ID: 049_create_core_audit_logs
Revises: 047_create_residents
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '049_create_core_audit_logs'
down_revision: Union[str, None] = '047_create_residents'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE core_audit_logs (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            uuid VARCHAR(36) NOT NULL UNIQUE,
            user_id BIGINT NOT NULL,
            action VARCHAR(20) NOT NULL,
            resource_type VARCHAR(50) NOT NULL,
            resource_id BIGINT NOT NULL,
            resource_uuid VARCHAR(36) NOT NULL,
            old_values TEXT NULL,
            new_values TEXT NULL,
            ip_address VARCHAR(45) NULL,
            user_agent VARCHAR(512) NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX ix_audit_resource (resource_type, resource_id),
            INDEX ix_audit_user (user_id),
            INDEX ix_audit_created (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    # FK is added separately to avoid circular dependency with alembic
    op.execute("""
        ALTER TABLE core_audit_logs
        ADD CONSTRAINT fk_audit_user FOREIGN KEY (user_id) REFERENCES users(id)
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS core_audit_logs")