"""
UserEntity — domain representation of a system user.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserEntity:
    id: int
    uuid: str
    email: str
    status: str  # active | suspended | inactive | locked
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    email_verified_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    token_version: int = 0

    # Profile fields (populated when joined)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    phone: Optional[str] = None
    profile_uuid: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "email": self.email,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "email_verified_at": (
                self.email_verified_at.isoformat() if self.email_verified_at else None
            ),
            "last_login_at": (
                self.last_login_at.isoformat() if self.last_login_at else None
            ),
            "failed_login_attempts": self.failed_login_attempts,
            "locked_until": self.locked_until.isoformat() if self.locked_until else None,
            "token_version": self.token_version,
            "profile": {
                "uuid": self.profile_uuid,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "document_type": self.document_type,
                "document_number": self.document_number,
                "phone": self.phone,
            } if self.profile_uuid or self.first_name else None,
        }

    def to_dict_brief(self) -> dict:
        """Lightweight dict for list views."""
        return {
            "id": self.id,
            "uuid": self.uuid,
            "email": self.email,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @property
    def full_name(self) -> str:
        parts = [p for p in (self.first_name, self.last_name) if p]
        return " ".join(parts) if parts else self.email.split("@")[0]

    def is_active(self) -> bool:
        return self.status == "active"

    def is_suspended(self) -> bool:
        return self.status == "suspended"
