from typing import Optional, List
from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
from chalicelib.dddpy.core_unittys_types.domain.unittys_types_repository import UnitysTypesQueryRepository
from chalicelib.dddpy.core_unittys_types.infrastructure.unittys_types import DBUnitysTypes
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("unittys_types_query_repository")


class UnitysTypesQueryRepositoryImpl(UnitysTypesQueryRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("UnitysTypesQueryRepositoryImpl initialized")
    
    def get_by_id(self, id: int) -> Optional[UnitysTypes]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting unity type by id: {id}")
        
        with session_scope() as session:
            db_unity_type = session.query(DBUnitysTypes).filter(DBUnitysTypes.id == id).first()
            if db_unity_type:
                return UnitysTypes.from_db(db_unity_type)
            return None
    
    def get_by_code(self, code: str) -> Optional[UnitysTypes]:
        logging.add_inside_method("get_by_code")
        logging.info(f"Getting unity type by code: {code}")
        
        with session_scope() as session:
            db_unity_type = session.query(DBUnitysTypes).filter(DBUnitysTypes.code == code).first()
            if db_unity_type:
                return UnitysTypes.from_db(db_unity_type)
            return None
    
    def get_all(self) -> List[UnitysTypes]:
        logging.add_inside_method("get_all")
        logging.info("Getting all unity types")
        
        with session_scope() as session:
            db_unity_types = session.query(DBUnitysTypes).all()
            return [UnitysTypes.from_db(db) for db in db_unity_types]
