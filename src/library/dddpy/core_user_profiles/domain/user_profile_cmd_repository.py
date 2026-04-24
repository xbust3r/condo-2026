"""
from typing import Optional
User profile command repository interface — write operations.
"""
from abc import ABC, abstractmethod
from datetime import date
from typing import Optional


class UserProfileCmdRepository(ABC):

    @abstractmethod
    def create(
        self,
        user_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        document_type: Optional[str] = None,
        document_number: Optional[str] = None,
        phone: Optional[str] = None,
        birth_date: Optional[date] = None,
    ) -> int:
        """Create a profile for a user. Raises UserProfileAlreadyExists if profile already exists."""
        pass

    @abstractmethod
    def update(
        self,
        user_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        document_type: Optional[str] = None,
        document_number: Optional[str] = None,
        phone: Optional[str] = None,
        birth_date: Optional[date] = None,
    ) -> None:
        """Update a user's profile."""
        pass
