"""
Vote factory — builds cmd and query use case instances.
"""
from library.dddpy.core_votes.infrastructure.vote_cmd_repository import VoteCmdRepositoryImpl
from library.dddpy.core_votes.infrastructure.vote_query_repository import VoteQueryRepositoryImpl
from library.dddpy.core_votes.usecase.vote_cmd_usecase import VoteCmdUseCase
from library.dddpy.core_votes.usecase.vote_query_usecase import VoteQueryUseCase


def vote_cmd_usecase_factory() -> VoteCmdUseCase:
    return VoteCmdUseCase(repository=VoteCmdRepositoryImpl())


def vote_query_usecase_factory() -> VoteQueryUseCase:
    return VoteQueryUseCase(repository=VoteQueryRepositoryImpl())
