from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class CreateUnitOccupancyData:
    """Data required to create a new unit occupancy record."""
    unit_id: int
    user_id: int
    occupancy_type: str
    status: str
    start_date: date
    end_date: Optional[date] = None
    is_primary: bool = False
    authorized_by_user_id: Optional[int] = None
    notes: Optional[str] = None


@dataclass(frozen=True)
class UpdateUnitOccupancyData:
    """Data required to update an existing unit occupancy record."""
    occupancy_type: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_primary: Optional[bool] = None
    authorized_by_user_id: Optional[int] = None
    notes: Optional[str] = None
