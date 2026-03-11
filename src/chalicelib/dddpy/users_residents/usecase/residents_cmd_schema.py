from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateResidentSchema(BaseModel):
    condominium_id: Optional[int] = None
    building_id: Optional[int] = None
    unity_id: Optional[int] = None
    type: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field("active", max_length=50)
    user_id: Optional[int] = None


class UpdateResidentSchema(BaseModel):
    condominium_id: Optional[int] = None
    building_id: Optional[int] = None
    unity_id: Optional[int] = None
    type: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=50)
    user_id: Optional[int] = None


class ResidentResponseSchema(BaseModel):
    id: int
    condominium_id: Optional[int]
    building_id: Optional[int]
    unity_id: Optional[int]
    type: Optional[str]
    status: Optional[str]
    user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
