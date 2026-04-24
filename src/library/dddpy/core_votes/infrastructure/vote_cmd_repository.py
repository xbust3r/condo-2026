"""
from typing import Optional
Vote command repository implementation — write operations.
"""
from datetime import datetime
from typing import Optional

from library.dddpy.core_votes.domain.vote_entity import VoteEntity
from library.dddpy.core_votes.domain.vote_repository import VoteRepository
from library.dddpy.core_votes.infrastructure.dbvote import DBVote, DBVoteOption, DBVoteRecord
from library.dddpy.core_votes.infrastructure.vote_mapper import VoteMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("VoteCmdRepository")


class VoteCmdRepositoryImpl(VoteRepository):

    def __init__(self):
        logger.info("VoteCmdRepositoryImpl initialized")

    def create(self, entity: VoteEntity) -> VoteEntity:
        logger.info(
            f"Creating vote title='{entity.title}', "
            f"condominium_id={entity.condominium_id}"
        )
        with session_scope() as session:
            db_vote = DBVote(
                uuid=entity.uuid,
                condominium_id=entity.condominium_id,
                meeting_id=entity.meeting_id,
                title=entity.title,
                description=entity.description,
                voting_starts_at=entity.voting_starts_at,
                voting_ends_at=entity.voting_ends_at,
                status=entity.status,
                vote_type=entity.vote_type,
                quorum_required=entity.quorum_required,
                quorum_percentage=entity.quorum_percentage,
                approval_threshold=entity.approval_threshold,
                total_eligible_voters=entity.total_eligible_voters,
                total_votes_cast=0,
                total_yes_votes=0,
                total_no_votes=0,
                total_abstain_votes=0,
                created_by_user_id=entity.created_by_user_id,
            )
            session.add(db_vote)
            session.flush()
            session.refresh(db_vote)

            # Create options
            for opt in entity.options:
                db_option = DBVoteOption(
                    vote_id=db_vote.id,
                    option_text=opt.option_text,
                    option_key=opt.option_key,
                    vote_count=0,
                )
                session.add(db_option)

            session.flush()
            logger.info(f"Vote created with id={db_vote.id}")
            return VoteMapper.to_domain(db_vote, db_options=[])

    def update(self, id: int, entity: VoteEntity) -> Optional[VoteEntity]:
        logger.info(f"Updating vote id={id}")
        with session_scope() as session:
            db_vote = session.query(DBVote).filter(DBVote.id == id).first()
            if not db_vote:
                logger.warning(f"Vote not found for update id={id}")
                return None

            db_vote.title = entity.title
            db_vote.description = entity.description
            db_vote.voting_starts_at = entity.voting_starts_at
            db_vote.voting_ends_at = entity.voting_ends_at
            db_vote.status = entity.status
            db_vote.vote_type = entity.vote_type
            db_vote.quorum_required = entity.quorum_required
            db_vote.quorum_percentage = entity.quorum_percentage
            db_vote.approval_threshold = entity.approval_threshold
            db_vote.total_eligible_voters = entity.total_eligible_voters
            db_vote.total_votes_cast = entity.total_votes_cast
            db_vote.total_yes_votes = entity.total_yes_votes
            db_vote.total_no_votes = entity.total_no_votes
            db_vote.total_abstain_votes = entity.total_abstain_votes
            db_vote.result_proclaimed_at = entity.result_proclaimed_at

            session.flush()
            session.refresh(db_vote)

            # Update options (replace all)
            session.query(DBVoteOption).filter(DBVoteOption.vote_id == id).delete()
            for opt in entity.options:
                db_option = DBVoteOption(
                    vote_id=id,
                    option_text=opt.option_text,
                    option_key=opt.option_key,
                    vote_count=opt.vote_count,
                )
                session.add(db_option)

            session.flush()
            logger.info(f"Vote updated id={id}")
            return VoteMapper.to_domain(db_vote)

    def delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        logger.info(f"Soft deleting vote id={id}")
        with session_scope() as session:
            db_vote = session.query(DBVote).filter(DBVote.id == id).first()
            if not db_vote:
                logger.warning(f"Vote not found for soft delete id={id}")
                return False
            db_vote.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Vote soft deleted id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        """Physical delete."""
        logger.info(f"Hard deleting vote id={id}")
        with session_scope() as session:
            db_vote = session.query(DBVote).filter(DBVote.id == id).first()
            if not db_vote:
                logger.warning(f"Vote not found for hard delete id={id}")
                return False
            # Cascade deletes options and records via FK (or delete manually)
            session.query(DBVoteRecord).filter(DBVoteRecord.vote_id == id).delete()
            session.query(DBVoteOption).filter(DBVoteOption.vote_id == id).delete()
            session.delete(db_vote)
            session.flush()
            logger.info(f"Vote hard deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        """Restore a soft-deleted record: clears deleted_at."""
        logger.info(f"Restoring vote id={id}")
        with session_scope() as session:
            db_vote = session.query(DBVote).filter(DBVote.id == id).first()
            if not db_vote:
                logger.warning(f"Vote not found for restore id={id}")
                return False
            db_vote.deleted_at = None
            session.flush()
            logger.info(f"Vote restored id={id}")
            return True

    def _get_by_id_any_status(self, id: int) -> Optional[VoteEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching vote by id={id} (any status)")
        with session_scope() as session:
            db_vote = (
                session.query(DBVote)
                .filter(DBVote.id == id)
                .first()
            )
            if not db_vote:
                return None
            db_options = (
                session.query(DBVoteOption)
                .filter(DBVoteOption.vote_id == id)
                .all()
            )
            return VoteMapper.to_domain(db_vote, db_options=db_options)

    def add_vote_record(
        self, vote_id: int, user_id: int, option_key: str
    ) -> bool:
        """
        Add a vote record and increment counters.
        Returns True on success, raises AlreadyVoted if duplicate.
        """
        from library.dddpy.core_votes.domain.vote_exception import AlreadyVoted

        logger.info(
            f"Recording vote vote_id={vote_id}, user_id={user_id}, option_key={option_key}"
        )
        with session_scope() as session:
            # Check for existing record (VOT-04)
            existing = (
                session.query(DBVoteRecord)
                .filter(DBVoteRecord.vote_id == vote_id)
                .filter(DBVoteRecord.user_id == user_id)
                .first()
            )
            if existing:
                logger.warning(
                    f"User {user_id} already voted in vote {vote_id}"
                )
                raise AlreadyVoted()

            # Insert record
            db_record = DBVoteRecord(
                vote_id=vote_id,
                user_id=user_id,
                option_key=option_key,
                voted_at=datetime.utcnow(),
            )
            session.add(db_record)

            # Increment counters on vote
            db_vote = session.query(DBVote).filter(DBVote.id == vote_id).first()
            if not db_vote:
                return False

            db_vote.total_votes_cast = (db_vote.total_votes_cast or 0) + 1

            if option_key == "yes":
                db_vote.total_yes_votes = (db_vote.total_yes_votes or 0) + 1
            elif option_key == "no":
                db_vote.total_no_votes = (db_vote.total_no_votes or 0) + 1
            elif option_key == "abstain":
                db_vote.total_abstain_votes = (db_vote.total_abstain_votes or 0) + 1

            # Increment option vote_count
            db_option = (
                session.query(DBVoteOption)
                .filter(DBVoteOption.vote_id == vote_id)
                .filter(DBVoteOption.option_key == option_key)
                .first()
            )
            if db_option:
                db_option.vote_count = (db_option.vote_count or 0) + 1

            session.flush()
            logger.info(
                f"Vote recorded for user_id={user_id} in vote_id={vote_id}"
            )
            return True
