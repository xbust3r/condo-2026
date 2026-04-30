# =============================================================================
# API Routes: core_accounts_receivable
# Módulo de cuentas por cobrar del condominio
#
# Endpoints:
#   POST   /accounts-receivable                        — create       [RBAC: ar.write]
#   POST   /accounts-receivable/generate-from-charge  — batch        [RBAC: ar.write]
#   GET    /accounts-receivable                        — list         [RBAC: ar.read]
#   GET    /accounts-receivable/{id}                 — get          [RBAC: ar.read]
#   GET    /accounts-receivable/uuid/{uuid}          — get          [RBAC: ar.read]
#   GET    /accounts-receivable/unit/{unit_id}/summary — summary     [RBAC: ar.read]
#   GET    /accounts-receivable/overdue              — overdue      [RBAC: ar.read]
#   PUT    /accounts-receivable/{id}                 — update       [RBAC: ar.write]
#   POST   /accounts-receivable/{id}/payment         — record       [RBAC: ar.write]
#   DELETE /accounts-receivable/{id}                 — soft delete  [RBAC: ar.delete]
#   POST   /accounts-receivable/{id}/restore          — restore     [RBAC: ar.write]
#   DELETE /accounts-receivable/{id}/hard             — hard delete [RBAC: ar.delete]
# =============================================================================

from typing import Optional
from fastapi import APIRouter, Depends, Query

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.core_accounts_receivable.usecase.ar_usecase import ARUseCase
from library.dddpy.core_accounts_receivable.usecase.ar_cmd_schema import (
    CreateARSchema,
    UpdateARSchema,
    RecordPaymentSchema,
    CreateARBatchSchema,
)
from library.dddpy.shared.decorators.api_handler import api_handler
from library.dddpy.shared.decorators.rbac_handler import rbac_required


PREFIX = "/accounts-receivable"

ar_routes = APIRouter(prefix=PREFIX)


@ar_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_accounts_receivable"}


@ar_routes.post("")
@api_handler
def create_ar(
    request: CreateARSchema,
    user: UserIdentity = Depends(rbac_required("ar", "write")),
) -> dict:
    """Create a single accounts receivable entry."""
    response = ARUseCase().create(request)
    return response.dict()


@ar_routes.post("/generate-from-charge")
@api_handler
def generate_ar_from_charge(
    request: CreateARBatchSchema,
    user: UserIdentity = Depends(rbac_required("ar", "write")),
) -> dict:
    """
    Generate AR entries for all active units from a global charge.
    One AR per active unit, debtor = primary occupant or owner.
    """
    response = ARUseCase().generate_from_charge(
        charge_id=request.charge_id,
        due_date=request.due_date,
        period=request.period,
    )
    return response.dict()


@ar_routes.get("")
@api_handler
def list_ar(
    condominium_id: Optional[int] = Query(None, description="Filter by condominium"),
    unit_id: Optional[int] = Query(None, description="Filter by unit"),
    debtor_user_id: Optional[int] = Query(None, description="Filter by debtor user"),
    status: Optional[str] = Query(None, description="Filter by status"),
    charge_id: Optional[int] = Query(None, description="Filter by charge"),
    include_deleted: bool = Query(False, description="Include soft-deleted"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: UserIdentity = Depends(rbac_required("ar", "read")),
) -> dict:
    """List accounts receivable with optional filters."""
    response = ARUseCase().list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        unit_id=unit_id,
        debtor_user_id=debtor_user_id,
        status=status,
        charge_id=charge_id,
        include_deleted=include_deleted,
    )
    return response.dict()


@ar_routes.get("/overdue")
@api_handler
def list_overdue_ar(
    condominium_id: int = Query(..., description="Condominium ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user: UserIdentity = Depends(rbac_required("ar", "read")),
) -> dict:
    """List overdue AR entries for a condominium."""
    response = ARUseCase().list_overdue(
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@ar_routes.get("/unit/{unit_id}/summary")
@api_handler
def get_ar_summary_by_unit(
    unit_id: int,
    user: UserIdentity = Depends(rbac_required("ar", "read")),
) -> dict:
    """Get debt summary for a unit: total debt, pending, overdue count."""
    response = ARUseCase().get_summary_by_unit(unit_id)
    return response.dict()


@ar_routes.get("/{id}")
@api_handler
def get_ar(
    id: int,
    user: UserIdentity = Depends(rbac_required("ar", "read")),
) -> dict:
    """Get an AR entry by id."""
    response = ARUseCase().get_by_id(id)
    return response.dict()


@ar_routes.get("/uuid/{uuid}")
@api_handler
def get_ar_by_uuid(
    uuid: str,
    user: UserIdentity = Depends(rbac_required("ar", "read")),
) -> dict:
    """Get an AR entry by uuid."""
    response = ARUseCase().get_by_uuid(uuid)
    return response.dict()


@ar_routes.put("/{id}")
@api_handler
def update_ar(
    id: int,
    request: UpdateARSchema,
    user: UserIdentity = Depends(rbac_required("ar", "write")),
) -> dict:
    """Update an AR entry (description, due_date, status)."""
    response = ARUseCase().update(id, request)
    return response.dict()


@ar_routes.post("/{id}/payment")
@api_handler
def record_ar_payment(
    id: int,
    request: RecordPaymentSchema,
    user: UserIdentity = Depends(rbac_required("ar", "write")),
) -> dict:
    """
    Record a payment against an AR.

    Automatically recalculates AR status:
    - pending → partial (first payment)
    - overdue → partial
    - partial/pending → paid (when paid_amount == amount)
    """
    response = ARUseCase().record_payment(id, request)
    return response.dict()


@ar_routes.delete("/{id}")
@api_handler
def delete_ar(
    id: int,
    user: UserIdentity = Depends(rbac_required("ar", "delete")),
) -> dict:
    """Soft delete an AR entry."""
    response = ARUseCase().soft_delete(id)
    return response.dict()


@ar_routes.post("/{id}/restore")
@api_handler
def restore_ar(
    id: int,
    user: UserIdentity = Depends(rbac_required("ar", "write")),
) -> dict:
    """Restore a soft-deleted AR entry."""
    response = ARUseCase().restore(id)
    return response.dict()


@ar_routes.delete("/{id}/hard")
@api_handler
def hard_delete_ar(
    id: int,
    user: UserIdentity = Depends(rbac_required("ar", "delete")),
) -> dict:
    """Hard delete an AR entry (permanent)."""
    response = ARUseCase().hard_delete(id)
    return response.dict()
