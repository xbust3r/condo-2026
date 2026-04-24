from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_unit_occupancies.domain.unit_occupancy_entity import UnitOccupancyEntity
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_data import CreateUnitOccupancyData, UpdateUnitOccupancyData


class UnitOccupancyRepository(ABC):
    """Contrato abstracto para persistencia de unit occupancies."""

    @abstractmethod
    def create(self, data: CreateUnitOccupancyData) -> UnitOccupancyEntity:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UnitOccupancyEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[UnitOccupancyEntity]:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateUnitOccupancyData) -> Optional[UnitOccupancyEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def list_by_unit(self, unit_id: int) -> List[UnitOccupancyEntity]:
        pass

    @abstractmethod
    def list_by_user(self, user_id: int) -> List[UnitOccupancyEntity]:
        pass
