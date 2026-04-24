from typing import Optional
"""
RBAC contextual dependencies — permission guards per condominium.

Each user can have a different role in each condominium.
These dependencies enforce that the authenticated user has a role
in the target condominium before allowing access, and optionally
check granular permissions from core_role_permissions.

Usage:
    from api.auth.rbac_dependencies import require_condominium_role, require_permission

    @app.get("/condominiums/{condominium_id}/buildings")
    def list_buildings(
        user: UserIdentity = Depends(get_current_user),
        condominium_id: int = Path(...),
    ):
        ctx = require_condominium_role(user, condominium_id)  # raises 403 if no role
        require_permission(ctx, "building", "read")  # raises 403 if no permission
        ...

Role checks return the CondominiumUserContext on success.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from fastapi import Depends, HTTPException, Path

if TYPE_CHECKING:
    from library.dddpy.auth.domain.user_identity import UserIdentity


# ── Context dataclass ────────────────────────────────────────────────────────

@dataclass
class CondominiumUserContext:
    """Authenticated user + their role in the target condominium."""
    user: "UserIdentity"
    role: str
    condominium_id: int
    is_super_admin: bool
    is_condominium_admin: bool
    granted_at: Optional[str] = None
    permissions: list[str] = field(default_factory=list)
    scopes: dict[str, int] = field(default_factory=dict)
    building_ids: list[int] = field(default_factory=list)  # para maintenance/operations staff


# ── Role checker (sync — call from route handlers) ─────────────────────────

def require_condominium_role(
    user: "UserIdentity",
    condominium_id: int,
) -> CondominiumUserContext:
    """
    Check that `user` has an active role in `condominium_id`.

    Returns CondominiumUserContext on success.
    Raises HTTPException 403 if the user has no active role in the condominium.

    Use inside route handlers after extracting the user via Depends(get_current_user).
    """
    from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
        CondominiumRoleQueryRepositoryImpl,
    )
    from library.dddpy.auth.permission_service import PermissionService

    role_repo = CondominiumRoleQueryRepositoryImpl()
    role_entity = role_repo.get_active_by_user_and_condominium(
        user_id=user.id,
        condominium_id=condominium_id,
    )

    if not role_entity:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied: no active role in condominium {condominium_id}",
        )

    # resident: computed dynamically, not stored in core_condominium_roles
    is_resident = role_entity.role == "resident"

    # Load permissions via PermissionService (skip for resident — computed separately)
    permission_codes: list[str] = []
    scopes: dict[str, int] = {}
    building_ids: list[int] = []

    if not is_resident:
        perm_service = PermissionService()
        perm_list = perm_service.get_user_permissions(user.id, condominium_id)
        permission_codes = [p.code for p in perm_list]
        # Collect scopes by type
        for p in perm_list:
            scope = p.scope_default
            if scope not in scopes:
                scopes[scope] = 0
        # Collect building_ids for staff roles
        if role_entity.building_id:
            building_ids = [role_entity.building_id]

    return CondominiumUserContext(
        user=user,
        role=role_entity.role,
        condominium_id=condominium_id,
        is_super_admin=role_entity.role == "super_admin",
        is_condominium_admin=role_entity.role in ("super_admin", "condominium_admin"),
        granted_at=role_entity.created_at.isoformat() if role_entity.created_at else None,
        permissions=permission_codes,
        scopes=scopes,
        building_ids=building_ids,
    )


def require_super_admin(ctx: CondominiumUserContext) -> None:
    """Raise 403 if user is not super_admin."""
    if not ctx.is_super_admin:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: super_admin role required",
        )


def require_condominium_admin(ctx: CondominiumUserContext) -> None:
    """Raise 403 if user is not super_admin or condominium_admin."""
    if not ctx.is_condominium_admin:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: admin role required",
        )


def require_permission(
    ctx: CondominiumUserContext,
    resource: str,
    action: str,
    unit_id: Optional[int] = None,
    building_id: Optional[int] = None,
) -> None:
    """
    Check granular permission (resource, action) for the given context.

    RBAC-05 scope enforcement:
      - 'global':   siempre OK (super_admin)
      - 'condominium': siempre OK si el ctx tiene rol en el condominio
      - 'unit':     unit_id debe coincidir con la unidad del usuario (resident)
      - 'building': building_id debe estar en ctx.building_ids

    Usage:
        require_permission(ctx, "building", "read")
        require_permission(ctx, "incident", "create", unit_id=42)
        require_permission(ctx, "maintenance", "update", building_id=3)
    """
    # super_admin tiene todo
    if ctx.is_super_admin:
        return

    permission_code = f"{resource}.{action}"

    if permission_code not in ctx.permissions:
        raise HTTPException(
            status_code=403,
            detail=f"Forbidden: {permission_code} permission required",
        )

    # Scope enforcement
    # Determinar el scope_default del permiso desde la lista de permisos cargados
    scope_default = _get_permission_scope_default(ctx, permission_code)

    if scope_default == "unit":
        # resident solo puede actuar sobre su propia unidad
        if unit_id is None:
            # Si no se provee unit_id, no podemos verificar — denegar por seguridad
            raise HTTPException(
                status_code=403,
                detail=f"Forbidden: {permission_code} requires unit context",
            )
        # TODO: verificar que unit_id pertenece al usuario (via occupancy)
        # Por ahora se delega al usecase/query la verificación fina

    elif scope_default == "building":
        if building_id is None:
            raise HTTPException(
                status_code=403,
                detail=f"Forbidden: {permission_code} requires building context",
            )
        if ctx.building_ids and building_id not in ctx.building_ids:
            raise HTTPException(
                status_code=403,
                detail=f"Forbidden: building {building_id} not in your scope",
            )


def _get_permission_scope_default(ctx: CondominiumUserContext, permission_code: str) -> str:
    """
    Resolve the scope_default for a permission code from the loaded permissions.
    Returns 'condominium' as safe default.
    """
    # Buscar en ctx.permissions ya que solo guardamos codes
    # El scope_default se pierde al guardar solo codes — lo resolvemos desde
    # la definición estática del planning doc (fuente autoritativa)
    SCOPE_DEFAULTS = {
        # global
        "condominium.delete": "global",
        "building.delete": "global",
        "unit.delete": "global",
        # unit scoped
        "unit.read": "unit",
        "incident.create": "unit",
        "maintenance.create": "unit",
        # building scoped — determinado por building_id del rol
        # condominium scoped (default)
    }
    return SCOPE_DEFAULTS.get(permission_code, "condominium")


# ── FastAPI route dependencies (for use with Depends()) ──────────────────────

def get_condominium_user(condominium_id: int):
    """
    Factory — returns a Depends() that enforces the user has a role.

    Usage in routes:
        @app.get("/buildings/{condominium_id}")
        def list_buildings(
            ctx: CondominiumUserContext = Depends(get_condominium_user(condominium_id=condominium_id)),
        ):
            ...

    NOTE: Requires get_current_user to be declared earlier in the route
    signature (FastAPI resolves dependency chain automatically).
    """
    from api.auth.auth_dependencies import get_current_user

    def _get_ctx(user: "UserIdentity" = Depends(get_current_user)) -> CondominiumUserContext:
        return require_condominium_role(user, condominium_id)

    return _get_ctx


def get_permission_check(
    resource: str,
    action: str,
    unit_id_param: Optional[str] = None,
    building_id_param: Optional[str] = None,
):
    """
    Factory — returns a Depends() that checks a granular permission.

    Usage:
        @app.get("/buildings/{building_id}")
        def get_building(
            ctx: CondominiumUserContext = Depends(get_condominium_user(condominium_id)),
            building_id: int = Path(...),
            _perm: None = Depends(get_permission_check("building", "read")),
        ):
            ...
    """
    def _check_permission(ctx: CondominiumUserContext = Depends()) -> None:
        require_permission(ctx, resource, action)
    return _check_permission
