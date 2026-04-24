"""
from typing import Optional
ChargeType command schemas — Pydantic models for API request bodies.
"""
from pydantic import BaseModel, Field
from typing import Optional


class CreateChargeTypeSchema(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Machine-readable code (e.g. monthly_fee, special_assessment)",
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Human-readable name",
    )
    description: Optional[str] = Field(None, description="Optional description")
    is_global: bool = Field(
        True,
        description="Whether this charge type applies to all units (global) or is unit-specific",
    )
    is_active: bool = Field(True, description="Whether this type is active")
    sort_order: int = Field(0, ge=0, description="Display sort order")


class UpdateChargeTypeSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None)
    is_global: Optional[bool] = Field(None)
    is_active: Optional[bool] = Field(None)
    sort_order: Optional[int] = Field(None, ge=0)
