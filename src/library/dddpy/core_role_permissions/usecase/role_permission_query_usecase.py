from __future__ import annotations
"""
RolePermission Query UseCase.
"""
from typing import List, Tuple

from library.dddpy.core_role_permissions.domain.role_permission_entity import RolePermissionEntity
from library.dddpy.core_role_permissions.domain.role_permission_exception import RoleNotFound
from library.dddpy.core_role_permissions.domain.role_permission_query_repository import RolePermissionQueryRepository
from library.dddpy.core_role_permissions.infrastructure.role_permission_query_repository import RolePermissionQueryRepositoryImpl
from library.dddpy.core_permissions.domain.permission_entity import PermissionEntity
from library.dddpy.core_permissions.domain.permission_query_repository import PermissionQueryRepository
from library.dddpy.core_permissions.infrastructure.permission_query_repository import PermissionQueryRepositoryImpl
from library.dddpy.shared.logging.logging import Logger


logger = Logger("RolePermissionQueryUseCase")


class RolePermissionQueryUseCase:

    def __init__(
        self,
        rp_repository: RolePermissionQueryRepository | None = None,
        perm_repository: PermissionQueryRepository | None = None,
    ) -> None:
        self._rp_repo = rp_repository or RolePermissionQueryRepositoryImpl()
        self._perm_repo = perm_repository or PermissionQueryRepositoryImpl()
        logger.info("RolePermissionQueryUseCase initialized")

    def list_by_role(self, role: str) -> List[RolePermissionEntity]:
        logger.debug(f"Listing role-permissions for role={role}")
        return self._rp_repo.list_by_role(role)

    def get_permissions_for_role(
        self, role: str, skip: int = 0, limit: int = 100
    ) -> Tuple[List[PermissionEntity], int]:
        """
        Get full PermissionEntity objects for all permissions assigned to a role.
        Returns (permissions, total).
        """
        logger.debug(f"Getting full permission objects for role={role}")
        if limit > 500:
            limit = 500
        rp_list, total = self._rp_repo.list_permissions_by_role(role, skip=skip, limit=limit)
        permissions = []
        for rp in rp_list:
            perm = self._perm_repo.get_by_code(rp.permission_code)
            if perm:
                permissions.append(perm)
        return permissions, total

    def get_roles_for_permission(self, permission_code: str) -> List[str]:
        logger.debug(f"Getting roles for permission={permission_code}")
        return self._rp_repo.get_roles_for_permission(permission_code)
