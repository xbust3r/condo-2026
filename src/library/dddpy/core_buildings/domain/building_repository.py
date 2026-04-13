from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_buildings.domain.building_entity import BuildingEntity
from library.dddpy.core_buildings.domain.building_data import CreateBuildingData, UpdateBuildingData


class BuildingRepository(ABC):
    """Contrato abstracto para persistencia de edificios."""

    @abstractmethod
    def create(self, data: CreateBuildingData) -> BuildingEntity:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[BuildingEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[BuildingEntity]:
        pass

    @abstractmethod
    def get_by_code_in_condominium(self, condominium_id: int, code: str) -> Optional[BuildingEntity]:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateBuildingData) -> Optional[BuildingEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def list_by_condominium(self, condominium_id: int) -> List[BuildingEntity]:
        pass