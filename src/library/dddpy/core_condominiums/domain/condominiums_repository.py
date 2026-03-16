# Condominium Repository Interface
from abc import ABC, abstractmethod
from typing import List, Optional


class CondominiumRepository(ABC):
    
    @abstractmethod
    def all(self) -> List:
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def update(self, id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def get_by_code(self, code: str):
        raise NotImplementedError

    @abstractmethod
    def get_by_status(self, status: int) -> List:
        raise NotImplementedError
