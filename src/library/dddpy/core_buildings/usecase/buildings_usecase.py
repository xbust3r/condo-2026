# Buildings Use Cases
from typing import List, Optional
from library.dddpy.core_buildings.domain.buildings import Buildings
from library.dddpy.core_buildings.domain.buildings_repository import BuildingsRepository
from library.dddpy.core_buildings.usecase.buildings_cmd_schema import (
    CreateBuildingsSchema,
    UpdateBuildingsSchema,
)
from library.dddpy.shared.logging.logging import Logger

logger = Logger("BuildingsUseCase")


class BuildingsCmdUseCase:
    
    def __init__(self, repository: BuildingsRepository):
        self.repository = repository

    def create(self, schema: CreateBuildingsSchema) -> Buildings:
        logger.info(f"Creating building with code: {schema.code}")
        data = schema.model_dump()
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateBuildingsSchema) -> Buildings:
        logger.info(f"Updating building with id: {id}")
        data = schema.model_dump(exclude_unset=True)
        return self.repository.update(id, data)

    def delete(self, id: int) -> bool:
        logger.info(f"Deleting building with id: {id}")
        return self.repository.delete(id)


class BuildingsQueryUseCase:
    
    def __init__(self, repository: BuildingsRepository):
        self.repository = repository

    def get_all(self) -> List[Buildings]:
        return self.repository.all()

    def get_by_id(self, id: int) -> Optional[Buildings]:
        return self.repository.get_by_id(id)

    def get_by_code(self, code: str) -> Optional[Buildings]:
        return self.repository.get_by_code(code)

    def get_by_condominium(self, condominium_id: int) -> List[Buildings]:
        return self.repository.get_by_condominium(condominium_id)


class BuildingsUseCase:
    """Facade for Buildings"""
    
    def __init__(self, repository: BuildingsRepository):
        self.cmd_use_case = BuildingsCmdUseCase(repository)
        self.query_use_case = BuildingsQueryUseCase(repository)

    def create(self, schema: CreateBuildingsSchema) -> Buildings:
        return self.cmd_use_case.create(schema)

    def update(self, id: int, schema: UpdateBuildingsSchema) -> Buildings:
        return self.cmd_use_case.update(id, schema)

    def delete(self, id: int) -> bool:
        return self.cmd_use_case.delete(id)

    def get_all(self) -> List[Buildings]:
        return self.query_use_case.get_all()

    def get_by_id(self, id: int) -> Optional[Buildings]:
        return self.query_use_case.get_by_id(id)

    def get_by_code(self, code: str) -> Optional[Buildings]:
        return self.query_use_case.get_by_code(code)

    def get_by_condominium(self, condominium_id: int) -> List[Buildings]:
        return self.query_use_case.get_by_condominium(condominium_id)


# Factory
def create_buildings_repository() -> BuildingsRepository:
    return BuildingsCmdRepositoryImpl()


def create_buildings_usecase() -> BuildingsUseCase:
    return BuildingsUseCase(create_buildings_repository())
