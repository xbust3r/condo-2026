# =============================================================================
# API Routes: core_buildings
# Módulo en construcción — Gestión de edificios/torres
#
# Endpoints:
#   POST   /buildings                    — create
#   GET    /buildings/{id}              — get by id
#   GET    /buildings/uuid/{uuid}       — get by uuid
#   PUT    /buildings/{id}              — update
#   DELETE /buildings/{id}              — soft delete
#   POST   /buildings/{id}/restore      — restore
#   DELETE /buildings/{id}/hard         — hard delete
#   GET    /buildings                    — list with filters
#   GET    /buildings/condominium/{id}  — list by condominium
# =============================================================================

from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_buildings.usecase.building_usecase import BuildingUseCase
from library.dddpy.core_buildings.usecase.building_cmd_schema import CreateBuildingSchema, UpdateBuildingSchema
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/buildings"

building_routes = APIRouter(prefix=PREFIX)


@building_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


@building_routes.post("")
@api_handler
def create_building(request: CreateBuildingSchema) -> dict:
    """Create a new building in a condominium."""
    response = BuildingUseCase().create(request)
    return response.dict()


@building_routes.get("/{id}")
@api_handler
def get_building(id: int) -> dict:
    """Get a building by its ID."""
    response = BuildingUseCase().get_by_id(id)
    return response.dict()


@building_routes.get("/uuid/{uuid}")
@api_handler
def get_building_by_uuid(uuid: str) -> dict:
    """Get a building by its UUID."""
    response = BuildingUseCase().get_by_uuid(uuid)
    return response.dict()


@building_routes.put("/{id}")
@api_handler
def update_building(id: int, request: UpdateBuildingSchema) -> dict:
    """Update an existing building."""
    response = BuildingUseCase().update(id, request)
    return response.dict()


@building_routes.delete("/{id}")
@api_handler
def delete_building(id: int) -> dict:
    """Soft delete a building (sets deleted_at timestamp)."""
    response = BuildingUseCase().delete(id)
    return response.dict()


@building_routes.post("/{id}/restore")
@api_handler
def restore_building(id: int) -> dict:
    """Restore a soft-deleted building."""
    response = BuildingUseCase().restore(id)
    return response.dict()


@building_routes.delete("/{id}/hard")
@api_handler
def hard_delete_building(id: int) -> dict:
    """Hard delete a building. Blocked if building has active units."""
    response = BuildingUseCase().hard_delete(id)
    return response.dict()


@building_routes.get("")
@api_handler
def list_buildings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    condominium_id: Optional[int] = Query(None, description="Filter by condominium"),
    building_type_id: Optional[int] = Query(None, description="Filter by building type"),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
) -> dict:
    """List all buildings with optional filters."""
    if limit > 500:
        limit = 500  # Safety cap
    response = BuildingUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        building_type_id=building_type_id,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()


@building_routes.get("/condominium/{condominium_id}")
@api_handler
def list_buildings_by_condominium(
    condominium_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
) -> dict:
    """List buildings for a specific condominium."""
    if limit > 500:
        limit = 500  # Safety cap
    response = BuildingUseCase().list_by_condominium(
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()