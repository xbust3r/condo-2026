# Buildings Types Use Cases
from typing import List, Optional
from library.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from library.dddpy.core_buildings_types.domain.buildings_types_repository import BuildingsTypesRepository
from library.dddpy.core_buildings_types.usecase.buildings_types_cmd_schema import (
    CreateBuildingsTypesSchema,
    UpdateBuildingsTypesSchema,
)
from library.dddpy.shared.logging.logging import Logger

logger = Logger("BuildingsTypesUseCase")


class BuildingsTypesCmdUseCase:
    
    def __init__(self, repository: BuildingsTypesRepository):
        self.repository = repository

    def create(self, schema: CreateBuildingsTypesSchema) -> BuildingsTypes:
        logger.info(f"Creating building type with code: {schema.code}")
        data = schema.model_dump()
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateBuildingsTypesSchema) -> BuildingsTypes:
        logger.info(f"Updating building type with id: {id}")
        data = schema.model_dump(exclude_unset=True)
        return self.repository.update(id, data)

    def delete(self, id: int) -> bool:
        logger.info(f"Deleting building type with id: {id}")
        return self.repository.delete(id)


class BuildingsTypesQueryUseCase:
    
    def __init__(self, repository: BuildingsTypesRepository):
        self.repository = repository

    def get_all(self) -> List[BuildingsTypes]:
        return self.repository.all()

    def get_by_id(self, id: int) -> Optional[BuildingsTypes]:
        return self.repository.get_by_id(id)

    def get_by_code(self, code: str) -> Optional[BuildingsTypes]:
        return self.repository.get_by_code(code)


class BuildingsTypesUseCase:
    """Facade for Buildings Types"""
    
    def __init__(self, repository: BuildingsTypesRepository):
        self.cmd_use_case = BuildingsTypesCmdUseCase(repository)
        self.query_use_case = BuildingsTypesQueryUseCase(repository)

    def create(self, schema: CreateBuildingsTypesSchema) -> BuildingsTypes:
        return self.cmd_use_case.create(schema)

    def update(self, id: int, schema: UpdateBuildingsTypesSchema) -> BuildingsTypes:
        return self.cmd_use_case.update(id, schema)

    def delete(self, id: int) -> bool:
        return self.cmd_use_case.delete(id)

    def get_all(self) -> List[BuildingsTypes]:
        return self.query_use_case.get_all()

    def get_by_id(self, id: int) -> Optional[BuildingsTypes]:
        return self.query_use_case.get_by_id(id)

    def get_by_code(self, code: str) -> Optional[BuildingsTypes]:
        return self.query_use_case.get_by_code(code)


# Factory
def create_buildings_types_repository() -> BuildingsTypesRepository:
    return BuildingsTypesCmdRepositoryImpl()


def create_buildings_types_usecase() -> BuildingsTypesUseCase:
    return BuildingsTypesUseCase(create_buildings_types_repository())
