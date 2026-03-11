from chalicelib.dddpy.users.usecase.users_cmd_usecase import UsersCmdUseCase
from chalicelib.dddpy.users.usecase.users_query_usecase import UsersQueryUseCase
from chalicelib.dddpy.users.infrastructure.users_cmd_repository import UsersCmdRepositoryImpl
from chalicelib.dddpy.users.infrastructure.users_query_repository import UsersQueryRepositoryImpl


def users_cmd_usecase_factory() -> UsersCmdUseCase:
    repository = UsersCmdRepositoryImpl()
    return UsersCmdUseCase(repository)


def users_query_usecase_factory() -> UsersQueryUseCase:
    repository = UsersQueryRepositoryImpl()
    return UsersQueryUseCase(repository)
