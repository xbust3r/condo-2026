# =============================================================================
# API Routes: core_charges
# Módulo de cargos recurrentes y extraordinarios del condominio
#
# Endpoints:
#   POST   /charges                    — create  [RBAC: charge.write]
#   GET    /charges                    — list   [RBAC: charge.read]
#   GET    /charges/{id}             — get    [RBAC: charge.read]
#   GET    /charges/uuid/{uuid}      — get    [RBAC: charge.read]
#   PUT    /charges/{id}             — update [RBAC: charge.write]
#   DELETE /charges/{id}             — soft delete [RBAC: charge.write]
#   POST   /charges/{id}/restore     — restore [RBAC: charge.write]
#   DELETE /charges/{id}/hard        — hard delete [RBAC: charge.delete]
# =============================================================================

from typing import Optional
from fastapi import APIRouter, Depends, Query

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.core_charges.usecase.charge_usecase import ChargeUseCase
from library.dddpy.core_charges.usecase.charge_cmd_schema import (
    CreateChargeSchema,
    UpdateChargeSchema,
)
from library.dddpy.core_permissions.infrastructure.permission_query_repository import (
    PermissionQueryRepositoryImpl,
)
from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
    CondominiumRoleQueryRepositoryImpl,
)
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.shared.decorators.rbac_handler import rbac_required


PREFIX = "/charges"
charge_routes = APIRouter(prefix=PREFIX)


@charge_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_charges"}


def _check_rbac(user: UserIdentity, permission_code: str, scope_id: int) -> None:
    """
    Verify user has permission_code for a given condominium scope.
    Raises HTTPException 403 if not authorized.
    """
    from fastapi import HTTPException
    perm_repo = PermissionQueryRepositoryImpl()
    role_repo = CondominiumRoleQueryRepositoryImpl()

    perm = perm_repo.get_by_code(permission_code)
    if not perm:
        raise HTTPException(status_code=500, detail=f"Permission '{permission_code}' not found in system")

    # super_admin bypass
    roles, _ = role_repo.list_by_user(user_id=user.id, status="active", include_deleted=False)
    if any(r.role == "super_admin" and r.is_active() for r in roles):
        return

    # Check permission at condominium scope
    user_roles, _ = role_repo.list_by_user_and_condominium(
        user_id=user.id, condominium_id=scope_id, status="active", include_deleted=False
    )
    if not user_roles:
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied: '{permission_code}' required. "
                   f"Contact your administrator if you believe this is an error.",
        )


@charge_routes.post("")
@api_handler
def create_charge(
    request: CreateChargeSchema,
    user: UserIdentity = Depends(rbac_required("charge", "write")),
) -> dict:
    """
    Create a new charge.

    For global recurrent charges (is_recurrent=True, unit_id=null),
    the response includes `ar_generation_needed: true` — the caller
    must invoke the AR generation flow after this returns.

    RBAC: charge.write on condominium_id from request body.
    """
    _check_rbac(user, "charge.write", request.condominium_id)
    response = ChargeUseCase().create(request)
    return response.dict()


@charge_routes.get("")
@api_handler
def list_charges(
    condominium_id: Optional[int] = Query(None),
    charge_type_id: Optional[int] = Query(None),
    unit_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    is_recurrent: Optional[bool] = Query(None),
    include_deleted: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: UserIdentity = Depends(rbac_required("charge", "read")),
) -> dict:
    """List charges with optional filters."""
    if condominium_id:
        _check_rbac(user, "charge.read", condominium_id)
    response = ChargeUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        charge_type_id=charge_type_id,
        unit_id=unit_id,
        status=status,
        is_recurrent=is_recurrent,
        include_deleted=include_deleted,
    )
    return response.dict()


@charge_routes.get("/{id}")
@api_handler
def get_charge(
    id: int,
    user: UserIdentity = Depends(rbac_required("charge", "read")),
) -> dict:
    """Get a charge by id."""
    response = ChargeUseCase().get_by_id(id)
    if response.data and (response.data.get("condominium_id") or response.data.get("charge", {}).get("condominium_id")):
        condo_id = response.data.get("condominium_id") or response.data.get("charge", {}).get("condominium_id")
        if condo_id:
            _check_rbac(user, "charge.read", condo_id)
    return response.dict()


@charge_routes.get("/uuid/{uuid}")
@api_handler
def get_charge_by_uuid(
    uuid: str,
    user: UserIdentity = Depends(rbac_required("charge", "read")),
) -> dict:
    """Get a charge by uuid."""
    response = ChargeUseCase().get_by_uuid(uuid)
    if response.data and (response.data.get("condominium_id") or response.data.get("charge", {}).get("condominium_id")):
        condo_id = response.data.get("condominium_id") or response.data.get("charge", {}).get("condominium_id")
        if condo_id:
            _check_rbac(user, "charge.read", condo_id)
    return response.dict()


@charge_routes.put("/{id}")
@api_handler
def update_charge(
    id: int,
    request: UpdateChargeSchema,
    user: UserIdentity = Depends(rbac_required("charge", "write")),
) -> dict:
    """Update a charge (amount, description, dates, status)."""
    # Get current charge to know its condominium
    existing = ChargeUseCase().get_by_id(id)
    condo_id = existing.data.get("condominium_id") if existing.data else None
    if condo_id:
        _check_rbac(user, "charge.write", condo_id)
    response = ChargeUseCase().update(id, request)
    return response.dict()


@charge_routes.delete("/{id}")
@api_handler
def delete_charge(
    id: int,
    user: UserIdentity = Depends(rbac_required("charge", "write")),
) -> dict:
    """Soft delete a charge."""
    existing = ChargeUseCase().get_by_id(id)
    condo_id = existing.data.get("condominium_id") if existing.data else None
    if condo_id:
        _check_rbac(user, "charge.write", condo_id)
    response = ChargeUseCase().soft_delete(id)
    return response.dict()


@charge_routes.post("/{id}/restore")
@api_handler
def restore_charge(
    id: int,
    user: UserIdentity = Depends(rbac_required("charge", "write")),
) -> dict:
    """Restore a soft-deleted charge."""
    existing = ChargeUseCase().get_by_id(id)
    condo_id = existing.data.get("condominium_id") if existing.data else None
    if condo_id:
        _check_rbac(user, "charge.write", condo_id)
    response = ChargeUseCase().restore(id)
    return response.dict()


@charge_routes.delete("/{id}/hard")
@api_handler
def hard_delete_charge(
    id: int,
    user: UserIdentity = Depends(rbac_required("charge", "delete")),
) -> dict:
    """Hard delete a charge (permanent). Requires charge.delete permission."""
    existing = ChargeUseCase().get_by_id(id)
    condo_id = existing.data.get("condominium_id") if existing.data else None
    if condo_id:
        _check_rbac(user, "charge.delete", condo_id)
    response = ChargeUseCase().hard_delete(id)
    return response.dict()
