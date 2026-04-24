# =============================================================================
# API Routes: core_unit_occupancies
# Módulo de relación de ocupación / uso usuario ↔ unidad
#
# Endpoints:
#   POST   /unit-occupancies                     — create
#   GET    /unit-occupancies/{id}                — get by id
#   GET    /unit-occupancies/uuid/{uuid}         — get by uuid
#   PUT    /unit-occupancies/{id}                — update
#   DELETE /unit-occupancies/{id}                — soft delete
#   POST   /unit-occupancies/{id}/restore        — restore
#   DELETE /unit-occupancies/{id}/hard           — hard delete
#   GET    /unit-occupancies                     — list with filters
#   GET    /unit-occupancies/unit/{unit_id}      — list by unit
#   GET    /unit-occupancies/user/{user_id}     — list by user
# =============================================================================

from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_usecase import (
    UnitOccupancyUseCase,
)
from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_cmd_schema import (
    CreateUnitOccupancySchema,
    UpdateUnitOccupancySchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/unit-occupancies"

unit_occupancy_routes = APIRouter(prefix=PREFIX)


@unit_occupancy_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_unit_occupancies"}


@unit_occupancy_routes.post("")
@api_handler
def create_unit_occupancy(request: CreateUnitOccupancySchema) -> dict:
    response = UnitOccupancyUseCase().create(request)
    return response.dict()


@unit_occupancy_routes.get("/{id}")
@api_handler
def get_unit_occupancy(id: int) -> dict:
    response = UnitOccupancyUseCase().get_by_id(id)
    return response.dict()


@unit_occupancy_routes.get("/uuid/{uuid}")
@api_handler
def get_unit_occupancy_by_uuid(uuid: str) -> dict:
    response = UnitOccupancyUseCase().get_by_uuid(uuid)
    return response.dict()


@unit_occupancy_routes.put("/{id}")
@api_handler
def update_unit_occupancy(id: int, request: UpdateUnitOccupancySchema) -> dict:
    response = UnitOccupancyUseCase().update(id, request)
    return response.dict()


@unit_occupancy_routes.delete("/{id}")
@api_handler
def delete_unit_occupancy(id: int) -> dict:
    response = UnitOccupancyUseCase().delete(id)
    return response.dict()


@unit_occupancy_routes.post("/{id}/restore")
@api_handler
def restore_unit_occupancy(id: int) -> dict:
    response = UnitOccupancyUseCase().restore(id)
    return response.dict()


@unit_occupancy_routes.delete("/{id}/hard")
@api_handler
def hard_delete_unit_occupancy(id: int) -> dict:
    response = UnitOccupancyUseCase().hard_delete(id)
    return response.dict()


@unit_occupancy_routes.get("")
@api_handler
def list_unit_occupancies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    unit_id: Optional[int] = Query(None, description="Filter by unit"),
    user_id: Optional[int] = Query(None, description="Filter by user"),
    occupancy_type_id: Optional[int] = Query(None, description="Filter by occupancy type FK"),
    status: Optional[str] = Query(None),
    is_primary: Optional[bool] = Query(None, description="Primary occupancy only"),
    include_deleted: bool = Query(False),
) -> dict:
    if limit > 500:
        limit = 500
    response = UnitOccupancyUseCase().list_all(
        skip=skip,
        limit=limit,
        unit_id=unit_id,
        user_id=user_id,
        occupancy_type_id=occupancy_type_id,
        status=status,
        is_primary=is_primary,
        include_deleted=include_deleted,
    )
    return response.dict()


@unit_occupancy_routes.get("/unit/{unit_id}")
@api_handler
def list_occupancies_by_unit(
    unit_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    occupancy_type_id: Optional[int] = Query(None, description="Filter by occupancy type FK"),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
) -> dict:
    if limit > 500:
        limit = 500
    response = UnitOccupancyUseCase().list_by_unit(
        unit_id=unit_id,
        skip=skip,
        limit=limit,
        occupancy_type_id=occupancy_type_id,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()


@unit_occupancy_routes.get("/user/{user_id}")
@api_handler
def list_occupancies_by_user(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    occupancy_type_id: Optional[int] = Query(None, description="Filter by occupancy type FK"),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
) -> dict:
    if limit > 500:
        limit = 500
    response = UnitOccupancyUseCase().list_by_user(
        user_id=user_id,
        skip=skip,
        limit=limit,
        occupancy_type_id=occupancy_type_id,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()