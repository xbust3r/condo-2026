"""
LedgerEntry data classes — DDD data layer.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CreateLedgerEntryData:
    """Data required to create a ledger entry."""
    condominium_id: int
    unit_id: int
    entry_type: str  # charge/payment/adjustment/balance_forward
    ar_id: Optional[int] = None
    payment_id: Optional[int] = None
    charge_id: Optional[int] = None
    description: str = ""
    debit: Decimal = Decimal("0.00")
    credit: Decimal = Decimal("0.00")
    period: Optional[str] = None
    reference: Optional[str] = None
