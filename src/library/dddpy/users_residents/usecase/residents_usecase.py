from typing import List, Optional
from library.dddpy.users_residents.domain.residents import Residents, ResidentsRepository
from library.dddpy.users_residents.usecase.cmd import CreateResidentsCmdSchema, UpdateResidentsCmdSchema

class ResidentsCmdUseCase:
    def __init__(self, repository: ResidentsRepository):
        self.repository = repository
    def create(self, schema: CreateResidentsCmdSchema) -> Residents:
        return self.repository.create(schema.model_dump())
    def update(self, id: int, schema: UpdateResidentsCmdSchema) -> Residents:
        return self.repository.update(id, schema.model_dump(exclude_unset=True))
    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

class ResidentsQueryUseCase:
    def __init__(self, repository: ResidentsRepository):
        self.repository = repository
    def get_all(self) -> List[Residents]:
        return self.repository.all()
    def get_by_id(self, id: int) -> Optional[Residents]:
        return self.repository.get_by_id(id)
    def get_by_user(self, user_id: int) -> List[Residents]:
        return self.repository.get_by_user(user_id)
    def get_by_unity(self, unity_id: int) -> List[Residents]:
        return self.repository.get_by_unity(unity_id)

class ResidentsUseCase:
    def __init__(self, repository: ResidentsRepository):
        self.cmd_use_case = ResidentsCmdUseCase(repository)
        self.query_use_case = ResidentsQueryUseCase(repository)
    def create(self, schema: CreateResidentsCmdSchema) -> Residents:
        return self.cmd_use_case.create(schema)
    def update(self, id: int, schema: UpdateResidentsCmdSchema) -> Residents:
        return self.cmd_use_case.update(id, schema)
    def delete(self, id: int) -> bool:
        return self.cmd_use_case.delete(id)
    def get_all(self) -> List[Residents]:
        return self.query_use_case.get_all()
    def get_by_id(self, id: int) -> Optional[Residents]:
        return self.query_use_case.get_by_id(id)
    def get_by_user(self, user_id: int) -> List[Residents]:
        return self.query_use_case.get_by_user(user_id)
    def get_by_unity(self, unity_id: int) -> List[Residents]:
        return self.query_use_case.get_by_unity(unity_id)

def create_residents_usecase():
    from library.dddpy.users_residents.infrastructure.residents import ResidentsCmdRepositoryImpl
    return ResidentsUseCase(ResidentsCmdRepositoryImpl())
