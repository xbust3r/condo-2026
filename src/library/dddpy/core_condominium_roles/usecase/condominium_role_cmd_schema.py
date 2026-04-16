from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date


_VALID_ROLES = {
    "super_admin",
    "condominium_admin",
    "board_member",
    "finance_reviewer",
    "security_staff",
    "maintenance_staff",
    "operations_staff",
}
_VALID_STATUSES = {"active", "inactive", "historical"}
_VALID_SCOPES = {"condominium", "unit", "building"}


class CreateCondominiumRoleSchema(BaseModel):
    condominium_id: int = Field(..., description="ID of the parent condominium")
    user_id: int = Field(..., description="ID of the user")
    role: str = Field(
        ...,
        max_length=40,
        description="Role: super_admin | condominium_admin | board_member | finance_reviewer | security_staff | maintenance_staff | operations_staff",
    )
    status: str = Field("active", description="Status: active|inactive|historical")
    scope: str = Field(
        "condominium",
        description="Scope: condominium | unit | building (default: condominium)",
    )
    building_id: Optional[int] = Field(
        None,
        description="Building ID for building-scoped roles (maintenance_staff, operations_staff)",
    )
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

    @validator("scope")
    def validate_scope(cls, value):
        if value not in _VALID_SCOPES:
            raise ValueError(
                f"scope must be one of: {', '.join(sorted(_VALID_SCOPES))}"
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
    scope: Optional[str] = Field(None)
    building_id: Optional[int] = Field(None)
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

    @validator("scope")
    def validate_scope(cls, value):
        if value is not None and value not in _VALID_SCOPES:
            raise ValueError(
                f"scope must be one of: {', '.join(sorted(_VALID_SCOPES))}"
            )
        return value
