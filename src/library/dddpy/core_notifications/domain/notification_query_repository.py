"""
from typing import Optional
Notification query repository ABC — read operations.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from library.dddpy.core_notifications.domain.notification_entity import NotificationEntity


class NotificationQueryRepository(ABC):
    """Abstract repository for notification read operations."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[NotificationEntity]:
        """Get notification by ID (excludes soft-deleted)."""
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[NotificationEntity]:
        """Get notification by UUID (excludes soft-deleted)."""
        pass

    @abstractmethod
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
        """List all notifications with optional filters."""
        pass

    @abstractmethod
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
        """List notifications for a specific user with pagination."""
        pass

    @abstractmethod
    def list_unread(self, user_id: int) -> List[NotificationEntity]:
        """List all unread notifications for a user."""
        pass

    @abstractmethod
    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications for a user."""
        pass

    @abstractmethod
    def _get_by_id_any_status(self, id: int) -> Optional[NotificationEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        pass