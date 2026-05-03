"""Booking domain exceptions."""
from library.dddpy.shared.decorators.domain_exception import DomainException


class BookingNotFound(DomainException):
    def __init__(self, message: str = "Booking not found"):
        super().__init__(message, status_code=404)


class BookingValidationError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=422)


class BookingOverlapError(DomainException):
    def __init__(self, message: str = "Booking time slot overlaps with an existing reservation"):
        super().__init__(message, status_code=409)


class BookingStatusError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=422)
