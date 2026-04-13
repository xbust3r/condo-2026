from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from decimal import Decimal


class CreateCondominiumSchema(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None)
    land_area: Optional[float] = Field(None, ge=0)
    built_area: Optional[float] = Field(None, ge=0)
    area_unit: Optional[str] = Field('m2', max_length=20)
    legal_name: Optional[str] = Field(None, max_length=255)
    document_number: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    contact_email: Optional[EmailStr] = Field(None)
    contact_phone: Optional[str] = Field(None, max_length=50)


class UpdateCondominiumSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None)
    land_area: Optional[float] = Field(None, ge=0)
    built_area: Optional[float] = Field(None, ge=0)
    area_unit: Optional[str] = Field(None, max_length=20)
    legal_name: Optional[str] = Field(None, max_length=255)
    document_number: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    contact_email: Optional[EmailStr] = Field(None)
    contact_phone: Optional[str] = Field(None, max_length=50)
    status: Optional[int] = Field(None, ge=0)
