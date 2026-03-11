from chalicelib.dddpy.users_residents.usecase.residents_cmd_usecase import UsersResidentsCmdUseCase
from chalicelib.dddpy.users_residents.usecase.residents_query_usecase import UsersResidentsQueryUseCase
from chalicelib.dddpy.users_residents.infrastructure.residents_cmd_repository import UsersResidentsCmdRepositoryImpl
from chalicelib.dddpy.users_residents.infrastructure.residents_query_repository import UsersResidentsQueryRepositoryImpl


def residents_cmd_usecase_factory() -> UsersResidentsCmdUseCase:
    repository = UsersResidentsCmdRepositoryImpl()
    return UsersResidentsCmdUseCase(repository)


def residents_query_usecase_factory() -> UsersResidentsQueryUseCase:
    repository = UsersResidentsQueryRepositoryImpl()
    return UsersResidentsQueryUseCase(repository)
