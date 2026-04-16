"""
RolePermission Query Repository ABC.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple

from library.dddpy.core_role_permissions.domain.role_permission_entity import RolePermissionEntity


class RolePermissionQueryRepository(ABC):
    """Abstract repository for role-permission queries."""

    @abstractmethod
    def list_by_role(self, role: str) -> List[RolePermissionEntity]:
        pass

    @abstractmethod
    def list_permissions_by_role(
        self, role: str, skip: int = 0, limit: int = 100
    ) -> Tuple[List[RolePermissionEntity], int]:
        pass

    @abstractmethod
    def get_roles_for_permission(self, permission_code: str) -> List[str]:
        pass
