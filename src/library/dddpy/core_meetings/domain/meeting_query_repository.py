"""
from typing import Optional
Meeting query repository interface — DDD domain layer.
"""
from datetime import date, datetime
from typing import Optional, List, Tuple


class MeetingQueryRepository:
    """Interface for querying meetings."""

    def get_by_id(self, id: int) -> Optional[object]:
        pass

    def get_by_uuid(self, uuid: str) -> Optional[object]:
        pass

    def list_all(
        self,
        condominium_id: Optional[int] = None,
        status: Optional[str] = None,
        meeting_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> Tuple[List[object], int]:
        pass

    def list_upcoming(
        self,
        condominium_id: int,
        as_of_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[object], int]:
        pass
