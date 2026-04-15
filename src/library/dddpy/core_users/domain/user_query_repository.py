"""
User query repository interface — read operations.
"""
from abc import ABC, abstractmethod
from typing import Optional, Tuple, List

from library.dddpy.core_users.domain.user_entity import UserEntity


class UserQueryRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int, include_deleted: bool = False) -> Optional[UserEntity]:
        """Get a user by numeric id."""
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str, include_deleted: bool = False) -> Optional[UserEntity]:
        """Get a user by uuid."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get a user by email address."""
        pass

    @abstractmethod
    def list(
        self,
        email: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[UserEntity], int]:
        """
        List users with optional filters.
        Returns (users, total_count).
        """
        pass
