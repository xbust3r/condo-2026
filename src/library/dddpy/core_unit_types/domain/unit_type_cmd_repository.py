from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_unit_types.domain.unit_type_data import (
    CreateUnitTypeData,
    UpdateUnitTypeData,
)
from library.dddpy.core_unit_types.domain.unit_type_entity import UnitTypeEntity


class UnitTypeCmdRepository(ABC):
    """Command repository: write operations for unit types."""

    @abstractmethod
    def create(self, data: CreateUnitTypeData) -> UnitTypeEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateUnitTypeData) -> Optional[UnitTypeEntity]:
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