from typing import Optional
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass(frozen=True)
class CreateCondominiumData:
    code: str
    name: str
    description: Optional[str] = None
    land_area: Optional[Decimal] = None
    built_area: Optional[Decimal] = None
    area_unit: Optional[str] = 'm2'
    legal_name: Optional[str] = None
    document_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    theme_id: Optional[str] = None


@dataclass(frozen=True)
class UpdateCondominiumData:
    name: Optional[str] = None
    description: Optional[str] = None
    land_area: Optional[Decimal] = None
    built_area: Optional[Decimal] = None
    area_unit: Optional[str] = None
    legal_name: Optional[str] = None
    document_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    theme_id: Optional[str] = None
    status: Optional[int] = None
