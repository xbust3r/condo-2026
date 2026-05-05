"""
ByUnitWeightPolicy — every unit_ownership_id gets weight 1.0.
"""
from decimal import Decimal

from library.dddpy.core_votes.domain.vote_weight_policy import VoteWeightPolicy
from library.dddpy.core_votes.domain.vote_entity import VoteEntity


class ByUnitWeightPolicy(VoteWeightPolicy):
    """BY_UNIT: each unit = 1 vote, weight = 1.0."""

    def calculate_weight(
        self,
        unit_ownership_id: int,
        vote: VoteEntity,
    ) -> Decimal:
        return Decimal("1.0")
