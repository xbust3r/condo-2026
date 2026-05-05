"""
DebtBasedEligibilityProvider — infrastructure implementation of VoterEligibilityPolicy.
Evaluates unit eligibility based on AR debt, ownership type, and vote scope.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func

from library.dddpy.core_votes.domain.voter_eligibility_policy import (
    VoterEligibilityPolicy,
    EligibilityResult,
)
from library.dddpy.core_votes.domain.vote_entity import VoteEntity
from library.dddpy.core_votes.domain.vote_rules_snapshot import VoteScope
from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR
from library.dddpy.core_unit_ownerships.infrastructure.dbunit_ownership import DBUnitOwnership
from library.dddpy.core_units.infrastructure.dbunits import DBUnits
from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("DebtBasedEligibilityProvider")


class DebtBasedEligibilityProvider(VoterEligibilityPolicy):
    """
    Eligibility = scope check + ownership type check + debt check.

    Reads the vote's frozen rules_snapshot.  Never reads live rules.
    """

    def is_eligible(
        self,
        unit_ownership_id: int,
        vote: VoteEntity,
    ) -> EligibilityResult:
        rules = vote.rules_snapshot  # VotingRulesSnapshot

        with session_scope() as session:
            # ── 1. Ownership record ────────────────────────────────────
            own = (
                session.query(DBUnitOwnership)
                .filter(DBUnitOwnership.id == unit_ownership_id)
                .filter(DBUnitOwnership.deleted_at.is_(None))
                .first()
            )
            if own is None:
                return EligibilityResult(
                    eligible=False,
                    reason_code="OWNERSHIP_INACTIVE",
                )

            ownership_observed = {
                "ownership_type": own.ownership_type,
                "status": own.status,
                "unit_id": own.unit_id,
                "user_id": own.user_id,
            }

            # ── 2. Owner / tenant rules ────────────────────────────────
            is_owner = own.ownership_type in ("owner", "co_owner")
            if rules.allow_only_owners and not is_owner:
                return EligibilityResult(
                    eligible=False,
                    reason_code="NOT_OWNER",
                    ownership_observed=ownership_observed,
                )
            if not is_owner and not rules.allow_tenants:
                return EligibilityResult(
                    eligible=False,
                    reason_code="TENANT_NOT_ALLOWED",
                    ownership_observed=ownership_observed,
                )

            # ── 3. Scope check ─────────────────────────────────────────
            if rules.scope == VoteScope.BUILDING:
                unit = (
                    session.query(DBUnits)
                    .filter(DBUnits.id == own.unit_id)
                    .first()
                )
                if unit is None or unit.building_id != rules.building_id:
                    return EligibilityResult(
                        eligible=False,
                        reason_code="UNIT_NOT_IN_SCOPE",
                        ownership_observed=ownership_observed,
                    )

            # ── 4. Debt check ───────────────────────────────────────────
            # Count distinct months with overdue/pending AR for this unit
            today = date.today()
            overdue_count = (
                session.query(func.count(func.distinct(DBAR.period)))
                .filter(DBAR.unit_id == own.unit_id)
                .filter(DBAR.deleted_at.is_(None))
                .filter(DBAR.status.in_(("pending", "partial", "overdue")))
                .filter(DBAR.due_date < today)
                .scalar()
            ) or 0

            debt_months = Decimal(str(overdue_count))

            if debt_months > rules.max_debt_months:
                return EligibilityResult(
                    eligible=False,
                    reason_code="DEBT_EXCEEDED",
                    debt_months_observed=debt_months,
                    ownership_observed=ownership_observed,
                )

            # ── 5. Eligible ─────────────────────────────────────────────
            reason = (
                "OWNER_OK"
                if debt_months == 0
                else "OWNER_DEBT_WITHIN_LIMIT"
            )
            return EligibilityResult(
                eligible=True,
                reason_code=reason,
                debt_months_observed=debt_months,
                ownership_observed=ownership_observed,
            )
