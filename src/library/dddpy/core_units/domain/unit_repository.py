from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_units.domain.unit_entity import UnitEntity
from library.dddpy.core_units.domain.unit_data import CreateUnitData, UpdateUnitData


class UnitRepository(ABC):
    """Contrato abstracto para persistencia de unidades."""

    @abstractmethod
    def create(self, data: CreateUnitData) -> UnitEntity:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UnitEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[UnitEntity]:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateUnitData) -> Optional[UnitEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def list_by_building(self, building_id: int) -> List[UnitEntity]:
        pass