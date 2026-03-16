from typing import Optional

from chalicelib.dddpy.example.usecase.example_cmd_schema import CreateExampleSchema, UpdateExampleSchema
from chalicelib.dddpy.example.domain.example_cmd_repository import ExampleCmdRepository
from chalicelib.dddpy.example.domain.example_entity import ExampleEntity
from chalicelib.dddpy.example.domain.example_data import CreateExampleData, UpdateExampleData
from chalicelib.dddpy.shared.logging.logging import Logger


logger = Logger("ExampleCmdUseCase")


class ExampleCmdUseCase:

    def __init__(self, repository: ExampleCmdRepository):
        self.repository = repository
        logger.info("ExampleCmdUseCase initialized")

    def create(self, example_data: CreateExampleSchema) -> ExampleEntity:
        logger.info(f"Delegating example creation for code={example_data.code}")
        data = CreateExampleData(
            code=example_data.code,
            name=example_data.name,
            description=example_data.description,
        )
        return self.repository.create(data)

    def update(self, id: int, example_data: UpdateExampleSchema) -> Optional[ExampleEntity]:
        logger.info(f"Delegating example update for id={id}")
        data = UpdateExampleData(
            name=example_data.name,
            description=example_data.description,
        )
        return self.repository.update(id, data)

    def delete(self, id: int) -> bool:
        logger.info(f"Delegating example delete for id={id}")
        return self.repository.delete(id)
