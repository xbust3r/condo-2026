"""
VotingRulesSnapshot — immutable boundary value object.
Freezes voting rules at vote creation time. No live-rule reads after creation.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID


class VoteCalculationType(str, Enum):
    BY_UNIT = "by_unit"
    BY_COEFFICIENT = "by_coefficient"


class VoteScope(str, Enum):
    CONDOMINIUM = "condominium"
    BUILDING = "building"


@dataclass(frozen=True)
class VotingRulesSnapshot:
    """Single typed source of truth for a vote's frozen rules.

    Built once at vote creation via ``from_dict``.  Everything downstream
    (policies, factory, use case) references this, never a raw ``dict``.
    """

    vote_calculation_type: VoteCalculationType
    scope: VoteScope
    building_id: int | None
    allow_only_owners: bool
    allow_tenants: bool
    max_debt_months: Decimal
    include_parking_storage: bool
    snapshot_at: datetime
    snapshot_version: int

    # ── invariants ──────────────────────────────────────────────────────
    def __post_init__(self) -> None:
        if self.scope == VoteScope.BUILDING and self.building_id is None:
            raise ValueError("building_id is required when scope is BUILDING")
        if self.scope == VoteScope.CONDOMINIUM and self.building_id is not None:
            raise ValueError("building_id must be None when scope is CONDOMINIUM")
        if self.max_debt_months < 0:
            raise ValueError("max_debt_months must be >= 0")
        if self.include_parking_storage and self.vote_calculation_type != VoteCalculationType.BY_COEFFICIENT:
            raise ValueError(
                "include_parking_storage only applies to BY_COEFFICIENT"
            )
        if self.snapshot_at.tzinfo is None:
            raise ValueError("snapshot_at must be timezone-aware")

    # ── factory / serialization ─────────────────────────────────────────
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> VotingRulesSnapshot:
        """Validate + hydrate from a raw dict.  The *only* entry point."""
        snapshot_at = datetime.fromisoformat(data["snapshot_at"])
        if snapshot_at.tzinfo is None:
            raise ValueError("snapshot_at must be timezone-aware")
        snapshot_at = snapshot_at.astimezone(timezone.utc)

        building_id_raw = data.get("building_id")
        return cls(
            vote_calculation_type=VoteCalculationType(data["vote_calculation_type"]),
            scope=VoteScope(data["scope"]),
            building_id=int(building_id_raw) if building_id_raw is not None else None,
            allow_only_owners=bool(data["allow_only_owners"]),
            allow_tenants=bool(data["allow_tenants"]),
            max_debt_months=Decimal(str(data["max_debt_months"])),
            include_parking_storage=bool(data.get("include_parking_storage", False)),
            snapshot_at=snapshot_at,
            snapshot_version=int(data["snapshot_version"]),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Canonical serialization for storage + deterministic hashing."""
        return {
            "vote_calculation_type": self.vote_calculation_type.value,
            "scope": self.scope.value,
            "building_id": self.building_id,
            "allow_only_owners": self.allow_only_owners,
            "allow_tenants": self.allow_tenants,
            "max_debt_months": str(self.max_debt_months),
            "include_parking_storage": self.include_parking_storage,
            "snapshot_at": self.snapshot_at.isoformat(),
            "snapshot_version": self.snapshot_version,
        }

    def compute_hash(self) -> str:
        """SHA-256 over the canonical dict (sorted keys, stable formatting)."""
        canonical = json.dumps(
            self.to_dict(),
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
