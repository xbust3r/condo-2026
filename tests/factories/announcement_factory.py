"""
Factory: Announcement.

Creates test announcement records directly in the DB via SQLAlchemy.
"""
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_announcements.infrastructure.dbannouncement import DBAnnouncement


class AnnouncementFactory:
    """Factory for creating test Announcement records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        author_user_id: int,
        title: str = None,
        content: str = None,
        category: str = "info",
        visibility: str = "public",
        is_pinned: bool = False,
        published_at: datetime = None,
        expires_at: datetime = None,
        tower_id: int = None,
        **kwargs,
    ) -> DBAnnouncement:
        db_ann = DBAnnouncement(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            author_user_id=author_user_id,
            title=title or "Factory Announcement",
            content=content or "This is a test announcement.",
            category=category,
            visibility=visibility,
            is_pinned=is_pinned,
            published_at=published_at or datetime.utcnow(),
            expires_at=expires_at or (datetime.utcnow() + timedelta(days=30)),
            tower_id=tower_id,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_ann)
        session.flush()
        session.refresh(db_ann)
        return db_ann
