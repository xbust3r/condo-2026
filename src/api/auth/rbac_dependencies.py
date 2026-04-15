"""
RBAC contextual dependencies — permission guards per condominium.

Each user can have a different role in each condominium.
These dependencies enforce that the authenticated user has a role
in the target condominium before allowing access.

Usage:
    @app.get("/condominiums/{condominium_id}/units")
    def list_units(
        ctx: CondominiumUserContext = Depends(get_condominium_user()),
    ):
        ...

Guards:
    require_super_admin(condominium_id) → 403 if not super_admin
    require_condominium_admin(condominium_id) → 403 if not admin
    require_any_role(condominium_id) → 403 if no role at all
"""
from dataclasses import dataclass
from typing import Optional, Literal

from fastapi import Depends, HTTPException, Header, status, Path, Query

from library.dddpy.auth.auth_dependencies import get_current_user
from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import CondominiumRoleQueryRepositoryImpl
from library.dddpy.core_user_profiles.infrastructure.user_profile_query_repository import UserProfileQueryRepositoryImpl


# ── Context dataclass ────────────────────────────────────────────────────────

@dataclass
class CondominiumUserContext:
    """Authenticated user + their role in the target condominium."""
    user: UserIdentity
    role: str  # "super_admin" | "condominium_admin"
    condominium_id: int
    is_super_admin: bool
    is_condominium_admin: bool
    granted_at: Optional[str] = None  # ISO date string from role entity


# ── Core dependency ─────────────────────────────────────────────────────────

def get_condominium_user(
    condominium_id: int = Path(..., description="Condominium ID"),
) -> CondominiumUserContext:
    """
    FastAPI dependency — returns the authenticated user's context within a condominium.

    Must be used together with Depends(get_current_user).
    Raises 403 if the user has no active role in the specified condominium.

    Usage in routes:
        ctx: CondominiumUserContext = Depends(get_condominium_user)

    Note: This function is NOT async — FastAPI resolves get_current_user first.
    """
    # Get authenticated user (raises 401 if not authenticated)
    user: UserIdentity = get_current_user()

    role_repo = CondominiumRoleQueryRepositoryImpl()
    role = role_repo.get_active_by_user_and_condominium(
        user_id=user.id,
        condominium_id=condominium_id,
    )

    if not role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
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
        Depends(require_super_admin(condominium_id))
    """
    user: UserIdentity = get_current_user()

    role_repo = CondominiumRoleQueryRepositoryImpl()
    role = role_repo.get_active_by_user_and_condominium(
        user_id=user.id,
        condominium_id=condominium_id,
    )

    if not role or role.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: super_admin role required in this condominium",
        )


def require_condominium_admin(condominium_id: int) -> None:
    """
    Guard — raises 403 if user is not super_admin or condominium_admin.

    Use as a dependency:
        Depends(require_condominium_admin(condominium_id))
    """
    user: UserIdentity = get_current_user()

    role_repo = CondominiumRoleQueryRepositoryImpl()
    role = role_repo.get_active_by_user_and_condominium(
        user_id=user.id,
        condominium_id=condominium_id,
    )

    if not role or role.role not in ("super_admin", "condominium_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: admin role required in this condominium",
        )


def require_any_role(condominium_id: int) -> None:
    """
    Guard — raises 403 if user has no active role in the condominium.
    Alias for the base check in get_condominium_user.
    """
    user: UserIdentity = get_current_user()

    role_repo = CondominiumRoleQueryRepositoryImpl()
    role = role_repo.get_active_by_user_and_condominium(
        user_id=user.id,
        condominium_id=condominium_id,
    )

    if not role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: no active role in condominium {condominium_id}",
        )
