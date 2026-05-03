"""
Booking command schemas — Pydantic input models.
"""
from typing import Optional
from datetime import datetime, date

from pydantic import BaseModel, Field, root_validator


class CreateBookingSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    building_id: int = Field(..., description="Building ID")
    amenity_id: int = Field(..., description="Amenity ID")
    unit_id: int = Field(..., description="Unit ID")
    owner_id: int = Field(..., description="Owner user ID")
    booking_date: date = Field(..., description="Booking date")
    start_at: datetime = Field(..., description="Start datetime")
    end_at: datetime = Field(..., description="End datetime")
    notes: Optional[str] = Field(None, description="Optional notes")

    @root_validator(skip_on_failure=True)
    def validate_dates(cls, values):
        start = values.get('start_at')
        end = values.get('end_at')
        if start and end and start >= end:
            raise ValueError("start_at must be before end_at")
        return values


class UpdateBookingSchema(BaseModel):
    start_at: Optional[datetime] = Field(None)
    end_at: Optional[datetime] = Field(None)
    notes: Optional[str] = Field(None)

    @root_validator(skip_on_failure=True)
    def validate_dates(cls, values):
        start = values.get('start_at')
        end = values.get('end_at')
        if start and end and start >= end:
            raise ValueError("start_at must be before end_at")
        return values


class ConfirmBookingSchema(BaseModel):
    """Confirm a booking — generates ARs for fee and deposit."""
    pass


class CancelBookingSchema(BaseModel):
    reason: Optional[str] = Field(None, description="Cancellation reason")


class DepositActionSchema(BaseModel):
    """Apply a deposit movement: return | partial_apply | full_apply"""
    action: str = Field(..., description="return | partial_apply | full_apply")
    amount: float = Field(..., gt=0, description="Amount to apply")
    notes: Optional[str] = Field(None)
