"""
VotingPolicyBundle — typed container for policies resolved per vote.
"""
from __future__ import annotations

from dataclasses import dataclass

from library.dddpy.core_votes.domain.voter_eligibility_policy import VoterEligibilityPolicy
from library.dddpy.core_votes.domain.vote_weight_policy import VoteWeightPolicy


@dataclass(frozen=True)
class VotingPolicyBundle:
    """Policies resolved from a vote's rules_snapshot.  Injected per-vote."""
    eligibility_policy: VoterEligibilityPolicy
    weight_policy: VoteWeightPolicy
