from typing import Optional, List
from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
from chalicelib.dddpy.core_condominiums.domain.condominiums_repository import CondominiumsQueryRepository
from chalicelib.dddpy.core_condominiums.infrastructure.condominiums import DBCondominiums
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("condominiums_query_repository")


class CondominiumsQueryRepositoryImpl(CondominiumsQueryRepository):
    def __init__(self):
        logging.add_inside_method("__init__")
        logging.info("CondominiumsQueryRepositoryImpl initialized")
    
    def get_by_id(self, id: int) -> Optional[Condominiums]:
        logging.add_inside_method("get_by_id")
        logging.info(f"Getting condominium by id: {id}")
        
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(DBCondominiums.id == id).first()
            if db_condominium:
                return Condominiums.from_db(db_condominium)
            return None
    
    def get_by_code(self, code: str) -> Optional[Condominiums]:
        logging.add_inside_method("get_by_code")
        logging.info(f"Getting condominium by code: {code}")
        
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(DBCondominiums.code == code).first()
            if db_condominium:
                return Condominiums.from_db(db_condominium)
            return None
    
    def get_all(self) -> List[Condominiums]:
        logging.add_inside_method("get_all")
        logging.info("Getting all condominiums")
        
        with session_scope() as session:
            db_condominiums = session.query(DBCondominiums).all()
            return [Condominiums.from_db(db) for db in db_condominiums]
