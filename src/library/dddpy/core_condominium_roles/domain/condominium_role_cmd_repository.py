from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_condominium_roles.domain.condominium_role_entity import CondominiumRoleEntity
from library.dddpy.core_condominium_roles.domain.condominium_role_data import CreateCondominiumRoleData, UpdateCondominiumRoleData


class CondominiumRoleCmdRepository(ABC):
    """Interfaz de escritura para operaciones de modificación de roles de condominio."""

    @abstractmethod
    def create(self, data: CreateCondominiumRoleData) -> CondominiumRoleEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateCondominiumRoleData) -> Optional[CondominiumRoleEntity]:
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        """Restore a soft-deleted role assignment: clears deleted_at."""
        pass

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        """Physical delete."""
        pass

    @abstractmethod
    def soft_delete_by_user(self, user_id: int) -> int:
        """Soft-delete all active roles for a user. Returns count of affected rows."""
        pass
