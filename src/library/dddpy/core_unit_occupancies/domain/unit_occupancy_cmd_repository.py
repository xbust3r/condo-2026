from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_unit_occupancies.domain.unit_occupancy_entity import UnitOccupancyEntity
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_data import CreateUnitOccupancyData, UpdateUnitOccupancyData


class UnitOccupancyCmdRepository(ABC):
    """Interfaz de escritura para operaciones de modificación de unit occupancies."""

    @abstractmethod
    def create(self, data: CreateUnitOccupancyData) -> UnitOccupancyEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateUnitOccupancyData) -> Optional[UnitOccupancyEntity]:
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        """Restore a soft-deleted record: clears deleted_at."""
        pass

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        """Physical delete."""
        pass

    @abstractmethod
    def find_primary_by_unit(self, unit_id: int) -> Optional[UnitOccupancyEntity]:
        """Find active primary occupancy for a unit."""
        pass

    @abstractmethod
    def get_unit_id(self, occupancy_id: int) -> Optional[int]:
        """Get unit_id for an existing occupancy record."""
        pass

    @abstractmethod
    def soft_delete_by_user(self, user_id: int) -> int:
        """Mark all active occupancies for a user as inactive (cascade on user soft-delete). Returns count."""
        pass
