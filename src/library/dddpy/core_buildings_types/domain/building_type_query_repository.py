from typing import Optional
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from library.dddpy.core_buildings_types.domain.building_type_entity import BuildingTypeEntity


class BuildingTypeQueryRepository(ABC):
    """Query repository: read operations for building types."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[BuildingTypeEntity]:
        """Get active (non-deleted) building type by id."""

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[BuildingTypeEntity]:
        """Get active (non-deleted) building type by uuid."""

    @abstractmethod
    def get_by_code_in_scope(
        self,
        condominium_id: Optional[int],
        code: str,
    ) -> Optional[BuildingTypeEntity]:
        """Get active type by code within a scope (global if condominium_id is None)."""

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        include_system: bool = True,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[BuildingTypeEntity], int]:
        """
        List building types.
        - condominium_id=None + include_system=True  → all global + system types
        - condominium_id=[id]                        → global types + custom for that condo
        - include_system=False                      → exclude global system types
        - include_deleted=True                      → include soft-deleted
        """

    @abstractmethod
    def count_references(self, type_id: int) -> int:
        """Count how many buildings reference this type."""

    @abstractmethod
    def get_active_in_scope(
        self,
        type_id: int,
        condominium_id: int,
    ) -> Optional[BuildingTypeEntity]:
        """
        Get a building type if it's active and accessible in the given scope.
        Returns None if not found, deleted, inactive, or from another condominium.
        """
