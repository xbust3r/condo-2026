from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass(frozen=True)
class CreateCondominiumData:
    code: str
    name: str
    description: Optional[str] = None
    size: Optional[Decimal] = None
    percentage: Optional[Decimal] = None


@dataclass(frozen=True)
class UpdateCondominiumData:
    name: Optional[str] = None
    description: Optional[str] = None
    size: Optional[Decimal] = None
    percentage: Optional[Decimal] = None
    status: Optional[int] = None