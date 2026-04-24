"""Create core_votes — digital voting system

Revision ID: 046_create_core_votes
Revises: 045_seed_visitor_permissions
Create Date: 2026-04-24
"""
from typing import Sequence, Union
from alembic import op


revision: str = '046_create_core_votes'
down_revision: Union[str, None] = '045_seed_visitor_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── core_votes ───────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE core_votes (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            uuid VARCHAR(36) NOT NULL UNIQUE,
            condominium_id BIGINT NOT NULL,
            meeting_id BIGINT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            voting_starts_at DATETIME NOT NULL,
            voting_ends_at DATETIME NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'draft',
            vote_type VARCHAR(20) NOT NULL DEFAULT 'open',
            quorum_required BOOLEAN NOT NULL DEFAULT FALSE,
            quorum_percentage INT NOT NULL DEFAULT 51,
            approval_threshold INT NOT NULL DEFAULT 51,
            total_eligible_voters INT NOT NULL DEFAULT 0,
            total_votes_cast INT NOT NULL DEFAULT 0,
            total_yes_votes INT NOT NULL DEFAULT 0,
            total_no_votes INT NOT NULL DEFAULT 0,
            total_abstain_votes INT NOT NULL DEFAULT 0,
            result_proclaimed_at DATETIME NULL,
            created_by_user_id BIGINT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
            deleted_at DATETIME NULL,
            INDEX idx_condo_status (condominium_id, status),
            INDEX idx_ends (voting_ends_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)

    # ── core_vote_options ────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE core_vote_options (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            vote_id BIGINT NOT NULL,
            option_text VARCHAR(100) NOT NULL,
            option_key VARCHAR(20) NOT NULL,
            vote_count INT NOT NULL DEFAULT 0,
            UNIQUE KEY uk_vote_option (vote_id, option_key)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)

    # ── core_vote_records ─────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE core_vote_records (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            vote_id BIGINT NOT NULL,
            user_id BIGINT NOT NULL,
            option_key VARCHAR(20) NOT NULL,
            voted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uk_vote_user (vote_id, user_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS core_vote_records")
    op.execute("DROP TABLE IF EXISTS core_vote_options")
    op.execute("DROP TABLE IF EXISTS core_votes")
