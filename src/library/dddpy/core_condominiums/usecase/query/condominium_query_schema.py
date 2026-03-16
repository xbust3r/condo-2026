# Condominium Query Schemas (Read)
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CondominiumQuerySchema(BaseModel):
    """Schema for reading/returning a condominium"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    code: str
    description: Optional[str]
    size: Optional[float]
    percentage: Optional[float]
    status: int
    created_at: datetime
    updated_at: datetime


class CondominiumListQuerySchema(BaseModel):
    """Schema for listing condominiums"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    code: str
    status: int
