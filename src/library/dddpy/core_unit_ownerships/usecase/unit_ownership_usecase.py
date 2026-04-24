from typing import Optional
from datetime import date

from library.dddpy.core_unit_ownerships.usecase.unit_ownership_cmd_usecase import UnitOwnershipCmdUseCase
from library.dddpy.core_unit_ownerships.usecase.unit_ownership_query_usecase import UnitOwnershipQueryUseCase
from library.dddpy.core_unit_ownerships.usecase.unit_ownership_factory import (
    unit_ownership_cmd_usecase_factory,
    unit_ownership_query_usecase_factory,
)
from library.dddpy.core_unit_ownerships.usecase.unit_ownership_cmd_schema import (
    CreateUnitOwnershipSchema,
    UpdateUnitOwnershipSchema,
)
from library.dddpy.core_unit_ownerships.domain.unit_ownership_exception import (
    UnitOwnershipNotFound,
    DuplicateOwnershipRecord,
    OwnershipPercentageSumExceeded,
)
from library.dddpy.core_unit_ownerships.domain.unit_ownership_success import UnitOwnershipSuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitOwnershipUseCase")


class UnitOwnershipUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self.unit_ownership_cmd_usecase: UnitOwnershipCmdUseCase = unit_ownership_cmd_usecase_factory()
        self.unit_ownership_query_usecase: UnitOwnershipQueryUseCase = unit_ownership_query_usecase_factory()
        logger.info("UnitOwnershipUseCase initialized")

    # ── Create ─────────────────────────────────────────────────────────────

    def create(self, data: CreateUnitOwnershipSchema):
        logger.add_inside_method("create")
        logger.info(f"Creating unit ownership with data: {data}")

        # Duplicate check: same user + unit (covers OWN-02)
        existing = self.unit_ownership_query_usecase.get_active_by_unit_and_user(
            data.unit_id, data.user_id
        )
        if existing:
            logger.warning(
                f"Active ownership already exists for unit_id={data.unit_id} "
                f"and user_id={data.user_id}"
            )
            raise DuplicateOwnershipRecord()

        # OWN-01: validate total ownership percentage ≤ 100
        self._validate_ownership_percentage(
            unit_id=data.unit_id,
            new_percentage=float(data.ownership_percentage),
            exclude_id=None,
        )

        new_ownership = self.unit_ownership_cmd_usecase.create(data)
        return ResponseSuccessSchema(
            success=True,
            message=UnitOwnershipSuccessMessage.CREATED,
            data=new_ownership.to_dict(),
        )

    # ── Read ────────────────────────────────────────────────────────────────

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        ownership = self.unit_ownership_query_usecase.get_by_id(id)
        if not ownership:
            logger.warning(f"Unit ownership not found by id={id}")
            raise UnitOwnershipNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=UnitOwnershipSuccessMessage.RETRIEVED,
            data=ownership.to_dict(),
        )

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        ownership = self.unit_ownership_query_usecase.get_by_uuid(uuid)
        if not ownership:
            logger.warning(f"Unit ownership not found by uuid={uuid}")
            raise UnitOwnershipNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=UnitOwnershipSuccessMessage.RETRIEVED,
            data=ownership.to_dict(),
        )

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, id: int, data: UpdateUnitOwnershipSchema):
        logger.add_inside_method("update")
        logger.info(f"Updating unit ownership id={id} with data: {data}")

        existing = self.unit_ownership_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unit ownership not found for update id={id}")
            raise UnitOwnershipNotFound()

        # OWN-01: if percentage is being changed, re-validate total
        if data.ownership_percentage is not None:
            self._validate_ownership_percentage(
                unit_id=existing.unit_id,
                new_percentage=float(data.ownership_percentage),
                exclude_id=id,
            )

        updated_ownership = self.unit_ownership_cmd_usecase.update(id, data)
        return ResponseSuccessSchema(
            success=True,
            message=UnitOwnershipSuccessMessage.UPDATED,
            data=updated_ownership.to_dict(),
        )

    # ── Delete / Restore ─────────────────────────────────────────────────

    def delete(self, id: int):
        logger.add_inside_method("delete")
        logger.info(f"Soft deleting unit ownership id={id}")

        existing = self.unit_ownership_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Unit ownership not found for delete id={id}")
            raise UnitOwnershipNotFound()

        deleted = self.unit_ownership_cmd_usecase.soft_delete(id)
        if not deleted:
            raise UnitOwnershipNotFound()

        fresh = self.unit_ownership_query_usecase._get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        return ResponseSuccessSchema(
            success=True,
            message=UnitOwnershipSuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )

    def restore(self, id: int):
        logger.add_inside_method("restore")
        logger.info(f"Restoring unit ownership id={id}")

        existing = self.unit_ownership_query_usecase._get_by_id_any_status(id)
        if not existing:
            logger.warning(f"Unit ownership not found for restore id={id}")
            raise UnitOwnershipNotFound()

        restored = self.unit_ownership_cmd_usecase.restore(id)
        if not restored:
            logger.warning(f"Failed to restore unit ownership id={id}")
            raise UnitOwnershipNotFound()

        refreshed = self.unit_ownership_query_usecase._get_by_id_any_status(id)
        return ResponseSuccessSchema(
            success=True,
            message=UnitOwnershipSuccessMessage.RESTORED,
            data=refreshed.to_dict(),
        )

    # ── List ───────────────────────────────────────────────────────────────

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        unit_id: Optional[int] = None,
        user_id: Optional[int] = None,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_all")
        if limit > 500:
            limit = 500
        ownerships, total = self.unit_ownership_query_usecase.list_all(
            skip=skip,
            limit=limit,
            unit_id=unit_id,
            user_id=user_id,
            ownership_type=ownership_type,
            status=status,
            include_deleted=include_deleted,
        )
        items = [o.to_dict() for o in ownerships]
        return ResponseSuccessSchema(
            success=True,
            message=UnitOwnershipSuccessMessage.LISTED,
            data={
                "items": items,
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters": {
                    "unit_id": unit_id,
                    "user_id": user_id,
                    "ownership_type": ownership_type,
                    "status": status,
                    "include_deleted": include_deleted,
                },
            },
        )

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_by_unit")
        if limit > 500:
            limit = 500
        ownerships, total = self.unit_ownership_query_usecase.list_by_unit(
            unit_id=unit_id,
            skip=skip,
            limit=limit,
            ownership_type=ownership_type,
            status=status,
            include_deleted=include_deleted,
        )
        items = [o.to_dict() for o in ownerships]
        return ResponseSuccessSchema(
            success=True,
            message=UnitOwnershipSuccessMessage.LIST_BY_UNIT,
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
        ownership_type: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ):
        logger.add_inside_method("list_by_user")
        if limit > 500:
            limit = 500
        ownerships, total = self.unit_ownership_query_usecase.list_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            ownership_type=ownership_type,
            status=status,
            include_deleted=include_deleted,
        )
        items = [o.to_dict() for o in ownerships]
        return ResponseSuccessSchema(
            success=True,
            message=UnitOwnershipSuccessMessage.LIST_BY_USER,
            data={
                "items": items,
                "total": total,
                "user_id": user_id,
                "skip": skip,
                "limit": limit,
            },
        )

    # ── Internal validators ─────────────────────────────────────────────

    def _validate_ownership_percentage(
        self,
        unit_id: int,
        new_percentage: float,
        exclude_id: Optional[int] = None,
    ) -> None:
        """
        OWN-01: Sum of all active ownership percentages for a unit must not exceed 100%.

        Args:
            unit_id:          Unit to validate
            new_percentage:    Percentage being added/updated
            exclude_id:       Ownership record id to exclude (for updates)
        """
        active_ownerships = self.unit_ownership_cmd_usecase.find_active_by_unit(unit_id)

        current_sum = sum(
            float(o.ownership_percentage)
            for o in active_ownerships
            if exclude_id is None or o.id != exclude_id
        )

        proposed_total = current_sum + new_percentage
        if proposed_total > 100:
            logger.warning(
                f"OWN-01 violation: unit_id={unit_id}, current_sum={current_sum}%, "
                f"new={new_percentage}%, total={proposed_total}% > 100%"
            )
            raise OwnershipPercentageSumExceeded(
                unit_id=unit_id,
                current_sum=current_sum,
                additional=new_percentage,
            )
