"""
User command repository implementation — write operations on users.
"""
import uuid as uuid_lib

from sqlalchemy import text

from library.dddpy.core_users.domain.user_cmd_repository import UserCmdRepository
from library.dddpy.core_users.domain.user_exception import UserAlreadyExists
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UserCmdRepository")


class UserCmdRepositoryImpl(UserCmdRepository):

    def create(
        self,
        email: str,
        password_hash: str,
        status: str = "active",
    ) -> int:
        """Create a new user. Raises UserAlreadyExists on duplicate email."""
        user_uuid = str(uuid_lib.uuid4())

        with session_scope() as session:
            # Check for duplicate email first
            existing = session.execute(
                text("SELECT id FROM users WHERE email = :email AND deleted_at IS NULL"),
                {"email": email},
            ).fetchone()

            if existing:
                raise UserAlreadyExists(f"User with email {email} already exists")

            result = session.execute(
                text("""
                    INSERT INTO users (uuid, email, password_hash, status)
                    VALUES (:uuid, :email, :password_hash, :status)
                """),
                {
                    "uuid": user_uuid,
                    "email": email,
                    "password_hash": password_hash,
                    "status": status,
                },
            )
            session.commit()
            user_id = result.lastrowid
            logger.info(f"Created user id={user_id}, uuid={user_uuid}, email={email}")
            return user_id

    def update(self, user_id: int, email: str, status: str) -> None:
        """Update email and/or status of a user."""
        with session_scope() as session:
            session.execute(
                text("""
                    UPDATE users
                    SET email = :email, status = :status, updated_at = NOW()
                    WHERE id = :user_id
                """),
                {"user_id": user_id, "email": email, "status": status},
            )
            session.commit()
            logger.info(f"Updated user id={user_id}")

    def soft_delete(self, user_id: int) -> None:
        """Soft delete a user (set deleted_at)."""
        with session_scope() as session:
            session.execute(
                text("UPDATE users SET deleted_at = NOW() WHERE id = :user_id"),
                {"user_id": user_id},
            )
            session.commit()
            logger.info(f"Soft deleted user id={user_id}")

    def restore(self, user_id: int) -> None:
        """Restore a soft-deleted user."""
        with session_scope() as session:
            session.execute(
                text("UPDATE users SET deleted_at = NULL, updated_at = NOW() WHERE id = :user_id"),
                {"user_id": user_id},
            )
            session.commit()
            logger.info(f"Restored user id={user_id}")

    def set_status(self, user_id: int, status: str) -> None:
        """Set user status directly."""
        with session_scope() as session:
            session.execute(
                text("UPDATE users SET status = :status, updated_at = NOW() WHERE id = :user_id"),
                {"user_id": user_id, "status": status},
            )
            session.commit()
            logger.info(f"Set status={status} for user id={user_id}")

    def increment_token_version(self, user_id: int) -> int:
        """Increment token_version and return new value."""
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
            return row.token_version if row else 0
