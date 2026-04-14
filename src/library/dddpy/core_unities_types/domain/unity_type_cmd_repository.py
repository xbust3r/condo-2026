from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_unities_types.domain.unity_type_data import (
    CreateUnityTypeData,
    UpdateUnityTypeData,
)
from library.dddpy.core_unities_types.domain.unity_type_entity import UnityTypeEntity


class UnityTypeCmdRepository(ABC):
    """Command repository: write operations for unity types."""

    @abstractmethod
    def create(self, data: CreateUnityTypeData) -> UnityTypeEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateUnityTypeData) -> Optional[UnityTypeEntity]:
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
