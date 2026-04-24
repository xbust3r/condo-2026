from typing import Optional
from typing import Optional, Tuple, List

from library.dddpy.core_unit_types.usecase.unit_type_cmd_usecase import (
    UnitTypeCmdUseCase,
)
from library.dddpy.core_unit_types.usecase.unit_type_query_usecase import (
    UnitTypeQueryUseCase,
)
from library.dddpy.core_unit_types.usecase.unit_type_factory import (
    unit_type_cmd_usecase_factory,
    unit_type_query_usecase_factory,
)
from library.dddpy.core_unit_types.usecase.unit_type_cmd_schema import (
    CreateUnitTypeSchema,
    UpdateUnitTypeSchema,
)
from library.dddpy.core_unit_types.domain.unit_type_exception import (
    UnitTypeNotFound,
    UnitTypeIsInactive,
    UnitTypeIsDeleted,
    UnitTypeNotAccessible,
)
from library.dddpy.core_unit_types.domain.unit_type_success import UnitTypeSuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitTypeUseCase")


class UnitTypeUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self._cmd: UnitTypeCmdUseCase = unit_type_cmd_usecase_factory()
        self._query: UnitTypeQueryUseCase = unit_type_query_usecase_factory()
        logger.info("UnitTypeUseCase initialized")

    # ── Create ─────────────────────────────────────────────────────────────

    def create(self, data: CreateUnitTypeSchema):
        logger.add_inside_method("create")
        from library.dddpy.core_unit_types.domain.unit_type_data import (
            CreateUnitTypeData,
        )
        cmd_data = CreateUnitTypeData(
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
            message=UnitTypeSuccessMessage.CREATED,
            data=entity.to_dict(),
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        entity = self._query.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=UnitTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        entity = self._query.get_by_uuid(uuid)
        return ResponseSuccessSchema(
            success=True,
            message=UnitTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateUnitTypeSchema):
        logger.add_inside_method("update")
        from library.dddpy.core_unit_types.domain.unit_type_data import (
            UpdateUnitTypeData,
        )
        cmd_data = UpdateUnitTypeData(
            name=data.name,
            description=data.description,
            usage_class=data.usage_class,
            sort_order=data.sort_order,
            status=data.status,
        )
        entity = self._cmd.update(id, cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=UnitTypeSuccessMessage.UPDATED,
            data=entity.to_dict(),
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def soft_delete(self, id: int):
        logger.add_inside_method("soft_delete")
        # Verify it exists first
        existing = self._query.get_by_id(id)
        if not existing:
            raise UnitTypeNotFound()
        self._cmd.soft_delete(id)
        # Re-fetch to return actual persisted state
        fresh = self._query.get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=UnitTypeSuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        # Verify it exists first (any-status since entity may be soft-deleted)
        existing = self._query.get_by_id_any_status(id)
        if not existing:
            raise UnitTypeNotFound()
        restored = self._cmd.restore(id)
        if not restored:
            raise UnitTypeNotFound()
        entity = self._query.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=UnitTypeSuccessMessage.RESTORED,
            data=entity.to_dict(),
        )

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        self._cmd.hard_delete(id)
        return ResponseSuccessSchema(
            success=True,
            message=UnitTypeSuccessMessage.HARD_DELETED,
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
            message=UnitTypeSuccessMessage.LISTED,
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

    def validate_for_unit_assignment(
        self,
        type_id: int,
        condominium_id: int,
    ) -> None:
        """
        Validate unit_type_id for assignment to a unit.

        Rules:
        - Type must exist and not be soft-deleted
        - Type must be active (status=1)
        - Type must be global OR belong to the same condominium

        Raises DomainException on failure. Silent pass if type_id is None.
        """
        if type_id is None:
            return
        logger.add_inside_method("validate_for_unit_assignment")
        entity = self._query.get_active_for_unit_assignment(type_id, condominium_id)
        if not entity:
            exists = self._query.get_by_id(type_id)
            if not exists:
                raise UnitTypeNotFound()
            if exists.is_deleted():
                raise UnitTypeIsDeleted()
            if exists.status != 1:
                raise UnitTypeIsInactive()
            raise UnitTypeNotAccessible()

    def get_active_for_unit_assignment(
        self,
        type_id: int,
        condominium_id: int,
    ):
        logger.add_inside_method("get_active_for_unit_assignment")
        entity = self._query.get_active_for_unit_assignment(type_id, condominium_id)
        return ResponseSuccessSchema(
            success=True,
            message=UnitTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )