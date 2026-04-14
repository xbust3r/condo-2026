from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_unitys.domain.unity_entity import UnityEntity


class UnityQueryRepository(ABC):
    """Interfaz de lectura para consultas de unidades."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UnityEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[UnityEntity]:
        pass

    @abstractmethod
    def get_by_unit_number_in_building(
        self, building_id: int, unit_number: str
    ) -> Optional[UnityEntity]:
        """Get unity by unit_number within a specific building."""
        pass

    @abstractmethod
    def get_by_code_in_building(
        self, building_id: int, code: str
    ) -> Optional[UnityEntity]:
        """Get unity by code within a specific building."""
        pass

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        building_id: Optional[int] = None,
        unity_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[UnityEntity], int]:
        """List unities with optional filters.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return (max 500)
            building_id: Filter by building
            unity_type_id: Filter by unity type
            occupancy_status: Filter by occupancy status
            status: Filter by status (1=active, 0=inactive)
            include_deleted: If True, include soft-deleted records
        """
        pass

    @abstractmethod
    def list_by_building(
        self,
        building_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[UnityEntity], int]:
        """List unities for a specific building."""
        pass

    @abstractmethod
    def count_active_residents(self, unity_id: int) -> int:
        """Count active residents for a unity. Used before hard delete."""
        pass
