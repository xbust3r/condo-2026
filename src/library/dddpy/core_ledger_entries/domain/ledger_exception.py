"""
Ledger domain exceptions.
"""
from library.dddpy.shared.mysql.base import DomainException


class LedgerEntryNotFound(DomainException):
    def __init__(self, message: str = "Ledger entry not found"):
        self.message = message
        super().__init__(self.message)
