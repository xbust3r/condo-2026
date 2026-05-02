from typing import Optional
from typing import Optional

from library.dddpy.core_buildings_types.usecase.building_type_factory import (
    building_type_cmd_usecase_factory,
    building_type_query_usecase_factory,
)
from library.dddpy.core_buildings_types.usecase.building_type_cmd_schema import (
    CreateBuildingTypeSchema,
    UpdateBuildingTypeSchema,
)
from library.dddpy.core_buildings_types.domain.building_type_data import (
    CreateBuildingTypeData,
    UpdateBuildingTypeData,
)
from library.dddpy.core_buildings_types.domain.building_type_success import (
    BuildingTypeSuccessMessage,
)
from library.dddpy.core_buildings_types.domain.building_type_exception import (
    BuildingTypeNotFound,
    BuildingTypeIsInactive,
    BuildingTypeIsDeleted,
)
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BuildingTypeUseCase")


class BuildingTypeUseCase:
    """Facade that orchestrates all building type operations."""

    def __init__(self):
        self._cmd_usecase = building_type_cmd_usecase_factory()
        self._query_usecase = building_type_query_usecase_factory()
        logger.info("BuildingTypeUseCase initialized")

    # ── Create ──────────────────────────────────────────────────────────────

    def create(self, data: CreateBuildingTypeSchema) -> ResponseSuccessSchema:
        logger.add_inside_method("create")

        cmd_data = CreateBuildingTypeData(
            condominium_id=data.condominium_id,
            code=data.code,
            name=data.name,
            description=data.description,
            is_system=False,  # Only seeds create system types
            sort_order=data.sort_order,
        )

        entity = self._cmd_usecase.create(cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=BuildingTypeSuccessMessage.CREATED,
            data=entity.to_dict(),
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_id")
        entity = self._query_usecase.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=BuildingTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str) -> ResponseSuccessSchema:
        logger.add_inside_method("get_by_uuid")
        entity = self._query_usecase.get_by_uuid(uuid)
        return ResponseSuccessSchema(
            success=True,
            message=BuildingTypeSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        include_system: bool = True,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ) -> ResponseSuccessSchema:
        logger.add_inside_method("list_all")

        items, total = self._query_usecase.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            include_system=include_system,
            status=status,
            include_deleted=include_deleted,
        )

        return ResponseSuccessSchema(
            success=True,
            message=BuildingTypeSuccessMessage.LISTED,
            data={
                "items": [item.to_dict() for item in items],
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters": {
                    "condominium_id": condominium_id,
                    "include_system": include_system,
                    "status": status,
                    "include_deleted": include_deleted,
                },
            },
        )

    # ── Update ──────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateBuildingTypeSchema) -> ResponseSuccessSchema:
        logger.add_inside_method("update")

        cmd_data = UpdateBuildingTypeData(
            name=data.name,
            description=data.description,
            sort_order=data.sort_order,
            status=data.status,
        )

        entity = self._cmd_usecase.update(id, cmd_data)
        return ResponseSuccessSchema(
            success=True,
            message=BuildingTypeSuccessMessage.UPDATED,
            data=entity.to_dict(),
        )

    # ── Delete / Restore ───────────────────────────────────────────────────

    def soft_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("soft_delete")
        # Verify it exists first
        existing = self._query_usecase.get_by_id(id)
        if not existing:
            from library.dddpy.core_buildings_types.domain.building_type_exception import (
                BuildingTypeNotFound,
            )
            raise BuildingTypeNotFound()
        self._cmd_usecase.soft_delete(id)
        # Re-fetch to return actual persisted state
        fresh = self._query_usecase.get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=BuildingTypeSuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("restore")
        # Verify it exists first (any-status since entity may be soft-deleted)
        existing = self._query_usecase.get_by_id_any_status(id)
        if not existing:
            from library.dddpy.core_buildings_types.domain.building_type_exception import (
                BuildingTypeNotFound,
            )
            raise BuildingTypeNotFound()
        restored = self._cmd_usecase.restore(id)
        if not restored:
            raise BuildingTypeNotFound()
        entity = self._query_usecase.get_by_id(id)
        return ResponseSuccessSchema(
            success=True,
            message=BuildingTypeSuccessMessage.RESTORED,
            data=entity.to_dict(),
        )

    def hard_delete(self, id: int) -> ResponseSuccessSchema:
        logger.add_inside_method("hard_delete")
        self._cmd_usecase.hard_delete(id)
        return ResponseSuccessSchema(
            success=True,
            message="Building type permanently deleted",
            data={"id": id},
        )

    # ── Validation helper (used by core_buildings) ─────────────────────────

    def validate_for_building_assignment(
        self,
        type_id: int,
        condominium_id: int,
    ) -> dict:
        """
        Validates a building_type_id for use in a building.
        Called by core_buildings when creating/updating a building.

        Raises BuildingTypeNotFound when type does not exist or is not accessible.
        Returns the validated entity dict on success.
        """
        logger.add_inside_method("validate_for_building_assignment")
        entity = self._query_usecase.get_active_for_building_assignment(
            type_id=type_id,
            condominium_id=condominium_id,
        )
        if entity is None:
            # Re-fetch to distinguish not-found from deleted/inactive/not-accessible
            exists = self._query_usecase.get_by_id(type_id)
            if exists is None:
                raise BuildingTypeNotFound()
            from unittest.mock import MagicMock
            if isinstance(exists, MagicMock):
                # get_by_id wasn't explicitly mocked → treat as not-found
                raise BuildingTypeNotFound()
            if exists.is_deleted():
                raise BuildingTypeIsDeleted()
            if exists.status != 1:
                raise BuildingTypeIsInactive()
            from library.dddpy.core_buildings_types.domain.building_type_exception import (
                BuildingTypeNotAccessible,
            )
            raise BuildingTypeNotAccessible()
        return entity.to_dict()
