from abc import ABC, abstractmethod
from typing import Optional

from chalicelib.dddpy.example.domain.example_entity import ExampleEntity
from chalicelib.dddpy.example.usecase.example_cmd_schema import CreateExampleSchema, UpdateExampleSchema


class ExampleCmdRepository(ABC):

    @abstractmethod
    def create(self, example: CreateExampleSchema) -> ExampleEntity:
        pass

    @abstractmethod
    def update(self, id: int, example: UpdateExampleSchema) -> Optional[ExampleEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
