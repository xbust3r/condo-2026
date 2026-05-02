"""
Factory: Notification.

Creates test notification records directly in the DB via SQLAlchemy.
"""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_notifications.infrastructure.db_notification import DBNotification


class NotificationFactory:
    """Factory for creating test Notification records."""

    @staticmethod
    def create(
        session: Session,
        user_id: int,
        type: str = "info",
        resource_type: str = "system",
        resource_id: int = 1,
        title: str = None,
        body: str = None,
        channel: str = "in_app",
        is_read: bool = False,
        metadata: dict = None,
        **kwargs,
    ) -> DBNotification:
        db_notif = DBNotification(
            uuid=str(uuid.uuid4()),
            user_id=user_id,
            channel=channel,
            type=type,
            resource_type=resource_type,
            resource_id=resource_id,
            title=title or "Factory Notification",
            body=body or "Test notification body.",
            is_read=is_read,
            metadata=metadata,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_notif)
        session.flush()
        session.refresh(db_notif)
        return db_notif
