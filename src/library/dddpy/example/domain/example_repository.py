from abc import ABC, abstractmethod
from typing import Optional, List

from chalicelib.dddpy.example.domain.example_entity import ExampleEntity
from chalicelib.dddpy.example.domain.example_data import CreateExampleData, UpdateExampleData


class ExampleRepository(ABC):

    @abstractmethod
    def create(self, data: CreateExampleData) -> ExampleEntity:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[ExampleEntity]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[ExampleEntity]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[ExampleEntity]:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateExampleData) -> Optional[ExampleEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[ExampleEntity]:
        pass
