"""
from typing import Optional
Vote command repository ABC — write operations.
"""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_votes.domain.vote_entity import VoteEntity


class VoteRepository(ABC):
    """Interfaz de escritura para operaciones de modificación de votes."""

    @abstractmethod
    def create(self, entity: VoteEntity) -> VoteEntity:
        pass

    @abstractmethod
    def update(self, id: int, entity: VoteEntity) -> Optional[VoteEntity]:
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
    def _get_by_id_any_status(self, id: int) -> Optional[VoteEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        pass
