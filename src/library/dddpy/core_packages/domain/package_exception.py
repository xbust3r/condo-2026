"""Package domain exceptions."""
from library.dddpy.shared.decorators.domain_exception import DomainException


class PackageNotFound(DomainException):
    def __init__(self):
        super().__init__("Package not found", status_code=404)


class PackageValidationError(DomainException):
    def __init__(self, message: str = "Invalid package data"):
        super().__init__(message, status_code=400)
