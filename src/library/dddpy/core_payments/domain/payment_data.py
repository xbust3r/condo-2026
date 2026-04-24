"""
Payment data classes — DDD data layer.
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CreatePaymentData:
    """Data required to register a payment."""
    condominium_id: int
    unit_id: int
    ar_id: int
    payer_user_id: int
    amount: Decimal
    payment_method: str
    reference: Optional[str] = None
    paid_at: datetime = None
