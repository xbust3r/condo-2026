from typing import List, Optional
from library.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from library.dddpy.core_buildings_types.domain.buildings_types_repository import BuildingsTypesRepository
from library.dddpy.core_buildings_types.usecase.cmd import CreateBuildingsTypesCmdSchema, UpdateBuildingsTypesCmdSchema
from library.dddpy.core_buildings_types.usecase.cmd import BuildingsTypesCmdUseCase
from library.dddpy.core_buildings_types.usecase.query import BuildingsTypesQueryUseCase

class BuildingsTypesUseCase:
    def __init__(self, repository: BuildingsTypesRepository):
        self.cmd_use_case = BuildingsTypesCmdUseCase(repository)
        self.query_use_case = BuildingsTypesQueryUseCase(repository)

    def create(self, schema: CreateBuildingsTypesCmdSchema) -> BuildingsTypes:
        return self.cmd_use_case.create(schema)
    def update(self, id: int, schema: UpdateBuildingsTypesCmdSchema) -> BuildingsTypes:
        return self.cmd_use_case.update(id, schema)
    def delete(self, id: int) -> bool:
        return self.cmd_use_case.delete(id)
    def get_all(self) -> List[BuildingsTypes]:
        return self.query_use_case.get_all()
    def get_by_id(self, id: int) -> Optional[BuildingsTypes]:
        return self.query_use_case.get_by_id(id)
    def get_by_code(self, code: str) -> Optional[BuildingsTypes]:
        return self.query_use_case.get_by_code(code)

def create_buildings_types_usecase():
    from library.dddpy.core_buildings_types.infrastructure.buildings_types_cmd_repository import BuildingsTypesCmdRepositoryImpl
    return BuildingsTypesUseCase(BuildingsTypesCmdRepositoryImpl())
