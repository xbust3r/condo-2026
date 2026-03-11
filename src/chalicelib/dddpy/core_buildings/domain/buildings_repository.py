from abc import ABC, abstractmethod
from typing import Optional, List
from chalicelib.dddpy.core_buildings.domain.buildings import Buildings


class BuildingsCmdRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> Buildings:
        pass
    
    @abstractmethod
    def update(self, id: int, data: dict) -> Buildings:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class BuildingsQueryRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Buildings]:
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Buildings]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Buildings]:
        pass
    
    @abstractmethod
    def get_by_condominium_id(self, condominium_id: int) -> List[Buildings]:
        pass
