"""
from typing import Optional
Amenity domain entity — DDD for condominium common area reservations.
"""
from datetime import datetime
from typing import Dict, Any, Optional


class AmenityEntity:
    """Entidad de dominio para amenidades/áreas comunes."""

    VALID_STATUSES = {'active', 'inactive'}

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        name: str,
        description: Optional[str] = None,
        location: Optional[str] = None,
        max_capacity: int = 1,
        booking_duration_min: int = 60,
        requires_approval: bool = False,
        status: str = 'active',
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enriched
        condominium_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.name = name
        self.description = description
        self.location = location
        self.max_capacity = max_capacity
        self.booking_duration_min = booking_duration_min
        self.requires_approval = requires_approval
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.condominium_name = condominium_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'uuid': self.uuid,
            'condominium_id': self.condominium_id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'max_capacity': self.max_capacity,
            'booking_duration_min': self.booking_duration_min,
            'requires_approval': self.requires_approval,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'condominium_name': self.condominium_name,
        }
