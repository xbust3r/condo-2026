# =============================================================================
# API Routes: core_charge_types
# Módulo de catálogo de tipos de cargo del condominio
#
# Endpoints:
#   GET    /charge-types              — list all with filters
#   GET    /charge-types/{id}       — get by id
#   GET    /charge-types/uuid/{uuid} — get by uuid
#   GET    /charge-types/code/{code} — get by code
#   POST   /charge-types              — create
#   PUT    /charge-types/{id}        — update
#   DELETE /charge-types/{id}        — soft delete
#   POST   /charge-types/{id}/restore — restore
#   DELETE /charge-types/{id}/hard   — hard delete
# =============================================================================

from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_charge_types.usecase.charge_type_usecase import (
    ChargeTypeUseCase,
)
from library.dddpy.core_charge_types.usecase.charge_type_cmd_schema import (
    CreateChargeTypeSchema,
    UpdateChargeTypeSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/charge-types"

charge_type_routes = APIRouter(prefix=PREFIX)


@charge_type_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_charge_types"}


@charge_type_routes.get("")
@api_handler
def list_charge_types(
    is_active: Optional[bool] = Query(None, description="Filter by is_active"),
    include_deleted: bool = Query(False, description="Include soft-deleted types"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List all charge types with optional filters."""
    response = ChargeTypeUseCase().list_all(
        is_active=is_active,
        include_deleted=include_deleted,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@charge_type_routes.get("/{id}")
@api_handler
def get_charge_type(id: int) -> dict:
    """Get a charge type by id."""
    response = ChargeTypeUseCase().get_by_id(id)
    return response.dict()


@charge_type_routes.get("/uuid/{uuid}")
@api_handler
def get_charge_type_by_uuid(uuid: str) -> dict:
    """Get a charge type by uuid."""
    response = ChargeTypeUseCase().get_by_uuid(uuid)
    return response.dict()


@charge_type_routes.get("/code/{code}")
@api_handler
def get_charge_type_by_code(code: str) -> dict:
    """Get a charge type by code."""
    response = ChargeTypeUseCase().get_by_code(code)
    return response.dict()


@charge_type_routes.post("")
@api_handler
def create_charge_type(request: CreateChargeTypeSchema) -> dict:
    """Create a new charge type."""
    response = ChargeTypeUseCase().create(request)
    return response.dict()


@charge_type_routes.put("/{id}")
@api_handler
def update_charge_type(id: int, request: UpdateChargeTypeSchema) -> dict:
    """Update a charge type."""
    response = ChargeTypeUseCase().update(id, request)
    return response.dict()


@charge_type_routes.delete("/{id}")
@api_handler
def delete_charge_type(id: int) -> dict:
    """Soft delete a charge type."""
    response = ChargeTypeUseCase().soft_delete(id)
    return response.dict()


@charge_type_routes.post("/{id}/restore")
@api_handler
def restore_charge_type(id: int) -> dict:
    """Restore a soft-deleted charge type."""
    response = ChargeTypeUseCase().restore(id)
    return response.dict()


@charge_type_routes.delete("/{id}/hard")
@api_handler
def hard_delete_charge_type(id: int) -> dict:
    """Hard delete a charge type (permanent)."""
    response = ChargeTypeUseCase().hard_delete(id)
    return response.dict()
