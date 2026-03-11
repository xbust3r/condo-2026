from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateUnitySchema(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    size: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    type: Optional[str] = Field(None, max_length=100)
    floor: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    building_id: Optional[int] = None
    unity_type_id: Optional[int] = None


class UpdateUnitySchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    size: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    type: Optional[str] = Field(None, max_length=100)
    floor: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    building_id: Optional[int] = None
    unity_type_id: Optional[int] = None


class UnityResponseSchema(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    size: Optional[float]
    percentage: Optional[float]
    type: Optional[str]
    floor: Optional[int]
    unit: Optional[str]
    building_id: Optional[int]
    unity_type_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
