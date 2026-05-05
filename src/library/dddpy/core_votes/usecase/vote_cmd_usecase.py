"""
Vote command use case — write operations with VOT-01 through VOT-06.
Refactored: electoral identity = unit_ownership_id, eligibility via
frozen rules_snapshot, full audit trail.
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
from library.dddpy.core_votes.domain.vote_rules_snapshot import (
    VotingRulesSnapshot,
    VoteCalculationType,
    VoteScope,
)
from library.dddpy.core_votes.domain.vote_exception import (
    VoteNotFound,
    UnauthorizedVoteAccess,
    VoteValidationError,
    QuorumNotReached,
    AlreadyVoted,
)
from library.dddpy.core_votes.domain.ownership_guard import OwnershipGuard
from library.dddpy.core_votes.usecase.voting_policy_factory import VotingPolicyFactory
from library.dddpy.core_votes.usecase.vote_cmd_schema import (
    CreateVoteSchema,
    CastVoteSchema,
    UpdateVoteSchema,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("VoteCmdUseCase")


class NotEligibleError(VoteValidationError):
    """Raised when a unit_ownership is not eligible to vote."""
    def __init__(self, reason_code: str):
        super().__init__(f"Not eligible to vote: {reason_code}")


class OutOfScopeError(VoteValidationError):
    """Raised when a unit_ownership is not in scope of the vote."""
    def __init__(self, reason_code: str = "UNIT_NOT_IN_SCOPE"):
        super().__init__(f"Unit not in scope of this vote: {reason_code}")


class NotAuthorizedError(VoteValidationError):
    """Raised when user does not control the unit_ownership_id."""
    def __init__(self):
        super().__init__("User does not control this unit")


class VoteCmdUseCase:

    def __init__(
        self,
        repository: VoteRepository,
        ownership_guard: OwnershipGuard,
        policy_factory: VotingPolicyFactory,
    ):
        self.repository = repository
        self.ownership_guard = ownership_guard
        self.policy_factory = policy_factory
        logger.info("VoteCmdUseCase initialized with ownership guard + policy factory")

    def create(self, data: CreateVoteSchema, created_by_user_id: int) -> VoteEntity:
        """
        Create a new vote with frozen rules_snapshot.

        VOT-06: voting_ends_at cannot be in the past at creation time.
        The rules in data.rules_snapshot are frozen into the entity immediately —
        they never change after creation.
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

        # Build frozen rules_snapshot if provided
        rules_snapshot = None
        if data.rules_snapshot is not None:
            rules_snapshot = VotingRulesSnapshot.from_dict(data.rules_snapshot)
        else:
            # Default snapshot for backward compatibility
            from datetime import timezone as tz
            rules_snapshot = VotingRulesSnapshot(
                vote_calculation_type=VoteCalculationType.BY_UNIT,
                scope=VoteScope.CONDOMINIUM,
                building_id=None,
                allow_only_owners=True,
                allow_tenants=False,
                max_debt_months=2,
                include_parking_storage=False,
                snapshot_at=datetime.now(tz.utc),
                snapshot_version=1,
            )

        # Build options
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
            # Denormalized from rules_snapshot
            scope_type=rules_snapshot.scope.value,
            vote_calculation_type=rules_snapshot.vote_calculation_type.value,
            building_id=rules_snapshot.building_id,
            options=options,
            rules_snapshot=rules_snapshot,
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
            pass

        if existing.voting_starts_at < now:
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
        self,
        vote_id: int,
        user_id: int,
        unit_ownership_id: int,
        option_key: str,
    ) -> bool:
        """
        Cast a vote for a specific unit_ownership_id.

        Flow (6 steps, 4 rejection points, all audited):
        1. NOT_OWNER          → OwnershipGuard (logged)
        2. UNIT_NOT_IN_SCOPE  → EligibilityPolicy (logged)
        3. DEBT_EXCEEDED/etc  → EligibilityPolicy (logged)
        4. ALREADY_VOTED      → vote_records unicity guard (logged)
        5. weight_policy      → calculate weight
        6. create record      → DBVoteRecord with weight

        VOT-05: secret vote means records are anonymous (but we still store them).
        """
        logger.info(
            f"User {user_id} casting vote in vote_id={vote_id}, "
            f"unit_ownership_id={unit_ownership_id}, option_key={option_key}"
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

        # Require rules_snapshot
        if vote.rules_snapshot is None:
            raise VoteValidationError(
                "Vote has no frozen rules_snapshot — cannot cast vote"
            )

        rules_snapshot_hash = vote.rules_snapshot.compute_hash()

        # Build policy bundle from frozen snapshot
        bundle = self.policy_factory.create(vote.rules_snapshot)

        # ── 1. Authorization: NOT_OWNER ──────────────────────────────────
        if not self.ownership_guard.assert_user_controls_unit(
            user_id, unit_ownership_id
        ):
            from library.dddpy.core_votes.domain.voter_eligibility_policy import (
                EligibilityResult,
            )
            self.repository.record_eligibility_log(
                vote_id, unit_ownership_id, user_id,
                EligibilityResult(eligible=False, reason_code="NOT_OWNER"),
                rules_snapshot_hash,
            )
            raise NotAuthorizedError()

        # ── 2. Eligibility material (scope + debt + owner/tenant rules) ──
        result = bundle.eligibility_policy.is_eligible(unit_ownership_id, vote)

        # Log EVERY evaluation
        self.repository.record_eligibility_log(
            vote_id, unit_ownership_id, user_id, result, rules_snapshot_hash,
        )

        if not result.eligible:
            raise NotEligibleError(result.reason_code)

        # ── 3. Unicity: ALREADY_VOTED ────────────────────────────────────
        if self.repository.vote_record_exists(vote_id, unit_ownership_id):
            from library.dddpy.core_votes.domain.voter_eligibility_policy import (
                EligibilityResult,
            )
            self.repository.record_eligibility_log(
                vote_id, unit_ownership_id, user_id,
                EligibilityResult(eligible=False, reason_code="ALREADY_VOTED"),
                rules_snapshot_hash,
            )
            raise AlreadyVoted()

        # ── 4. Weight ────────────────────────────────────────────────────
        weight = float(bundle.weight_policy.calculate_weight(unit_ownership_id, vote))

        # ── 5. Persist ───────────────────────────────────────────────────
        success = self.repository.add_vote_record(
            vote_id, user_id, unit_ownership_id, option_key, weight,
        )
        logger.info(
            f"Vote cast: user_id={user_id}, unit_ownership_id={unit_ownership_id}, "
            f"vote_id={vote_id}, option_key={option_key}, weight={weight}"
        )
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
                quorum_met = True

        now = datetime.utcnow()

        if not quorum_met:
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
