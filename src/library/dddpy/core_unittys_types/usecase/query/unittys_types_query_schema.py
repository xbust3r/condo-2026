from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UnittysTypesQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    code: str
    description: Optional[str]
    status: int
    created_at: datetime
    updated_at: datetime

class UnittysTypesListQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    code: str
    status: int
