# Unity Types Schemas and Use Cases
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from library.dddpy.core_unittys_types.domain.unittys_types import (
    UnittysTypes,
    UnittysTypesRepository,
)
from library.dddpy.core_unittys_types.infrastructure.unittys_types_cmd_repository import (
    UnittysTypesCmdRepositoryImpl,
)


class CreateUnittysTypesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    status: int = Field(default=1, ge=0, le=2)


class UpdateUnittysTypesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    status: Optional[int] = Field(None, ge=0, le=2)


class UnittysTypesUseCase:
    """Facade for Unity Types"""
    
    def __init__(self, repository: UnittysTypesRepository = None):
        self.repository = repository or UnittysTypesCmdRepositoryImpl()

    def create(self, schema: CreateUnittysTypesSchema) -> UnittysTypes:
        return self.repository.create(schema.model_dump())

    def update(self, id: int, schema: UpdateUnittysTypesSchema) -> UnittysTypes:
        return self.repository.update(id, schema.model_dump(exclude_unset=True))

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def get_all(self) -> List[UnittysTypes]:
        return self.repository.all()

    def get_by_id(self, id: int) -> UnittysTypes:
        return self.repository.get_by_id(id)

    def get_by_code(self, code: str) -> UnittysTypes:
        return self.repository.get_by_code(code)


def create_unittys_types_usecase() -> UnittysTypesUseCase:
    return UnittysTypesUseCase()
