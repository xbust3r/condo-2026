"""
Meeting command repository interface — DDD domain layer.
"""
from typing import Optional


class MeetingCmdRepository:
    """Interface for write operations on meetings."""

    def create(self, entity: object) -> int:
        pass

    def update(self, entity: object) -> bool:
        pass

    def approve(self, id: int) -> bool:
        pass

    def cancel(self, id: int) -> bool:
        pass

    def soft_delete(self, id: int) -> bool:
        pass

    def hard_delete(self, id: int) -> bool:
        pass
