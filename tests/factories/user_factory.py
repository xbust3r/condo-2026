"""
Factory: UserEntity (users table).

Creates test user records directly in the DB.
Note: uses the `users` table, not a domain-named table.
"""
import uuid
import hashlib
from sqlalchemy.orm import Session

from library.dddpy.core_users.infrastructure.dbuser import DBUser
from sqlalchemy import func


class UserFactory:
    """Factory for creating test User records."""

    @staticmethod
    def _hash_password(password: str) -> str:
        """Simple SHA256 hash for test fixtures (not for production)."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def create(
        session: Session,
        email: str = None,
        password: str = "TestPassword123!",
        status: str = "active",
        **kwargs,
    ) -> DBUser:
        """
        Create and persist a User record.

        Usage:
            user = UserFactory.create(session, email="john@example.com")
        """
        if email is None:
            email = f"user-{uuid.uuid4().hex[:8]}@test.local"

        db_user = DBUser(
            uuid=str(uuid.uuid4()),
            email=email,
            password_hash=UserFactory._hash_password(password),
            status=status,
            updated_at=kwargs.get("updated_at", func.now()),
            email_verified_at=kwargs.get("email_verified_at"),
            last_login_at=kwargs.get("last_login_at"),
            failed_login_attempts=kwargs.get("failed_login_attempts", 0),
            token_version=kwargs.get("token_version", 0),
        )
        session.add(db_user)
        session.flush()
        session.refresh(db_user)
        return db_user
