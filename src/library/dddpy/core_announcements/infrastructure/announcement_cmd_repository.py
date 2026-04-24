"""
Announcement command repository implementation — SQLAlchemy.
"""
from datetime import datetime
from typing import Optional

from library.dddpy.core_announcements.domain.announcement_cmd_repository import (
    AnnouncementCmdRepository,
)
from library.dddpy.core_announcements.domain.announcement_entity import AnnouncementEntity
from library.dddpy.core_announcements.infrastructure.dbannouncement import DBAnnouncement
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("AnnouncementCmdRepository")


class AnnouncementCmdRepositoryImpl(AnnouncementCmdRepository):

    def __init__(self):
        logger.info("AnnouncementCmdRepositoryImpl initialized")

    def create(self, entity: AnnouncementEntity) -> int:
        logger.info(f"Creating announcement condominium_id={entity.condominium_id}")
        with session_scope() as session:
            db_a = DBAnnouncement(
                uuid=entity.uuid,
                condominium_id=entity.condominium_id,
                author_user_id=entity.author_user_id,
                title=entity.title,
                content=entity.content,
                category=entity.category,
                visibility=entity.visibility,
                is_pinned=entity.is_pinned,
                published_at=entity.published_at,
                expires_at=entity.expires_at,
            )
            session.add(db_a)
            session.flush()
            session.refresh(db_a)
            logger.info(f"Announcement created id={db_a.id}")
            return db_a.id

    def update(self, entity: AnnouncementEntity) -> bool:
        logger.info(f"Updating announcement id={entity.id}")
        with session_scope() as session:
            db_a = session.query(DBAnnouncement).filter(
                DBAnnouncement.id == entity.id,
                DBAnnouncement.deleted_at.is_(None),
            ).first()
            if not db_a:
                return False
            db_a.title = entity.title
            db_a.content = entity.content
            db_a.category = entity.category
            db_a.visibility = entity.visibility
            db_a.is_pinned = entity.is_pinned
            db_a.published_at = entity.published_at
            db_a.expires_at = entity.expires_at
            db_a.updated_at = datetime.utcnow()
            session.flush()
            logger.info(f"Announcement updated id={entity.id}")
            return True

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft-deleting announcement id={id}")
        with session_scope() as session:
            db_a = session.query(DBAnnouncement).filter(
                DBAnnouncement.id == id,
                DBAnnouncement.deleted_at.is_(None),
            ).first()
            if not db_a:
                return False
            db_a.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Announcement soft-deleted id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard-deleting announcement id={id}")
        with session_scope() as session:
            db_a = session.query(DBAnnouncement).filter(
                DBAnnouncement.id == id,
            ).first()
            if not db_a:
                return False
            session.delete(db_a)
            session.flush()
            logger.info(f"Announcement hard-deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring announcement id={id}")
        with session_scope() as session:
            db_a = session.query(DBAnnouncement).filter(
                DBAnnouncement.id == id,
                DBAnnouncement.deleted_at.isnot(None),
            ).first()
            if not db_a:
                return False
            db_a.deleted_at = None
            session.flush()
            logger.info(f"Announcement restored id={id}")
            return True
