"""
Mapper — converts DB rows to UserEntity.
"""
from typing import Any

from library.dddpy.core_users.domain.user_entity import UserEntity


class UserMapper:

    @staticmethod
    def from_row_with_profile(row: Any) -> UserEntity:
        """
        Map a single DB row (users + user_profiles JOIN) to UserEntity.
        Profile columns are accessed directly from the joined row.
        """
        entity = UserEntity(
            id=row.id,
            uuid=row.uuid,
            email=row.email,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
            email_verified_at=getattr(row, "email_verified_at", None),
            last_login_at=getattr(row, "last_login_at", None),
            failed_login_attempts=getattr(row, "failed_login_attempts", 0) or 0,
            locked_until=getattr(row, "locked_until", None),
            token_version=getattr(row, "token_version", 0) or 0,
        )

        # Profile fields — present only when user has a profile (LEFT JOIN)
        if getattr(row, "profile_uuid", None) or getattr(row, "first_name", None):
            entity.profile_uuid = getattr(row, "profile_uuid", None)
            entity.first_name = getattr(row, "first_name", None)
            entity.last_name = getattr(row, "last_name", None)
            entity.document_type = getattr(row, "document_type", None)
            entity.document_number = getattr(row, "document_number", None)
            entity.phone = getattr(row, "phone", None)

        return entity

    @staticmethod
    def from_row_brief(row: Any) -> UserEntity:
        """Lightweight mapping for list views (no profile join)."""
        return UserEntity(
            id=row.id,
            uuid=row.uuid,
            email=row.email,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
            email_verified_at=None,
            last_login_at=None,
            failed_login_attempts=0,
            locked_until=None,
            token_version=getattr(row, "token_version", 0) or 0,
        )
