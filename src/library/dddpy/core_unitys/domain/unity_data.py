from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass(frozen=True)
class CreateUnityData:
    """Data required to create a new unity."""
    building_id: int
    unit_number: str
    unity_type_id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    private_area: Optional[Decimal] = None
    coefficient: Optional[Decimal] = None
    floor_number: Optional[int] = None
    floor_label: Optional[str] = None
    occupancy_status: str = "vacant"
    sort_order: int = 0


@dataclass(frozen=True)
class UpdateUnityData:
    """Data required to update an existing unity."""
    unity_type_id: Optional[int] = None
    unit_number: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    private_area: Optional[Decimal] = None
    coefficient: Optional[Decimal] = None
    floor_number: Optional[int] = None
    floor_label: Optional[str] = None
    occupancy_status: Optional[str] = None
    sort_order: Optional[int] = None
    status: Optional[int] = None
