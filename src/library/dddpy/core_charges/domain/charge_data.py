"""
Charge data classes — DDD data layer.
"""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CreateChargeData:
    """Data required to create a charge."""
    condominium_id: int
    charge_type_id: int
    scope: str = "unit"
    unit_id: Optional[int] = None
    building_id: Optional[int] = None
    distribution_mode: str = "fixed_unit_amount"
    description: Optional[str] = None
    amount: Decimal = Decimal("0.00")
    currency: str = "PEN"
    is_recurrent: bool = False
    period_pattern: Optional[str] = None  # 'YYYY-MM'
    start_date: date = None
    end_date: Optional[date] = None
    status: str = "active"


@dataclass(frozen=True)
class UpdateChargeData:
    """Data required to update a charge."""
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    distribution_mode: Optional[str] = None
    scope: Optional[str] = None
    unit_id: Optional[int] = None
    building_id: Optional[int] = None
    is_recurrent: Optional[bool] = None
    period_pattern: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
