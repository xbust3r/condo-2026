"""
from typing import Optional
Payment query repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from library.dddpy.core_payments.domain.payment_entity import PaymentEntity


class PaymentQueryRepository(ABC):
    """Abstract read repository for payments."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[PaymentEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[PaymentEntity]:
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
    ) -> Tuple[List[PaymentEntity], int]:
        pass
