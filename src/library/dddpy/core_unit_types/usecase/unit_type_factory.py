from library.dddpy.core_unit_types.infrastructure.unit_type_cmd_repository import (
    UnitTypeCmdRepositoryImpl,
)
from library.dddpy.core_unit_types.infrastructure.unit_type_query_repository import (
    UnitTypeQueryRepositoryImpl,
)
from library.dddpy.core_unit_types.usecase.unit_type_cmd_usecase import (
    UnitTypeCmdUseCase,
)
from library.dddpy.core_unit_types.usecase.unit_type_query_usecase import (
    UnitTypeQueryUseCase,
)


def unit_type_cmd_usecase_factory() -> UnitTypeCmdUseCase:
    """Factory for UnitTypeCmdUseCase with injected dependencies."""
    cmd_repo = UnitTypeCmdRepositoryImpl()
    query_repo = UnitTypeQueryRepositoryImpl()
    return UnitTypeCmdUseCase(cmd_repo=cmd_repo, query_repo=query_repo)


def unit_type_query_usecase_factory() -> UnitTypeQueryUseCase:
    """Factory for UnitTypeQueryUseCase with injected dependencies."""
    query_repo = UnitTypeQueryRepositoryImpl()
    return UnitTypeQueryUseCase(query_repo=query_repo)