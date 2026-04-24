"""
AccountsReceivable data classes — DDD data layer.
"""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CreateARData:
    """Data required to create an accounts receivable entry."""
    condominium_id: int
    unit_id: int
    debtor_user_id: int
    reference_code: Optional[str] = None
    description: Optional[str] = None
    amount: Decimal = Decimal("0.00")
    currency: str = "PEN"
    due_date: date = None
    period: Optional[str] = None  # 'YYYY-MM'
    charge_id: Optional[int] = None


@dataclass(frozen=True)
class UpdateARData:
    """Data required to update an AR entry (admin adjustments)."""
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


@dataclass(frozen=True)
class RecordPaymentData:
    """Data required to record a payment against an AR."""
    amount: Decimal  # amount being paid
    payment_method: str
    reference: Optional[str] = None
    paid_by_user_id: Optional[int] = None
