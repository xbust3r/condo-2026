from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ResidentsQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    condominium_id: int
    building_id: int
    unity_id: int
    user_id: int
    type: str
    status: int
    created_at: datetime
    updated_at: datetime

class ResidentsListQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    condominium_id: int
    building_id: int
    unity_id: int
    user_id: int
    type: str
    status: int
