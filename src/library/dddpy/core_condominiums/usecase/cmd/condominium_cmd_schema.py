# Condominium Command Schemas (Write)
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CreateCondominiumCmdSchema(BaseModel):
    """Schema for creating a condominium"""
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    size: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    status: int = Field(default=1, ge=0, le=2)


class UpdateCondominiumCmdSchema(BaseModel):
    """Schema for updating a condominium"""
    model_config = ConfigDict(from_attributes=True)
    
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    size: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    status: Optional[int] = Field(None, ge=0, le=2)
