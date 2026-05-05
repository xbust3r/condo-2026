"""Add voter eligibility audit trail and rules_snapshot

- core_votes: add rules_snapshot JSON column
- core_vote_records: add unit_ownership_id + weight, switch UNIQUE from user_id to unit_ownership_id
- voter_eligibility_reason_codes: normalized catalog
- voter_eligibility_log: forensic audit table

Revision ID: 070_add_voter_eligibility_audit
Revises: 069_extend_announcements
Create Date: 2026-05-05
"""
from typing import Sequence, Union
from alembic import op


revision: str = "070_add_voter_eligibility_audit"
down_revision: Union[str, None] = "069_extend_announcements"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = ("047_seed_vote_permissions",)


def upgrade() -> None:
    # ── 1. core_votes: rules_snapshot ──────────────────────────────────────
    op.execute("""
        ALTER TABLE core_votes
        ADD COLUMN rules_snapshot JSON NULL
        COMMENT 'Frozen VotingRulesSnapshot — never mutated after creation'
    """)

    # ── 2. voter_eligibility_reason_codes ──────────────────────────────────
    op.execute("""
        CREATE TABLE voter_eligibility_reason_codes (
            code VARCHAR(50) PRIMARY KEY,
            description VARCHAR(255) NOT NULL,
            category VARCHAR(20) NOT NULL,
            CONSTRAINT ck_reason_code_category CHECK (category IN ('ELIGIBLE','REJECTED'))
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)

    # Seed catalog
    op.execute("""
        INSERT INTO voter_eligibility_reason_codes (code, description, category) VALUES
        ('OWNER_OK',                      'Propietario sin deuda, dentro del scope',                        'ELIGIBLE'),
        ('OWNER_DEBT_WITHIN_LIMIT',       'Propietario con deuda dentro del límite',                         'ELIGIBLE'),
        ('DEBT_EXCEEDED',                 'Deuda superior al límite configurado',                            'REJECTED'),
        ('NOT_OWNER',                     'El usuario no controla esta unidad',                              'REJECTED'),
        ('OWNERSHIP_INACTIVE',            'La relación de propiedad está inactiva',                          'REJECTED'),
        ('TENANT_NOT_ALLOWED',            'Inquilinos no habilitados en esta votación',                      'REJECTED'),
        ('UNIT_NOT_IN_SCOPE',             'La unidad no pertenece al edificio/alcance',                      'REJECTED'),
        ('VOTE_CLOSED',                   'La votación ya fue cerrada',                                      'REJECTED'),
        ('ALREADY_VOTED',                 'Esta unidad ya emitió su voto',                                   'REJECTED'),
        ('SUSPENDED_OWNER',               'Propietario suspendido por junta directiva',                      'REJECTED')
    """)

    # ── 3. voter_eligibility_log ───────────────────────────────────────────
    op.execute("""
        CREATE TABLE voter_eligibility_log (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            vote_id BIGINT NOT NULL,
            unit_ownership_id BIGINT NOT NULL,
            user_id BIGINT NOT NULL,
            eligible BOOLEAN NOT NULL,
            reason_code VARCHAR(50) NOT NULL,
            debt_months_observed DECIMAL(5,2) NULL,
            ownership_observed JSON NULL,
            coefficient_observed DECIMAL(7,4) NULL,
            rules_snapshot_hash VARCHAR(64) NOT NULL,
            evaluated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_eligibility_vote (vote_id),
            INDEX idx_eligibility_vote_unit (vote_id, unit_ownership_id),
            INDEX idx_eligibility_rules_hash (rules_snapshot_hash),
            CONSTRAINT fk_eligibility_log_reason FOREIGN KEY (reason_code)
                REFERENCES voter_eligibility_reason_codes(code)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)

    # ── 4. core_vote_records: switch to unit_ownership_id identity ─────────
    op.execute("""
        ALTER TABLE core_vote_records
        ADD COLUMN unit_ownership_id BIGINT NULL
        COMMENT 'Electoral identity — one per unit_ownership_id per vote'
    """)
    op.execute("""
        ALTER TABLE core_vote_records
        ADD COLUMN weight DECIMAL(12,4) NOT NULL DEFAULT 1.0000
        COMMENT 'Vote weight: 1.0 for BY_UNIT, coefficient for BY_COEFFICIENT'
    """)

    # Drop old UNIQUE constraint and add new one
    op.execute("ALTER TABLE core_vote_records DROP INDEX uk_vote_user")
    op.execute("""
        ALTER TABLE core_vote_records
        ADD UNIQUE KEY uk_vote_unit_ownership (vote_id, unit_ownership_id)
    """)

    # Add index on unit_ownership_id
    op.execute("""
        ALTER TABLE core_vote_records
        ADD INDEX idx_vote_record_unit (unit_ownership_id)
    """)


def downgrade() -> None:
    # core_vote_records: revert
    op.execute("ALTER TABLE core_vote_records DROP INDEX uk_vote_unit_ownership")
    op.execute("ALTER TABLE core_vote_records DROP INDEX idx_vote_record_unit")
    op.execute("ALTER TABLE core_vote_records DROP COLUMN unit_ownership_id")
    op.execute("ALTER TABLE core_vote_records DROP COLUMN weight")
    op.execute("""
        ALTER TABLE core_vote_records
        ADD UNIQUE KEY uk_vote_user (vote_id, user_id)
    """)

    # voter_eligibility_log
    op.execute("DROP TABLE IF EXISTS voter_eligibility_log")

    # voter_eligibility_reason_codes
    op.execute("DROP TABLE IF EXISTS voter_eligibility_reason_codes")

    # core_votes
    op.execute("ALTER TABLE core_votes DROP COLUMN rules_snapshot")
