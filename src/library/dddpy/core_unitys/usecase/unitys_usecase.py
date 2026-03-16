from typing import List, Optional
from library.dddpy.core_unitys.domain.unitys import Unitys
from library.dddpy.core_unitys.domain.unitys_repository import UnitysRepository
from library.dddpy.core_unitys.usecase.cmd import CreateUnitysCmdSchema, UpdateUnitysCmdSchema

class UnitysCmdUseCase:
    def __init__(self, repository: UnitysRepository):
        self.repository = repository
    def create(self, schema: CreateUnitysCmdSchema) -> Unitys:
        return self.repository.create(schema.model_dump())
    def update(self, id: int, schema: UpdateUnitysCmdSchema) -> Unitys:
        return self.repository.update(id, schema.model_dump(exclude_unset=True))
    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

class UnitysQueryUseCase:
    def __init__(self, repository: UnitysRepository):
        self.repository = repository
    def get_all(self) -> List[Unitys]:
        return self.repository.all()
    def get_by_id(self, id: int) -> Optional[Unitys]:
        return self.repository.get_by_id(id)
    def get_by_code(self, code: str) -> Optional[Unitys]:
        return self.repository.get_by_code(code)
    def get_by_building(self, building_id: int) -> List[Unitys]:
        return self.repository.get_by_building(building_id)

class UnitysUseCase:
    def __init__(self, repository: UnitysRepository):
        self.cmd_use_case = UnitysCmdUseCase(repository)
        self.query_use_case = UnitysQueryUseCase(repository)
    def create(self, schema: CreateUnitysCmdSchema) -> Unitys:
        return self.cmd_use_case.create(schema)
    def update(self, id: int, schema: UpdateUnitysCmdSchema) -> Unitys:
        return self.cmd_use_case.update(id, schema)
    def delete(self, id: int) -> bool:
        return self.cmd_use_case.delete(id)
    def get_all(self) -> List[Unitys]:
        return self.query_use_case.get_all()
    def get_by_id(self, id: int) -> Optional[Unitys]:
        return self.query_use_case.get_by_id(id)
    def get_by_code(self, code: str) -> Optional[Unitys]:
        return self.query_use_case.get_by_code(code)
    def get_by_building(self, building_id: int) -> List[Unitys]:
        return self.query_use_case.get_by_building(building_id)

def create_unitys_usecase():
    from library.dddpy.core_unitys.infrastructure.unitys import UnitysCmdRepositoryImpl
    return UnitysUseCase(UnitysCmdRepositoryImpl())
