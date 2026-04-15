"""
User command repository interface — write operations.
"""
from abc import ABC, abstractmethod
from typing import Optional


class UserCmdRepository(ABC):

    @abstractmethod
    def create(
        self,
        email: str,
        password_hash: str,
        status: str,
    ) -> int:
        """Create a user. Returns new user id. Raises UserAlreadyExists on duplicate email."""
        pass

    @abstractmethod
    def update(self, user_id: int, email: str, status: str) -> None:
        """Update email and/or status of a user."""
        pass

    @abstractmethod
    def soft_delete(self, user_id: int) -> None:
        """Soft delete a user (set deleted_at)."""
        pass

    @abstractmethod
    def restore(self, user_id: int) -> None:
        """Restore a soft-deleted user."""
        pass

    @abstractmethod
    def set_status(self, user_id: int, status: str) -> None:
        """Set user status directly (active|suspended|inactive)."""
        pass

    @abstractmethod
    def increment_token_version(self, user_id: int) -> int:
        """Increment token_version and return new value."""
        pass
