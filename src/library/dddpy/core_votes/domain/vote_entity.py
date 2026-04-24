"""
from typing import Optional
Vote domain entity — DDD for digital voting system.
"""
from datetime import datetime
from typing import Dict, Any, Optional, List


class VoteStatus:
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

    ALL = {DRAFT, ACTIVE, CLOSED, APPROVED, REJECTED, CANCELLED}


class VoteType:
    OPEN = "open"
    SECRET = "secret"

    ALL = {OPEN, SECRET}


class VoteOptionEntity:
    """Option within a vote (e.g. 'yes', 'no', 'abstain')."""

    def __init__(
        self,
        id: int,
        vote_id: int,
        option_text: str,
        option_key: str,
        vote_count: int = 0,
    ) -> None:
        self.id = id
        self.vote_id = vote_id
        self.option_text = option_text
        self.option_key = option_key
        self.vote_count = vote_count

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "vote_id": self.vote_id,
            "option_text": self.option_text,
            "option_key": self.option_key,
            "vote_count": self.vote_count,
        }


class VoteEntity:
    """
    Entidad de dominio para votaciones digitales.
    """

    VALID_STATUSES = VoteStatus.ALL
    VALID_VOTE_TYPES = VoteType.ALL

    def __init__(
        self,
        id: int,
        uuid: str,
        condominium_id: int,
        meeting_id: Optional[int],
        title: str,
        description: Optional[str],
        voting_starts_at: datetime,
        voting_ends_at: datetime,
        status: str,
        vote_type: str,
        quorum_required: bool,
        quorum_percentage: int,
        approval_threshold: int,
        total_eligible_voters: int,
        total_votes_cast: int,
        total_yes_votes: int,
        total_no_votes: int,
        total_abstain_votes: int,
        result_proclaimed_at: Optional[datetime],
        created_by_user_id: int,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
        # Enrichment fields
        created_by_user_full_name: Optional[str] = None,
        condominium_name: Optional[str] = None,
        # Embedded options/records
        options: Optional[List[VoteOptionEntity]] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.condominium_id = condominium_id
        self.meeting_id = meeting_id
        self.title = title
        self.description = description
        self.voting_starts_at = voting_starts_at
        self.voting_ends_at = voting_ends_at
        self.status = status
        self.vote_type = vote_type
        self.quorum_required = quorum_required
        self.quorum_percentage = quorum_percentage
        self.approval_threshold = approval_threshold
        self.total_eligible_voters = total_eligible_voters
        self.total_votes_cast = total_votes_cast
        self.total_yes_votes = total_yes_votes
        self.total_no_votes = total_no_votes
        self.total_abstain_votes = total_abstain_votes
        self.result_proclaimed_at = result_proclaimed_at
        self.created_by_user_id = created_by_user_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        # Enrichment
        self.created_by_user_full_name = created_by_user_full_name
        self.condominium_name = condominium_name
        # Embedded
        self.options: List[VoteOptionEntity] = options or []

    def _validate_invariants(self) -> None:
        """Validate business invariants. Raises ValueError if invalid."""
        if self.status not in self.VALID_STATUSES:
            raise ValueError(
                f"status must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
            )
        if self.vote_type not in self.VALID_VOTE_TYPES:
            raise ValueError(
                f"vote_type must be one of: {', '.join(sorted(self.VALID_VOTE_TYPES))}"
            )
        # VOT-01/02 invariant: approved/rejected must have result_proclaimed_at set
        if self.status in (VoteStatus.APPROVED, VoteStatus.REJECTED):
            if self.result_proclaimed_at is None:
                raise ValueError(
                    f"Cannot set status to '{self.status}' without result_proclaimed_at"
                )

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def is_active(self) -> bool:
        return self.status == VoteStatus.ACTIVE

    def is_draft(self) -> bool:
        return self.status == VoteStatus.DRAFT

    def is_closed(self) -> bool:
        return self.status == VoteStatus.CLOSED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "condominium_id": self.condominium_id,
            "meeting_id": self.meeting_id,
            "title": self.title,
            "description": self.description,
            "voting_starts_at": self.voting_starts_at.isoformat() if self.voting_starts_at else None,
            "voting_ends_at": self.voting_ends_at.isoformat() if self.voting_ends_at else None,
            "status": self.status,
            "vote_type": self.vote_type,
            "quorum_required": self.quorum_required,
            "quorum_percentage": self.quorum_percentage,
            "approval_threshold": self.approval_threshold,
            "total_eligible_voters": self.total_eligible_voters,
            "total_votes_cast": self.total_votes_cast,
            "total_yes_votes": self.total_yes_votes,
            "total_no_votes": self.total_no_votes,
            "total_abstain_votes": self.total_abstain_votes,
            "result_proclaimed_at": self.result_proclaimed_at.isoformat() if self.result_proclaimed_at else None,
            "created_by_user_id": self.created_by_user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            # Enrichment
            "created_by_user_full_name": self.created_by_user_full_name,
            "condominium_name": self.condominium_name,
            # Embedded
            "options": [opt.to_dict() for opt in self.options],
        }
