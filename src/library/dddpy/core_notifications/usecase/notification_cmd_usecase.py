"""
Notification command use case — write operations.
"""
from datetime import datetime

from library.dddpy.core_notifications.domain.notification_entity import (
    NotificationEntity,
    NotificationType,
    NotificationChannel,
    NotificationResourceType,
)
from library.dddpy.core_notifications.domain.notification_repository import NotificationRepository
from library.dddpy.core_notifications.usecase.notification_cmd_schema import (
    CreateNotificationSchema,
    UpdateNotificationSchema,
)
from library.dddpy.core_notifications.domain.notification_exception import (
    NotificationNotFound,
    NotificationValidationError,
    UnauthorizedNotificationAccess,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("NotificationCmdUseCase")


class NotificationCmdUseCase:

    def __init__(self, repository: NotificationRepository):
        self.repository = repository
        logger.info("NotificationCmdUseCase initialized")

    def create(self, data: CreateNotificationSchema) -> NotificationEntity:
        """
        Create a new notification.

        Validates channel, type, and resource_type against allowed values.
        """
        logger.info(
            f"Creating notification title='{data.title}', "
            f"user_id={data.user_id}, channel={data.channel}, type={data.type}"
        )

        # Validate channel
        if data.channel not in NotificationChannel.ALL:
            raise NotificationValidationError(
                f"Invalid channel '{data.channel}'. Valid: {', '.join(sorted(NotificationChannel.ALL))}"
            )

        # Validate type
        if data.type not in NotificationType.ALL:
            raise NotificationValidationError(
                f"Invalid type '{data.type}'. Valid: {', '.join(sorted(NotificationType.ALL))}"
            )

        # Validate resource_type
        if data.resource_type not in NotificationResourceType.ALL:
            raise NotificationValidationError(
                f"Invalid resource_type '{data.resource_type}'. Valid: {', '.join(sorted(NotificationResourceType.ALL))}"
            )

        entity = NotificationEntity(
            id=0,
            uuid="",
            user_id=data.user_id,
            channel=data.channel,
            type=data.type,
            resource_type=data.resource_type,
            resource_id=data.resource_id,
            title=data.title,
            body=data.body,
            is_read=False,
            read_at=None,
            metadata=data.metadata or {},
        )

        return self.repository.create(entity)

    def mark_read(self, id: int, user_id: int) -> NotificationEntity:
        """
        Mark a notification as read.
        Validates that the user owns the notification.
        """
        logger.info(f"Marking notification id={id} as read for user_id={user_id}")

        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise NotificationNotFound()

        if existing.user_id != user_id:
            logger.warning(
                f"Unauthorized access attempt: user_id={user_id} tried to mark "
                f"notification id={id} owned by user_id={existing.user_id}"
            )
            raise UnauthorizedNotificationAccess()

        existing.mark_read()
        return self.repository.update(id, existing)

    def mark_all_read(self, user_id: int) -> int:
        """
        Mark all notifications as read for a user.
        Returns the count of updated notifications.
        """
        logger.info(f"Marking all notifications as read for user_id={user_id}")

        # Get all unread for this user
        from library.dddpy.core_notifications.infrastructure.notification_query_repository import (
            NotificationQueryRepositoryImpl,
        )
        query_repo = NotificationQueryRepositoryImpl()
        unread = query_repo.list_unread(user_id)

        count = 0
        for notification in unread:
            notification.mark_read()
            self.repository.update(notification.id, notification)
            count += 1

        logger.info(f"Marked {count} notifications as read for user_id={user_id}")
        return count

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting notification id={id}")
        return self.repository.delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring notification id={id}")
        return self.repository.restore(id)