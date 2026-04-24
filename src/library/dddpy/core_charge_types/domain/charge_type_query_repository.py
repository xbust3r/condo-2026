"""
ChargeType query repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from library.dddpy.core_charge_types.domain.charge_type_entity import ChargeTypeEntity


class ChargeTypeQueryRepository(ABC):
    """Abstract read repository for charge types."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[ChargeTypeEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[ChargeTypeEntity]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[ChargeTypeEntity]:
        pass

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ChargeTypeEntity], int]:
        pass

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[ChargeTypeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        pass
