"""
from typing import Optional
Permission Query Repository ABC.
"""
from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_permissions.domain.permission_entity import PermissionEntity


class PermissionQueryRepository(ABC):
    """Abstract repository for permission queries."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[PermissionEntity]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[PermissionEntity]:
        pass

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 100) -> tuple[List[PermissionEntity], int]:
        pass

    @abstractmethod
    def list_by_resource(self, resource: str, skip: int = 0, limit: int = 100) -> tuple[List[PermissionEntity], int]:
        pass

    @abstractmethod
    def list_by_action(self, action: str, skip: int = 0, limit: int = 100) -> tuple[List[PermissionEntity], int]:
        pass
