from typing import Optional, Tuple, List

from library.dddpy.core_buildings_types.domain.building_type_query_repository import (
    BuildingTypeQueryRepository,
)
from library.dddpy.core_buildings_types.domain.building_type_entity import BuildingTypeEntity
from library.dddpy.core_buildings_types.domain.building_type_exception import (
    BuildingTypeNotFound,
    BuildingTypeIsInactive,
    BuildingTypeIsDeleted,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BuildingTypeQueryUseCase")


class BuildingTypeQueryUseCase:
    """Use case for read operations on building types."""

    def __init__(self, query_repo: BuildingTypeQueryRepository):
        self._query = query_repo
        logger.info("BuildingTypeQueryUseCase initialized")

    def get_by_id(self, id: int) -> BuildingTypeEntity:
        logger.add_inside_method("get_by_id")
        entity = self._query.get_by_id(id)
        if not entity:
            raise BuildingTypeNotFound()
        return entity

    def get_by_uuid(self, uuid: str) -> BuildingTypeEntity:
        logger.add_inside_method("get_by_uuid")
        entity = self._query.get_by_uuid(uuid)
        if not entity:
            raise BuildingTypeNotFound()
        return entity

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        include_system: bool = True,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[BuildingTypeEntity], int]:
        logger.add_inside_method("list_all")
        return self._query.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            include_system=include_system,
            status=status,
            include_deleted=include_deleted,
        )

    def get_active_for_building_assignment(
        self,
        type_id: int,
        condominium_id: int,
    ) -> BuildingTypeEntity:
        """
        Validate a building_type_id for assignment to a building.

        Rules:
        - Type must exist and not be soft-deleted
        - Type must be active (status=1)
        - Type must be global (condominium_id IS NULL) OR belong to the same condominium
        """
        logger.add_inside_method("get_active_for_building_assignment")

        entity = self._query.get_active_in_scope(type_id, condominium_id)
        if not entity:
            # Distinguish not-found from not-accessible for better error messages
            exists = self._query.get_by_id(type_id)
            if not exists:
                raise BuildingTypeNotFound()
            if exists.is_deleted():
                raise BuildingTypeIsDeleted()
            if exists.status != 1:
                raise BuildingTypeIsInactive()
            from library.dddpy.core_buildings_types.domain.building_type_exception import (
                BuildingTypeNotAccessible,
            )
            raise BuildingTypeNotAccessible()

        return entity

    def get_by_id_any_status(self, id: int) -> Optional[BuildingTypeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Delegating building type fetch by id={id} (any status)")
        return self._query._get_by_id_any_status(id)
