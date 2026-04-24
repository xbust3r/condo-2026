# =============================================================================
# API Routes: core_unit_types + public alias
# =============================================================================
# Endpoints (core_unit_types — auth required for mutations, mixed for list):
#   POST   /core_unit_types               — create
#   GET    /core_unit_types/{id}          — get by id
#   GET    /core_unit_types/uuid/{uuid}   — get by uuid
#   PUT    /core_unit_types/{id}          — update
#   DELETE /core_unit_types/{id}          — soft delete
#   POST   /core_unit_types/{id}/restore  — restore
#   DELETE /core_unit_types/{id}/hard     — hard delete
#   GET    /core_unit_types               — list with filters (mixed access)
#
# Public alias (BE-UT-04):
#   GET    /unit-types                    — list global types only, no auth
#
# ACCESS RULES — list endpoint (BE-UT-03):
#   - sin auth → devuelve solo globales (condominium_id=NULL)
#   - con auth + rol en condominio X → globales + custom de X
#   - con auth pero sin rol en condominio X → 403
# =============================================================================

from fastapi import APIRouter, Query, Depends
from typing import Optional

from library.dddpy.core_unit_types.usecase.unit_type_usecase import (
    UnitTypeUseCase,
)
from library.dddpy.core_unit_types.usecase.unit_type_cmd_schema import (
    CreateUnitTypeSchema,
    UpdateUnitTypeSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.auth.domain.user_identity import UserIdentity
from api.auth.auth_dependencies import get_current_user, get_optional_user
from api.auth.rbac_dependencies import require_condominium_role


PREFIX = "/core_unit_types"
unit_type_routes = APIRouter(prefix=PREFIX)

# Public alias router for /unit-types (BE-UT-04)
public_unit_type_routes = APIRouter(prefix="")


@unit_type_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_unit_types"}


@unit_type_routes.post("")
@api_handler
def create_unit_type(request: CreateUnitTypeSchema) -> dict:
    response = UnitTypeUseCase().create(request)
    return response.dict()


@unit_type_routes.get("/{id}")
@api_handler
def get_unit_type(id: int) -> dict:
    response = UnitTypeUseCase().get_by_id(id)
    return response.dict()


@unit_type_routes.get("/uuid/{uuid}")
@api_handler
def get_unit_type_by_uuid(uuid: str) -> dict:
    response = UnitTypeUseCase().get_by_uuid(uuid)
    return response.dict()


@unit_type_routes.put("/{id}")
@api_handler
def update_unit_type(id: int, request: UpdateUnitTypeSchema) -> dict:
    response = UnitTypeUseCase().update(id, request)
    return response.dict()


@unit_type_routes.delete("/{id}")
@api_handler
def delete_unit_type(id: int) -> dict:
    response = UnitTypeUseCase().soft_delete(id)
    return response.dict()


@unit_type_routes.post("/{id}/restore")
@api_handler
def restore_unit_type(id: int) -> dict:
    response = UnitTypeUseCase().restore(id)
    return response.dict()


@unit_type_routes.delete("/{id}/hard")
@api_handler
def hard_delete_unit_type(id: int) -> dict:
    response = UnitTypeUseCase().hard_delete(id)
    return response.dict()


@unit_type_routes.get("")
@api_handler
def list_unit_types(
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
    user: Optional[UserIdentity] = Depends(get_optional_user),
) -> dict:
    """
    Mixed-access list endpoint (BE-UT-03):
    - Sin auth: devuelve SOLO globales (condominium_id=NULL, is_system=1)
    - Con auth + condominium_id=X: valida rol, devuelve globales + custom de X
    - Con auth sin condominium_id: devuelve solo globales
    - Con auth pero sin rol en X: 403
    """
    if limit > 500:
        limit = 500

    if user is None:
        # Acceso público: solo globales
        response = UnitTypeUseCase().list_all(
            skip=skip,
            limit=limit,
            condominium_id=None,
            include_system=True,
            status=status,
            usage_class=usage_class,
            include_deleted=include_deleted,
        )
        return response.dict()

    # Acceso autenticado
    if condominium_id is not None:
        # Validar rol en el condominio específico — lanza 403 si no tiene
        require_condominium_role(user, condominium_id)
        # Usuario con rol: devolver globales + custom del condominio
        response = UnitTypeUseCase().list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            include_system=True,
            status=status,
            usage_class=usage_class,
            include_deleted=include_deleted,
        )
        return response.dict()

    # Auth pero sin condominium_id: devolver globales
    response = UnitTypeUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=None,
        include_system=True,
        status=status,
        usage_class=usage_class,
        include_deleted=include_deleted,
    )
    return response.dict()


# =============================================================================
# Public alias /unit-types (BE-UT-04)
# Always returns global system types only — no auth required
# =============================================================================

@public_unit_type_routes.get("/unit-types")
@api_handler
def list_public_unit_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[int] = Query(
        None,
        description="Filter by status (1=active, 0=inactive).",
    ),
    usage_class: Optional[str] = Query(
        None,
        description="Filter by usage class: residential|commercial|parking|storage|service.",
    ),
) -> dict:
    """
    Public endpoint — returns only global system unit types.
    No authentication required.
    This is the clean alias for backdmin's unit-types page.
    """
    if limit > 500:
        limit = 500
    response = UnitTypeUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=None,
        include_system=True,
        status=status,
        usage_class=usage_class,
        include_deleted=False,
    )
    return response.dict()