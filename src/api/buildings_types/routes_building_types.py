# =============================================================================
# API Routes: core_buildings_types
# =============================================================================
# Endpoints:
#   POST   /building-types                       — create
#   GET    /building-types/{id}                 — get by id
#   GET    /building-types/uuid/{uuid}          — get by uuid
#   PUT    /building-types/{id}                 — update
#   DELETE /building-types/{id}                 — soft delete
#   POST   /building-types/{id}/restore         — restore
#   DELETE /building-types/{id}/hard             — hard delete
#   GET    /building-types                      — list with filters
# =============================================================================

from typing import Optional
from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_buildings_types.usecase.building_type_usecase import (
    BuildingTypeUseCase,
)
from library.dddpy.core_buildings_types.usecase.building_type_cmd_schema import (
    CreateBuildingTypeSchema,
    UpdateBuildingTypeSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/building-types"
building_type_routes = APIRouter(prefix=PREFIX)


@building_type_routes.post("")
@api_handler
def create_building_type(request: CreateBuildingTypeSchema) -> dict:
    response = BuildingTypeUseCase().create(request)
    return response.dict()


@building_type_routes.get("/{id}")
@api_handler
def get_building_type(id: int) -> dict:
    response = BuildingTypeUseCase().get_by_id(id)
    return response.dict()


@building_type_routes.get("/uuid/{uuid}")
@api_handler
def get_building_type_by_uuid(uuid: str) -> dict:
    response = BuildingTypeUseCase().get_by_uuid(uuid)
    return response.dict()


@building_type_routes.put("/{id}")
@api_handler
def update_building_type(id: int, request: UpdateBuildingTypeSchema) -> dict:
    response = BuildingTypeUseCase().update(id, request)
    return response.dict()


@building_type_routes.delete("/{id}")
@api_handler
def delete_building_type(id: int) -> dict:
    response = BuildingTypeUseCase().soft_delete(id)
    return response.dict()


@building_type_routes.post("/{id}/restore")
@api_handler
def restore_building_type(id: int) -> dict:
    response = BuildingTypeUseCase().restore(id)
    return response.dict()


@building_type_routes.delete("/{id}/hard")
@api_handler
def hard_delete_building_type(id: int) -> dict:
    response = BuildingTypeUseCase().hard_delete(id)
    return response.dict()


@building_type_routes.get("")
@api_handler
def list_building_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    condominium_id: Optional[int] = Query(
        None,
        description="Filter by condominium. Returns global + custom for that condo.",
    ),
    include_system: bool = Query(
        True,
        description="Include global system types. False = custom types only.",
    ),
    status: Optional[int] = Query(
        None,
        description="Filter by status (1=active, 0=inactive).",
    ),
    include_deleted: bool = Query(
        False,
        description="Include soft-deleted records.",
    ),
) -> dict:
    if limit > 500:
        limit = 500
    response = BuildingTypeUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        include_system=include_system,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()
