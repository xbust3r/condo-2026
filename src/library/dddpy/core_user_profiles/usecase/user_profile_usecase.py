"""
User profile use case — orchestrates all profile operations.

Coordinates UserProfileCmdRepositoryImpl (write) + UserProfileQueryRepositoryImpl (read).
Separated from auth concerns — no auth logic here.
"""
from library.dddpy.core_user_profiles.domain.user_profile_entity import UserProfileEntity
from library.dddpy.core_user_profiles.domain.user_profile_exception import (
    UserProfileNotFound,
    UserProfileAlreadyExists,
)
from library.dddpy.core_user_profiles.domain.user_profile_success import UserProfileSuccessMessage
from library.dddpy.core_user_profiles.infrastructure.user_profile_cmd_repository import UserProfileCmdRepositoryImpl
from library.dddpy.core_user_profiles.infrastructure.user_profile_query_repository import UserProfileQueryRepositoryImpl
from library.dddpy.core_user_profiles.usecase.user_profile_cmd_schema import (
    CreateUserProfileSchema,
    UpdateUserProfileSchema,
)
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UserProfileUseCase")


class UserProfileUseCase:

    def __init__(self):
        self._cmd = UserProfileCmdRepositoryImpl()
        self._query = UserProfileQueryRepositoryImpl()
        logger.info("UserProfileUseCase initialized")

    def create(self, schema: CreateUserProfileSchema) -> ResponseSuccessSchema:
        """Create a profile for a user."""
        profile_id = self._cmd.create(
            user_id=schema.user_id,
            first_name=schema.first_name,
            last_name=schema.last_name,
            document_type=schema.document_type,
            document_number=schema.document_number,
            phone=schema.phone,
            birth_date=schema.birth_date,
        )

        profile = self._query.get_by_user_id(schema.user_id)
        logger.info(f"Profile created: id={profile_id}, user_id={schema.user_id}")

        return ResponseSuccessSchema(
            success=True,
            message=UserProfileSuccessMessage.CREATED,
            data=profile.to_dict(),
        )

    def get_by_user_id(self, user_id: int) -> ResponseSuccessSchema:
        """Get a profile by user_id."""
        profile = self._query.get_by_user_id(user_id)
        if not profile:
            raise UserProfileNotFound(f"Profile for user_id={user_id} not found")

        return ResponseSuccessSchema(
            success=True,
            message=UserProfileSuccessMessage.FOUND,
            data=profile.to_dict(),
        )

    def update(self, user_id: int, schema: UpdateUserProfileSchema) -> ResponseSuccessSchema:
        """Update a user's profile."""
        existing = self._query.get_by_user_id(user_id)
        if not existing:
            raise UserProfileNotFound(f"Profile for user_id={user_id} not found")

        self._cmd.update(
            user_id=user_id,
            first_name=schema.first_name,
            last_name=schema.last_name,
            document_type=schema.document_type,
            document_number=schema.document_number,
            phone=schema.phone,
            birth_date=schema.birth_date,
        )

        updated = self._query.get_by_user_id(user_id)
        logger.info(f"Profile updated for user_id={user_id}")

        return ResponseSuccessSchema(
            success=True,
            message=UserProfileSuccessMessage.UPDATED,
            data=updated.to_dict(),
        )
