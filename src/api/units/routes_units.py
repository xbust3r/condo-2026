# =============================================================================
# API Routes: core_units
# Módulo de gestión de unidades inmobiliarias
#
# Endpoints:
#   POST   /units                         — create
#   GET    /units/{id}                   — get by id
#   GET    /units/uuid/{uuid}            — get by uuid
#   PUT    /units/{id}                   — update
#   DELETE /units/{id}                   — soft delete
#   POST   /units/{id}/restore           — restore
#   DELETE /units/{id}/hard              — hard delete (blocked if has residents)
#   GET    /units                         — list with filters
#   GET    /units/building/{building_id}  — list by building
# =============================================================================

from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_units.usecase.unit_usecase import UnitUseCase
from library.dddpy.core_units.usecase.unit_cmd_schema import (
    CreateUnitSchema,
    UpdateUnitSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/units"

unit_routes = APIRouter(prefix=PREFIX)


@unit_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_units"}


@unit_routes.post("")
@api_handler
def create_unit(request: CreateUnitSchema) -> dict:
    """Create a new unit in a building."""
    response = UnitUseCase().create(request)
    return response.dict()


@unit_routes.get("/{id}")
@api_handler
def get_unit(id: int) -> dict:
    """Get a unit by its ID."""
    response = UnitUseCase().get_by_id(id)
    return response.dict()


@unit_routes.get("/uuid/{uuid}")
@api_handler
def get_unit_by_uuid(uuid: str) -> dict:
    """Get a unit by its UUID."""
    response = UnitUseCase().get_by_uuid(uuid)
    return response.dict()


@unit_routes.put("/{id}")
@api_handler
def update_unit(id: int, request: UpdateUnitSchema) -> dict:
    """Update an existing unit."""
    response = UnitUseCase().update(id, request)
    return response.dict()


@unit_routes.delete("/{id}")
@api_handler
def delete_unit(id: int) -> dict:
    """Soft delete a unit (sets deleted_at timestamp)."""
    response = UnitUseCase().delete(id)
    return response.dict()


@unit_routes.post("/{id}/restore")
@api_handler
def restore_unit(id: int) -> dict:
    """Restore a soft-deleted unit."""
    response = UnitUseCase().restore(id)
    return response.dict()


@unit_routes.delete("/{id}/hard")
@api_handler
def hard_delete_unit(id: int) -> dict:
    """Hard delete a unit. Blocked if unit has active residents."""
    response = UnitUseCase().hard_delete(id)
    return response.dict()


@unit_routes.get("")
@api_handler
def list_units(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    building_id: Optional[int] = Query(None, description="Filter by building"),
    unit_type_id: Optional[int] = Query(None, description="Filter by unit type"),
    occupancy_status: Optional[str] = Query(
        None,
        description="Filter by occupancy status: vacant|occupied|reserved|maintenance|blocked",
    ),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
) -> dict:
    """List all units with optional filters."""
    if limit > 500:
        limit = 500
    response = UnitUseCase().list_all(
        skip=skip,
        limit=limit,
        building_id=building_id,
        unit_type_id=unit_type_id,
        occupancy_status=occupancy_status,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()


@unit_routes.get("/building/{building_id}")
@api_handler
def list_units_by_building(
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
    """List units for a specific building."""
    if limit > 500:
        limit = 500
    response = UnitUseCase().list_by_building(
        building_id=building_id,
        skip=skip,
        limit=limit,
        occupancy_status=occupancy_status,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()