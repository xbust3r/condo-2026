from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UnitysQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    code: str
    description: Optional[str]
    size: Optional[float]
    percentage: Optional[float]
    type: Optional[str]
    floor: Optional[int]
    unit: Optional[str]
    building_id: int
    unity_type_id: Optional[int]
    status: int
    created_at: datetime
    updated_at: datetime

class UnitysListQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    code: str
    building_id: int
    status: int
