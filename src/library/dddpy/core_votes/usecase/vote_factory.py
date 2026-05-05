"""
Vote factory — builds cmd and query use case instances.
"""
from library.dddpy.core_votes.infrastructure.vote_cmd_repository import VoteCmdRepositoryImpl
from library.dddpy.core_votes.infrastructure.vote_query_repository import VoteQueryRepositoryImpl
from library.dddpy.core_votes.infrastructure.ownership_guard_impl import OwnershipGuardImpl
from library.dddpy.core_votes.infrastructure.debt_based_eligibility_provider import (
    DebtBasedEligibilityProvider,
)
from library.dddpy.core_votes.infrastructure.by_unit_weight_policy import ByUnitWeightPolicy
from library.dddpy.core_votes.infrastructure.by_coefficient_weight_policy import (
    ByCoefficientWeightPolicy,
)
from library.dddpy.core_votes.usecase.vote_cmd_usecase import VoteCmdUseCase
from library.dddpy.core_votes.usecase.vote_query_usecase import VoteQueryUseCase
from library.dddpy.core_votes.usecase.voting_policy_factory import VotingPolicyFactory


def vote_cmd_usecase_factory() -> VoteCmdUseCase:
    return VoteCmdUseCase(
        repository=VoteCmdRepositoryImpl(),
        ownership_guard=OwnershipGuardImpl(),
        policy_factory=VotingPolicyFactory(
            eligibility_policy=DebtBasedEligibilityProvider(),
            by_unit_weight_policy=ByUnitWeightPolicy(),
            by_coefficient_weight_policy=ByCoefficientWeightPolicy(),
        ),
    )


def vote_query_usecase_factory() -> VoteQueryUseCase:
    return VoteQueryUseCase(repository=VoteQueryRepositoryImpl())
