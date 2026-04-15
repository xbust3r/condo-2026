"""
User command schemas — Pydantic models for API request bodies.
"""
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional


_VALID_STATUSES = {"active", "pending", "suspended", "inactive", "locked"}


class CreateUserSchema(BaseModel):
    email: EmailStr = Field(..., description="Unique email address")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    status: Optional[str] = Field("active", description="Initial status")


class UpdateUserSchema(BaseModel):
    email: Optional[EmailStr] = Field(None, description="New email address")
    status: Optional[str] = Field(None, description="New status: active|pending|suspended|inactive")

    @validator("status")
    def validate_status(cls, value):
        if value is not None and value not in _VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(_VALID_STATUSES))}"
            )
        return value
