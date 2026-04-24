from typing import Optional
from typing import Optional, List, Tuple

from library.dddpy.core_unit_occupancies.domain.unit_occupancy_query_repository import UnitOccupancyQueryRepository
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_entity import UnitOccupancyEntity
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOccupancyQueryUseCase")


class UnitOccupancyQueryUseCase:

    def __init__(self, repository: UnitOccupancyQueryRepository):
        self.repository = repository
        logger.info("UnitOccupancyQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[UnitOccupancyEntity]:
        logger.debug(f"Querying unit occupancy by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[UnitOccupancyEntity]:
        logger.debug(f"Querying unit occupancy by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def get_active_by_unit_and_user(
        self, unit_id: int, user_id: int
    ) -> Optional[UnitOccupancyEntity]:
        logger.debug(
            f"Querying active occupancy by unit_id={unit_id}, user_id={user_id}"
        )
        return self.repository.get_active_by_unit_and_user(unit_id, user_id)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        unit_id: Optional[int] = None,
        user_id: Optional[int] = None,
        occupancy_type_id: Optional[int] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOccupancyEntity], int]:
        logger.debug(f"Listing unit occupancies skip={skip} limit={limit}")
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            unit_id=unit_id,
            user_id=user_id,
            occupancy_type_id=occupancy_type_id,
            status=status,
            is_primary=is_primary,
            include_deleted=include_deleted,
        )

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_type_id: Optional[int] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOccupancyEntity], int]:
        logger.debug(f"Listing occupancies for unit_id={unit_id}")
        return self.repository.list_by_unit(
            unit_id=unit_id,
            skip=skip,
            limit=limit,
            occupancy_type_id=occupancy_type_id,
            status=status,
            is_primary=is_primary,
            include_deleted=include_deleted,
        )

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_type_id: Optional[int] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[UnitOccupancyEntity], int]:
        logger.debug(f"Listing occupancies for user_id={user_id}")
        return self.repository.list_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            occupancy_type_id=occupancy_type_id,
            status=status,
            is_primary=is_primary,
            include_deleted=include_deleted,
        )

    def count_active_by_unit(self, unit_id: int) -> int:
        logger.debug(f"Counting active occupancies for unit_id={unit_id}")
        return self.repository.count_active_by_unit(unit_id)

    def _get_by_id_any_status(self, id: int) -> Optional[UnitOccupancyEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Delegating unit occupancy fetch by id={id} (any status)")
        return self.repository._get_by_id_any_status(id)
