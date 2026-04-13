from library.dddpy.core_condominiums.infrastructure.condominium_cmd_repository import CondominiumCmdRepositoryImpl
from library.dddpy.core_condominiums.infrastructure.condominium_query_repository import CondominiumQueryRepositoryImpl
from library.dddpy.core_condominiums.usecase.condominium_cmd_usecase import CondominiumCmdUseCase
from library.dddpy.core_condominiums.usecase.condominium_query_usecase import CondominiumQueryUseCase


def condominium_cmd_usecase_factory():
    repository = CondominiumCmdRepositoryImpl()
    return CondominiumCmdUseCase(repository)


def condominium_query_usecase_factory():
    repository = CondominiumQueryRepositoryImpl()
    return CondominiumQueryUseCase(repository)