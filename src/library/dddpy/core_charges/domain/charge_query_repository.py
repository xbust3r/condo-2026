"""
from typing import Optional
Charge query repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from library.dddpy.core_charges.domain.charge_entity import ChargeEntity


class ChargeQueryRepository(ABC):
    """Abstract read repository for charges."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[ChargeEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[ChargeEntity]:
        pass

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        charge_type_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        status: Optional[str] = None,
        is_recurrent: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ChargeEntity], int]:
        pass

    @abstractmethod
    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        is_recurrent: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ChargeEntity], int]:
        pass

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[ChargeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        pass
