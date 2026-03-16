# Unitys Schemas and Use Cases
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from library.dddpy.core_unitys.domain.unitys import Unitys, UnitysRepository
from library.dddpy.core_unitys.infrastructure.unitys import UnitysCmdRepositoryImpl


class CreateUnitysSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    size: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    type: Optional[str] = Field(None, max_length=100)
    floor: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    building_id: int
    unity_type_id: Optional[int] = None
    status: int = Field(default=1, ge=0, le=2)


class UpdateUnitysSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    size: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    type: Optional[str] = Field(None, max_length=100)
    floor: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    building_id: Optional[int] = None
    unity_type_id: Optional[int] = None
    status: Optional[int] = Field(None, ge=0, le=2)


class UnitysUseCase:
    """Facade for Unitys"""
    
    def __init__(self, repository: UnitysRepository = None):
        self.repository = repository or UnitysCmdRepositoryImpl()

    def create(self, schema: CreateUnitysSchema) -> Unitys:
        return self.repository.create(schema.model_dump())

    def update(self, id: int, schema: UpdateUnitysSchema) -> Unitys:
        return self.repository.update(id, schema.model_dump(exclude_unset=True))

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def get_all(self) -> List[Unitys]:
        return self.repository.all()

    def get_by_id(self, id: int) -> Unitys:
        return self.repository.get_by_id(id)

    def get_by_code(self, code: str) -> Unitys:
        return self.repository.get_by_code(code)

    def get_by_building(self, building_id: int) -> List[Unitys]:
        return self.repository.get_by_building(building_id)


def create_unitys_usecase() -> UnitysUseCase:
    return UnitysUseCase()
