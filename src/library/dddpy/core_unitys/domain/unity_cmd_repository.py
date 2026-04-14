from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_unitys.domain.unity_entity import UnityEntity
from library.dddpy.core_unitys.domain.unity_data import CreateUnityData, UpdateUnityData


class UnityCmdRepository(ABC):
    """Interfaz de escritura para operaciones de modificación de unidades."""

    @abstractmethod
    def create(self, data: CreateUnityData) -> UnityEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateUnityData) -> Optional[UnityEntity]:
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        """Restore a soft-deleted unity: clears deleted_at."""
        pass

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        """Physical delete. Only allowed if unity has no active residents."""
        pass
