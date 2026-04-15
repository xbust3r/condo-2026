from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date


_VALID_OWNERSHIP_TYPES = {"owner", "co_owner"}
_VALID_STATUSES = {"active", "inactive", "historical"}


class CreateUnitOwnershipSchema(BaseModel):
    unit_id: int = Field(..., description="ID of the unit")
    user_id: int = Field(..., description="ID of the user")
    ownership_type: str = Field(
        ...,
        description="Ownership type: owner or co_owner",
    )
    ownership_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Ownership percentage 0-100",
    )
    start_date: date = Field(..., description="Start date of ownership")
    end_date: Optional[date] = Field(
        None,
        description="End date of ownership (optional, for historical records)",
    )
    notes: Optional[str] = Field(None, description="Administrative notes")

    @validator("ownership_type")
    def validate_ownership_type(cls, value):
        if value not in _VALID_OWNERSHIP_TYPES:
            raise ValueError(
                f"ownership_type must be one of: {', '.join(sorted(_VALID_OWNERSHIP_TYPES))}"
            )
        return value


class UpdateUnitOwnershipSchema(BaseModel):
    ownership_type: Optional[str] = Field(
        None,
        description="Ownership type: owner or co_owner",
    )
    ownership_percentage: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Ownership percentage 0-100",
    )
    status: Optional[str] = Field(
        None,
        description="Status: active, inactive, or historical",
    )
    start_date: Optional[date] = Field(None, description="Start date of ownership")
    end_date: Optional[date] = Field(None, description="End date of ownership")
    notes: Optional[str] = Field(None, description="Administrative notes")

    @validator("ownership_type")
    def validate_ownership_type(cls, value):
        if value is not None and value not in _VALID_OWNERSHIP_TYPES:
            raise ValueError(
                f"ownership_type must be one of: {', '.join(sorted(_VALID_OWNERSHIP_TYPES))}"
            )
        return value

    @validator("status")
    def validate_status(cls, value):
        if value is not None and value not in _VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(_VALID_STATUSES))}"
            )
        return value
