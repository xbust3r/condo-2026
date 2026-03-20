from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.example.domain.example_entity import ExampleEntity
from library.dddpy.example.domain.example_data import CreateExampleData, UpdateExampleData


class ExampleCmdRepository(ABC):

    @abstractmethod
    def create(self, data: CreateExampleData) -> ExampleEntity:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateExampleData) -> Optional[ExampleEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
