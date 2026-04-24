# =============================================================================
# API Routes: core_meetings
#
# Endpoints:
#   GET    /meetings/health                      — health check
#   POST   /meetings                            — create
#   GET    /meetings                            — list with filters
#   GET    /meetings/{id}                       — get by id
#   GET    /meetings/uuid/{uuid}                — get by uuid
#   GET    /meetings/condominium/{id}/upcoming  — upcoming meetings
#   PUT    /meetings/{id}                       — update
#   POST   /meetings/{id}/approve               — approve meeting
#   POST   /meetings/{id}/cancel                — cancel meeting
#   DELETE /meetings/{id}                       — soft delete
#   DELETE /meetings/{id}/hard                  — hard delete
# =============================================================================

from fastapi import APIRouter, Query

from library.dddpy.core_meetings.usecase.meeting_usecase import MeetingUseCase
from library.dddpy.core_meetings.usecase.meeting_cmd_schema import (
    CreateMeetingSchema,
    UpdateMeetingSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/meetings"
meeting_routes = APIRouter(prefix=PREFIX)


@meeting_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_meetings"}


@meeting_routes.post("")
@api_handler
def create_meeting(request: CreateMeetingSchema) -> dict:
    """
    Create a new meeting/minutes record.
    """
    response = MeetingUseCase().create(request)
    return response.dict()


@meeting_routes.get("")
@api_handler
def list_meetings(
    condominium_id: int = Query(None, description="Filter by condominium"),
    status: str = Query(None, description="Filter by status: scheduled, confirmed, held, cancelled"),
    meeting_type: str = Query(None, description="Filter by meeting type: assembly, board, committee"),
    include_deleted: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List meetings with optional filters."""
    response = MeetingUseCase().list_all(
        condominium_id=condominium_id,
        status=status,
        meeting_type=meeting_type,
        skip=skip,
        limit=limit,
        include_deleted=include_deleted,
    )
    return response.dict()


@meeting_routes.get("/{id}")
@api_handler
def get_meeting(id: int) -> dict:
    """Get a meeting by id."""
    response = MeetingUseCase().get_by_id(id)
    return response.dict()


@meeting_routes.get("/uuid/{uuid}")
@api_handler
def get_meeting_by_uuid(uuid: str) -> dict:
    """Get a meeting by uuid."""
    response = MeetingUseCase().get_by_uuid(uuid)
    return response.dict()


@meeting_routes.get("/condominium/{condominium_id}/upcoming")
@api_handler
def list_upcoming_meetings(
    condominium_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
) -> dict:
    """List upcoming meetings for a condominium."""
    response = MeetingUseCase().list_upcoming(
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@meeting_routes.put("/{id}")
@api_handler
def update_meeting(id: int, request: UpdateMeetingSchema) -> dict:
    """Update a meeting (title, description, date, location, status)."""
    response = MeetingUseCase().update(id, request)
    return response.dict()


@meeting_routes.post("/{id}/approve")
@api_handler
def approve_meeting(id: int) -> dict:
    """Approve a meeting (sets approved_at=now and status=confirmed)."""
    response = MeetingUseCase().approve(id)
    return response.dict()


@meeting_routes.post("/{id}/cancel")
@api_handler
def cancel_meeting(id: int) -> dict:
    """Cancel a meeting (sets status=cancelled)."""
    response = MeetingUseCase().cancel(id)
    return response.dict()


@meeting_routes.delete("/{id}")
@api_handler
def delete_meeting(id: int) -> dict:
    """Soft delete a meeting."""
    response = MeetingUseCase().soft_delete(id)
    return response.dict()


@meeting_routes.delete("/{id}/hard")
@api_handler
def hard_delete_meeting(id: int) -> dict:
    """Permanently delete a meeting."""
    response = MeetingUseCase().hard_delete(id)
    return response.dict()
