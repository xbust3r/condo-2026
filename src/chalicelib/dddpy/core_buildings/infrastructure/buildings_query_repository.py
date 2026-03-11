from typing import Optional, List
from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
from chalicelib.dddpy.core_buildings.domain.buildings_repository import BuildingsQueryRepository
from chalicelib.dddpy.core_buildings.infrastructure.buildings import DBBuildings
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("buildings_query_repository")


class BuildingsQueryRepositoryImpl(BuildingsQueryRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("BuildingsQueryRepositoryImpl initialized")
    
    def get_by_id(self, id: int) -> Optional[Buildings]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting building by id: {id}")
        
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(DBBuildings.id == id).first()
            if db_building:
                return Buildings.from_db(db_building)
            return None
    
    def get_by_code(self, code: str) -> Optional[Buildings]:
        logging.add_inside_method("get_by_code")
        logging.info(f"Getting building by code: {code}")
        
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(DBBuildings.code == code).first()
            if db_building:
                return Buildings.from_db(db_building)
            return None
    
    def get_all(self) -> List[Buildings]:
        logging.add_inside_method("get_all")
        logging.info("Getting all buildings")
        
        with session_scope() as session:
            db_buildings = session.query(DBBuildings).all()
            return [Buildings.from_db(db) for db in db_buildings]
    
    def get_by_condominium_id(self, condominium_id: int) -> List[Buildings]:
        logging.add_inside_method("get_by_condominium_id")
        logging.info(f"Getting buildings by condominium_id: {condominium_id}")
        
        with session_scope() as session:
            db_buildings = session.query(DBBuildings).filter(
                DBBuildings.condominium_id == condominium_id
            ).all()
            return [Buildings.from_db(db) for db in db_buildings]
