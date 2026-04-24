from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_units.domain.unit_entity import UnitEntity
from library.dddpy.core_units.domain.unit_data import CreateUnitData, UpdateUnitData


class UnitCmdRepository(ABC):
    """Interfaz de escritura para operaciones de modificación de unidades."""

    @abstractmethod
    def create(self, data: CreateUnitData) -> UnitEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateUnitData) -> Optional[UnitEntity]:
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        """Restore a soft-deleted unit: clears deleted_at."""
        pass

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        """Physical delete. Only allowed if unit has no active residents."""
        pass