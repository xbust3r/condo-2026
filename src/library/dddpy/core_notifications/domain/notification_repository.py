"""
from typing import Optional
Notification repository ABC — command operations.
"""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_notifications.domain.notification_entity import NotificationEntity


class NotificationRepository(ABC):
    """Abstract repository for notification write operations."""

    @abstractmethod
    def create(self, entity: NotificationEntity) -> NotificationEntity:
        """Create a new notification."""
        pass

    @abstractmethod
    def update(self, id: int, entity: NotificationEntity) -> NotificationEntity:
        """Update an existing notification."""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        pass

    @abstractmethod
    def hard_delete(self, id: int) -> bool:
        """Physical delete."""
        pass

    @abstractmethod
    def restore(self, id: int) -> bool:
        """Restore a soft-deleted record: clears deleted_at."""
        pass

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[NotificationEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        pass