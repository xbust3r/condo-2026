"""
Factory: Vote.

Creates test vote records directly in the DB via SQLAlchemy.
"""
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_votes.infrastructure.dbvote import DBVote


class VoteFactory:
    """Factory for creating test Vote records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        created_by_user_id: int,
        title: str = None,
        vote_type: str = "open",
        status: str = "active",
        meeting_id: int = None,
        voting_starts_at: datetime = None,
        voting_ends_at: datetime = None,
        quorum_percentage: int = 51,
        approval_threshold: int = 51,
        total_eligible_voters: int = 10,
        **kwargs,
    ) -> DBVote:
        now = datetime.utcnow()
        db_vote = DBVote(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            meeting_id=meeting_id,
            title=title or "Factory Vote",
            vote_type=vote_type,
            status=status,
            voting_starts_at=voting_starts_at or now,
            voting_ends_at=voting_ends_at or (now + timedelta(days=7)),
            quorum_percentage=quorum_percentage,
            approval_threshold=approval_threshold,
            total_eligible_voters=total_eligible_voters,
            created_by_user_id=created_by_user_id,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_vote)
        session.flush()
        session.refresh(db_vote)
        return db_vote
