"""Visitor domain exceptions."""
from library.dddpy.shared.decorators.domain_exception import DomainException


class VisitorNotFound(DomainException):
    def __init__(self):
        super().__init__("Visitor not found", status_code=404)


class UnauthorizedVisitorAccess(DomainException):
    def __init__(self):
        super().__init__(
            "User does not have an active occupancy or ownership in this unit to register visitors",
            status_code=403,
        )


class VisitorValidationError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)