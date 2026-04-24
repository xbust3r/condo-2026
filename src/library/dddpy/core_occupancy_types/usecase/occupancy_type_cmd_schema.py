"""
from typing import Optional
OccupancyType command schemas — Pydantic models for API request bodies.
"""
from pydantic import BaseModel, Field
from typing import Optional


class CreateOccupancyTypeSchema(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Machine-readable code (e.g. tenant, resident_owner)",
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Human-readable name (e.g. Inquilino, Propietario Residente)",
    )
    description: Optional[str] = Field(None, description="Optional description")
    scope: str = Field(
        "system",
        description="Scope: system (global) or condominium (custom per building)",
    )
    condominium_id: Optional[int] = Field(
        None,
        description="Required when scope=condominium. ID of the parent condominium.",
    )
    requires_authorization: bool = Field(
        False,
        description="Whether this type requires authorization by an owner",
    )
    allows_primary: bool = Field(
        True,
        description="Whether this type can be assigned as primary occupancy",
    )
    is_active: bool = Field(True, description="Whether this type is active")
    sort_order: int = Field(0, ge=0, description="Display sort order")


class UpdateOccupancyTypeSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None)
    scope: Optional[str] = Field(None, description="Scope: system or condominium")
    condominium_id: Optional[int] = Field(None)
    requires_authorization: Optional[bool] = Field(None)
    allows_primary: Optional[bool] = Field(None)
    is_active: Optional[bool] = Field(None)
    sort_order: Optional[int] = Field(None, ge=0)