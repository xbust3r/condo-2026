from abc import ABC, abstractmethod
from typing import Optional, List
from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes


class UnitysTypesCmdRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> UnitysTypes:
        pass
    
    @abstractmethod
    def update(self, id: int, data: dict) -> UnitysTypes:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class UnitysTypesQueryRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UnitysTypes]:
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[UnitysTypes]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[UnitysTypes]:
        pass
