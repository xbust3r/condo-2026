from chalicelib.dddpy.core_buildings_types.usecase.buildings_types_cmd_usecase import BuildingsTypesCmdUseCase
from chalicelib.dddpy.core_buildings_types.usecase.buildings_types_query_usecase import BuildingsTypesQueryUseCase
from chalicelib.dddpy.core_buildings_types.infrastructure.buildings_types_cmd_repository import BuildingsTypesCmdRepositoryImpl
from chalicelib.dddpy.core_buildings_types.infrastructure.buildings_types_query_repository import BuildingsTypesQueryRepositoryImpl


def buildings_types_cmd_usecase_factory() -> BuildingsTypesCmdUseCase:
    repository = BuildingsTypesCmdRepositoryImpl()
    return BuildingsTypesCmdUseCase(repository)


def buildings_types_query_usecase_factory() -> BuildingsTypesQueryUseCase:
    repository = BuildingsTypesQueryRepositoryImpl()
    return BuildingsTypesQueryUseCase(repository)
