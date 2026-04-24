# =============================================================================
# API Routes: core_users
#
# Endpoints:
#   POST   /users              — create
#   GET    /users              — list with filters: email, status, include_deleted
#   GET    /users/{id}        — get by id
#   GET    /users/uuid/{uuid}  — get by uuid
#   PUT    /users/{id}         — update (email, status)
#   DELETE /users/{id}         — soft delete
#   POST   /users/{id}/restore — restore
#   POST   /users/{id}/suspend — suspend
#   POST   /users/{id}/activate— activate
#   GET    /users/health
# =============================================================================

from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_users.usecase.user_usecase import UserUseCase
from library.dddpy.core_users.usecase.user_cmd_schema import CreateUserSchema, UpdateUserSchema
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/users"
user_routes = APIRouter(prefix=PREFIX)


@user_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_users"}


@user_routes.post("")
@api_handler
def create_user(request: CreateUserSchema) -> dict:
    """Create a new user."""
    response = UserUseCase().create(request)
    return response.dict()


@user_routes.get("")
@api_handler
def list_users(
    email: Optional[str] = Query(None, description="Filter by email (partial match)"),
    status: Optional[str] = Query(None, description="Filter by status"),
    include_deleted: bool = Query(False, description="Include soft-deleted users"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict:
    """List users with optional filters."""
    response = UserUseCase().list(
        email=email,
        status=status,
        include_deleted=include_deleted,
        limit=limit,
        offset=offset,
    )
    return response.dict()


@user_routes.get("/{id}")
@api_handler
def get_user(id: int) -> dict:
    """Get a user by id."""
    response = UserUseCase().get_by_id(id)
    return response.dict()


@user_routes.get("/{id}/consolidated-view")
@api_handler
def get_user_consolidated_view(id: int) -> dict:
    """
    Phase 1e — Consolidated view of a user.

    Returns:
      - user + profile data
      - active roles (condominium, building, unit level)
      - active ownerships (unit, percentage, type)
      - active occupancies (unit, occupancy type, is_primary)
    """
    return UserUseCase().get_consolidated_view(id)


@user_routes.get("/uuid/{uuid}")
@api_handler
def get_user_by_uuid(uuid: str) -> dict:
    """Get a user by uuid."""
    response = UserUseCase().get_by_uuid(uuid)
    return response.dict()


@user_routes.put("/{id}")
@api_handler
def update_user(id: int, request: UpdateUserSchema) -> dict:
    """Update a user's email and/or status."""
    response = UserUseCase().update(id, request)
    return response.dict()


@user_routes.delete("/{id}")
@api_handler
def delete_user(id: int) -> dict:
    """Soft delete a user."""
    response = UserUseCase().soft_delete(id)
    return response.dict()


@user_routes.post("/{id}/restore")
@api_handler
def restore_user(id: int) -> dict:
    """Restore a soft-deleted user."""
    response = UserUseCase().restore(id)
    return response.dict()


@user_routes.post("/{id}/suspend")
@api_handler
def suspend_user(id: int) -> dict:
    """Suspend a user — invalidates all active sessions via token_version."""
    response = UserUseCase().suspend(id)
    return response.dict()


@user_routes.post("/{id}/activate")
@api_handler
def activate_user(id: int) -> dict:
    """Activate a user."""
    response = UserUseCase().activate(id)
    return response.dict()
