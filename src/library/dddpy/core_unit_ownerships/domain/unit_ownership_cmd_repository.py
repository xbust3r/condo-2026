from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional, List

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

    @abstractmethod
    def find_active_by_unit(self, unit_id: int) -> List[UnitOwnershipEntity]:
        """Find all active (non-deleted, non-historical) ownerships for a unit."""
        pass

    @abstractmethod
    def get_by_id_any_status(self, id: int) -> Optional[UnitOwnershipEntity]:
        """Get ownership record by id ignoring deleted_at filter. For use in mutations."""
        pass

    @abstractmethod
    def soft_delete_by_user(self, user_id: int) -> int:
        """Mark all active ownerships for a user as historical (cascade on user soft-delete). Returns count."""
        pass