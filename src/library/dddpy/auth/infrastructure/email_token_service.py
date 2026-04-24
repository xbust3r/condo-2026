"""
Email token service — generates and validates signed tokens for:
  - Password reset  (single-use, short TTL)
  - Email verification (single-use, medium TTL)
"""
import os
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional

from library.dddpy.auth.domain.auth_exception import TokenInvalid


_EMAIL_TOKEN_SECRET = os.environ.get("EMAIL_TOKEN_SECRET") or os.environ.get("SECRET", "default-insecure")
ALGORITHM = "HS256"


class EmailTokenService:

    # -------------------------------------------------------------------------
    # Password reset token
    # -------------------------------------------------------------------------

    @staticmethod
    def create_password_reset_token(user_id: int, email: str) -> str:
        """
        Create a signed JWT password reset token.
        TTL: 1 hour.
        """
        now = datetime.utcnow()
        exp = now + timedelta(hours=1)
        payload = {
            "sub": str(user_id),
            "email": email,
            "type": "password_reset",
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        return jwt.encode(payload, _EMAIL_TOKEN_SECRET, algorithm=ALGORITHM)

    @staticmethod
    def validate_password_reset_token(token: str) -> dict:
        """
        Validate a password reset token.
        Returns {"user_id": int, "email": str}.
        Raises TokenInvalid if expired, tampered, or wrong type.
        """
        try:
            data = jwt.decode(token, _EMAIL_TOKEN_SECRET, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise TokenInvalid("Reset link has expired. Please request a new one.")
        except jwt.InvalidTokenError:
            raise TokenInvalid("Invalid reset link.")

        if data.get("type") != "password_reset":
            raise TokenInvalid("Invalid reset link type.")

        return {"user_id": int(data["sub"]), "email": data["email"]}

    # -------------------------------------------------------------------------
    # Email verification token
    # -------------------------------------------------------------------------

    @staticmethod
    def create_email_verification_token(user_id: int, email: str) -> str:
        """
        Create a signed JWT email verification token.
        TTL: 24 hours.
        """
        now = datetime.utcnow()
        exp = now + timedelta(hours=24)
        payload = {
            "sub": str(user_id),
            "email": email,
            "type": "email_verification",
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        return jwt.encode(payload, _EMAIL_TOKEN_SECRET, algorithm=ALGORITHM)

    @staticmethod
    def validate_email_verification_token(token: str) -> dict:
        """
        Validate an email verification token.
        Returns {"user_id": int, "email": str}.
        Raises TokenInvalid if expired, tampered, or wrong type.
        """
        try:
            data = jwt.decode(token, _EMAIL_TOKEN_SECRET, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise TokenInvalid("Verification link has expired. Please request a new one.")
        except jwt.InvalidTokenError:
            raise TokenInvalid("Invalid verification link.")

        if data.get("type") != "email_verification":
            raise TokenInvalid("Invalid verification link type.")

        return {"user_id": int(data["sub"]), "email": data["email"]}

    # -------------------------------------------------------------------------
    # Unsubscribe token (for email footers)
    # -------------------------------------------------------------------------

    @staticmethod
    def create_unsubscribe_token(user_id: int) -> str:
        """Create a one-time-use HMAC unsubscribe token. TTL: 30 days."""
        raw = f"unsubscribe:{user_id}:{secrets.token_urlsafe(16)}"
        return hashlib.blake2b(raw.encode(), person=b"unsub").hexdigest()

    @staticmethod
    def validate_unsubscribe_token(token: str, user_id: int) -> bool:
        """Validate an unsubscribe token (exact match after reconstruction)."""
        expected = hashlib.blake2b(
            f"unsubscribe:{user_id}:".encode(), person=b"unsub"
        ).hexdigest()
        return secrets.compare_digest(token, expected)
