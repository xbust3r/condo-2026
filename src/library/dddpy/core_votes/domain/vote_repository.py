"""
Vote command repository ABC — write operations.
"""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_votes.domain.vote_entity import VoteEntity
from library.dddpy.core_votes.domain.voter_eligibility_policy import EligibilityResult


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

    @abstractmethod
    def add_vote_record(
        self,
        vote_id: int,
        user_id: int,
        unit_ownership_id: int,
        option_key: str,
        weight: float,
    ) -> bool:
        """Add a vote record with electoral identity = unit_ownership_id."""
        pass

    @abstractmethod
    def vote_record_exists(
        self,
        vote_id: int,
        unit_ownership_id: int,
    ) -> bool:
        """Check if a unit_ownership_id has already voted in this vote."""
        pass

    @abstractmethod
    def record_eligibility_log(
        self,
        vote_id: int,
        unit_ownership_id: int,
        user_id: int,
        result: EligibilityResult,
        rules_snapshot_hash: str,
    ) -> None:
        """Record an eligibility evaluation in the audit log."""
        pass
