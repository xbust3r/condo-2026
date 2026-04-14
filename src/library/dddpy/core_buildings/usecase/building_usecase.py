from typing import Optional

from library.dddpy.core_buildings.usecase.building_cmd_usecase import BuildingCmdUseCase
from library.dddpy.core_buildings.usecase.building_query_usecase import BuildingQueryUseCase
from library.dddpy.core_buildings.usecase.building_factory import building_cmd_usecase_factory, building_query_usecase_factory
from library.dddpy.core_buildings.usecase.building_cmd_schema import CreateBuildingSchema, UpdateBuildingSchema
from library.dddpy.core_buildings.domain.building_exception import (
    BuildingNotFound,
    RepeatedBuildingCode,
    BuildingHasActiveUnits,
)
from library.dddpy.core_buildings.domain.building_success import BuildingSuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BuildingUseCase")


def _enrich_building_with_type(building_dict: dict) -> dict:
    """
    Fetch building type data and attach it to a building dict.

    Adds:
      - building_type_code:   code of the assigned type (or None)
      - building_type_name:   name of the assigned type (or None)
      - building_type_scope:  'global', 'custom', or None if no type assigned

    Safe to call even when building_type_id is None.
    """
    type_id = building_dict.get("building_type_id")
    if type_id is None:
        building_dict["building_type_code"] = None
        building_dict["building_type_name"] = None
        building_dict["building_type_scope"] = None
        return building_dict

    try:
        from library.dddpy.core_buildings_types.usecase.building_type_usecase import (
            BuildingTypeUseCase,
        )
        response = BuildingTypeUseCase().get_by_id(type_id)
        type_data = response.data  # ResponseSuccessSchema.data is the entity dict
        building_dict["building_type_code"] = type_data["code"]
        building_dict["building_type_name"] = type_data["name"]
        building_dict["building_type_scope"] = type_data["scope"]
    except Exception:
        # If type lookup fails (e.g. type was deleted), leave fields null
        building_dict["building_type_code"] = None
        building_dict["building_type_name"] = None
        building_dict["building_type_scope"] = None

    return building_dict


class BuildingUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self.building_cmd_usecase: BuildingCmdUseCase = building_cmd_usecase_factory()
        self.building_query_usecase: BuildingQueryUseCase = building_query_usecase_factory()
        logger.info("BuildingUseCase initialized")

    # ── Create ─────────────────────────────────────────────────────────────

    def create(self, data: CreateBuildingSchema):
        logger.add_inside_method("create")
        logger.info(f"Creating building with data: {data}")

        existing = self.building_query_usecase.get_by_code_in_condominium(
            data.condominium_id, data.code
        )
        if existing:
            logger.warning(
                f"Building code already exists: code={data.code} "
                f"in condominium_id={data.condominium_id}"
            )
            raise RepeatedBuildingCode()

        new_building = self.building_cmd_usecase.create(data)
        building_dict = new_building.to_dict()
        _enrich_building_with_type(building_dict)
        return ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.CREATED,
            data=building_dict,
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        building = self.building_query_usecase.get_by_id(id)
        if not building:
            logger.warning(f"Building not found by id={id}")
            raise BuildingNotFound()
        building_dict = building.to_dict()
        _enrich_building_with_type(building_dict)
        return ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.RETRIEVED,
            data=building_dict,
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        building = self.building_query_usecase.get_by_uuid(uuid)
        if not building:
            logger.warning(f"Building not found by uuid={uuid}")
            raise BuildingNotFound()
        building_dict = building.to_dict()
        _enrich_building_with_type(building_dict)
        return ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.RETRIEVED,
            data=building_dict,
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateBuildingSchema):
        logger.add_inside_method("update")
        logger.info(f"Updating building id={id} with data: {data}")

        existing = self.building_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Building not found for update id={id}")
            raise BuildingNotFound()

        updated_building = self.building_cmd_usecase.update(id, data)
        building_dict = updated_building.to_dict()
        _enrich_building_with_type(building_dict)
        return ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.UPDATED,
            data=building_dict,
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def delete(self, id: int):
        logger.add_inside_method("delete")
        logger.info(f"Soft deleting building id={id}")

        existing = self.building_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Building not found for delete id={id}")
            raise BuildingNotFound()

        deleted = self.building_cmd_usecase.soft_delete(id)
        if not deleted:
            logger.warning(f"Failed to soft delete building id={id}")
            raise BuildingNotFound()

        # Re-fetch to return actual persisted state (ignore soft-delete filter)
        fresh = self.building_query_usecase.get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        logger.info(f"Restoring building id={id}")

        # Verify it exists first (use any-status since entity may be soft-deleted)
        existing = self.building_query_usecase.get_by_id_any_status(id)
        if not existing:
            logger.warning(f"Building not found for restore id={id}")
            raise BuildingNotFound()

        restored = self.building_cmd_usecase.restore(id)
        if not restored:
            logger.warning(f"Failed to restore building id={id}")
            raise BuildingNotFound()

        # Re-fetch to return actual persisted state
        refreshed = self.building_query_usecase.get_by_id_any_status(id)
        building_dict = refreshed.to_dict()
        _enrich_building_with_type(building_dict)
        return ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.RESTORED,
            data=building_dict,
        )

    # ── List ───────────────────────────────────────────────────────────────

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        building_type_id: Optional[int] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_all")
        buildings, total = self.building_query_usecase.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            building_type_id=building_type_id,
            status=status,
            include_deleted=include_deleted,
        )
        items = [_enrich_building_with_type(b.to_dict()) for b in buildings]
        return ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.LISTED,
            data={
                "items": items,
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters": {
                    "condominium_id": condominium_id,
                    "building_type_id": building_type_id,
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
        status: Optional[int] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_by_condominium")
        buildings, total = self.building_query_usecase.list_by_condominium(
            condominium_id=condominium_id,
            skip=skip,
            limit=limit,
            status=status,
            include_deleted=include_deleted,
        )
        items = [_enrich_building_with_type(b.to_dict()) for b in buildings]
        return ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.LIST_BY_CONDOMINIUM,
            data={
                "items": items,
                "total": total,
                "condominium_id": condominium_id,
                "skip": skip,
                "limit": limit,
            },
        )

    # ── Hard delete ────────────────────────────────────────────────────────

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        logger.info(f"Attempting hard delete for building id={id}")

        existing = self.building_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Building not found for hard delete id={id}")
            raise BuildingNotFound()

        active_units = self.building_query_usecase.count_active_units(id)
        if active_units > 0:
            logger.warning(
                f"Building id={id} has {active_units} active units — hard delete blocked"
            )
            raise BuildingHasActiveUnits(id)

        deleted = self.building_cmd_usecase.hard_delete(id)
        if not deleted:
            logger.warning(f"Failed to hard delete building id={id}")
            raise BuildingNotFound()

        return ResponseSuccessSchema(
            success=True,
            message="Building permanently deleted",
            data={"id": id},
        )
