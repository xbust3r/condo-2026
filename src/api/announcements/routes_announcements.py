# =============================================================================
# API Routes: core_announcements
#
# Endpoints:
#   POST   /announcements                      — create [RBAC: announcement.write]
#   GET    /announcements                      — list   [RBAC: announcement.read]
#   GET    /announcements/{id}               — get    [RBAC: announcement.read]
#   GET    /announcements/uuid/{uuid}         — get    [RBAC: announcement.read]
#   GET    /announcements/condominium/{id}/active — list [RBAC: announcement.read]
#   PUT    /announcements/{id}                — update [RBAC: announcement.write]
#   DELETE /announcements/{id}               — delete [RBAC: announcement.delete]
#   POST   /announcements/{id}/restore        — restore [RBAC: announcement.write]
#   DELETE /announcements/{id}/hard          — hard   [RBAC: announcement.delete]
# =============================================================================

from fastapi import APIRouter, Depends, Query

from library.dddpy.core_announcements.usecase.announcement_usecase import AnnouncementUseCase
from library.dddpy.core_announcements.usecase.announcement_cmd_schema import (
    CreateAnnouncementSchema,
    UpdateAnnouncementSchema,
)
from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.shared.decorators.rbac_handler import rbac_required


PREFIX = "/announcements"
announcement_routes = APIRouter(prefix=PREFIX)


@announcement_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_announcements"}


@announcement_routes.post("")
@api_handler
def create_announcement(
    request: CreateAnnouncementSchema,
    user: UserIdentity = Depends(rbac_required("announcement", "write")),
) -> dict:
    """
    Create a new announcement.
    RBAC: announcement.write on condominium_id.
    """
    response = AnnouncementUseCase().create(
        condominium_id=request.condominium_id,
        author_user_id=request.author_user_id,
        title=request.title,
        content=request.content,
        category=request.category,
        visibility=request.visibility,
        is_pinned=request.is_pinned,
        published_at=request.published_at,
        expires_at=request.expires_at,
    )
    return response.dict()


@announcement_routes.get("")
@api_handler
def list_announcements(
    condominium_id: int = Query(None, description="Filter by condominium"),
    category: str = Query(None, description="Filter by category (info/warning/urgent/event)"),
    visibility: str = Query(None, description="Filter by visibility"),
    include_deleted: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: UserIdentity = Depends(rbac_required("announcement", "read")),
) -> dict:
    """List announcements with optional filters."""
    response = AnnouncementUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        category=category,
        visibility=visibility,
        include_deleted=include_deleted,
    )
    return response.dict()


@announcement_routes.get("/condominium/{condominium_id}/active")
@api_handler
def list_active_announcements(
    condominium_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    user: UserIdentity = Depends(rbac_required("announcement", "read")),
) -> dict:
    """
    List active (published + not expired) announcements for a condominium.
    Public endpoint for residents.
    """
    response = AnnouncementUseCase().list_active(
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@announcement_routes.get("/{id}")
@api_handler
def get_announcement(
    id: int,
    user: UserIdentity = Depends(rbac_required("announcement", "read")),
) -> dict:
    """Get an announcement by id."""
    response = AnnouncementUseCase().get_by_id(id)
    return response.dict()


@announcement_routes.get("/uuid/{uuid}")
@api_handler
def get_announcement_by_uuid(
    uuid: str,
    user: UserIdentity = Depends(rbac_required("announcement", "read")),
) -> dict:
    """Get an announcement by uuid."""
    response = AnnouncementUseCase().get_by_uuid(uuid)
    return response.dict()


@announcement_routes.put("/{id}")
@api_handler
def update_announcement(
    id: int,
    request: UpdateAnnouncementSchema,
    user: UserIdentity = Depends(rbac_required("announcement", "write")),
) -> dict:
    """Update an announcement (title, content, category, visibility, pinned, dates)."""
    response = AnnouncementUseCase().update(id, request)
    return response.dict()


@announcement_routes.delete("/{id}")
@api_handler
def delete_announcement(
    id: int,
    user: UserIdentity = Depends(rbac_required("announcement", "delete")),
) -> dict:
    """Soft delete an announcement."""
    response = AnnouncementUseCase().soft_delete(id)
    return response.dict()


@announcement_routes.post("/{id}/restore")
@api_handler
def restore_announcement(
    id: int,
    user: UserIdentity = Depends(rbac_required("announcement", "write")),
) -> dict:
    """Restore a soft-deleted announcement."""
    response = AnnouncementUseCase().restore(id)
    return response.dict()


@announcement_routes.delete("/{id}/hard")
@api_handler
def hard_delete_announcement(
    id: int,
    user: UserIdentity = Depends(rbac_required("announcement", "delete")),
) -> dict:
    """Permanently delete an announcement."""
    response = AnnouncementUseCase().hard_delete(id)
    return response.dict()
