from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_condominiums.domain.condominium_entity import CondominiumEntity
from library.dddpy.core_condominiums.domain.condominium_data import CreateCondominiumData, UpdateCondominiumData


class CondominiumRepository(ABC):

    @abstractmethod
    def create(self, data: CreateCondominiumData) -> CondominiumEntity:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[CondominiumEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[CondominiumEntity]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[CondominiumEntity]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[CondominiumEntity]:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateCondominiumData) -> Optional[CondominiumEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        """Restore a soft-deleted condominium."""
        pass

    @abstractmethod
    def list_all(self) -> List[CondominiumEntity]:
        pass