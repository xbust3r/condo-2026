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


class ForgotPasswordSchema(BaseModel):
    email: EmailStr = Field(..., description="Account email address")


class ResetPasswordSchema(BaseModel):
    token: str = Field(..., min_length=1, description="Password reset JWT token")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")



class VerifyEmailSchema(BaseModel):
    token: str = Field(..., min_length=1, description="Email verification JWT token")


class ChangePasswordSchema(BaseModel):
    current_password: str = Field(..., min_length=1, description="Current password to verify")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password (min 8 chars)")

