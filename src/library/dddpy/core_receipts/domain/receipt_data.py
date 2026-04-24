"""
Receipt data classes — DDD data layer.
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CreateReceiptData:
    """Data required to create a receipt."""
    condominium_id: int
    unit_id: int
    ar_id: int
    receipt_number: str
    issued_at: datetime
    payer_user_id: int
    amount_paid: Decimal
    payment_method: str
    reference: Optional[str] = None
    notes: Optional[str] = None
