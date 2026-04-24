"""
from typing import Optional
Notification domain entity — DDD for user notifications.
"""
from datetime import datetime
from typing import Dict, Any, Optional


class NotificationChannel:
    IN_APP = "in_app"
    EMAIL = "email"

    ALL = {IN_APP, EMAIL}


class NotificationType:
    ANNOUNCEMENT_PUBLISHED = "announcement_published"
    ANNOUNCEMENT_UPDATED = "announcement_updated"
    INCIDENT_CREATED = "incident_created"
    INCIDENT_ASSIGNED = "incident_assigned"
    INCIDENT_COMPLETED = "incident_completed"
    INCIDENT_CLOSED = "incident_closed"
    PAYMENT_RECEIVED = "payment_received"
    RECEIPT_GENERATED = "receipt_generated"

    ALL = {
        ANNOUNCEMENT_PUBLISHED,
        ANNOUNCEMENT_UPDATED,
        INCIDENT_CREATED,
        INCIDENT_ASSIGNED,
        INCIDENT_COMPLETED,
        INCIDENT_CLOSED,
        PAYMENT_RECEIVED,
        RECEIPT_GENERATED,
    }


class NotificationResourceType:
    ANNOUNCEMENT = "announcement"
    INCIDENT = "incident"
    PAYMENT = "payment"
    RECEIPT = "receipt"

    ALL = {ANNOUNCEMENT, INCIDENT, PAYMENT, RECEIPT}


class NotificationEntity:
    """
    Entidad de dominio para notificaciones de sistema.
    """

    VALID_CHANNELS = NotificationChannel.ALL
    VALID_TYPES = NotificationType.ALL
    VALID_RESOURCE_TYPES = NotificationResourceType.ALL

    def __init__(
        self,
        id: int,
        uuid: str,
        user_id: int,
        channel: str = "in_app",
        type: str = "info",
        resource_type: str = "generic",
        resource_id: int = 0,
        title: str = "",
        body: Optional[str] = None,
        is_read: bool = False,
        read_at: Optional[datetime] = None,
        metadata: Optional[dict] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enrichment fields
        user_full_name: Optional[str] = None,
        condominium_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.user_id = user_id
        self.channel = channel
        self.type = type
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.title = title
        self.body = body
        self.is_read = is_read
        self.read_at = read_at
        self.metadata = metadata or {}
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.user_full_name = user_full_name
        self.condominium_name = condominium_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "user_id": self.user_id,
            "channel": self.channel,
            "type": self.type,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "title": self.title,
            "body": self.body,
            "is_read": self.is_read,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            # Enrichment
            "user_full_name": self.user_full_name,
            "condominium_name": self.condominium_name,
        }

    def mark_read(self) -> None:
        self.is_read = True
        self.read_at = datetime.utcnow()

    def is_deleted(self) -> bool:
        return self.deleted_at is not None