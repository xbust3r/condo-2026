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


class BuildingUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self.building_cmd_usecase: BuildingCmdUseCase = building_cmd_usecase_factory()
        self.building_query_usecase: BuildingQueryUseCase = building_query_usecase_factory()
        logger.info("BuildingUseCase initialized")

    def create(self, data: CreateBuildingSchema):
        logger.add_inside_method("create")
        logger.info(f"Creating building with data: {data}")

        # Check duplicate code within condominium
        existing = self.building_query_usecase.get_by_code_in_condominium(
            data.condominium_id, data.code
        )
        if existing:
            logger.warning(f"Building code already exists: code={data.code} in condominium_id={data.condominium_id}")
            raise RepeatedBuildingCode()

        new_building = self.building_cmd_usecase.create(data)
        success = ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.CREATED,
            data=new_building.to_dict(),
        )
        logger.info(f"{success.message}: {new_building.id}")
        return success

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        building = self.building_query_usecase.get_by_id(id)
        if not building:
            logger.warning(f"Building not found by id={id}")
            raise BuildingNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.RETRIEVED,
            data=building.to_dict(),
        )
        logger.info(f"{success.message} by id={id}")
        return success

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        building = self.building_query_usecase.get_by_uuid(uuid)
        if not building:
            logger.warning(f"Building not found by uuid={uuid}")
            raise BuildingNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.RETRIEVED,
            data=building.to_dict(),
        )
        logger.info(f"{success.message} by uuid={uuid}")
        return success

    def update(self, id: int, data: UpdateBuildingSchema):
        logger.add_inside_method("update")
        logger.info(f"Updating building id={id} with data: {data}")

        # Verify exists
        existing = self.building_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Building not found for update id={id}")
            raise BuildingNotFound()

        updated_building = self.building_cmd_usecase.update(id, data)
        success = ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.UPDATED,
            data=updated_building.to_dict(),
        )
        logger.info(f"{success.message}: id={id}")
        return success

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

        success = ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.DELETED,
            data={"id": id},
        )
        logger.info(f"{success.message} for id={id}")
        return success

    def restore(self, id: int):
        logger.add_inside_method("restore")
        logger.info(f"Restoring building id={id}")

        restored = self.building_cmd_usecase.restore(id)
        if not restored:
            logger.warning(f"Failed to restore building id={id}")
            raise BuildingNotFound()

        building = self.building_query_usecase.get_by_id(id)
        success = ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.RESTORED,
            data=building.to_dict(),
        )
        logger.info(f"{success.message} for id={id}")
        return success

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
        success = ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.LISTED,
            data={
                "items": [building.to_dict() for building in buildings],
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
        logger.info(f"{success.message}: {len(buildings)}/{total} buildings")
        return success

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
        success = ResponseSuccessSchema(
            success=True,
            message=BuildingSuccessMessage.LIST_BY_CONDOMINIUM,
            data={
                "items": [building.to_dict() for building in buildings],
                "total": total,
                "condominium_id": condominium_id,
                "skip": skip,
                "limit": limit,
            },
        )
        logger.info(f"{success.message}: {len(buildings)}/{total} buildings for condominium_id={condominium_id}")
        return success

    def hard_delete(self, id: int):
        logger.add_inside_method("hard_delete")
        logger.info(f"Attempting hard delete for building id={id}")

        # Verify exists
        existing = self.building_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Building not found for hard delete id={id}")
            raise BuildingNotFound()

        # Check for active units
        active_units = self.building_query_usecase.count_active_units(id)
        if active_units > 0:
            logger.warning(f"Building id={id} has {active_units} active units — hard delete blocked")
            raise BuildingHasActiveUnits(id)

        deleted = self.building_cmd_usecase.hard_delete(id)
        if not deleted:
            logger.warning(f"Failed to hard delete building id={id}")
            raise BuildingNotFound()

        success = ResponseSuccessSchema(
            success=True,
            message="Building permanently deleted",
            data={"id": id},
        )
        logger.info(f"Hard delete completed for id={id}")
        return success