"""
Meeting domain entity — DDD for condominium assembly and board meeting minutes.
"""
from datetime import datetime
from typing import Dict, Any, Optional


class MeetingEntity:
    """Entidad de dominio para reuniones/asambleas de condominio."""

    VALID_MEETING_TYPES = {'assembly', 'board', 'committee'}
    VALID_STATUSES = {'scheduled', 'confirmed', 'held', 'cancelled'}

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        meeting_type: str,
        title: str,
        description: Optional[str] = None,
        meeting_date: Optional[datetime] = None,
        location: Optional[str] = None,
        status: str = 'scheduled',
        approved_at: Optional[datetime] = None,
        created_by_user_id: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enriched fields
        condominium_name: Optional[str] = None,
        created_by_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.meeting_type = meeting_type
        self.title = title
        self.description = description
        self.meeting_date = meeting_date
        self.location = location
        self.status = status
        self.approved_at = approved_at
        self.created_by_user_id = created_by_user_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.condominium_name = condominium_name
        self.created_by_name = created_by_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'uuid': self.uuid,
            'condominium_id': self.condominium_id,
            'meeting_type': self.meeting_type,
            'title': self.title,
            'description': self.description,
            'meeting_date': self.meeting_date.isoformat() if self.meeting_date else None,
            'location': self.location,
            'status': self.status,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_by_user_id': self.created_by_user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'condominium_name': self.condominium_name,
            'created_by_name': self.created_by_name,
        }
