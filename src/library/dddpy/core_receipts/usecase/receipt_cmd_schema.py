"""
Receipt command schemas — Pydantic models for API request bodies.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateReceiptSchema(BaseModel):
    """Schema for internal receipt creation (usually called by payment service)."""
    condominium_id: int
    unit_id: int
    ar_id: int
    receipt_number: str
    issued_at: datetime
    payer_user_id: int
    amount_paid: float = Field(..., gt=0)
    payment_method: str = Field(..., description="cash/bank_transfer/yape/plin/card/other")
    reference: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None)
