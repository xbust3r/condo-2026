"""
Auth domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class InvalidCredentials(DomainException):
    """Raised on wrong email or password. Same message for both to prevent enum."""

    def __init__(self):
        super().__init__(
            "Invalid email or password",
            status_code=401,
        )


class UserAccountLocked(DomainException):
    """Raised when account is locked due to failed attempts."""

    def __init__(self):
        super().__init__(
            "Account is temporarily locked due to too many failed attempts. Try again later.",
            status_code=423,
        )


class UserAccountInactive(DomainException):
    """Raised when account status is not active."""

    def __init__(self):
        super().__init__(
            "Account is not active. Contact your administrator.",
            status_code=403,
        )


class UserEmailNotVerified(DomainException):
    """Raised when email is not yet verified."""

    def __init__(self):
        super().__init__(
            "Email address has not been verified",
            status_code=403,
        )


class SessionExpired(DomainException):
    """Raised when session has expired or been revoked."""

    def __init__(self):
        super().__init__(
            "Session expired or revoked",
            status_code=401,
        )


class TokenInvalid(DomainException):
    """Raised when token is malformed, expired, or tampered."""

    def __init__(self):
        super().__init__(
            "Token is invalid or expired",
            status_code=401,
        )


class RefreshTokenUsed(DomainException):
    """Raised when a refresh token has already been used (possible attack)."""

    def __init__(self):
        super().__init__(
            "Session revoked due to security event",
            status_code=401,
        )



class RateLimitExceeded(DomainException):
    """Raised when too many requests hit an auth endpoint."""

    def __init__(self, retry_after_seconds: int = 60):
        super().__init__(
            f"Too many requests. Please try again in {retry_after_seconds} seconds.",
            status_code=429,
        )
        self.retry_after_seconds = retry_after_seconds



class EmailTokenExpired(DomainException):
    """Raised when an email token (reset/verify) has expired."""


    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, status_code=400)
