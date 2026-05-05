"""
VotingRuleEntity — domain entity for a voting rule configuration.
Represents a reusable rule template scoped to a condominium (or building).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class VotingRuleEntity:
    """
    A voting rule template that defines how votes are configured
    for a condominium or building.

    When a vote is created, the matching rule is frozen into
    a VotingRulesSnapshot — the live rule may change without
    affecting active votes.
    """

    id: int
    uuid: str
    condominium_id: int
    name: str

    # Eligibility
    owners_only: bool = True
    max_debt_months: int = 2
    allow_tenants: bool = False

    # Vote calculation
    vote_calculation_type: str = "by_unit"  # by_unit | by_coefficient
    include_parking: bool = False
    include_annexes: bool = False

    # Scope
    scope_type: str = "condominium"  # condominium | building
    building_id: Optional[int] = None

    # Lifecycle
    is_active: bool = True
    created_by_user_id: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "name": self.name,
            "owners_only": self.owners_only,
            "max_debt_months": self.max_debt_months,
            "allow_tenants": self.allow_tenants,
            "vote_calculation_type": self.vote_calculation_type,
            "include_parking": self.include_parking,
            "include_annexes": self.include_annexes,
            "scope_type": self.scope_type,
            "building_id": self.building_id,
            "is_active": self.is_active,
            "created_by_user_id": self.created_by_user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }
