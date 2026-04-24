from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_buildings_types.domain.building_type_entity import BuildingTypeEntity
from library.dddpy.core_buildings_types.domain.building_type_data import (
    CreateBuildingTypeData,
    UpdateBuildingTypeData,
)


class BuildingTypeCmdRepository(ABC):
    """Command repository: write operations for building types."""

    @abstractmethod
    def create(self, data: CreateBuildingTypeData) -> BuildingTypeEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateBuildingTypeData) -> Optional[BuildingTypeEntity]:
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        """Sets deleted_at timestamp. Blocked for system types."""

    @abstractmethod
    def restore(self, id: int) -> bool:
        """Clears deleted_at timestamp."""

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        """Physical deletion. Blocked if referenced by buildings or if is_system."""
