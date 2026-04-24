"""
from typing import Optional
ChargeType use case — orchestrates all charge type operations.
"""
from typing import Optional

from library.dddpy.core_charge_types.usecase.charge_type_cmd_usecase import (
    ChargeTypeCmdUseCase,
    charge_type_cmd_usecase_factory,
)
from library.dddpy.core_charge_types.usecase.charge_type_query_usecase import (
    ChargeTypeQueryUseCase,
    charge_type_query_usecase_factory,
)
from library.dddpy.core_charge_types.usecase.charge_type_cmd_schema import (
    CreateChargeTypeSchema,
    UpdateChargeTypeSchema,
)
from library.dddpy.core_charge_types.domain.charge_type_entity import ChargeTypeEntity
from library.dddpy.core_charge_types.domain.charge_type_exception import (
    ChargeTypeNotFound,
)
from library.dddpy.core_charge_types.domain.charge_type_success import ChargeTypeSuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ChargeTypeUseCase")


class ChargeTypeUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self._cmd: ChargeTypeCmdUseCase = charge_type_cmd_usecase_factory()
        self._query: ChargeTypeQueryUseCase = charge_type_query_usecase_factory()
        logger.info("ChargeTypeUseCase initialized")

    # ── Create ─────────────────────────────────────────────────────────────

    def create(self, data: CreateChargeTypeSchema):
        logger.add_inside_method("create")
        from library.dddpy.core_charge_types.domain.charge_type_data import (
            CreateChargeTypeData,
        )
        cmd_data = CreateChargeTypeData(
            code=data.code,
            name=data.name,
            description=data.description,
            is_global=data.is_global,
            is_active=data.is_active,
            sort_order=data.sort_order,
        )
        entity = self._cmd.create(cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=ChargeTypeSuccessMessage.CREATED,
            data=entity.to_dict(),
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        entity = self._query.get_by_id(id)
        if not entity:
            raise ChargeTypeNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=ChargeTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        entity = self._query.get_by_uuid(uuid)
        if not entity:
            raise ChargeTypeNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=ChargeTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_code(self, code: str):
        logger.add_inside_method("get_by_code")
        entity = self._query.get_by_code(code)
        if not entity:
            raise ChargeTypeNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=ChargeTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateChargeTypeSchema):
        logger.add_inside_method("update")
        existing = self._query.get_by_id(id)
        if not existing:
            raise ChargeTypeNotFound()

        from library.dddpy.core_charge_types.domain.charge_type_data import (
            UpdateChargeTypeData,
        )
        cmd_data = UpdateChargeTypeData(
            name=data.name,
            description=data.description,
            is_global=data.is_global,
            is_active=data.is_active,
            sort_order=data.sort_order,
        )
        entity = self._cmd.update(id, cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=ChargeTypeSuccessMessage.UPDATED,
            data=entity.to_dict(),
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def soft_delete(self, id: int):
        logger.add_inside_method("soft_delete")
        existing = self._query.get_by_id(id)
        if not existing:
            raise ChargeTypeNotFound()
        self._cmd.soft_delete(id)
        fresh = self._query._get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=ChargeTypeSuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        existing = self._query._get_by_id_any_status(id)
        if not existing:
            raise ChargeTypeNotFound()
        self._cmd.restore(id)
        entity = self._query.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=ChargeTypeSuccessMessage.RESTORED,
            data=entity.to_dict(),
        )

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        existing = self._query.get_by_id(id)
        if not existing:
            raise ChargeTypeNotFound()
        self._cmd.hard_delete(id)
        return ResponseSuccessSchema(
            success=True,
            message="Charge type hard deleted successfully",
            data={"id": id},
        )

    # ── List ───────────────────────────────────────────────────────────────

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")
        if limit > 500:
            limit = 500
        entities, total = self._query.list_all(
            skip=skip,
            limit=limit,
            is_active=is_active,
            include_deleted=include_deleted,
        )
        return ResponseSuccessSchema(
            success=True,
            message=ChargeTypeSuccessMessage.LISTED,
            data={
                "items": [e.to_dict() for e in entities],
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters": {
                    "is_active": is_active,
                    "include_deleted": include_deleted,
                },
            },
        )
