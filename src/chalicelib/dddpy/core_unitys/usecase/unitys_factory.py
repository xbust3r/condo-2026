from chalicelib.dddpy.core_unitys.usecase.unitys_cmd_usecase import UnitysCmdUseCase
from chalicelib.dddpy.core_unitys.usecase.unitys_query_usecase import UnitysQueryUseCase
from chalicelib.dddpy.core_unitys.infrastructure.unitys_cmd_repository import UnitysCmdRepositoryImpl
from chalicelib.dddpy.core_unitys.infrastructure.unitys_query_repository import UnitysQueryRepositoryImpl


def unitys_cmd_usecase_factory() -> UnitysCmdUseCase:
    repository = UnitysCmdRepositoryImpl()
    return UnitysCmdUseCase(repository)


def unitys_query_usecase_factory() -> UnitysQueryUseCase:
    repository = UnitysQueryRepositoryImpl()
    return UnitysQueryUseCase(repository)
