"""
Receipt query repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from library.dddpy.core_receipts.domain.receipt_entity import ReceiptEntity


class ReceiptQueryRepository(ABC):
    """Abstract read repository for receipts."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[ReceiptEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[ReceiptEntity]:
        pass

    @abstractmethod
    def get_by_receipt_number(self, receipt_number: str) -> Optional[ReceiptEntity]:
        pass

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        ar_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ReceiptEntity], int]:
        pass

    @abstractmethod
    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[ReceiptEntity], int]:
        pass
