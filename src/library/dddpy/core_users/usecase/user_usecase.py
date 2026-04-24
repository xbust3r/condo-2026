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

    def get_consolidated_view(self, user_id: int) -> dict:
        """
        Phase 1e: Get a consolidated view of a user.

        Returns user + profile + roles + ownerships + occupancies
        all merged into a single response dict.
        """
        user = self._query.get_by_id(user_id, include_deleted=False)
        if not user:
            raise UserNotFound(f"User with id={user_id} not found")

        # 1. User data
        result = {
            "user": user.to_dict(),
        }

        # 1b. Profile data
        from library.dddpy.core_user_profiles.infrastructure.user_profile_query_repository import (
            UserProfileQueryRepositoryImpl,
        )
        profile_repo = UserProfileQueryRepositoryImpl()
        profile = profile_repo.get_by_user_id(user_id)
        result["profile"] = profile.to_dict() if profile else None

        # 2. Active roles for this user
        from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
            CondominiumRoleQueryRepositoryImpl,
        )
        role_repo = CondominiumRoleQueryRepositoryImpl()
        roles, total_roles = role_repo.list_all(
            user_id=user_id,
            status="active",
            include_deleted=False,
        )
        result["roles"] = {
            "items": [r.to_dict() for r in roles],
            "total": total_roles,
        }

        # 3. Active ownerships for this user
        from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_query_repository import (
            UnitOwnershipQueryRepositoryImpl,
        )
        ownership_repo = UnitOwnershipQueryRepositoryImpl()
        ownerships, total_ownerships = ownership_repo.list_by_user(
            user_id=user_id,
            status="active",
            include_deleted=False,
        )
        result["ownerships"] = {
            "items": [o.to_dict() for o in ownerships],
            "total": total_ownerships,
        }

        # 4. Active occupancies for this user
        from library.dddpy.core_unit_occupancies.infrastructure.unit_occupancy_query_repository import (
            UnitOccupancyQueryRepositoryImpl,
        )
        occupancy_repo = UnitOccupancyQueryRepositoryImpl()
        occupancies, total_occupancies = occupancy_repo.list_by_user(
            user_id=user_id,
            status="active",
            include_deleted=False,
        )
        result["occupancies"] = {
            "items": [o.to_dict() for o in occupancies],
            "total": total_occupancies,
        }

        return result

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

        USR-01 cascade: also closes active roles, ownerships, and occupancies
        for this user to prevent orphan records.
        """
        user = self._query.get_by_id(user_id, include_deleted=False)
        if not user:
            raise UserNotFound(f"User with id={user_id} not found")

        self._cmd.soft_delete(user_id)
        new_version = self._cmd.increment_token_version(user_id)

        # USR-01 cascade: roles → soft-delete
        from library.dddpy.core_condominium_roles.infrastructure.condominium_role_cmd_repository import (
            CondominiumRoleCmdRepositoryImpl,
        )
        role_repo = CondominiumRoleCmdRepositoryImpl()
        roles_count = role_repo.soft_delete_by_user(user_id)

        # USR-01 cascade: ownerships → historical + end_date
        from library.dddpy.core_unit_ownerships.infrastructure.unit_ownership_cmd_repository import (
            UnitOwnershipCmdRepositoryImpl,
        )
        ownership_repo = UnitOwnershipCmdRepositoryImpl()
        ownerships_count = ownership_repo.soft_delete_by_user(user_id)

        # USR-01 cascade: occupancies → inactive + end_date
        from library.dddpy.core_unit_occupancies.infrastructure.unit_occupancy_cmd_repository import (
            UnitOccupancyCmdRepositoryImpl,
        )
        occupancy_repo = UnitOccupancyCmdRepositoryImpl()
        occupancies_count = occupancy_repo.soft_delete_by_user(user_id)

        logger.info(
            f"User soft deleted: id={user_id}, token_version={new_version}, "
            f"cascade: roles={roles_count}, ownerships={ownerships_count}, occupancies={occupancies_count}"
        )

        return ResponseSuccessSchema(
            success=True,
            message=UserSuccessMessage.SOFT_DELETED,
            data={
                "id": user_id,
                "token_version": new_version,
                "cascade": {
                    "roles_closed": roles_count,
                    "ownerships_historical": ownerships_count,
                    "occupancies_inactive": occupancies_count,
                },
            },
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
