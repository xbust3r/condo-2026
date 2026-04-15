"""
Auth User repository — fetches user identity for authentication.

Queries users + user_profiles in a single JOIN for the /auth/me endpoint.
Does NOT expose password_hash in results.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import text

from library.dddpy.auth.domain.user_identity import UserIdentity
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("AuthUserRepository")


class AuthUserRepository:

    def get_by_email(self, email: str) -> Optional[UserIdentity]:
        """
        Fetch user identity by email including profile data.
        Returns None if user does not exist.
        """
        logger.info(f"Fetching user by email={email}")
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT
                      u.id,
                      u.uuid,
                      u.email,
                      u.status,
                      u.email_verified_at,
                      u.created_at,
                      u.password_hash,
                      u.deleted_at AS user_deleted_at,
                      p.uuid AS profile_uuid,
                      p.first_name,
                      p.last_name,
                      p.document_type,
                      p.document_number,
                      p.phone,
                      p.deleted_at AS profile_deleted_at
                    FROM users u
                    LEFT JOIN user_profiles p ON p.user_id = u.id AND p.deleted_at IS NULL
                    WHERE u.email = :email
                      AND u.deleted_at IS NULL
                """),
                {"email": email},
            ).fetchone()

            if not row:
                logger.info(f"No user found for email={email}")
                return None

            return UserIdentity(
                id=row.id,
                uuid=row.uuid,
                email=row.email,
                status=row.status,
                email_verified_at=row.email_verified_at,
                created_at=row.created_at,
                first_name=row.first_name,
                last_name=row.last_name,
                document_type=row.document_type,
                document_number=row.document_number,
                phone=row.phone,
                profile_uuid=row.profile_uuid,
            )

    def get_by_id(self, user_id: int) -> Optional[UserIdentity]:
        """Fetch user identity by ID including profile data."""
        logger.info(f"Fetching user by id={user_id}")
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT
                      u.id,
                      u.uuid,
                      u.email,
                      u.status,
                      u.email_verified_at,
                      u.created_at,
                      p.uuid AS profile_uuid,
                      p.first_name,
                      p.last_name,
                      p.document_type,
                      p.document_number,
                      p.phone,
                      p.deleted_at AS profile_deleted_at
                    FROM users u
                    LEFT JOIN user_profiles p ON p.user_id = u.id AND p.deleted_at IS NULL
                    WHERE u.id = :user_id
                      AND u.deleted_at IS NULL
                """),
                {"user_id": user_id},
            ).fetchone()

            if not row:
                logger.info(f"No user found for id={user_id}")
                return None

            return UserIdentity(
                id=row.id,
                uuid=row.uuid,
                email=row.email,
                status=row.status,
                email_verified_at=row.email_verified_at,
                created_at=row.created_at,
                first_name=row.first_name,
                last_name=row.last_name,
                document_type=row.document_type,
                document_number=row.document_number,
                phone=row.phone,
                profile_uuid=row.profile_uuid,
            )

    def update_failed_login(self, user_id: int) -> None:
        """Increment failed_login_attempts and optionally lock the account."""
        with session_scope() as session:
            session.execute(
                text("""
                    UPDATE users
                    SET failed_login_attempts = failed_login_attempts + 1,
                        locked_until = CASE
                          WHEN failed_login_attempts + 1 >= 5
                           THEN DATE_ADD(NOW(), INTERVAL 30 MINUTE)
                          ELSE locked_until
                        END
                    WHERE id = :user_id
                """),
                {"user_id": user_id},
            )
            session.commit()

    def reset_failed_login(self, user_id: int) -> None:
        """Reset failed_login_attempts on successful login."""
        with session_scope() as session:
            session.execute(
                text("""
                    UPDATE users
                    SET failed_login_attempts = 0,
                        locked_until = NULL,
                        last_login_at = NOW()
                    WHERE id = :user_id
                """),
                {"user_id": user_id},
            )
            session.commit()

    def get_locked_until(self, user_id: int) -> Optional[datetime]:
        """Fetch locked_until for a user. Internal use by AuthUseCase."""
        with session_scope() as session:
            row = session.execute(
                text("SELECT locked_until FROM users WHERE id = :user_id"),
                {"user_id": user_id},
            ).fetchone()
            return row.locked_until if row else None

    def verify_password(self, user_id: int, plain_password: str) -> bool:
        """Fetch password hash and verify. Internal use by AuthUseCase."""
        with session_scope() as session:
            row = session.execute(
                text("SELECT password_hash FROM users WHERE id = :user_id AND deleted_at IS NULL"),
                {"user_id": user_id},
            ).fetchone()
            if not row or not row.password_hash:
                return False
            from library.dddpy.shared.utils.password import password
            return password.verify_password(plain_password, row.password_hash)

    def get_token_version(self, user_id: int) -> int:
        """Fetch current token_version for a user. Default 0 if column missing."""
        with session_scope() as session:
            row = session.execute(
                text("SELECT token_version FROM users WHERE id = :user_id"),
                {"user_id": user_id},
            ).fetchone()
            return row.token_version if row and row.token_version is not None else 0

    def increment_token_version(self, user_id: int) -> int:
        """
        Increment token_version and return the new value.
        Call this on logout-all, password reset, account suspension/lock.
        """
        with session_scope() as session:
            session.execute(
                text("UPDATE users SET token_version = token_version + 1 WHERE id = :user_id"),
                {"user_id": user_id},
            )
            session.commit()
            row = session.execute(
                text("SELECT token_version FROM users WHERE id = :user_id"),
                {"user_id": user_id},
            ).fetchone()
            new_version = row.token_version if row else 0
            logger.info(f"Incremented token_version to {new_version} for user_id={user_id}")
            return new_version
