from abc import ABC, abstractmethod
from typing import Optional, List

from library.dddpy.example.domain.example_entity import ExampleEntity


class ExampleQueryRepository(ABC):

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
    def list_all(self) -> List[ExampleEntity]:
        pass
