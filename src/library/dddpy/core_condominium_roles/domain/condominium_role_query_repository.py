from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from library.dddpy.core_condominium_roles.domain.condominium_role_entity import CondominiumRoleEntity


class CondominiumRoleQueryRepository(ABC):
    """Interfaz de lectura para consultas de roles de condominio."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[CondominiumRoleEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[CondominiumRoleEntity]:
        pass

    @abstractmethod
    def get_active_by_user_and_condominium(
        self, user_id: int, condominium_id: int
    ) -> Optional[CondominiumRoleEntity]:
        """Get active role assignment for a user in a specific condominium."""
        pass

    @abstractmethod
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        user_id: Optional[int] = None,
        role: Optional[str] = None,
        scope: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[CondominiumRoleEntity], int]:
        """List role assignments with optional filters."""
        pass

    @abstractmethod
    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[CondominiumRoleEntity], int]:
        """List role assignments for a specific condominium."""
        pass

    @abstractmethod
    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[CondominiumRoleEntity], int]:
        """List role assignments for a specific user."""
        pass
