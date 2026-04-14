# =============================================================================
# API Routes: core_unitys
# Módulo de gestión de unidades inmobiliarias
#
# Endpoints:
#   POST   /unitys                      — create
#   GET    /unitys/{id}                — get by id
#   GET    /unitys/uuid/{uuid}         — get by uuid
#   PUT    /unitys/{id}                — update
#   DELETE /unitys/{id}                — soft delete
#   POST   /unitys/{id}/restore        — restore
#   DELETE /unitys/{id}/hard           — hard delete (blocked if has residents)
#   GET    /unitys                      — list with filters
#   GET    /unitys/building/{building_id} — list by building
# =============================================================================

from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_unitys.usecase.unity_usecase import UnityUseCase
from library.dddpy.core_unitys.usecase.unity_cmd_schema import (
    CreateUnitySchema,
    UpdateUnitySchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/unitys"

unity_routes = APIRouter(prefix=PREFIX)


@unity_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_unitys"}


@unity_routes.post("")
@api_handler
def create_unity(request: CreateUnitySchema) -> dict:
    """Create a new unity in a building."""
    response = UnityUseCase().create(request)
    return response.dict()


@unity_routes.get("/{id}")
@api_handler
def get_unity(id: int) -> dict:
    """Get a unity by its ID."""
    response = UnityUseCase().get_by_id(id)
    return response.dict()


@unity_routes.get("/uuid/{uuid}")
@api_handler
def get_unity_by_uuid(uuid: str) -> dict:
    """Get a unity by its UUID."""
    response = UnityUseCase().get_by_uuid(uuid)
    return response.dict()


@unity_routes.put("/{id}")
@api_handler
def update_unity(id: int, request: UpdateUnitySchema) -> dict:
    """Update an existing unity."""
    response = UnityUseCase().update(id, request)
    return response.dict()


@unity_routes.delete("/{id}")
@api_handler
def delete_unity(id: int) -> dict:
    """Soft delete a unity (sets deleted_at timestamp)."""
    response = UnityUseCase().delete(id)
    return response.dict()


@unity_routes.post("/{id}/restore")
@api_handler
def restore_unity(id: int) -> dict:
    """Restore a soft-deleted unity."""
    response = UnityUseCase().restore(id)
    return response.dict()


@unity_routes.delete("/{id}/hard")
@api_handler
def hard_delete_unity(id: int) -> dict:
    """Hard delete a unity. Blocked if unity has active residents."""
    response = UnityUseCase().hard_delete(id)
    return response.dict()


@unity_routes.get("")
@api_handler
def list_unities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    building_id: Optional[int] = Query(None, description="Filter by building"),
    unity_type_id: Optional[int] = Query(None, description="Filter by unity type"),
    occupancy_status: Optional[str] = Query(
        None,
        description="Filter by occupancy status: vacant|occupied|reserved|maintenance|blocked",
    ),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
) -> dict:
    """List all unities with optional filters."""
    if limit > 500:
        limit = 500
    response = UnityUseCase().list_all(
        skip=skip,
        limit=limit,
        building_id=building_id,
        unity_type_id=unity_type_id,
        occupancy_status=occupancy_status,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()


@unity_routes.get("/building/{building_id}")
@api_handler
def list_unities_by_building(
    building_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    occupancy_status: Optional[str] = Query(
        None,
        description="Filter by occupancy status: vacant|occupied|reserved|maintenance|blocked",
    ),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
) -> dict:
    """List unities for a specific building."""
    if limit > 500:
        limit = 500
    response = UnityUseCase().list_by_building(
        building_id=building_id,
        skip=skip,
        limit=limit,
        occupancy_status=occupancy_status,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()
