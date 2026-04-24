"""
Announcement domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class AnnouncementNotFound(DomainException):
    def __init__(self):
        super().__init__("Announcement not found", status_code=404)


class AnnouncementValidationError(DomainException):
    def __init__(self, message: str = "Invalid announcement data"):
        super().__init__(message, status_code=400)
