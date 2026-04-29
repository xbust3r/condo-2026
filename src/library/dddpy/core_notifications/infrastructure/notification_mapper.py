"""
Notification mapper — maps between DB model and domain entity.
"""
from library.dddpy.core_notifications.infrastructure.db_notification import DBNotification
from library.dddpy.core_notifications.domain.notification_entity import NotificationEntity


class NotificationMapper:

    @staticmethod
    def to_domain(db_notification: DBNotification) -> NotificationEntity:
        return NotificationEntity(
            id=db_notification.id,
            uuid=db_notification.uuid,
            user_id=db_notification.user_id,
            channel=db_notification.channel,
            type=db_notification.type,
            resource_type=db_notification.resource_type,
            resource_id=db_notification.resource_id,
            title=db_notification.title,
            body=db_notification.body,
            is_read=db_notification.is_read or False,
            read_at=db_notification.read_at,
            metadata=db_notification.meta_data,
            created_at=db_notification.created_at,
            updated_at=db_notification.updated_at,
            deleted_at=db_notification.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(
        db_notification: DBNotification,
        user_full_name: str = None,
        condominium_name: str = None,
    ) -> NotificationEntity:
        entity = NotificationMapper.to_domain(db_notification)
        entity.user_full_name = user_full_name
        entity.condominium_name = condominium_name
        return entity