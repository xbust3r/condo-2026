"""
Document domain exceptions.
"""
from library.dddpy.shared.decorators.domain_exception import DomainException


class DocumentNotFound(DomainException):
    def __init__(self):
        super().__init__("Document not found", status_code=404)


class DocumentValidationError(DomainException):
    def __init__(self, message: str = "Invalid document data"):
        super().__init__(message, status_code=400)
