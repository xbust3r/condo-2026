from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateUnitTypeData:
    """Data required to create a unit type."""
    condominium_id: Optional[int]  # None = global/system type
    code: str
    name: str
    description: Optional[str] = None
    usage_class: Optional[str] = None  # residential|commercial|parking|storage|service
    is_system: bool = False  # True only for seed-initiated types
    sort_order: int = 0


@dataclass(frozen=True)
class UpdateUnitTypeData:
    """Data required to update a unit type."""
    name: Optional[str] = None
    description: Optional[str] = None
    usage_class: Optional[str] = None
    sort_order: Optional[int] = None
    status: Optional[int] = None