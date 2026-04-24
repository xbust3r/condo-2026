"""
AccountsReceivable domain exceptions.
"""
from library.dddpy.shared.mysql.base import DomainException


class ARNotFound(DomainException):
    def __init__(self, message: str = "Accounts receivable entry not found"):
        self.message = message
        super().__init__(self.message)


class InvalidARStatusTransition(DomainException):
    def __init__(self, message: str = "Invalid AR status transition"):
        self.message = message
        super().__init__(self.message)


class ARPaymentExceedsBalance(DomainException):
    def __init__(self, message: str = "Payment amount exceeds pending balance"):
        self.message = message
        super().__init__(self.message)
