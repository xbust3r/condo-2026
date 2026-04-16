"""
Permission Exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class PermissionNotFound(DomainException):
    """Raised when a permission is not found."""

    def __init__(self, identifier: str | int) -> None:
        detail = (
            f"Permission not found by id={identifier}"
            if isinstance(identifier, int)
            else f"Permission not found: {identifier}"
        )
        super().__init__(detail=detail, status_code=404)
