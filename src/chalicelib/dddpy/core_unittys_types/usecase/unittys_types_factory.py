from chalicelib.dddpy.core_unittys_types.usecase.unittys_types_cmd_usecase import UnitysTypesCmdUseCase
from chalicelib.dddpy.core_unittys_types.usecase.unittys_types_query_usecase import UnitysTypesQueryUseCase
from chalicelib.dddpy.core_unittys_types.infrastructure.unittys_types_cmd_repository import UnitysTypesCmdRepositoryImpl
from chalicelib.dddpy.core_unittys_types.infrastructure.unittys_types_query_repository import UnitysTypesQueryRepositoryImpl


def unittys_types_cmd_usecase_factory() -> UnitysTypesCmdUseCase:
    repository = UnitysTypesCmdRepositoryImpl()
    return UnitysTypesCmdUseCase(repository)


def unittys_types_query_usecase_factory() -> UnitysTypesQueryUseCase:
    repository = UnitysTypesQueryRepositoryImpl()
    return UnitysTypesQueryUseCase(repository)
