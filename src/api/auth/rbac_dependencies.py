"""
RBAC contextual dependencies — permission guards per condominium.

Each user can have a different role in each condominium.
These dependencies enforce that the authenticated user has a role
in the target condominium before allowing access.

Usage:
    from api.auth.rbac_dependencies import require_condominium_role

    @app.get("/condominiums/{condominium_id}/units")
    def list_units(
        user: UserIdentity = Depends(get_current_user),
        condominium_id: int = Path(...),
    ):
        require_condominium_role(user, condominium_id)  # raises 403 if no role
        ...

Role checks return the CondominiumUserContext on success:
    ctx = require_condominium_role(user, condominium_id)  # CondominiumUserContext
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from fastapi import Depends, HTTPException, Path

if TYPE_CHECKING:
    from library.dddpy.auth.domain.user_identity import UserIdentity


# ── Context dataclass ────────────────────────────────────────────────────────

@dataclass
class CondominiumUserContext:
    """Authenticated user + their role in the target condominium."""
    user: "UserIdentity"
    role: str  # "super_admin" | "condominium_admin"
    condominium_id: int
    is_super_admin: bool
    is_condominium_admin: bool
    granted_at: Optional[str] = None  # ISO date string from role entity


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

    role_repo = CondominiumRoleQueryRepositoryImpl()
    role = role_repo.get_active_by_user_and_condominium(
        user_id=user.id,
        condominium_id=condominium_id,
    )

    if not role:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied: no active role in condominium {condominium_id}",
        )

    return CondominiumUserContext(
        user=user,
        role=role.role,
        condominium_id=condominium_id,
        is_super_admin=role.role == "super_admin",
        is_condominium_admin=role.role in ("super_admin", "condominium_admin"),
        granted_at=role.created_at.isoformat() if role.created_at else None,
    )


def require_super_admin(user: "UserIdentity", condominium_id: int) -> None:
    """Raise 403 if user is not super_admin in this condominium."""
    ctx = require_condominium_role(user, condominium_id)
    if not ctx.is_super_admin:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: super_admin role required in this condominium",
        )


def require_condominium_admin(user: "UserIdentity", condominium_id: int) -> None:
    """Raise 403 if user is not super_admin or condominium_admin."""
    ctx = require_condominium_role(user, condominium_id)
    if not ctx.is_condominium_admin:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: admin role required in this condominium",
        )


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