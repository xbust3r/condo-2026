"""
User profile query repository interface — read operations.
"""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_user_profiles.domain.user_profile_entity import UserProfileEntity


class UserProfileQueryRepository(ABC):

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[UserProfileEntity]:
        """Get a profile by user_id."""
        pass
