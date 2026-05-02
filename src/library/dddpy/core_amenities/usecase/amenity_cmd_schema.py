"""
Amenity command schemas — Pydantic input models.

Supports scope-aware creation:
- scope=CONDOMINIUM → building_id not allowed
- scope=BUILDING → building_id required
"""
from typing import Optional

from pydantic import BaseModel, Field, root_validator


class CreateAmenitySchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    name: str = Field(..., min_length=3, max_length=200, description="Amenity name (min 3 chars)")
    description: Optional[str] = Field(None, description="Description of the amenity")
    location: Optional[str] = Field(None, max_length=255, description="Location within the property")
    max_capacity: int = Field(1, ge=1, description="Maximum capacity")
    booking_duration_min: int = Field(60, ge=15, description="Default booking duration in minutes")
    requires_approval: bool = Field(False, description="Whether booking requires approval")
    scope: str = Field('CONDOMINIUM', description="Scope: CONDOMINIUM or BUILDING")
    building_id: Optional[int] = Field(None, description="Building ID (required when scope=BUILDING)")

    @root_validator(skip_on_failure=True)
    def validate_scope_consistency(cls, values):
        scope = values.get("scope", "CONDOMINIUM")
        building_id = values.get("building_id")
        if scope == "CONDOMINIUM" and building_id is not None:
            raise ValueError("scope=CONDOMINIUM requires building_id=None (do not send building_id)")
        if scope == "BUILDING" and building_id is None:
            raise ValueError("scope=BUILDING requires building_id")
        if scope not in ("CONDOMINIUM", "BUILDING"):
            raise ValueError("scope must be CONDOMINIUM or BUILDING")
        return values


class UpdateAmenitySchema(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None)
    location: Optional[str] = Field(None, max_length=255)
    max_capacity: Optional[int] = Field(None, ge=1)
    booking_duration_min: Optional[int] = Field(None, ge=15)
    requires_approval: Optional[bool] = Field(None)
    scope: Optional[str] = Field(None)
    building_id: Optional[int] = Field(None)
    status: Optional[str] = Field(None)

    @root_validator(skip_on_failure=True)
    def validate_scope_consistency(cls, values):
        scope = values.get("scope")
        building_id = values.get("building_id")
        if scope is not None:
            if scope not in ("CONDOMINIUM", "BUILDING"):
                raise ValueError("scope must be CONDOMINIUM or BUILDING")
            if scope == "CONDOMINIUM" and building_id is not None:
                raise ValueError("scope=CONDOMINIUM requires building_id=None")
            if scope == "BUILDING" and building_id is None:
                raise ValueError("scope=BUILDING requires building_id")
        return values
