# =============================================================================
# API Routes: core_unities_types
# =============================================================================
# Endpoints:
#   POST   /core_unities_types               — create
#   GET    /core_unities_types/{id}          — get by id
#   GET    /core_unities_types/uuid/{uuid}   — get by uuid
#   PUT    /core_unities_types/{id}          — update
#   DELETE /core_unities_types/{id}          — soft delete
#   POST   /core_unities_types/{id}/restore  — restore
#   DELETE /core_unities_types/{id}/hard     — hard delete
#   GET    /core_unities_types               — list with filters
# =============================================================================

from fastapi import APIRouter, Query
from typing import Optional

from library.dddpy.core_unities_types.usecase.unity_type_usecase import (
    UnityTypeUseCase,
)
from library.dddpy.core_unities_types.usecase.unity_type_cmd_schema import (
    CreateUnityTypeSchema,
    UpdateUnityTypeSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/core_unities_types"
unity_type_routes = APIRouter(prefix=PREFIX)


@unity_type_routes.post("")
@api_handler
def create_unity_type(request: CreateUnityTypeSchema) -> dict:
    response = UnityTypeUseCase().create(request)
    return response.dict()


@unity_type_routes.get("/{id}")
@api_handler
def get_unity_type(id: int) -> dict:
    response = UnityTypeUseCase().get_by_id(id)
    return response.dict()


@unity_type_routes.get("/uuid/{uuid}")
@api_handler
def get_unity_type_by_uuid(uuid: str) -> dict:
    response = UnityTypeUseCase().get_by_uuid(uuid)
    return response.dict()


@unity_type_routes.put("/{id}")
@api_handler
def update_unity_type(id: int, request: UpdateUnityTypeSchema) -> dict:
    response = UnityTypeUseCase().update(id, request)
    return response.dict()


@unity_type_routes.delete("/{id}")
@api_handler
def delete_unity_type(id: int) -> dict:
    response = UnityTypeUseCase().soft_delete(id)
    return response.dict()


@unity_type_routes.post("/{id}/restore")
@api_handler
def restore_unity_type(id: int) -> dict:
    response = UnityTypeUseCase().restore(id)
    return response.dict()


@unity_type_routes.delete("/{id}/hard")
@api_handler
def hard_delete_unity_type(id: int) -> dict:
    response = UnityTypeUseCase().hard_delete(id)
    return response.dict()


@unity_type_routes.get("")
@api_handler
def list_unity_types(
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
    usage_class: Optional[str] = Query(
        None,
        description="Filter by usage class: residential|commercial|parking|storage|service.",
    ),
    include_deleted: bool = Query(
        False,
        description="Include soft-deleted records.",
    ),
) -> dict:
    if limit > 500:
        limit = 500
    response = UnityTypeUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        include_system=include_system,
        status=status,
        usage_class=usage_class,
        include_deleted=include_deleted,
    )
    return response.dict()
