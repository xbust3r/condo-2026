from library.dddpy.core_buildings_types.domain.building_type_cmd_repository import (
    BuildingTypeCmdRepository,
)
from library.dddpy.core_buildings_types.domain.building_type_data import (
    CreateBuildingTypeData,
    UpdateBuildingTypeData,
)
from library.dddpy.core_buildings_types.domain.building_type_query_repository import (
    BuildingTypeQueryRepository,
)
from library.dddpy.core_buildings_types.domain.building_type_exception import (
    DuplicateBuildingTypeCode,
    BuildingTypeIsSystem,
    BuildingTypeIsInUse,
)
from library.dddpy.core_buildings_types.domain.building_type_entity import (
    BuildingTypeEntity,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BuildingTypeCmdUseCase")


class BuildingTypeCmdUseCase:
    """Use case for write operations on building types."""

    def __init__(self, cmd_repo: BuildingTypeCmdRepository, query_repo: BuildingTypeQueryRepository):
        self._cmd = cmd_repo
        self._query = query_repo
        logger.info("BuildingTypeCmdUseCase initialized")

    def create(self, data: CreateBuildingTypeData) -> BuildingTypeEntity:
        logger.add_inside_method("create")

        # Check for duplicate in the same scope (active only)
        existing = self._query.get_by_code_in_scope(data.condominium_id, data.code)
        if existing:
            scope = "global" if data.condominium_id is None else f"condominium {data.condominium_id}"
            logger.warning(f"Duplicate code={data.code} in scope={scope}")
            raise DuplicateBuildingTypeCode(code=data.code, scope=scope)

        return self._cmd.create(data)

    def update(self, id: int, data: UpdateBuildingTypeData) -> None:
        logger.add_inside_method("update")

        # Verify type exists and is active
        existing = self._query.get_by_id(id)
        if not existing:
            from library.dddpy.core_buildings_types.domain.building_type_exception import (
                BuildingTypeNotFound,
            )
            raise BuildingTypeNotFound()

        return self._cmd.update(id, data)

    def soft_delete(self, id: int) -> bool:
        logger.add_inside_method("soft_delete")
        return self._cmd.soft_delete(id)

    def restore(self, id: int) -> bool:
        logger.add_inside_method("restore")
        return self._cmd.restore(id)

    def hard_delete(self, id: int) -> bool:
        logger.add_inside_method("hard_delete")

        # Verify it exists
        existing = self._query.get_by_id(id)
        if not existing:
            from library.dddpy.core_buildings_types.domain.building_type_exception import (
                BuildingTypeNotFound,
            )
            raise BuildingTypeNotFound()

        # Check references
        ref_count = self._query.count_references(id)
        if ref_count > 0:
            logger.warning(f"Building type id={id} has {ref_count} building references")
            raise BuildingTypeIsInUse(id)

        return self._cmd.hard_delete(id)
