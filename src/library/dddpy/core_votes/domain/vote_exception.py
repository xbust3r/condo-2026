"""
Vote domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class VoteNotFound(DomainException):
    def __init__(self):
        super().__init__("Vote not found", status_code=404)


class UnauthorizedVoteAccess(DomainException):
    def __init__(self, message: str = "User is not eligible to vote in this condominium"):
        super().__init__(message, status_code=403)


class VoteValidationError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class QuorumNotReached(DomainException):
    def __init__(self):
        super().__init__(
            "Quorum was not reached. A new vote is required.",
            status_code=422,
        )


class AlreadyVoted(DomainException):
    def __init__(self):
        super().__init__(
            "You have already cast your vote in this election.",
            status_code=409,
        )
