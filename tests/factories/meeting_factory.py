"""
Factory: Meeting.

Creates test meeting records directly in the DB via SQLAlchemy.
"""
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_meetings.infrastructure.dbmeeting import DBMeeting


class MeetingFactory:
    """Factory for creating test Meeting records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        created_by_user_id: int,
        title: str = None,
        meeting_type: str = "assembly",
        status: str = "scheduled",
        meeting_date: datetime = None,
        location: str = None,
        description: str = None,
        **kwargs,
    ) -> DBMeeting:
        db_meeting = DBMeeting(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            meeting_type=meeting_type,
            title=title or "Factory Meeting",
            description=description,
            meeting_date=meeting_date or (datetime.utcnow() + timedelta(days=14)),
            location=location or "Sala de Reuniones",
            status=status,
            created_by_user_id=created_by_user_id,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_meeting)
        session.flush()
        session.refresh(db_meeting)
        return db_meeting
