"""
Charge command schemas — Pydantic models for API request bodies.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CreateChargeSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    charge_type_id: int = Field(..., description="Charge type FK")
    unit_id: Optional[int] = Field(None, description="Unit ID (null = global charge)")
    description: Optional[str] = Field(None, description="Charge description")
    amount: float = Field(..., gt=0, description="Charge amount (must be > 0)")
    currency: str = Field("PEN", max_length=3, description="Currency code")
    is_recurrent: bool = Field(False, description="Whether this charge recurs monthly")
    period_pattern: Optional[str] = Field(
        None,
        max_length=7,
        pattern=r"^\d{4}-\d{2}$",
        description="Period pattern YYYY-MM (required if is_recurrent=True)",
    )
    start_date: date = Field(..., description="Charge start date")
    end_date: Optional[date] = Field(None, description="Charge end date (null = indefinite)")
    status: str = Field("active", description="Status: active/inactive/expired")


class UpdateChargeSchema(BaseModel):
    description: Optional[str] = Field(None)
    amount: Optional[float] = Field(None, gt=0)
    is_recurrent: Optional[bool] = Field(None)
    period_pattern: Optional[str] = Field(None, max_length=7, pattern=r"^\d{4}-\d{2}$")
    start_date: Optional[date] = Field(None)
    end_date: Optional[date] = Field(None)
    status: Optional[str] = Field(None, description="Status: active/inactive/expired")
