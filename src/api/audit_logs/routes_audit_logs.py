# =============================================================================
# API Routes: core_audit_logs — read-only audit trail
#
# Endpoints:
#   GET    /audit-logs                       — list with filters
#   GET    /audit-logs/{id}                — get by id
#   GET    /audit-logs/resource/{rt}/{rid} — list by resource
#   GET    /audit-logs/user/{uid}           — list by user
# =============================================================================

from fastapi import APIRouter, Query

from library.dddpy.core_audit_logs.usecase.audit_query_usecase import AuditQueryUseCase
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/audit-logs"
audit_log_routes = APIRouter(prefix=PREFIX)


@audit_log_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_audit_logs"}


@audit_log_routes.get("")
@api_handler
def list_audit_logs(
    action: str = Query(None, description="Filter by action: create, update, delete, restore"),
    resource_type: str = Query(None, description="Filter by resource type"),
    user_id: int = Query(None, description="Filter by user ID"),
    date_from: str = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: str = Query(None, description="Filter to date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """
    List audit logs with optional filters.
    Audit log is read-only — no create, update, or delete endpoints.
    """
    from datetime import date as date_class
    parsed_date_from = None
    parsed_date_to = None
    if date_from:
        try:
            parsed_date_from = date_class.fromisoformat(date_from)
        except ValueError:
            pass
    if date_to:
        try:
            parsed_date_to = date_class.fromisoformat(date_to)
        except ValueError:
            pass

    response = AuditQueryUseCase().list_all(
        action=action,
        resource_type=resource_type,
        user_id=user_id,
        date_from=parsed_date_from,
        date_to=parsed_date_to,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@audit_log_routes.get("/{id}")
@api_handler
def get_audit_log(id: int) -> dict:
    """Get a specific audit log entry by id."""
    response = AuditQueryUseCase().get_by_id(id)
    return response.dict()


@audit_log_routes.get("/resource/{resource_type}/{resource_id}")
@api_handler
def list_by_resource(
    resource_type: str,
    resource_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List audit trail for a specific resource (e.g. /resource/charge/42)."""
    response = AuditQueryUseCase().list_by_resource(
        resource_type=resource_type,
        resource_id=resource_id,
        skip=skip,
        limit=limit,
    )
    return response.dict()


@audit_log_routes.get("/user/{user_id}")
@api_handler
def list_by_user(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List all audit logs for a specific user."""
    response = AuditQueryUseCase().list_by_user(
        user_id=user_id,
        skip=skip,
        limit=limit,
    )
    return response.dict()