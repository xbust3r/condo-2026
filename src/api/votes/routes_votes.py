# =============================================================================
# API Routes: core_votes — Digital Voting System
#
# Endpoints:
#   POST   /votes                          — create (admin)
#   GET    /votes                          — list with filters
#   GET    /votes/{id}                     — get by id
#   GET    /votes/uuid/{uuid}             — get by uuid
#   PATCH  /votes/{id}                    — update (draft only, admin)
#   POST   /votes/{id}/publish            — publish (admin)
#   POST   /votes/{id}/cancel             — cancel (admin)
#   POST   /votes/{id}/cast               — cast vote (eligible user)
#   GET    /votes/{id}/results            — view aggregated results
#   POST   /votes/{id}/proclaim           — proclaim result (admin)
#   GET    /votes/{id}/records            — vote records (admin/open only)
#   POST   /votes/{id}/extend             — extend voting period (admin)
#
# Condominium-scoped:
#   GET    /condominiums/{id}/votes       — list by condominium
# =============================================================================

from typing import Optional
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query, Depends, Path
from sqlalchemy import text

from library.dddpy.core_votes.usecase.vote_factory import (
    vote_cmd_usecase_factory,
    vote_query_usecase_factory,
)
from library.dddpy.core_votes.usecase.vote_cmd_schema import (
    CreateVoteSchema,
    CastVoteSchema,
    UpdateVoteSchema,
)
from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.shared.decorators.rbac_handler import rbac_required
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


PREFIX = "/votes"
vote_routes = APIRouter(prefix=PREFIX)

CONDOMINIUM_PREFIX = "/condominiums"
condominium_vote_routes = APIRouter(prefix=CONDOMINIUM_PREFIX)

logger = Logger("VoteRoutes")


# ─── Vote CRUD ───────────────────────────────────────────────────────────────


@vote_routes.post("")
@api_handler
def create_vote(
    request: CreateVoteSchema,
    user: UserIdentity = Depends(rbac_required("votes", "create", "condominium_id")),
) -> dict:
    """
    Create a new vote.
    RBAC: votes:create permission.
    VOT-06: voting_ends_at cannot be in the past.
    """
    cmd = vote_cmd_usecase_factory()
    result = cmd.create(data=request, created_by_user_id=user.id)
    return result.to_dict()


@vote_routes.get("")
@api_handler
def list_votes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    condominium_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    created_by_user_id: Optional[int] = Query(None),
    include_deleted: bool = Query(False),
    user: UserIdentity = Depends(rbac_required("votes", "read")),
) -> dict:
    """
    List votes with optional filters.
    RBAC: votes:read permission.
    """
    query = vote_query_usecase_factory()
    votes, total = query.list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        status=status,
        created_by_user_id=created_by_user_id,
        include_deleted=include_deleted,
    )
    return {
        "data": [v.to_dict() for v in votes],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@vote_routes.get(f"/{PREFIX[1]}/{{id}}")
@api_handler
def get_vote(
    id: int = Path(..., ge=1),
    user: UserIdentity = Depends(rbac_required("votes", "read")),
) -> dict:
    """Get a vote by id."""
    query = vote_query_usecase_factory()
    vote = query.get_by_id(id)
    if not vote:
        from library.dddpy.core_votes.domain.vote_exception import VoteNotFound
        raise VoteNotFound()
    return vote.to_dict()


@vote_routes.get(f"/{PREFIX[1]}/uuid/{{uuid}}")
@api_handler
def get_vote_by_uuid(
    uuid: str = Path(...),
    user: UserIdentity = Depends(rbac_required("votes", "read")),
) -> dict:
    """Get a vote by UUID."""
    query = vote_query_usecase_factory()
    vote = query.get_by_uuid(uuid)
    if not vote:
        from library.dddpy.core_votes.domain.vote_exception import VoteNotFound
        raise VoteNotFound()
    return vote.to_dict()


@vote_routes.patch(f"/{PREFIX[1]}/{{id}}")
@api_handler
def update_vote(
    request: UpdateVoteSchema,
    id: int = Path(..., ge=1),
    user: UserIdentity = Depends(rbac_required("votes", "create", "condominium_id")),
) -> dict:
    """
    Update a vote (draft only).
    VOT-06: voting_ends_at can only be extended, not shortened.
    RBAC: votes:create permission.
    """
    cmd = vote_cmd_usecase_factory()
    result = cmd.update(id=id, data=request)
    return result.to_dict()


# ─── Vote lifecycle ──────────────────────────────────────────────────────────


@vote_routes.post(f"/{PREFIX[1]}/{{id}}/publish")
@api_handler
def publish_vote(
    id: int = Path(..., ge=1),
    user: UserIdentity = Depends(rbac_required("votes", "create", "condominium_id")),
) -> dict:
    """
    Publish a vote (draft → active).
    VOT-06: can only publish if voting_starts_at is now or in the future.
    RBAC: votes:create permission.
    """
    cmd = vote_cmd_usecase_factory()
    result = cmd.publish(id=id)
    return result.to_dict()


@vote_routes.post(f"/{PREFIX[1]}/{{id}}/cancel")
@api_handler
def cancel_vote(
    id: int = Path(..., ge=1),
    user: UserIdentity = Depends(rbac_required("votes", "cancel", "condominium_id")),
) -> dict:
    """
    Cancel a vote (draft or active only).
    RBAC: votes:cancel permission.
    """
    cmd = vote_cmd_usecase_factory()
    result = cmd.cancel(id=id)
    return result.to_dict()


@vote_routes.post(f"/{PREFIX[1]}/{{id}}/extend")
@api_handler
def extend_vote(
    id: int = Path(..., ge=1),
    new_ends_at: datetime = Query(..., description="New voting end datetime"),
    user: UserIdentity = Depends(rbac_required("votes", "create", "condominium_id")),
) -> dict:
    """
    Extend the voting period of a vote.
    VOT-06: new_ends_at must be after the current ends_at.
    RBAC: votes:create permission.
    """
    cmd = vote_cmd_usecase_factory()
    result = cmd.extend(id=id, new_ends_at=new_ends_at)
    return result.to_dict()


# ─── Voting ───────────────────────────────────────────────────────────────────


@vote_routes.post(f"/{PREFIX[1]}/{{id}}/cast")
@api_handler
def cast_vote(
    request: CastVoteSchema,
    id: int = Path(..., ge=1),
    user: UserIdentity = Depends(rbac_required("votes", "vote", "condominium_id")),
) -> dict:
    """
    Cast a vote in an active voting.
    VOT-03: unit ownership must be eligible (ownership + scope + debt).
    VOT-04: one vote per unit_ownership_id.
    VOT-05: secret vote means anonymous records (but we still store them).
    RBAC: votes:vote permission.
    """
    cmd = vote_cmd_usecase_factory()
    cmd.cast_vote(
        vote_id=id,
        user_id=user.id,
        unit_ownership_id=request.unit_ownership_id,
        option_key=request.option_key,
    )
    return {"message": "Vote recorded successfully", "vote_id": id}


# ─── Results ──────────────────────────────────────────────────────────────────


@vote_routes.get(f"/{PREFIX[1]}/{{id}}/results")
@api_handler
def get_vote_results(
    id: int = Path(..., ge=1),
    user: UserIdentity = Depends(rbac_required("votes", "read")),
) -> dict:
    """
    View aggregated vote results.
    For secret votes, only aggregate counts are shown (no per-user breakdown).
    RBAC: votes:read permission.
    """
    query = vote_query_usecase_factory()
    vote = query.get_by_id(id)
    if not vote:
        from library.dddpy.core_votes.domain.vote_exception import VoteNotFound
        raise VoteNotFound()

    return {
        "vote_id": vote.id,
        "uuid": vote.uuid,
        "title": vote.title,
        "status": vote.status,
        "vote_type": vote.vote_type,
        "quorum_required": vote.quorum_required,
        "quorum_percentage": vote.quorum_percentage,
        "approval_threshold": vote.approval_threshold,
        "total_eligible_voters": vote.total_eligible_voters,
        "total_votes_cast": vote.total_votes_cast,
        "total_yes_votes": vote.total_yes_votes,
        "total_no_votes": vote.total_no_votes,
        "total_abstain_votes": vote.total_abstain_votes,
        "result_proclaimed_at": (
            vote.result_proclaimed_at.isoformat()
            if vote.result_proclaimed_at else None
        ),
        "options": [
            {
                "option_key": opt.option_key,
                "option_text": opt.option_text,
                "vote_count": opt.vote_count,
            }
            for opt in vote.options
        ],
    }


@vote_routes.post(f"/{PREFIX[1]}/{{id}}/proclaim")
@api_handler
def proclaim_vote(
    id: int = Path(..., ge=1),
    user: UserIdentity = Depends(rbac_required("votes", "proclaim", "condominium_id")),
) -> dict:
    """
    Proclaim the result of a vote.
    VOT-01: quorum check (if required).
    VOT-02: approval computation.
    RBAC: votes:proclaim permission.
    """
    cmd = vote_cmd_usecase_factory()
    result = cmd.proclaim(vote_id=id)
    return result.to_dict()


@vote_routes.get(f"/{PREFIX[1]}/{{id}}/records")
@api_handler
def get_vote_records(
    id: int = Path(..., ge=1),
    user: UserIdentity = Depends(rbac_required("votes", "read")),
) -> dict:
    """
    Get vote records (per-user breakdown).
    VOT-05: only available if vote_type=open. For secret votes, return 403.
    RBAC: votes:read permission.
    """
    query = vote_query_usecase_factory()
    vote = query.get_by_id(id)
    if not vote:
        from library.dddpy.core_votes.domain.vote_exception import VoteNotFound
        raise VoteNotFound()

    if vote.vote_type == "secret":
        from library.dddpy.core_votes.domain.vote_exception import VoteValidationError
        raise VoteValidationError(
            "Vote records are not available for secret votes"
        )

    # Get records from DB
    from library.dddpy.core_votes.infrastructure.dbvote import DBVoteRecord
    from library.dddpy.core_votes.infrastructure.vote_mapper import VoteMapper
    with session_scope() as session:
        records = (
            session.query(DBVoteRecord)
            .filter(DBVoteRecord.vote_id == id)
            .all()
        )

        # Enrich with user names
        user_ids = list({r.user_id for r in records})
        user_name_map: dict[int, str] = {}
        if user_ids:
            placeholders = ", ".join([f":u{i}" for i in range(len(user_ids))])
            sql = f"SELECT user_id, first_name, last_name FROM user_profiles WHERE user_id IN ({placeholders})"
            params = {f"u{i}": uid for i, uid in enumerate(user_ids)}
            result = session.execute(text(sql), params)
            for row in result:
                uid, fname, lname = row[0], row[1], row[2]
                user_name_map[uid] = f"{fname or ''} {lname or ''}".strip()

        return {
            "vote_id": id,
            "vote_type": vote.vote_type,
            "records": [
                {
                    "user_id": r.user_id,
                    "user_full_name": user_name_map.get(r.user_id),
                    "option_key": r.option_key,
                    "voted_at": r.voted_at.isoformat() if r.voted_at else None,
                }
                for r in records
            ],
        }


# ─── Condominium-scoped ───────────────────────────────────────────────────────


@condominium_vote_routes.get(f"/{CONDOMINIUM_PREFIX[1]}/{{condominium_id}}{PREFIX}")
@api_handler
def list_votes_by_condominium(
    condominium_id: int = Path(..., ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
    user: UserIdentity = Depends(rbac_required("votes", "read", "condominium_id")),
) -> dict:
    """
    List votes for a specific condominium.
    RBAC: votes:read permission.
    """
    query = vote_query_usecase_factory()
    votes, total = query.list_by_condominium(
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
        status=status,
        include_deleted=include_deleted,
    )
    return {
        "data": [v.to_dict() for v in votes],
        "total": total,
        "skip": skip,
        "limit": limit,
    }
