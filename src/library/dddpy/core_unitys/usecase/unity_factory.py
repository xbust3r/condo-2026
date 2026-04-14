from library.dddpy.core_unitys.infrastructure.unity_cmd_repository import UnityCmdRepositoryImpl
from library.dddpy.core_unitys.infrastructure.unity_query_repository import UnityQueryRepositoryImpl
from library.dddpy.core_unitys.usecase.unity_cmd_usecase import UnityCmdUseCase
from library.dddpy.core_unitys.usecase.unity_query_usecase import UnityQueryUseCase


def unity_cmd_usecase_factory() -> UnityCmdUseCase:
    return UnityCmdUseCase(repository=UnityCmdRepositoryImpl())


def unity_query_usecase_factory() -> UnityQueryUseCase:
    return UnityQueryUseCase(repository=UnityQueryRepositoryImpl())
