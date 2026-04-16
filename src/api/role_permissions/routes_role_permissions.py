# =============================================================================
# API Routes: core_role_permissions
# Pivot rol → permisos — solo lectura
#
# Endpoints:
#   GET  /role-permissions                     — list all role-permission mappings
#   GET  /role-permissions/role/{role}        — get permissions for a specific role
#   GET  /role-permissions/permission/{code}  — get roles that have a specific permission
# =============================================================================

from fastapi import APIRouter, Query

from library.dddpy.core_role_permissions.usecase.role_permission_query_usecase import (
    RolePermissionQueryUseCase,
)
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/role-permissions"

role_permission_routes = APIRouter(prefix=PREFIX)


@role_permission_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "module": "core_role_permissions"}


@role_permission_routes.get("")
@api_handler
def list_all_role_permissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """
    List all role-permission mappings.
    Returns the pivot data (role, permission_code, scope_override).
    """
    use_case = RolePermissionQueryUseCase()
    # Map from planning: list all known roles
    all_roles = [
        "super_admin",
        "condominium_admin",
        "board_member",
        "finance_reviewer",
        "security_staff",
        "maintenance_staff",
        "operations_staff",
        "resident",
    ]
    data = []
    total = 0
    for role in all_roles:
        rp_list = use_case.list_by_role(role)
        for rp in rp_list:
            data.append({
                "role": rp.role,
                "permission_code": rp.permission_code,
                "scope_override": rp.scope_override,
            })
            total += 1

    # Slice for pagination
    data = data[skip : skip + limit]
    return {"data": data, "total": total, "skip": skip, "limit": limit}


@role_permission_routes.get("/role/{role}")
@api_handler
def get_permissions_for_role(
    role: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """
    Get all full PermissionEntity objects for a given role.
    Returns permission details (code, resource, action, scope_default).
    """
    use_case = RolePermissionQueryUseCase()
    permissions, total = use_case.get_permissions_for_role(role=role, skip=skip, limit=limit)
    return {
        "role": role,
        "data": [p.to_dict() for p in permissions],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@role_permission_routes.get("/permission/{permission_code}")
@api_handler
def get_roles_for_permission(permission_code: str) -> dict:
    """
    Get all roles that have a specific permission.
    """
    use_case = RolePermissionQueryUseCase()
    roles = use_case.get_roles_for_permission(permission_code)
    return {
        "permission_code": permission_code,
        "roles": roles,
    }
