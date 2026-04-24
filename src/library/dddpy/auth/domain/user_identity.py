"""
from typing import Optional
UserIdentity — the authenticated user identity returned by /auth/me.

Combines users (auth identity) + user_profiles (human attributes).
password_hash is NEVER included.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserIdentity:
    # From users
    id: int
    uuid: str
    email: str
    status: str
    email_verified_at: Optional[datetime]
    created_at: datetime
    # From user_profiles
    first_name: Optional[str]
    last_name: Optional[str]
    document_type: Optional[str]
    document_number: Optional[str]
    phone: Optional[str]
    profile_uuid: Optional[str]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "email": self.email,
            "status": self.status,
            "email_verified_at": (
                self.email_verified_at.isoformat()
                if self.email_verified_at else None
            ),
            "created_at": (
                self.created_at.isoformat()
                if self.created_at else None
            ),
            "profile": {
                "uuid": self.profile_uuid,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "document_type": self.document_type,
                "document_number": self.document_number,
                "phone": self.phone,
            },
        }

    @property
    def full_name(self) -> str:
        parts = [p for p in (self.first_name, self.last_name) if p]
        return " ".join(parts) if parts else self.email.split("@")[0]
