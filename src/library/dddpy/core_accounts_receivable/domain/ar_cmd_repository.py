"""
AccountsReceivable command repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_accounts_receivable.domain.ar_data import (
    CreateARData,
    UpdateARData,
)
from library.dddpy.core_accounts_receivable.domain.ar_entity import AREntity


class ARCmdRepository(ABC):
    """Abstract write repository for accounts receivable."""

    @abstractmethod
    def create(self, data: CreateARData) -> AREntity:
        pass

    @abstractmethod
    def create_batch(self, entries: list[CreateARData]) -> list[AREntity]:
        """Create multiple AR entries at once (for global charges → N units)."""
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateARData) -> Optional[AREntity]:
        pass

    @abstractmethod
    def update_status(self, id: int, status: str) -> Optional[AREntity]:
        """Update AR status with validation."""
        pass

    @abstractmethod
    def add_payment(self, id: int, amount: float) -> Optional[AREntity]:
        """Add a payment to the AR (increments paid_amount, updates status)."""
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        pass

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        pass
