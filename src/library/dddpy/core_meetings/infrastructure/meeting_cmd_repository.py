"""
Meeting command repository implementation — SQLAlchemy.
"""
from datetime import datetime
from typing import Optional

from library.dddpy.core_meetings.domain.meeting_cmd_repository import (
    MeetingCmdRepository,
)
from library.dddpy.core_meetings.domain.meeting_entity import MeetingEntity
from library.dddpy.core_meetings.infrastructure.dbmeeting import DBMeeting
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("MeetingCmdRepository")


class MeetingCmdRepositoryImpl(MeetingCmdRepository):

    def __init__(self):
        logger.info("MeetingCmdRepositoryImpl initialized")

    def create(self, entity: MeetingEntity) -> int:
        logger.info(f"Creating meeting condominium_id={entity.condominium_id}")
        with session_scope() as session:
            db_m = DBMeeting(
                uuid=entity.uuid,
                condominium_id=entity.condominium_id,
                meeting_type=entity.meeting_type,
                title=entity.title,
                description=entity.description,
                meeting_date=entity.meeting_date,
                location=entity.location,
                status=entity.status,
                created_by_user_id=entity.created_by_user_id,
            )
            session.add(db_m)
            session.flush()
            session.refresh(db_m)
            logger.info(f"Meeting created id={db_m.id}")
            return db_m.id

    def update(self, entity: MeetingEntity) -> bool:
        logger.info(f"Updating meeting id={entity.id}")
        with session_scope() as session:
            db_m = session.query(DBMeeting).filter(
                DBMeeting.id == entity.id,
                DBMeeting.deleted_at.is_(None),
            ).first()
            if not db_m:
                return False
            db_m.title = entity.title
            db_m.description = entity.description
            db_m.meeting_date = entity.meeting_date
            db_m.location = entity.location
            if entity.status:
                db_m.status = entity.status
            db_m.updated_at = datetime.utcnow()
            session.flush()
            logger.info(f"Meeting updated id={entity.id}")
            return True

    def approve(self, id: int) -> bool:
        logger.info(f"Approving meeting id={id}")
        with session_scope() as session:
            db_m = session.query(DBMeeting).filter(
                DBMeeting.id == id,
                DBMeeting.deleted_at.is_(None),
            ).first()
            if not db_m:
                return False
            db_m.approved_at = datetime.utcnow()
            db_m.status = 'confirmed'
            db_m.updated_at = datetime.utcnow()
            session.flush()
            logger.info(f"Meeting approved id={id}")
            return True

    def cancel(self, id: int) -> bool:
        logger.info(f"Cancelling meeting id={id}")
        with session_scope() as session:
            db_m = session.query(DBMeeting).filter(
                DBMeeting.id == id,
                DBMeeting.deleted_at.is_(None),
            ).first()
            if not db_m:
                return False
            db_m.status = 'cancelled'
            db_m.updated_at = datetime.utcnow()
            session.flush()
            logger.info(f"Meeting cancelled id={id}")
            return True

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft-deleting meeting id={id}")
        with session_scope() as session:
            db_m = session.query(DBMeeting).filter(
                DBMeeting.id == id,
                DBMeeting.deleted_at.is_(None),
            ).first()
            if not db_m:
                return False
            db_m.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Meeting soft-deleted id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard-deleting meeting id={id}")
        with session_scope() as session:
            db_m = session.query(DBMeeting).filter(
                DBMeeting.id == id,
            ).first()
            if not db_m:
                return False
            session.delete(db_m)
            session.flush()
            logger.info(f"Meeting hard-deleted id={id}")
            return True
