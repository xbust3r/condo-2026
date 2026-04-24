"""
ChargeType domain exceptions.
"""
from library.dddpy.shared.mysql.base import DomainException


class ChargeTypeNotFound(DomainException):
    """Raised when a charge type is not found."""
    def __init__(self, message: str = "Charge type not found"):
        self.message = message
        super().__init__(self.message)


class ChargeTypeAlreadyExists(DomainException):
    """Raised when trying to create a charge type with a code that already exists."""
    def __init__(self, message: str = "Charge type with this code already exists"):
        self.message = message
        super().__init__(self.message)
