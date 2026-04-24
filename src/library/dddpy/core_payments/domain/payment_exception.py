"""
Payment domain exceptions.
"""
from library.dddpy.shared.mysql.base import DomainException


class PaymentNotFound(DomainException):
    def __init__(self, message: str = "Payment not found"):
        self.message = message
        super().__init__(self.message)


class PaymentExceedsBalance(DomainException):
    def __init__(self, message: str = "Payment amount exceeds pending balance"):
        self.message = message
        super().__init__(self.message)
