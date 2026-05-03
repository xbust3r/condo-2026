# =============================================================================
# API Routes: core_amenities
#
# Endpoints:
#   GET    /amenities/health              — health check
#   POST   /amenities                      — create [RBAC: amenities.create]
#   GET    /amenities                      — list   [RBAC: amenities.read]
#   GET    /amenities/{id}                 — get    [RBAC: amenities.read]
#   GET    /amenities/uuid/{uuid}          — get    [RBAC: amenities.read]
#   PUT    /amenities/{id}                 — update [RBAC: amenities.update]
#   DELETE /amenities/{id}                 — delete [RBAC: amenities.delete]
#   DELETE /amenities/{id}/hard            — hard   [RBAC: amenities.delete]
#
# Scope-aware filtering:
#   ?condominium_id=X           → CONDOMINIUM amenities only
#   ?condominium_id=X&building_id=Y → CONDOMINIUM + BUILDING for building Y
# =============================================================================

from fastapi import APIRouter, Depends, Query

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.core_amenities.usecase.amenity_usecase import AmenityUseCase
from library.dddpy.core_amenities.usecase.amenity_cmd_schema import (
    CreateAmenitySchema,
    UpdateAmenitySchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.shared.decorators.rbac_handler import rbac_required


PREFIX = "/amenities"
amenity_routes = APIRouter(prefix=PREFIX)


@amenity_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_amenities"}


@amenity_routes.post("")
@api_handler
def create_amenity(
    request: CreateAmenitySchema,
    user: UserIdentity = Depends(rbac_required("amenities", "create")),
) -> dict:
    """
    Create a new amenity/common-area.

    scope=CONDOMINIUM → common area shared by all buildings (building_id not required)
    scope=BUILDING    → exclusive to a specific building (building_id required)
    """
    response = AmenityUseCase().create(
        condominium_id=request.condominium_id,
        name=request.name,
        description=request.description,
        location=request.location,
        max_capacity=request.max_capacity,
        booking_duration_min=request.booking_duration_min,
        requires_approval=request.requires_approval,
        scope=request.scope,
        building_id=request.building_id,
        booking_price=request.booking_price,
        security_deposit_amount=request.security_deposit_amount,
        is_reservable=request.is_reservable,
    )
    return response.dict()


@amenity_routes.get("")
@api_handler
def list_amenities(
    condominium_id: int = Query(None, description="Filter by condominium"),
    building_id: int = Query(None, description="Filter by building (shows CONDOMINIUM + exclusive)"),
    status: str = Query(None, description="Filter by status (active/inactive)"),
    include_deleted: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: UserIdentity = Depends(rbac_required("amenities", "read")),
) -> dict:
    """List amenities with optional scope-aware filters.

    - condominium_id only → CONDOMINIUM scope amenities
    - condominium_id + building_id → CONDOMINIUM + BUILDING amenities for that building
    """
    response = AmenityUseCase().list_all(
        condominium_id=condominium_id,
        building_id=building_id,
        status=status,
        skip=skip,
        limit=limit,
        include_deleted=include_deleted,
    )
    return response.dict()


@amenity_routes.get("/{id}")
@api_handler
def get_amenity(
    id: int,
    user: UserIdentity = Depends(rbac_required("amenities", "read")),
) -> dict:
    """Get an amenity by id."""
    response = AmenityUseCase().get_by_id(id)
    return response.dict()


@amenity_routes.get("/uuid/{uuid}")
@api_handler
def get_amenity_by_uuid(
    uuid: str,
    user: UserIdentity = Depends(rbac_required("amenities", "read")),
) -> dict:
    """Get an amenity by uuid."""
    response = AmenityUseCase().get_by_uuid(uuid)
    return response.dict()


@amenity_routes.put("/{id}")
@api_handler
def update_amenity(
    id: int,
    request: UpdateAmenitySchema,
    user: UserIdentity = Depends(rbac_required("amenities", "update")),
) -> dict:
    """Update an amenity (supports scope/building changes)."""
    response = AmenityUseCase().update(id, request)
    return response.dict()


@amenity_routes.delete("/{id}")
@api_handler
def delete_amenity(
    id: int,
    user: UserIdentity = Depends(rbac_required("amenities", "delete")),
) -> dict:
    """Soft delete an amenity."""
    response = AmenityUseCase().soft_delete(id)
    return response.dict()


@amenity_routes.delete("/{id}/hard")
@api_handler
def hard_delete_amenity(
    id: int,
    user: UserIdentity = Depends(rbac_required("amenities", "delete")),
) -> dict:
    """Permanently delete an amenity."""
    response = AmenityUseCase().hard_delete(id)
    return response.dict()
