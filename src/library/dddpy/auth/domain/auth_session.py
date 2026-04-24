"""
from typing import Optional
AuthSession entity — represents an active authentication session.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AuthSession:
    id: int
    uuid: str
    user_id: int
    user_agent: Optional[str]
    ip_address: Optional[str]
    expires_at: datetime
    created_at: datetime
    deleted_at: Optional[datetime]

    def is_active(self) -> bool:
        """Session is active if not soft-deleted and not expired."""
        if self.deleted_at is not None:
            return False
        return self.expires_at > datetime.utcnow()

    def is_expired(self) -> bool:
        return self.expires_at <= datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "user_id": self.user_id,
            "user_agent": self.user_agent,
            "ip_address": self.ip_address,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active(),
        }
