from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CreateUnitysCmdSchema(BaseModel):
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

class UpdateUnitysCmdSchema(BaseModel):
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
