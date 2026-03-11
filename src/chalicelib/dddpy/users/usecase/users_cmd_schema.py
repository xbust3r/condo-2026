from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class CreateUserSchema(BaseModel):
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    email: EmailStr
    password: Optional[str] = Field(None, max_length=255)
    doc_identity: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = Field("active", max_length=50)


class UpdateUserSchema(BaseModel):
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, max_length=255)
    doc_identity: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = Field(None, max_length=50)


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    doc_identity: Optional[str]
    phone: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
