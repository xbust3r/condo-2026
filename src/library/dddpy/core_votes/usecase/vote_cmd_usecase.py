"""
Vote command use case — write operations with VOT-01 through VOT-06.
"""
from datetime import datetime
import uuid as uuid_lib
from typing import Optional

from library.dddpy.core_votes.domain.vote_entity import (
    VoteEntity,
    VoteOptionEntity,
    VoteStatus,
    VoteType,
)
from library.dddpy.core_votes.domain.vote_repository import VoteRepository
from library.dddpy.core_votes.domain.vote_exception import (
    VoteNotFound,
    UnauthorizedVoteAccess,
    VoteValidationError,
    QuorumNotReached,
    AlreadyVoted,
)
from library.dddpy.core_votes.usecase.vote_cmd_schema import (
    CreateVoteSchema,
    CastVoteSchema,
    UpdateVoteSchema,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("VoteCmdUseCase")


class VoteCmdUseCase:

    def __init__(self, repository: VoteRepository):
        self.repository = repository
        logger.info("VoteCmdUseCase initialized")

    def _is_eligible_to_vote(self, user_id: int, condominium_id: int) -> bool:
        """
        VOT-03: Verify user has active ownership OR active role
        (board_member / condominium_admin) in the condominium.
        Denies maintenance_staff, security_staff, and tenants without ownership.
        """
        # Check active ownership in any unit of this condominium
        from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_query_repository import (
            UnitOwnershipQueryRepositoryImpl,
        )
        try:
            own_repo = UnitOwnershipQueryRepositoryImpl()
            # List active ownerships for this user
            active_owns, _ = own_repo.list_all(
                user_id=user_id,
                status="active",
                include_deleted=False,
            )
            # Filter by condominium via units
            from library.dddpy.core_units.infrastructure.dbunits import DBUnits
            from library.dddpy.shared.mysql.session_manager import session_scope
            if active_owns:
                with session_scope() as session:
                    unit_ids = [o.unit_id for o in active_owns]
                    units = session.query(DBUnits).filter(DBUnits.id.in_(unit_ids)).all()
                    building_condo_ids = {u.building_id for u in units}
                    # Get building -> condominium mapping
                    from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
                    buildings = session.query(DBBuildings).filter(
                        DBBuildings.id.in_(building_condo_ids)
                    ).all() if building_condo_ids else []
                    condo_ids = {b.condominium_id for b in buildings}
                    if condominium_id in condo_ids:
                        return True
        except Exception as e:
            logger.warning(f"VOT-03 ownership check failed: {e}")

        # Check active role board_member or condominium_admin
        from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
            CondominiumRoleQueryRepositoryImpl,
        )
        try:
            role_repo = CondominiumRoleQueryRepositoryImpl()
            active_roles, _ = role_repo.list_all(
                user_id=user_id,
                condominium_id=condominium_id,
                status="active",
                include_deleted=False,
            )
            ELIGIBLE_ROLES = {"board_member", "condominium_admin"}
            for role in active_roles:
                if role.role in ELIGIBLE_ROLES:
                    return True
        except Exception as e:
            logger.warning(f"VOT-03 role check failed: {e}")

        return False

    def create(self, data: CreateVoteSchema, created_by_user_id: int) -> VoteEntity:
        """
        Create a new vote.

        VOT-06: voting_ends_at cannot be in the past at creation time.
        """
        logger.info(
            f"Creating vote title='{data.title}', "
            f"condominium_id={data.condominium_id}, created_by_user_id={created_by_user_id}"
        )

        # VOT-06: ends_at cannot be in the past
        now = datetime.utcnow()
        if data.voting_ends_at < now:
            raise VoteValidationError(
                "voting_ends_at cannot be in the past"
            )

        # Validate vote_type
        if data.vote_type not in VoteType.ALL:
            raise VoteValidationError(
                f"Invalid vote_type '{data.vote_type}'. Valid: {', '.join(sorted(VoteType.ALL))}"
            )

        # Validate quorum_percentage and approval_threshold
        if not (1 <= data.quorum_percentage <= 100):
            raise VoteValidationError("quorum_percentage must be between 1 and 100")
        if not (1 <= data.approval_threshold <= 100):
            raise VoteValidationError("approval_threshold must be between 1 and 100")

        # Validate options
        if not data.options or len(data.options) < 2:
            raise VoteValidationError("At least 2 options are required")
        option_keys = set()
        for opt in data.options:
            if "option_key" not in opt or "option_text" not in opt:
                raise VoteValidationError("Each option must have option_key and option_text")
            if opt["option_key"] in option_keys:
                raise VoteValidationError(f"Duplicate option_key: {opt['option_key']}")
            option_keys.add(opt["option_key"])

        # Build entity
        options = [
            VoteOptionEntity(
                id=0,
                vote_id=0,
                option_text=opt["option_text"],
                option_key=opt["option_key"],
                vote_count=0,
            )
            for opt in data.options
        ]

        entity = VoteEntity(
            id=0,
            uuid=str(uuid_lib.uuid4()),
            condominium_id=data.condominium_id,
            meeting_id=data.meeting_id,
            title=data.title,
            description=data.description,
            voting_starts_at=data.voting_starts_at,
            voting_ends_at=data.voting_ends_at,
            status=VoteStatus.DRAFT,
            vote_type=data.vote_type,
            quorum_required=data.quorum_required,
            quorum_percentage=data.quorum_percentage,
            approval_threshold=data.approval_threshold,
            total_eligible_voters=0,
            total_votes_cast=0,
            total_yes_votes=0,
            total_no_votes=0,
            total_abstain_votes=0,
            result_proclaimed_at=None,
            created_by_user_id=created_by_user_id,
            options=options,
        )

        try:
            entity._validate_invariants()
        except ValueError as e:
            raise VoteValidationError(str(e))

        result = self.repository.create(entity)
        logger.info(f"Vote created id={result.id}")
        return result

    def publish(self, id: int) -> VoteEntity:
        """
        Publish a vote: change status from draft to active.
        VOT-06: can only publish if voting_starts_at is now or in the future.
        """
        logger.info(f"Publishing vote id={id}")
        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise VoteNotFound()

        if existing.status != VoteStatus.DRAFT:
            raise VoteValidationError(
                f"Cannot publish vote with status '{existing.status}'. Only draft votes can be published."
            )

        now = datetime.utcnow()
        if existing.voting_starts_at > now:
            # Future start is OK (will auto-activate when time comes — but for simplicity
            # we allow publish and require proclaim check for time)
            pass
        # VOT-06: starts_at must not be in the past
        if existing.voting_starts_at < now:
            # Allow if already past? The spec says "can only publish if starts_at is now or future"
            # Let's allow it but the vote won't be "active" until the time comes.
            # For simplicity: raise error if starts_at is in the past
            raise VoteValidationError(
                "Cannot publish a vote whose voting_starts_at is in the past"
            )

        existing.status = VoteStatus.ACTIVE

        try:
            existing._validate_invariants()
        except ValueError as e:
            raise VoteValidationError(str(e))

        result = self.repository.update(id, existing)
        if result is None:
            raise VoteNotFound()
        logger.info(f"Vote published id={id}")
        return result

    def cancel(self, id: int) -> VoteEntity:
        """
        Cancel a vote: only draft or active votes can be cancelled.
        """
        logger.info(f"Cancelling vote id={id}")
        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise VoteNotFound()

        if existing.status not in (VoteStatus.DRAFT, VoteStatus.ACTIVE):
            raise VoteValidationError(
                f"Cannot cancel a vote with status '{existing.status}'. "
                "Only draft or active votes can be cancelled."
            )

        existing.status = VoteStatus.CANCELLED
        result = self.repository.update(id, existing)
        if result is None:
            raise VoteNotFound()
        logger.info(f"Vote cancelled id={id}")
        return result

    def cast_vote(
        self, vote_id: int, user_id: int, option_key: str
    ) -> bool:
        """
        Cast a vote (VOT-03 eligibility, VOT-04 one vote per user).
        VOT-05: secret vote means records are anonymous (but we still store them).
        """
        logger.info(
            f"User {user_id} attempting to cast vote in vote_id={vote_id}, option_key={option_key}"
        )

        vote = self.repository._get_by_id_any_status(vote_id)
        if not vote:
            raise VoteNotFound()

        if vote.status != VoteStatus.ACTIVE:
            raise VoteValidationError(
                f"Cannot cast vote: vote is not active (status={vote.status})"
            )

        now = datetime.utcnow()
        if now < vote.voting_starts_at or now > vote.voting_ends_at:
            raise VoteValidationError(
                "Voting period is not currently open"
            )

        # VOT-03: eligibility check
        if not self._is_eligible_to_vote(user_id, vote.condominium_id):
            raise UnauthorizedVoteAccess(
                "User is not eligible to vote in this condominium. "
                "Only owners or board/condominium admins can vote."
            )

        # VOT-04: one vote per user — checked inside add_vote_record
        from library.dddpy.core_votes.infrastructure.vote_cmd_repository import VoteCmdRepositoryImpl
        cmd_repo = VoteCmdRepositoryImpl()
        success = cmd_repo.add_vote_record(vote_id, user_id, option_key)
        logger.info(f"Vote cast by user_id={user_id} in vote_id={vote_id}")
        return success

    def proclaim(self, vote_id: int) -> VoteEntity:
        """
        Proclaim the result of a vote.

        VOT-01: If quorum_required, check that votes_cast / eligible >= quorum_percentage/100.
                If quorum not met → status = 'closed', no result proclaimed.

        VOT-02: If quorum met (or not required):
                approved if yes_votes / (yes_votes + no_votes) >= approval_threshold/100
                rejected otherwise.
        """
        logger.info(f"Proclaiming vote result for vote_id={vote_id}")
        existing = self.repository._get_by_id_any_status(vote_id)
        if not existing:
            raise VoteNotFound()

        if existing.status not in (VoteStatus.ACTIVE, VoteStatus.CLOSED):
            raise VoteValidationError(
                f"Cannot proclaim result for vote with status '{existing.status}'. "
                "Only active or closed votes can be proclaimed."
            )

        total_eligible = existing.total_eligible_voters or 0
        total_cast = existing.total_votes_cast or 0
        total_yes = existing.total_yes_votes or 0
        total_no = existing.total_no_votes or 0
        total_abstain = existing.total_abstain_votes or 0

        # VOT-01: quorum check
        quorum_met = True
        if existing.quorum_required:
            if total_eligible > 0:
                quorum_ratio = total_cast / total_eligible
                quorum_met = quorum_ratio >= (existing.quorum_percentage / 100)
            else:
                # No eligible voters defined — skip quorum
                quorum_met = True

        now = datetime.utcnow()

        if not quorum_met:
            # VOT-01: quorum not reached → closed without result
            existing.status = VoteStatus.CLOSED
            existing.result_proclaimed_at = None
            logger.info(
                f"Vote {vote_id}: quorum not met ({total_cast}/{total_eligible}), "
                "status → closed"
            )
            result = self.repository.update(vote_id, existing)
            if result is None:
                raise VoteNotFound()
            return result

        # VOT-02: approval check
        denominator = total_yes + total_no
        if denominator == 0:
            # No yes/no votes — abstain only
            existing.status = VoteStatus.REJECTED
        else:
            approval_ratio = total_yes / denominator
            if approval_ratio >= (existing.approval_threshold / 100):
                existing.status = VoteStatus.APPROVED
            else:
                existing.status = VoteStatus.REJECTED

        existing.result_proclaimed_at = now

        try:
            existing._validate_invariants()
        except ValueError as e:
            raise VoteValidationError(str(e))

        result = self.repository.update(vote_id, existing)
        if result is None:
            raise VoteNotFound()
        logger.info(
            f"Vote {vote_id} proclaimed: status={existing.status}, "
            f"yes={total_yes}, no={total_no}, abstain={total_abstain}"
        )
        return result

    def extend(self, id: int, new_ends_at: datetime) -> VoteEntity:
        """
        Extend voting period.
        VOT-06: can only extend, not shorten. new_ends_at must be > current ends_at.
        """
        logger.info(f"Extending vote id={id} to ends_at={new_ends_at}")
        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise VoteNotFound()

        if existing.voting_ends_at >= new_ends_at:
            raise VoteValidationError(
                "Cannot shorten voting period. new_ends_at must be after current voting_ends_at"
            )

        existing.voting_ends_at = new_ends_at
        result = self.repository.update(id, existing)
        if result is None:
            raise VoteNotFound()
        logger.info(f"Vote {id} extended to {new_ends_at}")
        return result

    def update(self, id: int, data: UpdateVoteSchema) -> VoteEntity:
        """
        Update a vote — only allowed in draft status.
        VOT-06: voting_ends_at can only be extended, not shortened.
        """
        logger.info(f"Updating vote id={id}")
        existing = self.repository._get_by_id_any_status(id)
        if not existing:
            raise VoteNotFound()

        if existing.status != VoteStatus.DRAFT:
            raise VoteValidationError(
                "Can only update votes in draft status"
            )

        if data.title is not None:
            existing.title = data.title
        if data.description is not None:
            existing.description = data.description
        if data.voting_ends_at is not None:
            # VOT-06: can only extend
            if data.voting_ends_at <= existing.voting_ends_at:
                raise VoteValidationError(
                    "Cannot shorten voting period. new voting_ends_at must be after current"
                )
            existing.voting_ends_at = data.voting_ends_at

        try:
            existing._validate_invariants()
        except ValueError as e:
            raise VoteValidationError(str(e))

        result = self.repository.update(id, existing)
        if result is None:
            raise VoteNotFound()
        logger.info(f"Vote updated id={id}")
        return result

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting vote id={id}")
        return self.repository.delete(id)

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting vote id={id}")
        return self.repository.hard_delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring vote id={id}")
        return self.repository.restore(id)
