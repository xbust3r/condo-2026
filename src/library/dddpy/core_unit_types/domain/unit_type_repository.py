from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_unit_types.domain.unit_type_entity import UnitTypeEntity


class UnitTypeRepository(ABC):
    """Repository interface for unit type operations."""

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[UnitTypeEntity]:
        pass

    @abstractmethod
    def find_by_uuid(self, uuid: str) -> Optional[UnitTypeEntity]:
        pass