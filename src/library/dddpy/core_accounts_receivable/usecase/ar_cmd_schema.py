"""
from typing import Optional
AccountsReceivable command schemas — Pydantic models for API request bodies.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CreateARSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    unit_id: int = Field(..., description="Unit ID")
    debtor_user_id: int = Field(..., description="Debtor user ID")
    reference_code: Optional[str] = Field(None, max_length=50, description="Internal reference code")
    description: Optional[str] = Field(None, description="AR description")
    amount: float = Field(..., gt=0, description="Total amount (must be > 0)")
    currency: str = Field("PEN", max_length=3)
    due_date: date = Field(..., description="Due date")
    period: Optional[str] = Field(None, max_length=7, pattern=r"^\d{4}-\d{2}$")
    charge_id: Optional[int] = Field(None, description="Related charge ID (if any)")


class CreateARBatchSchema(BaseModel):
    """Generate AR entries for all active units in a charge (global charge)."""
    charge_id: int = Field(..., description="Charge ID to generate AR from")
    due_date: date = Field(..., description="Due date for all AR entries")
    period: Optional[str] = Field(None, max_length=7, pattern=r"^\d{4}-\d{2}$")


class UpdateARSchema(BaseModel):
    description: Optional[str] = Field(None)
    due_date: Optional[date] = Field(None)
    status: Optional[str] = Field(None, description="Status: pending/partial/paid/overdue/cancelled")


class RecordPaymentSchema(BaseModel):
    amount: float = Field(..., gt=0, description="Payment amount (must be > 0)")
    payment_method: str = Field(..., description="cash/bank_transfer/yape/plin/card/other")
    reference: Optional[str] = Field(None, max_length=100)
    paid_by_user_id: Optional[int] = Field(None, description="User making the payment")
