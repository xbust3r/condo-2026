from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_buildings.domain.building_entity import BuildingEntity


class BuildingQueryRepository(ABC):
    """Interfaz de lectura para consultas de edificios."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[BuildingEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[BuildingEntity]:
        pass

    @abstractmethod
    def get_by_code_in_condominium(self, condominium_id: int, code: str) -> Optional[BuildingEntity]:
        """Get building by code within a specific condominium."""
        pass

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        building_type_id: Optional[int] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[BuildingEntity], int]:
        """List buildings with optional filters.
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return (max 500)
            condominium_id: Filter by condominium
            building_type_id: Filter by building type
            status: Filter by status (1=active, 0=inactive)
            include_deleted: If True, include soft-deleted records
        """
        pass

    @abstractmethod
    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[BuildingEntity], int]:
        """List buildings for a specific condominium."""
        pass

    @abstractmethod
    def count_active_units(self, building_id: int) -> int:
        """Count active units for a building. Used before hard delete."""
        pass

    @abstractmethod
    def get_building_ids_by_condominiums(
        self,
        condominium_ids: List[int],
    ) -> List[int]:
        """Get all building IDs belonging to given condominium_ids."""
        pass