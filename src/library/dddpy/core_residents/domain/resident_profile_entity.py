"""
Resident profile domain entity — per-user preferences per condominium.
"""
from datetime import datetime
from typing import Dict, Any, Optional


class ResidentProfileEntity:
    """Preferences and settings for a resident in a specific condominium."""

    def __init__(
        self,
        id: int,
        uuid: str,
        user_id: int,
        condominium_id: int,
        notify_announcements: bool = True,
        notify_incidents: bool = True,
        notify_packages: bool = True,
        notify_visitors: bool = True,
        notify_payments: bool = True,
        language: str = 'es',
        theme: str = 'light',
        default_building_id: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enriched
        user_full_name: Optional[str] = None,
        condominium_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.user_id = user_id
        self.condominium_id = condominium_id
        self.notify_announcements = notify_announcements
        self.notify_incidents = notify_incidents
        self.notify_packages = notify_packages
        self.notify_visitors = notify_visitors
        self.notify_payments = notify_payments
        self.language = language
        self.theme = theme
        self.default_building_id = default_building_id
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.user_full_name = user_full_name
        self.condominium_name = condominium_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'uuid': self.uuid,
            'user_id': self.user_id,
            'condominium_id': self.condominium_id,
            'notify_announcements': self.notify_announcements,
            'notify_incidents': self.notify_incidents,
            'notify_packages': self.notify_packages,
            'notify_visitors': self.notify_visitors,
            'notify_payments': self.notify_payments,
            'language': self.language,
            'theme': self.theme,
            'default_building_id': self.default_building_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_full_name': self.user_full_name,
            'condominium_name': self.condominium_name,
        }
