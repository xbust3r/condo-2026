"""
Incident domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class IncidentNotFound(DomainException):
    def __init__(self):
        super().__init__("Incident not found", status_code=404)


class UnauthorizedIncidentAccess(DomainException):
    def __init__(self):
        super().__init__(
            "User does not have an active occupancy or ownership in this unit to report incidents",
            status_code=403,
        )


class IncidentValidationError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
