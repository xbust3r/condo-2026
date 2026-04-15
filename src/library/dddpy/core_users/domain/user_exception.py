"""
User exceptions — all extend DomainException for proper HTTP status mapping.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class UserNotFound(DomainException):
    """Raised when a user is not found by id or uuid."""

    def __init__(self, message: str = "User not found"):
        super().__init__(message=message, status_code=404)


class UserAlreadyExists(DomainException):
    """Raised when attempting to create or update a user with a duplicate email."""

    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(message=message, status_code=409)


class UserInvalidStatus(DomainException):
    """Raised when a status transition is invalid."""

    def __init__(self, message: str = "Invalid status transition"):
        super().__init__(message=message, status_code=422)


class UserPasswordRequired(DomainException):
    """Raised when password is missing on user creation."""

    def __init__(self, message: str = "Password is required"):
        super().__init__(message=message, status_code=400)
