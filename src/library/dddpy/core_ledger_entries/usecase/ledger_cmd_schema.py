"""
from typing import Optional
Ledger command schemas — Pydantic models for API request bodies.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CreateLedgerEntrySchema(BaseModel):
    unit_id: int = Field(..., description="Unit ID")
    entry_type: str = Field(
        ...,
        description="charge | payment | adjustment | balance_forward",
    )
    ar_id: Optional[int] = Field(None, description="Accounts receivable ID (for charge/payment)")
    payment_id: Optional[int] = Field(None, description="Payment ID (for payment entries)")
    charge_id: Optional[int] = Field(None, description="Charge ID (for charge entries)")
    description: str = Field(..., max_length=500, description="Entry description")
    debit: float = Field(0.0, ge=0, description="Debit amount (increases balance)")
    credit: float = Field(0.0, ge=0, description="Credit amount (decreases balance)")
    period: Optional[str] = Field(None, regex=r"^\d{4}-\d{2}$", description="Period YYYY-MM")
    reference: Optional[str] = Field(None, max_length=100)
