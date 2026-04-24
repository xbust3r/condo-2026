"""
API Routes: core_visitors
Visitor / access management system

Endpoints:
  POST   /visitors                          — create (VIS-01 validated)
  GET    /visitors                         — list with filters
  GET    /visitors/{id}                    — get by id
  GET    /visitors/uuid/{uuid}             — get by uuid
  GET    /visitors/my                      — my registered visits
  GET    /visitors/unit/{unit_id}           — visits by unit (host only)
  PATCH  /visitors/{id}                    — update (host)
  POST   /visitors/{id}/cancel             — cancel (host)
  POST   /visitors/{id}/check-in           — check-in (security staff)
  POST   /visitors/{id}/check-out          — check-out (security staff)
  GET    /visitors/access-code/{code}      — lookup by access code (security)

Condominium-scoped:
  GET    /condominiums/{id}/visitors       — list by condominium (paginated)
"""

from fastapi import APIRouter, Query, Depends, Path
from typing import Optional

from library.dddpy.core_visitors.usecase.visitor_factory import (
    visitor_cmd_usecase_factory,
    visitor_query_usecase_factory,
)
from library.dddpy.core_visitors.usecase.visitor_cmd_schema import (
    CreateVisitorSchema,
    UpdateVisitorSchema,
)
from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.shared.decorators.rbac_handler import rbac_required
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/visitors"
visitor_routes = APIRouter(prefix=PREFIX)

CONDOMINIUM_PREFIX = "/condominiums"
condominium_visitor_routes = APIRouter(prefix=CONDOMINIUM_PREFIX)


@visitor_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_visitors"}


@visitor_routes.post("")
@api_handler
def create_visitor(
    request: CreateVisitorSchema,
    user: UserIdentity = Depends(rbac_required("visitors", "create", "condominium_id")),
) -> dict:
    """
    Register a new visitor.
    VIS-01: User must have active occupancy or ownership in the unit.
    RBAC: visitors:create permission.
    """
    cmd_usecase = visitor_cmd_usecase_factory()
    result = cmd_usecase.create(data=request, host_user_id=user.id)
    return result.to_dict()


@visitor_routes.get("")
@api_handler
def list_visitors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    condominium_id: Optional[int] = Query(None),
    building_id: Optional[int] = Query(None),
    unit_id: Optional[int] = Query(None),
    host_user_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    expected_date: Optional[str] = Query(None),
    visit_purpose: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
    user: UserIdentity = Depends(rbac_required("visitors", "read")),
) -> dict:
    """List visitors with optional filters."""
    query_usecase = visitor_query_usecase_factory()
    visitors, total = query_usecase.list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        building_id=building_id,
        unit_id=unit_id,
        host_user_id=host_user_id,
        status=status,
        expected_date=expected_date,
        visit_purpose=visit_purpose,
        include_deleted=include_deleted,
    )
    return {
        "items": [v.to_dict() for v in visitors],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@visitor_routes.get("/my")
@api_handler
def list_my_visitors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
    user: UserIdentity = Depends(rbac_required("visitors", "read")),
) -> dict:
    """My registered visits (host_user_id = current user)."""
    query_usecase = visitor_query_usecase_factory()
    visitors, total = query_usecase.list_by_host(
        host_user_id=user.id,
        skip=skip,
        limit=limit,
        status=status,
        include_deleted=include_deleted,
    )
    return {
        "items": [v.to_dict() for v in visitors],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@visitor_routes.get("/{id}")
@api_handler
def get_visitor(
    id: int,
    user: UserIdentity = Depends(rbac_required("visitors", "read")),
) -> dict:
    """Get a visitor by id."""
    query_usecase = visitor_query_usecase_factory()
    result = query_usecase.get_by_id(id)
    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Visitor not found")
    return result.to_dict()


@visitor_routes.get("/uuid/{uuid}")
@api_handler
def get_visitor_by_uuid(
    uuid: str,
    user: UserIdentity = Depends(rbac_required("visitors", "read")),
) -> dict:
    """Get a visitor by uuid."""
    query_usecase = visitor_query_usecase_factory()
    result = query_usecase.get_by_uuid(uuid)
    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Visitor not found")
    return result.to_dict()


@visitor_routes.get("/unit/{unit_id}")
@api_handler
def list_visitors_by_unit(
    unit_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
    user: UserIdentity = Depends(rbac_required("visitors", "read")),
) -> dict:
    """List visitors for a specific unit (host only)."""
    query_usecase = visitor_query_usecase_factory()
    visitors, total = query_usecase.list_by_unit(
        unit_id=unit_id,
        skip=skip,
        limit=limit,
        status=status,
        include_deleted=include_deleted,
    )
    return {
        "items": [v.to_dict() for v in visitors],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@visitor_routes.patch("/{id}")
@api_handler
def update_visitor(
    id: int,
    request: UpdateVisitorSchema,
    user: UserIdentity = Depends(rbac_required("visitors", "update")),
) -> dict:
    """Update a visitor (host only — can update notes, expected_time, visit_purpose)."""
    cmd_usecase = visitor_cmd_usecase_factory()
    result = cmd_usecase.update(id=id, data=request, requesting_user_id=user.id)
    return result.to_dict()


@visitor_routes.post("/{id}/cancel")
@api_handler
def cancel_visitor(
    id: int,
    user: UserIdentity = Depends(rbac_required("visitors", "cancel")),
) -> dict:
    """Cancel a visitor registration (host only, must be pending)."""
    cmd_usecase = visitor_cmd_usecase_factory()
    result = cmd_usecase.cancel(id=id, requesting_user_id=user.id)
    return result.to_dict()


@visitor_routes.post("/{id}/check-in")
@api_handler
def check_in_visitor(
    id: int,
    user: UserIdentity = Depends(rbac_required("visitors", "checkin")),
) -> dict:
    """
    Register visitor arrival (security staff only).
    VIS-03: sets actual_checkin_at=now, status=checked_in.
    """
    cmd_usecase = visitor_cmd_usecase_factory()
    result = cmd_usecase.check_in(id=id, requesting_user_id=user.id)
    return result.to_dict()


@visitor_routes.post("/{id}/check-out")
@api_handler
def check_out_visitor(
    id: int,
    user: UserIdentity = Depends(rbac_required("visitors", "checkin")),
) -> dict:
    """
    Register visitor departure (security staff only).
    VIS-03: sets actual_checkout_at=now, status=checked_out.
    VIS-04: visitor must be checked_in first.
    """
    cmd_usecase = visitor_cmd_usecase_factory()
    result = cmd_usecase.check_out(id=id, requesting_user_id=user.id)
    return result.to_dict()


@visitor_routes.get("/access-code/{code}")
@api_handler
def get_visitor_by_access_code(
    code: str,
    condominium_id: Optional[int] = Query(None),
    user: UserIdentity = Depends(rbac_required("visitors", "checkin")),
) -> dict:
    """
    Lookup a visitor by access code (security desk use case).
    Used at the entrance gate to verify a visitor's registration.
    """
    query_usecase = visitor_query_usecase_factory()
    result = query_usecase.get_by_access_code(code, condominium_id)
    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Visitor not found for this access code")
    return result.to_dict()


# ── Condominium-scoped endpoints ─────────────────────────────────────────────

@condominium_visitor_routes.get("/{condominium_id}/visitors")
@api_handler
def list_condominium_visitors(
    condominium_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None),
    expected_date: Optional[str] = Query(None),
    visit_purpose: Optional[str] = Query(None),
    building_id: Optional[int] = Query(None),
    unit_id: Optional[int] = Query(None),
    include_deleted: bool = Query(False),
    user: UserIdentity = Depends(rbac_required("visitors", "read", "condominium_id")),
) -> dict:
    """List visitors for a condominium (paginated)."""
    query_usecase = visitor_query_usecase_factory()
    visitors, total = query_usecase.list_by_condominium(
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
        status=status,
        expected_date=expected_date,
        visit_purpose=visit_purpose,
        building_id=building_id,
        unit_id=unit_id,
        include_deleted=include_deleted,
    )
    return {
        "items": [v.to_dict() for v in visitors],
        "total": total,
        "skip": skip,
        "limit": limit,
    }