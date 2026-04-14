from typing import Optional

from library.dddpy.core_unities.usecase.unity_cmd_usecase import UnityCmdUseCase
from library.dddpy.core_unities.usecase.unity_query_usecase import UnityQueryUseCase
from library.dddpy.core_unities.usecase.unity_factory import (
    unity_cmd_usecase_factory,
    unity_query_usecase_factory,
)
from library.dddpy.core_unities.usecase.unity_cmd_schema import (
    CreateUnitySchema,
    UpdateUnitySchema,
)
from library.dddpy.core_unities.domain.unity_exception import (
    UnityNotFound,
    RepeatedUnityUnitNumber,
    RepeatedUnityCode,
    UnityHasActiveResidents,
)
from library.dddpy.core_unities.domain.unity_success import UnitySuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnityUseCase")


def _enrich_unity_with_type(unity_dict: dict) -> dict:
    """
    Fetch unity type data and attach it to a unity dict.

    Adds:
      - unity_type_code:   code of the assigned type (or None)
      - unity_type_name:  name of the assigned type (or None)
    """
    type_id = unity_dict.get("unity_type_id")
    if type_id is None:
        unity_dict["unity_type_code"] = None
        unity_dict["unity_type_name"] = None
        return unity_dict

    try:
        from library.dddpy.core_unities_types.usecase.unity_type_usecase import (
            UnityTypeUseCase,
        )
        response = UnityTypeUseCase().get_by_id(type_id)
        type_data = response.data
        unity_dict["unity_type_code"] = type_data["code"]
        unity_dict["unity_type_name"] = type_data["name"]
    except Exception:
        unity_dict["unity_type_code"] = None
        unity_dict["unity_type_name"] = None

    return unity_dict


class UnityUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self.unity_cmd_usecase: UnityCmdUseCase = unity_cmd_usecase_factory()
        self.unity_query_usecase: UnityQueryUseCase = unity_query_usecase_factory()
        logger.info("UnityUseCase initialized")

    # ── Create ─────────────────────────────────────────────────────────────

    def create(self, data: CreateUnitySchema):
        logger.add_inside_method("create")
        logger.info(f"Creating unity with data: {data}")

        # Check duplicate unit_number in same building
        existing = self.unity_query_usecase.get_by_unit_number_in_building(
            data.building_id, data.unit_number
        )
        if existing:
            logger.warning(
                f"Unit number already exists: {data.unit_number} "
                f"in building_id={data.building_id}"
            )
            raise RepeatedUnityUnitNumber()

        new_unity = self.unity_cmd_usecase.create(data)
        unity_dict = new_unity.to_dict()
        _enrich_unity_with_type(unity_dict)
        return ResponseSuccessSchema(
            success=True,
            message=UnitySuccessMessage.CREATED,
            data=unity_dict,
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        unity = self.unity_query_usecase.get_by_id(id)
        if not unity:
            logger.warning(f"Unity not found by id={id}")
            raise UnityNotFound()
        unity_dict = unity.to_dict()
        _enrich_unity_with_type(unity_dict)
        return ResponseSuccessSchema(
            success=True,
            message=UnitySuccessMessage.RETRIEVED,
            data=unity_dict,
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        unity = self.unity_query_usecase.get_by_uuid(uuid)
        if not unity:
            logger.warning(f"Unity not found by uuid={uuid}")
            raise UnityNotFound()
        unity_dict = unity.to_dict()
        _enrich_unity_with_type(unity_dict)
        return ResponseSuccessSchema(
            success=True,
            message=UnitySuccessMessage.RETRIEVED,
            data=unity_dict,
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateUnitySchema):
        logger.add_inside_method("update")
        logger.info(f"Updating unity id={id} with data: {data}")

        existing = self.unity_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unity not found for update id={id}")
            raise UnityNotFound()

        # If unit_number is being changed, check it's not duplicate in same building
        if data.unit_number is not None and data.unit_number != existing.unit_number:
            duplicate = self.unity_query_usecase.get_by_unit_number_in_building(
                existing.building_id, data.unit_number
            )
            if duplicate and duplicate.id != id:
                logger.warning(
                    f"Unit number already exists: {data.unit_number} "
                    f"in building_id={existing.building_id}"
                )
                raise RepeatedUnityUnitNumber()

        # If code is being changed, check it's not duplicate in same building
        if data.code is not None and data.code != existing.code:
            duplicate = self.unity_query_usecase.get_by_code_in_building(
                existing.building_id, data.code
            )
            if duplicate and duplicate.id != id:
                logger.warning(
                    f"Code already exists: {data.code} "
                    f"in building_id={existing.building_id}"
                )
                raise RepeatedUnityCode()

        updated_unity = self.unity_cmd_usecase.update(id, data)
        unity_dict = updated_unity.to_dict()
        _enrich_unity_with_type(unity_dict)
        return ResponseSuccessSchema(
            success=True,
            message=UnitySuccessMessage.UPDATED,
            data=unity_dict,
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def delete(self, id: int):
        logger.add_inside_method("delete")
        logger.info(f"Soft deleting unity id={id}")

        existing = self.unity_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unity not found for delete id={id}")
            raise UnityNotFound()

        deleted = self.unity_cmd_usecase.soft_delete(id)
        if not deleted:
            raise UnityNotFound()

        # Re-fetch to return actual persisted state (ignore soft-delete filter)
        fresh = self.unity_query_usecase.get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=UnitySuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        logger.info(f"Restoring unity id={id}")

        # Verify it exists first (use any-status since entity may be soft-deleted)
        existing = self.unity_query_usecase.get_by_id_any_status(id)
        if not existing:
            logger.warning(f"Unity not found for restore id={id}")
            raise UnityNotFound()

        restored = self.unity_cmd_usecase.restore(id)
        if not restored:
            logger.warning(f"Failed to restore unity id={id}")
            raise UnityNotFound()

        # Re-fetch to return actual persisted state
        refreshed = self.unity_query_usecase.get_by_id_any_status(id)
        unity_dict = refreshed.to_dict()
        _enrich_unity_with_type(unity_dict)
        return ResponseSuccessSchema(
            success=True,
            message=UnitySuccessMessage.RESTORED,
            data=unity_dict,
        )

    # ── List ───────────────────────────────────────────────────────────────

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        building_id: Optional[int] = None,
        unity_type_id: Optional[int] = None,
        occupancy_status: Optional[str] = None,
        status: Optional[int] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_all")
        if limit > 500:
            limit = 500
        unities, total = self.unity_query_usecase.list_all(
            skip=skip,
            limit=limit,
            building_id=building_id,
            unity_type_id=unity_type_id,
            occupancy_status=occupancy_status,
            status=status,
            include_deleted=include_deleted,
        )
        items = [_enrich_unity_with_type(u.to_dict()) for u in unities]
        return ResponseSuccessSchema(
            success=True,
            message=UnitySuccessMessage.LISTED,
            data={
                "items": items,
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters": {
                    "building_id": building_id,
                    "unity_type_id": unity_type_id,
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
        unities, total = self.unity_query_usecase.list_by_building(
            building_id=building_id,
            skip=skip,
            limit=limit,
            occupancy_status=occupancy_status,
            status=status,
            include_deleted=include_deleted,
        )
        items = [_enrich_unity_with_type(u.to_dict()) for u in unities]
        return ResponseSuccessSchema(
            success=True,
            message=UnitySuccessMessage.LIST_BY_BUILDING,
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
        logger.info(f"Attempting hard delete for unity id={id}")

        existing = self.unity_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unity not found for hard delete id={id}")
            raise UnityNotFound()

        active_residents = self.unity_query_usecase.count_active_residents(id)
        if active_residents > 0:
            logger.warning(
                f"Unity id={id} has {active_residents} active residents — hard delete blocked"
            )
            raise UnityHasActiveResidents(id)

        deleted = self.unity_cmd_usecase.hard_delete(id)
        if not deleted:
            raise UnityNotFound()

        return ResponseSuccessSchema(
            success=True,
            message=UnitySuccessMessage.HARD_DELETED,
            data={"id": id},
        )
