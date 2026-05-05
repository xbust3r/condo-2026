"""Add scope_type, vote_calculation_type, building_id columns to core_votes

Previously these lived only inside the rules_snapshot JSON.
Separate columns enable direct SQL queries without JSON parsing.

Revision ID: 071_add_vote_scope_and_calc_columns
Revises: 070_add_voter_eligibility_audit
Create Date: 2026-05-05
"""
from typing import Sequence, Union
from alembic import op


revision: str = "071_add_vote_scope_and_calc_columns"
down_revision: Union[str, None] = "070_add_voter_eligibility_audit"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. Add scope_type ────────────────────────────────────────────────
    op.execute("""
        ALTER TABLE core_votes
        ADD COLUMN scope_type VARCHAR(20) NOT NULL DEFAULT 'condominium'
        COMMENT 'CONDOMINIUM or BUILDING — who votes'
    """)

    # ── 2. Add vote_calculation_type ─────────────────────────────────────
    op.execute("""
        ALTER TABLE core_votes
        ADD COLUMN vote_calculation_type VARCHAR(20) NOT NULL DEFAULT 'by_unit'
        COMMENT 'by_unit or by_coefficient — how votes are weighted'
    """)

    # ── 3. Add building_id (nullable, for BUILDING scope) ────────────────
    op.execute("""
        ALTER TABLE core_votes
        ADD COLUMN building_id BIGINT NULL
        COMMENT 'FK core_buildings.id — set when scope_type=BUILDING'
    """)

    # ── 4. Add index on building_id ──────────────────────────────────────
    op.execute("""
        ALTER TABLE core_votes
        ADD INDEX idx_vote_building (building_id)
    """)

    # ── 5. Backfill from rules_snapshot (existing votes) ─────────────────
    op.execute("""
        UPDATE core_votes
        SET
            scope_type = COALESCE(
                JSON_UNQUOTE(JSON_EXTRACT(rules_snapshot, '$.scope')),
                'condominium'
            ),
            vote_calculation_type = COALESCE(
                JSON_UNQUOTE(JSON_EXTRACT(rules_snapshot, '$.vote_calculation_type')),
                'by_unit'
            ),
            building_id = CAST(
                JSON_UNQUOTE(JSON_EXTRACT(rules_snapshot, '$.building_id'))
                AS UNSIGNED
            )
        WHERE rules_snapshot IS NOT NULL
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE core_votes DROP INDEX idx_vote_building")
    op.execute("ALTER TABLE core_votes DROP COLUMN building_id")
    op.execute("ALTER TABLE core_votes DROP COLUMN vote_calculation_type")
    op.execute("ALTER TABLE core_votes DROP COLUMN scope_type")
