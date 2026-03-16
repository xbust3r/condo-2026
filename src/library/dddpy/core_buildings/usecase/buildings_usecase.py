# Buildings Use Case - Facade
from typing import List, Optional
from library.dddpy.core_buildings.domain.buildings import Buildings
from library.dddpy.core_buildings.domain.buildings_repository import BuildingsRepository
from library.dddpy.core_buildings.usecase.cmd import CreateBuildingsCmdSchema, UpdateBuildingsCmdSchema
from library.dddpy.core_buildings.usecase.cmd import BuildingsCmdUseCase
from library.dddpy.core_buildings.usecase.query import BuildingsQueryUseCase


class BuildingsUseCase:
    def __init__(self, repository: BuildingsRepository):
        self.cmd_use_case = BuildingsCmdUseCase(repository)
        self.query_use_case = BuildingsQueryUseCase(repository)

    # Command
    def create(self, schema: CreateBuildingsCmdSchema) -> Buildings:
        return self.cmd_use_case.create(schema)

    def update(self, id: int, schema: UpdateBuildingsCmdSchema) -> Buildings:
        return self.cmd_use_case.update(id, schema)

    def delete(self, id: int) -> bool:
        return self.cmd_use_case.delete(id)

    # Query
    def get_all(self) -> List[Buildings]:
        return self.query_use_case.get_all()

    def get_by_id(self, id: int) -> Optional[Buildings]:
        return self.query_use_case.get_by_id(id)

    def get_by_code(self, code: str) -> Optional[Buildings]:
        return self.query_use_case.get_by_code(code)

    def get_by_condominium(self, condominium_id: int) -> List[Buildings]:
        return self.query_use_case.get_by_condominium(condominium_id)


def create_buildings_usecase() -> BuildingsUseCase:
    from library.dddpy.core_buildings.infrastructure.buildings_cmd_repository import BuildingsCmdRepositoryImpl
    return BuildingsUseCase(BuildingsCmdRepositoryImpl())
