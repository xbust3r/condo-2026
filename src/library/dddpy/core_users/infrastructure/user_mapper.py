"""
Mapper — converts DB rows to UserEntity.
"""
from typing import Optional, Any

from library.dddpy.core_users.domain.user_entity import UserEntity


class UserMapper:

    @staticmethod
    def from_row(row: Any, profile_row: Any = None) -> UserEntity:
        """
        Map a DB row (users) + optional profile row (user_profiles) to UserEntity.
        """
        entity = UserEntity(
            id=row.id,
            uuid=row.uuid,
            email=row.email,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
            email_verified_at=row.email_verified_at,
            last_login_at=row.last_login_at,
            failed_login_attempts=getattr(row, "failed_login_attempts", 0) or 0,
            locked_until=getattr(row, "locked_until", None),
            token_version=getattr(row, "token_version", 0) or 0,
        )

        if profile_row:
            entity.first_name = profile_row.first_name
            entity.last_name = profile_row.last_name
            entity.document_type = getattr(profile_row, "document_type", None)
            entity.document_number = getattr(profile_row, "document_number", None)
            entity.phone = profile_row.phone
            entity.profile_uuid = profile_row.uuid

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
