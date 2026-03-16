from library.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from library.dddpy.core_buildings_types.domain.buildings_types_repository import BuildingsTypesRepository
from library.dddpy.core_buildings_types.usecase.cmd import CreateBuildingsTypesCmdSchema, UpdateBuildingsTypesCmdSchema
from library.dddpy.shared.logging.logging import Logger

logger = Logger("BuildingsTypesCmdUseCase")

class BuildingsTypesCmdUseCase:
    def __init__(self, repository: BuildingsTypesRepository):
        self.repository = repository

    def create(self, schema: CreateBuildingsTypesCmdSchema) -> BuildingsTypes:
        return self.repository.create(schema.model_dump())

    def update(self, id: int, schema: UpdateBuildingsTypesCmdSchema) -> BuildingsTypes:
        return self.repository.update(id, schema.model_dump(exclude_unset=True))

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
