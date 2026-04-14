from library.dddpy.core_unities_types.infrastructure.unity_type_cmd_repository import (
    UnityTypeCmdRepositoryImpl,
)
from library.dddpy.core_unities_types.infrastructure.unity_type_query_repository import (
    UnityTypeQueryRepositoryImpl,
)
from library.dddpy.core_unities_types.usecase.unity_type_cmd_usecase import (
    UnityTypeCmdUseCase,
)
from library.dddpy.core_unities_types.usecase.unity_type_query_usecase import (
    UnityTypeQueryUseCase,
)


def unity_type_cmd_usecase_factory() -> UnityTypeCmdUseCase:
    """Factory for UnityTypeCmdUseCase with injected dependencies."""
    cmd_repo = UnityTypeCmdRepositoryImpl()
    query_repo = UnityTypeQueryRepositoryImpl()
    return UnityTypeCmdUseCase(cmd_repo=cmd_repo, query_repo=query_repo)


def unity_type_query_usecase_factory() -> UnityTypeQueryUseCase:
    """Factory for UnityTypeQueryUseCase with injected dependencies."""
    query_repo = UnityTypeQueryRepositoryImpl()
    return UnityTypeQueryUseCase(query_repo=query_repo)
