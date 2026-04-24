"""
Ledger command repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_ledger_entries.domain.ledger_data import CreateLedgerEntryData
from library.dddpy.core_ledger_entries.domain.ledger_entity import LedgerEntryEntity


class LedgerCmdRepository(ABC):
    """Abstract write repository for ledger entries (append-only)."""

    @abstractmethod
    def create(self, data: CreateLedgerEntryData) -> LedgerEntryEntity:
        """Append a new ledger entry. Never updates or deletes."""
        pass

    @abstractmethod
    def create_batch(self, entries: list[CreateLedgerEntryData]) -> list[LedgerEntryEntity]:
        """Create multiple ledger entries at once."""
        pass

    @abstractmethod
    def get_latest_balance(self, unit_id: int) -> float:
        """Get the latest balance for a unit (last ledger entry balance)."""
        pass
