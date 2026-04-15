"""
User use case — orchestrates all user operations.

Coordinates UserCmdRepositoryImpl (write) + UserQueryRepositoryImpl (read).
"""
from typing import Optional

from library.dddpy.core_users.domain.user_entity import UserEntity
from library.dddpy.core_users.domain.user_exception import (
    UserNotFound,
    UserAlreadyExists,
    UserInvalidStatus,
    UserPasswordRequired,
)
from library.dddpy.core_users.domain.user_success import UserSuccessMessage
from library.dddpy.core_users.infrastructure.user_cmd_repository import UserCmdRepositoryImpl
from library.dddpy.core_users.infrastructure.user_query_repository import UserQueryRepositoryImpl
from library.dddpy.core_users.usecase.user_cmd_schema import CreateUserSchema, UpdateUserSchema
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.utils.password import password


logger = Logger("UserUseCase")

_VALID_STATUSES = {"active", "pending", "suspended", "inactive", "locked"}


class UserUseCase:

    def __init__(self):
        self._cmd = UserCmdRepositoryImpl()
        self._query = UserQueryRepositoryImpl()
        logger.info("UserUseCase initialized")

    # ── Create ──────────────────────────────────────────────────────────

    def create(self, schema: CreateUserSchema) -> ResponseSuccessSchema:
        """Create a new user. Password is hashed before storage."""
        if not schema.password:
            raise UserPasswordRequired("Password is required")

        password_hash = password.bcrypt_password(schema.password)

        user_id = self._cmd.create(
            email=schema.email,
            password_hash=password_hash,
            status=schema.status or "active",
        )

        user = self._query.get_by_id(user_id)
        logger.info(f"User created: id={user_id}, email={schema.email}")

        return ResponseSuccessSchema(
            success=True,
            message=UserSuccessMessage.CREATED,
            data=user.to_dict(),
        )

    # ── Read ─────────────────────────────────────────────────────────────

    def get_by_id(self, user_id: int, include_deleted: bool = False) -> ResponseSuccessSchema:
        """Get a user by numeric id."""
        user = self._query.get_by_id(user_id, include_deleted=include_deleted)
        if not user:
            raise UserNotFound(f"User with id={user_id} not found")

        return ResponseSuccessSchema(
            success=True,
            message=UserSuccessMessage.FOUND,
            data=user.to_dict(),
        )

    def get_by_uuid(self, uuid: str, include_deleted: bool = False) -> ResponseSuccessSchema:
        """Get a user by uuid."""
        user = self._query.get_by_uuid(uuid, include_deleted=include_deleted)
        if not user:
            raise UserNotFound(f"User with uuid={uuid} not found")

        return ResponseSuccessSchema(
            success=True,
            message=UserSuccessMessage.FOUND,
            data=user.to_dict(),
        )

    def list(
        self,
        email: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> ResponseSuccessSchema:
        """List users with optional filters."""
        users, total = self._query.list(
            email=email,
            status=status,
            include_deleted=include_deleted,
            limit=limit,
            offset=offset,
        )

        return ResponseSuccessSchema(
            success=True,
            message=UserSuccessMessage.LIST,
            data={
                "items": [u.to_dict_brief() for u in users],
                "total": total,
                "limit": limit,
                "offset": offset,
            },
        )

    # ── Update ───────────────────────────────────────────────────────────

    def update(self, user_id: int, schema: UpdateUserSchema) -> ResponseSuccessSchema:
        """Update email and/or status of a user."""
        user = self._query.get_by_id(user_id, include_deleted=False)
        if not user:
            raise UserNotFound(f"User with id={user_id} not found")

        new_email = schema.email if schema.email is not None else user.email
        new_status = schema.status if schema.status is not None else user.status

        if new_status not in _VALID_STATUSES:
            raise UserInvalidStatus(f"Invalid status: {new_status}")

        # Check for duplicate email (excluding current user)
        if new_email != user.email:
            existing = self._query.get_by_email(new_email)
            if existing and existing.id != user_id:
                raise UserAlreadyExists(f"Email {new_email} is already in use by another user")

        self._cmd.update(user_id=user_id, email=new_email, status=new_status)

        updated_user = self._query.get_by_id(user_id)
        logger.info(f"User updated: id={user_id}")

        return ResponseSuccessSchema(
            success=True,
            message=UserSuccessMessage.UPDATED,
            data=updated_user.to_dict(),
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def soft_delete(self, user_id: int) -> ResponseSuccessSchema:
        """
        Soft delete a user AND increment token_version.
        This immediately invalidates all active JWTs for this user.
        """
        user = self._query.get_by_id(user_id, include_deleted=False)
        if not user:
            raise UserNotFound(f"User with id={user_id} not found")

        self._cmd.soft_delete(user_id)
        new_version = self._cmd.increment_token_version(user_id)

        logger.info(
            f"User soft deleted: id={user_id}, token_version incremented to {new_version}"
        )

        return ResponseSuccessSchema(
            success=True,
            message=UserSuccessMessage.SOFT_DELETED,
            data={"id": user_id, "token_version": new_version},
        )

    def restore(self, user_id: int) -> ResponseSuccessSchema:
        """Restore a soft-deleted user."""
        user = self._query.get_by_id(user_id, include_deleted=True)
        if not user:
            raise UserNotFound(f"User with id={user_id} not found")
        if not user.deleted_at:
            raise UserInvalidStatus("User is not deleted — nothing to restore")

        self._cmd.restore(user_id)
        restored_user = self._query.get_by_id(user_id)
        logger.info(f"User restored: id={user_id}")

        return ResponseSuccessSchema(
            success=True,
            message=UserSuccessMessage.RESTORED,
            data=restored_user.to_dict(),
        )

    # ── Status transitions ────────────────────────────────────────────────

    def suspend(self, user_id: int) -> ResponseSuccessSchema:
        """Suspend a user — sets status=suspended and increments token_version."""
        user = self._query.get_by_id(user_id, include_deleted=False)
        if not user:
            raise UserNotFound(f"User with id={user_id} not found")

        self._cmd.set_status(user_id, "suspended")
        new_version = self._cmd.increment_token_version(user_id)

        suspended_user = self._query.get_by_id(user_id)
        logger.info(
            f"User suspended: id={user_id}, token_version incremented to {new_version}"
        )

        return ResponseSuccessSchema(
            success=True,
            message=UserSuccessMessage.SUSPENDED,
            data={**suspended_user.to_dict(), "token_version": new_version},
        )

    def activate(self, user_id: int) -> ResponseSuccessSchema:
        """Activate a user — sets status=active."""
        user = self._query.get_by_id(user_id, include_deleted=False)
        if not user:
            raise UserNotFound(f"User with id={user_id} not found")

        self._cmd.set_status(user_id, "active")
        activated_user = self._query.get_by_id(user_id)
        logger.info(f"User activated: id={user_id}")

        return ResponseSuccessSchema(
            success=True,
            message=UserSuccessMessage.ACTIVATED,
            data=activated_user.to_dict(),
        )
