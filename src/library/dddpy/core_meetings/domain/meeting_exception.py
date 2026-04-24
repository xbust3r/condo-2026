"""
Meeting domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class MeetingNotFound(DomainException):
    def __init__(self):
        super().__init__("Meeting not found", status_code=404)


class MeetingValidationError(DomainException):
    def __init__(self, message: str = "Invalid meeting data"):
        super().__init__(message, status_code=400)
