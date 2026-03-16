from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional

class CreateUsersCmdSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    email: EmailStr
    password: Optional[str] = Field(None, min_length=6)
    doc_identity: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    status: int = Field(default=1, ge=0, le=2)

class UpdateUsersCmdSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    doc_identity: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    status: Optional[int] = Field(None, ge=0, le=2)
