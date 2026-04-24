from typing import Optional
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateBuildingTypeData:
    """Data required to create a building type."""
    condominium_id: Optional[int]  # None = global/system type
    code: str
    name: str
    description: Optional[str] = None
    is_system: bool = False  # True only for seed-initiated types
    sort_order: int = 0


@dataclass(frozen=True)
class UpdateBuildingTypeData:
    """Data required to update a building type."""
    name: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None
    status: Optional[int] = None
