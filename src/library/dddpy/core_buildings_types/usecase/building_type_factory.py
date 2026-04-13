from library.dddpy.core_buildings_types.infrastructure.building_type_cmd_repository import (
    BuildingTypeCmdRepositoryImpl,
)
from library.dddpy.core_buildings_types.infrastructure.building_type_query_repository import (
    BuildingTypeQueryRepositoryImpl,
)
from library.dddpy.core_buildings_types.usecase.building_type_cmd_usecase import (
    BuildingTypeCmdUseCase,
)
from library.dddpy.core_buildings_types.usecase.building_type_query_usecase import (
    BuildingTypeQueryUseCase,
)


def building_type_cmd_usecase_factory() -> BuildingTypeCmdUseCase:
    cmd_repo = BuildingTypeCmdRepositoryImpl()
    query_repo = BuildingTypeQueryRepositoryImpl()
    return BuildingTypeCmdUseCase(cmd_repo, query_repo)


def building_type_query_usecase_factory() -> BuildingTypeQueryUseCase:
    query_repo = BuildingTypeQueryRepositoryImpl()
    return BuildingTypeQueryUseCase(query_repo)
