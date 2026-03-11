from typing import Optional, List
from chalicelib.dddpy.core_unitys.domain.unitys import Unitys
from chalicelib.dddpy.core_unitys.domain.unitys_repository import UnitysQueryRepository
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("unitys_query_usecase")


class UnitysQueryUseCase:
    def __init__(self, repository: UnitysQueryRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[Unitys]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting unity by id: {id}")
        return self.repository.get_by_id(id)
    
    def get_by_code(self, code: str) -> Optional[Unitys]:
        logging.add_inside_method("get_by_code")
        logging.info(f"Getting unity by code: {code}")
        return self.repository.get_by_code(code)
    
    def get_all(self) -> List[Unitys]:
        logging.add_inside_method("get_all")
        logging.info("Getting all unitys")
        return self.repository.get_all()
    
    def get_by_building_id(self, building_id: int) -> List[Unitys]:
        logging.add_inside_method("get_by_building_id")
        logging.info(f"Getting unitys by building_id: {building_id}")
        return self.repository.get_by_building_id(building_id)
