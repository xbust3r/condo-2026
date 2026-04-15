from typing import Optional

from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_cmd_usecase import UnitOccupancyCmdUseCase
from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_query_usecase import UnitOccupancyQueryUseCase
from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_factory import (
    unit_occupancy_cmd_usecase_factory,
    unit_occupancy_query_usecase_factory,
)
from library.dddpy.core_unit_occupancies.usecase.unit_occupancy_cmd_schema import (
    CreateUnitOccupancySchema,
    UpdateUnitOccupancySchema,
)
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_exception import (
    UnitOccupancyNotFound,
    DuplicateOccupancyRecord,
    PrimaryOccupancyConflict,
)
from library.dddpy.core_unit_occupancies.domain.unit_occupancy_success import UnitOccupancySuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOccupancyUseCase")


class UnitOccupancyUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self.unit_occupancy_cmd_usecase: UnitOccupancyCmdUseCase = unit_occupancy_cmd_usecase_factory()
        self.unit_occupancy_query_usecase: UnitOccupancyQueryUseCase = unit_occupancy_query_usecase_factory()
        logger.info("UnitOccupancyUseCase initialized")

    def _enrich_occupancy_with_details(self, occ_dict: dict) -> dict:
        """
        Fetch unit and user data and attach summary fields.
        """
        unit_id = occ_dict.get("unit_id")
        user_id = occ_dict.get("user_id")
        occ_dict["unit_uuid"] = None
        occ_dict["unit_number"] = None
        occ_dict["user_uuid"] = None
        occ_dict["user_full_name"] = None

        if unit_id is not None:
            try:
                from library.dddpy.core_units.usecase.unit_usecase import UnitUseCase
                unit_response = UnitUseCase().get_by_uuid(
                    self.unit_occupancy_query_usecase.repository.get_by_id_any_status(
                        self.unit_occupancy_query_usecase.repository._get_by_id_any_status(
                            unit_id
                        ).id
                    ).uuid
                )
            except Exception:
                pass

        if user_id is not None:
            try:
                from library.dddpy.core_users.usecase.user_usecase import UserUseCase
                user_response = UserUseCase().get_by_id(user_id)
                user_data = user_response.data
                occ_dict["user_full_name"] = user_data.get("full_name")
            except Exception:
                pass

        return occ_dict

    def create(self, data: CreateUnitOccupancySchema):
        logger.add_inside_method("create")
        logger.info(f"Creating unit occupancy with data: {data}")

        existing = self.unit_occupancy_query_usecase.get_active_by_unit_and_user(
            data.unit_id, data.user_id
        )
        if existing:
            logger.warning(
                f"Active occupancy already exists for unit_id={data.unit_id}, "
                f"user_id={data.user_id}"
            )
            raise DuplicateOccupancyRecord()

        if data.is_primary:
            active_count = self.unit_occupancy_query_usecase.count_active_by_unit(data.unit_id)
            if active_count > 0:
                existing_primary = self._get_primary_for_unit(data.unit_id)
                if existing_primary:
                    logger.warning(
                        f"Primary occupancy already exists for unit_id={data.unit_id}"
                    )
                    raise PrimaryOccupancyConflict()

        new_occupancy = self.unit_occupancy_cmd_usecase.create(data)
        occ_dict = new_occupancy.to_dict()
        return ResponseSuccessSchema(
            success=True,
            message=UnitOccupancySuccessMessage.CREATED,
            data=occ_dict,
        )

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        occupancy = self.unit_occupancy_query_usecase.get_by_id(id)
        if not occupancy:
            logger.warning(f"Unit occupancy not found by id={id}")
            raise UnitOccupancyNotFound()
        occ_dict = occupancy.to_dict()
        return ResponseSuccessSchema(
            success=True,
            message=UnitOccupancySuccessMessage.RETRIEVED,
            data=occ_dict,
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        occupancy = self.unit_occupancy_query_usecase.get_by_uuid(uuid)
        if not occupancy:
            logger.warning(f"Unit occupancy not found by uuid={uuid}")
            raise UnitOccupancyNotFound()
        occ_dict = occupancy.to_dict()
        return ResponseSuccessSchema(
            success=True,
            message=UnitOccupancySuccessMessage.RETRIEVED,
            data=occ_dict,
        )

    def update(self, id: int, data: UpdateUnitOccupancySchema):
        logger.add_inside_method("update")
        logger.info(f"Updating unit occupancy id={id} with data: {data}")

        existing = self.unit_occupancy_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unit occupancy not found for update id={id}")
            raise UnitOccupancyNotFound()

        updated_occupancy = self.unit_occupancy_cmd_usecase.update(id, data)
        occ_dict = updated_occupancy.to_dict()
        return ResponseSuccessSchema(
            success=True,
            message=UnitOccupancySuccessMessage.UPDATED,
            data=occ_dict,
        )

    def delete(self, id: int):
        logger.add_inside_method("delete")
        logger.info(f"Soft deleting unit occupancy id={id}")

        existing = self.unit_occupancy_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unit occupancy not found for delete id={id}")
            raise UnitOccupancyNotFound()

        deleted = self.unit_occupancy_cmd_usecase.soft_delete(id)
        if not deleted:
            raise UnitOccupancyNotFound()

        fresh = self.unit_occupancy_query_usecase._get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=UnitOccupancySuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        logger.info(f"Restoring unit occupancy id={id}")

        existing = self.unit_occupancy_query_usecase._get_by_id_any_status(id)
        if not existing:
            logger.warning(f"Unit occupancy not found for restore id={id}")
            raise UnitOccupancyNotFound()

        restored = self.unit_occupancy_cmd_usecase.restore(id)
        if not restored:
            logger.warning(f"Failed to restore unit occupancy id={id}")
            raise UnitOccupancyNotFound()

        refreshed = self.unit_occupancy_query_usecase._get_by_id_any_status(id)
        occ_dict = refreshed.to_dict()
        return ResponseSuccessSchema(
            success=True,
            message=UnitOccupancySuccessMessage.RESTORED,
            data=occ_dict,
        )

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        unit_id: Optional[int] = None,
        user_id: Optional[int] = None,
        occupancy_type: Optional[str] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_all")
        if limit > 500:
            limit = 500
        occupancies, total = self.unit_occupancy_query_usecase.list_all(
            skip=skip,
            limit=limit,
            unit_id=unit_id,
            user_id=user_id,
            occupancy_type=occupancy_type,
            status=status,
            is_primary=is_primary,
            include_deleted=include_deleted,
        )
        items = [o.to_dict() for o in occupancies]
        return ResponseSuccessSchema(
            success=True,
            message=UnitOccupancySuccessMessage.LISTED,
            data={
                "items": items,
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters": {
                    "unit_id": unit_id,
                    "user_id": user_id,
                    "occupancy_type": occupancy_type,
                    "status": status,
                    "is_primary": is_primary,
                    "include_deleted": include_deleted,
                },
            },
        )

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_type: Optional[str] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_by_unit")
        if limit > 500:
            limit = 500
        occupancies, total = self.unit_occupancy_query_usecase.list_by_unit(
            unit_id=unit_id,
            skip=skip,
            limit=limit,
            occupancy_type=occupancy_type,
            status=status,
            is_primary=is_primary,
            include_deleted=include_deleted,
        )
        items = [o.to_dict() for o in occupancies]
        return ResponseSuccessSchema(
            success=True,
            message=UnitOccupancySuccessMessage.LIST_BY_UNIT,
            data={
                "items": items,
                "total": total,
                "unit_id": unit_id,
                "skip": skip,
                "limit": limit,
            },
        )

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        occupancy_type: Optional[str] = None,
        status: Optional[str] = None,
        is_primary: Optional[bool] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_by_user")
        if limit > 500:
            limit = 500
        occupancies, total = self.unit_occupancy_query_usecase.list_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            occupancy_type=occupancy_type,
            status=status,
            is_primary=is_primary,
            include_deleted=include_deleted,
        )
        items = [o.to_dict() for o in occupancies]
        return ResponseSuccessSchema(
            success=True,
            message=UnitOccupancySuccessMessage.LIST_BY_USER,
            data={
                "items": items,
                "total": total,
                "user_id": user_id,
                "skip": skip,
                "limit": limit,
            },
        )

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        logger.info(f"Attempting hard delete for unit occupancy id={id}")

        existing = self.unit_occupancy_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unit occupancy not found for hard delete id={id}")
            raise UnitOccupancyNotFound()

        deleted = self.unit_occupancy_cmd_usecase.hard_delete(id)
        if not deleted:
            raise UnitOccupancyNotFound()

        return ResponseSuccessSchema(
            success=True,
            message=UnitOccupancySuccessMessage.HARD_DELETED,
            data={"id": id},
        )

    def _get_primary_for_unit(self, unit_id: int) -> Optional[UnitOccupancyEntity]:
        """Get the current primary occupancy for a unit, if any."""
        occupancies, _ = self.unit_occupancy_query_usecase.list_by_unit(
            unit_id=unit_id,
            is_primary=True,
            status="active",
            include_deleted=False,
        )
        return occupancies[0] if occupancies else None
