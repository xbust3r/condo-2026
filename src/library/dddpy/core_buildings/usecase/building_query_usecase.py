from typing import Optional, List

from library.dddpy.core_buildings.domain.building_query_repository import BuildingQueryRepository
from library.dddpy.core_buildings.domain.building_entity import BuildingEntity
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BuildingQueryUseCase")


class BuildingQueryUseCase:

    def __init__(self, repository: BuildingQueryRepository):
        self.repository = repository
        logger.info("BuildingQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[BuildingEntity]:
        logger.info(f"Delegating building fetch by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[BuildingEntity]:
        logger.info(f"Delegating building fetch by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

    def get_by_code_in_condominium(self, condominium_id: int, code: str) -> Optional[BuildingEntity]:
        logger.info(f"Delegating building fetch by code={code} in condominium_id={condominium_id}")
        return self.repository.get_by_code_in_condominium(condominium_id, code)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        building_type_id: Optional[int] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[BuildingEntity], int]:
        logger.info(
            f"Delegating building list_all (skip={skip}, limit={limit}, "
            f"condominium_id={condominium_id}, building_type_id={building_type_id}, "
            f"status={status}, include_deleted={include_deleted})"
        )
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            building_type_id=building_type_id,
            status=status,
            include_deleted=include_deleted,
        )

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> tuple[List[BuildingEntity], int]:
        logger.info(f"Delegating building list_by_condominium for condominium_id={condominium_id}")
        return self.repository.list_by_condominium(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )

    def count_active_units(self, building_id: int) -> int:
        logger.info(f"Delegating count_active_units for building_id={building_id}")
        return self.repository.count_active_units(building_id)

    def get_by_id_any_status(self, id: int) -> Optional[BuildingEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Delegating building fetch by id={id} (any status)")
        return self.repository._get_by_id_any_status(id)