"""
from typing import Optional
UserProfileEntity — domain representation of a user profile.
"""
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class UserProfileEntity:
    id: int
    uuid: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[date] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "document_type": self.document_type,
            "document_number": self.document_number,
            "phone": self.phone,
            "birth_date": (
                self.birth_date.isoformat()
                if self.birth_date else None
            ),
            "created_at": (
                self.created_at.isoformat()
                if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at else None
            ),
        }

    @property
    def full_name(self) -> str:
        parts = [p for p in (self.first_name, self.last_name) if p]
        return " ".join(parts) if parts else None
