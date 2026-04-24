from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_buildings_types.domain.building_type_entity import BuildingTypeEntity


class BuildingTypeRepository(ABC):
    """Repository interface for building type operations."""

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[BuildingTypeEntity]:
        pass

    @abstractmethod
    def find_by_uuid(self, uuid: str) -> Optional[BuildingTypeEntity]:
        pass
