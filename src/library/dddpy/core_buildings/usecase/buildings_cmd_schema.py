# Buildings Command Schemas
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CreateBuildingsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    size: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    type: Optional[str] = Field(None, max_length=100)
    condominium_id: int
    building_type_id: Optional[int] = None
    status: int = Field(default=1, ge=0, le=2)


class UpdateBuildingsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    size: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    type: Optional[str] = Field(None, max_length=100)
    condominium_id: Optional[int] = None
    building_type_id: Optional[int] = None
    status: Optional[int] = Field(None, ge=0, le=2)


class BuildingsResponseSchema(BaseModel):
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
