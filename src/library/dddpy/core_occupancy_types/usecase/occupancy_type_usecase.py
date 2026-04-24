"""
OccupancyType use case — orchestrates all occupancy type operations.
"""
from typing import Optional, Tuple, List

from library.dddpy.core_occupancy_types.usecase.occupancy_type_cmd_usecase import (
    OccupancyTypeCmdUseCase,
)
from library.dddpy.core_occupancy_types.usecase.occupancy_type_query_usecase import (
    OccupancyTypeQueryUseCase,
)
from library.dddpy.core_occupancy_types.usecase.occupancy_type_factory import (
    occupancy_type_cmd_usecase_factory,
    occupancy_type_query_usecase_factory,
)
from library.dddpy.core_occupancy_types.usecase.occupancy_type_cmd_schema import (
    CreateOccupancyTypeSchema,
    UpdateOccupancyTypeSchema,
)
from library.dddpy.core_occupancy_types.domain.occupancy_type_entity import OccupancyTypeEntity
from library.dddpy.core_occupancy_types.domain.occupancy_type_exception import (
    OccupancyTypeNotFound,
    OccupancyTypeAlreadyExists,
)
from library.dddpy.core_occupancy_types.domain.occupancy_type_success import OccupancyTypeSuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("OccupancyTypeUseCase")


class OccupancyTypeUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self._cmd: OccupancyTypeCmdUseCase = occupancy_type_cmd_usecase_factory()
        self._query: OccupancyTypeQueryUseCase = occupancy_type_query_usecase_factory()
        logger.info("OccupancyTypeUseCase initialized")

    # ── Create ─────────────────────────────────────────────────────────────

    def create(self, data: CreateOccupancyTypeSchema):
        logger.add_inside_method("create")
        from library.dddpy.core_occupancy_types.domain.occupancy_type_data import (
            CreateOccupancyTypeData,
        )
        cmd_data = CreateOccupancyTypeData(
            code=data.code,
            name=data.name,
            description=data.description,
            scope=data.scope,
            condominium_id=data.condominium_id,
            requires_authorization=data.requires_authorization,
            allows_primary=data.allows_primary,
            is_active=data.is_active,
            sort_order=data.sort_order,
        )
        entity = self._cmd.create(cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=OccupancyTypeSuccessMessage.CREATED,
            data=entity.to_dict(),
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        entity = self._query.get_by_id(id)
        if not entity:
            raise OccupancyTypeNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=OccupancyTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        entity = self._query.get_by_uuid(uuid)
        if not entity:
            raise OccupancyTypeNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=OccupancyTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateOccupancyTypeSchema):
        logger.add_inside_method("update")
        existing = self._query.get_by_id(id)
        if not existing:
            raise OccupancyTypeNotFound()

        from library.dddpy.core_occupancy_types.domain.occupancy_type_data import (
            UpdateOccupancyTypeData,
        )
        cmd_data = UpdateOccupancyTypeData(
            name=data.name,
            description=data.description,
            scope=data.scope,
            condominium_id=data.condominium_id,
            requires_authorization=data.requires_authorization,
            allows_primary=data.allows_primary,
            is_active=data.is_active,
            sort_order=data.sort_order,
        )
        entity = self._cmd.update(id, cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=OccupancyTypeSuccessMessage.UPDATED,
            data=entity.to_dict(),
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def soft_delete(self, id: int):
        logger.add_inside_method("soft_delete")
        existing = self._query.get_by_id(id)
        if not existing:
            raise OccupancyTypeNotFound()
        self._cmd.soft_delete(id)
        fresh = self._query._get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=OccupancyTypeSuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        existing = self._query._get_by_id_any_status(id)
        if not existing:
            raise OccupancyTypeNotFound()
        self._cmd.restore(id)
        entity = self._query.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=OccupancyTypeSuccessMessage.RESTORED,
            data=entity.to_dict(),
        )

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        existing = self._query.get_by_id(id)
        if not existing:
            raise OccupancyTypeNotFound()
        self._cmd.hard_delete(id)
        return ResponseSuccessSchema(
            success=True,
            message="Occupancy type hard deleted successfully",
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
            message=OccupancyTypeSuccessMessage.LISTED,
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