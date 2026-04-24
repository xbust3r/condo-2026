"""
from typing import Optional
OccupancyType data classes — DDD data layer.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateOccupancyTypeData:
    """Data required to create an occupancy type."""
    code: str
    name: str
    description: Optional[str] = None
    scope: str = "system"
    condominium_id: Optional[int] = None
    requires_authorization: bool = False
    allows_primary: bool = True
    is_active: bool = True
    sort_order: int = 0


@dataclass(frozen=True)
class UpdateOccupancyTypeData:
    """Data required to update an occupancy type."""
    name: Optional[str] = None
    description: Optional[str] = None
    scope: Optional[str] = None
    condominium_id: Optional[int] = None
    requires_authorization: Optional[bool] = None
    allows_primary: Optional[bool] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None