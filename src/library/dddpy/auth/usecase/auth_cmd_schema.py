"""
Auth use case schemas (Pydantic input models).
"""
from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=1, description="User password")


class RefreshSchema(BaseModel):
    refresh_token: str = Field(..., min_length=1, description="UUID refresh token")


class LogoutSchema(BaseModel):
    refresh_token: str = Field(..., min_length=1, description="UUID refresh token to revoke")
