"""
Notification command repository implementation — write operations.
"""
from datetime import datetime
import uuid as uuid_lib

from library.dddpy.core_notifications.domain.notification_entity import NotificationEntity
from library.dddpy.core_notifications.domain.notification_repository import NotificationRepository
from library.dddpy.core_notifications.infrastructure.db_notification import DBNotification
from library.dddpy.core_notifications.infrastructure.notification_mapper import NotificationMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("NotificationCmdRepository")


class NotificationCmdRepositoryImpl(NotificationRepository):

    def __init__(self):
        logger.info("NotificationCmdRepositoryImpl initialized")

    def create(self, entity: NotificationEntity) -> NotificationEntity:
        logger.info(
            f"Creating notification title='{entity.title}', "
            f"user_id={entity.user_id}, channel={entity.channel}"
        )
        with session_scope() as session:
            db_notification = DBNotification(
                uuid=str(uuid_lib.uuid4()),
                user_id=entity.user_id,
                channel=entity.channel,
                type=entity.type,
                resource_type=entity.resource_type,
                resource_id=entity.resource_id,
                title=entity.title,
                body=entity.body,
                is_read=entity.is_read,
                read_at=entity.read_at,
                metadata=entity.metadata,
            )
            session.add(db_notification)
            session.flush()
            session.refresh(db_notification)
            logger.info(f"Notification created with id={db_notification.id}")
            return NotificationMapper.to_domain(db_notification)

    def update(self, id: int, entity: NotificationEntity) -> NotificationEntity:
        logger.info(f"Updating notification id={id}")
        with session_scope() as session:
            db_notification = session.query(DBNotification).filter(DBNotification.id == id).first()
            if not db_notification:
                logger.warning(f"Notification not found for update id={id}")
                return None

            db_notification.is_read = entity.is_read
            db_notification.read_at = entity.read_at
            # Note: other mutable fields can be added as needed

            session.flush()
            session.refresh(db_notification)
            logger.info(f"Notification updated id={id}")
            return NotificationMapper.to_domain(db_notification)

    def delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        logger.info(f"Soft deleting notification id={id}")
        with session_scope() as session:
            db_notification = session.query(DBNotification).filter(DBNotification.id == id).first()
            if not db_notification:
                logger.warning(f"Notification not found for soft delete id={id}")
                return False
            db_notification.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Notification soft deleted id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        """Physical delete."""
        logger.info(f"Hard deleting notification id={id}")
        with session_scope() as session:
            db_notification = session.query(DBNotification).filter(DBNotification.id == id).first()
            if not db_notification:
                logger.warning(f"Notification not found for hard delete id={id}")
                return False
            session.delete(db_notification)
            session.flush()
            logger.info(f"Notification hard deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        """Restore a soft-deleted record: clears deleted_at."""
        logger.info(f"Restoring notification id={id}")
        with session_scope() as session:
            db_notification = session.query(DBNotification).filter(DBNotification.id == id).first()
            if not db_notification:
                logger.warning(f"Notification not found for restore id={id}")
                return False
            db_notification.deleted_at = None
            session.flush()
            logger.info(f"Notification restored id={id}")
            return True

    def _get_by_id_any_status(self, id: int):
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching notification by id={id} (any status)")
        with session_scope() as session:
            db_notification = (
                session.query(DBNotification)
                .filter(DBNotification.id == id)
                .first()
            )
            if not db_notification:
                return None
            return NotificationMapper.to_domain(db_notification)