"""
from typing import Optional
User profile command repository — write operations.
"""
import uuid as uuid_lib
from datetime import date
from typing import Optional

from sqlalchemy import text

from library.dddpy.core_user_profiles.domain.user_profile_cmd_repository import UserProfileCmdRepository
from library.dddpy.core_user_profiles.domain.user_profile_exception import UserProfileAlreadyExists
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UserProfileCmdRepository")


class UserProfileCmdRepositoryImpl(UserProfileCmdRepository):

    def create(
        self,
        user_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        document_type: Optional[str] = None,
        document_number: Optional[str] = None,
        phone: Optional[str] = None,
        birth_date: Optional[date] = None,
    ) -> int:
        """Create a profile for a user. Raises UserProfileAlreadyExists if already exists."""
        profile_uuid = str(uuid_lib.uuid4())

        with session_scope() as session:
            # Check if profile already exists
            existing = session.execute(
                text("SELECT id FROM user_profiles WHERE user_id = :user_id AND deleted_at IS NULL"),
                {"user_id": user_id},
            ).fetchone()

            if existing:
                raise UserProfileAlreadyExists(f"Profile for user_id={user_id} already exists")

            result = session.execute(
                text("""
                    INSERT INTO user_profiles
                      (uuid, user_id, first_name, last_name, document_type, document_number, phone, birth_date)
                    VALUES
                      (:uuid, :user_id, :first_name, :last_name, :document_type, :document_number, :phone, :birth_date)
                """),
                {
                    "uuid": profile_uuid,
                    "user_id": user_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "document_type": document_type,
                    "document_number": document_number,
                    "phone": phone,
                    "birth_date": birth_date,
                },
            )
            session.commit()
            profile_id = result.lastrowid
            logger.info(f"Created profile id={profile_id}, user_id={user_id}")
            return profile_id

    def update(
        self,
        user_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        document_type: Optional[str] = None,
        document_number: Optional[str] = None,
        phone: Optional[str] = None,
        birth_date: Optional[date] = None,
    ) -> None:
        """
        Update a user's profile — only sets fields that are explicitly provided (not None).
        Fields passed as None are preserved as-is in the database.
        """
        set_clauses = []
        params = {"user_id": user_id}

        if first_name is not None:
            set_clauses.append("first_name = :first_name")
            params["first_name"] = first_name
        if last_name is not None:
            set_clauses.append("last_name = :last_name")
            params["last_name"] = last_name
        if document_type is not None:
            set_clauses.append("document_type = :document_type")
            params["document_type"] = document_type
        if document_number is not None:
            set_clauses.append("document_number = :document_number")
            params["document_number"] = document_number
        if phone is not None:
            set_clauses.append("phone = :phone")
            params["phone"] = phone
        if birth_date is not None:
            set_clauses.append("birth_date = :birth_date")
            params["birth_date"] = birth_date

        if not set_clauses:
            logger.info(f"No fields to update for user_id={user_id}")
            return

        set_clauses.append("updated_at = NOW()")
        sql = text(f"""
            UPDATE user_profiles
            SET {', '.join(set_clauses)}
            WHERE user_id = :user_id
              AND deleted_at IS NULL
        """)

        with session_scope() as session:
            session.execute(sql, params)
            session.commit()
            logger.info(f"Updated profile for user_id={user_id}")
