"""
Visitor factory — builds cmd and query use case instances.
"""
from library.dddpy.core_visitors.infrastructure.visitor_cmd_repository import VisitorCmdRepositoryImpl
from library.dddpy.core_visitors.infrastructure.visitor_query_repository import VisitorQueryRepositoryImpl
from library.dddpy.core_visitors.usecase.visitor_cmd_usecase import VisitorCmdUseCase
from library.dddpy.core_visitors.usecase.visitor_query_usecase import VisitorQueryUseCase


def visitor_cmd_usecase_factory() -> VisitorCmdUseCase:
    return VisitorCmdUseCase(
        repository=VisitorCmdRepositoryImpl(),
        query_repository=VisitorQueryRepositoryImpl(),
    )


def visitor_query_usecase_factory() -> VisitorQueryUseCase:
    return VisitorQueryUseCase(repository=VisitorQueryRepositoryImpl())