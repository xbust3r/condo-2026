"""
JWT service — creates and validates access tokens.

Security requirements:
  - JWT_ACCESS_SECRET must be set in environment (no fallback, fails at boot)
  - JWT_REFRESH_SECRET must be set in environment (no fallback, fails at boot)
  - Access token TTL: 15 minutes (900 seconds)
"""
import os
import jwt
from datetime import datetime, timedelta
from typing import Optional

from library.dddpy.auth.domain.auth_token import AccessTokenPayload
from library.dddpy.auth.domain.auth_exception import TokenInvalid


_ACCESS_SECRET = os.environ.get("JWT_ACCESS_SECRET")
_REFRESH_SECRET = os.environ.get("JWT_REFRESH_SECRET")

if not _ACCESS_SECRET:
    raise RuntimeError(
        "JWT_ACCESS_SECRET environment variable is required. "
        "Set it to a cryptographically strong random string (min 32 chars)."
    )
if not _REFRESH_SECRET:
    raise RuntimeError(
        "JWT_REFRESH_SECRET environment variable is required. "
        "Set it to a cryptographically strong random string (min 32 chars)."
    )

ACCESS_TOKEN_TTL_SECONDS = 900  # 15 minutes
ALGORITHM = "HS256"


class JWTService:

    @staticmethod
    def create_access_token(
        payload: AccessTokenPayload,
        token_version: int,
    ) -> tuple[str, int]:
        """
        Create a signed JWT access token.
        Returns (token, expires_in_seconds).
        """
        now = datetime.utcnow()
        exp = now + timedelta(seconds=ACCESS_TOKEN_TTL_SECONDS)

        data = {
            "sub": str(payload.user_id),
            "email": payload.email,
            "uuid": payload.uuid,
            "token_version": token_version,
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
            "type": "access",
        }

        token = jwt.encode(data, _ACCESS_SECRET, algorithm=ALGORITHM)
        return token, ACCESS_TOKEN_TTL_SECONDS

    @staticmethod
    def decode_access_token(
        token: str,
    ) -> tuple[AccessTokenPayload, int]:
        """
        Decode and validate an access token.

        Returns (AccessTokenPayload, token_version).
        Raises TokenInvalid on failure.
        """
        try:
            data = jwt.decode(token, _ACCESS_SECRET, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise TokenInvalid()
        except jwt.InvalidTokenError:
            raise TokenInvalid()

        if data.get("type") != "access":
            raise TokenInvalid()

        return (
            AccessTokenPayload(
                user_id=int(data["sub"]),
                email=data["email"],
                uuid=data["uuid"],
            ),
            data.get("token_version", 0),
        )

    @staticmethod
    def decode_token_unsafe(token: str) -> Optional[dict]:
        """
        Decode token WITHOUT validation. Used only for logging/error reporting.
        NEVER use this for auth decisions.
        """
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except Exception:
            return None
