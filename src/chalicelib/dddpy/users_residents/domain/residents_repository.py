from abc import ABC, abstractmethod
from typing import Optional, List
from chalicelib.dddpy.users_residents.domain.residents import UsersResidents


class UsersResidentsCmdRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> UsersResidents:
        pass
    
    @abstractmethod
    def update(self, id: int, data: dict) -> UsersResidents:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class UsersResidentsQueryRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[UsersResidents]:
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[UsersResidents]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[UsersResidents]:
        pass
    
    @abstractmethod
    def get_by_unity_id(self, unity_id: int) -> List[UsersResidents]:
        pass
    
    @abstractmethod
    def get_by_building_id(self, building_id: int) -> List[UsersResidents]:
        pass
    
    @abstractmethod
    def get_by_condominium_id(self, condominium_id: int) -> List[UsersResidents]:
        pass
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[UsersResidents]:
        pass
