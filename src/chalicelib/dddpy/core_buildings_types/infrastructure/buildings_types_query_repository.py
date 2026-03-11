from typing import Optional, List
from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
from chalicelib.dddpy.core_buildings_types.domain.buildings_types_repository import BuildingsTypesQueryRepository
from chalicelib.dddpy.core_buildings_types.infrastructure.buildings_types import DBBuildingsTypes
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("buildings_types_query_repository")


class BuildingsTypesQueryRepositoryImpl(BuildingsTypesQueryRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("BuildingsTypesQueryRepositoryImpl initialized")
    
    def get_by_id(self, id: int) -> Optional[BuildingsTypes]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting building type by id: {id}")
        
        with session_scope() as session:
            db_building_type = session.query(DBBuildingsTypes).filter(DBBuildingsTypes.id == id).first()
            if db_building_type:
                return BuildingsTypes.from_db(db_building_type)
            return None
    
    def get_by_code(self, code: str) -> Optional[BuildingsTypes]:
        logging.add_inside_method("get_by_code")
        logging.info(f"Getting building type by code: {code}")
        
        with session_scope() as session:
            db_building_type = session.query(DBBuildingsTypes).filter(DBBuildingsTypes.code == code).first()
            if db_building_type:
                return BuildingsTypes.from_db(db_building_type)
            return None
    
    def get_all(self) -> List[BuildingsTypes]:
        logging.add_inside_method("get_all")
        logging.info("Getting all building types")
        
        with session_scope() as session:
            db_building_types = session.query(DBBuildingsTypes).all()
            return [BuildingsTypes.from_db(db) for db in db_building_types]
