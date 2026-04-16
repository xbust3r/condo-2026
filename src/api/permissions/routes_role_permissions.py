"""
API Routes: role-permissions
Mapeos entre roles y permisos RBAC (read-only).

Endpoints:
  GET  /role-permissions/{role}   — list all permissions assigned to a role
"""
from fastapi import APIRouter, Query

from library.dddpy.core_role_permissions.usecase.role_permission_query_usecase import RolePermissionQueryUseCase
from library.dddpy.core_role_permissions.usecase.role_permission_factory import (
    role_permission_query_usecase_factory,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/role-permissions"

role_permission_routes = APIRouter(prefix=PREFIX)


@role_permission_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "role_permissions"}


@role_permission_routes.get("/{role}")
@api_handler
def list_permissions_for_role(
    role: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List all permissions (full objects) assigned to a given role."""
    if limit > 500:
        limit = 500
    usecase: RolePermissionQueryUseCase = role_permission_query_usecase_factory()
    permissions, total = usecase.get_permissions_for_role(role=role, skip=skip, limit=limit)
    return {
        "success": True,
        "message": "Role permissions retrieved",
        "data": {
            "items": [p.to_dict() for p in permissions],
            "total": total,
            "role": role,
            "skip": skip,
            "limit": limit,
        },
    }
