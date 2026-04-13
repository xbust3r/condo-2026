from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_buildings.domain.building_entity import BuildingEntity
from library.dddpy.core_buildings.domain.building_data import CreateBuildingData, UpdateBuildingData


class BuildingCmdRepository(ABC):
    """Interfaz de escritura para operaciones de modificacion de edificios."""

    @abstractmethod
    def create(self, data: CreateBuildingData) -> BuildingEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateBuildingData) -> Optional[BuildingEntity]:
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        """Restore a soft-deleted building: clears deleted_at."""
        pass

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        """Physical delete. Only allowed if building has no active units."""
        pass