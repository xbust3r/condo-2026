"""
RolePermission Exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class RolePermissionNotFound(DomainException):
    """Raised when a role-permission mapping is not found."""

    def __init__(self, role: str, permission_code: str) -> None:
        detail = f"Role-permission mapping not found: role={role}, permission={permission_code}"
        super().__init__(detail=detail, status_code=404)


class RoleNotFound(DomainException):
    """Raised when a role has no permissions defined."""

    def __init__(self, role: str) -> None:
        detail = f"No permissions found for role: {role}"
        super().__init__(detail=detail, status_code=404)
