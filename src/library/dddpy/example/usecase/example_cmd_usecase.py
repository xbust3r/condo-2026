from typing import Optional

from chalicelib.dddpy.example.usecase.example_cmd_schema import CreateExampleSchema, UpdateExampleSchema
from chalicelib.dddpy.example.domain.example_cmd_repository import ExampleCmdRepository
from chalicelib.dddpy.example.domain.example_entity import ExampleEntity
from chalicelib.dddpy.shared.logging.logging import Logger


logger = Logger("ExampleCmdUseCase")


class ExampleCmdUseCase:

    def __init__(self, repository: ExampleCmdRepository):
        self.repository = repository
        logger.info("ExampleCmdUseCase initialized")

    def create(self, example_data: CreateExampleSchema) -> ExampleEntity:
        logger.info(f"Delegating example creation for code={example_data.code}")
        return self.repository.create(example_data)

    def update(self, id: int, example_data: UpdateExampleSchema) -> Optional[ExampleEntity]:
        logger.info(f"Delegating example update for id={id}")
        return self.repository.update(id, example_data)

    def delete(self, id: int) -> bool:
        logger.info(f"Delegating example delete for id={id}")
        return self.repository.delete(id)
