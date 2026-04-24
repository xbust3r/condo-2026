from typing import Optional
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal


class CondominiumEntity:
    """Entidad de dominio para condominios."""

    def __init__(
        self,
        id: int,
        uuid: str,
        code: str,
        name: str,
        description: Optional[str] = None,
        land_area: Optional[Decimal] = None,
        built_area: Optional[Decimal] = None,
        area_unit: Optional[str] = 'm2',
        legal_name: Optional[str] = None,
        document_number: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        contact_email: Optional[str] = None,
        contact_phone: Optional[str] = None,
        status: int = 1,
        theme_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.code = code
        self.name = name
        self.description = description
        self.land_area = land_area
        self.built_area = built_area
        self.area_unit = area_unit or 'm2'
        self.legal_name = legal_name
        self.document_number = document_number
        self.address = address
        self.city = city
        self.country = country
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.status = status
        self.theme_id = theme_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "land_area": float(self.land_area) if self.land_area else None,
            "built_area": float(self.built_area) if self.built_area else None,
            "area_unit": self.area_unit,
            "legal_name": self.legal_name,
            "document_number": self.document_number,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "status": self.status,
            "theme_id": self.theme_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }
