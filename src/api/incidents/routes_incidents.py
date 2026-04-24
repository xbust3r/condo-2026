# =============================================================================
# API Routes: core_incidents
# Maintenance ticketing / incident reporting system
#
# Endpoints:
#   POST   /incidents                         — create (INC-01 validated)
#   GET    /incidents                         — list with filters
#   GET    /incidents/{id}                    — get by id
#   GET    /incidents/uuid/{uuid}             — get by uuid
#   GET    /incidents/my                      — my incidents (reported_by = current user)
#   PATCH  /incidents/{id}                   — update (admin/staff)
#   POST   /incidents/{id}/assign            — assign to user (admin/staff)
#   POST   /incidents/{id}/escalate          — mark as escalated (admin)
#   POST   /incidents/{id}/complete          — mark completed (staff/admin)
#   POST   /incidents/{id}/close             — close (admin)
#   POST   /incidents/{id}/cancel            — cancel (admin)
#
# Condominium-scoped:
#   GET    /condominiums/{id}/incidents      — list by condominium (paginated)
# =============================================================================

from typing import Optional
from fastapi import APIRouter, Query, Depends, Path
from typing import Optional

from library.dddpy.core_incidents.usecase.incident_factory import (
    incident_cmd_usecase_factory,
    incident_query_usecase_factory,
)
from library.dddpy.core_incidents.usecase.incident_cmd_schema import (
    CreateIncidentSchema,
    UpdateIncidentSchema,
)
from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.shared.decorators.rbac_handler import rbac_required
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/incidents"
incident_routes = APIRouter(prefix=PREFIX)

# Separate router for condominium-scoped endpoints
CONDOMINIUM_PREFIX = "/condominiums"
condominium_incident_routes = APIRouter(prefix=CONDOMINIUM_PREFIX)


@incident_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_incidents"}


@incident_routes.post("")
@api_handler
def create_incident(
    request: CreateIncidentSchema,
    user: UserIdentity = Depends(rbac_required("incident", "create", "condominium_id")),
) -> dict:
    """
    Create a new incident.
    INC-01: User must have active occupancy or ownership in the unit.
    RBAC: incident.create permission.
    """
    cmd_usecase = incident_cmd_usecase_factory()
    result = cmd_usecase.create(data=request, reported_by_user_id=user.id)
    return result.to_dict()


@incident_routes.get("")
@api_handler
def list_incidents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    condominium_id: Optional[int] = Query(None),
    building_id: Optional[int] = Query(None),
    unit_id: Optional[int] = Query(None),
    reported_by_user_id: Optional[int] = Query(None),
    assigned_to_user_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    is_escalated: Optional[bool] = Query(None),
    include_deleted: bool = Query(False),
    user: UserIdentity = Depends(rbac_required("incident", "read")),
) -> dict:
    """List incidents with optional filters."""
    query_usecase = incident_query_usecase_factory()
    incidents, total = query_usecase.list_all(
        skip=skip,
        limit=limit,
        condominium_id=condominium_id,
        building_id=building_id,
        unit_id=unit_id,
        reported_by_user_id=reported_by_user_id,
        assigned_to_user_id=assigned_to_user_id,
        category=category,
        priority=priority,
        status=status,
        is_escalated=is_escalated,
        include_deleted=include_deleted,
    )
    return {
        "items": [i.to_dict() for i in incidents],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@incident_routes.get("/my")
@api_handler
def list_my_incidents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
    user: UserIdentity = Depends(rbac_required("incident", "read")),
) -> dict:
    """My incidents (reported_by = current user)."""
    query_usecase = incident_query_usecase_factory()
    incidents, total = query_usecase.list_by_user(
        user_id=user.id,
        skip=skip,
        limit=limit,
        status=status,
        include_deleted=include_deleted,
    )
    return {
        "items": [i.to_dict() for i in incidents],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@incident_routes.get("/{id}")
@api_handler
def get_incident(
    id: int,
    user: UserIdentity = Depends(rbac_required("incident", "read")),
) -> dict:
    """Get an incident by id."""
    query_usecase = incident_query_usecase_factory()
    result = query_usecase.get_by_id(id)
    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Incident not found")
    return result.to_dict()


@incident_routes.get("/uuid/{uuid}")
@api_handler
def get_incident_by_uuid(
    uuid: str,
    user: UserIdentity = Depends(rbac_required("incident", "read")),
) -> dict:
    """Get an incident by uuid."""
    query_usecase = incident_query_usecase_factory()
    result = query_usecase.get_by_uuid(uuid)
    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Incident not found")
    return result.to_dict()


@incident_routes.patch("/{id}")
@api_handler
def update_incident(
    id: int,
    request: UpdateIncidentSchema,
    user: UserIdentity = Depends(rbac_required("incident", "update")),
) -> dict:
    """Update an incident (admin/staff)."""
    cmd_usecase = incident_cmd_usecase_factory()
    result = cmd_usecase.update(id=id, data=request, requesting_user_id=user.id)
    return result.to_dict()


@incident_routes.post("/{id}/assign")
@api_handler
def assign_incident(
    id: int,
    assigned_to_user_id: int = Query(..., description="User ID to assign to"),
    user: UserIdentity = Depends(rbac_required("incident", "assign")),
) -> dict:
    """Assign incident to a staff/contractor user (admin/staff)."""
    cmd_usecase = incident_cmd_usecase_factory()
    result = cmd_usecase.assign(id=id, assigned_to_user_id=assigned_to_user_id)
    return result.to_dict()


@incident_routes.post("/{id}/escalate")
@api_handler
def escalate_incident(
    id: int,
    user: UserIdentity = Depends(rbac_required("incident", "escalate")),
) -> dict:
    """Mark incident as escalated (admin)."""
    cmd_usecase = incident_cmd_usecase_factory()
    result = cmd_usecase.escalate(id=id)
    return result.to_dict()


@incident_routes.post("/{id}/complete")
@api_handler
def complete_incident(
    id: int,
    resolution_notes: Optional[str] = Query(None),
    user: UserIdentity = Depends(rbac_required("incident", "update")),
) -> dict:
    """Mark incident as completed (set completed_date, status=resolved) (staff/admin)."""
    cmd_usecase = incident_cmd_usecase_factory()
    result = cmd_usecase.complete(id=id, resolution_notes=resolution_notes)
    return result.to_dict()


@incident_routes.post("/{id}/close")
@api_handler
def close_incident(
    id: int,
    user: UserIdentity = Depends(rbac_required("incident", "update")),
) -> dict:
    """Close an incident (admin). Requires completed_date."""
    cmd_usecase = incident_cmd_usecase_factory()
    result = cmd_usecase.close(id=id)
    return result.to_dict()


@incident_routes.post("/{id}/cancel")
@api_handler
def cancel_incident(
    id: int,
    user: UserIdentity = Depends(rbac_required("incident", "update")),
) -> dict:
    """Cancel an incident (admin)."""
    cmd_usecase = incident_cmd_usecase_factory()
    result = cmd_usecase.cancel(id=id)
    return result.to_dict()


# ── Condominium-scoped endpoints ─────────────────────────────────────────────

@condominium_incident_routes.get("/{condominium_id}/incidents")
@api_handler
def list_condominium_incidents(
    condominium_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    building_id: Optional[int] = Query(None),
    unit_id: Optional[int] = Query(None),
    assigned_to_user_id: Optional[int] = Query(None),
    is_escalated: Optional[bool] = Query(None),
    include_deleted: bool = Query(False),
    user: UserIdentity = Depends(rbac_required("incident", "read", "condominium_id")),
) -> dict:
    """List incidents for a condominium (paginated)."""
    query_usecase = incident_query_usecase_factory()
    incidents, total = query_usecase.list_by_condominium(
        condominium_id=condominium_id,
        skip=skip,
        limit=limit,
        status=status,
        priority=priority,
        category=category,
        building_id=building_id,
        unit_id=unit_id,
        assigned_to_user_id=assigned_to_user_id,
        is_escalated=is_escalated,
        include_deleted=include_deleted,
    )
    return {
        "items": [i.to_dict() for i in incidents],
        "total": total,
        "skip": skip,
        "limit": limit,
    }
