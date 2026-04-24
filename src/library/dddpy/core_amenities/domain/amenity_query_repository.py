"""
from typing import Optional
Amenity query repository interface — DDD domain layer.
"""
from typing import Optional, List, Tuple


class AmenityQueryRepository:
    """Interface for querying amenities."""

    def get_by_id(self, id: int) -> Optional[object]:
        pass

    def get_by_uuid(self, uuid: str) -> Optional[object]:
        pass

    def list_all(
        self,
        condominium_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> Tuple[List[object], int]:
        pass

    def list_active(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[object], int]:
        pass
