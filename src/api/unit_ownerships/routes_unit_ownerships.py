# =============================================================================
# API Routes: core_unit_ownerships
# Módulo de relación patrimonial usuario ↔ unidad
#
# Endpoints:
#   POST   /unit-ownerships                      — create
#   GET    /unit-ownerships/{id}                — get by id
#   GET    /unit-ownerships/uuid/{uuid}          — get by uuid
#   PUT    /unit-ownerships/{id}                 — update
#   DELETE /unit-ownerships/{id}                 — soft delete
#   POST   /unit-ownerships/{id}/restore         — restore
#   DELETE /unit-ownerships/{id}/hard            — hard delete
#   GET    /unit-ownerships                      — list with filters
#   GET    /unit-ownerships/unit/{unit_id}        — list by unit
#   GET    /unit-ownerships/user/{user_id}       — list by user
# =============================================================================

from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_unit_ownerships.usecase.unit_ownership_usecase import (
    UnitOwnershipUseCase,
)
from library.dddpy.core_unit_ownerships.usecase.unit_ownership_cmd_schema import (
    CreateUnitOwnershipSchema,
    UpdateUnitOwnershipSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/unit-ownerships"

unit_ownership_routes = APIRouter(prefix=PREFIX)


@unit_ownership_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_unit_ownerships"}


@unit_ownership_routes.post("")
@api_handler
def create_unit_ownership(request: CreateUnitOwnershipSchema) -> dict:
    response = UnitOwnershipUseCase().create(request)
    return response.dict()


@unit_ownership_routes.get("/{id}")
@api_handler
def get_unit_ownership(id: int) -> dict:
    response = UnitOwnershipUseCase().get_by_id(id)
    return response.dict()


@unit_ownership_routes.get("/uuid/{uuid}")
@api_handler
def get_unit_ownership_by_uuid(uuid: str) -> dict:
    response = UnitOwnershipUseCase().get_by_uuid(uuid)
    return response.dict()


@unit_ownership_routes.put("/{id}")
@api_handler
def update_unit_ownership(id: int, request: UpdateUnitOwnershipSchema) -> dict:
    response = UnitOwnershipUseCase().update(id, request)
    return response.dict()


@unit_ownership_routes.delete("/{id}")
@api_handler
def delete_unit_ownership(id: int) -> dict:
    response = UnitOwnershipUseCase().delete(id)
    return response.dict()


@unit_ownership_routes.post("/{id}/restore")
@api_handler
def restore_unit_ownership(id: int) -> dict:
    response = UnitOwnershipUseCase().restore(id)
    return response.dict()


@unit_ownership_routes.delete("/{id}/hard")
@api_handler
def hard_delete_unit_ownership(id: int) -> dict:
    response = UnitOwnershipUseCase().hard_delete(id)
    return response.dict()


@unit_ownership_routes.get("")
@api_handler
def list_unit_ownerships(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    unit_id: Optional[int] = Query(None, description="Filter by unit"),
    user_id: Optional[int] = Query(None, description="Filter by user"),
    ownership_type: Optional[str] = Query(
        None,
        description="Filter by ownership type: owner / co_owner",
    ),
    status: Optional[str] = Query(None, description="Filter by status"),
    include_deleted: bool = Query(False),
) -> dict:
    if limit > 500:
        limit = 500
    response = UnitOwnershipUseCase().list_all(
        skip=skip,
        limit=limit,
        unit_id=unit_id,
        user_id=user_id,
        ownership_type=ownership_type,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()


@unit_ownership_routes.get("/unit/{unit_id}")
@api_handler
def list_ownerships_by_unit(
    unit_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
) -> dict:
    if limit > 500:
        limit = 500
    response = UnitOwnershipUseCase().list_by_unit(
        unit_id=unit_id,
        skip=skip,
        limit=limit,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()


@unit_ownership_routes.get("/user/{user_id}")
@api_handler
def list_ownerships_by_user(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
) -> dict:
    if limit > 500:
        limit = 500
    response = UnitOwnershipUseCase().list_by_user(
        user_id=user_id,
        skip=skip,
        limit=limit,
        status=status,
        include_deleted=include_deleted,
    )
    return response.dict()