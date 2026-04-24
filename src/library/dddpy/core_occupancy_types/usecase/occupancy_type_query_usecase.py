"""
from typing import Optional
OccupancyType query use case — handles read operations.
"""
from typing import List, Optional, Tuple
from library.dddpy.core_occupancy_types.domain.occupancy_type_entity import OccupancyTypeEntity
from library.dddpy.core_occupancy_types.domain.occupancy_type_query_repository import (
    OccupancyTypeQueryRepository,
)
from library.dddpy.core_occupancy_types.infrastructure.occupancy_type_query_repository import (
    OccupancyTypeQueryRepositoryImpl,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("OccupancyTypeQueryUseCase")


class OccupancyTypeQueryUseCase:
    def __init__(self):
        self._repository: OccupancyTypeQueryRepository = OccupancyTypeQueryRepositoryImpl()

    def get_by_id(self, id: int) -> Optional[OccupancyTypeEntity]:
        logger.info(f"OccupancyTypeQueryUseCase.get_by_id id={id}")
        return self._repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[OccupancyTypeEntity]:
        logger.info(f"OccupancyTypeQueryUseCase.get_by_uuid uuid={uuid}")
        return self._repository.get_by_uuid(uuid)

    def get_by_code(self, code: str) -> Optional[OccupancyTypeEntity]:
        logger.info(f"OccupancyTypeQueryUseCase.get_by_code code={code}")
        return self._repository.get_by_code(code)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[OccupancyTypeEntity], int]:
        logger.info(
            f"OccupancyTypeQueryUseCase.list_all skip={skip}, limit={limit}"
        )
        return self._repository.list_all(
            skip=skip,
            limit=limit,
            is_active=is_active,
            include_deleted=include_deleted,
        )

    def _get_by_id_any_status(self, id: int) -> Optional[OccupancyTypeEntity]:
        return self._repository._get_by_id_any_status(id)


_occupancy_type_query_instance: OccupancyTypeQueryUseCase | None = None


def occupancy_type_query_usecase_factory() -> OccupancyTypeQueryUseCase:
    global _occupancy_type_query_instance
    if _occupancy_type_query_instance is None:
        _occupancy_type_query_instance = OccupancyTypeQueryUseCase()
    return _occupancy_type_query_instance