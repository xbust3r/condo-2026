from typing import Optional
from typing import Optional

from library.dddpy.shared.decorators.domain_exception import DomainException


class CondominiumRoleNotFound(DomainException):
    def __init__(self):
        super().__init__("Condominium role not found", status_code=404)


class DuplicateRoleAssignment(DomainException):
    def __init__(self, message: Optional[str] = None):
        detail = message or "User already has an active role assignment for this condominium"
        super().__init__(detail, status_code=409)


class RoleIsSystem(DomainException):
    def __init__(self):
        super().__init__("System roles cannot be modified", status_code=403)


class InvalidCondominiumRoleData(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class CondominiumNotFoundForRole(DomainException):
    def __init__(self):
        super().__init__("Condominium not found for the specified role assignment", status_code=400)


class UserNotFoundForRole(DomainException):
    def __init__(self):
        super().__init__("User not found for the specified role assignment", status_code=400)
