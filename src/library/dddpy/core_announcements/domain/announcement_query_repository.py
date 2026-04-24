"""
Announcement query repository interface — DDD domain layer.
"""
from typing import Optional, List, Tuple


class AnnouncementQueryRepository:
    """Interface for querying announcements."""

    def get_by_id(self, id: int) -> Optional[object]:
        pass

    def get_by_uuid(self, uuid: str) -> Optional[object]:
        pass

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        category: Optional[str] = None,
        visibility: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[object], int]:
        pass

    def list_active(
        self,
        condominium_id: int,
        as_of_date=None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[object], int]:
        pass
