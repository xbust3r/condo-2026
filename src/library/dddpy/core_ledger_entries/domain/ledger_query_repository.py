"""
Ledger query repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from library.dddpy.core_ledger_entries.domain.ledger_entity import LedgerEntryEntity


class LedgerQueryRepository(ABC):
    """Abstract read repository for ledger entries."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[LedgerEntryEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[LedgerEntryEntity]:
        pass

    @abstractmethod
    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        period: Optional[str] = None,
    ) -> Tuple[List[LedgerEntryEntity], int]:
        """Get full ledger for a unit with computed running balance."""
        pass

    @abstractmethod
    def get_balance_summary(self, unit_id: int) -> dict:
        """Get total debt, total paid, and current balance for a unit."""
        pass
