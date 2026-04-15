from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from library.dddpy.core_unit_ownerships.domain.unit_ownership_entity import UnitOwnershipEntity


class UnitOwnershipQueryRepository(ABC):
    """Interfaz de lectura para consultas de unit ownerships."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UnitOwnershipEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[UnitOwnershipEntity]:
        pass

    @abstractmethod
    def get_active_by_unit_and_user(
        self, unit_id: int, user_id: int
    ) -> Optional[UnitOwnershipEntity]:
        """Get active ownership record for a unit-user pair."""
        pass

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        unit_id: Optional[int] = None,
        user_id: Optional[int] = None,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOwnershipEntity], int]:
        """List unit ownerships with optional filters.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return (max 500)
            unit_id: Filter by unit
            user_id: Filter by user
            ownership_type: Filter by ownership type (owner/co_owner)
            status: Filter by status (active/inactive/historical)
            include_deleted: If True, include soft-deleted records
        """
        pass

    @abstractmethod
    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOwnershipEntity], int]:
        """List ownerships for a specific unit."""
        pass

    @abstractmethod
    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOwnershipEntity], int]:
        """List ownerships for a specific user."""
        pass

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[UnitOwnershipEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        pass
