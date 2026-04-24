"""
from typing import Optional
User profile query repository — read operations.
"""
from typing import Optional

from sqlalchemy import text

from library.dddpy.core_user_profiles.domain.user_profile_entity import UserProfileEntity
from library.dddpy.core_user_profiles.domain.user_profile_query_repository import UserProfileQueryRepository
from library.dddpy.core_user_profiles.infrastructure.user_profile_mapper import UserProfileMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UserProfileQueryRepository")


class UserProfileQueryRepositoryImpl(UserProfileQueryRepository):

    def get_by_user_id(self, user_id: int) -> Optional[UserProfileEntity]:
        """Get a profile by user_id."""
        with session_scope() as session:
            row = session.execute(
                text("""
                    SELECT
                      id, uuid, user_id,
                      first_name, last_name,
                      document_type, document_number,
                      phone, birth_date,
                      created_at, updated_at
                    FROM user_profiles
                    WHERE user_id = :user_id
                      AND deleted_at IS NULL
                """),
                {"user_id": user_id},
            ).fetchone()

            if not row:
                return None

            return UserProfileMapper.from_row(row)
