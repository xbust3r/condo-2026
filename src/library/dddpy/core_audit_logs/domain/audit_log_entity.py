"""
from typing import Optional
AuditLog domain entity.
"""
from datetime import datetime
from typing import Dict, Any, Optional


class AuditLogEntity:
    """Immutable audit log entry — tracks all system transactions."""

    def __init__(
        self,
        id: int,
        uuid: str,
        user_id: int,
        action: str,
        resource_type: str,
        resource_id: int,
        resource_uuid: str,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.user_id = user_id
        self.action = action
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.resource_uuid = resource_uuid
        self.old_values = old_values
        self.new_values = new_values
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "user_id": self.user_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "resource_uuid": self.resource_uuid,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }