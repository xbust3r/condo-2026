from abc import ABC, abstractmethod
from typing import Optional, List
from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums

class CondominiumsCmdRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> Condominiums:
        pass
    
    @abstractmethod
    def update(self, id: int, data: dict) -> Condominiums:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class CondominiumsQueryRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Condominiums]:
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Condominiums]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Condominiums]:
        pass
