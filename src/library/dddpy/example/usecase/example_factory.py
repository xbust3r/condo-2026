from library.dddpy.example.infrastructure.example_cmd_repository import ExampleCmdRepositoryImpl
from library.dddpy.example.infrastructure.example_query_repository import ExampleQueryRepositoryImpl
from library.dddpy.example.usecase.example_cmd_usecase import ExampleCmdUseCase
from library.dddpy.example.usecase.example_query_usecase import ExampleQueryUseCase


def example_cmd_usecase_factory():
    repository = ExampleCmdRepositoryImpl()
    return ExampleCmdUseCase(repository)


def example_query_usecase_factory():
    repository = ExampleQueryRepositoryImpl()
    return ExampleQueryUseCase(repository)
