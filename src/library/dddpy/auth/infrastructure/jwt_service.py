"""
JWT service — creates and validates access tokens.

SECRET and JWT config come from environment.
Access token TTL: 15 minutes (900 seconds).
"""
import os
import jwt
from datetime import datetime, timedelta
from typing import Optional

from library.dddpy.auth.domain.auth_token import AccessTokenPayload
from library.dddpy.auth.domain.auth_exception import TokenInvalid


SECRET = os.environ.get("SECRET", "dev-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_TTL_SECONDS = 900  # 15 minutes


class JWTService:

    @staticmethod
    def create_access_token(payload: AccessTokenPayload) -> tuple[str, int]:
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
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
            "type": "access",
        }

        token = jwt.encode(data, SECRET, algorithm=ALGORITHM)
        return token, ACCESS_TOKEN_TTL_SECONDS

    @staticmethod
    def decode_access_token(token: str) -> AccessTokenPayload:
        """
        Decode and validate an access token.
        Raises TokenInvalid on failure.
        """
        try:
            data = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise TokenInvalid()
        except jwt.InvalidTokenError:
            raise TokenInvalid()

        if data.get("type") != "access":
            raise TokenInvalid()

        return AccessTokenPayload(
            user_id=int(data["sub"]),
            email=data["email"],
            uuid=data["uuid"],
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
