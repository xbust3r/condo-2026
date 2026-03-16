from typing import List, Optional
from library.dddpy.core_unittys_types.domain.unittys_types import UnittysTypes, UnittysTypesRepository
from library.dddpy.core_unittys_types.usecase.cmd import CreateUnittysTypesCmdSchema, UpdateUnittysTypesCmdSchema

class UnittysTypesCmdUseCase:
    def __init__(self, repository: UnittysTypesRepository):
        self.repository = repository
    def create(self, schema: CreateUnittysTypesCmdSchema) -> UnittysTypes:
        return self.repository.create(schema.model_dump())
    def update(self, id: int, schema: UpdateUnittysTypesCmdSchema) -> UnittysTypes:
        return self.repository.update(id, schema.model_dump(exclude_unset=True))
    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

class UnittysTypesQueryUseCase:
    def __init__(self, repository: UnittysTypesRepository):
        self.repository = repository
    def get_all(self) -> List[UnittysTypes]:
        return self.repository.all()
    def get_by_id(self, id: int) -> Optional[UnittysTypes]:
        return self.repository.get_by_id(id)
    def get_by_code(self, code: str) -> Optional[UnittysTypes]:
        return self.repository.get_by_code(code)

class UnittysTypesUseCase:
    def __init__(self, repository: UnittysTypesRepository):
        self.cmd_use_case = UnittysTypesCmdUseCase(repository)
        self.query_use_case = UnittysTypesQueryUseCase(repository)
    def create(self, schema: CreateUnittysTypesCmdSchema) -> UnittysTypes:
        return self.cmd_use_case.create(schema)
    def update(self, id: int, schema: UpdateUnittysTypesCmdSchema) -> UnittysTypes:
        return self.cmd_use_case.update(id, schema)
    def delete(self, id: int) -> bool:
        return self.cmd_use_case.delete(id)
    def get_all(self) -> List[UnittysTypes]:
        return self.query_use_case.get_all()
    def get_by_id(self, id: int) -> Optional[UnittysTypes]:
        return self.query_use_case.get_by_id(id)
    def get_by_code(self, code: str) -> Optional[UnittysTypes]:
        return self.query_use_case.get_by_code(code)

def create_unittys_types_usecase():
    from library.dddpy.core_unittys_types.infrastructure.unittys_types_cmd_repository import UnittysTypesCmdRepositoryImpl
    return UnittysTypesUseCase(UnittysTypesCmdRepositoryImpl())
