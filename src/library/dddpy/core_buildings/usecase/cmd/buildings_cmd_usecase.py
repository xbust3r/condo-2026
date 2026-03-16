# Buildings Command Use Case
from library.dddpy.core_buildings.domain.buildings import Buildings
from library.dddpy.core_buildings.domain.buildings_repository import BuildingsRepository
from library.dddpy.core_buildings.usecase.cmd import CreateBuildingsCmdSchema, UpdateBuildingsCmdSchema
from library.dddpy.shared.logging.logging import Logger

logger = Logger("BuildingsCmdUseCase")


class BuildingsCmdUseCase:
    def __init__(self, repository: BuildingsRepository):
        self.repository = repository

    def create(self, schema: CreateBuildingsCmdSchema) -> Buildings:
        logger.info(f"Creating building with code: {schema.code}")
        return self.repository.create(schema.model_dump())

    def update(self, id: int, schema: UpdateBuildingsCmdSchema) -> Buildings:
        logger.info(f"Updating building with id: {id}")
        return self.repository.update(id, schema.model_dump(exclude_unset=True))

    def delete(self, id: int) -> bool:
        logger.info(f"Deleting building with id: {id}")
        return self.repository.delete(id)
