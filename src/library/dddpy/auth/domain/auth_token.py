"""
JWT token pair: access token payload and token pair result.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AccessTokenPayload:
    """Payload stored inside the JWT access token."""
    user_id: int
    email: str
    uuid: str  # user uuid


@dataclass(frozen=True)
class TokenPair:
    """Pair of access token + refresh token returned on login/refresh."""
    access_token: str
    refresh_token: str
    expires_in: int  # seconds
    token_type: str = "Bearer"
