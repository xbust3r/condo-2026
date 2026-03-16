# Buildings Query Schemas (Read)
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class BuildingsQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    code: str
    description: Optional[str]
    size: Optional[float]
    percentage: Optional[float]
    type: Optional[str]
    condominium_id: int
    building_type_id: Optional[int]
    status: int
    created_at: datetime
    updated_at: datetime


class BuildingsListQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    code: str
    condominium_id: int
    status: int
