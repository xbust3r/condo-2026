from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_unit_ownerships.domain.unit_ownership_entity import UnitOwnershipEntity
from library.dddpy.core_unit_ownerships.domain.unit_ownership_data import CreateUnitOwnershipData, UpdateUnitOwnershipData


class UnitOwnershipCmdRepository(ABC):
    """Interfaz de escritura para operaciones de modificación de unit ownerships."""

    @abstractmethod
    def create(self, data: CreateUnitOwnershipData) -> UnitOwnershipEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateUnitOwnershipData) -> Optional[UnitOwnershipEntity]:
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        """Restore a soft-deleted record: clears deleted_at."""
        pass
