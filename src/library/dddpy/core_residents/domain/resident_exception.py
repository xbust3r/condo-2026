"""
Resident domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class ResidentProfileNotFound(DomainException):
    def __init__(self):
        super().__init__("Resident profile not found", status_code=404)


class ResidentProfileValidationError(DomainException):
    def __init__(self, message: str = "Invalid resident profile data"):
        super().__init__(message, status_code=400)
