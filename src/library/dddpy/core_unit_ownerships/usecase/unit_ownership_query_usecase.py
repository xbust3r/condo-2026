from typing import Optional, List, Tuple

from library.dddpy.core_unit_ownerships.domain.unit_ownership_query_repository import UnitOwnershipQueryRepository
from library.dddpy.core_unit_ownerships.domain.unit_ownership_entity import UnitOwnershipEntity
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOwnershipQueryUseCase")


class UnitOwnershipQueryUseCase:

    def __init__(self, repository: UnitOwnershipQueryRepository):
        self.repository = repository
        logger.info("UnitOwnershipQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[UnitOwnershipEntity]:
        logger.debug(f"Querying unit ownership by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[UnitOwnershipEntity]:
        logger.debug(f"Querying unit ownership by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def get_active_by_unit_and_user(
        self, unit_id: int, user_id: int
    ) -> Optional[UnitOwnershipEntity]:
        logger.debug(
            f"Querying active unit ownership by unit_id={unit_id}, user_id={user_id}"
        )
        return self.repository.get_active_by_unit_and_user(unit_id, user_id)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        unit_id: Optional[int] = None,
        user_id: Optional[int] = None,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOwnershipEntity], int]:
        logger.debug(f"Listing unit ownerships skip={skip} limit={limit}")
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            unit_id=unit_id,
            user_id=user_id,
            ownership_type=ownership_type,
            status=status,
            include_deleted=include_deleted,
        )

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOwnershipEntity], int]:
        logger.debug(f"Listing unit ownerships for unit_id={unit_id}")
        return self.repository.list_by_unit(
            unit_id=unit_id,
            skip=skip,
            limit=limit,
            ownership_type=ownership_type,
            status=status,
            include_deleted=include_deleted,
        )

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOwnershipEntity], int]:
        logger.debug(f"Listing unit ownerships for user_id={user_id}")
        return self.repository.list_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            ownership_type=ownership_type,
            status=status,
            include_deleted=include_deleted,
        )

    def _get_by_id_any_status(self, id: int) -> Optional[UnitOwnershipEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Delegating unit ownership fetch by id={id} (any status)")
        return self.repository._get_by_id_any_status(id)
