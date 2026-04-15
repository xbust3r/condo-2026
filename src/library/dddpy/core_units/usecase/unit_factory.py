from library.dddpy.core_units.infrastructure.unit_cmd_repository import UnitCmdRepositoryImpl
from library.dddpy.core_units.infrastructure.unit_query_repository import UnitQueryRepositoryImpl
from library.dddpy.core_units.usecase.unit_cmd_usecase import UnitCmdUseCase
from library.dddpy.core_units.usecase.unit_query_usecase import UnitQueryUseCase


def unit_cmd_usecase_factory() -> UnitCmdUseCase:
    return UnitCmdUseCase(repository=UnitCmdRepositoryImpl())


def unit_query_usecase_factory() -> UnitQueryUseCase:
    return UnitQueryUseCase(repository=UnitQueryRepositoryImpl())