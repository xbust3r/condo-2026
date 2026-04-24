"""
from typing import Optional
Payment command schemas — Pydantic models for API request bodies.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreatePaymentSchema(BaseModel):
    ar_id: int = Field(..., description="Accounts receivable ID to pay")
    payer_user_id: int = Field(..., description="User making the payment")
    amount: float = Field(..., gt=0, description="Payment amount (must be > 0 and ≤ pending)")
    payment_method: str = Field(
        ...,
        description="cash/bank_transfer/yape/plin/card/other"
    )
    reference: Optional[str] = Field(None, max_length=100, description="Payment reference/number")
    paid_at: datetime = Field(default_factory=datetime.utcnow, description="Payment timestamp")
