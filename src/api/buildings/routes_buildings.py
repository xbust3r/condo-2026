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
#
# RBAC: Todas las rutas que acceden/modifican edificios requieren que el
# usuario autenticado tenga un rol activo en el condominio del edificio.
# =============================================================================

import anyio
from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional

from library.dddpy.core_buildings.usecase.building_usecase import BuildingUseCase
from library.dddpy.core_buildings.usecase.building_cmd_schema import CreateBuildingSchema, UpdateBuildingSchema
from library.dddpy.shared.decorators.api_handler import api_handler
from api.auth.rbac_dependencies import get_condominium_user, CondominiumUserContext


PREFIX = "/buildings"

building_routes = APIRouter(prefix=PREFIX)


@building_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


@building_routes.post("")
@api_handler
def create_building(
    request: CreateBuildingSchema,
    ctx: CondominiumUserContext = Depends(get_condominium_user),
) -> dict:
    """Create a new building in a condominium.
    Requires authenticated user with an active role in the target condominium.
    """
    if request.condominium_id != ctx.condominium_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create building in a condominium you don't have access to",
        )
    response = BuildingUseCase().create(request)
    return response.dict()


def _get_building_condominium_id(building_id: int) -> int:
    """Fetch building and return its condominium_id. Raises BuildingNotFound."""
    building_resp = BuildingUseCase().get_by_id(building_id)
    building_data = building_resp.data
    if not building_data:
        from library.dddpy.core_buildings.domain.building_exception import BuildingNotFound
        raise BuildingNotFound()
    condominium_id = building_data.get("condominium_id")
    if not condominium_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Building has no condominium association",
        )
    return condominium_id


def _check_condominium_access_sync(condominium_id: int) -> None:
    """
    Synchronous wrapper that calls the async get_condominium_user in a thread pool.
    This lets us perform the RBAC check from sync route handlers.
    Raises HTTPException 403 if the user has no role in the condominium.
    """
    anyio.run(get_condominium_user, condominium_id)


@building_routes.get("/{id}")
@api_handler
def get_building(id: int) -> dict:
    """Get a building by its ID.
    Requires authenticated user with an active role in the building's condominium.
    """
    condominium_id = _get_building_condominium_id(id)
    _check_condominium_access_sync(condominium_id)
    return BuildingUseCase().get_by_id(id).dict()


@building_routes.get("/uuid/{uuid}")
@api_handler
def get_building_by_uuid(uuid: str) -> dict:
    """Get a building by its UUID."""
    return BuildingUseCase().get_by_uuid(uuid).dict()


@building_routes.put("/{id}")
@api_handler
def update_building(id: int, request: UpdateBuildingSchema) -> dict:
    """Update an existing building.
    Requires authenticated user with an active role in the building's condominium.
    """
    condominium_id = _get_building_condominium_id(id)
    _check_condominium_access_sync(condominium_id)
    return BuildingUseCase().update(id, request).dict()


@building_routes.delete("/{id}")
@api_handler
def delete_building(id: int) -> dict:
    """Soft delete a building (sets deleted_at timestamp).
    Requires authenticated user with an active role in the building's condominium.
    """
    condominium_id = _get_building_condominium_id(id)
    _check_condominium_access_sync(condominium_id)
    return BuildingUseCase().delete(id).dict()


@building_routes.post("/{id}/restore")
@api_handler
def restore_building(id: int) -> dict:
    """Restore a soft-deleted building.
    Requires authenticated user with an active role in the building's condominium.
    """
    condominium_id = _get_building_condominium_id(id)
    _check_condominium_access_sync(condominium_id)
    return BuildingUseCase().restore(id).dict()


@building_routes.delete("/{id}/hard")
@api_handler
def hard_delete_building(id: int) -> dict:
    """Hard delete a building. Blocked if building has active units.
    Requires authenticated user with an active role in the building's condominium.
    """
    condominium_id = _get_building_condominium_id(id)
    _check_condominium_access_sync(condominium_id)
    return BuildingUseCase().hard_delete(id).dict()


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
        limit = 500
    return BuildingUseCase().list_all(
        skip=skip, limit=limit,
        condominium_id=condominium_id,
        building_type_id=building_type_id,
        status=status,
        include_deleted=include_deleted,
    ).dict()


@building_routes.get("/condominium/{condominium_id}")
@api_handler
def list_buildings_by_condominium(
    condominium_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[int] = Query(None, description="Filter by status (1=active, 0=inactive)"),
    include_deleted: bool = Query(False, description="Include soft-deleted records"),
    ctx: CondominiumUserContext = Depends(get_condominium_user),
) -> dict:
    """List buildings for a specific condominium.
    Requires authenticated user with an active role in the target condominium.
    """
    if limit > 500:
        limit = 500
    return BuildingUseCase().list_by_condominium(
        condominium_id=condominium_id,
        skip=skip, limit=limit,
        status=status,
        include_deleted=include_deleted,
    ).dict()
