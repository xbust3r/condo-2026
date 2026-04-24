"""
Charge domain exceptions.
"""
from library.dddpy.shared.mysql.base import DomainException


class ChargeNotFound(DomainException):
    def __init__(self, message: str = "Charge not found"):
        self.message = message
        super().__init__(self.message)


class ChargeAlreadyExists(DomainException):
    def __init__(self, message: str = "Charge already exists"):
        self.message = message
        super().__init__(self.message)


class InvalidChargeStatus(DomainException):
    def __init__(self, message: str = "Invalid charge status transition"):
        self.message = message
        super().__init__(self.message)


class ChargeAmountInvalid(DomainException):
    def __init__(self, message: str = "Charge amount must be greater than 0"):
        self.message = message
        super().__init__(self.message)
