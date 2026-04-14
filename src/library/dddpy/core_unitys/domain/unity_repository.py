from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_unitys.domain.unity_entity import UnityEntity
from library.dddpy.core_unitys.domain.unity_data import CreateUnityData, UpdateUnityData


class UnityRepository(ABC):
    """Contrato abstracto para persistencia de unidades."""

    @abstractmethod
    def create(self, data: CreateUnityData) -> UnityEntity:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UnityEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[UnityEntity]:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateUnityData) -> Optional[UnityEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def list_by_building(self, building_id: int) -> List[UnityEntity]:
        pass
