from typing import Optional
from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_unit_ownerships.domain.unit_ownership_entity import UnitOwnershipEntity
from library.dddpy.core_unit_ownerships.domain.unit_ownership_data import CreateUnitOwnershipData, UpdateUnitOwnershipData


class UnitOwnershipRepository(ABC):
    """Contrato abstracto para persistencia de unit ownerships."""

    @abstractmethod
    def create(self, data: CreateUnitOwnershipData) -> UnitOwnershipEntity:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UnitOwnershipEntity]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[UnitOwnershipEntity]:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateUnitOwnershipData) -> Optional[UnitOwnershipEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def list_by_unit(self, unit_id: int) -> List[UnitOwnershipEntity]:
        pass

    @abstractmethod
    def list_by_user(self, user_id: int) -> List[UnitOwnershipEntity]:
        pass
