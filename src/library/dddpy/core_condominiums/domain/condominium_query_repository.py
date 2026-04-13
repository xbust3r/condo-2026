from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.core_condominiums.domain.condominium_entity import CondominiumEntity


class CondominiumQueryRepository(ABC):

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
    def list_all(self, skip: int = 0, limit: int = 100) -> tuple[List[CondominiumEntity], int]:
        pass