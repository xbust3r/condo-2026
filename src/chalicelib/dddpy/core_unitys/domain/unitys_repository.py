from abc import ABC, abstractmethod
from typing import Optional, List
from chalicelib.dddpy.core_unitys.domain.unitys import Unitys


class UnitysCmdRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> Unitys:
        pass
    
    @abstractmethod
    def update(self, id: int, data: dict) -> Unitys:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class UnitysQueryRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Unitys]:
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Unitys]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Unitys]:
        pass
    
    @abstractmethod
    def get_by_building_id(self, building_id: int) -> List[Unitys]:
        pass
