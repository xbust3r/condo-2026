from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_condominiums.domain.condominium_entity import CondominiumEntity
from library.dddpy.core_condominiums.domain.condominium_data import CreateCondominiumData, UpdateCondominiumData


class CondominiumCmdRepository(ABC):

    @abstractmethod
    def create(self, data: CreateCondominiumData) -> CondominiumEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateCondominiumData) -> Optional[CondominiumEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass