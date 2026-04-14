from typing import Optional, List

from library.dddpy.core_unitys.domain.unity_query_repository import UnityQueryRepository
from library.dddpy.core_unitys.domain.unity_entity import UnityEntity
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnityQueryUseCase")


class UnityQueryUseCase:

    def __init__(self, repository: UnityQueryRepository):
        self.repository = repository
        logger.info("UnityQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[UnityEntity]:
        logger.debug(f"Querying unity by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[UnityEntity]:
        logger.debug(f"Querying unity by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def get_by_unit_number_in_building(
        self, building_id: int, unit_number: str
    ) -> Optional[UnityEntity]:
        return self.repository.get_by_unit_number_in_building(building_id, unit_number)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        building_id: Optional[int] = None,
        unity_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[UnityEntity], int]:
        logger.debug(f"Listing unities skip={skip} limit={limit}")
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            building_id=building_id,
            unity_type_id=unity_type_id,
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
    ) -> tuple[List[UnityEntity], int]:
        logger.debug(f"Listing unities for building_id={building_id}")
        return self.repository.list_by_building(
            building_id=building_id,
            skip=skip,
            limit=limit,
            occupancy_status=occupancy_status,
            status=status,
            include_deleted=include_deleted,
        )

    def count_active_residents(self, unity_id: int) -> int:
        logger.debug(f"Counting active residents for unity_id={unity_id}")
        return self.repository.count_active_residents(unity_id)
