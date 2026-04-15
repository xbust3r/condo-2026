"""
User exceptions.
"""
class UserException(Exception):
    """Base exception for user operations."""
    pass


class UserNotFound(UserException):
    """Raised when a user is not found by id or uuid."""
    pass


class UserAlreadyExists(UserException):
    """Raised when attempting to create a user with a duplicate email."""
    pass


class UserInvalidStatus(UserException):
    """Raised when a status transition is invalid."""
    pass


class UserPasswordRequired(UserException):
    """Raised when password is missing on user creation."""
    pass
