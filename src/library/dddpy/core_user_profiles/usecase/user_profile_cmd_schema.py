"""
User profile command schemas — Pydantic models for API request bodies.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CreateUserProfileSchema(BaseModel):
    user_id: int = Field(..., description="ID of the user this profile belongs to")
    first_name: Optional[str] = Field(None, max_length=255, description="First name")
    last_name: Optional[str] = Field(None, max_length=255, description="Last name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    document_type: Optional[str] = Field(None, max_length=20, description="Document type: DNI|PASAPORTE|CEDULA")
    document_number: Optional[str] = Field(None, max_length=50, description="Document number")
    birth_date: Optional[date] = Field(None, description="Birth date (YYYY-MM-DD)")


class UpdateUserProfileSchema(BaseModel):
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    document_type: Optional[str] = Field(None, max_length=20)
    document_number: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[date] = Field(None)
