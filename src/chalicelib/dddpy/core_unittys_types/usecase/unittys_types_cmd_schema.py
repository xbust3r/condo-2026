from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateUnityTypeSchema(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None


class UpdateUnityTypeSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None


class UnityTypeResponseSchema(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
