from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CreateUnitOwnershipData:
    """Data required to create a new unit ownership record."""
    unit_id: int
    user_id: int
    ownership_type: str
    ownership_percentage: Decimal
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = None


@dataclass(frozen=True)
class UpdateUnitOwnershipData:
    """Data required to update an existing unit ownership record."""
    ownership_type: Optional[str] = None
    ownership_percentage: Optional[Decimal] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None
