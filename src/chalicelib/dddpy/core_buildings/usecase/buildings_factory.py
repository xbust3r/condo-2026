from chalicelib.dddpy.core_buildings.usecase.buildings_cmd_usecase import BuildingsCmdUseCase
from chalicelib.dddpy.core_buildings.usecase.buildings_query_usecase import BuildingsQueryUseCase
from chalicelib.dddpy.core_buildings.infrastructure.buildings_cmd_repository import BuildingsCmdRepositoryImpl
from chalicelib.dddpy.core_buildings.infrastructure.buildings_query_repository import BuildingsQueryRepositoryImpl


def buildings_cmd_usecase_factory() -> BuildingsCmdUseCase:
    repository = BuildingsCmdRepositoryImpl()
    return BuildingsCmdUseCase(repository)


def buildings_query_usecase_factory() -> BuildingsQueryUseCase:
    repository = BuildingsQueryRepositoryImpl()
    return BuildingsQueryUseCase(repository)
