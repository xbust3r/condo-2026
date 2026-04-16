"""
RolePermission Factory — factory functions.
"""
from typing import Optional

from library.dddpy.core_role_permissions.domain.role_permission_query_repository import RolePermissionQueryRepository
from library.dddpy.core_role_permissions.infrastructure.role_permission_query_repository import RolePermissionQueryRepositoryImpl
from library.dddpy.core_role_permissions.usecase.role_permission_query_usecase import RolePermissionQueryUseCase


def role_permission_query_usecase_factory() -> RolePermissionQueryUseCase:
    """Factory for RolePermissionQueryUseCase."""
    rp_repo: RolePermissionQueryRepository = RolePermissionQueryRepositoryImpl()
    return RolePermissionQueryUseCase(rp_repository=rp_repo)
