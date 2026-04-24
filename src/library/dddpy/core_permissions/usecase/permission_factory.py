"""
from typing import Optional
Permission Factory — factory functions for Permission use cases.
"""
from typing import Optional

from library.dddpy.core_permissions.domain.permission_query_repository import PermissionQueryRepository
from library.dddpy.core_permissions.infrastructure.permission_query_repository import PermissionQueryRepositoryImpl
from library.dddpy.core_permissions.usecase.permission_query_usecase import PermissionQueryUseCase


def permission_query_usecase_factory() -> PermissionQueryUseCase:
    """Factory for PermissionQueryUseCase."""
    repository: Optional[PermissionQueryRepository] = PermissionQueryRepositoryImpl()
    return PermissionQueryUseCase(repository=repository)
