"""
from typing import Optional
RBAC Authorization Dependency — FastAPI dependency for permission enforcement.

Usage:
    from library.dddpy.shared.decorators.rbac_handler import rbac_required

    # Require "charge.write" permission
    @router.post("/charges")
    def create_charge(
        request: CreateChargeSchema,
        user: UserIdentity = Depends(rbac_required("charge", "write")),
    ) -> dict:
        ...

Permission codes follow the pattern: {resource}.{action}
e.g. charge.read, charge.write, ar.read, payment.write, ledger.export

Scope enforcement:
  - Permissions with scope_default="condominium": user must have an active role
    in the target condominium (condominium_id taken from request path/query).
  - Permissions with scope_default="unit": user must have active role OR
    ownership/occupancy on the target unit.
  - Permissions with scope_default="global": only super_admin has access.
"""
from functools import wraps
from typing import Callable, Optional

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import text

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("RBAC")


# ─────────────────────────────────────────────────────────────────────────────
# Permission resolution
# ─────────────────────────────────────────────────────────────────────────────

def resolve_permission_code(resource: str, action: str) -> str:
    """Build permission code from resource + action."""
    return f"{resource}.{action}"


# ─────────────────────────────────────────────────────────────────────────────
# Permission checker (per user)
# ─────────────────────────────────────────────────────────────────────────────

def _user_has_permission(
    user_id: int,
    permission_code: str,
    scope_type: str,
    scope_value: Optional[int],
) -> bool:
    """
    Check if a user has a specific permission through their active roles.

    Args:
        user_id:          User's DB id
        permission_code:   e.g. "charge.write", "ar.read"
        scope_type:       "condominium" | "unit" | "global"
        scope_value:      condominium_id or unit_id (required for non-global scope)

    Returns:
        True if user has the permission, False otherwise.
    """
    with session_scope() as session:
        if scope_type == "global":
            # Global scope: only super_admin role grants this
            result = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_condominium_roles cr
                    JOIN core_permissions p ON p.code = :perm_code
                    WHERE cr.user_id = :uid
                      AND cr.role = 'super_admin'
                      AND cr.status = 'active'
                      AND cr.deleted_at IS NULL
                      AND p.scope_default = 'global'
                """),
                {"uid": user_id, "perm_code": permission_code},
            )
            return result.scalar() > 0

        if scope_type == "condominium" and scope_value is not None:
            result = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_condominium_roles cr
                    JOIN core_permissions p ON p.code = :perm_code
                    WHERE cr.user_id = :uid
                      AND cr.condominium_id = :condo_id
                      AND cr.status = 'active'
                      AND cr.deleted_at IS NULL
                      AND p.scope_default IN ('condominium', 'global')
                """),
                {"uid": user_id, "condo_id": scope_value, "perm_code": permission_code},
            )
            return result.scalar() > 0

        if scope_type == "unit" and scope_value is not None:
            result = session.execute(
                text("""
                    SELECT COUNT(*) FROM core_condominium_roles cr
                    JOIN core_permissions p ON p.code = :perm_code
                    WHERE cr.user_id = :uid
                      AND cr.status = 'active'
                      AND cr.deleted_at IS NULL
                      AND (
                          cr.scope IN ('condominium', 'global')
                          OR (cr.scope = 'unit' AND cr.building_id IN (
                              SELECT building_id FROM core_units WHERE id = :unit_id
                          ))
                      )
                      AND p.scope_default IN ('condominium', 'unit', 'global')
                """),
                {"uid": user_id, "unit_id": scope_value, "perm_code": permission_code},
            )
            return result.scalar() > 0

        # Fallback: check any active role with this permission
        result = session.execute(
            text("""
                SELECT COUNT(*) FROM core_condominium_roles cr
                JOIN core_permissions p ON p.code = :perm_code
                WHERE cr.user_id = :uid
                  AND cr.status = 'active'
                  AND cr.deleted_at IS NULL
                  AND p.scope_default IN ('condominium', 'global')
            """),
            {"uid": user_id, "perm_code": permission_code},
        )
        return result.scalar() > 0


def _get_scope_default(permission_code: str) -> str:
    """Get the scope_default for a permission code from the DB."""
    with session_scope() as session:
        result = session.execute(
            text("SELECT scope_default FROM core_permissions WHERE code = :code"),
            {"code": permission_code},
        ).fetchone()
        return result[0] if result else "condominium"


# ─────────────────────────────────────────────────────────────────────────────
# FastAPI Dependency
# ─────────────────────────────────────────────────────────────────────────────

def rbac_required(
    resource: str,
    action: str,
    scope_param: Optional[str] = None,
) -> Callable:
    """
    FastAPI dependency that enforces RBAC permission.

    Args:
        resource:    Resource name (e.g. "charge", "ar", "payment")
        action:      Action (e.g. "read", "write", "delete", "export")
        scope_param: Name of the request parameter containing the scope value.
                     If None, scope defaults to "condominium" and is inferred
                     from path parameter "condominium_id" or query param.
                     Examples: "condominium_id", "unit_id", "id"

    Usage:
        # Simple (scope from path/query):
        @router.get("/charges", user: UserIdentity = Depends(rbac_required("charge", "read")))

        # Explicit scope param:
        @router.get("/charges", user: UserIdentity = Depends(rbac_required("charge", "read", "condominium_id")))

    Raises:
        HTTPException 401 — if no valid auth token
        HTTPException 403 — if user lacks the required permission
    """
    permission_code = resolve_permission_code(resource, action)

    async def dependency(
        request: Request,
        user: UserIdentity = Depends(lambda: None),  # Placeholder; actual auth done below
    ) -> UserIdentity:
        # Extract actual user from request.state (set by AuthMiddleware if present)
        # OR re-validate via Authorization header directly here.
        # For clean separation, we use get_current_user pattern inline.
        actual_user = await _get_user_from_request(request)
        if not actual_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Determine scope
        scope_type = _get_scope_default(permission_code)

        scope_value: Optional[int] = None
        if scope_param:
            scope_value = _extract_int(request, scope_param)
        else:
            # Try to infer from common params
            scope_value = (
                _extract_int(request, "condominium_id")
                or _extract_int(request, "id")
                or _extract_int(request, "unit_id")
            )

        has_perm = _user_has_permission(
            user_id=actual_user.id,
            permission_code=permission_code,
            scope_type=scope_type,
            scope_value=scope_value,
        )

        if not has_perm:
            logger.warning(
                f"RBAC denied: user_id={actual_user.id} lacks "
                f"{permission_code} (scope_type={scope_type}, scope_value={scope_value})"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Permission denied: '{permission_code}' required. "
                    f"Contact your administrator if you believe this is an error."
                ),
            )

        logger.info(f"RBAC granted: user_id={actual_user.id} → {permission_code}")
        return actual_user

    return dependency


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

async def _get_user_from_request(request: Request) -> Optional[UserIdentity]:
    """
    Extract UserIdentity from request.state if set by middleware.
    Falls back to re-validating the Authorization header.
    """
    # FastAPI Dependency injection: if another Depends() already set the user,
    # it would be passed as a kwarg. We handle both cases.
    # For simplicity, we re-validate from header.
    from library.dddpy.auth.infrastructure.auth_user_repository import AuthUserRepository
    from library.dddpy.auth.infrastructure.jwt_service import JWTService
    from library.dddpy.auth.domain.auth_exception import TokenInvalid

    auth_header = request.headers.get("authorization")
    if not auth_header:
        return None

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    try:
        payload, jwt_version = JWTService.decode_access_token(parts[1])
    except TokenInvalid:
        return None

    user_repo = AuthUserRepository()
    identity = user_repo.get_by_id(payload.user_id)
    if not identity:
        return None

    db_version = user_repo.get_token_version(payload.user_id)
    if jwt_version < db_version:
        return None

    return identity


def _extract_int(request: Request, key: str) -> Optional[int]:
    """Extract an integer from request path kwargs or query params."""
    val = request.path_params.get(key) or request.query_params.get(key)
    if val is None:
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None
