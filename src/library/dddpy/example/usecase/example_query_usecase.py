from typing import Optional, List

from library.dddpy.example.domain.example_query_repository import ExampleQueryRepository
from library.dddpy.example.domain.example_entity import ExampleEntity
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ExampleQueryUseCase")


class ExampleQueryUseCase:

    def __init__(self, repository: ExampleQueryRepository):
        self.repository = repository
        logger.info("ExampleQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[ExampleEntity]:
        logger.info(f"Delegating example fetch by id={id}")
        return self.repository.get_by_id(id)

    def get_by_code(self, code: str) -> Optional[ExampleEntity]:
        logger.info(f"Delegating example fetch by code={code}")
        return self.repository.get_by_code(code)

    def get_by_name(self, name: str) -> Optional[ExampleEntity]:
        logger.info(f"Delegating example fetch by name={name}")
        return self.repository.get_by_name(name)

    def list_all(self) -> List[ExampleEntity]:
        logger.info("Delegating example list_all")
        return self.repository.list_all()
