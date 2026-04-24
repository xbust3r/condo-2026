# =============================================================================
# API Routes: core_occupancy_types
# Módulo de catálogo de tipos de ocupación de unidades
#
# Endpoints:
#   GET    /occupancy-types              — list all with filters
#   GET    /occupancy-types/{id}       — get by id
#   GET    /occupancy-types/uuid/{uuid} — get by uuid
#   POST   /occupancy-types              — create
#   PUT    /occupancy-types/{id}        — update
#   DELETE /occupancy-types/{id}       — soft delete
#   POST   /occupancy-types/{id}/restore — restore
#   DELETE /occupancy-types/{id}/hard   — hard delete
# =============================================================================

from typing import Optional
from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_occupancy_types.usecase.occupancy_type_usecase import (
    OccupancyTypeUseCase,
)
from library.dddpy.core_occupancy_types.usecase.occupancy_type_cmd_schema import (
    CreateOccupancyTypeSchema,
    UpdateOccupancyTypeSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/occupancy-types"

occupancy_type_routes = APIRouter(prefix=PREFIX)


@occupancy_type_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_occupancy_types"}


@occupancy_type_routes.get("")
@api_handler
def list_occupancy_types(
    is_active: Optional[bool] = Query(None, description="Filter by is_active"),
    include_deleted: bool = Query(False, description="Include soft-deleted types"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List all occupancy types with optional filters."""
    response = OccupancyTypeUseCase().list_all(
        is_active=is_active,
        include_deleted=include_deleted,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@occupancy_type_routes.get("/{id}")
@api_handler
def get_occupancy_type(id: int) -> dict:
    """Get an occupancy type by id."""
    response = OccupancyTypeUseCase().get_by_id(id)
    return response.dict()


@occupancy_type_routes.get("/uuid/{uuid}")
@api_handler
def get_occupancy_type_by_uuid(uuid: str) -> dict:
    """Get an occupancy type by uuid."""
    response = OccupancyTypeUseCase().get_by_uuid(uuid)
    return response.dict()


@occupancy_type_routes.post("")
@api_handler
def create_occupancy_type(request: CreateOccupancyTypeSchema) -> dict:
    """Create a new occupancy type."""
    response = OccupancyTypeUseCase().create(request)
    return response.dict()


@occupancy_type_routes.put("/{id}")
@api_handler
def update_occupancy_type(id: int, request: UpdateOccupancyTypeSchema) -> dict:
    """Update an occupancy type."""
    response = OccupancyTypeUseCase().update(id, request)
    return response.dict()


@occupancy_type_routes.delete("/{id}")
@api_handler
def delete_occupancy_type(id: int) -> dict:
    """Soft delete an occupancy type."""
    response = OccupancyTypeUseCase().soft_delete(id)
    return response.dict()


@occupancy_type_routes.post("/{id}/restore")
@api_handler
def restore_occupancy_type(id: int) -> dict:
    """Restore a soft-deleted occupancy type."""
    response = OccupancyTypeUseCase().restore(id)
    return response.dict()


@occupancy_type_routes.delete("/{id}/hard")
@api_handler
def hard_delete_occupancy_type(id: int) -> dict:
    """Hard delete an occupancy type (permanent)."""
    response = OccupancyTypeUseCase().hard_delete(id)
    return response.dict()