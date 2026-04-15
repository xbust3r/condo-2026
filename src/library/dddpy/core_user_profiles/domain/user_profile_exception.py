"""
User profile exceptions — all extend DomainException for proper HTTP status mapping.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class UserProfileNotFound(DomainException):
    """Raised when a profile is not found."""

    def __init__(self, message: str = "Profile not found"):
        super().__init__(message=message, status_code=404)


class UserProfileAlreadyExists(DomainException):
    """Raised when attempting to create a profile that already exists."""

    def __init__(self, message: str = "Profile already exists for this user"):
        super().__init__(message=message, status_code=409)
