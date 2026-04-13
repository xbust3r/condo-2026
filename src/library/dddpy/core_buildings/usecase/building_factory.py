from library.dddpy.core_buildings.infrastructure.building_cmd_repository import BuildingCmdRepositoryImpl
from library.dddpy.core_buildings.infrastructure.building_query_repository import BuildingQueryRepositoryImpl
from library.dddpy.core_buildings.usecase.building_cmd_usecase import BuildingCmdUseCase
from library.dddpy.core_buildings.usecase.building_query_usecase import BuildingQueryUseCase


def building_cmd_usecase_factory():
    repository = BuildingCmdRepositoryImpl()
    return BuildingCmdUseCase(repository)


def building_query_usecase_factory():
    repository = BuildingQueryRepositoryImpl()
    return BuildingQueryUseCase(repository)