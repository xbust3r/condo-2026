from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_units.domain.unit_entity import UnitEntity


class UnitQueryRepository(ABC):
    """Interfaz de lectura para consultas de unidades."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UnitEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[UnitEntity]:
        pass

    @abstractmethod
    def get_by_unit_number_in_building(
        self, building_id: int, unit_number: str
    ) -> Optional[UnitEntity]:
        """Get unit by unit_number within a specific building."""
        pass

    @abstractmethod
    def get_by_code_in_building(
        self, building_id: int, code: str
    ) -> Optional[UnitEntity]:
        """Get unit by code within a specific building."""
        pass

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        building_id: Optional[int] = None,
        unit_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[UnitEntity], int]:
        """List units with optional filters.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return (max 500)
            building_id: Filter by building
            unit_type_id: Filter by unit type
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
    ) -> tuple[List[UnitEntity], int]:
        """List units for a specific building."""
        pass

    @abstractmethod
    def count_active_residents(self, unit_id: int) -> int:
        """Count active residents for a unit. Used before hard delete."""
        pass