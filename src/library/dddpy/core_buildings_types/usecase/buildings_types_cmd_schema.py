# Buildings Types Command Schemas
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CreateBuildingsTypesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    status: int = Field(default=1, ge=0, le=2)


class UpdateBuildingsTypesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    status: Optional[int] = Field(None, ge=0, le=2)


class BuildingsTypesResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    code: str
    description: Optional[str]
    status: int
    created_at: datetime
    updated_at: datetime
