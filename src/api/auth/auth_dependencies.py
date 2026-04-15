"""
FastAPI dependencies for auth — extract JWT from Authorization header.

Usage:
    @app.get("/protected")
    def protected(user: UserIdentity = Depends(get_current_user)):
        ...
"""
from fastapi import Depends, Header, HTTPException, status
from typing import Optional

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.auth.domain.auth_exception import TokenInvalid
from library.dddpy.auth.infrastructure.auth_user_repository import AuthUserRepository
from library.dddpy.auth.infrastructure.jwt_service import JWTService


async def get_current_user(
    authorization: Optional[str] = Header(None, description="Bearer <access_token>"),
) -> UserIdentity:
    """
    Extract and validate access token from Authorization header.

    Usage: `user: UserIdentity = Depends(get_current_user)`

    Raises HTTPException 401 if token is missing, invalid, or expired.
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

    try:
        payload = JWTService.decode_access_token(token)
    except TokenInvalid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_repo = AuthUserRepository()
    identity = user_repo.get_by_id(payload.user_id)
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
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
