from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_condominium_roles.domain.condominium_role_entity import CondominiumRoleEntity
from library.dddpy.core_condominium_roles.domain.condominium_role_data import CreateCondominiumRoleData, UpdateCondominiumRoleData


class CondominiumRoleRepository(ABC):
    """Contrato abstracto para persistencia de roles de condominio."""

    @abstractmethod
    def create(self, data: CreateCondominiumRoleData) -> CondominiumRoleEntity:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[CondominiumRoleEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[CondominiumRoleEntity]:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateCondominiumRoleData) -> Optional[CondominiumRoleEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def list_by_condominium(self, condominium_id: int) -> List[CondominiumRoleEntity]:
        pass
