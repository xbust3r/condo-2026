# =============================================================================
# API Routes: core_permissions
# Catálogo de permisos RBAC — solo lectura (seed de DB, no editable por API)
#
# Endpoints:
#   GET  /permissions                     — list all (with optional resource/action filter)
#   GET  /permissions/{id}              — get by id
#   GET  /permissions/code/{code}       — get by code
#   GET  /permissions/resource/{resource} — list by resource
# =============================================================================

from fastapi import APIRouter, Query

from library.dddpy.core_permissions.usecase.permission_query_usecase import PermissionQueryUseCase
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/permissions"

permission_routes = APIRouter(prefix=PREFIX)


@permission_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_permissions"}


@permission_routes.get("")
@api_handler
def list_permissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    resource: str = Query(None, description="Filter by resource (e.g. 'building', 'finance')"),
    action: str = Query(None, description="Filter by action (e.g. 'read', 'create')"),
) -> dict:
    use_case = PermissionQueryUseCase()

    if resource:
        result, total = use_case.list_by_resource(resource=resource, skip=skip, limit=limit)
    elif action:
        result, total = use_case.list_by_action(action=action, skip=skip, limit=limit)
    else:
        result, total = use_case.list_all(skip=skip, limit=limit)

    return {
        "data": [p.to_dict() for p in result],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@permission_routes.get("/{id}")
@api_handler
def get_permission_by_id(id: int) -> dict:
    use_case = PermissionQueryUseCase()
    entity = use_case.get_by_id(id)
    return entity.to_dict()


@permission_routes.get("/code/{code}")
@api_handler
def get_permission_by_code(code: str) -> dict:
    use_case = PermissionQueryUseCase()
    entity = use_case.get_by_code(code)
    return entity.to_dict()


@permission_routes.get("/resource/{resource}")
@api_handler
def list_permissions_by_resource(
    resource: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    use_case = PermissionQueryUseCase()
    result, total = use_case.list_by_resource(resource=resource, skip=skip, limit=limit)
    return {
        "data": [p.to_dict() for p in result],
        "total": total,
        "skip": skip,
        "limit": limit,
    }
