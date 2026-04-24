"""
Notification factory — builds cmd and query use case instances.
"""
from library.dddpy.core_notifications.infrastructure.notification_cmd_repository import NotificationCmdRepositoryImpl
from library.dddpy.core_notifications.infrastructure.notification_query_repository import NotificationQueryRepositoryImpl
from library.dddpy.core_notifications.usecase.notification_cmd_usecase import NotificationCmdUseCase
from library.dddpy.core_notifications.usecase.notification_query_usecase import NotificationQueryUseCase


def notification_cmd_usecase_factory() -> NotificationCmdUseCase:
    return NotificationCmdUseCase(repository=NotificationCmdRepositoryImpl())


def notification_query_usecase_factory() -> NotificationQueryUseCase:
    return NotificationQueryUseCase(repository=NotificationQueryRepositoryImpl())