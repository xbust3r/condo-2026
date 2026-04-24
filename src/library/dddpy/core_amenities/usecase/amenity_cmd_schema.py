"""
Amenity command schemas — Pydantic input models.
"""
from typing import Optional

from pydantic import BaseModel, Field


class CreateAmenitySchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    name: str = Field(..., min_length=3, max_length=200, description="Amenity name (min 3 chars)")
    description: Optional[str] = Field(None, description="Description of the amenity")
    location: Optional[str] = Field(None, max_length=255, description="Location within the property")
    max_capacity: int = Field(1, ge=1, description="Maximum capacity")
    booking_duration_min: int = Field(60, ge=15, description="Default booking duration in minutes")
    requires_approval: bool = Field(False, description="Whether booking requires approval")


class UpdateAmenitySchema(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None)
    location: Optional[str] = Field(None, max_length=255)
    max_capacity: Optional[int] = Field(None, ge=1)
    booking_duration_min: Optional[int] = Field(None, ge=15)
    requires_approval: Optional[bool] = Field(None)
    status: Optional[str] = Field(None)
