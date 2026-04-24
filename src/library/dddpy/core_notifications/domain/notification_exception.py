"""
Notification domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class NotificationNotFound(DomainException):
    def __init__(self):
        super().__init__("Notification not found", status_code=404)


class NotificationValidationError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class UnauthorizedNotificationAccess(DomainException):
    def __init__(self):
        super().__init__(
            "User does not have permission to access this notification",
            status_code=403,
        )