from typing import Optional
"""
FastAPI dependencies for auth — extract JWT from Authorization header.

Security:
  - Validates token_version in JWT against DB on every request
  - If token_version in DB is higher than in JWT, the token is rejected
    (logout-all, password reset, or account lock increments token_version)
  - This means revoked tokens are invalidated immediately, before expiration
"""
from datetime import datetime, timezone
from fastapi import Depends, Header, HTTPException, status
from typing import Optional

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.auth.domain.auth_exception import TokenInvalid
from library.dddpy.auth.infrastructure.auth_user_repository import AuthUserRepository
from library.dddpy.auth.infrastructure.jwt_service import JWTService
from library.dddpy.shared.logging.logging import Logger


logger = Logger("AuthDependencies")


async def get_current_user(
    authorization: Optional[str] = Header(None, description="Bearer <access_token>"),
) -> UserIdentity:
    """
    Extract and validate access token from Authorization header.

    Validation steps:
      1. Bearer format check
      2. JWT signature validation
      3. token_version in JWT matches current DB value
      4. User status is active
      5. Account is not locked (locked_until)

    Usage: `user: UserIdentity = Depends(get_current_user)`

    Raises HTTPException 401 if token is missing, invalid, expired,
    or has a stale token_version.
    Raises HTTPException 403 if account is inactive or 423 if locked.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Use: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]

    # Step 1: decode JWT and verify signature
    try:
        payload, jwt_token_version = JWTService.decode_access_token(token)
    except TokenInvalid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 2: fetch user from DB
    user_repo = AuthUserRepository()
    identity = user_repo.get_by_id(payload.user_id)
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 3: validate token_version against DB
    # If token_version in JWT < DB value, the token was issued before a
    # logout-all / password reset / account lock — reject it
    db_token_version = user_repo.get_token_version(payload.user_id)
    if jwt_token_version < db_token_version:
        logger.warning(
            f"Stale token rejected: JWT_version={jwt_token_version}, "
            f"DB_version={db_token_version}, user_id={payload.user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has been revoked. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 4: validate user status
    if identity.status != "active":
        logger.warning(
            f"Inactive user rejected: status={identity.status}, user_id={identity.id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active. Contact your administrator.",
        )

    # Step 5: validate account is not locked
    now = datetime.now(timezone.utc)
    if identity.locked_until is not None and identity.locked_until > now:
        logger.warning(
            f"Locked user rejected: locked_until={identity.locked_until}, user_id={identity.id}"
        )
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account is temporarily locked. Try again later.",
        )

    return identity


async def get_optional_user(
    authorization: Optional[str] = Header(None),
) -> Optional[UserIdentity]:
    """
    Like get_current_user but returns None instead of 401 if no token provided.
    """
    if not authorization:
        return None
    try:
        return await get_current_user(authorization)
    except HTTPException:
        return None
