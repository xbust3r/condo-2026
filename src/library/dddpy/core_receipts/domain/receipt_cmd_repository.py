"""
Receipt command repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_receipts.domain.receipt_data import CreateReceiptData
from library.dddpy.core_receipts.domain.receipt_entity import ReceiptEntity


class ReceiptCmdRepository(ABC):
    """Abstract write repository for receipts."""

    @abstractmethod
    def create(self, data: CreateReceiptData) -> ReceiptEntity:
        pass

    @abstractmethod
    def get_next_receipt_number(self, condominium_id: int) -> str:
        """Generate next receipt number: C{condo_code}-{YYYY}{MM}-{correlativo:06d}."""
        pass
