# Residents Schemas and Use Cases
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from library.dddpy.users_residents.domain.residents import Residents, ResidentsRepository
from library.dddpy.users_residents.infrastructure.residents import ResidentsCmdRepositoryImpl


class CreateResidentsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    condominium_id: int
    building_id: int
    unity_id: int
    user_id: int
    type: str = Field(..., max_length=100)  # Owner, Tenant, Family, Employee
    status: int = Field(default=1, ge=0, le=2)


class UpdateResidentsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    condominium_id: Optional[int] = None
    building_id: Optional[int] = None
    unity_id: Optional[int] = None
    user_id: Optional[int] = None
    type: Optional[str] = Field(None, max_length=100)
    status: Optional[int] = Field(None, ge=0, le=2)


class ResidentsUseCase:
    """Facade for Residents"""
    
    def __init__(self, repository: ResidentsRepository = None):
        self.repository = repository or ResidentsCmdRepositoryImpl()

    def create(self, schema: CreateResidentsSchema) -> Residents:
        return self.repository.create(schema.model_dump())

    def update(self, id: int, schema: UpdateResidentsSchema) -> Residents:
        return self.repository.update(id, schema.model_dump(exclude_unset=True))

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def get_all(self) -> List[Residents]:
        return self.repository.all()

    def get_by_id(self, id: int) -> Residents:
        return self.repository.get_by_id(id)

    def get_by_user(self, user_id: int) -> List[Residents]:
        return self.repository.get_by_user(user_id)

    def get_by_unity(self, unity_id: int) -> List[Residents]:
        return self.repository.get_by_unity(unity_id)


def create_residents_usecase() -> ResidentsUseCase:
    return ResidentsUseCase()
