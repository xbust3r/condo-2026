from typing import Optional, List
from chalicelib.dddpy.core_buildings.usecase.buildings_factory import (
    buildings_cmd_usecase_factory,
    buildings_query_usecase_factory,
)
from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
from chalicelib.dddpy.core_buildings.domain.buildings_success import SuccessMessages
from chalicelib.dddpy.core_buildings.domain.buildings_exception import BuildingNotFoundException
from chalicelib.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("buildings_usecase")


class BuildingsUseCase:
    def __init__(self):
        logging.add_inside_method("__init__")
        self.cmd = buildings_cmd_usecase_factory()
        self.query = buildings_query_usecase_factory()
        logging.info("BuildingsUseCase initialized")
    
    def create(self, data) -> ResponseSuccessSchema:
        logging.add_inside_method("create")
        new_building = self.cmd.create(data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.BUILDING_CREATED,
            data=new_building.to_dict()
        )
    
    def update(self, id: int, data) -> ResponseSuccessSchema:
        logging.add_inside_method("update")
        updated_building = self.cmd.update(id, data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.BUILDING_UPDATED,
            data=updated_building.to_dict()
        )
    
    def delete(self, id: int) -> ResponseSuccessSchema:
        logging.add_inside_method("delete")
        result = self.cmd.delete(id)
        return ResponseSuccessSchema(
            success=result,
            message=SuccessMessages.BUILDING_DELETED,
            data={"deleted": result}
        )
    
    def get_by_id(self, id: int) -> Buildings:
        logging.add_inside_method("get_by_id")
        building = self.query.get_by_id(id)
        if not building:
            raise BuildingNotFoundException()
        return building
    
    def get_by_code(self, code: str) -> Buildings:
        logging.add_inside_method("get_by_code")
        building = self.query.get_by_code(code)
        if not building:
            raise BuildingNotFoundException()
        return building
    
    def get_all(self) -> List[Buildings]:
        logging.add_inside_method("get_all")
        return self.query.get_all()
    
    def get_by_condominium_id(self, condominium_id: int) -> List[Buildings]:
        logging.add_inside_method("get_by_condominium_id")
        return self.query.get_by_condominium_id(condominium_id)
