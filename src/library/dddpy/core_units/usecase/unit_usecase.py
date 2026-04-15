from typing import Optional

from library.dddpy.core_units.usecase.unit_cmd_usecase import UnitCmdUseCase
from library.dddpy.core_units.usecase.unit_query_usecase import UnitQueryUseCase
from library.dddpy.core_units.usecase.unit_factory import (
    unit_cmd_usecase_factory,
    unit_query_usecase_factory,
)
from library.dddpy.core_units.usecase.unit_cmd_schema import (
    CreateUnitSchema,
    UpdateUnitSchema,
)
from library.dddpy.core_units.domain.unit_exception import (
    UnitNotFound,
    RepeatedUnitUnitNumber,
    RepeatedUnitCode,
    UnitHasActiveResidents,
)
from library.dddpy.core_units.domain.unit_success import UnitSuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitUseCase")


def _enrich_unit_with_type(unit_dict: dict) -> dict:
    """
    Fetch unit type data and attach it to a unit dict.

    Adds:
      - unit_type_code:   code of the assigned type (or None)
      - unit_type_name:  name of the assigned type (or None)
    """
    type_id = unit_dict.get("unit_type_id")
    if type_id is None:
        unit_dict["unit_type_code"] = None
        unit_dict["unit_type_name"] = None
        return unit_dict

    try:
        from library.dddpy.core_unit_types.usecase.unit_type_usecase import (
            UnitTypeUseCase,
        )
        response = UnitTypeUseCase().get_by_id(type_id)
        type_data = response.data
        unit_dict["unit_type_code"] = type_data["code"]
        unit_dict["unit_type_name"] = type_data["name"]
    except Exception:
        unit_dict["unit_type_code"] = None
        unit_dict["unit_type_name"] = None

    return unit_dict


class UnitUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self.unit_cmd_usecase: UnitCmdUseCase = unit_cmd_usecase_factory()
        self.unit_query_usecase: UnitQueryUseCase = unit_query_usecase_factory()
        logger.info("UnitUseCase initialized")

    # ── Create ─────────────────────────────────────────────────────────────

    def create(self, data: CreateUnitSchema):
        logger.add_inside_method("create")
        logger.info(f"Creating unit with data: {data}")

        existing = self.unit_query_usecase.get_by_unit_number_in_building(
            data.building_id, data.unit_number
        )
        if existing:
            logger.warning(
                f"Unit number already exists: {data.unit_number} "
                f"in building_id={data.building_id}"
            )
            raise RepeatedUnitUnitNumber()

        new_unit = self.unit_cmd_usecase.create(data)
        unit_dict = new_unit.to_dict()
        _enrich_unit_with_type(unit_dict)
        return ResponseSuccessSchema(
            success=True,
            message=UnitSuccessMessage.CREATED,
            data=unit_dict,
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        unit = self.unit_query_usecase.get_by_id(id)
        if not unit:
            logger.warning(f"Unit not found by id={id}")
            raise UnitNotFound()
        unit_dict = unit.to_dict()
        _enrich_unit_with_type(unit_dict)
        return ResponseSuccessSchema(
            success=True,
            message=UnitSuccessMessage.RETRIEVED,
            data=unit_dict,
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        unit = self.unit_query_usecase.get_by_uuid(uuid)
        if not unit:
            logger.warning(f"Unit not found by uuid={uuid}")
            raise UnitNotFound()
        unit_dict = unit.to_dict()
        _enrich_unit_with_type(unit_dict)
        return ResponseSuccessSchema(
            success=True,
            message=UnitSuccessMessage.RETRIEVED,
            data=unit_dict,
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateUnitSchema):
        logger.add_inside_method("update")
        logger.info(f"Updating unit id={id} with data: {data}")

        existing = self.unit_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unit not found for update id={id}")
            raise UnitNotFound()

        if data.unit_number is not None and data.unit_number != existing.unit_number:
            duplicate = self.unit_query_usecase.get_by_unit_number_in_building(
                existing.building_id, data.unit_number
            )
            if duplicate and duplicate.id != id:
                logger.warning(
                    f"Unit number already exists: {data.unit_number} "
                    f"in building_id={existing.building_id}"
                )
                raise RepeatedUnitUnitNumber()

        if data.code is not None and data.code != existing.code:
            duplicate = self.unit_query_usecase.get_by_code_in_building(
                existing.building_id, data.code
            )
            if duplicate and duplicate.id != id:
                logger.warning(
                    f"Code already exists: {data.code} "
                    f"in building_id={existing.building_id}"
                )
                raise RepeatedUnitCode()

        updated_unit = self.unit_cmd_usecase.update(id, data)
        unit_dict = updated_unit.to_dict()
        _enrich_unit_with_type(unit_dict)
        return ResponseSuccessSchema(
            success=True,
            message=UnitSuccessMessage.UPDATED,
            data=unit_dict,
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def delete(self, id: int):
        logger.add_inside_method("delete")
        logger.info(f"Soft deleting unit id={id}")

        existing = self.unit_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unit not found for delete id={id}")
            raise UnitNotFound()

        deleted = self.unit_cmd_usecase.soft_delete(id)
        if not deleted:
            raise UnitNotFound()

        fresh = self.unit_query_usecase._get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=UnitSuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        logger.info(f"Restoring unit id={id}")

        existing = self.unit_query_usecase._get_by_id_any_status(id)
        if not existing:
            logger.warning(f"Unit not found for restore id={id}")
            raise UnitNotFound()

        restored = self.unit_cmd_usecase.restore(id)
        if not restored:
            logger.warning(f"Failed to restore unit id={id}")
            raise UnitNotFound()

        refreshed = self.unit_query_usecase._get_by_id_any_status(id)
        unit_dict = refreshed.to_dict()
        _enrich_unit_with_type(unit_dict)
        return ResponseSuccessSchema(
            success=True,
            message=UnitSuccessMessage.RESTORED,
            data=unit_dict,
        )

    # ── List ───────────────────────────────────────────────────────────────

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        building_id: Optional[int] = None,
        unit_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_all")
        if limit > 500:
            limit = 500
        units, total = self.unit_query_usecase.list_all(
            skip=skip,
            limit=limit,
            building_id=building_id,
            unit_type_id=unit_type_id,
            occupancy_status=occupancy_status,
            status=status,
            include_deleted=include_deleted,
        )
        items = [_enrich_unit_with_type(u.to_dict()) for u in units]
        return ResponseSuccessSchema(
            success=True,
            message=UnitSuccessMessage.LISTED,
            data={
                "items": items,
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters": {
                    "building_id": building_id,
                    "unit_type_id": unit_type_id,
                    "occupancy_status": occupancy_status,
                    "status": status,
                    "include_deleted": include_deleted,
                },
            },
        )

    def list_by_building(
        self,
        building_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_by_building")
        if limit > 500:
            limit = 500
        units, total = self.unit_query_usecase.list_by_building(
            building_id=building_id,
            skip=skip,
            limit=limit,
            occupancy_status=occupancy_status,
            status=status,
            include_deleted=include_deleted,
        )
        items = [_enrich_unit_with_type(u.to_dict()) for u in units]
        return ResponseSuccessSchema(
            success=True,
            message=UnitSuccessMessage.LIST_BY_BUILDING,
            data={
                "items": items,
                "total": total,
                "building_id": building_id,
                "skip": skip,
                "limit": limit,
            },
        )

    # ── Hard delete ────────────────────────────────────────────────────────

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        logger.info(f"Attempting hard delete for unit id={id}")

        existing = self.unit_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unit not found for hard delete id={id}")
            raise UnitNotFound()

        active_residents = self.unit_query_usecase.count_active_residents(id)
        if active_residents > 0:
            logger.warning(
                f"Unit id={id} has {active_residents} active residents — hard delete blocked"
            )
            raise UnitHasActiveResidents(id)

        deleted = self.unit_cmd_usecase.hard_delete(id)
        if not deleted:
            raise UnitNotFound()

        return ResponseSuccessSchema(
            success=True,
            message=UnitSuccessMessage.HARD_DELETED,
            data={"id": id},
        )