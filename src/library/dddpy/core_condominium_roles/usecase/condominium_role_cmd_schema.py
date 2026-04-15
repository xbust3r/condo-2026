from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date


_VALID_ROLES = {"super_admin", "condominium_admin", "building_manager", "security_staff", "maintenance_staff", "support_staff"}
_VALID_STATUSES = {"active", "inactive", "historical"}


class CreateCondominiumRoleSchema(BaseModel):
    condominium_id: int = Field(..., description="ID of the parent condominium")
    user_id: int = Field(..., description="ID of the user")
    role: str = Field(
        ...,
        max_length=40,
        description="Role: super_admin|condominium_admin|building_manager|security_staff|maintenance_staff|support_staff",
    )
    status: str = Field("active", description="Status: active|inactive|historical")
    start_date: Optional[date] = Field(None, description="Start date of the role assignment")
    end_date: Optional[date] = Field(None, description="End date of the role assignment (nullable)")

    @validator("role")
    def validate_role(cls, value):
        if value not in _VALID_ROLES:
            raise ValueError(
                f"role must be one of: {', '.join(sorted(_VALID_ROLES))}"
            )
        return value

    @validator("status")
    def validate_status(cls, value):
        if value not in _VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(_VALID_STATUSES))}"
            )
        return value

    @validator("end_date")
    def validate_end_date(cls, value, values):
        start = values.get("start_date")
        if value is not None and start is not None and value < start:
            raise ValueError("end_date cannot be before start_date")
        return value


class UpdateCondominiumRoleSchema(BaseModel):
    role: Optional[str] = Field(None, max_length=40)
    status: Optional[str] = Field(None)
    end_date: Optional[date] = Field(None)

    @validator("role")
    def validate_role(cls, value):
        if value is not None and value not in _VALID_ROLES:
            raise ValueError(
                f"role must be one of: {', '.join(sorted(_VALID_ROLES))}"
            )
        return value

    @validator("status")
    def validate_status(cls, value):
        if value is not None and value not in _VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(_VALID_STATUSES))}"
            )
        return value
