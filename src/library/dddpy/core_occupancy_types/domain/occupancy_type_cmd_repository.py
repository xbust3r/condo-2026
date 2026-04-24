"""
OccupancyType command repository — interface.
"""
from abc import ABC, abstractmethod
from library.dddpy.core_occupancy_types.domain.occupancy_type_data import (
    CreateOccupancyTypeData,
    UpdateOccupancyTypeData,
)
from library.dddpy.core_occupancy_types.domain.occupancy_type_entity import (
    OccupancyTypeEntity,
)


class OccupancyTypeCmdRepository(ABC):
    """Interface for write operations on occupancy types."""

    @abstractmethod
    def create(self, data: CreateOccupancyTypeData) -> OccupancyTypeEntity:
        ...

    @abstractmethod
    def update(self, id: int, data: UpdateOccupancyTypeData) -> OccupancyTypeEntity:
        ...

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        ...

    @abstractmethod
    def restore(self, id: int) -> bool:
        ...

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        ...