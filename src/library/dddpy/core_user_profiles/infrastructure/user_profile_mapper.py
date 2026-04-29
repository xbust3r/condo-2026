"""
Mapper — converts DB rows to UserProfileEntity.
"""
import json
from typing import Optional, Any

from library.dddpy.core_user_profiles.domain.user_profile_entity import UserProfileEntity


class UserProfileMapper:

    @staticmethod
    def from_row(row: Any) -> UserProfileEntity:
        """Map a DB row to UserProfileEntity."""
        return UserProfileEntity(
            id=row.id,
            uuid=row.uuid,
            user_id=row.user_id,
            first_name=row.first_name,
            last_name=row.last_name,
            document_type=getattr(row, "document_type", None),
            document_number=getattr(row, "document_number", None),
            phone=getattr(row, "phone", None),
            birth_date=getattr(row, "birth_date", None),
            emergency_contact=json.loads(row.emergency_contact) if getattr(row, 'emergency_contact', None) else None,
            notification_preferences=json.loads(row.notification_preferences) if getattr(row, 'notification_preferences', None) else None,
            avatar_url=getattr(row, "avatar_url", None),
            created_at=row.created_at,
            updated_at=getattr(row, "updated_at", None),
        )
