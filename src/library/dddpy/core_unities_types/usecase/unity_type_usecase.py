from typing import Optional, Tuple, List

from library.dddpy.core_unities_types.usecase.unity_type_cmd_usecase import (
    UnityTypeCmdUseCase,
)
from library.dddpy.core_unities_types.usecase.unity_type_query_usecase import (
    UnityTypeQueryUseCase,
)
from library.dddpy.core_unities_types.usecase.unity_type_factory import (
    unity_type_cmd_usecase_factory,
    unity_type_query_usecase_factory,
)
from library.dddpy.core_unities_types.usecase.unity_type_cmd_schema import (
    CreateUnityTypeSchema,
    UpdateUnityTypeSchema,
)
from library.dddpy.core_unities_types.domain.unity_type_exception import (
    UnityTypeNotFound,
    UnityTypeIsInactive,
    UnityTypeIsDeleted,
    UnityTypeNotAccessible,
)
from library.dddpy.core_unities_types.domain.unity_type_success import UnityTypeSuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnityTypeUseCase")


class UnityTypeUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self._cmd: UnityTypeCmdUseCase = unity_type_cmd_usecase_factory()
        self._query: UnityTypeQueryUseCase = unity_type_query_usecase_factory()
        logger.info("UnityTypeUseCase initialized")

    # ── Create ─────────────────────────────────────────────────────────────

    def create(self, data: CreateUnityTypeSchema):
        logger.add_inside_method("create")
        from library.dddpy.core_unities_types.domain.unity_type_data import (
            CreateUnityTypeData,
        )
        cmd_data = CreateUnityTypeData(
            condominium_id=data.condominium_id,
            code=data.code,
            name=data.name,
            description=data.description,
            usage_class=data.usage_class,
            is_system=False,
            sort_order=data.sort_order,
        )
        entity = self._cmd.create(cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=UnityTypeSuccessMessage.CREATED,
            data=entity.to_dict(),
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        entity = self._query.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=UnityTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        entity = self._query.get_by_uuid(uuid)
        return ResponseSuccessSchema(
            success=True,
            message=UnityTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateUnityTypeSchema):
        logger.add_inside_method("update")
        from library.dddpy.core_unities_types.domain.unity_type_data import (
            UpdateUnityTypeData,
        )
        cmd_data = UpdateUnityTypeData(
            name=data.name,
            description=data.description,
            usage_class=data.usage_class,
            sort_order=data.sort_order,
            status=data.status,
        )
        entity = self._cmd.update(id, cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=UnityTypeSuccessMessage.UPDATED,
            data=entity.to_dict(),
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def soft_delete(self, id: int):
        logger.add_inside_method("soft_delete")
        # Verify it exists first
        existing = self._query.get_by_id(id)
        if not existing:
            raise UnityTypeNotFound()
        self._cmd.soft_delete(id)
        # Re-fetch to return actual persisted state
        fresh = self._query.get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=UnityTypeSuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        # Verify it exists first (any-status since entity may be soft-deleted)
        existing = self._query.get_by_id_any_status(id)
        if not existing:
            raise UnityTypeNotFound()
        restored = self._cmd.restore(id)
        if not restored:
            raise UnityTypeNotFound()
        entity = self._query.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=UnityTypeSuccessMessage.RESTORED,
            data=entity.to_dict(),
        )

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        self._cmd.hard_delete(id)
        return ResponseSuccessSchema(
            success=True,
            message=UnityTypeSuccessMessage.HARD_DELETED,
            data={"id": id},
        )

    # ── List ───────────────────────────────────────────────────────────────

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        include_system: bool = True,
        status: Optional[int] = None,
        usage_class: Optional[str] = None,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        if limit > 500:
            limit = 500
        entities, total = self._query.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            include_system=include_system,
            status=status,
            usage_class=usage_class,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message=UnityTypeSuccessMessage.LISTED,
            data={
                "items": [e.to_dict() for e in entities],
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters": {
                    "condominium_id": condominium_id,
                    "include_system": include_system,
                    "status": status,
                    "usage_class": usage_class,
                    "include_deleted": include_deleted,
                },
            },
        )

    # ── Validation for assignment ────────────────────────────────────────

    def validate_for_unity_assignment(
        self,
        type_id: int,
        condominium_id: int,
    ) -> None:
        """
        Validate unity_type_id for assignment to a unity.

        Rules:
        - Type must exist and not be soft-deleted
        - Type must be active (status=1)
        - Type must be global OR belong to the same condominium

        Raises DomainException on failure. Silent pass if type_id is None.
        """
        if type_id is None:
            return
        logger.add_inside_method("validate_for_unity_assignment")
        entity = self._query.get_active_for_unity_assignment(type_id, condominium_id)
        if not entity:
            exists = self._query.get_by_id(type_id)
            if not exists:
                raise UnityTypeNotFound()
            if exists.is_deleted():
                raise UnityTypeIsDeleted()
            if exists.status != 1:
                raise UnityTypeIsInactive()
            raise UnityTypeNotAccessible()

    def get_active_for_unity_assignment(
        self,
        type_id: int,
        condominium_id: int,
    ):
        logger.add_inside_method("get_active_for_unity_assignment")
        entity = self._query.get_active_for_unity_assignment(type_id, condominium_id)
        return ResponseSuccessSchema(
            success=True,
            message=UnityTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )
