from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateCondominiumSchema(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    size: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)


class UpdateCondominiumSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    size: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)


class CondominiumResponseSchema(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    size: Optional[float]
    percentage: Optional[float]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
