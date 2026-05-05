"""
VoterEligibilityPolicy — domain interface for eligibility checks.
Operates on unit_ownership_id, NOT user_id.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class EligibilityResult:
    """Immutable result of an eligibility evaluation."""
    eligible: bool
    reason_code: str
    debt_months_observed: Decimal | None = None
    ownership_observed: Dict[str, Any] | None = None
    coefficient_observed: Decimal | None = None
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eligible": self.eligible,
            "reason_code": self.reason_code,
            "debt_months_observed": str(self.debt_months_observed)
                if self.debt_months_observed is not None else None,
            "ownership_observed": self.ownership_observed,
            "coefficient_observed": str(self.coefficient_observed)
                if self.coefficient_observed is not None else None,
            "evaluated_at": self.evaluated_at.isoformat(),
        }


class VoterEligibilityPolicy(ABC):
    """
    Validates whether a specific unit_ownership_id can vote
    in a given vote, according to the vote's frozen rules_snapshot.

    Responsibility:
    - scope check (unit belongs to building / condominium)
    - debt check (months_debt <= max_debt_months)
    - owner/tenant rules (allow_only_owners, allow_tenants)
    """

    @abstractmethod
    def is_eligible(
        self,
        unit_ownership_id: int,
        vote,  # VoteEntity — forward ref to avoid circular import
    ) -> EligibilityResult:
        ...
