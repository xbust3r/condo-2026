from typing import Optional, List
from chalicelib.dddpy.core_buildings_types.usecase.buildings_types_factory import (
    buildings_types_cmd_usecase_factory,
    buildings_types_query_usecase_factory,
)
from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from chalicelib.dddpy.core_buildings_types.domain.buildings_types_success import SuccessMessages
from chalicelib.dddpy.core_buildings_types.domain.buildings_types_exception import BuildingTypeNotFoundException
from chalicelib.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("buildings_types_usecase")


class BuildingsTypesUseCase:
    def __init__(self):
        logging.add_inside_method("__init__")
        self.cmd = buildings_types_cmd_usecase_factory()
        self.query = buildings_types_query_usecase_factory()
        logging.info("BuildingsTypesUseCase initialized")
    
    def create(self, data) -> ResponseSuccessSchema:
        logging.add_inside_method("create")
        new_building_type = self.cmd.create(data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.BUILDING_TYPE_CREATED,
            data=new_building_type.to_dict()
        )
    
    def update(self, id: int, data) -> ResponseSuccessSchema:
        logging.add_inside_method("update")
        updated_building_type = self.cmd.update(id, data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.BUILDING_TYPE_UPDATED,
            data=updated_building_type.to_dict()
        )
    
    def delete(self, id: int) -> ResponseSuccessSchema:
        logging.add_inside_method("delete")
        result = self.cmd.delete(id)
        return ResponseSuccessSchema(
            success=result,
            message=SuccessMessages.BUILDING_TYPE_DELETED,
            data={"deleted": result}
        )
    
    def get_by_id(self, id: int) -> BuildingsTypes:
        logging.add_inside_method("get_by_id")
        building_type = self.query.get_by_id(id)
        if not building_type:
            raise BuildingTypeNotFoundException()
        return building_type
    
    def get_by_code(self, code: str) -> BuildingsTypes:
        logging.add_inside_method("get_by_code")
        building_type = self.query.get_by_code(code)
        if not building_type:
            raise BuildingTypeNotFoundException()
        return building_type
    
    def get_all(self) -> List[BuildingsTypes]:
        logging.add_inside_method("get_all")
        return self.query.get_all()
