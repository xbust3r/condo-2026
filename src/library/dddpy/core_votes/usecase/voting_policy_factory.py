"""
VotingPolicyFactory — creates policy bundles from a frozen rules_snapshot.
"""
from __future__ import annotations

from library.dddpy.core_votes.domain.vote_rules_snapshot import (
    VotingRulesSnapshot,
    VoteCalculationType,
)
from library.dddpy.core_votes.domain.voter_eligibility_policy import VoterEligibilityPolicy
from library.dddpy.core_votes.domain.vote_weight_policy import VoteWeightPolicy
from library.dddpy.core_votes.usecase.voting_policy_bundle import VotingPolicyBundle


class UnsupportedVoteCalculationType(Exception):
    """Raised when the snapshot contains an unknown calculation type."""
    pass


class VotingPolicyFactory:
    """
    Stateless factory.  Stateless → injected once into the use case.
    Creates a VotingPolicyBundle **per vote** from its frozen rules_snapshot.
    """

    def __init__(
        self,
        eligibility_policy: VoterEligibilityPolicy,
        by_unit_weight_policy: VoteWeightPolicy,
        by_coefficient_weight_policy: VoteWeightPolicy,
    ) -> None:
        self._eligibility_policy = eligibility_policy
        self._by_unit_weight = by_unit_weight_policy
        self._by_coefficient_weight = by_coefficient_weight_policy

    def create(self, snapshot: VotingRulesSnapshot) -> VotingPolicyBundle:
        calc_type = snapshot.vote_calculation_type

        if calc_type == VoteCalculationType.BY_UNIT:
            weight = self._by_unit_weight
        elif calc_type == VoteCalculationType.BY_COEFFICIENT:
            weight = self._by_coefficient_weight
        else:
            raise UnsupportedVoteCalculationType(
                f"Unknown vote_calculation_type: {calc_type}"
            )

        return VotingPolicyBundle(
            eligibility_policy=self._eligibility_policy,
            weight_policy=weight,
        )
