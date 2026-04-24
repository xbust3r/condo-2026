"""
from typing import Optional
Notification query repository implementation — read operations with enrichment.
"""
from typing import Optional, List, Tuple
from sqlalchemy import and_, text

from library.dddpy.core_notifications.domain.notification_entity import NotificationEntity
from library.dddpy.core_notifications.domain.notification_query_repository import NotificationQueryRepository
from library.dddpy.core_notifications.infrastructure.db_notification import DBNotification
from library.dddpy.core_notifications.infrastructure.notification_mapper import NotificationMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("NotificationQueryRepository")


class NotificationQueryRepositoryImpl(NotificationQueryRepository):

    def __init__(self):
        logger.info("NotificationQueryRepositoryImpl initialized")

    def _bulk_enrich(self, rows: List[DBNotification]) -> List[NotificationEntity]:
        """Apply user full_name enrichment to notification rows."""
        if not rows:
            return []

        user_ids = list({r.user_id for r in rows if r.user_id})

        user_name_map: dict[int, str] = {}
        if user_ids:
            with session_scope() as session:
                placeholders = ", ".join([f":u{i}" for i in range(len(user_ids))])
                sql = f"SELECT user_id, first_name, last_name FROM user_profiles WHERE user_id IN ({placeholders})"
                params = {f"u{i}": uid for i, uid in enumerate(user_ids)}
                result = session.execute(text(sql), params)
                for row in result:
                    uid, fname, lname = row[0], row[1], row[2]
                    user_name_map[uid] = f"{fname or ''} {lname or ''}".strip()

        result_entities = []
        for row in rows:
            entity = NotificationMapper.to_domain_enriched(
                row,
                user_full_name=user_name_map.get(row.user_id),
                condominium_name=None,  # notifications are user-scoped, no condo enrichment
            )
            result_entities.append(entity)
        return result_entities

    def get_by_id(self, id: int) -> Optional[NotificationEntity]:
        logger.debug(f"Fetching notification by id={id}")
        with session_scope() as session:
            db_notification = (
                session.query(DBNotification)
                .filter(
                    DBNotification.id == id,
                    DBNotification.deleted_at.is_(None),
                )
                .first()
            )
            if not db_notification:
                return None
            enriched = self._bulk_enrich([db_notification])
            return enriched[0] if enriched else None

    def get_by_uuid(self, uuid: str) -> Optional[NotificationEntity]:
        logger.debug(f"Fetching notification by uuid={uuid}")
        with session_scope() as session:
            db_notification = (
                session.query(DBNotification)
                .filter(
                    DBNotification.uuid == uuid,
                    DBNotification.deleted_at.is_(None),
                )
                .first()
            )
            if not db_notification:
                return None
            enriched = self._bulk_enrich([db_notification])
            return enriched[0] if enriched else None

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        channel: Optional[str] = None,
        type: Optional[str] = None,
        is_read: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[NotificationEntity], int]:
        logger.debug(f"Listing notifications skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBNotification)

            if not include_deleted:
                query = query.filter(DBNotification.deleted_at.is_(None))
            if user_id is not None:
                query = query.filter(DBNotification.user_id == user_id)
            if channel is not None:
                query = query.filter(DBNotification.channel == channel)
            if type is not None:
                query = query.filter(DBNotification.type == type)
            if is_read is not None:
                query = query.filter(DBNotification.is_read == is_read)

            total = query.count()
            results = (
                query
                .order_by(DBNotification.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        channel: Optional[str] = None,
        type: Optional[str] = None,
        is_read: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[NotificationEntity], int]:
        logger.debug(f"Listing notifications for user_id={user_id}")
        with session_scope() as session:
            query = session.query(DBNotification).filter(
                DBNotification.user_id == user_id
            )

            if not include_deleted:
                query = query.filter(DBNotification.deleted_at.is_(None))
            if channel is not None:
                query = query.filter(DBNotification.channel == channel)
            if type is not None:
                query = query.filter(DBNotification.type == type)
            if is_read is not None:
                query = query.filter(DBNotification.is_read == is_read)

            total = query.count()
            results = (
                query
                .order_by(DBNotification.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_unread(self, user_id: int) -> List[NotificationEntity]:
        logger.debug(f"Listing unread notifications for user_id={user_id}")
        with session_scope() as session:
            results = (
                session.query(DBNotification)
                .filter(
                    DBNotification.user_id == user_id,
                    DBNotification.is_read == False,
                    DBNotification.deleted_at.is_(None),
                )
                .order_by(DBNotification.created_at.desc())
                .all()
            )
            return self._bulk_enrich(results)

    def get_unread_count(self, user_id: int) -> int:
        logger.debug(f"Counting unread notifications for user_id={user_id}")
        with session_scope() as session:
            count = (
                session.query(DBNotification)
                .filter(
                    DBNotification.user_id == user_id,
                    DBNotification.is_read == False,
                    DBNotification.deleted_at.is_(None),
                )
                .count()
            )
            return count

    def _get_by_id_any_status(self, id: int) -> Optional[NotificationEntity]:
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
            enriched = self._bulk_enrich([db_notification])
            return enriched[0] if enriched else None