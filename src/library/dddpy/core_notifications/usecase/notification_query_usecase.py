"""
from typing import Optional
Notification query use case — read operations.
"""
from typing import Optional, List, Tuple

from library.dddpy.core_notifications.domain.notification_entity import NotificationEntity
from library.dddpy.core_notifications.domain.notification_query_repository import NotificationQueryRepository
from library.dddpy.shared.logging.logging import Logger


logger = Logger("NotificationQueryUseCase")


class NotificationQueryUseCase:

    def __init__(self, repository: NotificationQueryRepository):
        self.repository = repository
        logger.info("NotificationQueryUseCase initialized")

    def get_by_id(self, id: int) -> Optional[NotificationEntity]:
        logger.debug(f"Querying notification by id={id}")
        return self.repository.get_by_id(id)

    def get_by_uuid(self, uuid: str) -> Optional[NotificationEntity]:
        logger.debug(f"Querying notification by uuid={uuid}")
        return self.repository.get_by_uuid(uuid)

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
        return self.repository.list_all(
            skip=skip,
            limit=limit,
            user_id=user_id,
            channel=channel,
            type=type,
            is_read=is_read,
            include_deleted=include_deleted,
        )

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
        return self.repository.list_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            channel=channel,
            type=type,
            is_read=is_read,
            include_deleted=include_deleted,
        )

    def list_unread(self, user_id: int) -> List[NotificationEntity]:
        logger.debug(f"Listing unread notifications for user_id={user_id}")
        return self.repository.list_unread(user_id)

    def get_unread_count(self, user_id: int) -> int:
        logger.debug(f"Counting unread notifications for user_id={user_id}")
        return self.repository.get_unread_count(user_id)

    def _get_by_id_any_status(self, id: int) -> Optional[NotificationEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Querying notification by id={id} (any status)")
        return self.repository._get_by_id_any_status(id)