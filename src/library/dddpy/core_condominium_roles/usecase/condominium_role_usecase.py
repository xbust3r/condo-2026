from typing import Optional

from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_usecase import CondominiumRoleCmdUseCase
from library.dddpy.core_condominium_roles.usecase.condominium_role_query_usecase import CondominiumRoleQueryUseCase
from library.dddpy.core_condominium_roles.usecase.condominium_role_factory import (
    condominium_role_cmd_usecase_factory,
    condominium_role_query_usecase_factory,
)
from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
    CreateCondominiumRoleSchema,
    UpdateCondominiumRoleSchema,
)
from library.dddpy.core_condominium_roles.domain.condominium_role_exception import (
    CondominiumRoleNotFound,
    DuplicateRoleAssignment,
)
from library.dddpy.core_condominium_roles.domain.condominium_role_success import CondominiumRoleSuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumRoleUseCase")


class CondominiumRoleUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self.role_cmd_usecase: CondominiumRoleCmdUseCase = condominium_role_cmd_usecase_factory()
        self.role_query_usecase: CondominiumRoleQueryUseCase = condominium_role_query_usecase_factory()
        logger.info("CondominiumRoleUseCase initialized")

    # ── Create ─────────────────────────────────────────────────────────────

    def create(self, data: CreateCondominiumRoleSchema):
        logger.add_inside_method("create")
        logger.info(f"Creating condominium role with data: {data}")

        existing = self.role_query_usecase.get_active_by_user_and_condominium(
            data.user_id, data.condominium_id
        )
        if existing:
            logger.warning(
                f"User {data.user_id} already has an active role in condominium "
                f"{data.condominium_id}"
            )
            raise DuplicateRoleAssignment()

        new_role = self.role_cmd_usecase.create(data)
        return ResponseSuccessSchema(
            success=True,
            message=CondominiumRoleSuccessMessage.CREATED,
            data=new_role.to_dict(),
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        role = self.role_query_usecase.get_by_id(id)
        if not role:
            logger.warning(f"Condominium role not found by id={id}")
            raise CondominiumRoleNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=CondominiumRoleSuccessMessage.RETRIEVED,
            data=role.to_dict(),
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        role = self.role_query_usecase.get_by_uuid(uuid)
        if not role:
            logger.warning(f"Condominium role not found by uuid={uuid}")
            raise CondominiumRoleNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=CondominiumRoleSuccessMessage.RETRIEVED,
            data=role.to_dict(),
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateCondominiumRoleSchema):
        logger.add_inside_method("update")
        logger.info(f"Updating condominium role id={id} with data: {data}")

        existing = self.role_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Condominium role not found for update id={id}")
            raise CondominiumRoleNotFound()

        updated_role = self.role_cmd_usecase.update(id, data)
        if not updated_role:
            raise CondominiumRoleNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=CondominiumRoleSuccessMessage.UPDATED,
            data=updated_role.to_dict(),
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def delete(self, id: int):
        logger.add_inside_method("delete")
        logger.info(f"Soft deleting condominium role id={id}")

        existing = self.role_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Condominium role not found for delete id={id}")
            raise CondominiumRoleNotFound()

        deleted = self.role_cmd_usecase.soft_delete(id)
        if not deleted:
            raise CondominiumRoleNotFound()

        fresh = self.role_query_usecase._get_by_id_any_status(id)
        return ResponseSuccessSchema(
            success=True,
            message=CondominiumRoleSuccessMessage.DELETED,
            data={"id": id, "deleted_at": fresh.deleted_at if fresh else None},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        logger.info(f"Restoring condominium role id={id}")

        existing = self.role_query_usecase._get_by_id_any_status(id)
        if not existing:
            logger.warning(f"Condominium role not found for restore id={id}")
            raise CondominiumRoleNotFound()

        restored = self.role_cmd_usecase.restore(id)
        if not restored:
            logger.warning(f"Failed to restore condominium role id={id}")
            raise CondominiumRoleNotFound()

        refreshed = self.role_query_usecase._get_by_id_any_status(id)
        return ResponseSuccessSchema(
            success=True,
            message=CondominiumRoleSuccessMessage.RESTORED,
            data=refreshed.to_dict() if refreshed else {"id": id},
        )

    # ── List ───────────────────────────────────────────────────────────────

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        user_id: Optional[int] = None,
        role: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_all")
        if limit > 500:
            limit = 500
        roles, total = self.role_query_usecase.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            user_id=user_id,
            role=role,
            status=status,
            include_deleted=include_deleted,
        )
        items = [r.to_dict() for r in roles]
        return ResponseSuccessSchema(
            success=True,
            message=CondominiumRoleSuccessMessage.LISTED,
            data={
                "items": items,
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters": {
                    "condominium_id": condominium_id,
                    "user_id": user_id,
                    "role": role,
                    "status": status,
                    "include_deleted": include_deleted,
                },
            },
        )

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_by_condominium")
        if limit > 500:
            limit = 500
        roles, total = self.role_query_usecase.list_by_condominium(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
            role=role,
            status=status,
            include_deleted=include_deleted,
        )
        items = [r.to_dict() for r in roles]
        return ResponseSuccessSchema(
            success=True,
            message=CondominiumRoleSuccessMessage.LIST_BY_CONDOMINIUM,
            data={
                "items": items,
                "total": total,
                "condominium_id": condominium_id,
                "skip": skip,
                "limit": limit,
            },
        )

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_by_user")
        if limit > 500:
            limit = 500
        roles, total = self.role_query_usecase.list_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )
        items = [r.to_dict() for r in roles]
        return ResponseSuccessSchema(
            success=True,
            message=CondominiumRoleSuccessMessage.LIST_BY_USER,
            data={
                "items": items,
                "total": total,
                "user_id": user_id,
                "skip": skip,
                "limit": limit,
            },
        )

    # ── Hard delete ────────────────────────────────────────────────────────

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        logger.info(f"Attempting hard delete for condominium role id={id}")

        existing = self.role_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Condominium role not found for hard delete id={id}")
            raise CondominiumRoleNotFound()

        deleted = self.role_cmd_usecase.hard_delete(id)
        if not deleted:
            raise CondominiumRoleNotFound()

        return ResponseSuccessSchema(
            success=True,
            message=CondominiumRoleSuccessMessage.HARD_DELETED,
            data={"id": id},
        )
