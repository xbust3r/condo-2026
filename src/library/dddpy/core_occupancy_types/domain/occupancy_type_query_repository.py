"""
OccupancyType query repository — interface.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from library.dddpy.core_occupancy_types.domain.occupancy_type_entity import (
    OccupancyTypeEntity,
)


class OccupancyTypeQueryRepository(ABC):
    """Interface for read operations on occupancy types."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[OccupancyTypeEntity]:
        ...

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[OccupancyTypeEntity]:
        ...

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[OccupancyTypeEntity]:
        ...

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[OccupancyTypeEntity], int]:
        ...

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[OccupancyTypeEntity]:
        ...