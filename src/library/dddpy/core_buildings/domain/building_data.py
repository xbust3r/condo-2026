from typing import Optional
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass(frozen=True)
class CreateBuildingData:
    """Data required to create a new building."""
    condominium_id: int
    code: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    building_type_id: Optional[int] = None
    built_area: Optional[Decimal] = None
    common_area: Optional[Decimal] = None
    coefficient: Optional[Decimal] = None
    floors_count: int = 0
    basements_count: int = 0
    units_planned: int = 0
    sort_order: int = 0


@dataclass(frozen=True)
class UpdateBuildingData:
    """Data required to update an existing building."""
    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    building_type_id: Optional[int] = None
    built_area: Optional[Decimal] = None
    common_area: Optional[Decimal] = None
    coefficient: Optional[Decimal] = None
    floors_count: Optional[int] = None
    basements_count: Optional[int] = None
    units_planned: Optional[int] = None
    sort_order: Optional[int] = None
    status: Optional[int] = None