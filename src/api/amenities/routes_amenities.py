# =============================================================================
# API Routes: core_amenities
#
# Endpoints:
#   GET    /amenities                      — health check
#   POST   /amenities                      — create
#   GET    /amenities                      — list with filters
#   GET    /amenities/{id}                 — get by id
#   GET    /amenities/uuid/{uuid}          — get by uuid
#   PUT    /amenities/{id}                 — update
#   DELETE /amenities/{id}                 — soft delete
#   DELETE /amenities/{id}/hard            — hard delete
# =============================================================================

from fastapi import APIRouter, Query

from library.dddpy.core_amenities.usecase.amenity_usecase import AmenityUseCase
from library.dddpy.core_amenities.usecase.amenity_cmd_schema import (
    CreateAmenitySchema,
    UpdateAmenitySchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/amenities"
amenity_routes = APIRouter(prefix=PREFIX)


@amenity_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_amenities"}


@amenity_routes.post("")
@api_handler
def create_amenity(request: CreateAmenitySchema) -> dict:
    """
    Create a new amenity/common-area.
    """
    response = AmenityUseCase().create(
        condominium_id=request.condominium_id,
        name=request.name,
        description=request.description,
        location=request.location,
        max_capacity=request.max_capacity,
        booking_duration_min=request.booking_duration_min,
        requires_approval=request.requires_approval,
    )
    return response.dict()


@amenity_routes.get("")
@api_handler
def list_amenities(
    condominium_id: int = Query(None, description="Filter by condominium"),
    status: str = Query(None, description="Filter by status (active/inactive)"),
    include_deleted: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List amenities with optional filters."""
    response = AmenityUseCase().list_all(
        condominium_id=condominium_id,
        status=status,
        skip=skip,
        limit=limit,
        include_deleted=include_deleted,
    )
    return response.dict()


@amenity_routes.get("/{id}")
@api_handler
def get_amenity(id: int) -> dict:
    """Get an amenity by id."""
    response = AmenityUseCase().get_by_id(id)
    return response.dict()


@amenity_routes.get("/uuid/{uuid}")
@api_handler
def get_amenity_by_uuid(uuid: str) -> dict:
    """Get an amenity by uuid."""
    response = AmenityUseCase().get_by_uuid(uuid)
    return response.dict()


@amenity_routes.put("/{id}")
@api_handler
def update_amenity(id: int, request: UpdateAmenitySchema) -> dict:
    """Update an amenity."""
    response = AmenityUseCase().update(id, request)
    return response.dict()


@amenity_routes.delete("/{id}")
@api_handler
def delete_amenity(id: int) -> dict:
    """Soft delete an amenity."""
    response = AmenityUseCase().soft_delete(id)
    return response.dict()


@amenity_routes.delete("/{id}/hard")
@api_handler
def hard_delete_amenity(id: int) -> dict:
    """Permanently delete an amenity."""
    response = AmenityUseCase().hard_delete(id)
    return response.dict()
