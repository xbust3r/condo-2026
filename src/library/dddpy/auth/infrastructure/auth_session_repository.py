"""
from typing import Optional
Repository for auth_sessions — stores hashed refresh tokens.

One session per refresh token. Sessions are soft-deleted on logout.
"""
import uuid as uuid_lib
import hashlib
from datetime import datetime, timedelta
from typing import Optional

import bcrypt

from library.dddpy.auth.infrastructure.dbauth_session import DBAuthSession
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("AuthSessionRepository")

REFRESH_TOKEN_TTL_DAYS = 7


class AuthSessionRepository:

    @staticmethod
    def _hash_token(token: str) -> str:
        """SHA-256 hash of the refresh token."""
        return hashlib.sha256(token.encode()).hexdigest()

    def create_session(
        self,
        user_id: int,
        refresh_token: str,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> DBAuthSession:
        """Create a new auth session with hashed refresh token."""
        logger.info(f"Creating auth session for user_id={user_id}")
        expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_TTL_DAYS)

        with session_scope() as session:
            db_session = DBAuthSession(
                uuid=str(uuid_lib.uuid4()),
                user_id=user_id,
                refresh_token_hash=self._hash_token(refresh_token),
                user_agent=user_agent,
                ip_address=ip_address,
                expires_at=expires_at,
            )
            session.add(db_session)
            session.flush()
            session.refresh(db_session)
            logger.info(f"Auth session created uuid={db_session.uuid}")
            return db_session

    def get_by_refresh_token(self, refresh_token: str) -> Optional[DBAuthSession]:
        """Find an active session by refresh token hash."""
        token_hash = self._hash_token(refresh_token)
        with session_scope() as session:
            db_session = session.query(DBAuthSession).filter(
                DBAuthSession.refresh_token_hash == token_hash,
                DBAuthSession.deleted_at.is_(None),
                DBAuthSession.expires_at > datetime.utcnow(),
            ).first()
            return db_session

    def revoke_session(self, session_uuid: str) -> bool:
        """Soft-delete a session (logout) by its UUID."""
        logger.info(f"Revoking session uuid={session_uuid}")
        with session_scope() as session:
            db_session = session.query(DBAuthSession).filter(
                DBAuthSession.uuid == session_uuid,
                DBAuthSession.deleted_at.is_(None),
            ).first()
            if not db_session:
                logger.warning(f"Session not found for revoke: {session_uuid}")
                return False
            db_session.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Session revoked uuid={session_uuid}")
            return True

    def revoke_session_by_token(self, refresh_token: str) -> bool:
        """Soft-delete a session by its refresh token (logout)."""
        token_hash = self._hash_token(refresh_token)
        logger.info(f"Revoking session by refresh token hash={token_hash[:8]}...")
        with session_scope() as session:
            db_session = session.query(DBAuthSession).filter(
                DBAuthSession.refresh_token_hash == token_hash,
                DBAuthSession.deleted_at.is_(None),
            ).first()
            if not db_session:
                logger.warning("Session not found for this refresh token")
                return False
            db_session.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Session revoked by token uuid={db_session.uuid}")
            return True

    def revoke_all_user_sessions(self, user_id: int) -> int:
        """Revoke ALL active sessions for a user (change password, compromise, etc)."""
        logger.info(f"Revoking all sessions for user_id={user_id}")
        with session_scope() as session:
            count = session.query(DBAuthSession).filter(
                DBAuthSession.user_id == user_id,
                DBAuthSession.deleted_at.is_(None),
            ).update({"deleted_at": datetime.utcnow()})
            session.flush()
            logger.info(f"Revoked {count} sessions for user_id={user_id}")
            return count

    def cleanup_expired(self) -> int:
        """Delete all expired sessions (can be run as a cron)."""
        with session_scope() as session:
            count = session.query(DBAuthSession).filter(
                DBAuthSession.expires_at < datetime.utcnow(),
            ).delete()
            session.flush()
            logger.info(f"Cleaned up {count} expired sessions")
            return count

    def list_active_sessions(self, user_id: int) -> list[DBAuthSession]:
        """List all active sessions for a user (not expired, not revoked)."""
        with session_scope() as session:
            rows = session.query(DBAuthSession).filter(
                DBAuthSession.user_id == user_id,
                DBAuthSession.deleted_at.is_(None),
                DBAuthSession.expires_at > datetime.utcnow(),
            ).order_by(DBAuthSession.created_at.desc()).all()
            return rows
