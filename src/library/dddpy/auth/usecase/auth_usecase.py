"""
Auth use case — login, logout, refresh, me.

Coordinates:
  - AuthUserRepository (fetch user + verify password)
  - AuthSessionRepository (manage refresh token sessions)
  - JWTService (create access tokens)

Security hardening:
  - token_version in JWT payload — validated against DB on every request
  - logout-all increments token_version, instantly invalidating all active JWTs
  - password_hash NEVER leaves the infrastructure layer
  - Login: same error message whether email exists or not (no user enum)
  - Failed attempts: tracked in users.failed_login_attempts + locked_until
  - Refresh tokens: UUID v4 stored hashed in auth_sessions
"""
import uuid as uuid_lib
from datetime import datetime
from typing import Optional, Tuple

from library.dddpy.auth.domain.auth_exception import (
    InvalidCredentials,
    UserAccountLocked,
    UserAccountInactive,
    TokenInvalid,
)
from library.dddpy.auth.domain.auth_token import AccessTokenPayload
from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.auth.infrastructure.auth_session_repository import AuthSessionRepository
from library.dddpy.auth.infrastructure.auth_user_repository import AuthUserRepository
from library.dddpy.auth.infrastructure.jwt_service import JWTService
from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema


logger = Logger("AuthUseCase")


class AuthUseCase:

    def __init__(self):
        self._user_repo = AuthUserRepository()
        self._session_repo = AuthSessionRepository()
        logger.info("AuthUseCase initialized")

    # ── Login ────────────────────────────────────────────────────────────

    def login(
        self,
        email: str,
        password: str,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> ResponseSuccessSchema:
        """
        Authenticate user and return token pair.

        Raises InvalidCredentials (same msg whether user exists or not).
        Raises UserAccountLocked.
        Raises UserAccountInactive.
        """
        logger.add_inside_method("login")

        # Step 1: Fetch user identity (no password leak via timing)
        identity = self._user_repo.get_by_email(email)

        # Step 2: Constant-time dummy bcrypt for non-existent user
        # Runs bcrypt operations to match the timing profile of a real login.
        # bcrypt.gen_salt() and hashpw are inherently slow, matching real auth timing.
        if identity is None:
            import bcrypt
            bcrypt.gensalt(10)
            bcrypt.hashpw(b"__dummy__", bcrypt.gensalt(10))
            raise InvalidCredentials()

        # Step 3: Check account status
        if identity.status not in ("active",):
            raise UserAccountInactive()

        # Step 4: Check if locked
        locked_until = self._user_repo.get_locked_until(identity.id)
        if locked_until and locked_until > datetime.utcnow():
            raise UserAccountLocked()

        # Step 5: Verify password hash
        if not self._user_repo.verify_password(identity.id, password):
            self._user_repo.update_failed_login(identity.id)
            raise InvalidCredentials()

        # Step 6: Success — reset failed attempts
        self._user_repo.reset_failed_login(identity.id)

        # Step 7: Get current token_version and generate tokens
        token_version = self._user_repo.get_token_version(identity.id)
        payload = AccessTokenPayload(
            user_id=identity.id,
            email=identity.email,
            uuid=identity.uuid,
        )
        access_token, expires_in = JWTService.create_access_token(
            payload, token_version=token_version,
        )
        refresh_token = str(uuid_lib.uuid4())

        # Step 8: Store session
        self._session_repo.create_session(
            user_id=identity.id,
            refresh_token=refresh_token,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        logger.info(f"Login successful for user_id={identity.id}, token_version={token_version}")
        return ResponseSuccessSchema(
            success=True,
            message="Login successful",
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": expires_in,
                "token_type": "Bearer",
                "user": identity.to_dict(),
            },
        )

    # ── Refresh ─────────────────────────────────────────────────────────

    def refresh(self, refresh_token: str) -> ResponseSuccessSchema:
        """
        Validate refresh token, rotate session, return new token pair.
        Implements refresh token rotation (old token is NOT reused).
        Preserves user_agent and ip_address from the original session.
        """
        logger.add_inside_method("refresh")

        # Find active session by refresh token
        session = self._session_repo.get_by_refresh_token(refresh_token)
        if not session:
            logger.warning("Refresh token not found or expired")
            raise TokenInvalid()

        # Preserve original session metadata for the new session
        original_user_agent = session.user_agent
        original_ip_address = session.ip_address

        # Fetch user identity
        identity = self._user_repo.get_by_id(session.user_id)
        if not identity:
            raise TokenInvalid()

        if identity.status not in ("active",):
            raise UserAccountInactive()

        # Revoke old session (rotation — token used only once)
        self._session_repo.revoke_session(session.uuid)

        # Issue new tokens with current token_version
        token_version = self._user_repo.get_token_version(identity.id)
        payload = AccessTokenPayload(
            user_id=identity.id,
            email=identity.email,
            uuid=identity.uuid,
        )
        access_token, expires_in = JWTService.create_access_token(
            payload, token_version=token_version,
        )
        new_refresh_token = str(uuid_lib.uuid4())

        # New session — preserve original metadata
        self._session_repo.create_session(
            user_id=identity.id,
            refresh_token=new_refresh_token,
            user_agent=original_user_agent,
            ip_address=original_ip_address,
        )

        logger.info(f"Token refreshed for user_id={identity.id}, token_version={token_version}")
        return ResponseSuccessSchema(
            success=True,
            message="Token refreshed",
            data={
                "access_token": access_token,
                "refresh_token": new_refresh_token,
                "expires_in": expires_in,
                "token_type": "Bearer",
            },
        )

    # ── Logout ───────────────────────────────────────────────────────────

    def logout(self, refresh_token: str) -> ResponseSuccessSchema:
        """Revoke a refresh token session."""
        logger.add_inside_method("logout")
        self._session_repo.revoke_session_by_token(refresh_token)
        logger.info("Logout successful")
        return ResponseSuccessSchema(
            success=True,
            message="Session terminated",
            data=None,
        )

    def logout_all(self, user_id: int) -> ResponseSuccessSchema:
        """
        Revoke ALL sessions for a user AND increment token_version.

        This immediately invalidates ALL active access tokens for this user,
        regardless of their expiration time.
        """
        logger.add_inside_method("logout_all")

        # Revoke all sessions
        count = self._session_repo.revoke_all_user_sessions(user_id)

        # Increment token_version — all existing JWTs become invalid instantly
        new_version = self._user_repo.increment_token_version(user_id)

        logger.info(
            f"Revoked {count} sessions and incremented token_version "
            f"to {new_version} for user_id={user_id}"
        )
        return ResponseSuccessSchema(
            success=True,
            message=f"All sessions terminated ({count} revoked)",
            data={"revoked_count": count, "token_version": new_version},
        )

    # ── Me ───────────────────────────────────────────────────────────────

    def me(self, user_id: int) -> ResponseSuccessSchema:
        """Get current authenticated user identity (users + profile)."""
        logger.add_inside_method("me")
        identity = self._user_repo.get_by_id(user_id)
        if not identity:
            raise TokenInvalid()
        return ResponseSuccessSchema(
            success=True,
            message="Identity retrieved",
            data=identity.to_dict(),
        )
