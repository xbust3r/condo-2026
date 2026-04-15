from typing import Optional, List

from library.dddpy.core_units.domain.unit_query_repository import UnitQueryRepository
from library.dddpy.core_units.domain.unit_entity import UnitEntity
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitQueryUseCase")


class UnitQueryUseCase:

    def __init__(self, repository: UnitQueryRepository):
        self.repository = repository
        logger.info("UnitQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[UnitEntity]:
        logger.debug(f"Querying unit by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[UnitEntity]:
        logger.debug(f"Querying unit by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def get_by_unit_number_in_building(
        self, building_id: int, unit_number: str
    ) -> Optional[UnitEntity]:
        return self.repository.get_by_unit_number_in_building(building_id, unit_number)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        building_id: Optional[int] = None,
        unit_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[UnitEntity], int]:
        logger.debug(f"Listing units skip={skip} limit={limit}")
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            building_id=building_id,
            unit_type_id=unit_type_id,
            occupancy_status=occupancy_status,
            status=status,
            include_deleted=include_deleted,
        )

    def list_by_building(
        self,
        building_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[UnitEntity], int]:
        logger.debug(f"Listing units for building_id={building_id}")
        return self.repository.list_by_building(
            building_id=building_id,
            skip=skip,
            limit=limit,
            occupancy_status=occupancy_status,
            status=status,
            include_deleted=include_deleted,
        )

    def count_active_residents(self, unit_id: int) -> int:
        logger.debug(f"Counting active residents for unit_id={unit_id}")
        return self.repository.count_active_residents(unit_id)

    def _get_by_id_any_status(self, id: int) -> Optional[UnitEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Delegating unit fetch by id={id} (any status)")
        return self.repository._get_by_id_any_status(id)