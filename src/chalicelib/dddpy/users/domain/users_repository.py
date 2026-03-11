from abc import ABC, abstractmethod
from typing import Optional, List
from chalicelib.dddpy.users.domain.users import Users


class UsersCmdRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> Users:
        pass
    
    @abstractmethod
    def update(self, id: int, data: dict) -> Users:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class UsersQueryRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Users]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Users]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Users]:
        pass
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[Users]:
        pass
