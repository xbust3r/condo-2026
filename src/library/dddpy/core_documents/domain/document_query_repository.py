"""
from typing import Optional
Document query repository interface.
"""
from typing import Optional, List, Tuple


class DocumentQueryRepository:
    def get_by_id(self, id: int) -> Optional[object]: pass
    def get_by_uuid(self, uuid: str) -> Optional[object]: pass
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        category: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[object], int]: pass
