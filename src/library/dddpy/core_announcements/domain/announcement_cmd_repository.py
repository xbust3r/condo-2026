"""
Announcement command repository interface — DDD domain layer.
"""
from typing import Optional


class AnnouncementCmdRepository:
    """Interface for write operations on announcements."""

    def create(self, entity: object) -> int:
        pass

    def update(self, entity: object) -> bool:
        pass

    def soft_delete(self, id: int) -> bool:
        pass

    def hard_delete(self, id: int) -> bool:
        pass

    def restore(self, id: int) -> bool:
        pass
