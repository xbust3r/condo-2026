from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, Any
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
    unit_id: Optional[int] = Field(
        None,
        description="Unit ID for unit-scoped roles",
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

    # Cross-field validators (run after individual field validators)
    @root_validator(skip_on_failure=True)
    def validate_end_date_after_start(cls, values):
        if values.get('end_date') is not None and values.get('start_date') is not None:
            if values.get('end_date') < values.get('start_date'):
                raise ValueError("end_date cannot be before start_date")
        return values

    @root_validator(skip_on_failure=True)
    def validate_historical_requires_end_date(cls, values):
        """Historical roles must have an end_date set."""
        if values.get('status') == "historical" and values.get('end_date') is None:
            raise ValueError("end_date is required when status is 'historical'")
        return values

    @root_validator(skip_on_failure=True)
    def validate_scope_building_requires_building_id(cls, values):
        """Scope 'building' requires building_id."""
        if values.get('scope') == "building" and values.get('building_id') is None:
            raise ValueError("building_id is required when scope is 'building'")
        return values

    @root_validator(skip_on_failure=True)
    def validate_scope_unit_requires_unit_id(cls, values):
        """Scope 'unit' requires unit_id."""
        if values.get('scope') == "unit" and values.get('unit_id') is None:
            raise ValueError("unit_id is required when scope is 'unit'")
        return values


class UpdateCondominiumRoleSchema(BaseModel):
    role: Optional[str] = Field(None, max_length=40)
    status: Optional[str] = Field(None)
    scope: Optional[str] = Field(None)
    building_id: Optional[int] = Field(None)
    unit_id: Optional[int] = Field(None)
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

    @root_validator(skip_on_failure=True)
    def validate_scope_building_requires_building_id(cls, values):
        if values.get('scope') == "building" and values.get('building_id') is None:
            raise ValueError("building_id is required when scope is 'building'")
        return values

    @root_validator(skip_on_failure=True)
    def validate_scope_unit_requires_unit_id(cls, values):
        if values.get('scope') == "unit" and values.get('unit_id') is None:
            raise ValueError("unit_id is required when scope is 'unit'")
        return values

    @root_validator(skip_on_failure=True)
    def validate_status_historical_requires_end_date(cls, values):
        """For update, we can only validate end_date requirement when status is being set to historical AND end_date not provided."""
        if values.get('status') == "historical" and values.get('end_date') is None:
            raise ValueError("end_date is required when status is set to 'historical'")
        return values