from typing import Optional, List
from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
from chalicelib.dddpy.core_buildings.domain.buildings_repository import BuildingsQueryRepository
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("buildings_query_usecase")


class BuildingsQueryUseCase:
    def __init__(self, repository: BuildingsQueryRepository):
        logging.add_inside_method("__init__")
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[Buildings]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting building by id: {id}")
        return self.repository.get_by_id(id)
    
    def get_by_code(self, code: str) -> Optional[Buildings]:
        logging.add_inside_method("get_by_code")
        logging.info(f"Getting building by code: {code}")
        return self.repository.get_by_code(code)
    
    def get_all(self) -> List[Buildings]:
        logging.add_inside_method("get_all")
        logging.info("Getting all buildings")
        return self.repository.get_all()
    
    def get_by_condominium_id(self, condominium_id: int) -> List[Buildings]:
        logging.add_inside_method("get_by_condominium_id")
        logging.info(f"Getting buildings by condominium_id: {condominium_id}")
        return self.repository.get_by_condominium_id(condominium_id)
