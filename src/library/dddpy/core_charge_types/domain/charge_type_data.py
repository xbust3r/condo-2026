"""
from typing import Optional
ChargeType data classes — DDD data layer.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateChargeTypeData:
    """Data required to create a charge type."""
    code: str
    name: str
    description: Optional[str] = None
    is_global: bool = True
    is_active: bool = True
    sort_order: int = 0


@dataclass(frozen=True)
class UpdateChargeTypeData:
    """Data required to update a charge type."""
    name: Optional[str] = None
    description: Optional[str] = None
    is_global: Optional[bool] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None
