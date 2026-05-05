"""Create core_voting_rules config table

Reusable voting rule templates per condominium/building.
When a vote is created, the matching rule is frozen into rules_snapshot.

Revision ID: 072_create_core_voting_rules
Revises: 071_add_vote_scope_and_calc_columns
Create Date: 2026-05-05
"""
from typing import Sequence, Union
from alembic import op


revision: str = "072_create_core_voting_rules"
down_revision: Union[str, None] = "071_add_vote_scope_and_calc_columns"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE core_voting_rules (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            uuid VARCHAR(36) NOT NULL UNIQUE,
            condominium_id BIGINT NOT NULL,
            building_id BIGINT NULL
                COMMENT 'NULL = applies to whole condominium',
            name VARCHAR(100) NOT NULL,

            -- Eligibility
            owners_only BOOLEAN NOT NULL DEFAULT TRUE,
            max_debt_months INT NOT NULL DEFAULT 2
                COMMENT '0 = no debt limit',
            allow_tenants BOOLEAN NOT NULL DEFAULT FALSE,

            -- Vote calculation
            vote_calculation_type VARCHAR(20) NOT NULL DEFAULT 'by_unit',
            include_parking BOOLEAN NOT NULL DEFAULT FALSE,
            include_annexes BOOLEAN NOT NULL DEFAULT FALSE,

            -- Scope
            scope_type VARCHAR(20) NOT NULL DEFAULT 'condominium',

            -- Audits
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_by_user_id BIGINT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NULL,
            deleted_at DATETIME NULL,

            INDEX idx_rule_condo_building (condominium_id, building_id),
            INDEX idx_rule_active (condominium_id, is_active),
            CONSTRAINT fk_voting_rule_condominium
                FOREIGN KEY (condominium_id)
                REFERENCES core_condominiums(id),
            CONSTRAINT fk_voting_rule_created_by
                FOREIGN KEY (created_by_user_id)
                REFERENCES users(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS core_voting_rules")
