# Condominium Use Case - Facade
from typing import List, Optional
from library.dddpy.core_condominiums.domain.condominiums import Condominium
from library.dddpy.core_condominiums.domain.condominiums_repository import CondominiumRepository
from library.dddpy.core_condominiums.usecase.cmd import CreateCondominiumCmdSchema, UpdateCondominiumCmdSchema
from library.dddpy.core_condominiums.usecase.cmd import CondominiumCmdUseCase
from library.dddpy.core_condominiums.usecase.query import CondominiumQueryUseCase


class CondominiumUseCase:
    """Facade that combines Command and Query operations"""
    
    def __init__(self, repository: CondominiumRepository):
        self.cmd_use_case = CondominiumCmdUseCase(repository)
        self.query_use_case = CondominiumQueryUseCase(repository)

    # Command operations
    def create(self, schema: CreateCondominiumCmdSchema) -> Condominium:
        return self.cmd_use_case.create(schema)

    def update(self, id: int, schema: UpdateCondominiumCmdSchema) -> Condominium:
        return self.cmd_use_case.update(id, schema)

    def delete(self, id: int) -> bool:
        return self.cmd_use_case.delete(id)

    # Query operations
    def get_all(self) -> List[Condominium]:
        return self.query_use_case.get_all()

    def get_by_id(self, id: int) -> Optional[Condominium]:
        return self.query_use_case.get_by_id(id)

    def get_by_code(self, code: str) -> Optional[Condominium]:
        return self.query_use_case.get_by_code(code)

    def get_by_status(self, status: int) -> List[Condominium]:
        return self.query_use_case.get_by_status(status)
