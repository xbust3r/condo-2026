"""
Audit log domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class AuditLogNotFound(DomainException):
    def __init__(self, message: str = "Audit log entry not found"):
        self.message = message
        self.status_code = 404
        super().__init__(self.message, self.status_code)