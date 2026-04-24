"""Package command schemas — Pydantic input models."""
from typing import Optional

from pydantic import BaseModel, Field


class CreatePackageSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    unit_id: int = Field(..., description="Unit ID of the recipient")
    recipient_user_id: int = Field(..., description="Recipient user ID")
    carrier: Optional[str] = Field(None, max_length=100, description="Courier name")
    tracking_number: Optional[str] = Field(None, max_length=100, description="Tracking number")
    description: Optional[str] = Field(None, description="Package description")


class UpdatePackageSchema(BaseModel):
    status: Optional[str] = Field(None, description="Status: pending, with_concierge, delivered, cancelled")
    carrier: Optional[str] = Field(None, max_length=100)
    tracking_number: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)


class DeliverPackageSchema(BaseModel):
    pickup_code: str = Field(..., min_length=4, max_length=4, description="4-digit pickup code for verification")
