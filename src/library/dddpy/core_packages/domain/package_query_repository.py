"""Package query repository interface."""
from typing import Optional, List, Tuple


class PackageQueryRepository:
    def get_by_id(self, id: int) -> Optional[object]: pass

    def get_by_uuid(self, uuid: str) -> Optional[object]: pass

    def list_all(
        self,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        recipient_user_id: Optional[int] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[object], int]: pass

    def list_pending(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[object], int]: pass

    def list_by_unit(
        self,
        unit_id: int,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[object], int]: pass
