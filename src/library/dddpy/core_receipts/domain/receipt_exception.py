"""
Receipt domain exceptions.
"""
from library.dddpy.shared.mysql.base import DomainException


class ReceiptNotFound(DomainException):
    def __init__(self, message: str = "Receipt not found"):
        self.message = message
        super().__init__(self.message)


class ReceiptNumberAlreadyExists(DomainException):
    def __init__(self, message: str = "Receipt number already exists"):
        self.message = message
        super().__init__(self.message)
