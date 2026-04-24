from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from library.dddpy.core_unit_occupancies.domain.unit_occupancy_entity import UnitOccupancyEntity


class UnitOccupancyQueryRepository(ABC):
    """Interfaz de lectura para consultas de unit occupancies."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UnitOccupancyEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[UnitOccupancyEntity]:
        pass

    @abstractmethod
    def get_active_by_unit_and_user(
        self, unit_id: int, user_id: int
    ) -> Optional[UnitOccupancyEntity]:
        """Get active occupancy record for a unit-user pair."""
        pass

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        unit_id: Optional[int] = None,
        user_id: Optional[int] = None,
        occupancy_type_id: Optional[int] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOccupancyEntity], int]:
        """List unit occupancies with optional filters.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return (max 500)
            unit_id: Filter by unit
            user_id: Filter by user
            occupancy_type_id: Filter by occupancy type FK
            status: Filter by status (active/inactive/historical/pending)
            is_primary: Filter by is_primary flag
            include_deleted: If True, include soft-deleted records
        """
        pass

    @abstractmethod
    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_type_id: Optional[int] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOccupancyEntity], int]:
        """List occupancies for a specific unit."""
        pass

    @abstractmethod
    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_type_id: Optional[int] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOccupancyEntity], int]:
        """List occupancies for a specific user."""
        pass

    @abstractmethod
    def count_active_by_unit(self, unit_id: int) -> int:
        """Count active occupancy records for a unit."""
        pass

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[UnitOccupancyEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        pass
