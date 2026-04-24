"""
from typing import Optional
User query repository implementation — read operations on users + user_profiles.
"""
from typing import Optional, Tuple, List

from sqlalchemy import text

from library.dddpy.core_users.domain.user_entity import UserEntity
from library.dddpy.core_users.infrastructure.user_mapper import UserMapper
from library.dddpy.core_users.domain.user_query_repository import UserQueryRepository
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UserQueryRepository")


class UserQueryRepositoryImpl(UserQueryRepository):

    def get_by_id(
        self, user_id: int, include_deleted: bool = False,
    ) -> Optional[UserEntity]:
        """Get a user by numeric id with profile data."""
        deleted_filter = "" if include_deleted else "AND u.deleted_at IS NULL"

        with session_scope() as session:
            row = session.execute(
                text(f"""
                    SELECT
                      u.id, u.uuid, u.email, u.status,
                      u.created_at, u.updated_at, u.deleted_at,
                      u.email_verified_at, u.last_login_at,
                      u.failed_login_attempts, u.locked_until, u.token_version,
                      p.uuid AS profile_uuid,
                      p.first_name, p.last_name,
                      p.document_type, p.document_number,
                      p.phone
                    FROM users u
                    LEFT JOIN user_profiles p ON p.user_id = u.id AND p.deleted_at IS NULL
                    WHERE u.id = :user_id {deleted_filter}
                """),
                {"user_id": user_id},
            ).fetchone()

            if not row:
                return None

            return UserMapper.from_row_with_profile(row)

    def get_by_uuid(
        self, uuid: str, include_deleted: bool = False,
    ) -> Optional[UserEntity]:
        """Get a user by uuid with profile data."""
        deleted_filter = "" if include_deleted else "AND u.deleted_at IS NULL"

        with session_scope() as session:
            row = session.execute(
                text(f"""
                    SELECT
                      u.id, u.uuid, u.email, u.status,
                      u.created_at, u.updated_at, u.deleted_at,
                      u.email_verified_at, u.last_login_at,
                      u.failed_login_attempts, u.locked_until, u.token_version,
                      p.uuid AS profile_uuid,
                      p.first_name, p.last_name,
                      p.document_type, p.document_number,
                      p.phone
                    FROM users u
                    LEFT JOIN user_profiles p ON p.user_id = u.id AND p.deleted_at IS NULL
                    WHERE u.uuid = :uuid {deleted_filter}
                """),
                {"uuid": uuid},
            ).fetchone()

            if not row:
                return None

            return UserMapper.from_row_with_profile(row)

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get a user by email address (only active, non-deleted users)."""
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT id FROM users WHERE email = :email AND deleted_at IS NULL
                """),
                {"email": email},
            ).fetchone()
            if not row:
                return None
            return self.get_by_id(row.id, include_deleted=False)

    def list(
        self,
        email: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[UserEntity], int]:
        """
        List users with optional filters.
        Returns (users, total_count).
        """
        deleted_filter = "" if include_deleted else "AND u.deleted_at IS NULL"
        email_filter = f"AND u.email LIKE :email" if email else ""
        status_filter = f"AND u.status = :status" if status else ""

        count_query = text(f"""
            SELECT COUNT(*) FROM users u
            WHERE 1=1 {deleted_filter} {email_filter} {status_filter}
        """)
        params = {}
        if email:
            params["email"] = f"%{email}%"
        if status:
            params["status"] = status

        with session_scope() as session:
            total = session.execute(count_query, params).scalar() or 0

            rows = session.execute(
                text(f"""
                    SELECT
                      u.id, u.uuid, u.email, u.status,
                      u.created_at, u.updated_at, u.deleted_at,
                      u.token_version
                    FROM users u
                    WHERE 1=1 {deleted_filter} {email_filter} {status_filter}
                    ORDER BY u.created_at DESC
                    LIMIT :limit OFFSET :offset
                """),
                {**params, "limit": limit, "offset": offset},
            ).fetchall()

            users = [UserMapper.from_row_brief(r) for r in rows]
            return users, total
