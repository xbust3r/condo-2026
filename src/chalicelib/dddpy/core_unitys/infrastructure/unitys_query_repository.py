from typing import Optional, List
from chalicelib.dddpy.core_unitys.domain.unitys import Unitys
from chalicelib.dddpy.core_unitys.domain.unitys_repository import UnitysQueryRepository
from chalicelib.dddpy.core_unitys.infrastructure.unitys import DBUnitys
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("unitys_query_repository")


class UnitysQueryRepositoryImpl(UnitysQueryRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("UnitysQueryRepositoryImpl initialized")
    
    def get_by_id(self, id: int) -> Optional[Unitys]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting unity by id: {id}")
        
        with session_scope() as session:
            db_unity = session.query(DBUnitys).filter(DBUnitys.id == id).first()
            if db_unity:
                return Unitys.from_db(db_unity)
            return None
    
    def get_by_code(self, code: str) -> Optional[Unitys]:
        logging.add_inside_method("get_by_code")
        logging.info(f"Getting unity by code: {code}")
        
        with session_scope() as session:
            db_unity = session.query(DBUnitys).filter(DBUnitys.code == code).first()
            if db_unity:
                return Unitys.from_db(db_unity)
            return None
    
    def get_all(self) -> List[Unitys]:
        logging.add_inside_method("get_all")
        logging.info("Getting all unitys")
        
        with session_scope() as session:
            db_unitys = session.query(DBUnitys).all()
            return [Unitys.from_db(db) for db in db_unitys]
    
    def get_by_building_id(self, building_id: int) -> List[Unitys]:
        logging.add_inside_method("get_by_building_id")
        logging.info(f"Getting unitys by building_id: {building_id}")
        
        with session_scope() as session:
            db_unitys = session.query(DBUnitys).filter(
                DBUnitys.building_id == building_id
            ).all()
            return [Unitys.from_db(db) for db in db_unitys]
