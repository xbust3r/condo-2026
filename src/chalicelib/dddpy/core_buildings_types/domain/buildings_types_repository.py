from abc import ABC, abstractmethod
from typing import Optional, List
from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes


class BuildingsTypesCmdRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> BuildingsTypes:
        pass
    
    @abstractmethod
    def update(self, id: int, data: dict) -> BuildingsTypes:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class BuildingsTypesQueryRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[BuildingsTypes]:
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[BuildingsTypes]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[BuildingsTypes]:
        pass
