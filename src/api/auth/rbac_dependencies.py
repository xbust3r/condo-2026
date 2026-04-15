"""
RBAC contextual dependencies — permission guards per condominium.

Each user can have a different role in each condominium.
These dependencies enforce that the authenticated user has a role
in the target condominium before allowing access.

Usage in routes:
    from api.auth.rbac_dependencies import get_condominium_user, CondominiumUserContext

    @app.get("/condominiums/{condominium_id}/units")
    def list_units(
        ctx: CondominiumUserContext = Depends(get_condominium_user),
    ):
        ...

Guards:
    require_super_admin(condominium_id) → 403 if not super_admin
    require_condominium_admin(condominium_id) → 403 if not admin
    require_any_role(condominium_id) → 403 if no role at all
"""
from dataclasses import dataclass
from typing import Optional

from fastapi import Depends, HTTPException, Path


# ── Context dataclass ────────────────────────────────────────────────────────

@dataclass
class CondominiumUserContext:
    """Authenticated user + their role in the target condominium."""
    user: "UserIdentity"  # resolved via lazy import in functions
    role: str  # "super_admin" | "condominium_admin"
    condominium_id: int
    is_super_admin: bool
    is_condominium_admin: bool
    granted_at: Optional[str] = None  # ISO date string from role entity


# ── Core dependency ─────────────────────────────────────────────────────────

async def get_condominium_user(
    condominium_id: int = Path(..., description="Condominium ID"),
) -> CondominiumUserContext:
    """
    FastAPI dependency — returns the authenticated user's context within a condominium.

    Must be used together with Depends(get_current_user).
    Raises 403 if the user has no active role in the specified condominium.

    Note: get_current_user is imported lazily inside the function to avoid
    loading the JWT module (which requires env vars) at module import time.
    """
    # Lazy import to avoid triggering JWT env validation at import time
    from api.auth.auth_dependencies import get_current_user
    from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
        CondominiumRoleQueryRepositoryImpl,
    )

    # Get authenticated user (raises 401 if not authenticated)
    user = await get_current_user()

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


# ── Role guards ─────────────────────────────────────────────────────────────

def require_super_admin(condominium_id: int) -> None:
    """
    Guard — raises 403 if user is not super_admin in the given condominium.

    Use as a dependency:
        Depends(lambda: require_super_admin(condominium_id))
    """
    from api.auth.auth_dependencies import get_current_user
    from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
        CondominiumRoleQueryRepositoryImpl,
    )

    user = get_current_user()

    role_repo = CondominiumRoleQueryRepositoryImpl()
    role = role_repo.get_active_by_user_and_condominium(
        user_id=user.id,
        condominium_id=condominium_id,
    )

    if not role or role.role != "super_admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden: super_admin role required in this condominium",
        )


def require_condominium_admin(condominium_id: int) -> None:
    """
    Guard — raises 403 if user is not super_admin or condominium_admin.

    Use as a dependency:
        Depends(lambda: require_condominium_admin(condominium_id))
    """
    from api.auth.auth_dependencies import get_current_user
    from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
        CondominiumRoleQueryRepositoryImpl,
    )

    user = get_current_user()

    role_repo = CondominiumRoleQueryRepositoryImpl()
    role = role_repo.get_active_by_user_and_condominium(
        user_id=user.id,
        condominium_id=condominium_id,
    )

    if not role or role.role not in ("super_admin", "condominium_admin"):
        raise HTTPException(
            status_code=403,
            detail="Forbidden: admin role required in this condominium",
        )


def require_any_role(condominium_id: int) -> None:
    """
    Guard — raises 403 if user has no active role in the condominium.
    Alias for the base check in get_condominium_user.
    """
    from api.auth.auth_dependencies import get_current_user
    from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
        CondominiumRoleQueryRepositoryImpl,
    )

    user = get_current_user()

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
