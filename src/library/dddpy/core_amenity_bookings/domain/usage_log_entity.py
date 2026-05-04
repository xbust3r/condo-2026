"""
UsageLog domain entity — operational usage tracking for amenity bookings.

Separate from allocation_audit: this captures what actually happened.
"""
from datetime import datetime
from typing import Optional, Dict, Any


VALID_EVENT_TYPES = {'CHECK_IN', 'CHECK_OUT', 'NO_SHOW', 'AUTO_RELEASE', 'MANUAL_CLOSE'}
VALID_SOURCES = {'resident_app', 'admin_panel', 'system'}


class UsageLogEntity:
    """Entidad de dominio para logs de uso operativo de amenities."""

    def __init__(
        self,
        id: int = 0,
        uuid: str = '',
        booking_id: int = 0,
        amenity_id: int = 0,
        condominium_id: int = 0,
        unit_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        event_type: str = '',
        event_at: Optional[datetime] = None,
        recorded_by: Optional[int] = None,
        source: str = 'system',
        notes: Optional[str] = None,
        event_context_json: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.uuid = uuid
        self.booking_id = booking_id
        self.amenity_id = amenity_id
        self.condominium_id = condominium_id
        self.unit_id = unit_id
        self.owner_id = owner_id
        self.event_type = event_type
        self.event_at = event_at or datetime.utcnow()
        self.recorded_by = recorded_by
        self.source = source
        self.notes = notes
        self.event_context_json = event_context_json
        self.created_at = created_at or datetime.utcnow()

    def validate(self) -> None:
        """Validate entity invariants."""
        if self.event_type not in VALID_EVENT_TYPES:
            raise ValueError(f"Invalid event_type: {self.event_type}. Must be one of {VALID_EVENT_TYPES}")
        if self.source not in VALID_SOURCES:
            raise ValueError(f"Invalid source: {self.source}. Must be one of {VALID_SOURCES}")
        if not self.booking_id:
            raise ValueError("booking_id is required")
        if not self.amenity_id:
            raise ValueError("amenity_id is required")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'uuid': self.uuid,
            'booking_id': self.booking_id,
            'amenity_id': self.amenity_id,
            'condominium_id': self.condominium_id,
            'unit_id': self.unit_id,
            'owner_id': self.owner_id,
            'event_type': self.event_type,
            'event_at': self.event_at.isoformat() if isinstance(self.event_at, datetime) else str(self.event_at),
            'recorded_by': self.recorded_by,
            'source': self.source,
            'notes': self.notes,
            'event_context_json': self.event_context_json,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
        }

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> 'UsageLogEntity':
        return cls(
            id=row.get('id', 0),
            uuid=row.get('uuid', ''),
            booking_id=row.get('booking_id', 0),
            amenity_id=row.get('amenity_id', 0),
            condominium_id=row.get('condominium_id', 0),
            unit_id=row.get('unit_id'),
            owner_id=row.get('owner_id'),
            event_type=row.get('event_type', ''),
            event_at=row.get('event_at'),
            recorded_by=row.get('recorded_by'),
            source=row.get('source', 'system'),
            notes=row.get('notes'),
            event_context_json=row.get('event_context_json'),
            created_at=row.get('created_at'),
        )
