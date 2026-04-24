"""
Amenity domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class AmenityNotFound(DomainException):
    def __init__(self):
        super().__init__("Amenity not found", status_code=404)


class AmenityValidationError(DomainException):
    def __init__(self, message: str = "Invalid amenity data"):
        super().__init__(message, status_code=400)
