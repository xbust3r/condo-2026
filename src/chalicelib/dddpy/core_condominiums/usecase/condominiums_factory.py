from chalicelib.dddpy.core_condominiums.usecase.condominiums_cmd_usecase import CondominiumsCmdUseCase
from chalicelib.dddpy.core_condominiums.usecase.condominiums_query_usecase import CondominiumsQueryUseCase
from chalicelib.dddpy.core_condominiums.infrastructure.condominiums_cmd_repository import CondominiumsCmdRepositoryImpl
from chalicelib.dddpy.core_condominiums.infrastructure.condominiums_query_repository import CondominiumsQueryRepositoryImpl


def condominiums_cmd_usecase_factory() -> CondominiumsCmdUseCase:
    repository = CondominiumsCmdRepositoryImpl()
    return CondominiumsCmdUseCase(repository)


def condominiums_query_usecase_factory() -> CondominiumsQueryUseCase:
    repository = CondominiumsQueryRepositoryImpl()
    return CondominiumsQueryUseCase(repository)
